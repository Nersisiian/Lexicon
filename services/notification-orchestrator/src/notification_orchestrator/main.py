import asyncio

import time
import socket
# ∆дЄм, пока Kafka не станет доступна
for _ in range(30):
    try:
        s = socket.create_connection(("kafka", 9092), timeout=2)
        s.close()
        break
    except:
        time.sleep(1)
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from compliance_sdk.kafka import KafkaClient
from .config import settings
from .service import NotificationService

configure_logging()
init_tracing("notification-orchestrator")

async def main():
    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "notification-orchestrator")
    await kafka.start()
    svc = NotificationService(kafka)
    await svc.consumer.start()
    try:
        await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    asyncio.run(main())
