from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'openanalyse.herokuapp.com']
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
CORS_ALLOWED_ORIGINS = [
    'https://openanalyse.netlify.app'
]
