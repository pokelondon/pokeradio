from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, WeekArchiveView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Point, Credit


class ThisWeek(RedirectView):
    """ Redirect to WeekArchiveView for the current week
    """
    permanent = False
    pattern = 'scoring:statement_week'

    def get_redirect_url(self, **kwargs):
        now = datetime.now()
        return reverse(self.pattern, kwargs={'year': now.year,
                                             'week': now.strftime('%U')})



class StatementView(WeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'scoring/credit_archive_week.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = False

    def get_queryset(self):
        return Credit.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(StatementView, self).get_context_data(**kwargs)
        c['my_credits'] = Credit.objects.total(user=self.request.user)
        return c


class PointsView(WeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'scoring/credit_archive_week.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = False

    def get_queryset(self):
        return Point.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(PointsView, self).get_context_data(**kwargs)
        c['my_credits'] = Point.objects.total(user=self.request.user)
        return c


statement_index = login_required(ThisWeek.as_view())
points_index = login_required(ThisWeek.as_view(pattern='scoring:points_week'))

statement_week = login_required(StatementView.as_view())
points_week = login_required(PointsView.as_view())

index = login_required(
        TemplateView.as_view(template_name='scoring/index.html'))
