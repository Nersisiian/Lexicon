from fastapi import FastAPI
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router
from .config import settings

configure_logging()
init_tracing("intake-gateway")

app = FastAPI(title="Intake Gateway", version="2.5")
app.include_router(router)

@app.on_event("startup")
async def startup():
    # pre-warm connections, etc.
    pass