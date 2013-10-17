# Load defaults in order to then add/override with dev-only settings
from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
# ... etc.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# pip install django-debug-toolbar
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += (
    'debug_toolbar',
)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
