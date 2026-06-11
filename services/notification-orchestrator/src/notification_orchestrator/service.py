import httpx
import structlog
from compliance_sdk.kafka import ResilientConsumer, KafkaClient
from .config import settings

logger = structlog.get_logger(__name__)

class NotificationService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="notification-v1",
            topics=["document.reasoned", "document.review"],
            dlq_topic="notification.dlq",
        )
        self._kafka = kafka

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        event_type = msg.topic
        logger.info("notification_dispatch", doc_id=doc_id, event=event_type)
        if event_type == "document.reasoned":
            await self._send_slack(f"Document {doc_id} reasoning complete.")
        elif event_type == "document.review":
            await self._send_slack(f"Document {doc_id} needs human review.")

    async def _send_slack(self, text: str):
        if not settings.SLACK_WEBHOOK_URL:
            logger.info("slack_disabled", text=text)
            return
        async with httpx.AsyncClient() as client:
            await client.post(settings.SLACK_WEBHOOK_URL, json={"text": text})




