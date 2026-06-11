from datetime import datetime, timezone
from uuid import uuid4
import structlog
from opentelemetry import trace
from .repository import AuditRepository
from .models import AuditEvent

logger = structlog.get_logger(__name__)

class AuditService:
    def __init__(self, repo: AuditRepository):
        self._repo = repo

    async def record(self, payload: dict) -> AuditEvent:
        span_context = trace.get_current_span().get_span_context()
        event = AuditEvent(
            event_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            trace_id=format(span_context.trace_id, "032x") if span_context.is_valid else "",
            span_id=format(span_context.span_id, "016x") if span_context.is_valid else "",
            payload=payload,
        )
        await self._repo.save(event)
        logger.info("audit_event_recorded", event_id=str(event.event_id))
        return event

    async def get(self, event_id) -> AuditEvent | None:
        return await self._repo.get_by_id(event_id)
