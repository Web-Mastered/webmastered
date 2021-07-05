from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'insecure--wm-am!aar8!c@!zgppa*j^&ay63wbn=+s(ld!alq4z6mo!i)dvk3%-engine'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'wagtail.contrib.styleguide',
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1')

SENTRY_RELEASE = "development"
SENTRY_DSN = env('SENTRY_DSN')

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


try:
    from .local import *
except ImportError:
    pass
