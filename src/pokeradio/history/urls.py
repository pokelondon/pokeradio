"""
.. module:: pokeradio.history.urls
   :synopsis: URLs for the history app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
urlpatterns += patterns('pokeradio.history.views', *urls)

