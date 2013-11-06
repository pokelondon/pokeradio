from django.conf import settings
import requests
import musicbrainzngs
from PIL import Image
from os.path import join
from StringIO import StringIO
from os import stat

musicbrainzngs.set_useragent('pokeradio', '0.1', 'developers@pokelondon.com')

OUTPUT_BASE_DIR = join(settings.MEDIA_ROOT, 'albumart', 'spotify')

def get_image_url(mediatype, code):
	url = settings.SPOTIFY_LOOKUP_ENDPOINT.format('%s:%s' % (mediatype, code))
	try:
		r = requests.get(url)
	except requests.exceptions.HTTPError:
		pass
		#return default

	spotify_meta = r.json().get(mediatype)
	spotify_meta.get('external-ids')
	ids = spotify_meta.get('external-ids')
	artist = spotify_meta.get('artist')
	release = spotify_meta.get('name')
	barcode = ids[0].get('id')
	imageurl = musicbrainz_get_image(barcode=barcode, artistname=artist, release=release)
	return imageurl

def musicbrainz_get_image(barcode, artistname, release):
	
	m = musicbrainzngs.search_releases(
		barcode=barcode,
		artistname=artistname,
		release=release
		).get('release-list', 0)
	id = m[0].get('release-group').get('id')
	url  = settings.COVERART_ENDPOINT.format(id)
	r = requests.get(url)
	imagejson =  r.json()

	return imagejson['images'][0]['thumbnails']['small']

def create_image(imageurl, output_file):

	output_dir = join(OUTPUT_BASE_DIR, output_file)
	r = requests.get(imageurl)
	image = Image.open(StringIO(r.content))
	image.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
	output_file = ('%s.jpg' % output_dir)
	image.save(output_file)
	statinfo = stat(output_file)

	return (image, statinfo.st_size)