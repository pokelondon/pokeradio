import json
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView
from django.views.generic.base import ContextMixin

from pokeradio.history.models import ArchiveTrack


class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        c = super(Index, self).get_context_data(**kwargs)
        blacklist = ArchiveTrack.blacklist.all().values_list('spotify_href',
                                                              flat=True)
        if len(blacklist) == 1:
            blacklist = [blacklist[0], ]
        c['blacklist'] = json.dumps(map(str, blacklist))
        return c

home = login_required(Index.as_view())


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
