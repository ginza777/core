"""
Development settings for Multi Parser Project
"""
from .base import *  # noqa

# Development-specific settings
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'sherzamon.jprq.site', '*.jprq.site']

# Database - Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache - Use local memory for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery - Use local Redis for development
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Email - Use console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar - Only in development
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Telegram Bot Configuration
BOT_TOKEN = "7015018136:AAG6-dBJZaeoOzZCKeOJUGKYC7PKfRwKRik"  # Replace with your actual bot token
WEBHOOK_URL = env.str("WEBHOOK_URL", default="http://localhost:8000")  # For development, use HTTP

# Logging - Only debug when DJANGO_DEBUG=1
if env.bool("DJANGO_DEBUG", default=False):
    LOGGING['loggers']['django']['level'] = 'DEBUG'
else:
    LOGGING['loggers']['django']['level'] = 'INFO'

# Static and media files for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Jazzmin settings for development
JAZZMIN_SETTINGS = {
    "site_title": "Multi Parser Admin",
    "site_header": "Multi Parser",
    "site_brand": "Multi Parser",
    "site_logo": None,
    "welcome_sign": "Welcome to Multi Parser",
    "copyright": "Multi Parser Ltd",
    "search_model": ["core.Product", "core.Document", "core.Seller"],
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Product": "fas fa-box",
        "core.Document": "fas fa-file",
        "core.Seller": "fas fa-store",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "collapsible",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
