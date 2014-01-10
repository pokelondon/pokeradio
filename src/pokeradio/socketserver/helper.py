import simplejson as json
import logging
from itertools import chain
from importlib import import_module

from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.conf import settings

from pokeradio.models import Track



logger = logging.getLogger()

class TrackList:

    def _add_track(self, new_track, user):
        track = Track()
        track.name = new_track['name']
        track.artist = new_track['artist']
        track.href = new_track['href']
        track.user = user
        track.length = float(new_track['length'])
        track.album_href = new_track['album']['href']
        try:
            track.save()
        except IntegrityError, error:
            logger.error('Some thing has gone wrong %s' % error.message)
        return track


    def _add_album(self, new_track):
        pass

    def add(self, user_id, new_track):
        user = User.objects.get(pk=user_id)
        self._add_track(new_track, user)

    def get_user(self, sessionid):
        """ Exception handerling required """
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        s = SessionStore(session_key = sessionid)
        return s.get(SESSION_KEY)

    def get_mopidy_track(self, href=None):
        if href == None:
            track = Track.objects.filter(played__exact=False)[0]
            return json.dumps({ 'id' : track.id, 'href' : track.href })
        else:
            return Track.objects.filter(Q(played__exact=False),Q(href__exact=href))[0]

    def set_played(self,href, played=True):
        """ href is single string """
        track = self.get_mopidy_track(href)
        track.played = played
        track.save()

    def get_playlist(self):
        from pokeradio.models import Track
        tracks_new = Track.objects.filter(played__exact=False)
        tracks_played = Track.objects.filter(played__exact=True).reverse()[:3]
        tracks = list(chain(tracks_played, tracks_new))
        output = []
        for track in tracks:
            output.append(track.to_dict())
        return json.dumps(output)

    #def get_album_art(href):
        #print href.replace('spotify', )


