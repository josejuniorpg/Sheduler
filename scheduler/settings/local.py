# Django imports
import os

# Packages imports
import environ

# Local imports
from .base import *

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LINK_BASE_URL = 'http://127.0.0.1:8000/'

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
# EMAIL_USE_TLS = True
EMAIL_HOST = env.str('EMAIL_SENDER_HOST')
EMAIL_HOST_USER = env.str('EMAIL_USER_SENDER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_SENDER_PASSWORD') # Mail's password.
EMAIL_PORT = env.str('EMAIL_SENDER_PORT')