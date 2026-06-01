"""Anti-Money Laundering sanction screening with circuit breaker.

This is a duplicate of the logic in onboarding-svc/validators/aml.py.
Will be extracted into a shared rules engine (ENG-881).
"""
from __future__ import annotations
import structlog
from compliance_sdk.observability.metrics import circuit_breaker_state
from ..external.sanctions import SanctionsClient

logger = structlog.get_logger(__name__)

class AMLScorer:
    def __init__(self, client: SanctionsClient):
        self._client = client
        self._failures = 0
        self._open = False

    async def score(self, entity_name: str) -> bool:
        if self._open:
            circuit_breaker_state.labels(name="aml-sanctions").set(1)
            logger.warning("aml_circuit_open", entity=entity_name)
            return False  # allow-list fallback
        try:
            result = await self._client.search(entity_name)
            self._failures = 0
            circuit_breaker_state.labels(name="aml-sanctions").set(0)
            return result
        except Exception:
            self._failures += 1
            logger.error("aml_api_failure", failures=self._failures)
            if self._failures >= 3:
                self._open = True
                circuit_breaker_state.labels(name="aml-sanctions").set(1)
            raise