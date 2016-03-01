"""
Django settings for amoki_music project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys


# Environment
PYTHON_ENV = os.environ.get('PYTHON_ENV', 'development')

if PYTHON_ENV == 'production':  # pragma: no cover
    DEBUG = False
    TEMPLATE_DEBUG = False
    WS4REDIS_DB = 1
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    WS4REDIS_DB = 0
    WSGI_APPLICATION = 'ws4redis.django_runserver.application'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Amoki', 'hugo.duroux@gmail.com'),
    ('Eirika', 'chanove.tristan@gmail.com'),
)

MANAGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5h9@)57rjgoe3m_sb12kcp-ku7w!#x86a_k5_59t#g=!e$nhha'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    # Pip lib
    'ws4redis',
    'rest_framework',
    'ordered_model',
    'rest_framework_swagger',
    'django_nose',

    # Our apps
    'player',
    'music',
    'endpoints',
    'sources',
    'website',
)

SOURCES = ["youtube", "soundcloud"]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'amoki_music.urls'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'collected-static/')

# URL prefix for static files.
# Example: "http://media.l
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'website/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)


# Websockets
WEBSOCKET_URL = '/ws/'

WS4REDIS_SUBSCRIBER = 'amoki_music.subscriber.RedisSubscriber'

WS4REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': WS4REDIS_DB,
    'password': None,
}

WS4REDIS_EXPIRE = 0

WS4REDIS_PREFIX = 'ws_' + PYTHON_ENV

WS4REDIS_HEARTBEAT = '--heartbeat--'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'ws4redis.context_processors.default',
)

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'

#
# Modules
#

# Youtube
YOUTUBE_KEY = os.environ.get('YOUTUBE_KEY', None)
YOUTUBE_LANGUAGE = os.environ.get('YOUTUBE_LANGUAGE', 'FR')

# Soundcloud
SOUNDCLOUD_KEY = os.environ.get('SOUNDCLOUD_KEY', None)


SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'patch',
        'delete'
    ],
    'info': {
        'contact': 'hugo.duroux@gmail.com',
        'title': 'Amoki Music',
    },
    'doc_expansion': 'none',
    'token_type': 'Bearer'
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Keep the original host behind a proxy for direct use of ws://
USE_X_FORWARDED_HOST = True


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

TESTING = False

if len(sys.argv) > 1 and 'test' in sys.argv:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',  # Replace hasher with a simpler and faster hash method
    )
    DEBUG = False
    TEMPLATE_DEBUG = False
    TESTING = True
    MIGRATION_MODULES = DisableMigrations()  # Disable migrations during tests
