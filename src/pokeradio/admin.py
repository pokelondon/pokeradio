"""
.. module:: pokeradio.admin
   :synopsis: View some of the Pokeradio models in the admin view
"""
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Track, Profile, Message, AwardedBadge

class TrackAdmin(admin.ModelAdmin):
    search_fields = ('name', 'artist', 'user__first_name', 'user__last_name')
    list_display = ('name', 'artist', 'played', 'user', 'length')
    list_filter = ('played',)


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_to_individuals', )
    search_fields = ('to_be_seen_by__first_name', 'to_be_seen_by__last_name',
                     'text', 'title')

    fieldsets = (
        ('',
            {'fields': ('title', 'text', 'timeout')}),
        ('Broadcast',
            {'fields': ('seenby', ),
             'description': 'Ignore this if it\'s meant for an indiviudal'}),
        ('Targeted',
            {'fields': ('target_to_individuals', 'to_be_seen_by')}),
    )


class AwardedBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'expires', )
    list_filter = ('badge', 'expires', )
    search_fields = ('note', 'user__first_name')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Track, TrackAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(AwardedBadge, AwardedBadgeAdmin)

admin.site.unregister(Site)
