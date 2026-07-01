from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, Request
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router
import time
from collections import defaultdict

configure_logging()
init_tracing("intake-gateway")

app = FastAPI(title="Intake Gateway", version="2.5")

# In-memory rate limiter (10 requests per 60 seconds per IP)
RATE_LIMIT = 10
WINDOW = 60
hits = defaultdict(list)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    # Remove old timestamps
    hits[ip] = [t for t in hits[ip] if now - t < WINDOW]
    if len(hits[ip]) >= RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
    hits[ip].append(now)
    return await call_next(request)


@app.middleware("http")
async def profiling_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(router)

@app.on_event("startup")
async def startup():
    pass
