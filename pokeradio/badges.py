from __future__ import division

from math import ceil
from logging import getLogger

from datetime import datetime, timedelta
from django.db import models

logger = getLogger(__file__)


class BaseBadge(object):
    slug = ''
    name = ''
    description = ''
    delta = timedelta(days=1)

    def __unicode__(self):
        return u'{0} badge'.format(self.name)

    def to_dict(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
        }


class SentimentBaseBadge(BaseBadge):
    # How long to check the running average for * may not be a running average
    # in the way that mathsers call it.
    window_length = 14

    # Factor of average votes to reprensent a threshold
    multiplier = 0.2

    def check_sentiment(self, user):
        from pokeradio.scoring.models import Point
        today = datetime.today().date()
        window = [today - timedelta(days=self.window_length), today]

        this_week = Point.objects.filter(vote_from=user,created__range=window)
        votes_this_week = this_week.count()

        week_sum = this_week.aggregate(models.Sum('value'))['value__sum']
        week_sum = week_sum if week_sum else 0

        average = ceil(week_sum / 5)

        net_today = Point.objects.filter(vote_from=user,
                                    created__startswith=today)\
                            .aggregate(models.Sum('value'))['value__sum']

        net_today = net_today if net_today else 0

        # Scale of difference required
        personal_threshold = ceil(votes_this_week / 5 * self.multiplier) + 2

        difference_from_average = (net_today - average)

        happy = difference_from_average > (personal_threshold -1)
        sad = difference_from_average < -1 * personal_threshold

        return (happy, sad)


class AcidHouseBadge(SentimentBaseBadge):
    slug = 'acidhouse'
    name = 'Acid House'
    description = "Happier than your average for a fortnight"
    delta = timedelta(days=1)

    def on_vote(self, point):
        from pokeradio.scoring.models import Point

        if 0 < point.value:
            happy, sad = self.check_sentiment(point.vote_from)
            awarded = happy
        else:
            awarded = False
        return (awarded, point.vote_from, None)


class CherryBadge(BaseBadge):
    slug = 'cherry'
    name = 'Cherry'
    description = "Played a track for the first time"
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        previous = Track.objects.filter(href=track.href) \
                                .exclude(pk=track.pk)
        return (previous.count() == 0, track.user, track.name)


class EarlyBirdBadge(BaseBadge):
    slug = 'earlybird'
    name = 'Early Bird'
    description = "First play of the day"
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        epoch = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(timestamp__gt=epoch) \
                                .exclude(pk=track.pk)
        return (previous.count() == 0, track.user, track.name)


class EnoBadge(BaseBadge):
    slug = 'eno'
    name = 'Eno'
    description = "Played a track longer than 20 minutes"
    delta = timedelta(days=7)

    def on_add(self, track):
        return (track.length > (20 * 60), track.user, track.name)


class FloridaBadge(BaseBadge):
    slug = 'florida'
    name = 'Florida'
    description = "Your vote caused a track to be binned. Swing state!"
    delta = timedelta(days=1)

    def on_skip(self, point):
        return (True, point.vote_from, point.track_name)


class GrumpyBuggerBadge(SentimentBaseBadge):
    slug = 'grumpybugger'
    name = 'Grumpy Bugger'
    description = "Downvoted more than usual; does someone need a hug?"
    delta = timedelta(days=1)

    def on_vote(self, point):
        from pokeradio.scoring.models import Point

        if 0 > point.value:
            happy, sad = self.check_sentiment(point.vote_from)
            awarded = sad
        else:
            awarded = False
        return (awarded, point.vote_from, None)


class LateNightVibesBadge(BaseBadge):
    slug = 'latenightvibes'
    name = 'Late Night Vibes'
    description = "Played a track after midnight"
    delta = timedelta(days=7)

    def on_add(self, track):
        return (datetime.now().hour >= 0 and datetime.now().hour < 5,
                track.user, track.name)


class LiamBadge(BaseBadge):
    slug = 'liam'
    name = 'Liam'
    description = "Played a track that was already played today"
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(timestamp__gt=epoch, href=track.href) \
                                .exclude(pk=track.pk)
        return (previous.count() > 0, track.user, track.name)


class RickrollBadge(BaseBadge):
    slug = 'rickroll'
    name = 'Rickroll'
    description = "We're no strangers to love..."
    delta = timedelta(days=30)

    def on_add(self, track):
        return (track.artist.lower() == 'rick astley'
                    and 'never gonna give you up' in track.name.lower(),
                track.user, None)


class SwipeBadge(BaseBadge):
    slug = 'swipe'
    name = 'Swipe'
    description = "Played a song that got voted off"
    delta = timedelta(days=1)

    def on_skip(self, point):
        return (True, point.user, point.track_name)


class BadgeManager(object):
    _badges = [
        AcidHouseBadge(),
        CherryBadge(),
        EarlyBirdBadge(),
        EnoBadge(),
        FloridaBadge(),
        GrumpyBuggerBadge(),
        LateNightVibesBadge(),
        LiamBadge(),
        RickrollBadge(),
        SwipeBadge(),
    ]
    _events = ['add', 'delete', 'skip', 'vote',]

    @classmethod
    def get_badge(self, slug):
        for badge in self._badges:
            if badge.slug == slug:
                return badge
        return None

    @classmethod
    def trigger(self, event, instance):
        if event not in self._events:
            raise KeyError("No such event")
        for badge in self._badges:
            try:
                handler = getattr(badge, 'on_' + event)
                result, user, note = handler(instance)
                if result is True:
                    self.apply_badge(badge, user, note)
            except AttributeError:
                pass
        return self

    @classmethod
    def apply_badge(self, badge, user, note):
        from pokeradio.models import AwardedBadge
        expire_at = datetime.today() + badge.delta
        expire_at = expire_at.replace(hour=5, minute=0, second=0)
        if AwardedBadge.objects.active().filter(badge=badge.slug, user=user) \
                                        .count() == 0:
            print "Applying {0} to {1}".format(badge, user)
            AwardedBadge.objects.create(badge=badge.slug,
                                        user=user,
                                        expires=expire_at,
                                        note=note or '')
        else:
            print "User {0} already has {1}".format(user, badge)
        return self
