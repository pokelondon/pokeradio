from calendar import timegm

import simplejson as json

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

from pokeradio.scoring.models import Point

from .recievers import badge_saved, track_saved, track_deleted
from .managers import AwardedBadgeManager, TrackManager
from .badges import BadgeManager


class Profile(models.Model):
    user = models.OneToOneField(User)
    colour = models.CharField(max_length=6, default='FFFFFF')


class Track(models.Model):

    """ A track in a playlist
    """
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    href = models.CharField(max_length=255)  # TODO, maybe index this
    timestamp = models.DateTimeField(auto_now_add=True)
    played = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    length = models.FloatField(null=True)
    album_href = models.CharField(max_length=255)
    artist_href = models.CharField(max_length=255)

    objects = TrackManager()

    class Meta:
        ordering = ['timestamp']

    def _get_action_ids(self, action):
        """ For displaying things in the playlist, fetch IDs of users who
        have liked and disliked a track. Only for FE to compare against
        logged in user id, as this model doesn't know who that is
        """

        """Prevent hitting the DB"""
        return [ p.vote_from_id for p in self.point_set.all() if p.action == action]

        """return map(int, self.point_set.all().filter(action=action)
                   .values_list('vote_from__id', flat=True))"""


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

    def is_playing(self):
        # get the latest unplayed track in the playlist
        try:
            current_track = Track.objects.filter(played__exact=False)[:1][0]

            if self.id == current_track.id and not self.played:
                return True
            return False
        except IndexError:
            return False

post_save.connect(track_saved, sender=Track)
post_delete.connect(track_deleted, sender=Track)


class Message(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    text = models.CharField(max_length=300, blank=True, null=True)
    timeout = models.IntegerField(blank=True, null=True)
    target_to_individuals = models.BooleanField(default=False,
            help_text='Select "To be seen by" for people to show the message to')

    seenby = models.ManyToManyField('auth.User', related_name='seenby',
                                    blank=True, null=True)
    to_be_seen_by = models.ManyToManyField('auth.User',
                                           related_name='to_be_seen_by',
                                           blank=True, null=True)

    def __unicode__(self):
        return self.title

    def to_dict(self):

        as_dict = {
            'title': self.title,
            'text': self.text,
            'modal': True,
            'timeout': False,
            'closable': True,
        }

        if self.timeout:
            as_dict['timeout'] = self.timeout

        return as_dict


class AwardedBadge(models.Model):
    user = models.ForeignKey(User)
    badge = models.CharField(max_length=50, blank=False)
    expires = models.DateField(null=True)

    objects = AwardedBadgeManager()

    def description(self):
        return BadgeManager().get_badge(self.badge)

    def __unicode__(self):
        return u'{0} badge awarded to {1}'.format(self.badge, self.user)


post_save.connect(badge_saved, sender=AwardedBadge)
