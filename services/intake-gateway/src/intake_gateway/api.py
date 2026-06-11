"""Public API for document ingestion.

Deprecated v1 endpoint remains for legacy internal tools; will be removed Q4 2025 (PLAT-3421).
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
from .service import IntakeService
from .deps import get_intake_service, limiter

router = APIRouter()

@limiter.limit("100/minute")
@router.post("/v2/documents")
async def upload_document(
    file: UploadFile = File(...),
    service: IntakeService = Depends(get_intake_service),
):
    if not file.filename:
        raise HTTPException(400, "filename required")
    content = await file.read()
    doc = await service.ingest(file.filename, file.content_type, content)
    return {"document_id": str(doc.id), "status": doc.status}

@router.get("/health")
async def health():
    return {"status": "ok"}

# Deprecated v1 endpoint – kept for backwards compatibility until all internal
# tools migrate to /v2. Remove after PLAT-3421.
@router.post("/documents", deprecated=True)
async def upload_v1(file: UploadFile = File(...)):
    raise HTTPException(410, detail="Use POST /v2/documents")


