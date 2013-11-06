from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
	'',
	url(r'^albumart/spotify/(?P<mediatype>\w+)/(?P<code>\w+).jpg$',
		'pokeradio.albumart.views.image', name='getimage'),
)