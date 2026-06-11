from fastapi import FastAPI
from compliance_sdk.observability.logging import configure_logging
from compliance_sdk.observability.tracing import init_tracing
from .api import router

configure_logging()
init_tracing("review-workbench")

app = FastAPI(title="Review Workbench")
app.include_router(router)
