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

    # Redirects to the tracks votes archive for the current week
    url(r'^votes/(?P<who>(all|me))/tracks/$', 'vote_tracks_index',
        name='vote_tracks_index'),

    # Redirects to the artists votes archive for the current week
    url(r'^votes/(?P<who>(all|me))/artists/$', 'vote_artists_index',
        name='vote_artists_index'),

    # Weekly track archive
    url(r'^(?P<who>(all|me))/choons/(?P<year>\d{4})/(?P<week>\d+)/$',
        'play_archive_tracks', name='play_archive_tracks'),

    # Weekly artist archive
    url(r'^(?P<who>(all|me))/artists/(?P<year>\d{4})/(?P<week>\d+)/$',
        'play_archive_artists', name='play_archive_artists'),

    # Weekly best voted tracks archive
    url(r'^votes/(?P<who>(all|me))/choons/(?P<year>\d{4})/(?P<week>\d+)/$',
        'vote_archive_tracks', name='vote_archive_tracks'),

    # Weekly best voted artists archive
    url(r'^votes/(?P<who>(all|me))/artists/(?P<year>\d{4})/(?P<week>\d+)/$',
        'vote_archive_artists', name='vote_archive_artists'),
]
urlpatterns += patterns('pokeradio.history.views', *urls)

