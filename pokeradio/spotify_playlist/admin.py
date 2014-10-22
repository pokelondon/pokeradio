from django.contrib import admin

from .models import Credential


class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'playlist_id')


admin.site.register(Credential, CredentialAdmin)
