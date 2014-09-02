from spotipy import oauth2

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

oa = oauth2.SpotifyOAuth(
        settings.SPOTIFY_CLIENT_ID,
        settings.SPOTIFY_CLIENT_SECRET,
        'http://dev.errkk.co/spotify/oauth_callback/')


def authorize(request):
    return HttpResponseRedirect(oa.get_authorize_url())

def oauth_callback(request):
    auth_code = request.GET.get('code')
    res = oa.get_access_token(auth_code)
    access_token = res['access_token']
    return HttpResponse(access_token)

