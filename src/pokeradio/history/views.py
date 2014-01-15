from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, WeekArchiveView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Play, Artist, ArchiveTrack

class ThisWeek(RedirectView):
    """ Redirect to WeekArchiveView for the current week
    """

    permanent = False

    def get_redirect_url(self, **kwargs):
        now = datetime.now()
        return reverse('history:play_archive_week',
                kwargs={'year': now.year, 'week': now.strftime('%U')})

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

    def get_queryset(self):
        return ArchiveTrack.objects.plays()


play_archive_week = login_required(WeekView.as_view())
