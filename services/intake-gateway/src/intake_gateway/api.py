"""Public API for document ingestion.

Deprecated v1 endpoint remains for legacy internal tools; will be removed Q4 2025 (PLAT-3421).
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response, Request
from .service import IntakeService
from .deps import get_intake_service
from .metrics import DOCUMENTS_UPLOADED, PROCESSING_TIME
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
@router.post("/v2/documents", summary="Upload a document for compliance processing",
          description="Upload a PDF or image. The document goes through OCR, classification, compliance checks, and fraud detection.")
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

# Deprecated v1 endpoint вЂ“ kept for backwards compatibility until all internal
# tools migrate to /v2. Remove after PLAT-3421.
@router.post("/documents", deprecated=True)
async def upload_v1(file: UploadFile = File(...)):
    raise HTTPException(410, detail="Use POST /v2/documents")