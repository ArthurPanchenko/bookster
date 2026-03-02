import redis.asyncio as redis


redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None: 
        redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0
        )

    return redis_client