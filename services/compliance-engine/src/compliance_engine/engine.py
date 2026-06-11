"""Core compliance evaluation engine.

Isolated from Kafka transport so it can be tested independently and reused
by synchronous batch processes if needed.
"""

from __future__ import annotations
from typing import Dict, Any, List
import structlog
from opentelemetry import trace
from compliance_sdk.observability.metrics import processing_duration, document_processed
from .rules.aml import AMLScorer
from .rules.completeness import RULES_REGISTRY
from .external.sanctions import SanctionsClient
from .config import settings

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class ComplianceEngine:
    """Evaluates a document against all active compliance rules.

    Dependencies (AML scorer) are initialised once per process;
    the engine itself is stateless and safe to call concurrently.
    """

    def __init__(self) -> None:
        sanctions_client = SanctionsClient(settings.SANCTIONS_API_URL)
        self._aml = AMLScorer(sanctions_client)

    async def evaluate(self, doc_id: str, doc_type: str, extracted_entities: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full compliance check suite.

        Returns a dictionary suitable for downstream consumers.
        """
        with tracer.start_as_current_span("compliance.engine.evaluate") as span:
            span.set_attribute("document_id", doc_id)
            span.set_attribute("doc_type", doc_type)

            # 1. Completeness validation
            completeness_result = self._check_completeness(doc_type, extracted_entities)

            # 2. AML sanction screening (only for organisation entities)
            aml_hits = await self._run_aml_screening(extracted_entities.get("organizations", []))

            # 3. Determine overall status
            overall_status = self._compute_overall_status(completeness_result, aml_hits)

            with processing_duration.labels(service="compliance-engine", stage="full_evaluation").time():
                result = {
                    "completeness": completeness_result,
                    "aml_hits": aml_hits,
                    "overall_status": overall_status,
                }

            document_processed.labels(
                service="compliance-engine",
                document_type=doc_type,
                status=overall_status,
            ).inc()

            logger.info(
                "compliance_evaluation_complete",
                doc_id=doc_id,
                doc_type=doc_type,
                overall=overall_status,
            )
            return result

    def _check_completeness(self, doc_type: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        rule = RULES_REGISTRY.get(doc_type)
        if rule is None:
            return {"score": 1.0, "missing_fields": []}
        return rule.validate(entities)

    async def _run_aml_screening(self, organisations: List[str]) -> List[str]:
        hits = []
        for org in organisations:
            try:
                if await self._aml.score(org):
                    hits.append(org)
            except Exception:
                logger.warning("aml_check_skipped", organisation=org)
        return hits

    def _compute_overall_status(self, completeness: Dict[str, Any], aml_hits: List[str]) -> str:
        if aml_hits or completeness["score"] < 0.8:
            return "pending_review"
        return "passed"
