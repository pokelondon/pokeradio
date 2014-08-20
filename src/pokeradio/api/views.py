import json
from itertools import chain

from django.db import IntegrityError
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest,
                         HttpResponseNotModified,
                         HttpResponseNotAllowed)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.conf import settings

from pokeradio.history.utils import get_or_create_track
from pokeradio.models import Track
from pokeradio.scoring.models import Point
from pokeradio.responses import JSONResponse, JSONResponseError

from .models import Token


@csrf_exempt
def vote(request):
    """ Token-based voting on current playing track, or most recently played
    track, if nothing's playing
    """

    token = request.POST.get('token')
    id = request.POST.get('id')
    vote = request.POST.get('vote')

    # flip this to disable this endpoint
    if False:
        response = HttpResponse("This isn't implemented just yet. Try again later.",
                                content_type='text/plain')
        response.status_code = 501
        return response

    # validate POST data
    if token is None or vote is None or id is None:
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

    # validate track
    id = int(id)
    try:
        track = Track.objects.get(pk=id)
    except Track.DoesNotExist:
        return HttpResponseForbidden('Invalid track, sorry.',
                                     content_type='text/plain')

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


class Playlist(ListView):
    model = Track

    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        tracks_new = self.model.objects.filter(played__exact=False)
        tracks_played = self.model.objects.filter(played__exact=True)\
                .reverse()[:1]
        tracks = list(chain(tracks_played, tracks_new))
        data = [track.to_dict() for track in tracks]
        return JSONResponse(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        # Remove defaults from Backbone Model
        for prop in ['liked', 'disliked', 'isMine', 'isPlaying']:
            data.pop(prop)

        data['album_href'] = data.pop('album').get('href')
        data['user'] = request.user

        t = self.model.objects.create(**data)
        return JSONResponse(t.to_dict())


class PlaylistTrack(DetailView):
    model = Track
    http_method_names = ['get', 'delete', 'patch']

    def delete(self, request, pk):
        try:
            track = Track.objects.get(user=request.user, id=int(pk),
                                      played=False)
        except Track.DoesNotExist:
            return JSONResponseError('You cant do that')
        else:
            track.delete()
            return JSONResponse({'status': 'OK'})

    def patch(self, request, pk):
        data = json.loads(request.body)
        print data
        try:
            track = Track.objects.get(id=int(pk))
        except Track.DoesNotExist:
            return JSONResponseError('Track not found')
        else:
            if track.user == request.user:
                return JSONResponseError('You cant vote for your own track')
            print 'Vote'
            return JSONResponse({'status': 'OK'})


playlist = csrf_exempt(Playlist.as_view())
playlist_track = csrf_exempt(PlaylistTrack.as_view())
