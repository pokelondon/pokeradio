from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
	'',
	url(r'^create/albumart/(?P<code>\w+).jpg$',
		'pokeradio.albumart.views.image', name='getimage'),
)