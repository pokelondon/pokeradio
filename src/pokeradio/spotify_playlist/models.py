import spotipy

from django.db import models
from django.contrib.auth.models import User


class Credential(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    refresh_token = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    playlist_id = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def get_spotify_api(self):
        # TODO do something about refresh token if it is expired
        return spotipy.Spotify(auth=self.access_token)

    def _refresh_access_token(self):
        pass
