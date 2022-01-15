from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'insecure--wm-am!aar8!c@!zgppa*j^&ay63wbn=+s(ld!alq4z6mo!i)dvk3%-engine'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For Django Debug Toolbar
if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']
MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
def show_toolbar(request):
        return True
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

INSTALLED_APPS = INSTALLED_APPS + [
    'wagtail.contrib.styleguide',
    'debug_toolbar',
]

INTERNAL_IPS = ('127.0.0.1')

SENTRY_RELEASE = "development"
SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_DEV_TRACE_SAMPLE_RATE = os.environ.get('SENTRY_DEV_TRACE_SAMPLE_RATE')

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), ModulesIntegration()],
    release=VERSION,
    environment=SENTRY_RELEASE,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=SENTRY_DEV_TRACE_SAMPLE_RATE,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


try:
    from .local import *
except ImportError:
    pass
