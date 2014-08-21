"""
.. module:: pokeradio.api.urls
   :synopsis: URLs for the API app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    # PokeRadioMon Endpoint
    url(r'^vote/$', 'vote', name='vote'),

    # Endpoints for webapp
    url(r'^playlist/$', 'playlist', name='playlist'),
    url(r'^playlist/(?P<pk>\d+)$', 'playlist_track', name='playlist_track'),

    # Endpoints for mopidy
    url(r'^mopidy/$', 'mopidy', name='mopidy'),
]
urlpatterns += patterns('pokeradio.api.views', *urls)
