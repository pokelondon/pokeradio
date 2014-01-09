from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext as rc
from django.contrib.auth.decorators import login_required
from django.conf import settings

def _base_context(request):
	context = {
	    'socketio_client_url': settings.SOCKETIO_CLIENT_URL
	}
	return context

def _set_user_id(request, response):
	if request.user.is_authenticated():
		response.set_cookie('poke_radio_user_id',request.user.id)
	return response

@login_required
def home(request):
	context = _base_context(request)
	response = render_to_response('home/index.html', context, context_instance=rc(request))
	response =  _set_user_id(request, response)
	return response
	
	


