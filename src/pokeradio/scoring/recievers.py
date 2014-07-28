import json
import requests
import logging
import redis

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .slack import Slack

logger = logging.getLogger('raven')


def report_vote(sender, instance, created, **kwargs):
    """ Accepts an instance of pokeradio.Track
    Sends a message to the Dev slack channel when one of us gets a vote
    """

    from .models import Point
    if not created:
        return

    if not instance.user.groups.filter(name='Slack'):
        return

    msg = Slack('Track Disliked',
                'Track Dissed: {0}'.format(instance.archive_track.name),
                Slack.PINK,
                Slack.GENERAL,
                Slack.DEV)

    if instance.action == Point.TRACK_LIKED:
        msg.pretext = 'Track Liked'
        msg.fallback = 'Track Liked: {0}'.format(instance.archive_track.name)


    user_votes = instance.user.point_set.all().aggregate(
            models.Sum('value'))['value__sum']
    track_votes = instance.archive_track.point_set.all().aggregate(
            models.Sum('value'))['value__sum']
    title = '{0} - {1}'.format(unicode(instance.archive_track.name),
                               unicode(instance.archive_track.artist.name))

    msg.add_field(title=title, value=track_votes, short=True)
    msg.add_field(title=instance.user.get_full_name(), value=user_votes,
                  short=True)

    msg.send()


def send_light_vote(sender, instance, created, **kwargs):
    from .models import Point
    if not created:
        return

    #send data to lights app
    post_vars = {}
    post_vars["action"] = instance.action
    try:
        post_vars["colour"] = instance.vote_from.profile.colour
    except:
        post_vars["colour"] = 'FFFFFF'

    try:
        r = requests.post(settings.LIGHTS_WEBHOOK_URL, data=post_vars)
    except Exception, e:
        logger.warn('cannot send data to lights server')


def send_dweet_vote(sender, instance, created, **kwargs):
    if not created:
        return

    params = {'key': instance.action}
    data = json.dumps({
        'action': instance.action,
        'track': instance.archive_track.name,
        'artist': instance.archive_track.artist.name,
        'dj': instance.user.get_full_name(),
    })
    headers = {'content-type': 'application/json'}

    try:
        r = requests.post('https://dweet.io:443/dweet/for/{0}'.format(settings.DWEET_NAME),
                          data=data, params=params, headers=headers)
    except Exception, e:
        logger.warn('Cannot send data to lights Dweet')


def send_push(sender, instance, created, **kwargs):
    import pusher
    if not created:
        return

    if not settings.USE_PUSHER:
        return

    #Send notification to pusher
    p = pusher.Pusher(
      app_id = settings.PUSHER_APP_ID,
      key= settings.PUSHER_KEY,
      secret= settings.PUSHER_SECRET
    )

    data = json.dumps({
        'track': unicode(instance.archive_track.name),
        'artist': unicode(instance.archive_track.artist.name),
        'dj': instance.user.get_full_name(),
        'action': instance.action,
    })
    p['poke_radio'].trigger('vote', data)


def track_voted(sender, instance, created, **kwargs):
    """
    When a track has been voted up or down send redis message to the socket server to alert connect clients
    """
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

    data = json.dumps({
        "track": {
            "id": instance.playlist_track.id,
            "name": unicode(instance.archive_track.name),
            "artist": unicode(instance.archive_track.artist.name),
        },
        "user": {
            "full_name": instance.user.get_full_name(),
            "id":instance.user.id,
        },
        "action": instance.action,
        "value": instance.user.point_set.all().aggregate(models.Sum('value'))['value__sum']
        })
    r.publish('pr:track_voted', data)


def track_skip(sender, instance, created, **kwargs):
    """ Triggered by downvotes, Takes an instance of Point
    """
    r = redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

    # Check the cumulative score for this track -
    # if it is lower than the threshold then delete or skip
    score = instance.playlist_track.point_set.all().aggregate(
            models.Sum('value'))['value__sum']


    if score <= settings.POKERADIO_SKIP_THRESHOLD:
        # Get the latest unplayed track in the playlist
        r.publish('pr:track_skip',
                  json.dumps(instance.playlist_track.to_dict()))

        msg = Slack('Track Skipped',
                    'Track Skipped: {0}'.format(instance.archive_track.name),
                    Slack.PINK,
                    '#music',
                    Slack.PUBLIC)

        total_votes = instance.archive_track.point_set.all().aggregate(
                models.Sum('value'))['value__sum']
        title = '{0} - {1}'.format(unicode(instance.archive_track.name),
                                   unicode(instance.archive_track.artist.name))

        msg.add_field(title=title, value=total_votes, short=True)
        msg.add_field(title=instance.user.get_full_name(), value=score, short=True)

        msg.send()
