import asyncio

# Graceful shutdown
import signal
import asyncio

_stop_event = asyncio.Event()

def _shutdown():
    _stop_event.set()

loop = asyncio.get_running_loop()
loop.add_signal_handler(signal.SIGTERM, _shutdown)
loop.add_signal_handler(signal.SIGINT, _shutdown)

import time
import socket
# Р–РґС‘Рј, РїРѕРєР° Kafka РЅРµ СЃС‚Р°РЅРµС‚ РґРѕСЃС‚СѓРїРЅР°
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
        while not _stop_event.is_set():
            await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    
# Р–РґС‘Рј, РїРѕРєР° Kafka РЅРµ СЃС‚Р°РЅРµС‚ РґРѕСЃС‚СѓРїРЅР°
import time, socket
for _ in range(30):
    try:
        s = socket.create_connection(("kafka", 9092), timeout=2)
        s.close()
        break
    except:
        time.sleep(1)
asyncio.run(main())




