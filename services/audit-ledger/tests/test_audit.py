import pytest
from unittest.mock import AsyncMock
from audit_ledger.service import AuditService
from audit_ledger.repository import AuditRepository

@pytest.mark.asyncio
async def test_record_event():
    repo = AsyncMock(spec=AuditRepository)
    svc = AuditService(repo)
    event = await svc.record({"action": "test"})
    repo.save.assert_called_once()
    assert event.action == "test"

