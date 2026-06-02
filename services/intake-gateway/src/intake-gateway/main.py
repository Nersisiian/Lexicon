import signal
import asyncio
from fastapi import FastAPI
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router
from .config import settings
from .deps import get_kafka_client

configure_logging()
init_tracing("intake-gateway")

async def lifespan(app: FastAPI):
    client = get_kafka_client()
    await client.start()
    yield
    await client.stop()

app = FastAPI(title="Intake Gateway", version="2.5", lifespan=lifespan)
app.include_router(router)