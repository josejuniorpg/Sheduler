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


# EMAIL SETTINGS
# EMAIL_USE_TLS = True   #Activate the emails sender.
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = get_secret('EMAIL') #Mail Sender
# EMAIL_HOST_PASSWORD = get_secret('PASS_EMAIL') #Mail's password.
# EMAIL_PORT = 587
