import os
import redis.asyncio as redis_async
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis_async.from_url(
    REDIS_URL,
    decode_responses=True,
)

async def get_redis():
    return redis_client

