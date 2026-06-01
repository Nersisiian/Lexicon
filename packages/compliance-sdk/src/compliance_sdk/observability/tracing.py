"""Manual OTel bootstrapper. We avoid auto-instrumentation because
it caused duplicate spans in Kafka consumers (PLAT-299).
"""

from __future__ import annotations
import os
from opentelemetry import trace, propagate
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagators.textmap import Getter
import structlog

logger = structlog.get_logger(__name__)

def init_tracing(service_name: str) -> trace.Tracer | None:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        logger.warning("otel_collector_missing")
        return None
    resource = Resource(attributes={SERVICE_NAME: service_name})
    provider = TracerProvider(resource=resource)
    try:
        exporter = OTLPSpanExporter(endpoint=endpoint)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        return trace.get_tracer(service_name)
    except Exception:
        logger.exception("otel_init_failed", endpoint=endpoint)
        return None


class KafkaGetter(Getter):
    def get(self, carrier, key):
        for k, v in carrier:
            if k == key.encode():
                return [v.decode()]
        return []
    def keys(self, carrier):
        return [k.decode() for k, _ in carrier]

_propagator = propagate.get_global_textmap()

def extract_ctx_from_kafka(headers: list) -> trace.Context:
    return _propagator.extract(headers, getter=KafkaGetter())

def inject_ctx_to_kafka(headers: dict, ctx: trace.Context) -> dict:
    _propagator.inject(headers, context=ctx)
    return headers
