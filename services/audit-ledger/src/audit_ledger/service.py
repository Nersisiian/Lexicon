from datetime import datetime, timezone
import logging.handlers

siem_logger = logging.getLogger('siem')
siem_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(settings.SIEM_SYSLOG_HOST, settings.SIEM_SYSLOG_PORT))
siem_logger.addHandler(handler)

def audit_event(event: dict):
    siem_logger.info(str(event))
from uuid import uuid4
import structlog
import logging.handlers

siem_logger = logging.getLogger('siem')
siem_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(settings.SIEM_SYSLOG_HOST, settings.SIEM_SYSLOG_PORT))
siem_logger.addHandler(handler)

def audit_event(event: dict):
    siem_logger.info(str(event))
from opentelemetry import trace
import logging.handlers

siem_logger = logging.getLogger('siem')
siem_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(settings.SIEM_SYSLOG_HOST, settings.SIEM_SYSLOG_PORT))
siem_logger.addHandler(handler)

def audit_event(event: dict):
    siem_logger.info(str(event))
from .repository import AuditRepository
import logging.handlers

siem_logger = logging.getLogger('siem')
siem_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(settings.SIEM_SYSLOG_HOST, settings.SIEM_SYSLOG_PORT))
siem_logger.addHandler(handler)

def audit_event(event: dict):
    siem_logger.info(str(event))
from .models import AuditEvent
import logging.handlers

siem_logger = logging.getLogger('siem')
siem_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(settings.SIEM_SYSLOG_HOST, settings.SIEM_SYSLOG_PORT))
siem_logger.addHandler(handler)

def audit_event(event: dict):
    siem_logger.info(str(event))

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

