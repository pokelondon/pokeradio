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
    url(r'^disco-biscuits/$', 'statement_index', name='statement'),
    url(r'^disco-biscuits/(?P<year>\d{4})/(?P<week>\d+)/$', 'statement_week',
        name='statement_week'),
    url(r'^fake-internet-points/$', 'points_index', name='points'),
    url(r'^fake-internet-points/(?P<year>\d{4})/(?P<week>\d+)/$', 'points_week',
        name='points_week'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
