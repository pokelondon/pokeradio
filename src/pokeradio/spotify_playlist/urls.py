"""
.. module:: pokeradio.spotify_playlist.urls
   :synopsis: URLs for the playlist
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$',
        TemplateView.as_view(template_name='spotify_playlist/index.html'),
        name='index'),
    url(r'^auth/$', 'authorize', name='authorize'),
    url(r'^oauth_callback/$', 'oauth_callback', name='oauth_callback'),
]
urlpatterns += patterns('pokeradio.spotify_playlist.views', *urls)

