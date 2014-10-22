"""
.. module:: pokeradio.api.models
   :synopsis: For storing user API tokens
"""

from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    user = models.ForeignKey(User,
                             related_name='tokens')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.token, self.user)
