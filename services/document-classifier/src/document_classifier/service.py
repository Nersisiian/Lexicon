from __future__ import annotations
import structlog
from opentelemetry import trace
from compliance_sdk.kafka import KafkaClient, ResilientConsumer
from compliance_sdk.observability.metrics import document_processed
from .classifier import DocumentClassifierModel

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class ClassificationService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="classifier-v1",
            topics=["document.ocr.completed"],
            dlq_topic="document.classification.dlq",
        )
        self._kafka = kafka
        self._model = DocumentClassifierModel()

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        text = msg.value.decode()
        with tracer.start_as_current_span("classify") as span:
            span.set_attribute("document_id", doc_id)
            result = await self._model.classify(text)
            logger.info("classified", doc_id=doc_id, label=result["label"])
            document_processed.labels(
                service="document-classifier", document_type=result["label"], status="classified"
            ).inc()
            # Emit result downstream
            await self._kafka.publish(
                "document.classified",
                key=doc_id,
                value=str(result).encode(),
            )