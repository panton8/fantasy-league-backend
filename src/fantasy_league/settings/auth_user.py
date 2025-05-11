import environ

env = environ.Env()


__all__ = (
    'AUTH_PASSWORD_VALIDATORS',
    'AUTH_USER_MODEL',
    'AUTHENTICATION_BACKENDS',
)

AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = [
    'user.auth.backends.ModelBackend',
]

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
