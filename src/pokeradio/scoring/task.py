
from django.db import models

from .models import Point
from .slack import Slack

@app.task
def send_slack_vote(point_id):
    """
    Accepts an instance of pokeradio.Track
    Sends a message to the Dev slack channel when one of us gets a vote
    """
    point = Point.objects.get(pk=point_id)
    
    if not point.user.groups.filter(name='Slack'):
        return

    msg = Slack('Track Disliked',
                'Track Dissed: {0}'.format(point.archive_track.name),
                Slack.PINK,
                'tech',
                Slack.PUBLIC)

    if point.action == Point.TRACK_LIKED:
        msg.pretext = 'Track Liked'
        msg.fallback = 'Track Liked: {0}'.format(instance.archive_track.name)


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