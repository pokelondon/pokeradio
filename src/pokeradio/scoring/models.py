"""
.. module:: pokeradio.scoring.models
   :synopsis: For storing game state
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save

from .managers import TransactionManager
from .recievers import report_vote, send_light_vote, send_dweet


class BaseTransaction(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    track_name = models.CharField(max_length=100, blank=True, null=True)

    # Managers
    objects = TransactionManager()

    class Meta:
        abstract = True
        ordering = ['-created']

    def __unicode__(self):
        return u'{0} {1}'.format(self.user, self.action)

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

    TRACK_LIKED = 'TRACK_LIKED'
    TRACK_DISLIKED = 'TRACK_DISLIKED'

    TYPES = (
        (TRACK_LIKED, 'Track was liked'),
        (TRACK_DISLIKED, 'Track was disliked'),
    )

    action = models.CharField(max_length=20, choices=TYPES)
    # Prevent multiple votes for the same track from an individual
    vote_from = models.ForeignKey(User, blank=True, null=True,
            related_name='vote_from',
            help_text='Voter, to prevent multiple votes')
    playlist_track = models.ForeignKey('pokeradio.Track', blank=True,
                                       null=True, on_delete=models.SET_NULL)

    # Link to the persistent track obkect for reporting
    archive_track = models.ForeignKey('history.ArchiveTrack',
                                      blank=True, null=True)

    class Meta(BaseTransaction.Meta):
        unique_together = ('vote_from', 'playlist_track')

    def _get_cost(self):
        """ Considering the action, caculate the cost of this transaction
        """
        return settings.POKERADIO_SCORING_POINT.get(self.action, 0)

post_save.connect(report_vote, sender=Point)
post_save.connect(send_light_vote, sender=Point)
post_save.connect(send_dweet, sender=Point)
