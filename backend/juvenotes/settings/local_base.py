from .base import *


DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "secret"  # noqa: S105

STATICFILES_DIRS = (base_dir_join("../frontend"),)

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"

DATABASES = {
        "default": config("DATABASE_URL", cast=db_url),
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AUTH_PASSWORD_VALIDATORS = []  # allow easy passwords only on local

LOGIN_URL = 'https://localhost:8000/api-auth/login'

# Celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="")
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email settings for mailhog
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailhog"
EMAIL_PORT = 1025

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
    "formatters": {
        "standard": {
            "format": "%(levelname)-8s [%(asctime)s] [%(correlation_id)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": ["correlation_id"],
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "celery": {"handlers": ["console"], "level": "INFO"},
        "django_guid": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

JS_REVERSE_JS_MINIFY = False

# Django-CSP
LOCAL_HOST_URL = "http://localhost:3000"
LOCAL_HOST_WS_URL = "ws://localhost:3000/ws"
CSP_SCRIPT_SRC += [LOCAL_HOST_URL, LOCAL_HOST_WS_URL]
CSP_CONNECT_SRC += [LOCAL_HOST_URL, LOCAL_HOST_WS_URL]
CSP_FONT_SRC += [LOCAL_HOST_URL]
CSP_IMG_SRC += [LOCAL_HOST_URL]

# Django-defender
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_COOLOFF_TIME = 300  # 5 minutes
DEFENDER_LOCKOUT_TEMPLATE = "defender/lockout.html"
DEFENDER_REDIS_URL = config("REDIS_URL") 