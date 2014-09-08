"""
.. module:: pokeradio.history.models
   :synopsis: For storing canonical records to tracks, and instances of them
   being played
"""

import random
import os

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

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
    no_artwork = models.BooleanField(default=False,
            help_text="This track is known to return no artwork from the "
                      "lookup service. Prevents additional lookups")

    artist = models.ForeignKey(Artist)

    objects = TrackManager()
    blacklist = BlacklistManager()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.artist)

    @property
    def artwork_url(self):
        """ Return the URL to the artwork lookup view.
        This will query an external API if the file does not exist, so if the
        album (identified by code; a subset of spotify_album_href) will be
        marked as having no artwork so as to prevent further unnecesary
        lookups
        """
        if self.no_artwork:
            static = settings.STATIC_ROOT
            # Dev uses a single static folder thats not collectstatic'ed
            if not static:
                static = os.path.join(settings.PROJECT_ROOT, 'public')

            filename = random.choice(os.listdir(os.path.join(static, 'img',
                                                             'artwork')))
            return os.path.join(settings.STATIC_URL, 'img', 'artwork',
                                filename)

        album_id = self.spotify_album_href.split(':')[2]
        return reverse('albumart:getimage', args=(album_id, ))

    @property
    def score(self):
        """ Total net score for this track
        """
        return self.point_set.all().aggregate(models.Sum('value'))['value__sum']


class Play(Base):
    track = models.ForeignKey(ArchiveTrack)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{0} played by {1}'.format(self.track, self.user)
