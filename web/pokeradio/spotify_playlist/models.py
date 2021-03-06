from datetime import datetime

import spotipy
from spotipy import oauth2

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


oa = oauth2.SpotifyOAuth(
        settings.SPOTIFY_CLIENT_ID,
        settings.SPOTIFY_CLIENT_SECRET,
        settings.SPOTIFY_OAUTH_REDIRECT)


class Credential(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    refresh_token = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    playlist_id = models.CharField(max_length=200, blank=True, null=True)
    spotify_id = models.CharField(max_length=20, blank=True, null=True)


    def __unicode__(self):
        return self.user.get_full_name()

    def get_spotify_api(self):
        """ Get a scoped, authorised instance of spotipi API wrapper
        refreshing the access token if necessary
        """
        if not self.access_token:
            return None

        if self.expires_at and datetime.now() > self.expires_at:
            print 'Refreshing Token'
            self._refresh_access_token()

        sp = spotipy.Spotify(auth=self.access_token)

        if not self.spotify_id:
            self.spotify_id = sp.me()['id']
            self.save()

        return sp

    def _refresh_access_token(self):
        """ Same process as on the oauth callback view. Using the refresh
        token to request a new access_token
        """
        if not self.refresh_token:
            raise Exception('No refresh token')

        res = oa._refresh_access_token(self.refresh_token)
        access_token = res['access_token']
        refresh_token = res['refresh_token']
        expires_at = res['expires_at']

        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = datetime.fromtimestamp(int(expires_at))
        self.save()

    def token_valid(self):

        if not self.access_token:
            return False

        if self.expires_at and datetime.now() > self.expires_at:
            return False

        return True


class PlaylistItem(models.Model):
    """ TO keep track of what's in the spotify playlist.
    Items in here wont be sent to the API. To prevent deduping.
    If a track is removed remotely, then its probably best not to re-send it
    """
    created = models.DateTimeField(auto_now_add=True)
    href = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User')

    class Meta:
        unique_together = ('user', 'href')

    def __unicode__(self):
        return self.href
