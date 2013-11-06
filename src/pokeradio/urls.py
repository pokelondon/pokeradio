"""
.. module:: pokeradio.urls
   :synopsis: Root URL patterns.
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
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

# Root Patterns
urls = [
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pokeradio.views.home', name='home'),
    url(r'^login/$','pokeradio.accounts.views.login_view',name='login'),
    url(r'^logout/$','pokeradio.accounts.views.logout_view',name='logout'),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('pokeradio.albumart.urls'))

]
urlpatterns = patterns('', *urls)