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

# Use cached templates
if not DEBUG:
    del TEMPLATES[0]['OPTIONS']['APP_DIRS']
    TEMPLATES[0]['OPTIONS']['DIRS'] = []
    TEMPLATES[0]['OPTIONS']['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ])
    ]


EMAIL_BACKEND = 'django.core.mail.backends.smtp'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
