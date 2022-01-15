from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

SENTRY_RELEASE = "production"
SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_PROD_TRACE_SAMPLE_RATE = os.environ.get('SENTRY_PROD_TRACE_SAMPLE_RATE')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), ModulesIntegration()],
    release=VERSION,
    environment=SENTRY_RELEASE,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=SENTRY_PROD_TRACE_SAMPLE_RATE,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

try:
    from .local import *
except ImportError:
    pass




from .base import *

DEBUG = False

SECRET_KEY = 'django-insecure-^*(40d8bgsnl7s$(*_(j8!3%=x7wd)a=i%s3&goin&5c=bbr%0'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
