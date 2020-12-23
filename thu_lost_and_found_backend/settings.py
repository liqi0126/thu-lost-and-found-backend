import os
from datetime import timedelta
from pathlib import Path

import pymysql
from environs import Env

pymysql.version_info = (1, 4, 0, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# local for dev, prod for production
APP_ENV = env('APP_ENV')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('APP_DEBUG', False)

APP_URL = env('APP_URL')

ALLOWED_HOSTS = ['*']

<<<<<<< HEAD
CORS_ORIGIN_ALLOW_ALL = DEBUG
=======
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1"
]
>>>>>>> add-tests

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',

    'corsheaders',
    'channels',
    'rest_framework',

    # thu-lost-and-found
    'thu_lost_and_found_backend',
    'thu_lost_and_found_backend.authentication_service.apps.AuthenticationServiceConfig',
    'thu_lost_and_found_backend.contact_service.apps.ContactServiceConfig',
    'thu_lost_and_found_backend.found_notice_service.apps.FoundNoticeServiceConfig',
    'thu_lost_and_found_backend.lost_notice_service.apps.LostNoticeServiceConfig',
    'thu_lost_and_found_backend.property_service.apps.PropertyServiceConfig',
    'thu_lost_and_found_backend.user_service.apps.UserServiceConfig',
    'thu_lost_and_found_backend.tag_service.apps.TagServiceConfig',
    'thu_lost_and_found_backend.matching_service.apps.MatchingServiceConfig',
    'thu_lost_and_found_backend.report_service.apps.ReportServiceConfig',
    'thu_lost_and_found_backend.chat_service.apps.ChatServiceConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'thu_lost_and_found_backend.authentication_service.middleware.JWTAuthenticationMiddleware',
    'thu_lost_and_found_backend.authentication_service.middleware.UserStatusValidationMiddleware',
]

ROOT_URLCONF = 'thu_lost_and_found_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thu_lost_and_found_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DB_CONNECTION'),
        'NAME': env('DB_DATABASE'),
        'USER': env('DB_USERNAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

AUTH_USER_MODEL = "user_service.User"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = env.bool('USE_TZ', False)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25

EMAIL_HOST_USER = 'thu_lost_and_found@163.com'
EMAIL_HOST_PASSWORD = 'TMGHFYDVFSTRTIYU'

EMAIL_FROM = 'noreply@thu-lost-and-found.com'
DEFAULT_FROM_EMAIL = 'thu_lost_and_found@163.com'

DEFAULT_RENDERER_CLASSES = ['rest_framework.renderers.JSONRenderer']
if DEBUG:
    DEFAULT_RENDERER_CLASSES.append('rest_framework.renderers.BrowsableAPIRenderer')

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
        # 'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', False)

EMAIL_DISPLAY_NAME = env('EMAIL_DISPLAY_NAME')

WECHAT_APP_ID = env('WECHAT_APP_ID')
WECHAT_APP_SECRET = env('WECHAT_APP_SECRET')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6)
}

# Channels
ASGI_APPLICATION = "thu_lost_and_found_backend.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(env('REDIS_HOST'), 6379)],
        },
    },
}

# CELERY STUFF
CELERY_BROKER_URL = "redis://" + env('REDIS_HOST') + ":6379/0"
CELERY_RESULT_BACKEND = "redis://" + env('REDIS_HOST') + ":6379/0"
