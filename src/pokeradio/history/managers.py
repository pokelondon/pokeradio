"""
.. module:: pokeradio.history.managers
   :synopsis: Model managers for doing baddas data queries
"""

from django.db.models import Manager, Count



class ArtistManager(Manager):
    use_for_related_fields = True

    def plays(self, **kwargs):
        return super(ArtistManager, self).get_query_set()\
                .annotate(plays=Count('archivetrack__play')).order_by('-plays')


class TrackManager(Manager):
    use_for_related_fields = True

    def plays(self, **kwargs):
        return super(TrackManager, self).get_query_set()\
                .annotate(plays=Count('play')).order_by('-plays')
