from datetime import datetime, timedelta


class BaseBadge(object):
    slug = ''
    name = ''
    description = ''
    image = ''
    expiry = timedelta(days=1)

    def __unicode__(self):
        return u'{0} badge'.format(self.name)


class CherryBadge(BaseBadge):
    slug = 'cherry'
    name = 'Cherry'
    description = "Played a track for the first time"
    image = 'foo.png'
    delta = timedelta(days=7)

    def on_add(self, track):
        from pokeradio.models import Track
        previous = Track.objects.filter(href=track.href) \
                                .exclude(pk=track.pk)
        return previous.count() == 0


class EarlyBirdBadge(BaseBadge):
    slug = 'earlybird'
    name = 'Early Bird'
    description = "First play of the day"
    image = 'foo.png'
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        epoch = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(timestamp__gt=epoch) \
                                .exclude(pk=track.pk)
        return previous.count() == 0


class EnoBadge(BaseBadge):
    slug = 'eno'
    name = 'Eno'
    description = "Played a track longer than 20 minutes"
    image = 'foo.png'
    delta = timedelta(days=7)

    def on_add(self, track):
        return track.length > (20 * 60)


class LateNightVibesBadge(BaseBadge):
    slug = 'latenightvibes'
    name = 'Late Night Vibes'
    description = "Played a track after midnight"
    image = 'foo.png'
    delta = timedelta(days=7)

    def on_add(self, track):
        return (datetime.now().hour >= 0 and datetime.now().hour < 5)


class LiamBadge(BaseBadge):
    slug = 'liam'
    name = 'Liam'
    description = "Played a track that was already played today"
    image = 'foo.png'
    delta = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(timestamp__gt=epoch, href=track.href) \
                                .exclude(pk=track.pk)
        return previous.count() > 0


class RickrollBadge(BaseBadge):
    slug = 'rickroll'
    name = 'Rickroll'
    description = "Never gonna give you up..."
    image = 'foo.png'
    delta = timedelta(days=30)

    def on_add(self, track):
        return (track.artist.lower() == 'rick astley'
                and 'never gonna give you up' in track.name.lower())


class SwipeBadge(BaseBadge):
    slug = 'swipe'
    name = 'Swipe'
    description = "Played a song that got more than 5 dislikes"
    image = 'foo.png'
    delta = timedelta(days=7)

    def on_vote(self, vote):
        # WIP
        return False


class BadgeManager(object):
    _badges = []
    _events = ['add', 'play', 'vote', 'skip', 'login',]

    def __init__(self):
        # instantiate badges
        self._badges.append(CherryBadge())
        self._badges.append(EarlyBirdBadge())
        self._badges.append(EnoBadge())
        self._badges.append(LateNightVibesBadge())
        self._badges.append(LiamBadge())
        self._badges.append(RickrollBadge())
        self._badges.append(SwipeBadge())

    def get_badge(slug):
        for badge in self._badges:
            if badge.slug == slug:
                return badge
        return None

    def trigger(self, event, instance, user):
        if event not in self._events:
            raise KeyError("No such event")
        for badge in self._badges:
            try:
                handler = getattr(badge, 'on_' + event)
                if (handler(instance)) is True:
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
