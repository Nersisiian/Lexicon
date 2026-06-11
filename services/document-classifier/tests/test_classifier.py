import pytest
from unittest.mock import AsyncMock, patch
from document_classifier.service import ClassificationService

@pytest.mark.asyncio
async def test_classify():
    with patch.object(ClassificationService, "__init__", lambda self: None):
        svc = ClassificationService.__new__(ClassificationService)
        svc._model = AsyncMock()
        svc._model.classify.return_value = {"label": "annual_report", "score": 0.95}
        svc._kafka = AsyncMock()
        msg = AsyncMock()
        msg.key = b"doc-1"
        msg.value = b"Annual financial statements..."
        await svc.process(msg)
        svc._model.classify.assert_called_once()
