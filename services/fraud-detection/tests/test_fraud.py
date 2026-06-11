import pytest
from unittest.mock import AsyncMock
from fraud_detection.service import FraudDetectionService

@pytest.mark.asyncio
async def test_fraud_check():
    svc = FraudDetectionService.__new__(FraudDetectionService)
    svc._kafka = AsyncMock()
    svc._model = AsyncMock()
    svc._model.predict_risk.return_value = {"probability": 0.1}
    msg = AsyncMock()
    msg.key = b"doc-1"
    msg.value = b'{"completeness":{"score":0.9}}'
    await svc.process(msg)
    svc._kafka.publish.assert_called_once()
