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

    # Points
    url(r'^fake-internet-points/$', 'points_index', name='points_index'),
    url(r'^fake-internet-points/(?P<year>\d{4})/(?P<week>\d+)/$', 'points_week',
        name='points_week'),

    # Leaderboard
    url(r'^playas/$', 'leaderboard_index', name='leaderboard_index'),
    url(r'^playas/(?P<year>\d{4})/(?P<week>\d+)/$', 'leaderboard',
        name='leaderboard'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
