from functools import lru_cache
from compliance_sdk.kafka import KafkaClient
from .config import settings

from slowapi import Limiter
from slowapi.util import get_remote_address
import redis.asyncio as redis
from .config import settings

# Rate limiting: 100 запросов в минуту на IP
redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL)
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

