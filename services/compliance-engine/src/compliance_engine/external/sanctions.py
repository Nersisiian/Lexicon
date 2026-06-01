import httpx
import structlog

logger = structlog.get_logger(__name__)

class SanctionsClient:
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(timeout=5.0)
        self._base_url = base_url

    async def search(self, name: str) -> bool:
        resp = await self._client.get(f"{self._base_url}?q={name}")
        resp.raise_for_status()
        data = resp.json()
        return len(data.get("matches", [])) > 0