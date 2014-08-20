import simplejson as json

from emitter import Emitter

from django.conf import settings

from pokeradio.scoring.models import Credit


io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT})


def track_saved(sender, instance, created, **kwargs):

    if created:
        # Deduct a credit for this play
        c = Credit.objects.create(user=instance.user, action='TRACK_ADD',
                track_name=str(instance)[:100])

        print json.dumps(instance.to_dict())
        io.Of('/app').Emit('playlist:add', json.dumps(instance.to_dict()))
    else:
        # Updating a track record, must be marking it as played
        io.Of('/app').Emit('playlist:played', json.dumps(instance.to_dict()))


def track_deleted(sender, instance, **kwargs):

    if not instance.played:
        # Refund the user a credit
        c = Credit.objects.create(user=instance.user, action='REFUND',
                track_name=str(instance)[:100])

        io.Of('/app').Emit('playlist:delete', instance.id)
