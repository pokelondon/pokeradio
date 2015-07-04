from __future__ import unicode_literals

import simplejson as json

import redis
import spotipy
from emitter import Emitter

from django.conf import settings

from pokeradio.tasks import trigger_badge_add_task
from pokeradio.channels import CHANNEL_ADD


io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT,
    'db': settings.REDIS_DB, 'password': settings.REDIS_PASSWORD})

r_conn = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT,
                           db=settings.REDIS_DB)

sp = spotipy.Spotify()


def badge_saved(sender, instance, created, **kwargs):

    if created:
         io.Of('/app').Emit('badge:add', str(instance.user_id))



def track_saved(sender, instance, created, **kwargs):
    if created:
        try:
            track = sp.track(instance.href)
        except spotipy.SpotifyException:
            instance.delete()
            raise Http404()
        else:
            instance.name = track['name']
            instance.artist = track['artists'][0]['name']
            instance.artist_href = track['artists'][0]['uri']
            instance.album_href = track['album']['uri']
            instance.length = int(track['duration_ms']) / 1000
            instance.save(update_fields=['name', 'artist', 'artist_href',
                                        'album_href', 'length'])

        data = json.dumps(instance.to_dict())
        io.Of('/{0}'.format(settings.ENV)).Emit(
            '{0}:playlist:add'.format(settings.ENV), data)

        # Track add redis event. Mopidy may resume if it's been waiting
        r_conn.publish(CHANNEL_ADD, data)

        try:
            trigger_badge_add_task.delay(instance.id)
        except InconsistencyError:
            # A not very bad error that i dont want to raise a 500 response
            pass
    else:
        # Updating a track record, must be marking it as played
        io.Of('/{0}'.format(settings.ENV)).Emit(
            '{0}:playlist:played'.format(settings.ENV),
            json.dumps(instance.to_dict()))


def track_deleted(sender, instance, **kwargs):

    if not instance.played:
        io.Of('/app').Emit('playlist:delete', instance.id)
