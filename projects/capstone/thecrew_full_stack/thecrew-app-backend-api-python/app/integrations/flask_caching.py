"""Utility methods to check Redis server.

    redis_is_available(): Verify if the Redis server is available.
"""

from flask import current_app
from redis import Redis, exceptions


def redis_is_available():
    """Check if there's a Redis server configured with the application and 
    available.
    
    :return: True if it's available, False otherwise.
    """
    return redis_is_not_available() == False


def redis_is_not_available():
    """Try to reach the Redis server configured with the application.
    
    :return: True if it's not configured or not reachable, False otherwise.
    """
    if not current_app.config['CACHE_REDIS_URL']:
        return True
    pong = None
    try:
        redis_client = Redis.from_url(current_app.config['CACHE_REDIS_URL'])
        pong = redis_client.ping()
    except exceptions.ConnectionError:
        return True
    return not pong
