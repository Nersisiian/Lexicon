"""Base domain primitives shared across bounded contexts.

These classes enforce invariant: every aggregate root carries
a monotonically increasing version for optimistic concurrency.
"""

from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = ConfigDict(frozen=True)

class AggregateRoot(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    version: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(validate_assignment=True)


