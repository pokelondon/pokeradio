
import requests
import logging

from django.db import models, IntegrityError
from django.conf import settings

from pokeradio.celery import app
from pokeradio.spotify_playlist.utils import get_or_create_cred
from pokeradio.spotify_playlist.models import PlaylistItem
from .slack import Slack

logger = logging.getLogger('raven')

@app.task
def send_slack_vote_task(point_id):
    from .models import Point

    point = Point.objects.get(pk=point_id)

    msg = Slack('Track Disliked',
                'Track Dissed: {0}'.format(point.archive_track.name),
                Slack.PINK,
                'tech',
                Slack.PUBLIC)

    if point.action == Point.TRACK_LIKED:
        msg.pretext = 'Track Liked'
        msg.fallback = 'Track Liked: {0}'.format(point.archive_track.name)


    user_votes = point.user.point_set.all().aggregate(
            models.Sum('value'))['value__sum']
    track_votes = point.archive_track.point_set.all().aggregate(
            models.Sum('value'))['value__sum']
    title = '{0} - {1}'.format(unicode(point.archive_track.name),
                               unicode(point.archive_track.artist.name))

    msg.add_field(title=title, value=track_votes, short=True)
    msg.add_field(title=point.user.get_full_name(), value=user_votes,
                  short=True)
    msg.send()

@app.task
def send_light_vote_task(post_vars):
    try:
        r = requests.post(settings.LIGHTS_WEBHOOK_URL, data=post_vars)
    except Exception:
        logger.warn('cannot send data to lights server')

@app.task
def send_slack_skip_task(self, verb, score, point_id):
    from .models import Point

    point = Point.objects.get(pk=point_id)
    msg = Slack('Track {0}'.format(verb),
                'Track {0}: {1}'.format(verb, point.archive_track.name),
                Slack.PINK,
                '#music',
                Slack.PUBLIC)

    total_votes = point.archive_track.point_set.all().aggregate(
            models.Sum('value'))['value__sum']

    title = '{0} - {1}'.format(unicode(point.archive_track.name),
                                unicode(point.archive_track.artist.name))

    msg.add_field(title=title, value=total_votes, short=True)
    msg.add_field(title=point.user.get_full_name(), value=score, short=True)

    msg.send()
    

@app.task
def add_to_personal_playlist_task(point_id):
    
    from .models import Point
    
    point = Point.objects.get(pk=point_id)

    cred = get_or_create_cred(point.vote_from)

    if not cred.playlist_id:
        return

    # TODO, if this doesnt work, and the token is the problem
    # queue a message to the user telling them to reauthorise

    try:
        playlist_item = PlaylistItem.objects.create(
                user=point.vote_from,
                href=point.playlist_track.href)
    except IntegrityError:
        # Already probably in their playlist
        return

    try:
        sp = cred.get_spotify_api()
        res = sp.user_playlist_add_tracks(cred.spotify_id, cred.playlist_id,
                                          [point.playlist_track.href, ])
    except:
        playlist_item.delete()


