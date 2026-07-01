from __future__ import annotations
import structlog
from opentelemetry import trace
from compliance_sdk.kafka import KafkaClient, ResilientConsumer
from .rules.aml import AMLScorer
from .rules.completeness import RULES_REGISTRY
from .external.sanctions import SanctionsClient
from .config import settings

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class ComplianceService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="compliance-engine-v1",
            topics=[f"document.classified.{settings.REGULATOR_ID}"],
            dlq_topic="document.compliance.dlq",
        )
        self._kafka = kafka
        sanctions = SanctionsClient(settings.SANCTIONS_API_URL)
        self._aml = AMLScorer(sanctions)

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        # msg.value is JSON containing classification + extracted entities
        import json
        data = json.loads(msg.value)
        label = data.get("label")
        extracted = data.get("entities", {})
        with tracer.start_as_current_span("compliance.evaluate") as span:
            span.set_attribute("document_id", doc_id)
            # 1. Completeness check
            rule = RULES_REGISTRY.get(label)
            if rule:
                completeness = rule.validate(extracted)
            else:
                completeness = {"score": 1.0, "missing_fields": []}
            # 2. AML screening (if entities contain names)
            aml_hits = []
            for entity in extracted.get("organizations", []):
                try:
                    if await self._aml.score(entity):
                        aml_hits.append(entity)
                except Exception:
                    logger.warning("aml_skip", entity=entity)
            result = {
                "completeness": completeness,
                "aml_hits": aml_hits,
                "overall_status": "pending_review" if aml_hits or completeness["score"] < 0.8 else "passed",
            }
            await self._kafka.publish(
                "document.compliance.evaluated",
                key=doc_id,
                value=json.dumps(result).encode(),
            )




