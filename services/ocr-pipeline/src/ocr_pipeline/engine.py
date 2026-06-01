"""OCR engine abstraction with legacy fallback.

PLAT-412: Legacy tesserocr path still used for vector‑heavy PDFs
because PaddleOCR struggles with CAD diagrams. Plan to replace with
a dedicated rasterization pre‑processor by Q2 2026.
"""
from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor
import structlog
from .config import settings

logger = structlog.get_logger(__name__)

# Legacy thread pool for blocking OCR; will be replaced by async gRPC engine.
_legacy_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ocr-legacy")

async def extract_text_paddle(image_bytes: bytes) -> str:
    # Async-compatible wrapper around PaddleOCR
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, ocr.ocr, image_bytes)
    texts = [line[1][0] for line in result[0]] if result and result[0] else []
    return "\n".join(texts)

async def extract_text_legacy(image_bytes: bytes) -> str:
    loop = asyncio.get_running_loop()
    # pytesseract not imported here to keep dependency light
    return await loop.run_in_executor(_legacy_executor, _tesseract_ocr, image_bytes)

def _tesseract_ocr(image_bytes):
    import pytesseract
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img)

async def extract_text(image_bytes: bytes) -> str:
    if settings.OCR_BACKEND == "paddle":
        try:
            return await extract_text_paddle(image_bytes)
        except Exception:
            logger.warning("paddle_failed_falling_back_to_legacy")
            return await extract_text_legacy(image_bytes)
    return await extract_text_legacy(image_bytes)