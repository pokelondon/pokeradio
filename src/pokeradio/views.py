import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings



def _set_user_id(request, response):
    if request.user.is_authenticated():
        response.set_cookie('poke_radio_user_id', request.user.id)
    return response


@login_required
def home(request):
    c = {
        'user_id': request.user.id,
    }
    return render(request, 'home/index.html', c)
