import json

import pusher

from django.conf import settings


if settings.PUSHER_APP_ID:
    p = pusher.Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET
    )

def track_played_pusher(track):
    if not p:
        return
    data = json.dumps({
        'action': 'playing',
        'id': track.pk,
        'href': track.href,
        'track': track.name,
        'artist': track.artist,
        'album_href': track.album_href,
        'dj': track.user.get_full_name(),
    })

    p['poke_radio'].trigger('on_playing', data)
