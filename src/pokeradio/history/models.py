"""
.. module:: pokeradio.history.models
   :synopsis: For storing canonical records to tracks, and instances of them
   being played
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .managers import ArtistManager, TrackManager, BlacklistManager


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Artist(Base):
    name = models.CharField(max_length=255)
    spotify_artist_href = models.CharField(max_length=255, unique=True)

    objects = ArtistManager()

    def __unicode__(self):
        return self.name


class ArchiveTrack(Base):
    name = models.CharField(max_length=255)
    spotify_href = models.CharField(max_length=255, unique=True)
    length = models.FloatField(null=True)
    spotify_album_href = models.CharField(max_length=255)
    in_blacklist = models.BooleanField(default=False)

    artist = models.ForeignKey(Artist)

    objects = TrackManager()
    blacklist = BlacklistManager()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.artist)


class Play(Base):
    track = models.ForeignKey(ArchiveTrack)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{0} played by {1}'.format(self.track, self.user)



