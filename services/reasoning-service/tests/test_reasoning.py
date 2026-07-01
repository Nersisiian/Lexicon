import pytest
from unittest.mock import AsyncMock
from reasoning_service.service import ReasoningService

@pytest.mark.asyncio
async def test_reasoning():
    svc = ReasoningService.__new__(ReasoningService)
    svc._kafka = AsyncMock()
    svc._llm = AsyncMock()
    svc._llm.reason.return_value = "Low risk"
    msg = AsyncMock()
    msg.key = b"doc-1"
    msg.value = b'{"doc_type":"annual_report","entities":{},"completeness":{},"fraud_flags":[]}'
    await svc.process(msg)
    svc._kafka.publish.assert_called_once()

