"""
.. module:: clients.socketserver.management.commands.start_socketserver
   :synopsis: This is an admin command to run a socket server on a port for
   local development
"""

import tornadio2
import tornado

from django.core.management.base import BaseCommand
from django.conf import settings

from clients.socketserver.server import UploadSockets


class Command(BaseCommand):

    def __init__(self):
        pass

    def handle(self, *args, **kwargs):
        print 'Starting Server on {0}'.format(settings.SOCKET_PORT)

        UploadRouter = tornadio2.router.TornadioRouter(
            UploadSockets, {'websockets_check': True})

        application = tornado.web.Application(
            UploadRouter.urls,
            socket_io_port=settings.SOCKET_PORT)

        tornadio2.server.SocketServer(application)
