from __future__ import annotations
import structlog
from opentelemetry import trace
from compliance_sdk.kafka import KafkaClient, ResilientConsumer
from compliance_sdk.observability.metrics import processing_duration, document_processed
from .engine import extract_text

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class OCRPipelineService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="ocr-pipeline-v3",
            topics=["document.ingested"],
            dlq_topic="document.ocr.dlq",
            max_retries=2,
        )
        self._kafka = kafka

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        with tracer.start_as_current_span("ocr.process") as span:
            span.set_attribute("document_id", doc_id)
            logger.info("processing_ocr", doc_id=doc_id)
            # In production, we'd fetch the raw bytes from S3 using doc_id.
            # Simulated here: assume msg.value contains raw bytes (simplified).
            raw_bytes = msg.value
            with processing_duration.labels(service="ocr-pipeline", stage="ocr").time():
                try:
                    text = await extract_text(raw_bytes)
                except Exception:
                    logger.exception("ocr_failed", doc_id=doc_id)
                    document_processed.labels(
                        service="ocr-pipeline", document_type="unknown", status="ocr_error"
                    ).inc()
                    raise
            # Publish completion event
            await self._kafka.publish(
                "document.ocr.completed",
                key=doc_id,
                value=text.encode()[:100_000],  # truncation guard
            )
            document_processed.labels(
                service="ocr-pipeline", document_type="unknown", status="ocr_completed"
            ).inc()
