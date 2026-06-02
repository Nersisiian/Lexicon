from fastapi import APIRouter, Depends
from uuid import UUID
from .service import ReviewService
from .deps import get_review_service
import asyncpg
from .config import settings

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/tasks/assign")
async def assign_task(doc_id: UUID, reviewer: str, service: ReviewService = Depends(get_review_service)):
    task = await service.assign(doc_id, reviewer)
    return {"task_id": str(task.id)}

@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: UUID, decision: str, service: ReviewService = Depends(get_review_service)):
    await service.complete(task_id, decision)
    return {"status": "completed"}

@router.get("/health")
async def health():
    try:
        conn = await asyncpg.connect(str(settings.DATABASE_URL))
        await conn.close()
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok", "database": db_ok}