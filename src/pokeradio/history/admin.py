"""
.. module:: pokeradio.history.admin
   :synopsis: View some of the Pokeradio models in the admin view
"""

from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import ArchiveTrack, Artist, Play


class TrackInline(admin.TabularInline):
    model = ArchiveTrack
    extra = 0


class PlayInline(admin.TabularInline):
    model = Play
    extra = 0
    readonly_fields = ('user', 'created')


class ArtistAdmin(admin.ModelAdmin):
    inlines = (TrackInline, )
    list_display = ('name', 'tracks')

    def tracks(self, obj):
        return obj.archivetrack_set.all().count()


class ArchiveTrackAdmin(admin.ModelAdmin):
    inlines = (PlayInline, )
    list_display = ('name', 'artist', 'plays', 'created')
    search_fields = ('name', 'artist__name')

    def plays(self, obj):
        return obj.play_set.all().count()


admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArchiveTrack, ArchiveTrackAdmin)
