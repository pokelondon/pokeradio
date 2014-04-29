from calendar import timegm

import simplejson as json

import requests

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

from pokeradio.scoring.models import Point
from .recievers import track_saved, track_deleted

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

post_save.connect(track_saved, sender=Track)
post_delete.connect(track_deleted, sender=Track)