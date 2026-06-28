import hashlib
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

def publish_hash(event: dict) -> str:
    """Публикует хеш события в DLT (заглушка)."""
    if not settings.BLOCKCHAIN_ENABLED:
        return ""
    event_json = json.dumps(event, sort_keys=True, default=str)
    event_hash = hashlib.sha256(event_json.encode()).hexdigest()
    # В реальном проекте здесь будет вызов DLT API (Hyperledger, Ethereum)
    logger.info("blockchain_publish", hash=event_hash, event_id=event.get("id"))
    return event_hash
