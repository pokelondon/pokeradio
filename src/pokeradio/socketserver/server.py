import logging
import tornado
import brukva
import simplejson as json
from itertools import chain
from tornadio2 import SocketConnection
from tornadio2 import event, router, server

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from pokeradio.models import Track

from .utils import flush_transaction


logger = logging.getLogger()


class PlayerConnection(SocketConnection):
    """ Socket connection for Mopidy client to connect to
    Bridged to browser connections via Redis PubSub
    """

    def __init__(self, *args, **kwargs):
        super(PlayerConnection, self).__init__(*args, **kwargs)
        self.client = brukva.Client(host=settings.REDIS_HOST,
                                    port=settings.REDIS_PORT,
                                    selected_db=settings.REDIS_DB)
        self.client.connect()

    def on_open(self, request):
        print 'Mopidy Connected'

    @event('request_track')
    def on_request_track(self, message=None):
        """ Mopidy wants a track to play
        Find the next track in the playlist
        """
        flush_transaction()
        try:
            track = Track.objects.filter(played__exact=False)[:1][0]
        except IndexError:
            pass
        else:
            payload = json.dumps({'id': track.id, 'href': track.href})
            self.emit('mopidy_play_track', payload)

    @event('track_playback_ended')
    def on_track_playback_ended(self, href):
       """ Track complete. Mark it as played in the DB and request the next one
       """
       try:
           track = Track.objects.get(href=href)
           track.played = True
           track.save()
       except Track.DoesNotExist:
           pass

       self.on_request_track()

    @event('track_playback_started')
    def on_track_playlist_started(self, data):
        print 'started playing', data

    @event('player_update')
    def on_player_update(self, data):
        """ Player state change, pass message onto redis channel
        """
        self.client.publish('player_update', data)


class AppConnection(SocketConnection):
    """ Instances of this class represent connections to the browsers via
    websocket. Connection to the player socket server is via redis
    """
    def __init__(self, *args, **kwargs):
        super(AppConnection, self).__init__(*args, **kwargs)
        # Connect to redis to recieve messages from the other socket server
        self.client = brukva.Client(host=settings.REDIS_HOST,
                                    port=settings.REDIS_PORT,
                                    selected_db=settings.REDIS_DB)
        self.client.connect()
        self.client.subscribe('playlist')
        self.client.subscribe('player_update')
        self.client.subscribe('deleted')

    def on_open(self, request):
        """ Websocket connection opened with the browser
        """
        session_key = request.get_cookie('sessionid').value
        try:
            session = Session.objects.get(session_key=session_key)
        except session.DoesNotExist:
            print 'Session expired'
        else:
            user_id = session.get_decoded().get('_auth_user_id')
            self.user_id = user_id
            self.user = User.objects.get(pk=self.user_id)
            print 'Webapp connected:', self.user
            self.client.listen(self.on_redis_message)

    def on_redis_message(self, data):
        """ Player events, emit them back down to the browsers
        """
        if data.channel == 'player_update':
            self.emit('playlist:progress', data.body)
        if data.channel == 'deleted':
            self.emit('playlist:deleted', data.body);
        else:
            self.emit('playlist:update', data.body)

    @event('add_track')
    def do_add_track(self, data):
        """ Save the new track to the playlist
        """
        data = json.loads(data)
        track_data = data
        track_data['album_href'] = track_data.pop('album').get('href')
        track_data['user_id'] = self.user_id
        t = Track.objects.create(**data)
        print '{0} has queued {1}'.format(self.user, t)


    @event('remove_track')
    def do_remove_track(self, track_id):
        try:
            track = Track.objects.get(user=self.user, id=int(track_id),
                                      played=False)
        except Track.DoesNotExist:
            print 'Track not in playlist'
            self.emit('playlist:message', 'You cant do that')
        else:
            self.emit('playlist:message', '{0} deleted'.format(track))
            track.delete()

    def on_close(self):
        self.client.unsubscribe('playlist')
        self.client.unsubscribe('player_update')
        self.client.unsubscribe('deleted')

    @event('fetch_playlist')
    def playlist(self):
        """ Get all tracks in the playlist to bootstrap the view
        """
        # Ensure new data is retrieved, incase another process has changed
        # the playlist
        flush_transaction()
        tracks_new = Track.objects.filter(played__exact=False)
        tracks_played = Track.objects.filter(played__exact=True).reverse()[:3]
        tracks = list(chain(tracks_played, tracks_new))
        output = [track.to_dict() for track in tracks]
        self.emit('playlist:load', json.dumps(output))



class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                     '/app':AppConnection}


Router = router.TornadioRouter(RouterConnection, {'websockets_check': True})

app = tornado.web.Application(Router.urls, socket_io_port=settings.SOCKET_PORT)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
