import asyncpg
import structlog
from datetime import timezone
from .domain.document import DocumentCreated

logger = structlog.get_logger(__name__)

class DocumentRepository:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool = None

    async def _get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._dsn)
        return self._pool

    @property
    def regulator_id(self) -> str:
        return "default"

    async def save(self, doc: DocumentCreated) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO documents (id, regulator_id, filename, content_type, s3_key_raw, status, created_at, updated_at) "
                "VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                doc.id, doc.submission.regulator_id, doc.submission.filename,
                doc.submission.content_type, doc.submission.s3_key_raw,
                doc.status,
                doc.created_at.astimezone(timezone.utc),
                doc.updated_at.astimezone(timezone.utc),
            )


