from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, WeekArchiveView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from pokeradio.views import WeekArchiveRedirect

from .models import Point, Credit


class StatementView(WeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'scoring/credit_archive_week.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = False
    model = Credit

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """ Additional context data """
        c = super(StatementView, self).get_context_data(**kwargs)
        c['my_credits'] = self.model.objects.total(user=self.request.user)
        return c


# Index views to redirect to the weekly archives
credits_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:credits_week'))
points_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:points_week'))

# Week archive views, filtered by current user
credits_week = login_required(StatementView.as_view(model=Credit,
    template_name='scoring/credit_archive_week.html'))
points_week = login_required(StatementView.as_view(model=Point,
    template_name='scoring/point_archive_week.html'))

# Dashboard View
index = login_required(
        TemplateView.as_view(template_name='scoring/index.html'))
