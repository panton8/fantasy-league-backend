import environ

env = environ.Env()

__all__ = (
    'STORAGES',

    'MINIO_STORAGE_ENDPOINT',
    'MINIO_STORAGE_ACCESS_KEY',
    'MINIO_STORAGE_SECRET_KEY',
    'FILE_NAME_MAX_LENGTH',
)


STORAGES = {
    'default': {
        'BACKEND': env('DEFAULT_FILE_STORAGE', default='storages.backends.s3boto3.S3Boto3Storage'),
    }
}

MINIO_STORAGE_ENDPOINT = env('MINIO_STORAGE_ENDPOINT', default='localhost:9000')
MINIO_STORAGE_ACCESS_KEY = env('MINIO_ROOT_USER', default='minio_admin')
MINIO_STORAGE_SECRET_KEY = env('MINIO_ROOT_PASSWORD', default='minio_pass')


FILE_NAME_MAX_LENGTH = env('FILE_NAME_MAX_LENGTH', default=256)
