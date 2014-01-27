from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from pokeradio.history.models import Play


class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        now = datetime.now()
        a_week = timedelta(weeks=1)
        this_week = [now - a_week, now]
        qs = Play.objects.filter(created__range=this_week)
        hours = sum([p.track.length for p in qs]) / 60 / 60
        print 'Music played this week:', hours, 'hrs', len(qs), 'Tracks'
