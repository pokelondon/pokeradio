from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, ListView
from django.views.generic.dates import _date_from_string
from django.views.generic.base import ContextMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Sum

from pokeradio.badges import get_badge_manager
from pokeradio.models import AwardedBadge
from pokeradio.views import WeekArchiveRedirect

from .models import Play, Artist, ArchiveTrack
from .patched_generic_views import PatchedWeekArchiveView


bm = get_badge_manager()


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
        context['awarded_badges'] = [bm.get_badge(ab.badge) for ab in awarded_badges]
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


# Most liked songs
vote_archive_tracks = login_required(TopTracks.as_view())

# Dashboard page, links to the current week redirector for different archives
index = login_required(Dashboard.as_view())

# Redirects to different archives, depending on URL for the current week
vote_tracks_index = login_required(WeekArchiveRedirect.as_view(
    pattern='history:vote_archive_tracks', who='me'))
