import os

from django.core.wsgi import get_wsgi_application


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juvenotes.settings.production")

settings_module = 'juvenotes.settings.production' if 'HOSTNAME' in os.environ else config("DJANGO_SETTINGS_MODULE", default=None)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()