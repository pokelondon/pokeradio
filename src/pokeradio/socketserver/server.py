import redis
import logging
import tornado
import tornadoredis
import simplejson as json
import tornado.gen

from datetime import datetime
from itertools import chain
from tornadio2 import SocketConnection
from tornadio2 import event, router, server, gen
from raven import Client
from raven.middleware import Sentry

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db import IntegrityError

from pokeradio.models import Track, Point
from pokeradio.history.utils import record_track_play, get_or_create_track

from .utils import flush_transaction


logger = logging.getLogger('socketserver')


class PlayerConnection(SocketConnection):
    """ Socket connection for Mopidy client to connect to
    Bridged to browser connections via Redis PubSub
    """

    waiting_for_more_tracks = False
    CHANNELS = ['pr:track_add', ]

    def __init__(self, *args, **kwargs):
        super(PlayerConnection, self).__init__(*args, **kwargs)

        self.connection_pool = tornadoredis.connection.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT)
        self.client = tornadoredis.Client(connection_pool=self.connection_pool,
                                          selected_db=settings.REDIS_DB)
        self.listen()

    @gen.engine
    def listen(self):
        self.client.connect()
        yield gen.Task(self.client.subscribe, self.CHANNELS)
        self.client.listen(self.on_redis_message)

    def on_open(self, request):
        logger.info('Mopidy Connected via websocket')

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe(self.CHANNELS)
            self.client.disconnect()

    @event('request_track')
    def on_request_track(self, message=None):
        """ Mopidy wants a track to play
        Find the next track in the playlist
        """
        flush_transaction()
        try:
            track = Track.objects.filter(played__exact=False)[:1][0]
        except IndexError:
            logger.warn('No Track to play')
            self.waiting_for_more_tracks = True
        else:
            self.waiting_for_more_tracks = False
            payload = json.dumps({'id': track.id, 'href': track.href})
            self.emit('mopidy_play_track', payload)

            # Save to archive and count play
            record_track_play(track)

    @event('track_playback_started')
    def on_track_playback_started(self, href):
        # TODO Mark track as playing in DB
        pass

    @event('track_playback_ended')
    def on_track_playback_ended(self, href):
       """ Track complete. Mark it as played in the DB and request the next one
       """
       try:
           track = Track.objects.filter(href=href, played=False)[0]
           track.set_played()
       except (Track.DoesNotExist, IndexError):
           pass

       self.on_request_track()

    @event('player_update')
    def on_player_update(self, data):
        """ Player state change, pass message onto redis channel
        """
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.publish('pr:progress', data)

    def on_new_track(self):
        """ Message from ORM, a track has been added.
        Use this to kick mopidy if the playlist has been empty
        """
        if self.waiting_for_more_tracks:
            logger.info('Restarting from empty playlist')
            self.on_request_track()

    def on_redis_message(self, data):
        if data.kind == 'message':
            if data.channel == 'pr:track_add':
                self.on_new_track()


class AppConnection(SocketConnection):
    """ Instances of this class represent connections to the browsers via
    websocket. Connection to the player socket server is via redis
    """
    CHANNELS = ['pr:track_add', 'pr:track_delete', 'pr:progress']

    def __init__(self, *args, **kwargs):
        super(AppConnection, self).__init__(*args, **kwargs)
        self.connection_pool = tornadoredis.connection.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT)
        self.client = tornadoredis.Client(connection_pool=self.connection_pool,
                                          selected_db=settings.REDIS_DB)
        self.listen()

    @gen.engine
    def listen(self):
        self.client.connect()
        yield gen.Task(self.client.subscribe, self.CHANNELS)
        self.client.listen(self.on_redis_message)

    def _get_user_id(self, request):
        """ Get the user ID from the session and save it to the connection
        instance
        """
        flush_transaction()

        try:
            cookie = request.get_cookie('sessionid')
            session_key = cookie.value
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            logger.error('Session expired', exc_info=True,
                    extra={'session_key': session_key})
            return False
        except AttributeError:
            logger.error('No Cookie Found')
            return False
        else:
            user_id = session.get_decoded().get('_auth_user_id')
            self.user_id = user_id
            self.user = User.objects.get(pk=self.user_id)
            self.session_expire = session.expire_date
            logger.debug('Webapp connected', exc_info=True,
                    extra={'user': self.user, 'expires': self.session_expire})
            return True

    def on_open(self, request):
        """ Websocket connection opened with the browser
        """
        #self.client.listen(self.on_redis_message)
        return self._get_user_id(request)


    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe(self.CHANNELS)
            self.client.disconnect()


    def on_redis_message(self, data):
        """ Player events, emit them back down to the browsers
        """
        if data.kind == 'message':
            if data.channel == 'pr:track_delete':
                self.emit('playlist:deleted', data.body);

            if data.channel == 'pr:progress':
                if 'percentage' in data.body:
                    self.emit('playlist:progress', data.body)

            if data.channel == 'pr:track_add':
                self.emit('playlist:update', data.body)

    def check_expiry(self):
        """ Check the session hasnt expired before doing any events
        """
        now = datetime.now()
        if self.session_expire < now:
            self.emit('playlist:expired')
            return True
        return False

    @event('add_track')
    def do_add_track(self, rawdata):
        """ Save the new track to the playlist
        """
        if self.check_expiry():
            return
        data = json.loads(rawdata)
        data['album_href'] = data.pop('album').get('href')
        data['user_id'] = self.user_id
        t = Track.objects.create(**data)

        logger.debug('{0} has queued {1}'.format(self.user, t))


    @event('remove_track')
    def do_remove_track(self, track_id):
        if self.check_expiry():
            return
        try:
            # TODO Check that this isnt the first unplayed track in the playlist
            # as this could mean that its playing now.
            track = Track.objects.get(user=self.user, id=int(track_id),
                                      played=False)
        except Track.DoesNotExist:
            logger.warn('Delete: Track not in playlist')
            self.emit('playlist:message', 'You cant do that')
        else:
            self.emit('playlist:message', '{0} deleted'.format(track))
            track.delete()

    @event('fetch_playlist')
    def playlist(self):
        """ Get all tracks in the playlist to bootstrap the view
        """
        if self.check_expiry():
            return
        # Ensure new data is retrieved, incase another process has changed
        # the playlist
        flush_transaction()
        tracks_new = Track.objects.filter(played__exact=False)
        tracks_played = Track.objects.filter(played__exact=True).reverse()[:3]
        tracks = list(chain(tracks_played, tracks_new))
        output = [track.to_dict() for track in tracks]
        self.emit('playlist:load', json.dumps(output))

    @event('like_track')
    def like_track(self, track_id):
        if self.check_expiry():
            return
        self.value_judgement(track_id, Point.TRACK_LIKED)

    @event('dislike_track')
    def dislike_track(self, track_id):
        if self.check_expiry():
            return
        self.value_judgement(track_id, Point.TRACK_DISLIKED)

    def value_judgement(self, track_id, action):
        """ Checking various integrity constraints, record a like or dislike
        from a user, for another user against a playlist track item
        """
        # Score a point to the user
        try:
            # Get the track being liked, but not if its queued by the
            # current user
            track = Track.objects.exclude(user=self.user).get(id=int(track_id))
        except Track.DoesNotExist:
            self.emit('playlist:message', 'You cant do that')
        else:
            try:
                archive_track = get_or_create_track(track)
                # Make a point, but catch the exception raised by the
                # violation of unique_togetherness of (playlist) track and voter
                p = Point.objects.create(user=track.user, action=action,
                                         track_name=str(track)[:100],
                                         playlist_track=track,
                                         archive_track=archive_track,
                                         vote_from=self.user)
            except IntegrityError:
                # User has already voted for this track
                self.emit('playlist:message',
                          'Thanks, you appear to have already voiced an '\
                          'opinion on {0}\'s choice to play {1}'
                          .format(track.user.first_name, track))
            else:
                return True


class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                     '/app': AppConnection}


Router = router.TornadioRouter(RouterConnection, {'websockets_check': True})

tornado_app = tornado.web.Application(Router.urls,
                                      socket_io_port=settings.SOCKET_PORT)

if hasattr(settings, 'DSN'):
    client = Client(settings.DSN.replace('udp', 'http'))
    app = Sentry(tornado_app, client=client)
else:
    app = tornado_app


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
