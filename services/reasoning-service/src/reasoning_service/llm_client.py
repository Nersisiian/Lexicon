"""LLM client for compliance reasoning."""
from __future__ import annotations
import httpx
import structlog
from .config import settings

logger = structlog.get_logger(__name__)

class LLMClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)

    async def reason(self, prompt: str) -> str:
        """Call the LLM endpoint or fall back to a mock response."""
        if not settings.LLM_ENDPOINT:
            return self._mock_response(prompt)

        try:
            resp = await self._client.post(
                settings.LLM_ENDPOINT,
                json={
                    "model": "compliance-llm",
                    "prompt": prompt,
                    "max_tokens": 500,
                    "temperature": 0.1,
                },
            )
            resp.raise_for_status()
            result = resp.json()["choices"][0]["text"].strip()
            logger.info("llm_reasoning_success", length=len(result))
            return result
        except Exception as e:
            logger.error("llm_reasoning_failed", error=str(e))
            return self._mock_response(prompt)

    @staticmethod
    def _mock_response(prompt: str) -> str:
        """Fallback when LLM is unavailable."""
        if "annual_report" in prompt:
            return "Low risk: financials appear consistent."
        if "aml_kyc" in prompt:
            return "Medium risk: entity name matches sanction list."
        return "Insufficient data for assessment."
