"""
.. module:: clients.socketserver.run
   :synopsis: This is the server app that is used by Gunicorn in production
"""

import tornadio2
import tornado

from pokeradio.socketserver.server import RouterConnection


Router = tornadio2.router.TornadioRouter(RouterConnection,
                                         {'websockets_check': True})

app = tornado.web.Application(Router.urls)
