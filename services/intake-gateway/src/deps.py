"""Manual DI container; not using a framework to avoid magic."""
from functools import lru_cache
from compliance_sdk.kafka import KafkaClient
from .config import settings
from .service import IntakeService
from .repository import DocumentRepository
from .storage import MinioObjectStore

@lru_cache()
def get_kafka_client() -> KafkaClient:
    client = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "intake-gateway")
    # In production this would be started once, but for simplicity we rely on lifespan
    return client

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