#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Django imports
import os
import sys

# Packages imports
import environ

# Initialize the environment variables
env = environ.Env()
environ.Env.read_env()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str('DJANGO_ENVIRONMENT_FILE', default='blog.settings.prod'))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
