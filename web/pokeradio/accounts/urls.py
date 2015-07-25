"""
.. module:: pokeradio.accounts.urls
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^logout/$', 'pokeradio.accounts.views.logout_view', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^profile/$', 'pokeradio.accounts.views.edit_profile',
        name='edit_profile'),
]

urlpatterns += patterns('', *urls)

