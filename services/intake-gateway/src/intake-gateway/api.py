"""Public API for document ingestion.

Deprecated v1 endpoint remains for legacy internal tools; will be removed Q4 2025 (PLAT-3421).
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
from .service import IntakeService
from .deps import get_intake_service

router = APIRouter()

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
    from aiokafka import AIOKafkaProducer
    try:
        producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await producer.start()
        await producer.stop()
        kafka_ok = True
    except Exception:
        kafka_ok = False
    status_code = 200 if kafka_ok else 503
    return Response(
        content='{"status":"ok","kafka":true}' if kafka_ok else '{"status":"degraded","kafka":false}',
        media_type="application/json",
        status_code=status_code,
    )

# Deprecated v1 endpoint Р В Р’В Р В РІР‚В Р В Р’В Р Р†Р вЂљРЎв„ўР В Р вЂ Р В РІР‚С™Р РЋРЎв„ў kept for backwards compatibility until all internal
# tools migrate to /v2. Remove after PLAT-3421.
@router.post("/documents", deprecated=True)
async def upload_v1(file: UploadFile = File(...)):
    raise HTTPException(410, detail="Use POST /v2/documents")

