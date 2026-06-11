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
# Р В Р’В Р Р†Р вЂљРІР‚СљР В Р’В Р СћРІР‚ВР В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р РЋР’В, Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В° Kafka Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р Р†Р вЂљРЎв„ў Р В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚СћР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р РЋРІР‚СљР В Р’В Р РЋРІР‚вЂќР В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’В°
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
from .service import ClassificationService

configure_logging()
init_tracing("document-classifier")

async def main():
    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "document-classifier")
    await kafka.start()
    svc = ClassificationService(kafka)
    await svc.consumer.start()
    try:
        while not _stop_event.is_set():
            await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    
# Р В Р’В Р Р†Р вЂљРІР‚СљР В Р’В Р СћРІР‚ВР В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р РЋР’В, Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В° Kafka Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р Р†Р вЂљРЎв„ў Р В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚СћР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р РЋРІР‚СљР В Р’В Р РЋРІР‚вЂќР В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’В°
import time, socket
for _ in range(30):
    try:
        s = socket.create_connection(("kafka", 9092), timeout=2)
        s.close()
        break
    except:
        time.sleep(1)
asyncio.run(main())




