"""
.. module:: pokeradio.config.settings
   :synopsis: Common project settings, applies to all environments.
"""

import os

from os.path import abspath, join, dirname

ENV = os.environ.get('ENV', 'dev')
DEBUG = True

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
    #python-social-auth
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
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
    # Social Auth
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
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
    'social.apps.django_app.default',
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    # Project Apps here
    'pokeradio',
    'pokeradio.scoring',
    'pokeradio.history',
    'pokeradio.api',
    'pokeradio.spotify_playlist',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.google.GoogleOAuth2',
    'oauth2_provider.backends.OAuth2Backend',
)

""" GOOGLE AUTH BACKEND"""
SOCIAL_AUTH_GOOGLE_RAISE_EXCEPTIONS = True
RAISE_EXCEPTIONS = True
DEBUG = True

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = 'pokelondon.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_SESSION_EXPIRATION = False

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

SPOTIFY_LOOKUP_ENDPOINT = 'http://ws.spotify.com/lookup/1/.json?uri=spotify:album:{0}'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'pokeradio.accounts.pipeline.get_profile_pic',
)

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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_USER'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'postgres',
        'PORT': 5432,
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

""" Google OAuth Credientials """
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', None)

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
    'default': 'social.apps.django_app.default.south_migrations',
    'oauth2_provider': 'oauth2_provider.south_migrations',
}
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True

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
