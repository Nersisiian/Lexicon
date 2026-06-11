import httpx
import structlog

logger = structlog.get_logger(__name__)

class SanctionsClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def search(self, name: str) -> bool:
        # Mock implementation: treat "ACME Corp" and "EvilCo" as sanctioned
        if name.lower() in ["acme corp", "evilco"]:
            return True
        # If a real API is configured, use it
        if self._base_url.startswith("http://real-api"):
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self._base_url}?q={name}")
                resp.raise_for_status()
                data = resp.json()
                return len(data.get("matches", [])) > 0
        return False

