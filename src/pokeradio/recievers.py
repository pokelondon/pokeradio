from __future__ import unicode_literals

import simplejson as json

import redis
from emitter import Emitter

from django.conf import settings


io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT,
              'db': settings.REDIS_DB})

r_conn = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT,
                           db=settings.REDIS_DB)

def track_saved(sender, instance, created, **kwargs):

    if created:
        data = json.dumps(instance.to_dict())
        io.Of('/app').Emit('playlist:add', data)

        # Tell mopidy to resume now there is a track
        if r_conn.get('mopidy:track_waiting'):
            r_conn.publish('mopdiy:track_play', data)
    else:
        # Updating a track record, must be marking it as played
        io.Of('/app').Emit('playlist:played', json.dumps(instance.to_dict()))


def track_deleted(sender, instance, **kwargs):

    if not instance.played:
        io.Of('/app').Emit('playlist:delete', instance.id)
