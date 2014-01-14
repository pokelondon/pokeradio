"""
.. module:: pokeradio.scoring.urls
   :synopsis: URLs for the scoring app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$', 'index', name='index'),
    url(r'^statement/$', 'point_statement', name='statement'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
