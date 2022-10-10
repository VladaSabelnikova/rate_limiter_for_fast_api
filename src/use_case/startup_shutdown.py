from src.db.async_db_session import redis_client


async def startup():
    await redis_client.rate_limiter_client.start()


async def shutdown():
    await redis_client.rate_limiter_client.stop()

