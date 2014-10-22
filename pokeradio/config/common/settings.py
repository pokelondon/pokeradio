"""
.. module:: pokeradio.config.common.settings
   :synopsis: Common project settings, applies to all environments.
"""

from os.path import abspath, join, dirname

""" Object Cache """
CACHE_LEADERBOARD_HP = 120

""" Spotify web API """
SPOTIFY_CLIENT_ID = '9f6b1904b64d49f9ac31e3e36277dfb8'
SPOTIFY_CLIENT_SECRET = '5da8784c283547bfb56c530f6ba5eeb5'
SPOTIFY_OAUTH_REDIRECT = 'http://pokerad.io/spotify/oauth_callback/'


""" Slack """
SLACK = True
DEV_SLACK_WEBHOOK_URL = "https://poke.slack.com/services/hooks/incoming-webhook?token=sASvh1h3UsQFTitVfHwKnvQq"
EVERYONE_SLACK_WEBHOOK_URL = "https://pokelondon.slack.com/services/hooks/incoming-webhook?token=fkRdgxArG8YcGCCGzOdxNz7K"
SLACK_WEBHOOK_URL = EVERYONE_SLACK_WEBHOOK_URL

""" LEDS """
LIGHTS_WEBHOOK_URL = "http://stage.leds.oddish.pokedev.net?token=cFRbuBogZKFNqRZvEyfgIVNk"

""" Paths """
PROJECT_ROOT = abspath(join(dirname(__file__), '..', '..'))
MEDIA_ROOT = join(PROJECT_ROOT,'media')
ALBUM_ART_BASE_DIR = join(MEDIA_ROOT, 'albumart')
USER_PROFILE_PICTURES_BASE_DIR = join(MEDIA_ROOT, 'profilepictures')
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'public'), ]
LOG_ROOT = join(PROJECT_ROOT, 'logs')

SOCKET_PORT = 8001
ALBUM_ART_FALLBACK = '/s/img/404-album.jpg'
SESSION_COOKIE_AGE = 1209600

""" Urls """
STATIC_URL = '/s/'
MEDIA_URL = '/m/'
ALBUM_ART_URL = '/albumart/'
ROOT_URLCONF = 'pokeradio.urls'

""" Secret Key & Site ID """
SITE_ID = 1
SECRET_KEY = 'feb53#ep6w)e*0r_1m6b(452@5p_9fil^a-a0h3@&d%iy0_mow'

""" Location """
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = True
USE_L10N = True

""" Image sizes """
THUMBNAIL_SIZE = 195, 195
PROFILE_PICTURE_SIZE = 70,70

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
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Debug Toolbar
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    #socail auth middleware
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
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
    # Project Apps here
    'pokeradio',
    'pokeradio.scoring',
    'pokeradio.history',
    'pokeradio.api',
    'pokeradio.spotify_playlist',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social.apps.django_app.utils.BackendWrapper'
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

""" Pusher Settings """
PUSHER_APP_ID='72958'
PUSHER_KEY='a991dbecdd488ffe748e'
PUSHER_SECRET='e32f7633c8fbae37da3d'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'pokeradio.utils.debug_toolbar_callback',
}

""" Test Suite """
NOSE_ARGS = [
    '--include=^(can|it|ensure|must|should|specs?|examples?)',
    '--with-spec',
    '--spec-color',
    '-s',
    '--with-coverage',
    '--cover-erase',
    '--cover-package=pokeradio']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SPOTIFY_LOOKUP_ENDPOINT = 'http://ws.spotify.com/lookup/1/.json?uri=spotify:album:{0}'

COVERART_ENDPOINT = 'http://coverartarchive.org/release-group/{0}'

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

""" Dweet device name """
DWEET_NAME = 'pokeradio'


''' Pusher enabled/disabled '''
USE_PUSHER = False

''' Google analytics '''
ANALYTICS_ENABLED = False

""" Celery """
BROKER_URL = 'redis://localhost:6379/0'
