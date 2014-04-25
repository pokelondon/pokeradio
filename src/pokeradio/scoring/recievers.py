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

    try:
        r = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except Exception, e:
        logger.warn('cannot send data to Slack')



def send_light_vote(sender, instance, created, **kwargs):
    logger.info("send_light_vote called")
    from .models import Point
    if not created:
        logger.warn("send_light_vote - point was not created")
        return

    #send data to lights app
    post_vars = {}
    post_vars["action"] = instance.action
    try:
        post_vars["colour"] = instance.vote_from.profile.colour
    except ObjectDoesNotExist:
        post_vars["colour"] = 'FFFFFF'

    try:
        logger.info("send_light_vote - requesting light url")
        r = requests.post(settings.LIGHTS_WEBHOOK_URL, data=post_vars)
    except Exception, e:
        logger.warn('cannot send data to lights server')


def send_dweet(sender, instance, created, **kwargs):
    from .models import Point
    if not created:
        return

    #send data to lights app
    params = {'key': instance.action}
    data = json.dumps({
        'track': instance.archive_track.name,
        'artist': instance.archive_track.artist.name,
        'dj': instance.user.get_full_name(),
    })
    headers = {'content-type': 'application/json'}

    try:
        r = requests.post('https://dweet.io:443/dweet/for/pokeradio',
                          data=data, params=params, headers=headers)
    except Exception, e:
        logger.warn('Cannot send data to lights Dweet')


def send_push(sender, instance, created, **kwargs):
    import pusher
    if not created:
        return
    
    #Send notification to pusher    
    p = pusher.Pusher(
      app_id = settings.PUSHER_APP_ID,
      key= settings.PUSHER_KEY,
      secret= settings.PUSHER_SECRET
    )

    data = json.dumps({
        'track': instance.archive_track.name,
        'artist': instance.archive_track.artist.name,
        'dj': instance.user.get_full_name(),
        'action': instance.action,
    })
    p['poke_radio'].trigger('vote', data)

