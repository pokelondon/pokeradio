from __future__ import unicode_literals

from itertools import chain
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)


from django.db import IntegrityError
from django.http import Http404
from django.conf import settings

from pokeradio.badges import BadgeManager
from pokeradio.history.utils import get_or_create_track, record_track_play
from pokeradio.models import Track, AwardedBadge
from pokeradio.scoring.models import Point


class response_codes:
    OWN_TRACK = {'error': 'OWN_TRACK'}
    RATE_LIMIT = {'error': 'RATE_LIMIT'}
    ALREADY_VOTED = {'error': 'ALREADY_VOTED'}


class Identify(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if not request.auth:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = {
            'user_id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        return Response(data)


class Playlist(APIView):

    model = Track
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        tracks_new = self.model.objects.filter(played__exact=False)
        tracks_played = self.model.objects.filter(played__exact=True)\
                .reverse()[:1]
        tracks = list(chain(tracks_played, tracks_new))
        data = [track.to_dict() for track in tracks]
        return Response(data)

    def post(self, request, format=None):
        data = request.data
        t = self.model.objects.create(user=request.user, href=data.get('href'))
        return Response(t.to_dict())


class PlaylistDetail(APIView):

    model = Track
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        try:
            track = self.model.objects.get(user=request.user, id=pk,
                                           played=False)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            track.delete()
            return Response({'status': 'OK'})

    def patch(self, request, pk, format=None):
        data = request.data
        user = request.user

        if 'vote' in data:
            action = Point.TRACK_LIKED
            if 0 > data['vote']:
                action = Point.TRACK_DISLIKED

            return self._vote(pk, action, user)


    def _vote(self, pk, action, user):

        try:
            # Get the track being liked
            track = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            raise Http404()

        else:
            # Check not self vote
            if track.user == user:
                return Response(response_codes.OWN_TRACK,
                                status=status.HTTP_400_BAD_REQUEST)

            # Check vote rate limits, if this is a downvote
            if action == Point.TRACK_DISLIKED:
                delta_5_sec = datetime.now() - timedelta(seconds=5)
                count_5_sec = user.vote_from.filter(
                        created__gte=delta_5_sec,
                        action=Point.TRACK_DISLIKED).count()
                # Chance to save a query with early return here
                if count_5_sec > settings.POKERADIO_5_SEC_VOTE_LIMIT:
                    return Response(response_codes.RATE_LIMIT,
                                    status=status.HTTP_400_BAD_REQUEST)

                delta_10_sec = datetime.now() - timedelta(seconds=10)
                count_10_sec = user.vote_from.filter(
                        created__gte=delta_10_sec,
                        action=Point.TRACK_DISLIKED).count()

                if count_10_sec > settings.POKERADIO_10_SEC_VOTE_LIMIT:
                    return Response(response_codes.RATE_LIMIT,
                                    status=status.HTTP_400_BAD_REQUEST)

                delta_30_sec = datetime.now() - timedelta(seconds=30)
                count_30_sec = user.vote_from.filter(
                        created__gte=delta_30_sec,
                        action=Point.TRACK_DISLIKED).count()

                if count_30_sec > settings.POKERADIO_30_SEC_VOTE_LIMIT:
                    return Response(response_codes.RATE_LIMIT,
                                    status=status.HTTP_400_BAD_REQUEST)

                delta_60_sec = datetime.now() - timedelta(seconds=60)
                count_60_sec = user.vote_from.filter(
                        created__gte=delta_60_sec,
                        action=Point.TRACK_DISLIKED).count()

                if count_60_sec > settings.POKERADIO_60_SEC_VOTE_LIMIT:
                    return Response(response_codes.RATE_LIMIT,
                                    status=status.HTTP_400_BAD_REQUEST)

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
                                         vote_from=user)

            except IntegrityError:
                # User has already voted for this track
                return Response(response_codes.ALREADY_VOTED,
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'OK'})


identify = Identify.as_view()
playlist = Playlist.as_view()
playlist_detail = PlaylistDetail.as_view()

