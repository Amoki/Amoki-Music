# -*- coding: utf-8 -*-

from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

SITE_URL = 'localhost:8000'

WSGI_APPLICATION = 'ws4redis.django_runserver.application'

PYTHON_ENV = "development"
