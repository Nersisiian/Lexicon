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
# Р В РІР‚вЂњР В РўвЂР РЋРІР‚ВР В РЎВ, Р В РЎвЂ”Р В РЎвЂўР В РЎвЂќР В Р’В° Kafka Р В Р вЂ¦Р В Р’Вµ Р РЋР С“Р РЋРІР‚С™Р В Р’В°Р В Р вЂ¦Р В Р’ВµР РЋРІР‚С™ Р В РўвЂР В РЎвЂўР РЋР С“Р РЋРІР‚С™Р РЋРЎвЂњР В РЎвЂ”Р В Р вЂ¦Р В Р’В°
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
from .service import FraudDetectionService

configure_logging()
init_tracing("fraud-detection")

async def main():
    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "fraud-detection")
    await kafka.start()
    svc = FraudDetectionService(kafka)
    await svc.consumer.start()
    try:
        while not _stop_event.is_set():
            await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    
# Р В РІР‚вЂњР В РўвЂР РЋРІР‚ВР В РЎВ, Р В РЎвЂ”Р В РЎвЂўР В РЎвЂќР В Р’В° Kafka Р В Р вЂ¦Р В Р’Вµ Р РЋР С“Р РЋРІР‚С™Р В Р’В°Р В Р вЂ¦Р В Р’ВµР РЋРІР‚С™ Р В РўвЂР В РЎвЂўР РЋР С“Р РЋРІР‚С™Р РЋРЎвЂњР В РЎвЂ”Р В Р вЂ¦Р В Р’В°
import time, socket
for _ in range(30):
    try:
        s = socket.create_connection(("kafka", 9092), timeout=2)
        s.close()
        break
    except:
        time.sleep(1)
asyncio.run(main())




