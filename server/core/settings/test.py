from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, f"{os.environ.get('POSTGRES_DB', 'postgres')}_test.sqlite3"),
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

CELERY_TASK_ALWAYS_EAGER = True