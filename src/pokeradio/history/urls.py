"""
.. module:: pokeradio.history.urls
   :synopsis: URLs for the history app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$', 'week_index', name='week_index'),
    url(r'^week/(?P<year>\d{4})/(?P<week>\d+)/$', 'play_archive_week',
        name='play_archive_week'),
]
urlpatterns += patterns('pokeradio.history.views', *urls)

