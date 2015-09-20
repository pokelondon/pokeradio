from __future__ import division

import json
from datetime import datetime

from django.conf import settings
from django.views.generic import (TemplateView, RedirectView, ListView,
                                  DetailView)
from django.views.generic.dates import _date_from_string
from django.views.generic.base import ContextMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Sum

from pokeradio.badges import BadgeManager
from pokeradio.models import AwardedBadge
from pokeradio.views import WeekArchiveRedirect

from .models import Play, Artist, ArchiveTrack
from .patched_generic_views import PatchedWeekArchiveView


class Dashboard(TemplateView, ContextMixin):
    template_name = 'history/index.html'

    def get_user_favs(self):
        qs = ArchiveTrack.objects\
            .filter(Q(point__isnull=False) &
                    Q(point__vote_from=self.request.user))\
            .annotate(number=Sum('point__value'))\
            .order_by('-number')[:20]
        return qs

    def get_context_data(self, **kwargs):
        context = {}
        context['object_list'] = self.get_user_favs()
        awarded_badges = AwardedBadge.objects.active().filter(user=self.request.user)
        context['awarded_badges'] = \
            [dict(BadgeManager.get_badge(ab.badge).to_dict().items() + {
                'id': ab.pk,
                'note': ab.note,
            }.items()) for ab in awarded_badges]
        context.update(kwargs)
        return super(Dashboard, self).get_context_data(**context)


class TopTracks(PatchedWeekArchiveView):
    """ Week view for top Tracks.
    For everyone or by current user
    """
    template_name = 'history/top_40_tracks.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = True
    model = ArchiveTrack

    ALL = 'all'
    ME = 'me'

    fk_date_field = 'point__created' # from patched base class

    def filter_queryset_by_user(self, **lookup):
        if self.ALL == self.who:
            return self.model.objects.filter(Q(point__isnull=False) &
                                             Q(**lookup))
        else:
            return self.model.objects.filter(
                    Q(point__isnull=False) &
                    Q(point__action='TRACK_LIKED') &
                    Q(point__vote_from=self.request.user) &
                    Q(**lookup))

    def annotate_queryset(self, qs):
        return qs.annotate(number=Sum('point__value'))\
                         .order_by('-number')[:20]

    def dispatch(self, request, *args, **kwargs):
        self.who = kwargs.get('who', 'all')
        return super(TopTracks, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(TopTracks, self).get_context_data(**kwargs)
        c['who'] = self.who
        c['object_list'] = self.annotate_queryset(kwargs['object_list'])
        return c

    def get_dated_queryset(self, ordering=None, **lookup):
        """ User filtering done in this function by filter_queryset_by_user
        to use the Q object to keep the conditionals working
        """
        date_field = self.get_date_field()
        allow_future = self.get_allow_future()
        allow_empty = self.get_allow_empty()

        qs = self.filter_queryset_by_user(**lookup)

        paginate_by = self.get_paginate_by(qs)

        return qs


class TrackDetail(DetailView):
    model = ArchiveTrack

    def get_context_data(self, **kwargs):
        c = super(TrackDetail, self).get_context_data(**kwargs)
        c['observations'] = []
        count = Play.objects.filter(track=c['object'])\
                .extra(select={'month': 'MONTH(created)',
                               'year': 'YEAR(created)'})\
                .values('month', 'year')\
                .annotate(count=Count('id'))

        time_series = [{'date': '{month}-{year}'.format(**i), \
                        'value': i['count']} for i in count]
        c['time_series'] = json.dumps(time_series)

        c['first_play'] = Play.objects.filter(track=c['object'])\
                .order_by('created').first()

        if c['first_play'].user == self.request.user:
            c['observations'].append('You brought {} to POKE'.format(c['object'].name))

        user_plays = c['object'].play_set.all()\
                .values('user')\
                .annotate(plays=Count('user'))\
                .order_by('-plays')

        c['user_plays'] = user_plays

        ave_plays = (sum([p['plays'] for p in user_plays]) / len(user_plays))
        for i in user_plays:
            if i['user'] == self.request.user.id:
                if i['plays'] > ave_plays:
                    c['observations'].append('You play this quite a bit')

        c['score'] = c['object'].point_set.all()\
                .aggregate(score=Sum('value'))['score']

        c['plays'] = Play.objects.filter(track=c['object'])

        c['ave_score'] = c['score'] / c['plays'].count()

        return c


class TrackLisingByPlays(ListView):
    model = ArchiveTrack
    template_name = 'history/archivetrack_list.html'

    def get_queryset(self):
        res = ArchiveTrack.objects.select_related('Play').all()\
                .annotate(count=Count('play', score=Sum('point__value')))\
                .order_by('-count')[:100]

        return res



# Most liked songs
vote_archive_tracks = login_required(TopTracks.as_view())

# Dashboard page, links to the current week redirector for different archives
index = login_required(Dashboard.as_view())

# Redirects to different archives, depending on URL for the current week
vote_tracks_index = login_required(WeekArchiveRedirect.as_view(
    pattern='history:vote_archive_tracks', who='me'))

track_detail = TrackDetail.as_view()
track_listing = TrackLisingByPlays.as_view()
