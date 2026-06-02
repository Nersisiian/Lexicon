import structlog
from .config import settings

logger = structlog.get_logger(__name__)

class LLMClient:
    async def reason(self, prompt: str) -> str:
        # Mock response for demonstration
        if "annual_report" in prompt:
            return "Low risk: financials appear consistent."
        if "aml_kyc" in prompt:
            return "Medium risk: entity name matches sanction list."
        return "Insufficient data for assessment."
