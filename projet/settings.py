"""
Django settings for projet project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_42oe4&wkls(d-f^_x+u#27sob6b(@tdkj#p+-aofkf6!9nc89'

# SECURITY WARNING: don't run with debug turned on in production!
# Mettez False pour la production, True pour le développement local
DEBUG = False

# Ajoutez ici l'adresse de votre site PythonAnywhere
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DHT',            # Votre app
    'rest_framework', # Pour l'API
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

ROOT_URLCONF = 'projet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Dossier templates à la racine
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'projet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr' # Mis en français

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- CONFIGURATION DES FICHIERS STATIQUES ---
# C'est crucial pour que votre site soit joli en ligne

STATIC_URL = '/static/'

# Où Django cherche vos fichiers static pendant le développement (votre dossier local)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Où Django rassemble tous les fichiers pour la mise en ligne (PythonAnywhere)
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CONFIGURATION EMAIL ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "oussama.boutalount.23@ump.ac.ma"
EMAIL_HOST_PASSWORD = "hvzy rghr numf lpgg"  # Mot de passe d'application

# --- CONFIGURATION TELEGRAM ---
TELEGRAM_BOT_TOKEN = "8301834025:AAHnrqs-NSsw5rZVD9FZUvwqYFXFcinGAyo"
TELEGRAM_CHAT_ID = "1967212473"