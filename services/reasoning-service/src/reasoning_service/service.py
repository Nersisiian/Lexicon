import json
from opentelemetry import trace
from compliance_sdk.observability.metrics import processing_duration
logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)
import structlog
from compliance_sdk.kafka import ResilientConsumer, KafkaClient
from .llm_client import LLMClient

logger = structlog.get_logger(__name__)

PROMPT_TEMPLATE = """
You are a senior compliance analyst. Review the following document summary and highlight risks and gaps.

Document type: {doc_type}
Extracted entities: {entities}
Completeness: {completeness}
Fraud flags: {fraud_flags}

Provide a concise risk assessment.
"""

class ReasoningService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="reasoning-v1",
            topics=["document.fraud.checked"],
            dlq_topic="document.reasoning.dlq",
        )
        self._kafka = kafka
        self._llm = LLMClient()

    async def process(self, msg):
        doc_id = msg.key.decode()
        with tracer.start_as_current_span("reasoning") as span:
            span.set_attribute("document_id", doc_id)
            with processing_duration.labels(service="reasoning-service", stage="llm").time():
                # ... -> None:
        doc_id = msg.key.decode()
        data = json.loads(msg.value)
        prompt = PROMPT_TEMPLATE.format(
            doc_type=data.get("doc_type", "unknown"),
            entities=data.get("entities", {}),
            completeness=data.get("completeness", {}),
            fraud_flags=data.get("fraud_flags", []),
        )
        try:
            reasoning = await self._llm.reason(prompt)
            logger.info("llm_reasoning_complete", doc_id=doc_id)
            await self._kafka.publish(
                "document.reasoned",
                key=doc_id,
                value=json.dumps({"reasoning": reasoning}).encode(),
            )
        except Exception:
            logger.exception("llm_failed", doc_id=doc_id)
            # Don't block pipeline; publish empty reasoning
            await self._kafka.publish(
                "document.reasoned",
                key=doc_id,
                value=json.dumps({"reasoning": "LLM unavailable"}).encode(),
            )
