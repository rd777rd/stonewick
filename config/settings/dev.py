from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Console email backend for local dev so order confirmations print to terminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INTERNAL_IPS = ["127.0.0.1"]
