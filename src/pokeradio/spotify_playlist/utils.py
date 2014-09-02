from .models import Credential


def get_or_create_cred(user):
    """ Access or create the Credential model for the user
    """
    try:
        return Credential.objects.get(user=user)
    except Credential.DoesNotExist:
        return Credential.objects.create(user=user)


def get_spotify_api(user):
    """ Find a user's credentials and return a spotify API instance
    """
    cred = get_or_create_cred(user)
    return cred.get_spotify_api()
