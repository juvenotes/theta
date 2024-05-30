import os

from django.core.wsgi import get_wsgi_application


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juvenotes.settings.production")
# Check for the WEBSITE_HOSTNAME environment variable to see if we are running in Azure Ap Service
# If so, then load the settings from production.py
settings_module = 'juvenotes.settings.production' if os.environ.get('DJANGO_SETTINGS_MODULE') == 'juvenotes.settings.production' else 'juvenotes.settings.base'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
