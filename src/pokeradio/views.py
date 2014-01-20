from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView


@login_required
def home(request):
    return render(request, 'home/index.html', {})


class WeekArchiveRedirect(RedirectView):
    """ Redirect to a WeekArchiveView for the current week
    """
    permanent = False
    pattern = 'scoring:statement_week'
    who = 'me'

    def get_redirect_url(self, **kwargs):
        now = datetime.now()
        url_params = {'year': now.year, 'week': now.strftime('%U')}
        if 'who' in kwargs:
            url_params['who'] = kwargs.get('who')
        return reverse(self.pattern, kwargs=url_params)
