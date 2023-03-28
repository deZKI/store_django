import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env.dev')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv(os.path.join(BASE_DIR, '.env.prod'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG_VALUE') == 'TRUE'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    'rest_framework',
    'rest_framework.authtoken',

    "phonenumber_field",
    'debug_toolbar',
    'image_uploader_widget',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',

    'api',
    'users',
    'games',
    'orders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'store_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',

                'games.context_processor.baskets',
            ],
        },
    },
]

WSGI_APPLICATION = 'store_django.wsgi.application'

# postgres
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

if DEBUG: AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    ]

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# users
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/users/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# django-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# rest_api
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
PAGE_SIZE = 10

# django-redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:{}/1'.format(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT')),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
# CACHE_MIDDLEWARE_SECONDS = 60
# CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # по умолчанию стоит такой, добавил по приколу

HOST_URL = os.getenv('HOST_URL')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

# https://git.yoomoney.ru/projects/SDK/repos/yookassa-sdk-python/browse/docs/examples/01-configuration.md#%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F
CSRF_TRUSTED_ORIGINS = ['https://e621-185-48-112-241.jp.ngrok.io', ]
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY')
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID')

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

# Celery
CELERY_BROKER_URL = 'redis://{}:{}'.format(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))
CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))
