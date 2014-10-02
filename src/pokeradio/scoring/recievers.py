from __future__ import unicode_literals

import json

import logging
import redis

from emitter import Emitter

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from pokeradio.badges import get_badge_manager

from .slack import Slack
from tasks import (send_slack_vote_task,
                    send_light_vote_task,
                    send_slack_skip_task,
                    add_to_personal_playlist_task)


bm = get_badge_manager()

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

    if not created:
        return

    if not instance.user.groups.filter(name='Slack'):
        return

    send_slack_vote_task.delay(instance.id)

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

    send_light_vote_task.delay(post_vars)


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

    bm.trigger('skip', instance)

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

    send_slack_skip_task.delay(verb, score, instance.id)


def check_vote_badges(sender, instance, created, **kwargs):
    """ Check any vote-related badges for possible awards
    """
    if created:
        bm.trigger('vote', instance)



def add_to_personal_playlist(sender, instance, created, **kwargs):
    """ If the user casting an upvote has a connected spotify account,
    post the track to their poke radio playlist
    """
    if not created:
        return

    if instance.value < 0:
        return

    add_to_personal_playlist_task.delay(instance.id)
