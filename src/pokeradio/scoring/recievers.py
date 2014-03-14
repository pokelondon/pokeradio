import json
import requests
import logging

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('raven')

payload = {
    "channel": "#general",
    "username": "Poke Radio",
    "fallback": "Track Vote",
}

def report_vote(sender, instance, created, **kwargs):
    from .models import Point
    if not created:
        return

    if not instance.user.groups.filter(name='Slack'):
        return

    if instance.action == Point.TRACK_LIKED:
        payload["fallback"] =  "Track Liked: {0}".format(instance.archive_track.name)
        payload["pretext"] = "Track Liked"
        payload["color"] = "#f5007f"
    else:
        payload["fallback"] =  "Track Dissed: {0}".format(instance.archive_track.name)
        payload["pretext"] = "Track Disliked"
        payload["color"] = "#f5007f"

    payload["fields"] = [
        {
            "title": '{0} - {1}'.format(instance.archive_track.name,
                instance.archive_track.artist.name),
            "value": instance.archive_track.point_set.all().aggregate(models.Sum('value'))['value__sum'],
            "short": True
        },
        {
            "title": instance.user.get_full_name(),
            "value": instance.user.point_set.all().aggregate(models.Sum('value'))['value__sum'],
            "short": True
        },
    ]

    r = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))


def send_light_vote(sender, instance, created, **kwargs):
    from .models import Point
    if not created:
        return

    #send data to lights app
    post_vars = {}
    post_vars["action"] = instance.action
    try:
        post_vars["colour"] = instance.vote_from.profile.colour
    except ObjectDoesNotExist:
        post_vars["colour"] = 'FFFFFF'
    
    try:
        r = requests.post(settings.LIGHTS_WEBHOOK_URL, data=post_vars)
    except Exception, e:
        logger.warn('cannot send data to lights server')
