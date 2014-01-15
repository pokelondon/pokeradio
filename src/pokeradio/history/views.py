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


class WeekView(WeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'history/play_archive_week.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = False

    def get_queryset(self):
        return ArchiveTrack.objects.select_related().all()

play_archive_week = login_required(WeekView.as_view())
