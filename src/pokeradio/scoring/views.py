from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView, RedirectView, WeekArchiveView
from django.views.generic.dates import DateMixin, WeekMixin, _date_from_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pokeradio.views import WeekArchiveRedirect

from .models import Point, Credit


class StatementView(WeekArchiveView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'scoring/point_archive_week.html'
    date_field = 'created'
    allow_empty = True
    make_object_list = True
    allow_future = False
    model = Point

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class Leaderboard(WeekArchiveView):
    template_name = 'scoring/leaderboard.html'
    model = Point
    date_field = 'created'

    def get_dated_items(self):
        """ Special dated query, that filters on the foreign key model Point,
        rather than the main model of the queryset User
        """
        # From Base Weekarchiveview
        year = self.get_year()
        week = self.get_week()
        date_field = self.get_date_field()
        week_format = self.get_week_format()
        week_start = {
            '%W': '1',
            '%U': '0',
        }[week_format]
        date = _date_from_string(year, self.get_year_format(),
                                week_start, '%w',
                                week, week_format)
        since = self._make_date_lookup_arg(date)
        until = self._make_date_lookup_arg(self._get_next_week(date))
        period = [since, until]

        # Special Query
        qs = User.objects.select_related('point').all()
        object_list = []

        for i in qs:
            points = i.point_set.filter(created__range=period)
            likes = points.filter(action=Point.TRACK_LIKED).count()
            dislikes = points.filter(action=Point.TRACK_DISLIKED).count()
            if likes + dislikes > 0:
                object_list.append({'user': i, 'likes': likes,
                    'dislikes': dislikes, 'net': likes - dislikes})

        # Get the highest value
        max_value = float(max(object_list, key=lambda i: i['likes'])['likes'])

        # Find percentage of max value for the week
        for k, v in enumerate(object_list):
            # Percent. /2 to fill half the width
            object_list[k]['dislikes_percent'] = v['dislikes'] / max_value * 50
            object_list[k]['likes_percent'] = v['likes'] / max_value * 50

        # Return navidational datetime objects as well for traversing other
        # weeks in the template
        return (None, object_list, {
            'week': date,
            'next_week': self.get_next_week(date),
            'previous_week': self.get_previous_week(date),
            'max_value': max_value,
        })

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)
        return super(Leaderboard, self).get_context_data(**context)


# Index views to redirect to the weekly archives
points_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:points_week'))

# Week archive views, filtered by current user
points_week = login_required(StatementView.as_view())

# Dashboard View
index = login_required(
        TemplateView.as_view(template_name='scoring/index.html'))

# TODO
leaderboard = login_required(Leaderboard.as_view())
leaderboard_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:leaderboard'))
