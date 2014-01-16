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

    def get_redirect_url(self, who='all', **kwargs):
        now = datetime.now()
        return reverse('history:play_archive_week',
                kwargs={'year': now.year, 'week': now.strftime('%U'),
                        'who': who})

week_index = login_required(ThisWeek.as_view())


class WeekView(PatchedWeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'history/play_archive_week.html'
    date_field = 'created'
    fk_date_field = 'play__created' # from patched base class
    allow_empty = True
    make_object_list = True
    allow_future = False
    model = ArchiveTrack

    ALL = 'all'
    ME = 'me'

    def dispatch(self, request, *args, **kwargs):
        self.who = kwargs.get('who', 'all')
        return super(WeekView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.ALL == self.who:
            return ArchiveTrack.objects.plays()
        else:
            return ArchiveTrack.objects.plays().filter(
                    play__user=self.request.user)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(WeekView, self).get_context_data(**kwargs)
        c['who'] = self.who
        return c


play_archive_week = login_required(WeekView.as_view())

index = login_required(
        TemplateView.as_view(template_name='history/index.html'))
