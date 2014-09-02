from datetime import datetime

import spotipy
from spotipy import oauth2

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from .utils import get_spotify_api, get_or_create_cred
from .models import Credential


oa = oauth2.SpotifyOAuth(
        settings.SPOTIFY_CLIENT_ID,
        settings.SPOTIFY_CLIENT_SECRET,
        settings.SPOTIFY_OAUTH_REDIRECT)


class Index(TemplateView):
    template_name = 'spotify_playlist/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        sp = get_spotify_api(self.request.user)

        playlists = sp.user_playlists('***REMOVED***')

        context.update({'sp': sp, 'playlists': playlists})
        return context


def authorize(request):
    """ Redirect to Spotify site to request authorisation
    """
    return HttpResponseRedirect(oa.get_authorize_url())


def oauth_callback(request):
    """ Handle Oauth Callback, Redirect to the Spotify site if the reponse
    code is not valid
    """
    auth_code = request.GET.get('code')
    try:
        res = oa.get_access_token(auth_code)
    except spotipy.oauth2.SpotifyOauthError:
        return HttpResponseRedirect(oa.get_authorize_url())

    access_token = res['access_token']
    refresh_token = res['refresh_token']
    expires_at = res['expires_at']

    cred = get_or_create_cred(request.user)
    cred.access_token = access_token
    cred.refresh_token = refresh_token
    cred.expires_at = datetime.fromtimestamp(int(expires_at))
    cred.save()

    return HttpResponseRedirect(reverse('spotify_playlist:index'))


index = Index.as_view()
