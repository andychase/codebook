from .settings import *

DEBUG = False

import dj_database_url

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'static'

static_path = os.path.join(BASE_DIR, 'static')

if not os.path.isdir(static_path):
    os.mkdir(static_path)

STATICFILES_DIRS = (
    static_path,
)

PIPELINE_COFFEE_SCRIPT_BINARY = "/app/.heroku/node/bin/node ./node_modules/coffee-script/bin/coffee"
