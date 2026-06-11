from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel\nfrom compliance_sdk.domain.base import AggregateRoot

class DocumentSubmission(BaseModel):
    filename: str
    content_type: str
    regulator_id: str
    s3_key_raw: str

class DocumentCreated(AggregateRoot):
    submission: DocumentSubmission
    status: str = "received"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))




