import os
import tornado
from tornadio2 import SocketConnection
import simplejson as json
import logging
import brukva
from tornado.web import RequestHandler
from django.conf import settings
from tornadio2 import event, router, server
#from clients.store.models import Asset, get_or_create_asset_type

logger = logging.getLogger()



class PlayerConnection(SocketConnection):
    """ Mopidy Endpoint
    """
    mopidyConnection = set()

    @classmethod
    def get_players(self):
        return self.mopidyConnection
   
    def on_open(self, request):
        print 'mopidy connected'
        self.mopidyConnection.add(self)
   
    @event
    def track_playback_started(self,message):
       print message
       self.emit('track',message)


class AppConnection(SocketConnection):
    """ App Endpoint
    """
    def on_open(self,request):
        print 'app connected'

    @event
    def open_uri(self,uri):
        for p in PlayerConnection.get_players():
            p.emit('p_open_uri',uri)	


class RouterConnection(SocketConnection):
    __endpoints__ = {'/player': PlayerConnection,
                    '/app':AppConnection}

    def on_open(self,request):
        pass

Router = router.TornadioRouter(RouterConnection,
                                         {'websockets_check': True})

app = tornado.web.Application(Router.urls)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    server = server.SocketServer(app)
