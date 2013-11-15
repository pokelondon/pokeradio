import tornado
from tornadio2 import SocketConnection
import simplejson as json
import brukva
from tornadio2 import event, router, server
from helper import TrackList
import logging
from django.conf import settings
logger = logging.getLogger()


class PlayerConnection(SocketConnection):
    """ Mopidy Endpoint """
    
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
        print 'started playing'
       
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
        self.tracklist = TrackList()

    def on_open(self, request):
        print 'app connected'
        self.client.listen(self.on_redis_message)
    

    def on_redis_message(self, data):
        if data.channel == 'player_update':
            self.emit('playlist:progress', data.body)
        else:
            self.emit('playlist:update', data.body)
        
    
    @event('add_track')
    def do_add_track(self, new_track):
        user_id = self.session.info.get_cookie('poke_radio_user_id').value
        new_track = json.loads(new_track)
        self.tracklist.add(user_id, new_track)
    
    def on_close(self):
        self.client.unsubscribe('playlist')
    
    @event('playlist')
    def playlist(self, command):
        print command
        if command == 'fetch':
            self.emit('playlist:fetch',self.tracklist.get_playlist())



class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                    '/app':AppConnection}

    def on_open(self, request):
        pass



Router = router.TornadioRouter(RouterConnection,
                                         {'websockets_check': True})

app = tornado.web.Application(
    Router.urls,
    socket_io_port=settings.SOCKET_PORT)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
