import httpx
import structlog
from .config import settings

logger = structlog.get_logger(__name__)

class LLMClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)

    async def reason(self, prompt: str) -> str:
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
        return resp.json()["choices"][0]["text"]