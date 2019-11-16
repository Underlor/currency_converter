import os

REQUIRED = os.environ.__getitem__
OPTIONAL = os.environ.get

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = OPTIONAL('SECRET_KEY', '13m6!z%-bori!6ubx=#2!4do#mm@2v(vyof3)7@ae0kd09t8_b')

DEBUG: bool = OPTIONAL('DEBUG', False)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'converter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'currency_converter.urls'

WSGI_APPLICATION = 'currency_converter.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': OPTIONAL('DB_NAME', 'currency_converter'),
        'USER': OPTIONAL('DB_USER', 'currency_converter'),
        'PASSWORD': OPTIONAL('DB_PASSWORD', 'currency_converter'),
        'HOST': OPTIONAL('DB_HOST', 'localhost'),
        'PORT': OPTIONAL('DB_PORT', ''),
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Celery configuration
BROKER_HOST = OPTIONAL('BROKER_HOST', '127.0.0.1')
BROKER_PORT = OPTIONAL('BROKER_PORT', 5672)
BROKER_USER = OPTIONAL('BROKER_USER', "guest")
BROKER_PASSWORD = OPTIONAL('BROKER_PASSWORD', "guest")

CELERY_BROKER_URL = f'amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}'

CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 86400
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_DEFAULT_QUEUE = 'currency_converter'
CELERY_TASK_DEFAULT_EXCHANGE = 'currency_converter'
CELERY_RESULT_BACKEND = 'django-db'

# Parser configuration
EXCHANGE_RATE_URL = OPTIONAL('NEWS_URL', 'https://openexchangerates.org/api/latest.json')
APP_ID = OPTIONAL('APP_ID', 'c16523fcb098490fa868fd73b0c90cb5')