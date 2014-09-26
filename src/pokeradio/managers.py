from datetime import datetime
from django.db.models import Manager, Q
from django.core.exceptions import ObjectDoesNotExist


class AwardedBadgeManager(Manager):
    def active(self, *args, **kwargs):
        return super(AwardedBadgeManager, self).get_queryset(*args, **kwargs) \
            .filter(expires__gt=datetime.today())


class TrackManager(Manager):

    def new(self, *args, **kwargs):
        try:
            return super(TrackManager, self).get_queryset(*args, **kwargs)\
                .filter(played__exact=False)[:1][0]
        except (ObjectDoesNotExist, IndexError):
            return None
