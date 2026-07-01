import hashlib, json, httpx, logging
from .config import settings

logger = logging.getLogger(__name__)
BLOCKCYPHER_URL = "https://api.blockcypher.com/v1/eth/test/hook"

async def publish_hash(event: dict) -> str:
    if not settings.BLOCKCHAIN_ENABLED:
        return ""
    event_json = json.dumps(event, sort_keys=True, default=str)
    event_hash = hashlib.sha256(event_json.encode()).hexdigest()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(BLOCKCYPHER_URL, json={"event": "hash", "hash": event_hash})
            if resp.status_code == 200:
                tx = resp.json()
                logger.info("blockchain_publish", hash=event_hash, txid=tx.get("hash"))
                return tx.get("hash", "")
            else:
                logger.error("blockcypher_error", status=resp.status_code, text=resp.text)
    except Exception as e:
        logger.error("blockcypher_exception", error=str(e))
    return ""
