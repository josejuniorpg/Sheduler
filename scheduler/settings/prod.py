import os
from .base import *
import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = False
ALLOWED_HOSTS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}