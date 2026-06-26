import structlog
from opentelemetry import trace
from compliance_sdk.kafka import KafkaClient
from compliance_sdk.observability.metrics import document_processed
from .domain.document import DocumentSubmission, DocumentCreated
from .storage import ObjectStore
from .repository import DocumentRepository
from .config import settings

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class IntakeService:
    def __init__(self, repo: DocumentRepository, storage: ObjectStore, kafka: KafkaClient):
        self._repo = repo
        self._storage = storage
        self._kafka = kafka

    async def ingest(self, filename: str, content_type: str, content: bytes) -> DocumentCreated:
        with tracer.start_as_current_span("intake.ingest") as span:
            span.set_attribute("filename", filename)
            s3_key = f"{settings.REGULATOR_ID}/{filename}"
            await self._storage.upload(s3_key, content)
            submission = DocumentSubmission(
                filename=filename, content_type=content_type,
                regulator_id=settings.REGULATOR_ID, s3_key_raw=s3_key
            )
            doc = DocumentCreated(submission=submission)
            await self._repo.save(doc)
            # РџСѓР±Р»РёРєР°С†РёСЏ РІ Kafka вЂ“ РѕРїС†РёРѕРЅР°Р»СЊРЅРѕ (РјРѕР¶РµС‚ Р±С‹С‚СЊ РЅРµРґРѕСЃС‚СѓРїРЅР° РІ С‚РµСЃС‚Р°С…)
            try:
                await self._kafka.publish(
                    f"document.ingested.{settings.REGULATOR_ID}",
                    key=str(doc.id),
                    value=doc.json().encode(),
                )
            except Exception as e:
                logger.warning("kafka_publish_failed", error=str(e))
            document_processed.labels(
                service="intake-gateway", document_type="unknown", status="received"
            ).inc()
            logger.info(f"document.ingested.{settings.REGULATOR_ID}", doc_id=str(doc.id))
            return doc

