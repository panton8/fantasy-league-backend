__all__ = (
    'INSTALLED_APPS',
)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_spectacular',
    'corsheaders',
    'storages',
    'huey.contrib.djhuey',

    'base',
    'user',
    'team',
    'match',
    'statistics'
]
