class IntakeService:
    def __init__(self, repository=None, storage=None, kafka=None):
        self.repo = repository
        self.store = storage
        self.kafka = kafka

    async def ingest(self, filename: str, content_type: str, content: bytes):
        # В production здесь сохранение в БД и отправка в Kafka.
        # Пока возвращаем заглушку.
        return type("Document", (), {"id": "fake-id", "status": "accepted"})()
