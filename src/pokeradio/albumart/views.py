from django.conf import settings
from pokeradio.albumart.tasks import get_image_url
from pokeradio.tasks import create_image
from django.http import HttpResponse
from os.path import join



def image(request, *args, **kwargs):
	"""
	if NGINX fails to find a jpg it is then routed to django
	to fetch the image from musicbrainz
	"""
	
	response = HttpResponse(mimetype="image/jpg")
	mediatype = kwargs.get('mediatype')
	code = kwargs.get('code')
	output_file = join(mediatype, code)
	image_url =  get_image_url(mediatype, code)
	image, fsize  = create_image(image_url, output_file, settings.ALBUM_ART_BASE_DIR, settings.THUMBNAIL_SIZE )
	image.save(response,'JPEG')
	response['Content-Length'] = fsize
	return response






	

