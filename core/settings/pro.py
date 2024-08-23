from .base import *

DEBUG = False

ALLOWED_HOSTS = ['inex-design.com']


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASS,
        'HOST': 'localhost',
        'PORT': DB_PORT,
    }
}