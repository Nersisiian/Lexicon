"""Kafka client wrappers with built-in tracing, retries, and DLQ support.

All services use these abstractions to ensure uniform error handling,
trace propagation, and DLQ routing per the platform's SLOs.
Refactored after INC-2025-08-14 to include per‑message retry budgets.
"""

from __future__ import annotations
import asyncio
from typing import Optional
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import structlog
from opentelemetry import trace, context
from .observability.tracing import inject_ctx_to_kafka, extract_ctx_from_kafka

logger = structlog.get_logger(__name__)

class KafkaClient:
    """Shared producer used across services. Must be started before publishing."""

    def __init__(self, bootstrap_servers: str, service_name: str):
        self.bootstrap_servers = [s.strip() for s in bootstrap_servers.split(',')]
        self.service_name = service_name
        self._producer: Optional[AIOKafkaProducer] = None
        self.tracer = trace.get_tracer(service_name)

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()

    async def publish(self, topic: str, key: str, value: bytes, headers: Optional[dict] = None) -> None:
        if self._producer is None:
            raise RuntimeError("KafkaClient not started")
        headers = dict(headers or {})
        inject_ctx_to_kafka(headers, context.get_current())
        try:
            with self.tracer.start_as_current_span(f"kafka.publish {topic}"):
                await self._producer.send_and_wait(topic, key=key.encode(), value=value, headers=list(headers.items()))
        except Exception:
            logger.exception("kafka_publish_failed", topic=topic, key=key)
            raise


class ResilientConsumer:
    """Consumer that implements per-message retries and DLQ routing.

    After max_retries attempts, the message is sent to dlq_topic and committed.
    This prevents a single poison message from blocking the entire partition.
    """

    def __init__(
        self,
        bootstrap_servers: list[str],
        group_id: str,
        topics: list[str],
        dlq_topic: str,
        max_retries: int = 3,
    ):
        self.bootstrap_servers = [s.strip() for s in bootstrap_servers.split(',')]
        self.group_id = group_id
        self.topics = topics
        self.dlq_topic = dlq_topic
        self.max_retries = max_retries
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._producer: Optional[AIOKafkaProducer] = None
        self.tracer = trace.get_tracer(__name__)

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False,
        )
        self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await asyncio.gather(self._consumer.start(), self._producer.start())

    async def stop(self) -> None:
        if self._consumer:
            await self._consumer.stop()
        if self._producer:
            await self._producer.stop()

    async def consume(self, handler) -> None:
        async for msg in self._consumer:
            ctx = extract_ctx_from_kafka(msg.headers)
            token = context.attach(ctx)
            retry_count = 0
            with self.tracer.start_as_current_span(f"consume {msg.topic}"):
                span = trace.get_current_span()
                span.set_attribute("kafka.offset", msg.offset)
                while retry_count <= self.max_retries:
                    try:
                        await handler(msg)
                        await self._consumer.commit()
                        break
                    except Exception as exc:
                        retry_count += 1
                        logger.warning("consumer_retry", offset=msg.offset, attempt=retry_count, error=str(exc))
                        if retry_count > self.max_retries:
                            logger.error("dlq_routing", offset=msg.offset, dlq=self.dlq_topic)
                            await self._producer.send_and_wait(
                                self.dlq_topic,
                                key=msg.key,
                                value=msg.value,
                                headers=msg.headers,
                            )
                            await self._consumer.commit()
                            break
                        else:
                            await asyncio.sleep(2 ** retry_count)
            context.detach(token)


