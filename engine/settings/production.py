from .base import *

DEBUG = False
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')
SECRET_KEY = env('SECRET_KEY')

SENTRY_RELEASE = "production"
SENTRY_DSN = env('SENTRY_DSN')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), ModulesIntegration()],
    release=VERSION,
    environment=SENTRY_RELEASE,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

REDIS_DB_NAME = env('REDIS_DB_NAME')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/' + REDIS_DB_NAME,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

try:
    from .local import *
except ImportError:
    pass
