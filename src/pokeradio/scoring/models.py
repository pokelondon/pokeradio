"""
.. module:: pokeradio.scoring.models
   :synopsis: For storing game state
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class BaseTransaction(models.Model):
    TYPES = (
        ('TRACK_ADD', 'Add track'),
        ('TRACK_LIKED', 'Liked a track'),
        ('TRACK_DISLIKED', 'Had a track disliked'),
        ('TRACK_DISLIKE', 'Disliked a track'),
    )
    user = models.ForeignKey(User)
    value = models.IntegerField(default=0)
    action = models.CharField(max_length=20, choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return '{0} {1}'.format(self.user, self.action)

    def save(self, *args, **kwargs):
        """ Save the cost into a DB field for summing on DB server
        """
        self.value = self._get_cost()
        super(BaseTransaction, self).save(*args, **kwargs)

    def _get_cost(self):
        """ Considering the action, caculate the cost of this transaction
        """
        return getattr(self, self.action)


class Credit(BaseTransaction):
    """ Credits are earnt doing good stuff, and spent by adding tracks.
    """
    # Costs of the available actions
    TRACK_ADD = -1
    TRACK_LIKED = 5
    TRACK_DISLIKED = 0
    TRACK_DISLIKE = -5


class Point(BaseTransaction):
    """ Fake internet points, the DogeCoin of PokeRadio, this sought after
    currency is awarded for legendary DJing, and shit music is punished with
    point deduction.
    """
    # Costs of the available actions
    TRACK_ADD = -1
    TRACK_LIKED = 5
    TRACK_DISLIKED = -2
