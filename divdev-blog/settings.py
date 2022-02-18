import dj_database_url
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'staticfiles', 'sw.js')

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = "j%vr*5iu43ks_w6j4#op223o96$p=#r7)jdevdiv%vr*5iudivineik43ks_w6j4#op223o96$p=#r7)"

DEBUG = False
ALLOWED_HOSTS = ['devdiv.herokuapp.com', 'localhost']
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/login/"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'posts',
    'core.api',
    'history',

    # # Third Party
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
]

CKEDITOR_CONFIGS = {
  'default': {
    'removePlugins': 'stylesheetparser',
    'allowedContent': True,
  },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'divdev-blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'divdev-blog.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'divdev.sqlite3'),
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static-root")
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply.devdiv@gmail.com'
EMAIL_HOST_PASSWORD = 'ddiivviinneeq1'
EMAIL_PORT = 587

DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]

DEFAULT_PERMISSION_CLASSES = [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
]

DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

if DEBUG:
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': DEFAULT_PERMISSION_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}
