from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ReviewTask(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    reviewer: str
    status: str = "pending"
    decision: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))