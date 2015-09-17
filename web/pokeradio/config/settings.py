"""
.. module:: pokeradio.config.settings
   :synopsis: Common project settings, applies to all environments.
"""

import os

from os.path import abspath, join, dirname
from django.core.urlresolvers import reverse_lazy

ENV = os.environ.get('ENV', 'dev')
DEBUG = os.environ.get('DEBUG', True)

""" Object Cache """
CACHE_LEADERBOARD_HP = 120

""" Paths """
PROJECT_ROOT = abspath(join(dirname(__file__), '..', ))
ROOTS_ROOT = abspath(join(dirname(PROJECT_ROOT), '..', 'app'))

STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'public'), ]

LOG_ROOT = join(ROOTS_ROOT, 'logs')
STATIC_ROOT = join(ROOTS_ROOT, 'public')
MEDIA_ROOT = join(ROOTS_ROOT, 'media')

ALBUM_ART_FALLBACK = '/s/img/404-album.jpg'

MEDIA_URL = '/m/'

ALBUM_ART_URL = '{0}/albumart/'.format(MEDIA_URL)

THUMBNAIL_MEDIA_URL = MEDIA_URL

SESSION_COOKIE_AGE = 1209600

""" Urls """
STATIC_URL = '/s/'

ROOT_URLCONF = 'pokeradio.urls'

""" Location """
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = True
USE_L10N = True

""" Image sizes """
THUMBNAIL_SIZE = 195, 195
PROFILE_PICTURE_SIZE = 70,70
AUTH_PROFILE_MODULE = 'pokeradio.Profile'

""" Templates """
TEMPLATE_DIRS = [join(PROJECT_ROOT, 'templates')]
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    # Common django context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    # Custom project context processprs
    'pokeradio.context_processors.domain',
    'pokeradio.context_processors.analytics',
)

""" Middleware """
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware', # After session middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

""" Installed Applications """
INSTALLED_APPS = (
    # Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # Third Party Apps here
    'south',
    'django_extensions',
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    'registration',
    # Project Apps here
    'pokeradio',
    'pokeradio.accounts',
    'pokeradio.scoring',
    'pokeradio.history',
    'pokeradio.api',
    'pokeradio.spotify_playlist',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

#LOGIN_URL = reverse_lazy('accounts:login')
#LOGOUT_URL = reverse_lazy('accounts:logout')

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'

SPOTIFY_LOOKUP_ENDPOINT = 'http://ws.spotify.com/lookup/1/.json?uri=spotify:album:{0}'

""" Credits and Points """
POKERADIO_SCORING_POINT = {
    'TRACK_LIKED': 1,
    'TRACK_DISLIKED': -1,
}

POKERADIO_SKIP_THRESHOLD = -5

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'object_cache': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': 'localhost',
    }
}

""" Dweet device name """
DWEET_NAME = os.environ.get('DWEET_NAME')

""" Google analytics """
ANALYTICS_ENABLED = False
GA_ID = os.environ.get('GA_ID')

""" Redis Pubsub """
REDIS_HOST = os.environ.get('REDIS_1_PORT_6379_TCP_ADDR', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_1_PORT_6379_TCP_PORT', 6379))
REDIS_PASSWORD = ''
REDIS_DB = 0

""" Celery """
BROKER_URL = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

""" Secret Key & Site ID """
SITE_ID = 1
DEFAULT_SECRET_KEY = 'feb53#ep6w)e*0r_1m6b(452@5p_9fil^a-a0h3@&d%iy0_mow'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

""" Databases """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MYSQL_DATABASE'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        'HOST': 'db',
    }
}

""" Pusher Settings """
USE_PUSHER = False
PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID')
PUSHER_KEY = os.environ.get('PUSHER_KEY')
PUSHER_SECRET = os.environ.get('PUSHER_SECRET')

""" Spotify web API """
USE_SPOTIFY_PLAYLIST = False
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_OAUTH_REDIRECT = os.environ.get('SPOTIFY_OAUTH_REDIRECT')

""" Slack """
SLACK = False
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

""" LEDS """
LIGHTS_WEBHOOK_URL = ""

""" Socket Server """
SOCKET_PORT = 80

SOCKETIO_CLIENT_URL = '/app'

CORS_ORIGIN_ALLOW_ALL = True

SOUTH_MIGRATION_MODULES = {
    'oauth2_provider': 'oauth2_provider.south_migrations',
    'registration': 'registration.south_migrations',
}

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

""" User Registration """
REGISTRATION_AUTO_LOGIN = True
ACCOUNT_ACTIVATION_DAYS = 7

domain_whitelist = os.environ.get('REGISTRATION_DOMAIN_WHITELIST', None)
if domain_whitelist:
    REGISTRATION_DOMAIN_WHITELIST = domain_whitelist.split(',')
    REGISTRATION_FORM = 'pokeradio.accounts.forms.RegistrationFormWhiteListDomains'
