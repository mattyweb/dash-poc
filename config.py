from os import environ
from distutils import util

API_HOST = environ.get('API_HOST') or 'https://dev-api.311-data.org'
# PRELOAD = bool(util.strtobool(environ.get('PRELOAD'))) or True
PRELOAD = bool(environ.get('PRELOAD'))
DASH_FILES = environ.get('DASH_FILES') or 'dashboards'
