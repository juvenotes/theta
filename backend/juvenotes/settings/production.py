import os

import sentry_sdk
from decouple import Csv, config
from django_guid.integrations import SentryIntegration as DjangoGUIDSentryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *


ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS += ['.juvenotes.com']
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

CONNECTION = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
CONNECTION_STR = {pair.split('=')[0]:pair.split('=')[1] for pair in CONNECTION.split(' ')}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": CONNECTION_STR['dbname'],
        "HOST": CONNECTION_STR['host'],
        "USER": CONNECTION_STR['user'],
        "PASSWORD": CONNECTION_STR['password'],
        "ATOMIC_REQUESTS": True,
        "OPTIONS": {'sslmode': 'require'},
    }
}

CACHES = {
        "default": {  
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get('AZURE_REDIS_CONNECTIONSTRING'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}

# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"

SERVER_EMAIL = "noreply@juvenotes.com"
DEFAULT_FROM_EMAIL = "noreply@juvenotes.com" 

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN"),  
}

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend" # or sendgrid.EmailBackend

EMAIL_HOST = "smtp.mailgun.org"
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Security
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = os.environ("SECURE_HSTS_SECONDS", default=3600, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# Webpack
WEBPACK_LOADER["DEFAULT"]["CACHE"] = True

# Celery
# Recommended settings for reliability: https://gist.github.com/fjsj/da41321ac96cf28a96235cb20e7236f6
CELERY_BROKER_URL = os.environ.get("RABBITMQ_URL", default="") or os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")
CELERY_SEND_TASK_ERROR_EMAILS = True

# Redbeat https://redbeat.readthedocs.io/en/latest/config.html#redbeat-redis-url
redbeat_redis_url = os.environ.get("REDBEAT_REDIS_URL", default="")

# Whitenoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Django GUID
DJANGO_GUID = {
    "INTEGRATIONS": [
        DjangoGUIDSentryIntegration(),
    ],
}


# django-log-request-id
MIDDLEWARE.insert(  # insert RequestIDMiddleware on the top
    0, "log_request_id.middleware.RequestIDMiddleware"
)

LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
LOG_REQUESTS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
    "formatters": {
        "standard": {
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] [%(correlation_id)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["request_id", "correlation_id"],
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "django_guid": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "log_request_id.middleware": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

JS_REVERSE_EXCLUDE_NAMESPACES = ["admin"]

# Sentry
sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()], release=COMMIT_SHA)
