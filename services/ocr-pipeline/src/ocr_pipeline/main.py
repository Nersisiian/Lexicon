import signal
import asyncio
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from compliance_sdk.kafka import KafkaClient
from .config import settings
from .service import OCRPipelineService

configure_logging()
init_tracing("ocr-pipeline")

async def main():
    kafka = KafkaClient(settings.KAFKA_BOOTSTRAP_SERVERS, "ocr-pipeline")
    await kafka.start()
    svc = OCRPipelineService(kafka)
    await svc.consumer.start()

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        stop_event.set()

    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)

    try:
        await svc.consumer.consume(svc.process)
    finally:
        await svc.consumer.stop()
        await kafka.stop()

if __name__ == "__main__":
    asyncio.run(main())