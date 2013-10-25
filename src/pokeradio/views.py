from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

def _base_context(request):
	context = {
	    'socketio_client_url': settings.SOCKETIO_CLIENT_URL
	}
	return context


@login_required
def home(request):
	context = _base_context(request)
	return render(request,'home/index.html',context)

