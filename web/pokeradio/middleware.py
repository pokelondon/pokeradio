"""
.. module:: pokeradio.middleware
   :synopsis: Custom django middleware.
"""

from raven.contrib.django.raven_compat.models import sentry_exception_handler


class SentryExceptionMiddleware(object):

    def process_exception(self, request, exception):
        # Make sure the exception signal is fired for Sentry
        sentry_exception_handler(request=request)