"""Async PostgreSQL repository for review tasks.

Uses asyncpg directly (not SQLAlchemy ORM) to align with
the rest of the platform and keep dependencies light.
"""

from __future__ import annotations
from uuid import UUID
import asyncpg
import structlog
from .models import ReviewTask

logger = structlog.get_logger(__name__)

class ReviewRepository:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._dsn, min_size=2, max_size=10)
        return self._pool

    async def save(self, task: ReviewTask) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO review_tasks (id, document_id, reviewer, status, decision, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO UPDATE
                SET status = EXCLUDED.status,
                    decision = EXCLUDED.decision
                """,
                task.id, task.document_id, task.reviewer,
                task.status, task.decision, task.created_at,
            )

    async def get_by_id(self, task_id: UUID) -> ReviewTask | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, document_id, reviewer, status, decision, created_at "
                "FROM review_tasks WHERE id = $1", task_id
            )
            if row is None:
                return None
            return ReviewTask(
                id=row["id"],
                document_id=row["document_id"],
                reviewer=row["reviewer"],
                status=row["status"],
                decision=row["decision"],
                created_at=row["created_at"],
            )

    async def list_pending(self, reviewer: str | None = None) -> list[ReviewTask]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            query = "SELECT id, document_id, reviewer, status, decision, created_at FROM review_tasks WHERE status = 'pending'"
            params = []
            if reviewer:
                query += " AND reviewer = $1"
                params.append(reviewer)
            rows = await conn.fetch(query, *params)
            return [
                ReviewTask(
                    id=r["id"], document_id=r["document_id"],
                    reviewer=r["reviewer"], status=r["status"],
                    decision=r["decision"], created_at=r["created_at"],
                )
                for r in rows
            ]
