import spotipy

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect

from pokeradio.tasks import create_image

from pokeradio.history.models import ArchiveTrack

sp = spotipy.Spotify()


def image(request, album_id, *args, **kwargs):
    """
    if NGINX fails to find a jpg it is then routed to django
    to fetch the image from spotify
    """
    full_album_id = 'spotify:album:{0}'.format(album_id)

    res = sp.album(full_album_id)
    try:
        url = res['images'][-1]['url']
    except KeyError:
        return HttpResponseRedirect(settings.ALBUM_ART_FALLBACK)

    response = HttpResponse(mimetype="image/jpg")

    try:
        image, fsize  = create_image(url, album_id,
                                     settings.ALBUM_ART_BASE_DIR,
                                     settings.THUMBNAIL_SIZE)
    except Http404:
        # Mark tracks as not having an image (for speed)
        res = ArchiveTrack.objects.get(album_href=full_album_id).update(
                no_artwork=True)
        print 'No artwork for', res, 'items', full_album_id
        return HttpResponseRedirect(settings.ALBUM_ART_FALLBACK)
    else:
        image.save(response, 'JPEG')
        response['Content-Length'] = fsize
        return response
