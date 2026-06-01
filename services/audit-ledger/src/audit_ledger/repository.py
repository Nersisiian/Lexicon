import json
from .models import AuditEvent
import asyncpg
import structlog

logger = structlog.get_logger(__name__)

class AuditRepository:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool = None

    async def _get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._dsn)
        return self._pool

    async def save(self, event) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO audit_events (event_id, timestamp, trace_id, span_id, service, user_id, action, payload) "
                "VALUES ($1,$2,$3,$4,$5,$6,$7,$8)",
                event.event_id, event.timestamp, event.trace_id, event.span_id,
                event.service, event.user_id, event.action, json.dumps(event.payload)
            )

    async def get_by_id(self, event_id) -> AuditEvent | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM audit_events WHERE event_id=$1", event_id
            )
            if row:
                return AuditEvent(**dict(row))
        return None
