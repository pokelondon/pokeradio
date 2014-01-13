import logging
import tornado
import brukva
import simplejson as json
from tornadio2 import SocketConnection
from tornadio2 import event, router, server

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from helper import TrackList
from pokeradio.models import Track


logger = logging.getLogger()


class PlayerConnection(SocketConnection):
    """ Socket connection for Mopidy client to connect to
    Bridged to browser connections via Redis PubSub
    """

    def __init__(self, *args, **kwargs):
        super(PlayerConnection, self).__init__(*args, **kwargs)
        self.client = brukva.Client(host='localhost', port=6379, selected_db=0)
        self.client.connect()
        self.tracklist = TrackList()

    def on_open(self, request):
        print 'mopidy connected'

    @event('request_track')
    def on_request_track(self, message=''):
        track_payload = self.tracklist.get_mopidy_track()
        self.emit('mopidy_play_track', track_payload)

    @event('track_playback_ended')
    def on_track_playback_ended(self, href):
       self.tracklist.set_played(href)
       self.on_request_track()

    @event('track_playback_started')
    def on_track_playlist_started(self, data):
        print 'started playing', data

    @event('player_update')
    def on_player_update(self, data):
        self.client.publish('player_update', data)


class AppConnection(SocketConnection):
    """ App Endpoint
    """
    def __init__(self, *args, **kwargs):
        """ Create a connection to the redis pubsub channel for this client """
        super(AppConnection, self).__init__(*args, **kwargs)
        self.client = brukva.Client(host='localhost', port=6379, selected_db=0)
        self.client.connect()
        self.client.subscribe('playlist')
        self.client.subscribe('player_update')

        self.tracklist = TrackList(user_id=None)

    def on_open(self, request):
        session_key = request.get_cookie('sessionid').value
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get('_auth_user_id')
        self.user_id = user_id
        self.user = User.objects.get(pk=self.user_id)
        print 'Webapp connected:', self.user
        self.client.listen(self.on_redis_message)

    def on_redis_message(self, data):
        if data.channel == 'player_update':
            self.emit('playlist:progress', data.body)
        else:
            self.emit('playlist:update', data.body)

    @event('add_track')
    def do_add_track(self, data):
        data = json.loads(data)
        # Create track object
        track_data = data
        track_data['album_href'] = track_data.pop('album').get('href')
        track_data['user_id'] = self.user_id
        t = Track.objects.create(**data)


    @event('remove_track')
    def do_remove_track(self, track_id):
        try:
            track = Track.objects.get(user=self.user, id=int(track_id),
                                      played=False)
        except Track.DoesNotExist:
            print 'Track not in playlist'
            # TODO Send a message to the frontend
        else:
            track.delete()

    def on_close(self):
        self.client.unsubscribe('playlist')

    @event('fetch_playlist')
    def playlist(self):
        playlist = self.tracklist.get_playlist()
        self.emit('playlist:load', playlist)



class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                     '/app':AppConnection}

    def on_open(self, request):
        pass



Router = router.TornadioRouter(RouterConnection, {'websockets_check': True})

app = tornado.web.Application(Router.urls, socket_io_port=settings.SOCKET_PORT)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
