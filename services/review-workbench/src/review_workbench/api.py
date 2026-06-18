from fastapi import APIRouter, Depends
from uuid import UUID
from .service import ReviewService
from .deps import get_review_service
import asyncpg
from .config import settings

router = APIRouter(prefix="/review", tags=["review"])


import csv
import io
from fastapi.responses import StreamingResponse

@router.get("/export/csv")
async def export_documents_csv():
    docs = await repository.get_all_documents()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "regulator_id", "status", "created_at"])
    for doc in docs:
        writer.writerow([doc.id, doc.regulator_id, doc.status, doc.created_at])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=documents.csv"})
@router.post("/tasks/assign")
async def assign_task(doc_id: UUID, reviewer: str, service: ReviewService = Depends(get_review_service)):
    task = await service.assign(doc_id, reviewer)
    return {"task_id": str(task.id)}


import csv
import io
from fastapi.responses import StreamingResponse

@router.get("/export/csv")
async def export_documents_csv():
    docs = await repository.get_all_documents()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "regulator_id", "status", "created_at"])
    for doc in docs:
        writer.writerow([doc.id, doc.regulator_id, doc.status, doc.created_at])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=documents.csv"})
@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: UUID, decision: str, service: ReviewService = Depends(get_review_service)):
    await service.complete(task_id, decision)
    return {"status": "completed"}


import csv
import io
from fastapi.responses import StreamingResponse

@router.get("/export/csv")
async def export_documents_csv():
    docs = await repository.get_all_documents()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "regulator_id", "status", "created_at"])
    for doc in docs:
        writer.writerow([doc.id, doc.regulator_id, doc.status, doc.created_at])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=documents.csv"})
@router.get("/health")
async def health():
    try:
        conn = await asyncpg.connect(str(settings.DATABASE_URL))
        await conn.close()
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok", "database": db_ok}

