from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect

from pokeradio.albumart.tasks import get_image_url
from pokeradio.tasks import create_image


def image(request, *args, **kwargs):
    """
    if NGINX fails to find a jpg it is then routed to django
    to fetch the image from musicbrainz
    """

    response = HttpResponse(mimetype="image/jpg")
    code = kwargs.get('code')
    output_file = code
    try:
        image_url =  get_image_url(code)
        image, fsize  = create_image(image_url, output_file,
                                    settings.ALBUM_ART_BASE_DIR,
                                    settings.THUMBNAIL_SIZE)
    except Http404:
        return HttpResponseRedirect(settings.ALBUM_ART_FALLBACK)
    else:
        image.save(response, 'JPEG')
        response['Content-Length'] = fsize
        return response
