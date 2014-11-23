# -*- coding: utf-8 -*-

from .common import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/../..")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'gunicorn',
)
