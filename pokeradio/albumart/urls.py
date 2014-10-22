from django.conf.urls import patterns, url

urlpatterns = patterns(
    'pokeradio.albumart.views',
    url(r'^(?P<album_id>\w+).jpg$', 'image', name='getimage'),
)
