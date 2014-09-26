from datetime import datetime, timedelta


class BaseBadge(object):
    slug = ''
    name = ''
    description = ''
    image = ''
    expiry = timedelta(days=1)

    def __unicode__(self):
        return u'{0} badge'.format(self.name)


class LiamBadge(BaseBadge):
    slug = 'liam'
    name = 'Liam'
    description = "Stick with something good! We get it."
    image = 'foo.png'
    expiry = timedelta(days=1)

    def on_add(self, track):
        from pokeradio.models import Track
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(timestamp__gt=epoch, href=track.href) \
                                .exclude(pk=track.pk)
        return previous.count() > 0


class BadgeManager(object):
    _badges = []
    _events = ['add', 'play', 'vote', 'skip', 'login',]

    def __init__(self):
        # instantiate badges
        self._badges.append(LiamBadge())

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

        if AwardedBadge.objects.active(badge=badge.slug, user=user).count() == 0:
            AwardedBadge.objects.create(badge=badge.slug,
                                        user=user,
                                        expires=datetime.today() + badge.expiry)
        return self
