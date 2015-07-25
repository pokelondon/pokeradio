"""
.. module:: pokeradio.urls
   :synopsis: Root URL patterns.
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()
urlpatterns = patterns('')

# Development URL Patterns Only - For example 404 / 500 Page Previews
if settings.DEBUG:
    urls = [
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
        (r'^500/$', TemplateView.as_view(template_name="500.html")),
    ]
    urlpatterns += patterns('', *urls)
    urlpatterns += staticfiles_urlpatterns()

# Root Patterns
urls = [
    url(r'^$', 'pokeradio.views.home', name='home'),

    (r'^admin/', include(admin.site.urls)),
    (r'^scoring/', include('pokeradio.scoring.urls', namespace='scoring')),
    (r'^history/', include('pokeradio.history.urls', namespace='history')),
    (r'^albumart/', include('pokeradio.albumart.urls', namespace='albumart')),
    (r'^api/', include('pokeradio.api.urls', namespace='api')),
    (r'^spotify/', include('pokeradio.spotify_playlist.urls',
        namespace='spotify_playlist')),
    (r'^accounts/', include('pokeradio.accounts.urls', namespace='accounts')),
    (r'^registration/', include('registration.backends.default.urls')),

    (r'^monitor/$', TemplateView.as_view(template_name="pokeradiomon.html")),
]
urlpatterns += patterns('', *urls)
