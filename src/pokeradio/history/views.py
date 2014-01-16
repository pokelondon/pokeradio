from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from django.views.generic.dates import _date_from_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Play, Artist, ArchiveTrack
from .patched_generic_views import PatchedWeekArchiveView


class ThisWeek(RedirectView):
    """ Redirect to WeekArchiveView for the current week
    """

    permanent = False

    def get_redirect_url(self, who='all', archive='tracks', **kwargs):
        now = datetime.now()
        kwargs={'year': now.year, 'week': now.strftime('%U'), 'who': who}
        return reverse('history:play_archive_{0}'.format(archive),
                       kwargs=kwargs)


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

    def get_queryset(self):
        if self.ALL == self.who:
            return self.model.objects.plays()
        else:
            return self.get_personalised_queryset()

    def get_personalised_queryset(self):
        """ Adding user clause to the query on the play foreign key
        """
        return self.model.objects.plays().filter(
                play__user=self.request.user)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(WeekView, self).get_context_data(**kwargs)
        c['who'] = self.who
        c['archive'] = self.archive
        return c


class WeekViewArtists(WeekView):
    """ Overrides for doing an artist query
    """

    fk_date_field = 'archivetrack__play__created' # from patched base class
    model = Artist
    archive = 'artists'

    def get_personalised_queryset(self):
        """ Adding user clause to the query on the play foreign key
        Normal query is the same as ancestor class
        """
        return self.model.objects.plays().filter(
                archivetrack__play__user=self.request.user)


# WeekView archive of the top tracks for the logged in user or everyone
play_archive_tracks = login_required(WeekView.as_view())

# WeekView Decendant, lists top artists for the logged in user or everyone
play_archive_artists = login_required(WeekViewArtists.as_view())

# Dashboard page, links to the current week redirector for different archives
index = login_required(
        TemplateView.as_view(template_name='history/index.html'))

# Redirects to different archives, depending on URL for the current week
week_index = login_required(ThisWeek.as_view())

