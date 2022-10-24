import environ

from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'pybo.kr', 'django.pybo.kr']
# ALLOWED_HOSTS = ['3.37.58.70', 'pybo.kr', 'django.pybo.kr']
# ALLOWED_HOSTS = ['192.168.219.101', 'pybo.kr', 'django.pybo.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}
