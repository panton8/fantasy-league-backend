import os

__all__ = (
    'DATABASES',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'fantasy_league'),
        'USER': os.environ.get('POSTGRES_USER', 'fantasy_league'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'fantasy_league'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'TEST': {
            'NAME': 'test_fantasy_league_default',
        },
    }
}
