from calendar import timegm
import simplejson as json
import redis

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings


class Track(models.Model):
    """ A track in a playlist
    """
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    played = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    length = models.FloatField(null=True)
    album_href = models.CharField(max_length=255)

    class Meta:
        ordering = ['timestamp']

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'href': self.href,
            'timestamp': timegm(self.timestamp.utctimetuple()),
            'played': self.played,
            'length': self.length,
            'album_href': self.album_href,
            'user': {
                'id': self.user.id,
                'full_name': self.user.get_full_name(),
            }
        }

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.artist)


@receiver(post_save, sender=Track)
def track_saved(sender, instance, **kwargs):
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)
    r.publish('playlist', json.dumps(instance.to_dict()))


@receiver(post_delete, sender=Track)
def track_deleted(sender, instance, **kwargs):
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)
    r.publish('deleted', instance.id)
