from spotipy import oauth2

from django.conf import settings

from .models import Credential


PLAYLIST_NAME = 'Poke Radio'


def get_or_create_cred(user):
    """ Access or create the Credential model for the user
    """
    try:
        return Credential.objects.get(user=user)
    except Credential.DoesNotExist:
        return Credential.objects.create(user=user)


def get_or_create_spotify_playlist(cred, sp):
    # Get or create Prad Playlist
    if cred.playlist_id:
        # Check its on sp
        res = sp.user_playlist(cred.spotify_id, cred.playlist_id)
    else:
        # Create playlist
        res = sp.user_playlist_create(cred.spotify_id, PLAYLIST_NAME, True)
        cred.playlist_id = res['id']
        cred.save()

    return res
