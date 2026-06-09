import json
import structlog
from compliance_sdk.kafka import ResilientConsumer, KafkaClient
from compliance_sdk.observability.metrics import document_processed, processing_duration
from opentelemetry import trace
from .ensemble import FraudEnsemble
from .config import settings

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

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

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        data = json.loads(msg.value)
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