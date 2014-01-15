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
    url(r'^statement/$', 'statement_index', name='statement'),
    url(r'^statement/(?P<year>\d{4})/(?P<week>\d+)/$', 'statement_week',
        name='statement_week'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
