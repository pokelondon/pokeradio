from datetime import datetime, timedelta
from django.db import models


class BaseBadge(object):
    slug = ''
    name = ''
    description = ''
    expiry = timedelta(days=1)

    def __unicode__(self):
        return u'{0} badge'.format(self.name)

    def to_dict(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
        }


class AcidHouseBadge(BaseBadge):
    slug = 'acidhouse'
    name = 'Acid House'
    description = "Super happy this week - lots of upvotes"
    delta = timedelta(days=7)

    def on_vote(self, point):
        from pokeradio.scoring.models import Point
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) \
                - self.delta
        upvote_count = Point.objects.filter(vote_from=point.vote_from,
                                            created__gte=epoch,
                                            action=Point.TRACK_LIKED).count()
        return (upvote_count >= 10, point.vote_from)


class BackpedalBadge(BaseBadge):
    slug = 'backpedal'
    name = 'Backpedal'
    description = "Delete a track you added"
    delta = timedelta(days=7)

    def on_delete(self, track):
        return (True, track.user)


class CherryBadge(BaseBadge):
    slug = 'cherry'
    name = 'Cherry'
    description = "Played a track for the first time"
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        previous = Track.objects.filter(href=track.href) \
                                .exclude(pk=track.pk)
        return (previous.count() == 0, track.user)


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
        return (previous.count() == 0, track.user)


class EnoBadge(BaseBadge):
    slug = 'eno'
    name = 'Eno'
    description = "Played a track longer than 20 minutes"
    delta = timedelta(days=7)

    def on_add(self, track):
        return (track.length > (20 * 60), track.user)


class FloridaBadge(BaseBadge):
    slug = 'florida'
    name = 'Florida'
    description = "Your vote caused a track to be binned. Swing state!"
    delta = timedelta(days=7)

    def on_skip(self, point):
        return (True, point.vote_from)


class GrumpyBuggerBadge(BaseBadge):
    slug = 'grumpybugger'
    name = 'Grumpy Bugger'
    description = "Gave a lot of downvotes this week"
    delta = timedelta(days=7)

    def on_vote(self, point):
        from pokeradio.scoring.models import Point
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) \
                - self.delta
        downvote_count = Point.objects.filter(vote_from=point.vote_from,
                                              created__gte=epoch,
                                              action=Point.TRACK_DISLIKED).count()
        return (downvote_count >= 10, point.vote_from)


class LateNightVibesBadge(BaseBadge):
    slug = 'latenightvibes'
    name = 'Late Night Vibes'
    description = "Played a track after midnight"
    delta = timedelta(days=7)

    def on_add(self, track):
        return (datetime.now().hour >= 0 and datetime.now().hour < 5, track.user)


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
        return (previous.count() > 0, track.user)


class RickrollBadge(BaseBadge):
    slug = 'rickroll'
    name = 'Rickroll'
    description = "Never gonna give you up..."
    delta = timedelta(days=30)

    def on_add(self, track):
        return (track.artist.lower() == 'rick astley'
                    and 'never gonna give you up' in track.name.lower(),
                track.user)


class SwipeBadge(BaseBadge):
    slug = 'swipe'
    name = 'Swipe'
    description = "Played a song that got voted off"
    delta = timedelta(days=7)

    def on_skip(self, point):
        return (True, point.playlist_track.user)


class BadgeManager(object):
    _badges = []
    _events = ['add', 'delete', 'skip', 'vote',]

    def __init__(self):
        # instantiate badges
        self._badges.append(AcidHouseBadge())
        self._badges.append(BackpedalBadge())
        self._badges.append(CherryBadge())
        self._badges.append(EarlyBirdBadge())
        self._badges.append(EnoBadge())
        self._badges.append(FloridaBadge())
        self._badges.append(GrumpyBuggerBadge())
        self._badges.append(LateNightVibesBadge())
        self._badges.append(LiamBadge())
        self._badges.append(RickrollBadge())
        self._badges.append(SwipeBadge())

    def get_badge(self, slug):
        for badge in self._badges:
            if badge.slug == slug:
                return badge
        return None

    def trigger(self, event, instance):
        if event not in self._events:
            raise KeyError("No such event")
        for badge in self._badges:
            try:
                handler = getattr(badge, 'on_' + event)
                result, user = handler(instance)
                if result is True:
                    self.apply_badge(badge, user)
            except AttributeError:
                pass
        return self

    def apply_badge(self, badge, user):
        from pokeradio.models import AwardedBadge
        print "Applying {0} to {1}".format(badge, user)

        if AwardedBadge.objects.active().filter(badge=badge.slug, user=user).count() == 0:
            AwardedBadge.objects.create(badge=badge.slug,
                                        user=user,
                                        expires=datetime.today() + badge.delta)
        return self


bm = False


def get_badge_manager():
    global bm
    if bm is False:
        bm = BadgeManager()
    return bm
