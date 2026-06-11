from functools import lru_cache
from compliance_sdk.kafka import KafkaClient
from .config import settings

import redis.asyncio as redis
from .config import settings

redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def rate_limit(client_ip: str) -> bool:
    """Return True if under limit, False if exceeded."""
    key = f"rate:{client_ip}"
    count = await redis_client.get(key)
    if count is None:
        await redis_client.setex(key, 60, 1)
        return True
    count = int(count)
    if count > 100:
        return False
    await redis_client.incr(key)
    return True
from .service import IntakeService
from .repository import DocumentRepository
from .storage import MinioObjectStore

@lru_cache()
def get_kafka_client() -> KafkaClient:
    client = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "intake-gateway")
    return client

def get_intake_service() -> IntakeService:
    repo = DocumentRepository(str(settings.DATABASE_URL))
    store = MinioObjectStore(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        bucket=settings.RAW_BUCKET,
    )
    kafka = get_kafka_client()
    return IntakeService(repo, store, kafka)

