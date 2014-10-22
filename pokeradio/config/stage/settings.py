"""
.. module:: pokeradio.config.common.settings
   :synopsis: Stage environment settings.
"""

import errno
import os

from ..common.settings import *

""" Google OAuth Creds """
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '190611052995-kbesr8siuvgbhitaca0i6qgt8h3mji6j.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'gjvMjvImqxYOYvNq14XLbZVY'
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = 'pokelondon.com, gmail.com'

""" Debugging (default True for local environment) """
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

""" Paths """
STATIC_ROOT = join(PROJECT_ROOT, '..', '..', '..', 'static')
MEDIA_ROOT = join(PROJECT_ROOT, '..', '..', '..', 'media')
LOG_ROOT = join(PROJECT_ROOT, '..', '..', '..', 'logs')
ALBUM_ART_BASE_DIR = join(MEDIA_ROOT, 'albumart')
USER_PROFILE_PICTURES_BASE_DIR = join(MEDIA_ROOT, 'profilepictures')

""" Create dirs encase they don't exist """
for path in [STATIC_ROOT, MEDIA_ROOT, LOG_ROOT]:
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

""" Databases (default is mysql) """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pokeradio_stage',
        'USER': 'pokeradio_stage',
        'PASSWORD': 'pokeradio_stage',
        'HOST': 'pradvpc.c6sdj13huel1.eu-west-1.rds.amazonaws.com'
    }
}

""" Admins """
ADMINS = (('Developers', 'developers@pokelondon.com'),)
MANAGERS = ADMINS

""" Cacheing (default is dummy, see django docs) """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'object_cache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'prad_stage',
    }
}

""" REDIS PUBSUB """
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

BROKER_URL = 'redis://{0}:{1}/{2}'.format(
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB)

""" DEV socket io url"""
SOCKETIO_CLIENT_URL = '/app'

""" Dweet device name """
DWEET_NAME = 'pokeradio_stage'

POKERADIO_SKIP_THRESHOLD = -1
