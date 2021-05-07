"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import ugettext_lazy as _

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
env = os.getenv('ENV')
filename = '.env'
if env:
    filename = '{filename}.{env}'.format(filename=filename, env=env)

ENV_FILE = os.path.join(CURRENT_PATH, filename)
load_dotenv(ENV_FILE)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
ENV = os.getenv("ENV")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if ENV == 'production' else True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'model_utils',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_extensions',
    'django_injector',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_injector.inject_request_middleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
APPEND_SLASH = False
# file upload
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv("REDIS_PASSWORD")
        },
        "KEY_PREFIX": "marketing_api"
    }
}

# https://docs.djangoproject.com/en/3.0/topics/logging/
# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'file': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'filters': ['require_debug_true'],
        },
        'file': {
            'formatter': 'file',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs/api.log"),
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'email_backend': 'sendgrid_backend.SendgridBackend',
            'filters': ['require_debug_false'],
            'level': 'ERROR',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
        'api': {
            'handlers': ['file'],
            'level': os.getenv('API_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'serializers': {
            'handlers': ['file'],
            'level': os.getenv('API_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
        'oauth2': {
            'handlers': ['file', 'console'],
            'level': os.getenv('OAUTH2_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
        'jobs': {
            'handlers': ['file', 'console'],
            'level': os.getenv('CRON_JOBS_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
        'test': {
            'handlers': ['console'],
            'level': os.getenv('TEST_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
    },
}

DEFAULT_RENDERER_CLASSES = ['rest_framework.renderers.JSONRenderer']

if DEBUG:
    DEFAULT_RENDERER_CLASSES = [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        # default one
        'rest_framework.permissions.AllowAny',
    ],
    'SEARCH_PARAM': 'filter',
    'ORDERING_PARAM': 'order',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_PAGINATION_CLASS': 'api.utils.pagination.LargeResultsSetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/min',
        'user': '10000/min'
    }
}

# https://docs.djangoproject.com/en/3.0/ref/settings/
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "api/locale")
]

OAUTH2 = {
    'IDP': {
        'BASE_URL': os.getenv('OAUTH2_IDP_BASE_URL'),
        'INTROSPECTION_ENDPOINT': os.getenv('OAUTH2_IDP_INTROSPECTION_ENDPOINT')
    },
    'CLIENT': {
        'ID': os.getenv('OAUTH2_CLIENT_ID'),
        'SECRET': os.getenv('OAUTH2_CLIENT_SECRET'),
        'ENDPOINTS': {
            # user-roles
            '/api/v1/user-roles': {
                'delete': {
                    'name': _('DeleteUserRole'),
                    'desc': _('Delete User Role'),
                    'scopes': os.getenv('OAUTH2_SCOPE_REMOVE_USER_ROLE')
                },
                'post': {
                    'name': _('AddUser ole'),
                    'desc': _('Register User Role'),
                    'scopes': os.getenv('OAUTH2_SCOPE_ADD_USER_ROLE'),
                }
            },
        }
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "backend/media"),
]

SUPPORTED_LOCALES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
}

INJECTOR_MODULES = ['api.ioc.ApiAppModule']

DEV_EMAIL = os.getenv('DEV_EMAIL')

SUPABASE = {
    'URL': os.getenv('SUPABASE_URL'),
    'KEY': os.getenv('SUPABASE_KEY')
};