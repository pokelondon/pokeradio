from os import stat

import requests
import spotipy
from PIL import Image
from StringIO import StringIO

from django.http import Http404
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

    r = requests.get(url)

    if 200 != r.status_code:
        return Http404()

    image = Image.open(StringIO(r.content))
    response = HttpResponse(content_type="image/jpg")
    image.save(response, 'JPEG')
    return response
