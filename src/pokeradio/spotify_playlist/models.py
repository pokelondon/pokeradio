from django.db import models

from django.contrib.auth.models import User


class Credential(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()
