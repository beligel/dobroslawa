"""
Django settings for dobroslawa — БЕЗОПАСНАЯ ВЕРСИЯ
Для продакшена измените следующее:
1. Создайте .env файл с SECRET_KEY
2. Установите DEBUG=False
3. Укажите корректные ALLOWED_HOSTS
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# === БЕЗОПАСНОСТЬ: SECRET_KEY должен быть в переменной окружения ===
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-change-this-in-production'
)

# === БЕЗОПАСНОСТЬ: Отключить в продакшене ===
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# === БЕЗОПАСНОСТЬ: Укажите ваш домен ===
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'modeltranslation',
    'pages',
    'rooms',
    'bookings',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dobroslawa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'dobroslawa.wsgi.application'

# === БЕЗОПАСНОСТЬ: PostgreSQL для продакшена ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # Для PostgreSQL:
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.environ.get('DB_NAME', 'dobroslawa'),
        # 'USER': os.environ.get('DB_USER', 'postgres'),
        # 'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        # 'HOST': os.environ.get('DB_HOST', 'localhost'),
        # 'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('zh-hans', '简体中文'),
]

LOCALE_PATHS = [BASE_DIR / 'locale',]

HOTEL_NAME = 'Доброславия / Dobroslawa'
HOTEL_ADDRESS = 'ул. Пушкина, 10, Ростов-на-Дону'
HOTEL_PHONE = '+7 (999) 000-00-00'
HOTEL_EMAIL = 'info@dobroslawa.ru'

BOOKING_HOURS_ADVANCE = 3

# === БЕЗОПАСНОСТЬ: Настройки для продакшена ===
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Заголовки безопасности
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # CSRF
    CSRF_TRUSTED_ORIGINS = [
        'https://yourdomain.com',
        'https://www.yourdomain.com',
    ]