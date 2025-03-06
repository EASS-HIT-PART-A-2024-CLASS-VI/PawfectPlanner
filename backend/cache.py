# File: backend/cache.py
import redis
import json

# Hardcode "redis" as the service name, 6379 as the port
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

def get_json(key: str):
    """
    Return JSON data from Redis for the given key, or None if not found.
    """
    val = r.get(key)
    if val is None:
        return None
    return json.loads(val)

def set_json(key: str, data: dict, expire_seconds: int = 86400):
    """
    Store a dict in Redis as JSON, with an optional expiry (default 24h).
    """
    r.setex(key, expire_seconds, json.dumps(data))
