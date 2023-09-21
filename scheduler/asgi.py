"""
ASGI config for scheduler project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# Django imports
import os
from django.core.asgi import get_asgi_application

# Packages imports
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str('DJANGO_ENVIRONMENT_FILE', default='blog.settings.prod'))

application = get_asgi_application()
