"""Shared Redis client."""

import redis

from src.core.config import settings

redis_client: redis.Redis = redis.from_url(
    settings.redis_url,
    decode_responses=True,
)