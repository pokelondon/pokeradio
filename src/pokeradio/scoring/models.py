"""
.. module:: pokeradio.scoring.models
   :synopsis: For storing game state
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .managers import TransactionManager


class BaseTransaction(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    track_name = models.CharField(max_length=50, blank=True, null=True)

    # Managers
    objects = TransactionManager()

    class Meta:
        abstract = True
        ordering = ['-created']

    def __unicode__(self):
        return '{0} {1}'.format(self.user, self.action)

    def save(self, *args, **kwargs):
        """ Save the cost into a DB field for summing on DB server
        """
        if not self.pk:
            self.value = self._get_cost()
        super(BaseTransaction, self).save(*args, **kwargs)


class Credit(BaseTransaction):
    """ Credits are earnt doing good stuff, and spent by adding tracks.
    """

    TYPES = (
        ('TRACK_ADD', 'Add track'),
        ('TRACK_DISLIKE', 'Disliked a track'),
        ('CREDIT', 'Credit allowance'),
        ('REFUND', 'Refund'),
    )

    action = models.CharField(max_length=20, choices=TYPES)

    def _get_cost(self):
        """ Considering the action, caculate the cost of this transaction
        """
        return settings.POKERADIO_SCORING_CREDIT.get(self.action, 0)


class Point(BaseTransaction):
    """ Fake internet points, the DogeCoin of PokeRadio, this sought after
    currency is awarded for legendary DJing, and shit music is punished with
    point deduction.
    """

    TYPES = (
        ('TRACK_LIKED', 'Track was liked'),
        ('TRACK_DISLIKED', 'Track was disliked'),
    )

    action = models.CharField(max_length=20, choices=TYPES)

    def _get_cost(self):
        """ Considering the action, caculate the cost of this transaction
        """
        return settings.POKERADIO_SCORING_POINT.get(self.action, 0)
