"""
.. module:: pokeradio.context_processors
   :synopsis: Custom context processors for returning extra data into
   the request context.
"""

from django.conf import settings
from django.contrib.sites.models import Site
from .models import Brand


def domain(request):
    """ Get current site information.

    :param request: HTTP request data
    :type request: object

    :returns: dict -- current site data
    """

    try:
        current_site = Site.objects.get_current()
    except Site.DoesNotExist:
        current_site = Site.objects.create()
    finally:
        domain = getattr(settings, 'DOMAIN', 'http://%s' % current_site.domain)

    try:
        brand = Brand.objects.all().get()
    except Brand.DoesNotExist:
        brand = Brand.objects.create()

    return {
        'DOMAIN': domain,
        'site': current_site,
        'SOCKETIO_CLIENT_URL': settings.SOCKETIO_CLIENT_URL,
        'BRAND': brand,
    }


def analytics(request):
    """ Get ANALYTICS_ENABLED setting.

    :param request: HTTP request data
    :type request: object

    :returns: dict -- analytics setting
    """
    return {
        'ANALYTICS_ENABLED': settings.ANALYTICS_ENABLED,
        'GA_ID': settings.GA_ID,
    }
