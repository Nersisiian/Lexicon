import pytest
from unittest.mock import AsyncMock
from compliance_engine.service import ComplianceService

@pytest.mark.asyncio
async def test_evaluation():
    svc = ComplianceService.__new__(ComplianceService)
    svc._kafka = AsyncMock()
    svc._aml = AsyncMock()
    svc._aml.score.return_value = False
    msg = AsyncMock()
    msg.key = b"doc-1"
    msg.value = b'{"label":"annual_report","entities":{"company_name":"ACME","revenue":"100"}}'
    await svc.process(msg)
    svc._kafka.publish.assert_called_once()

