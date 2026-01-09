import redis.asyncio as redis
import os

# Redis Configuration - allow override via env vars
REDIS_HOST = os.getenv("REDIS_HOST", "47.95.11.247")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "Asiainfo2@")
REDIS_DB = int(os.getenv("REDIS_DB", 0))

async def get_redis():
    """Dependency that provides a Redis client"""
    client = redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        password=REDIS_PASSWORD,
        db=REDIS_DB, 
        decode_responses=True,
        protocol=2
    )
    try:
        yield client
    finally:
        await client.close()
