from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
	'',
	url(r'^albumart/(?P<code>\w+).jpg$',
		'pokeradio.albumart.views.image', name='getimage'),
)