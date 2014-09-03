from spotipy import oauth2

from django.conf import settings

from .models import Credential


def get_or_create_cred(user):
    """ Access or create the Credential model for the user
    """
    try:
        return Credential.objects.get(user=user)
    except Credential.DoesNotExist:
        return Credential.objects.create(user=user)
