"""Public API for document ingestion.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response, Request
from .service import IntakeService
from .deps import get_intake_service
from .metrics import DOCUMENTS_UPLOADED, PROCESSING_TIME

router = APIRouter()

@router.post("/v2/documents")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    service: IntakeService = Depends(get_intake_service),
):
    DOCUMENTS_UPLOADED.inc()
    with PROCESSING_TIME.time():
        if not file.filename:
            raise HTTPException(400, "filename required")
        content = await file.read()
        doc = await service.ingest(file.filename, file.content_type, content)
        return {"document_id": str(doc.id), "status": doc.status}

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/documents", deprecated=True)
async def upload_v1(file: UploadFile = File(...)):
    raise HTTPException(410, detail="Use POST /v2/documents")
