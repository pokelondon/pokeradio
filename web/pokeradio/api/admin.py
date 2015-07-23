"""
.. module:: pokeradio.api.admin
   :synopsis: View user API tokens in the admin view
"""

from django.contrib import admin

from .models import Token


admin.site.register(Token)
