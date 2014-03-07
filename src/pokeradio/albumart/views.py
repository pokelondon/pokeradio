from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect

from pokeradio.albumart.tasks import get_image_url
from pokeradio.tasks import create_image

from pokeradio.history.models import ArchiveTrack


def image(request, code, *args, **kwargs):
    """
    if NGINX fails to find a jpg it is then routed to django
    to fetch the image from musicbrainz
    """

    response = HttpResponse(mimetype="image/jpg")
    try:
        image_url =  get_image_url(code)
        image, fsize  = create_image(image_url, code,
                                     settings.ALBUM_ART_BASE_DIR,
                                     settings.THUMBNAIL_SIZE)
    except Http404:
        # Mark tracks as not having an image (for speed)
        res = ArchiveTrack.objects.by_album_code(code=code).update(
                no_artwork=True)
        print 'No artwork for', res, 'items', code
        return HttpResponseRedirect(settings.ALBUM_ART_FALLBACK)
    else:
        image.save(response, 'JPEG')
        response['Content-Length'] = fsize
        return response
