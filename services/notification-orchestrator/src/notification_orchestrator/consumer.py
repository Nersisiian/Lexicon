"""
Standalone Kafka consumer entry point for the notification orchestrator.

This module can be invoked directly for debugging or as a sidecar process.
The container uses main.py, which calls the same run function.
"""

import asyncio
import structlog
from compliance_sdk.kafka import KafkaClient
from compliance_sdk.observability.tracing import init_tracing
from compliance_sdk.observability.logging import configure_logging
from .config import settings
from .service import NotificationService

logger = structlog.get_logger(__name__)

async def run_consumer() -> None:
    configure_logging()
    init_tracing("notification-orchestrator")

    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "notification-orchestrator")
    await kafka.start()

    service = NotificationService(kafka)
    await service.consumer.start()

    logger.info("notification_consumer_started", topics=service.consumer.topics)
    try:
        await service.consumer.consume(service.process)
    finally:
        logger.info("notification_consumer_shutting_down")
        await service.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    asyncio.run(run_consumer())

