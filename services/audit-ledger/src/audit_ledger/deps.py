from .service import AuditService
from .repository import AuditRepository
from .config import settings

_repo = AuditRepository(settings.DATABASE_URL)

def get_audit_service():
    return AuditService(_repo)