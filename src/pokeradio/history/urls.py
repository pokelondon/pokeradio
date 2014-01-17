"""
.. module:: pokeradio.history.urls
   :synopsis: URLs for the history app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$', 'index', name='index'),

    # Redirects to the archive for the current week
    url(r'^(?P<who>(all|me))/(?P<archive>(artists|tracks))$', 'week_index',
        name='week_index'),

    # Weekly track archive
    url(r'^(?P<who>(all|me))/tracks/(?P<year>\d{4})/(?P<week>\d+)/$',
        'play_archive_tracks', name='play_archive_tracks'),

    # Weekly artist archive
    url(r'^(?P<who>(all|me))/artists/(?P<year>\d{4})/(?P<week>\d+)/$',
        'play_archive_artists', name='play_archive_artists'),
]
urlpatterns += patterns('pokeradio.history.views', *urls)
