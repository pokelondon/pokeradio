"""
.. module:: pokeradio.config.dev.settings
   :synopsis: Development settings, all developers should use this which is
   designed to be used with the salt / vagrant setup.
"""

import os
import dj_database_url

from ..common.settings import *

""" Spotify web API """
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '9f6b1904b64d49f9ac31e3e36277dfb8')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '5da8784c283547bfb56c530f6ba5eeb5')
SPOTIFY_OAUTH_REDIRECT = os.environ.get('SPOTIFY_OAUTH_REDIRECT', 'http://dev.errkk.co/spotify/oauth_callback/')

POKERADIO_SKIP_THRESHOLD = -1

SLACK = False

""" LEDS """
LIGHTS_WEBHOOK_URL = "http://localhost:8081?token=cFRbuBogZKFNqRZvEyfgIVNk"

# Ipython Notebook, bind to this ip so it can be forwarded
IPYTHON_ARGUMENTS = [
    '--ip=0.0.0.0',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '190611052995-kbesr8siuvgbhitaca0i6qgt8h3mji6j.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'gjvMjvImqxYOYvNq14XLbZVY'
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = 'pokelondon.com, gmail.com'

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

""" Debugging (default True for development environment) """
DEBUG = True
TEMPLATE_DEBUG = DEBUG


""" Cacheing (default is dummy, see django docs) """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'object_cache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ.get('MEMCACHE', '127.0.0.1:11211'),
        'KEY_PREFIX': 'prad_dev',
    }
}

""" REDIS PUBSUB """
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_HOST = os.environ.get('REDIS_HOST', REDIS_HOST)
REDIS_PORT = os.environ.get('REDIS_PORT', REDIS_PORT)

POKERADIO_SKIP_THRESHOLD = -1

""" Use MD5 Password Hashing for Dev - Speeds things up """
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

""" DEV socket io url"""
SOCKETIO_CLIENT_URL = 'http://localhost/app'

""" Dweet device name """
DWEET_NAME = 'pokeradio_dev'



DEFAULT_SECRET_KEY = '3iy-!-d$!pc_ll$#$elg&cpr@*tfn-d5&n9ag=)%#()t$$5%5^'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
