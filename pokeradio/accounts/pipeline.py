from django.conf import settings
from django.core.files.base import ContentFile

from pokeradio.tasks import create_image
from pokeradio.models import Profile


def get_or_create_user_profile(user):
    try:
        return user.get_profile()
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)


def get_profile_pic(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    image_url = response.get('picture', None)

    if not image_url:
        return

    image = create_image(image_url, settings.THUMBNAIL_SIZE)
    profile = get_or_create_user_profile(user)
    filename = 'profile_{0}.jpg'.format(user.id)
    profile.image.save(filename, ContentFile(image.getvalue()), save=False)
    profile.save(update_fields=['image'])

