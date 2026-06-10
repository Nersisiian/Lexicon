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
from .service import ReasoningService

configure_logging()
init_tracing("reasoning-service")

async def main():
    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "reasoning-service")
    await kafka.start()
    svc = ReasoningService(kafka)
    await svc.consumer.start()
    try:
        await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    
# ∆дЄм, пока Kafka не станет доступна
import time, socket
for _ in range(30):
    try:
        s = socket.create_connection(("kafka", 9092), timeout=2)
        s.close()
        break
    except:
        time.sleep(1)
asyncio.run(main())

