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

    # Redirects to the tracks votes archive for the current week
    url(r'^votes/(?P<who>(all|me))/tracks/$', 'vote_tracks_index',
        name='vote_tracks_index'),

    # Weekly best voted tracks archive
    url(r'^votes/(?P<who>(all|me))/choons/(?P<year>\d{4})/(?P<week>\d+)/$',
        'vote_archive_tracks', name='vote_archive_tracks'),

    url(r'^track/(?P<pk>\d+)/$', 'track_detail', name='track_detail'),

]
urlpatterns += patterns('pokeradio.history.views', *urls)

