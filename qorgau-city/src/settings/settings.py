import os
from datetime import timedelta
from pathlib import Path

# from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = os.getenv('SECRET_KEY')
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(' ')
# ALLOWED_HOSTS.append('192.168.1.4')  # Add this line
# ALLOWED_HOSTS = ['192.168.1.4', 'localhost', '127.0.0.1']

ALLOWED_HOSTS = ["*"]
# load_dotenv()

CORS_ALLOWED_ORIGINS = [
    'http://165.22.63.97:5173',
    'http://192.168.1.4:3000',
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:87',
    'https://www.qorgau-city.kz',
    'http://www.qorgau-city.kz',
    'https://qorgau-city.kz',
    'http://qorgau-city.kz',
    'https://91.216.178.150',
    'http://91.216.178.150',
    'https://api.qorgau-city.kz',
    'http://api.qorgau-city.kz',
    'https://www.api.qorgau-city.kz',
    'http://www.api.qorgau-city.kz',
    'https://minio.qorgau-city.kz',
    'https://www.minio.qorgau-city.kz'
]

DJANGO_AND_THIRD_PARTY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "corsheaders",
    "channels",

    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework_swagger',

    'drf_yasg',
    'drf_spectacular',
    'django_db_logger',
    'storages',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'My project description',
    'VERSION': '1.0.0',
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'list',
        'defaultModelsExpandDepth': 2,
        'supportedSubmitMethods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'],
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVERS': [
        {'url': '/api/v1', 'description': 'Current API'}
    ],
}

PROJECT_APPS = [
    'auths.apps.AuthsConfig',
    'objects.apps.ObjectsConfig',
    'generators.apps.GeneratorsConfig',
    'statements.apps.StatementsConfig',
    'specifications.apps.SpecificationsConfig',
    'chats.apps.ChatsConfig',
]

INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

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

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LEFT': timedelta(days=7),
    'SLIDING_TOKEN_REFRESH_LEFT_AT': timedelta(days=1),
}

AUTH_USER_MODEL = 'auths.CustomUser'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'  # Временно отключено
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")

AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False    # True
AWS_S3_FILE_OVERWRITE = False   # True

# Static files settings - временно используем локальное хранение
# AWS_STATIC_LOCATION = 'static'
# AWS_STATIC_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT")
# Используем публичный endpoint для MEDIA_URL, если он задан, иначе внутренний
MEDIA_URL = f'{MINIO_PUBLIC_ENDPOINT or MINIO_ENDPOINT}/isec/' if MINIO_PUBLIC_ENDPOINT or MINIO_ENDPOINT else '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SMS_API_SERVER = os.getenv('SMS_API_SERVER', None)
SMS_API_KEY = os.getenv('SMS_API_KEY', None)
SMS_API_VERSION = os.getenv('SMS_API_VERSION', 1)
SMS_OUTPUT_FORMAT = os.getenv('SMS_OUTPUT_FORMAT', 'json')
SMS_FORCE_HTTP = os.getenv('SMS_FORCE_HTTP', False)
SMS_SENDER = os.getenv('SMS_SENDER', 'isec')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = True
QR_GENERATOR_LINK = "https://api.qrserver.com/v1/create-qr-code/?size=320x320"

# SSL настройки только для продакшн
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SSL_CERTIFICATE_PATH = "/etc/letsencrypt/live/api.qorgau-city.kz/fullchain.pem"
    SSL_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/api.qorgau-city.kz/privkey.pem"

SMSC_OTP_HOST = os.getenv('SMSC_OTP_HOST')
SMSC_OTP_LOGIN = os.getenv('SMSC_OTP_LOGIN')
SMSC_OTP_PASSWORD = os.getenv('SMSC_OTP_PASSWORD')
SMSC_OTP_SENDER_ID = os.getenv('SMSC_OTP_SENDER_ID')

INSTALLED_APPS += ['django_celery_beat']

CELERY_BROKER_URL = 'redis://redis_backend:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis_backend:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Almaty'

# This line ensures Celery can find tasks
CELERY_IMPORTS = ('objects.tasks',)

# Microservices authentication
MICROSERVICE_ALLOWED_SERVICES = ['main_server', 'chat_server', ]
THIS_SERVICE_NAME = 'main_server'
MICROSERVICE_JWT_SECRET_KEY = '123'

# Channels configuration
ASGI_APPLICATION = 'settings.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}