from datetime import datetime

from pokeradio.models import Track


class BaseBadge(object):
    slug = ''
    name = ''
    description = ''
    image = ''


class LiamBadge(BaseBadge):
    slug = 'liam'
    name = 'Liam'
    description = "Stick with something good! We get it."
    image = 'foo.png'

    def on_add(self, track):
        epoch = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        previous = Track.objects.filter(created__gt=epoch, href=track.href)
        return previous.count() > 0


class BadgeManager(object):
    _badges = []
    _events = ['add', 'play', 'vote', 'skip', 'login',]

    def __init__(self):
        # instantiate badges
        self._badges.append(LiamBadge())

    def trigger(self, event, instance, user_id):
        if event not in self._events:
            raise KeyError("No such event")
        for badge in self._badges:
            try:
                handler = getattr(badge, 'on_' + event)
                if (handler(instance)) is True:
                    self.apply_badge(badge, user_id)
            except AttributeError:
                pass
        return self

    def apply_badge(self, badge, user_id):
        # IOU some ORM code
        return self


# somewhere else in the app...
#bm = BadgeManager()
#bm.trigger('add', track, user_id)
