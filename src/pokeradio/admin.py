"""
.. module:: pokeradio.admin
   :synopsis: View some of the Pokeradio models in the admin view
"""
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from .models import Track

class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'played', 'user', 'length')
    list_filter = ('artist', 'user', 'played')


admin.site.register(Track, TrackAdmin)

admin.site.unregister(Group)
admin.site.unregister(Site)

