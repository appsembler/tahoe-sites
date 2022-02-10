import os

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = 'insecure-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'organizations',
    'tahoe_sites',
    'django_nose',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'organizations.urls'

# DRF Settings
REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ'
}

# Django requires this for admin usage.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": {
                "django.contrib.auth.context_processors.auth",  # this is required for admin
                "django.contrib.messages.context_processors.messages",
            }
        }
    },
]

SITE_ID = 1

# We can only run tests with a known flag value
TAHOE_SITES_USE_ORGS_MODELS = os.environ.get('TAHOE_SITES_USE_ORGS_MODELS')
if TAHOE_SITES_USE_ORGS_MODELS is None:
    raise ValueError('Please set TAHOE_SITES_USE_ORGS_MODELS value in your test environment')
if isinstance(TAHOE_SITES_USE_ORGS_MODELS, str):
    TAHOE_SITES_USE_ORGS_MODELS = (TAHOE_SITES_USE_ORGS_MODELS.lower() == 'true')
if not isinstance(TAHOE_SITES_USE_ORGS_MODELS, bool):
    raise TypeError('Bad datatype for TAHOE_SITES_USE_ORGS_MODELS')
FEATURES = {
    'TAHOE_SITES_USE_ORGS_MODELS': TAHOE_SITES_USE_ORGS_MODELS
}
