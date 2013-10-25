import tornado
from tornadio2 import SocketConnection
import simplejson as json
import logging
import brukva
from tornado.web import RequestHandler
from django.conf import settings
from tornadio2 import event, router, server
#from clients.store.models import Asset, get_or_create_asset_type
from pokeradio.models import Track
from importlib import import_module
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.core import serializers

logger = logging.getLogger()

class TrackList:

    def __init__(self):
        pass


    def add(self, sessionid, new_track):
        user_id = self.get_user(sessionid)
        user = User.objects.get(pk=user_id)
        track = Track()
        track.name = new_track['name']
        track.artist = new_track['artist']
        track.href = new_track['href']
        track.user = user

        try:
            track.save()
            return True
        except IntegrityError, error:
            logger.error('Some thing has gone wrong %s' % error.message)
        
        return False

    def get_user(self, sessionid):
        """ Exception handerling required """
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        s = SessionStore(session_key = sessionid)
        return s.get(SESSION_KEY)
    
    @classmethod
    def get_mopidy_track(self, href = None):
        if href == None:
            track = Track.objects.filter(played__exact = False)[0]
            return json.dumps({ 'id' : track.id, 'href' : track.href })
        else:
            return Track.objects.filter(Q(played__exact = False),Q(href__exact=href))[0]    

    def set_played(self,href, played=True):
        """ href is single string """
        track = self.get_mopidy_track(href)
        track.played = played
        track.save()
    
    def get_playlist(self):
        tracks = Track.objects.filter(played__exact = False)
        return serializers.serialize('json', tracks)




class PlayerConnection(SocketConnection):
    """ Mopidy Endpoint """

    def on_open(self, request):
        print 'mopidy connected'
    
    @event('request_track')
    def on_request_track(self, message):
        track_payload = TrackList.get_mopidy_track() 
        self.emit('mopidy_play_track', track_payload)

   
    @event('track_playback_ended')
    def on_track_playback_started(self, href):
       print 'ended'
       tracklist = TrackList() 
       tracklist.set_played(href)



class AppConnection(SocketConnection):
    """ App Endpoint
    """
    def __init__(self, *args, **kwargs):
        """ Create a connection to the redis pubsub channel for this client """
        super(AppConnection, self).__init__(*args, **kwargs)
        self.client = brukva.Client(host='localhost', port=6379, selected_db=0)
        self.client.connect()
        self.client.subscribe('playlist_changed')
        self.tracklist = TrackList()

    def on_open(self, request):
        print 'app connected'
        self.client.listen(self.on_redis_message)
    

    def on_redis_message(self, message):
        self.emit('playlist:update',self.tracklist.get_playlist())
        
    
    @event('add_track')
    def do_add_track(self, new_track):
        sessionid = self.session.info.get_cookie('sessionid').value
        new_track = json.loads(new_track)
        self.tracklist.add(sessionid, new_track)
    
    def on_close(self):
        self.client.unsubscribe('playlist_changed')
    
    @event
    def get_playlist(self):
        self.emit('playlist:update',self.tracklist.get_playlist())



class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                    '/app':AppConnection}

    def on_open(self, request):
        pass



Router = router.TornadioRouter(RouterConnection,
                                         {'websockets_check': True})

app = tornado.web.Application(Router.urls)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
