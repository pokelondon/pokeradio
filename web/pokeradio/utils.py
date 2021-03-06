"""
.. module:: pokeradio.utils
   :synopsis: Common utility helper functions.
"""

from django.conf import settings
from itertools import chain
from pokeradio.models import Track


def debug_toolbar_callback(request):
    return settings.DEBUG


def current_playlist():
    tracks_new = Track.objects.filter(played__exact=False).prefetch_related('point_set').select_related('user')
    tracks_played = Track.objects.filter(played__exact=True).prefetch_related('point_set').select_related('user').reverse()[:1]

    tracks = list(chain(tracks_played, tracks_new))
    output = [track.to_dict() for track in tracks]
    return output
