from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, ListView
from django.views.generic.dates import _date_from_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Sum

from pokeradio.views import WeekArchiveRedirect

from .models import Play, Artist, ArchiveTrack
from .patched_generic_views import PatchedWeekArchiveView


class WeekView(PatchedWeekArchiveView):
    """ Week view for top Tracks
    """
    template_name = 'history/play_archive_week.html'
    date_field = 'created'
    fk_date_field = 'play__created' # from patched base class
    allow_empty = True
    make_object_list = True
    allow_future = False
    model = ArchiveTrack
    archive = 'tracks'

    ALL = 'all'
    ME = 'me'

    def dispatch(self, request, *args, **kwargs):
        self.who = kwargs.get('who', 'all')
        return super(WeekView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(WeekView, self).get_context_data(**kwargs)
        c['who'] = self.who
        c['archive'] = self.archive
        c['object_list'] = self.annotate_queryset(kwargs['object_list'])
        return c

    def annotate_queryset(self, qs):
        """ Finally annotate the filtered QS with stuff to count plays
        just before it gets sent to the view after the Week Archive View
        has added filters and stuff
        """
        res = qs.annotate(plays=Count('play')).order_by('-plays')
        return res

    def get_dated_queryset(self, ordering=None, **lookup):
        """ Dont add filters to get_queryset, or it will confuse things,
        Date query needs to be part of a Q object. So the date filtering is
        done manually as part of this method
        """
        date_field = self.get_date_field()
        allow_future = self.get_allow_future()
        allow_empty = self.get_allow_empty()

        if self.ALL == self.who:
            qs = self.model.objects.filter(**lookup)
        else:
            qs = self.model.objects.filter(Q(play__user=self.request.user) &
                                           Q(**lookup))

        paginate_by = self.get_paginate_by(qs)

        return qs


class WeekViewArtists(WeekView):
    """ Overrides for doing an artist query
    """

    fk_date_field = 'archivetrack__play__created' # from patched base class
    model = Artist
    archive = 'artists'

    def get_dated_queryset(self, ordering=None, **lookup):
        """ Dont add filters to get_queryset, or it will confuse things,
        Date query needs to be part of a Q object. So the date filtering is
        done manually as part of this method

        lookup is a dict of archivetrack__play__created__gt and ..lt params
        """
        date_field = self.get_date_field()
        allow_future = self.get_allow_future()
        allow_empty = self.get_allow_empty()

        if self.ALL == self.who:
            qs = self.model.objects.filter(**lookup)
        else:
            qs = self.model.objects.filter(
                    Q(archivetrack__play__user=self.request.user) &
                    Q(**lookup))

        paginate_by = self.get_paginate_by(qs)

        return qs

    def annotate_queryset(self, qs):
        return qs.annotate(plays=Count('archivetrack__play'))\
                .order_by('-plays')


class WeekViewVoteTracks(ListView):
    """ Like the artist archive aggregated by plays, this is agregated by
    points. The total of the added up point values gives a score
    """
    template_name = 'history/score_archive.html'
    def get_queryset(self):
            return ArchiveTrack.objects.filter(point__isnull=False)\
                    .annotate(number=Sum('point__value'))\
                    .order_by('-number')[:20]


# WeekView archive of the top tracks for the logged in user or everyone
play_archive_tracks = login_required(WeekView.as_view())

# WeekView Decendant, lists top artists for the logged in user or everyone
play_archive_artists = login_required(WeekViewArtists.as_view())

# Most liked songs
play_archive_artists_votes = login_required(WeekViewVoteTracks.as_view())

# Dashboard page, links to the current week redirector for different archives
index = login_required(
        TemplateView.as_view(template_name='history/index.html'))

# Redirects to different archives, depending on URL for the current week
week_index = login_required(WeekArchiveRedirect.as_view(
    pattern='history:play_archive_tracks', who='me'))

