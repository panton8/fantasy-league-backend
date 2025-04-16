import environ

from redis import (
    ConnectionPool,
    Redis,
)

__all__ = (
    'HUEY',
)

env = environ.Env()

redis_host = env.str('REDIS_HOST', 'redis')
redis_port = env.str('REDIS_PORT', 6379)
redis_db = env.str('REDIS_DB', 0)
redis_pool_max_connections = env.int('REDIS_POOL_MAX_CONNECTIONS', 10)

redis_pool = ConnectionPool(
    host=redis_host,
    port=redis_port,
    db=redis_db,
    max_connections=redis_pool_max_connections
)

redis_client = Redis(connection_pool=redis_pool)


HUEY = {
    'name': 'fantasy_league',
    'immediate': env.bool('HUEY_IMMEDIATE', False),
    'immediate_use_memory': env.bool('HUEY_IMMEDIATE_USE_MEMORY', False),
    'connection': {
        'connection_pool': redis_pool,
    },
    'consumer': {
        'workers': 2,
    },
}