"""
Django settings for AdminSumarte project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u=#&!09t51u#*mz%-o2gi&b_mt%$o5q5m0$er%hu64n6zh$rku'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    'localhost',  # Permitir localhost
    '127.0.0.1',  # Permitir localhost
    '0.0.0.0',
    '8000-idx-adminsumarte-1728973718758.cluster-23wp6v3w4jhzmwncf7crloq3kw.cloudworkstations.dev',
    # Agrega cualquier otro dominio que necesites permitir
]

CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0:8000/',
    'https://8000-idx-adminsumarte-1728973718758.cluster-23wp6v3w4jhzmwncf7crloq3kw.cloudworkstations.dev/',
    'https://8000-idx-adminsumarte-1728973718758.cluster-23wp6v3w4jhzmwncf7crloq3kw.cloudworkstations.dev',
    'https://8000-idx-adminsumarte-1728973718758.cluster-23wp6v3w4jhzmwncf7crloq3kw.cloudworkstations.dev/accounts/login/login',
] 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AdminSumarteApp',
    'Autenticacion',
    'Avisos',
    'Contadores',
    'Personal_Red',
    'Instalaciones',
    'Printer',
    'crispy_forms',
    'crispy_bootstrap5',
    
]
# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# telegram-token
TELEGRAM_BOT_TOKEN = '8004995881:AAHVc78jSzLUggQuNZK4sArgSf6MJtW-9z8'

# twilio-configs
TWILIO_ACCOUNT_SID = 'AC881cb26d92f6ccafedae21c4d258d61a'
TWILIO_AUTH_TOKEN = '6928a475e878438e0c21f0b044d146fc'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # El número de WhatsApp de Twilio


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AdminSumarte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./AdminSumarte/AdminSumarteApp/templates/'],
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

WSGI_APPLICATION = 'AdminSumarte.wsgi.application'

#para la aplicacion channels
ASGI_APPLICATION = 'AdminSumarte.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
   
   # CONFIGURACION CON LA MARIA_DB bd_sumarte_admin
#    'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bd_sumarte_admin',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-es'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Madrid'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
