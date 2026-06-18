from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response, JSONResponse

from fastapi import FastAPI

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router

configure_logging()
init_tracing("intake-gateway")

app = FastAPI(title="Intake Gateway", version="2.5")
app.include_router(router)

@app.on_event("startup")
async def startup():
    pass




