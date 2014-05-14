import simplejson as json
import redis
from django.conf import settings

from pokeradio.scoring.models import Credit

def track_saved(sender, instance, created, **kwargs):
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

    if created:
        # Deduct a credit for this play
        c = Credit.objects.create(user=instance.user, action='TRACK_ADD',
                track_name=str(instance)[:100])

        r.publish('pr:track_add', json.dumps(instance.to_dict()))
    else:
        # Updating a track record, must be marking it as played
        r.publish('pr:track_played', json.dumps(instance.to_dict()))

def track_deleted(sender, instance, **kwargs):
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

    if not instance.played:
        # Refund the user a credit
        c = Credit.objects.create(user=instance.user, action='REFUND',
                track_name=str(instance)[:100])

        r.publish('pr:track_delete', instance.id)