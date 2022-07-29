from .base import *
import environ

env = environ.Env()
environ.Env.read_env()

ALLOWED_HOSTS = [
    '127.0.0.1',
    env('LOCAL_HOST_URL', default=None),
    env('PUBLIC_HOST_URL', default=None),
    ]

DEBUG = env('DEBUG', default=True)

if not DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

INSTALLED_APPS += (
    'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME', default=''),
        'USER': env('DATABASE_USER', default=''),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default=''),
        # 'PORT': '',
    }
}

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TIME_ZONE = 'America/Mexico_City'