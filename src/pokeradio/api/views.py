from __future__ import unicode_literals

import json
import redis
from itertools import chain

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

from pokeradio.history.utils import get_or_create_track, record_track_play
from pokeradio.models import Track
from pokeradio.scoring.models import Point
from pokeradio.responses import (JSONResponse,
                                 JSONResponseError,
                                 JSONResponseNotFound,
                                 JSONResponseBadRequest)

from .models import Token


io = Emitter({'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT})

r_conn = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)


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

def track_played_dweet(track):

    data = json.dumps({
        'action': 'playing',
        'id': track.pk,
        'href': track.href,
        'track': track.name,
        'artist': track.artist,
        'album_href': track.album_href,
        'dj': track.user.get_full_name(),
    })

    headers = {'content-type': 'application/json'}
    try:
        requests.post(
            'https://dweet.io:443/dweet/for/{0}'.format(
                settings.DWEET_NAME),
            data=data, params=params, headers=headers)
    except Exception, e:
        pass

def track_played_pusher(track):
    p = pusher.Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET
    )

    data = json.dumps({
        'action': 'playing',
        'id': track.pk,
        'href': track.href,
        'track': track.name,
        'artist': track.artist,
        'album_href': track.album_href,
        'dj': track.user.get_full_name(),
    })

    p['poke_radio'].trigger('on_playing', data)


class MopidyPlaylistTrack(View):

    http_method_names = ['get', 'put', 'post']

    # Next track
    def get(self, request):
        self.object = Track.objects.new()
        payload = {'id': self.object.id, 'href': self.object.href}
        return JSONResponse(payload)

    # Update progress
    def put(self, request):
        print request.body
        data = json.loads(request.body)

        print data
        href = data['href']

        # Find first unplayed instance of the track by href
        try:
            self.object = Track.objects.filter(href=href, played=False)[0]
        except (Track.DoesNotExist, IndexError):
            pass
        else:

            if 'started' == data['action']:
                record_track_play(self.object)

                if settings.USE_PUSHER:
                    track_played_pusher(self.object)

                if settings.DWEET_NAME:
                    track_played_dweet(self.object)

                print 'Track started', self.object.name
                return JSONResponse({'status': 'OK'})

            if 'ended' == data['action']:
                self.object.set_played()
                print 'Track ended', self.object.name
                return JSONResponse({'status': 'OK'})

    def post(self, request):
        data = json.loads(request.body)

        if 'progress' == data['action']:
            io.Of('/app').Emit('play:progress', request.body)
            return JSONResponse({'status': 'OK'})



class MopidyInstruction(View):
    def get(self, request):
        action = r_conn.get('mopidy_instruction')
        r_conn.delete('mopidy_instruction')
        return JSONResponse({'action': action})


playlist = csrf_exempt(Playlist.as_view())
playlist_track = csrf_exempt(PlaylistTrack.as_view())

mopidy = csrf_exempt(MopidyPlaylistTrack.as_view())
mopidy_instruction = csrf_exempt(MopidyInstruction.as_view())
