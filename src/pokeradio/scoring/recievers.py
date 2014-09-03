from __future__ import unicode_literals

import json
import requests
import logging
import redis

from emitter import Emitter

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ..spotify_playlist.utils import get_or_create_cred

from .slack import Slack

logger = logging.getLogger('raven')

# for Emiting events to be sent to browers via socket server
io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT,
              'db': settings.REDIS_DB})

# for publishing events to be sent to mopidy on the Pi
r_conn = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT,
                           db=settings.REDIS_DB)


def send_slack_vote(sender, instance, created, **kwargs):
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
                'tech',
                Slack.PUBLIC)

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
    """ post_save on instance of Point
    Send vote to lights server
    """
    if not created:
        return

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


def check_track_skip(sender, instance, created, **kwargs):
    """ Triggered by downvotes, Takes an instance of Point
    """
    # Check the cumulative score for this track -
    # if it is lower than the threshold then delete or skip
    score = instance.playlist_track.point_set.all().aggregate(
            models.Sum('value'))['value__sum']

    if score >= settings.POKERADIO_SKIP_THRESHOLD:
        return

    verb = 'Scratched'
    data = json.dumps(instance.playlist_track.to_dict())

    if instance.playlist_track.is_playing():
        # Notify browsers
        io.Of('/app').Emit('playlist:scratch', data)
        # Notify mopidy
        r_conn.publish('mopdiy:track_scratch', data)
        instance.playlist_track.set_played()
    else:
        io.Of('/app').Emit('playlist:skip', data)
        verb = 'Skipped'

        # Removes the track from the playlist if not yet played
        instance.playlist_track.delete()


    msg = Slack('Track {0}'.format(verb),
                'Track {0}: {1}'.format(verb, instance.archive_track.name),
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


def add_to_personal_playlist(sender, instance, created, **kwargs):
    """ If the user casting an upvote has a connected spotify account,
    post the track to their poke radio playlist
    """
    if not created:
        return

    if instance.value < 0:
        return

    cred = get_or_create_cred(instance.vote_from)

    if not cred.playlist_id:
        return

    # TODO, if this doesnt work, and the token is the problem
    # queue a message to the user telling them to reauthorise

    sp = cred.get_spotify_api()
    res = sp.user_playlist_add_tracks(cred.spotify_id, cred.playlist_id,
                                      [instance.playlist_track.href, ])
