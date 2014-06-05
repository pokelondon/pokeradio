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
]
urlpatterns += patterns('pokeradio.api.views', *urls)
