"""
.. module:: pokeradio.api.urls
   :synopsis: URLs for the API app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    # Voting endpoint
    url(r'^vote/$', 'vote', name='vote'),
    url(r'^playlist/$', 'playlist', name='playlist'),
    url(r'^playlist/(?P<pk>\d+)$', 'playlist_track', name='playlist_track'),
]
urlpatterns += patterns('pokeradio.api.views', *urls)
