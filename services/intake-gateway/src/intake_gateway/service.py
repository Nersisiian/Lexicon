from .deps import get_repository  # предположим, что есть такой доступ к репозиторию
from .domain.document import Document  # модель документа

class IntakeService:
    def __init__(self, repository=None):
        self.repository = repository or get_repository()

    async def ingest(self, filename: str, content_type: str, content: bytes, tenant_id: str = "default") -> Document:
        """Принимает документ, сохраняет его в БД и возвращает объект Document."""
        doc = Document(
            tenant_id=tenant_id,
            filename=filename,
            content_type=content_type,
            status="accepted",
            content=content
        )
        await self.repository.save(doc)
        return doc
