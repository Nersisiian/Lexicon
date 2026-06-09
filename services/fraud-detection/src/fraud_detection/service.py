import json
from opentelemetry import trace
from compliance_sdk.observability.metrics import processing_duration
logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)
import structlog
from compliance_sdk.kafka import ResilientConsumer, KafkaClient
from compliance_sdk.observability.metrics import document_processed
from .ensemble import FraudEnsemble
from .config import settings

logger = structlog.get_logger(__name__)

class FraudDetectionService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="fraud-detection-v1",
            topics=["document.compliance.evaluated"],
            dlq_topic="document.fraud.dlq",
        )
        self._kafka = kafka
        self._model = FraudEnsemble(settings.MODEL_PATH)

    async def process(self, msg):
        doc_id = msg.key.decode()
            span.set_attribute("document_id", doc_id)
            with processing_duration.labels(service="fraud-detection", stage="fraud").time():
                # ... -> None:
        doc_id = msg.key.decode()
        data = json.loads(msg.value)
        # Extract features from compliance result; simplified here
        result = self._model.predict_risk(data)
        logger.info("fraud_assessment", doc_id=doc_id, prob=result["probability"])
        document_processed.labels(
            service="fraud-detection", document_type="unknown", status="fraud_checked"
        ).inc()
        await self._kafka.publish(
            "document.fraud.checked",
            key=doc_id,
            value=json.dumps(result).encode(),
        )

