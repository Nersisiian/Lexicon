"""
Kafka consumer lifecycle for the compliance engine.

This module exists so that the service can be started as a standalone process
using `python -m compliance_engine.consumer` without touching FastAPI.
In containerised deployments it is called from main.py.
"""

import asyncio
import structlog
from compliance_sdk.kafka import KafkaClient
from compliance_sdk.observability.tracing import init_tracing
from compliance_sdk.observability.logging import configure_logging
from .config import settings
from .service import ComplianceService

logger = structlog.get_logger(__name__)

async def run_consumer() -> None:
    """Bootstrap Kafka and start processing messages."""
    configure_logging()
    init_tracing("compliance-engine")

    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "compliance-engine")
    await kafka.start()

    service = ComplianceService(kafka)
    await service.consumer.start()

    logger.info("compliance_consumer_started", topics=service.consumer.topics)
    try:
        await service.consumer.consume(service.process)
    finally:
        logger.info("compliance_consumer_shutting_down")
        await service.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    asyncio.run(run_consumer())


