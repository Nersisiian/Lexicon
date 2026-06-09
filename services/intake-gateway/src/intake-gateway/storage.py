from abc import ABC, abstractmethod
from minio import Minio
import structlog

logger = structlog.get_logger(__name__)

class ObjectStore(ABC):
    @abstractmethod
    async def upload(self, key: str, data: bytes) -> None:
        ...

class MinioObjectStore(ObjectStore):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        self._client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self._bucket = bucket
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    async def upload(self, key: str, data: bytes) -> None:
        import asyncio
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, self._client.put_object, self._bucket, key, data, len(data)
        )