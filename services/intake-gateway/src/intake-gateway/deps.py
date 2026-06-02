"""Manual DI container with lifespan management."""
from functools import lru_cache
from contextlib import asynccontextmanager
from fastapi import FastAPI
from compliance_sdk.kafka import KafkaClient
from .config import settings
from .service import IntakeService
from .repository import DocumentRepository
from .storage import MinioObjectStore

_kafka_client = None

@lru_cache()
def get_kafka_client() -> KafkaClient:
    global _kafka_client
    if _kafka_client is None:
        _kafka_client = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "intake-gateway")
    return _kafka_client

def get_intake_service() -> IntakeService:
    repo = DocumentRepository(settings.DATABASE_URL)
    store = MinioObjectStore(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        bucket=settings.RAW_BUCKET,
    )
    kafka = get_kafka_client()
    return IntakeService(repo, store, kafka)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    client = get_kafka_client()
    await client.start()
    yield
    # shutdown
    await client.stop()