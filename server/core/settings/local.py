from .base import *

INTERNAL_IPS = os.environ.get("INTERNAL_IPS", "*").split(",")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

import sys

TESTING = "test" in sys.argv or "PYTEST_VERSION" in os.environ

if not TESTING:
    INSTALLED_APPS += [    
        'silk',
        "debug_toolbar",
    ]

    MIDDLEWARE += [
        'silk.middleware.SilkyMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    ]


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'IS_RUNNING_TESTS': False,
}