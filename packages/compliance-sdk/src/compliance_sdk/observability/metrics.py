from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest

REGISTRY = CollectorRegistry(auto_describe=True)

document_processed = Counter(
    "document_processed_total", "Documents by final status",
    ["service", "document_type", "status"], registry=REGISTRY
)
processing_duration = Histogram(
    "document_processing_seconds", "PerР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р В РІР‚В Р В Р’В Р Р†Р вЂљРЎв„ўР В РІР‚в„ўР вЂ™Р’Вstage processing time",
    ["service", "stage"], buckets=(0.5, 1, 5, 15, 30, 60, 120), registry=REGISTRY
)
consumer_lag = Gauge(
    "kafka_consumer_lag_records", "Approximate lag",
    ["topic", "partition", "group"], registry=REGISTRY
)
circuit_breaker_state = Gauge(
    "circuit_breaker_state", "1=open", ["name"], registry=REGISTRY
)

def metrics_endpoint():
    return generate_latest(REGISTRY)

