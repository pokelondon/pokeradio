from calendar import timegm
import simplejson as json

import requests
import redis

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings

from pokeradio.scoring.models import Credit, Point


class Profile(models.Model):
    user = models.OneToOneField(User)
    colour = models.CharField(max_length=6, default='FFFFFF')


class Track(models.Model):
    """ A track in a playlist
    """
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    href = models.CharField(max_length=255) # TODO, maybe index this
    timestamp = models.DateTimeField(auto_now_add=True)
    played = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    length = models.FloatField(null=True)
    album_href = models.CharField(max_length=255)
    artist_href = models.CharField(max_length=255)

    class Meta:
        ordering = ['timestamp']

    def _get_action_ids(self, action):
        """ For displaying things in the playlist, fetch IDs of users who
        have liked and disliked a track. Only for FE to compare against
        logged in user id, as this model doesn't know who that is
        """
        return map(int, self.point_set.filter(action=action)\
            .values_list('vote_from__id', flat=True))

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
            },
            'liked_ids': self._get_action_ids(Point.TRACK_LIKED),
            'disliked_ids': self._get_action_ids(Point.TRACK_DISLIKED),
        }

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.artist)

    def set_played(self):
        """ When the track has been played, run this.
        """
        self.played = True
        self.save()

    def __init__(self, *args, **kwargs):
        super(Track, self).__init__(*args, **kwargs)
        self.old_play_state = self.played

    def save(self, *args, **kwargs):
        if self.played != self.old_play_state:
            self.send_dweet_play()
        super(Track, self).save(*args, **kwargs)


    def send_dweet_play(self):
        params = {'key': 'played'}
        data = json.dumps({
            'action': 'played',
            'track': self.name,
            'id': self.pk,
            'href': self.href,
            'artist': self.artist,
            'dj': self.user.get_full_name(),
        })
        headers = {'content-type': 'application/json'}

        try:
            r = requests.post('https://dweet.io:443/dweet/for/pokeradio',
                            data=data, params=params, headers=headers)
        except Exception, e:
            pass


@receiver(post_save, sender=Track)
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


@receiver(post_delete, sender=Track)
def track_deleted(sender, instance, **kwargs):
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

    if not instance.played:
        # Refund the user a credit
        c = Credit.objects.create(user=instance.user, action='REFUND',
                track_name=str(instance)[:100])

        r.publish('pr:track_delete', instance.id)
