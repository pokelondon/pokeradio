from django.conf.urls import patterns, url

urlpatterns = patterns(
    'pokeradio.albumart.views',
    url(r'^(?P<code>\w+).jpg$', 'image', name='getimage'),
)
