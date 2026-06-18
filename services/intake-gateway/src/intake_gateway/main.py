from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response, JSONResponse

from fastapi import FastAPI

from slowapi.errors import RateLimitExceededfrom slowapi.util import get_remote_address
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router
from .limiter import limiter

configure_logging()
init_tracing("intake-gateway")

app = FastAPI(title="Intake Gateway", version="2.5")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(status_code=429, content={'detail': 'Too many requests'}))
app.include_router(router)

@app.on_event("startup")
async def startup():
    pass




