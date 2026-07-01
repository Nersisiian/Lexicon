import pytest
from unittest.mock import AsyncMock, patch
from ocr_pipeline.service import OCRPipelineService

@pytest.mark.asyncio
async def test_process_message():
    with patch("ocr_pipeline.service.extract_text", return_value="Sample text") as mock_ocr:
        msg = AsyncMock()
        msg.key = b"doc-1"
        msg.value = b"fake image"
        kafka = AsyncMock()
        service = OCRPipelineService(kafka)
        service.consumer = AsyncMock()
        await service.process(msg)
        mock_ocr.assert_called_once()

