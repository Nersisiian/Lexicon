from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field
from compliance_sdk.domain.base import AggregateRoot

class DocumentSubmission(BaseModel):
    filename: str
    content_type: str
    regulator_id: str
    s3_key_raw: str

class DocumentCreated(AggregateRoot):
    submission: DocumentSubmission
    status: str = "received"
