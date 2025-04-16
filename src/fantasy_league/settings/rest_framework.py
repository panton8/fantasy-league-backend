__all__ = (
    'REST_FRAMEWORK',
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_api.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'EXCEPTION_HANDLER': 'rest_api.exception_handler.custom_exception_handler',

    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%f',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '6/minute'
    }
}
