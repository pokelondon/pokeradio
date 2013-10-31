"""
.. module:: clients.socketserver.management.commands.start_socketserver
   :synopsis: This is an admin command to run a socket server on a port for
   local development
"""

import tornado
from tornadio2 import router, server
from django.core.management.base import BaseCommand
from django.conf import settings

from pokeradio.socketserver.server import RouterConnection


class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        Router = router.TornadioRouter(RouterConnection,
                                         {'websockets_check': True})
        app = tornado.web.Application(Router.urls)

        server.SocketServer(app)

