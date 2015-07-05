from __future__ import unicode_literals

import json
from itertools import chain
from logging import getLogger

import redis
from emitter import Emitter

from django.db import IntegrityError
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest,
                         HttpResponseNotModified,
                         HttpResponseNotAllowed)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.conf import settings

from .push import track_played_pusher

from pokeradio.badges import BadgeManager
from pokeradio.history.utils import get_or_create_track, record_track_play
from pokeradio.models import Track, AwardedBadge
from pokeradio.scoring.models import Point
from pokeradio.responses import (JSONResponse,
                                 JSONResponseError,
                                 JSONResponseNotFound,
                                 JSONResponseBadRequest)

from .models import Token

logger = getLogger(__file__)

# for Emiting events to be sent to browers via socket server
io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT,
    'db': settings.REDIS_DB})

redis_conn = redis.StrictRedis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
    """ RESTish endpoints for the (web)app for the Playlist
    """
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
    """ RESTish endpoints for the (web)app for the Tracks
    """
    model = Track
    http_method_names = ['get', 'delete', 'patch']

    def delete(self, request, pk):
        try:
            track = Track.objects.get(user=request.user, id=pk, played=False)
        except Track.DoesNotExist:
            return JSONResponseBadRequest(message='You cant do that')
        else:
            track.delete()
            return JSONResponse({'status': 'OK'})

    def patch(self, request, pk):
        data = json.loads(request.body)
        self.user = request.user

        if 'vote' in data:
            return self.vote(pk, data['vote'])

    def vote(self, pk, action):

        try:
            # Get the track being liked
            track = Track.objects.get(id=pk)
        except Track.DoesNotExist:
            return JSONResponseNotFound()
        else:
            # Check not self vote
            if track.user == self.user:
                return JSONResponseBadRequest(
                        message='You cant vote for your own track')

            try:
                archive_track = get_or_create_track(track)

                # Make a point, but catch the exception raised by the
                # violation of unique_togetherness of (playlist) track and
                # voter
                p = Point.objects.create(user=track.user,
                                         action=action,
                                         track_name=str(track)[:100],
                                         playlist_track=track,
                                         archive_track=archive_track,
                                         vote_from=self.user)

            except IntegrityError:
                # User has already voted for this track
                return JSONResponseBadRequest(
                    message='Thanks, you appear to have already voiced an '
                            'opinion on {0}\'s choice to play {1}'
                            .format(track.user.first_name, track))
            else:
                return JSONResponse({'status': 'OK'})


class MopidyPlaylistTrack(View):
    """ RESTish endpoints for the Raspberry Pi
    """

    http_method_names = ['get', 'put', 'post']

    # Next track
    def get(self, request):
        """ If there is no track to play, set a redis key.
        On the save signal, this key is checked, and a pubsub message is issued
        if a track is created while the waiting flag is set
        """
        self.object = Track.objects.new()

        if self.object:
            payload = {'id': self.object.id, 'href': self.object.href}
        else:
            payload = {'status': 'empty'}

        return JSONResponse(payload)

    # Update progress
    def put(self, request):
        try:
            data = json.loads(request.body)
        except ValueError:
            return JSONResponse({'status': 'Not JSON'})

        href = data['href']

        # Find first unplayed instance of the track by href
        try:
            self.object = Track.objects.filter(href=href, played=False)[0]
        except (Track.DoesNotExist, IndexError):
            logger.error('Setting traock as played - Track not found')
            return JSONResponseNotFound()
        else:

            if 'started' == data['action']:
                record_track_play(self.object)

                if settings.USE_PUSHER:
                    track_played_pusher(self.object)

                return JSONResponse({'status': 'OK'})

            if 'ended' == data['action']:
                self.object.set_played()
                return JSONResponse({'status': 'OK'})

    def post(self, request):
        data = json.loads(request.body)

        if 'progress' == data['action']:
            io.Of('/app').Emit('play:progress', request.body)

            playback_state = json.loads(request.body).get('playback_state',
                                                          'unknown')
            pipe = redis_conn.pipeline()
            pipe.set('playback_state', playback_state)
            pipe.expire('playback_state', 20)
            pipe.execute()

            return JSONResponse({'status': 'OK'})

def badges(request, user_id):
    awarded_badges = AwardedBadge.objects.active().filter(user_id=user_id)
    awarded_badges_json = \
        [dict(BadgeManager.get_badge(ab.badge).to_dict().items() + {
            'id': ab.pk,
        }.items()) for ab in awarded_badges]
    return JSONResponse(awarded_badges_json)


playlist = csrf_exempt(Playlist.as_view())
playlist_track = csrf_exempt(PlaylistTrack.as_view())

mopidy = csrf_exempt(MopidyPlaylistTrack.as_view())
