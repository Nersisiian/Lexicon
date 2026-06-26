from typing import Any

class IntakeService:
    async def ingest(
        self,
        filename: str,
        content_type: str,
        content: bytes,
        tenant_id: str = "default",
    ) -> Any:
        # Stub implementation: in production, this saves to DB and returns a Document.
        return type("Document", (), {"id": "fake-id", "status": "accepted"})()