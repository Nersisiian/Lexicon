"""Structured logging configuration used by every service.

After INC-2025-03 (logging pipeline migration), we standardised on structlog
with JSON in staging/prod and coloured console in dev.
"""

from __future__ import annotations
import os
import structlog
from structlog.types import Processor
from opentelemetry import trace

def _inject_trace_ids(logger, method_name, event_dict):
    ctx = trace.get_current_span().get_span_context()
    if ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict

def _add_service_name(_, __, event_dict):
    event_dict.setdefault("service", os.getenv("OTEL_SERVICE_NAME", "unknown"))
    return event_dict

def configure_logging(level: str = "INFO") -> None:
    env = os.getenv("DEPLOY_ENV", "dev")
    renderer = (
        structlog.dev.ConsoleRenderer() if env == "dev"
        else structlog.processors.JSONRenderer()
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _inject_trace_ids,
            _add_service_name,
            structlog.processors.dict_tracebacks,
            renderer,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )