import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import (TemplateView, RedirectView, WeekArchiveView,
                                  View)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import connection

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

class GraphDataView(View):
    def get(self, request):
        users = User.objects.all()

        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM (
            SELECT scoring_point.action, voter.id as voter_id, dj.id as dj_id, count(scoring_point.action) as num
                FROM scoring_point
                LEFT JOIN  auth_user as voter ON (voter.id = scoring_point.vote_from_id)
                LEFT JOIN  auth_user as dj ON (dj.id = scoring_point.user_id)
                WHERE scoring_point.action = 'TRACK_LIKED'
                GROUP BY voter.id, scoring_point.action, dj.id
                ORDER BY scoring_point.action, voter.first_name) as T1
            WHERE T1.num > 1
        """)
        rows = cursor.fetchall()

        node_index_lookup = {}
        nodes = []
        for i, val in enumerate(users):
            node_index_lookup[val.id] = i
            nodes.append({'id': int(val.id), 'name': val.get_full_name()})

        links = []
        for i in rows:
            if i[0] == u'TRACK_DISLIKED':
                val = int(i[3]) * -1
            else:
                val = int(i[3])
            links.append({"source": node_index_lookup[int(i[1])], "target": node_index_lookup[int(i[2])], "value": val})


        payload = {'links': links,
                   'nodes': nodes}

        return HttpResponse(json.dumps(payload),
                            content_type="application/json")


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

graph_json = GraphDataView.as_view()
