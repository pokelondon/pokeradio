import requests
import musicbrainzngs
import logging

from django.conf import settings
from django.http import Http404

logger = logging.getLogger()

musicbrainzngs.set_useragent('pokeradio', '0.1', 'developers@pokelondon.com')


def get_image_url(code):
    """ Using spoitfy API, find release information, then use it to
    query MusicBrainz for album artwork
    """
    # Query spotify for album metadata
    url = settings.SPOTIFY_LOOKUP_ENDPOINT.format(code)
    try:
        r = requests.get(url)
    except requests.exceptions.HTTPError:
        raise Http404()

    spotify_meta = r.json().get('album')
    spotify_meta.get('external-ids')
    ids = spotify_meta.get('external-ids')
    artist = spotify_meta.get('artist')
    release = spotify_meta.get('name')
    barcode = ids[0].get('id')
    print barcode, artist, release
    imageurl = musicbrainz_get_image(barcode=barcode, artistname=artist,
                                     release=release)
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

    if 404 == r.status_code:
        raise Http404()

    imagejson = r.json()
    return imagejson['images'][0]['thumbnails']['small']
