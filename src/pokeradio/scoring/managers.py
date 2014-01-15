"""
.. module:: pokeradio.scoring.managers
   :synopsis: Model managers
"""

from django.db import models


class TransactionManager(models.Manager):
    def total(self, **kwargs):
        return super(TransactionManager, self).get_query_set()\
                .filter(**kwargs).aggregate(models.Sum('value'))['value__sum']
