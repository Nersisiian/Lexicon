import pytest
from unittest.mock import AsyncMock, patch
from compliance_sdk.kafka import KafkaClient

@pytest.mark.asyncio
async def test_publish():
    with patch("compliance_sdk.kafka.AIOKafkaProducer") as mock:
        client = KafkaClient(["localhost:9092"], "test-svc")
        client._producer = mock.return_value
        client._producer.send_and_wait = AsyncMock()
        await client.publish("test", "key", b"value")
        client._producer.send_and_wait.assert_called_once()