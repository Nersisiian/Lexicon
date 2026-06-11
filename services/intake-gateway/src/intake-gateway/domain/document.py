from __future__ import annotations
from pydantic import BaseModel
from compliance_sdk.domain.base import AggregateRoot

class DocumentSubmission(BaseModel):
    filename: str
    content_type: str
    regulator_id: str
    s3_key_raw: str

class DocumentCreated(AggregateRoot):
    submission: DocumentSubmission
    status: str = "received"


