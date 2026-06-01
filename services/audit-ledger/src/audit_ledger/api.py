from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from .service import AuditService
from .deps import get_audit_service

router = APIRouter(prefix="/audit", tags=["audit"])

@router.post("/events")
async def record_event(payload: dict, service: AuditService = Depends(get_audit_service)):
    event = await service.record(payload)
    return {"event_id": str(event.event_id)}

@router.get("/events/{event_id}")
async def get_event(event_id: UUID, service: AuditService = Depends(get_audit_service)):
    event = await service.get(event_id)
    if not event:
        raise HTTPException(404)
    return event.dict()