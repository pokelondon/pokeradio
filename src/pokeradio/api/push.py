import json

import requests
import pusher

from django.conf import settings


p = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET
)


def dweet(data):
    """ Sends the data in the dict to the standard Dweet name for this app
    """
    data = json.dumps(data)

    headers = {'content-type': 'application/json'}
    try:
        res = requests.post('https://dweet.io:443/dweet/for/{0}'.format(
                settings.DWEET_NAME), data=data, headers=headers)
        return True
    except Exception, e:
        return False


def track_played_dweet(track):
    print 'Dweeting', track

    dweet({
        'action': 'playing',
        'id': track.pk,
        'href': track.href,
        'track': track.name,
        'artist': track.artist,
        'album_href': track.album_href,
        'dj': track.user.get_full_name(),
    })


def track_played_pusher(track):

    print 'Pusher-ing', track

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



