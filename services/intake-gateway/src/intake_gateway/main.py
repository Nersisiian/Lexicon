from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, Request
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router
import redis.asyncio as redis
import time

configure_logging()
init_tracing("intake-gateway")

app = FastAPI(title="Intake Gateway", version="2.5")

# Rate-limit middleware (Redis)
LIMIT = 10           # requests
WINDOW = 60          # seconds
REDIS_URL = "redis://redis:6379/0"

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    r = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    now = int(time.time())
    window_start = now - WINDOW

    async with r.pipeline(transaction=True) as pipe:
        pipe.zremrangebyscore(key, 0, window_start)   # удаляем старые
        pipe.zcard(key)                                # текущее количество
        pipe.zadd(key, {str(now): now})                # добавляем текущий
        pipe.expire(key, WINDOW + 10)                  # TTL
        _, count, _, _ = await pipe.execute()

    if count > LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
    return await call_next(request)

app.include_router(router)

@app.on_event("startup")
async def startup():
    pass
