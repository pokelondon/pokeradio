"""
.. module:: pokeradio.config.common.settings
   :synopsis: Live environment settings.
"""

import errno
import os

from ..common.settings import *

""" DEV socket io url"""
SOCKETIO_CLIENT_URL = 'http://pokerad.io/app'

""" Google OAuth Creds """
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '727842630129-5qj2uo9p7eqsqvevmm814sr2er1cpf6s.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'AEvnWCmOrEAyGtTkr1WbecZJ'

""" Debugging (default True for local environment) """
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = (
    'pokerad.io',
    'live.pokeradio.poke.pokedev.net',
    'live-pokeradio-poke.pokedev.net',
)

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
        'NAME': 'pokeradio_live',
        'USER': 'pokeradio_live',
        'PASSWORD': 'pokeradio_live',
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
        'KEY_PREFIX': 'prad_live',
    }
}

""" REDIS PUBSUB """
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

BROKER_URL = 'redis://{0}:{1}/{2}'.format(
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB)

""" Sentry Logging using Raven """
DSN = "http://fad70c76e13b479ab33699200a50ae32:4d770ccfe8b242d8b5f78167e38cf720"\
      "@sentry.pokedev.net/16"
SENTRY_DSN = DSN
RAVEN_CONFIG = {'dsn': DSN}
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)
MIDDLEWARE_CLASSES = (
    ('pokeradio.middleware.SentryExceptionMiddleware', )
    + MIDDLEWARE_CLASSES)

""" Logging """
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.raven_compat.handlers.'
                     'SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'socketserver' : {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': True,
        }
    },
}

''' Pusher enabled/disabled '''
USE_PUSHER = True

''' Google analytics '''
ANALYTICS_ENABLED = True
