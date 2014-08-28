"""
.. module:: pokeradio.scoring
   :synopsis: View some of the Pokeradio models in the admin view
"""

from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Point


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'value', 'created')
    list_filter = ('user', 'created')

    readonly_fields = ('value', 'track_name', 'action', 'user')


admin.site.register(Point, TransactionAdmin)
