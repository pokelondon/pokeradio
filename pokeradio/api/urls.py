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

    # App Endpoints
    url(r'^identify/$', 'identify', name='identify'),

    # Endpoints for webapp
    url(r'^playlist/$', 'playlist', name='playlist'),
    url(r'^playlist/(?P<pk>\d+)$', 'playlist_track', name='playlist_track'),
    url(r'^badges/(?P<user_id>\d+)/$', 'badges', name='badges'),

    # Endpoints for mopidy
    url(r'^mopidy/$', 'mopidy', name='mopidy'),
]
urlpatterns += patterns('pokeradio.api.views', *urls)

v2_urls = [
    url(r'^v2/playlist/$', 'playlist'),
    url(r'^v2/playlist/(?P<pk>\d+)/$', 'playlist_detail'),
    url(r'^v2/identify/$', 'identify'),
]
urlpatterns += patterns('pokeradio.api.v2_views', *v2_urls)
