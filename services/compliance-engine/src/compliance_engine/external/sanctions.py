"""Sanctions list checker using OpenSanctions API."""
from __future__ import annotations
import httpx
import structlog
from compliance_sdk.observability.metrics import circuit_breaker_state

logger = structlog.get_logger(__name__)

class SanctionsClient:
    def __init__(self, base_url: str = ""):
        self._base_url = base_url or "https://api.opensanctions.org"
        self._client = httpx.AsyncClient(timeout=10.0)
        self._failures = 0

    async def search(self, name: str) -> bool:
        """Return True if name matches any sanction list."""
        try:
            resp = await self._client.get(
                f"{self._base_url}/search/default",
                params={"q": name, "limit": 1},
            )
            resp.raise_for_status()
            data = resp.json()
            hits = data.get("total", 0)
            self._failures = 0
            circuit_breaker_state.labels(name="sanctions").set(0)
            return hits > 0
        except Exception:
            self._failures += 1
            logger.error("sanctions_api_failure", failures=self._failures)
            if self._failures >= 3:
                circuit_breaker_state.labels(name="sanctions").set(1)
            return False
