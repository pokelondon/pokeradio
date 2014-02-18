from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import RedirectView, TemplateView
from django.views.generic.base import ContextMixin

from pokeradio.scoring.models import Point


class HomeView(TemplateView, ContextMixin):
    template_name = 'home/index.html'

    def get_leaderboard(self):
        now = datetime.now()
        a_week = timedelta(weeks=4)
        this_week = [now - a_week, now]

        qs = User.objects.all()
        object_list = []

        for i in qs:
            points = i.point_set.filter(created__range=this_week)
            likes = points.filter(action=Point.TRACK_LIKED).count()
            dislikes = points.filter(action=Point.TRACK_DISLIKED).count()
            if likes < 1 or likes - dislikes < 1:
                continue
            object_list.append({'user': i, 'likes': likes,
                                'dislikes': dislikes})
        items = sorted(object_list, key=lambda i: i['likes'])
        items.reverse()
        return items[:5]

    def get_context_data(self, **kwargs):
        c = super(HomeView, self).get_context_data(**kwargs)
        c['leaderboard'] = self.get_leaderboard()
        return c


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

home = login_required(HomeView.as_view())
