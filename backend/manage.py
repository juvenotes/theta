#!/usr/bin/env python

import os
import sys

from decouple import config
from dotenv import load_dotenv


# if __name__ == "__main__":
#     settings_module = 'juvenotes.settings.production' if 'WEBSITE_HOSTNAME' in os.environ else config("DJANGO_SETTINGS_MODULE", default=None)
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

#     if sys.argv[1] == "test":
#         if settings_module:
#             print(
#                 "Ignoring config('DJANGO_SETTINGS_MODULE') because it's test. "
#                 "Using 'juvenotes.settings.test'"
#             )
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juvenotes.settings.test")
#     else:
#         if settings_module is None:
#             print(
#                 "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
#                 "Remember to create .env file at project root. "
#                 "Check README for more info."
#             )
#             sys.exit(1)
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

#     from django.core.management import execute_from_command_line

#     execute_from_command_line(sys.argv)

def main():
    """Run administrative tasks."""
    # If WEBSITE_HOSTNAME is defined as an environment variable, then we're running on Azure App Service

    # Only for Local Development - Load environment variables from the .env file
    if 'WEBSITE_HOSTNAME' not in os.environ:
        print("Loading environment variables for .env file")
        load_dotenv('.env')

    # When running on Azure App Service you should use the production settings.
    settings_module = "juvenotes.settings.production" if 'WEBSITE_HOSTNAME' in os.environ else 'azureproject.settings.base'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

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