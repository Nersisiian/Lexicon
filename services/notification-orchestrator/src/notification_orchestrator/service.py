import json
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
        data = json.loads(msg.value)
        logger.info("notification_dispatch", doc_id=doc_id, event=event_type)

        if event_type == "document.reasoned":
            await self._send_slack(f"Document {doc_id} reasoning complete.")
            await self._send_email(f"Document {doc_id} reasoning complete", data.get("reasoning", ""))
        elif event_type == "document.review":
            await self._send_slack(f"Document {doc_id} needs human review.")
            await self._send_email(f"Document {doc_id} needs human review", json.dumps(data))

    async def _send_slack(self, text: str):
        if not settings.SLACK_WEBHOOK_URL:
            return
        async with httpx.AsyncClient() as client:
            await client.post(settings.SLACK_WEBHOOK_URL, json={"text": text})

    async def _send_email(self, subject: str, body: str):
        if not settings.SMTP_HOST:
            return
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = settings.SMTP_TO
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._send_smtp, msg)

    def _send_smtp(self, msg):
        import smtplib
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

