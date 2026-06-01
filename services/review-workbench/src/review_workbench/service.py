from uuid import UUID, uuid4
import structlog
from .repository import ReviewRepository
from .models import ReviewTask

logger = structlog.get_logger(__name__)

class ReviewService:
    def __init__(self, repo: ReviewRepository):
        self._repo = repo

    async def assign(self, doc_id: UUID, reviewer: str) -> ReviewTask:
        task = ReviewTask(id=uuid4(), document_id=doc_id, reviewer=reviewer, status="pending")
        await self._repo.save(task)
        return task

    async def complete(self, task_id: UUID, decision: str) -> None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        task.status = "completed"
        task.decision = decision
        await self._repo.save(task)