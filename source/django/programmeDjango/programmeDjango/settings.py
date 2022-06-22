"""
Django settings for programmeDjango project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# we define the repertory where there is all temporary data
TEMPORARY_DATA = os.path.join(BASE_DIR,'docker_volume/data')
ARTICLE_DATA = os.path.join(BASE_DIR,'docker_volume/articles')
PLOT_DATA = os.path.join(BASE_DIR,'docker_volume/plot')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-96*q09uh20(^i4sdxqh3n_v#d-$o=**7zrri&k-j3@f10hm88)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UI_Front',
    'oauth2_provider',
    'DataBase',
    'BackEnd',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'programmeDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PLOT_DATA + "/"],
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

WSGI_APPLICATION = 'programmeDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_test',
        'USER': 'user_test',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL='UI_Front.CustomUser'

STATICFILES_DIRS = [
('css',os.path.join(BASE_DIR,'static/css')),
('script',os.path.join(BASE_DIR,'static/script'))]
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

NUMBER_THREADS_ALLOWED = 2
NUMBER_TRIALS = 300

NUMBER_ARTICLE_BY_PAGE = 30

#we define interval coordinate to display
# LITTLE if < 10 000 articles
X_INTERVAL_LITTLE = 490
Y_INTERVAL_LITTLE = 1000

# BIG if > 10 000 articles
X_INTERVAL_BIG = 2000
Y_INTERVAL_BIG = 4000

#we define in seconds the interval between update research
# we define 1 month
UPDATE_INTERVAL = 2700000

is_decentralized=False