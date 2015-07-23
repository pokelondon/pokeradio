import requests
import collections
import plotly
import random
import time
import redis

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta

from pokeradio.history.models import *


ws = 'http://ws.spotify.com/lookup/1/.json?uri={0}'


class Year:
    request_count = 0
    SLEEP = 1
    RATE_INTERVAL = 5

    def __init__(self):
        self.r = redis.StrictRedis()

    def get_year(self, spotify_id):
        didsleep = False
        key = 'year:{0}'.format(spotify_id)
        year = self.r.get(key)
        if year:
            return year, didsleep

        else:
            if self.request_count % self.RATE_INTERVAL == 0:
                print "Pause"
                time.sleep(self.SLEEP)
                didsleep = True

            self.request_count += 1
            res = requests.get(ws.format(spotify_id))
            data = res.json()

            try:
                year = data['track']['album']['released']
            except KeyError:
                year = None

            self.r.set(key, year)
            if year:
                return year, didsleep


class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        now = datetime.now()
        a_week = timedelta(weeks=1)
        this_week = [now - a_week, now]

        qs = ArchiveTrack.objects.filter(Q(play__created__range=this_week))\
                .annotate(plays=Count('play')).order_by('-plays')

        consolodated = {}
        total = qs.count()
        y = Year()

        for count, item in enumerate(qs):
            year, didsleep = y.get_year(item.spotify_href)
            if count % 10 == 0:
                print float(count) / total * 100, '%', y.request_count
            if not year:
                pass
            if year in consolodated:
                consolodated[year].append(item)
            else:
                consolodated[year] = [item]

        consolodated = collections.OrderedDict(sorted(consolodated.items()))

        py = plotly.plotly(username_or_email='EricGeorge', key='cp9m5tn1ix')
        l = {'autosize': False,'width': 1200, 'height': 600,
             'showlegend': False,
            'xaxis' : {"linecolor": "rgba(0, 0, 0, 0)","ticks":"",
                        "showgrid": True, "zeroline": False,
                        "showticklabels": True},
            'yaxis' : {"linecolor": "rgba(0, 0, 0, 0)", "ticks": "",
                        "showgrid": True, "zeroline": True,
                        "showticklabels": True}}

        print py.plot([{'y': [len(i) for i in consolodated.values()],
                        'x': consolodated.keys(),
                        'type': 'bar'}], layout=l)

