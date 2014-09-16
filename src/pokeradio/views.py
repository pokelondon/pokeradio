import json
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView
from django.views.generic.base import ContextMixin
from django.db.models import F, Q, Sum

from pokeradio.models import Message
from pokeradio.history.models import ArchiveTrack
from pokeradio.scoring.models import Point
from pokeradio.utils import current_playlist
from django.utils.safestring import mark_safe


class HomeView(TemplateView, ContextMixin):
    template_name = 'home/index.html'

    def get_leaderboard(self):
        today = datetime.today().date()
        td = timedelta(days=1)
        period = [today, today + td]

        """ 
            Return id with a point instead of 
            User.objects.all()
            
        """
        ids = Point.objects.values('user_id').filter(created__range=period)
        qs = User.objects.filter(pk__in=ids)
        object_list = []
        for i in qs:
            points = i.point_set.filter(created__range=period)
            """ if no points move prevent wasted cycle"""
            if not points.exists():
                continue
            likes = points.filter(action=Point.TRACK_LIKED).count()
            dislikes = points.filter(action=Point.TRACK_DISLIKED).count()
            net = likes - dislikes
            if likes < 1 or net < 1:
                continue
            object_list.append({'user': i, 'likes': likes, 'net': net,
                                'dislikes': dislikes})
        items = sorted(object_list, key=lambda i: i['net'])
        items.reverse()
        return items[:5]
        return []
        

    def get_messages(self):
        # General messages for everyone that this user hasn't seen
        messages = Message.objects.exclude(seenby=self.request.user)\
                .filter(target_to_individuals=False)
        for m in messages:
            m.seenby.add(self.request.user)

        data = [m.to_dict() for m in messages]

        # Specific messages for this user
        messages = Message.objects.filter(target_to_individuals=True,
                                          to_be_seen_by=self.request.user)

        for m in messages:
            m.to_be_seen_by.remove(self.request.user)

        data += [m.to_dict() for m in messages]

        return json.dumps(data)

    def get_context_data(self, **kwargs):
        c = super(HomeView, self).get_context_data(**kwargs)

        blacklist = ArchiveTrack.blacklist.all().values_list('spotify_href',
                                                             flat=True)
        initial_playlist = current_playlist()
        if len(blacklist) == 1:
            blacklist = [blacklist[0], ]

        c['initial_playlist'] = mark_safe(json.dumps(initial_playlist))
        c['blacklist'] = json.dumps(map(str, blacklist))
        c['leaderboard'] = self.get_leaderboard()
        c['alerts'] = self.get_messages()
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
