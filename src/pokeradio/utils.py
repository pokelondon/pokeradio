"""
.. module:: pokeradio.utils
   :synopsis: Common utility helper functions.
"""

from django.conf import settings


def debug_toolbar_callback(request):
    return settings.DEBUG