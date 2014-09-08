import json
from random import randint
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import (TemplateView, RedirectView, WeekArchiveView,
                                  View)
from django.views.generic.dates import DateMixin, WeekMixin, _date_from_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Sum

from pokeradio.views import WeekArchiveRedirect

from .models import Point


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

    def get_context_data(self, **kwargs):
        context = {}
        context['my_total'] = self.model.objects.total(user=self.request.user)
        context.update(kwargs)
        return super(StatementView, self).get_context_data(**context)


class Leaderboard(WeekArchiveView):
    template_name = 'scoring/leaderboard.html'
    model = Point
    date_field = 'created'

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Leaderboard'):
            self.template_name = 'coming_soon.html'
        return super(Leaderboard, self).get(request, *args, **kwargs)

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
        if len(object_list) < 1:
            return (None, object_list, {
                'week': date,
                'next_week': self.get_next_week(date),
                'previous_week': self.get_previous_week(date),
            })


        # Get the highest value
        max_value = float(max(object_list, key=lambda i: i['net'])['net'])

        # Find percentage of max value for the week
        for k, v in enumerate(object_list):
            # Percent. /2 to fill half the width
            object_list[k]['dislikes_percent'] = v['dislikes'] / max_value * 50
            object_list[k]['likes_percent'] = v['likes'] / max_value * 50
            object_list[k]['net_percent'] = v['net'] / max_value * 50

        # Return navidational datetime objects as well for traversing other
        # weeks in the template
        return (None, object_list, {
            'week': date,
            'next_week': self.get_next_week(date),
            'previous_week': self.get_previous_week(date),
            'max_value': max_value,
        })


class GraphDataView(View):

    node_index_lookup = {}

    def get_users(self):
        users = User.objects.filter(point__isnull=False).distinct()

        nodes = []
        for i, val in enumerate(users):
            self.node_index_lookup[val.id] = i
            nodes.append({'id': int(val.id), 'name': val.get_full_name()})
        return nodes

    def get_counts(self):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM (
            SELECT scoring_point.action, voter.id as voter_id, dj.id as dj_id, count(scoring_point.action) as num
                FROM scoring_point
                LEFT JOIN  auth_user as voter ON (voter.id = scoring_point.vote_from_id)
                LEFT JOIN  auth_user as dj ON (dj.id = scoring_point.user_id)
                #WHERE scoring_point.action = 'TRACK_LIKED'
                GROUP BY voter.id, scoring_point.action, dj.id
                ORDER BY scoring_point.action, voter.first_name) as T1
            WHERE T1.num > 8
        """)
        rows = cursor.fetchall()

        return rows

    def get(self, request):
        nodes = self.get_users()
        links = []
        for i in self.get_counts():
            if i[0] == u'TRACK_DISLIKED':
                val = int(i[3]) * -1
            else:
                val = int(i[3])

            try:
                links.append({"source": self.node_index_lookup[int(i[1])],
                              "target": self.node_index_lookup[int(i[2])],
                              "value": val})
            except KeyError:
                pass


        payload = {'links': links, 'nodes': nodes}

        return HttpResponse(json.dumps(payload),
                            content_type="application/json")


class MatrixDataView(GraphDataView):
    def get(self, request):
        users = User.objects.all()
        matrix = [[0 for i in range(len(users))] for j in range(len(users))]

        for rownum, obj in enumerate(users):
            # Each row is a user's likes of other users
            for colnum, jobj in enumerate(users):
                likes = Point.objects.filter(vote_from=jobj, user_id=obj)\
                        .aggregate(Sum('value'))['value__sum']
                likes = likes if likes else 0
                # TODO something about negatives
                matrix[rownum][colnum] = likes if likes > 0 else 0

        payload = {'links': matrix,
                   'nodes': [u.get_full_name() for u in users]}

        return HttpResponse(json.dumps(payload),
                            content_type="application/json")


# Index views to redirect to the weekly archives
points_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:points_week'))

# Week archive views, filtered by current user
points_week = login_required(StatementView.as_view())

# Dashboard View
index = login_required(
        TemplateView.as_view(template_name='scoring/index.html'))

# Leaderboard
leaderboard = login_required(Leaderboard.as_view())
leaderboard_index = login_required(WeekArchiveRedirect.as_view(
    pattern='scoring:leaderboard'))

force_graph_json = GraphDataView.as_view()
wheel_graph_json = MatrixDataView.as_view()
