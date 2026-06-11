"""Document classifier using HuggingFace transformers."""
from __future__ import annotations
import asyncio
from transformers import pipeline
import structlog
from .config import settings

logger = structlog.get_logger(__name__)

class DocumentClassifierModel:
    def __init__(self):
        logger.info("loading_model", name=settings.MODEL_NAME)
        self._pipe = pipeline(
            "text-classification",
            model=settings.MODEL_NAME,
            device=settings.DEVICE,
        )

    async def classify(self, text: str) -> dict:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, lambda: self._pipe(text[:512])
        )
        return {"label": result[0]["label"], "score": result[0]["score"]}
