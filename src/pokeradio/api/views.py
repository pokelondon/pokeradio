from django.db import IntegrityError
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest,
                         HttpResponseNotModified,
                         HttpResponseNotAllowed)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from pokeradio.history.utils import get_or_create_track
from pokeradio.models import Track
from pokeradio.scoring.models import Point


from .models import Token


@csrf_exempt
def vote(request):
    """ Token-based voting on current playing track, or most recently played
    track, if nothing's playing
    """

    token = request.POST.get('token')
    vote = request.POST.get('vote')

    # flip this to disable this endpoint
    if False:
        response = HttpResponse("This isn't implemented just yet. Try again later.",
                                content_type='text/plain')
        response.status_code = 501
        return response

    # validate POST data
    if token is None or vote is None:
        return HttpResponseBadRequest('Malformed request, sorry. Needs to '
                                      'contain token and vote.',
                                      content_type='text/plain')

    # validate vote
    vote = int(vote)
    if vote not in [-1, 1]:
        return HttpResponseBadRequest('Malformed request, sorry. Vote needs to '
                                      'be 1 or -1.',
                                      content_type='text/plain')

    # validate token
    try:
        token = Token.objects.get(token=token, enabled=True)
    except Token.DoesNotExist:
        return HttpResponseForbidden('Invalid voting token, sorry.',
                                     content_type='text/plain')

    # get 'current' track
    # 'current' playing track as earliest added unplayed track
    track = Track.objects.filter(played=False).order_by('timestamp').first()
    if track is None:
        # or... most recently played track, if nothing playing
        track = Track.objects.filter(played=True).order_by('timestamp').last()

    # check this isn't one of the user's tracks
    if track.user == token.user:
        return HttpResponseNotAllowed("You can't vote on your own track!",
                                       content_type='text/plain')

    # convert vote to action
    action = Point.TRACK_LIKED if vote == 1 else Point.TRACK_DISLIKED

    # attempt to register Point
    try:
        archive_track = get_or_create_track(track)
        Point.objects.create(user=track.user, action=action,
                             track_name=str(track)[:100],
                             playlist_track=track,
                             archive_track=archive_track,
                             vote_from=token.user)
    except IntegrityError:
        return HttpResponseNotModified()

    return HttpResponse('Got it.', content_type='text/plain')
