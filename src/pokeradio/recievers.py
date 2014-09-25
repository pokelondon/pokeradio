from __future__ import unicode_literals

import simplejson as json

import redis
from emitter import Emitter

from django.conf import settings

from pokeradio.badges import BadgeManager


io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT,
              'db': settings.REDIS_DB})

r_conn = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT,
                           db=settings.REDIS_DB)

def track_saved(sender, instance, created, **kwargs):

    if created:
        data = json.dumps(instance.to_dict())
        io.Of('/app').Emit('playlist:add', data)

        # Track add redis event. Mopidy may resume if it's been waiting
        r_conn.publish('mopidy:track_added', data)
    else:
        # Updating a track record, must be marking it as played
        io.Of('/app').Emit('playlist:played', json.dumps(instance.to_dict()))


def track_saved_badge_handler(sender, instance, created, **kwargs):

    bm = BadgeManager()

    if created:
        bm.trigger('add', instance, instance.user)


def track_deleted(sender, instance, **kwargs):

    if not instance.played:
        io.Of('/app').Emit('playlist:delete', instance.id)
