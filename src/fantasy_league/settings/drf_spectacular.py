import environ


__all__ = (
    'SPECTACULAR_SETTINGS',
    'IS_SWAGGER_ENABLED',
)

env = environ.Env()


IS_SWAGGER_ENABLED = env.bool('IS_SWAGGER_ENABLED', default=True)

SPECTACULAR_SETTINGS = {
    'TITLE': 'Fantasy League API',
    'DESCRIPTION': 'Fantasy League API documentation',
    'VERSION': '0.0.1',
    'SCHEMA_PATH_PREFIX': r'/v[0-9]',
    'COMPONENT_SPLIT_REQUEST': True

}