from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class AuditEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trace_id: str = ""
    span_id: str = ""
    service: str = "unknown"
    user_id: str | None = None
    action: str = "record"
    payload: dict