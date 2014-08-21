from django.db.models import Manager, Q


class TrackManager(Manager):

    def new(self, *args, **kwargs):
        try:
            return super(TrackManager, self).get_queryset(*args, **kwargs)\
                .filter(played__exact=False)[:1][0]
        except (ObjectDoesNotExist, IndexError):
            return None
