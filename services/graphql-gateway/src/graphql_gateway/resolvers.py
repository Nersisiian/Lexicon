import strawberry
from typing import List
import httpx

INTAKE_GATEWAY_URL = "http://intake-gateway:8000"
ANALYTICS_URL = "http://analytics-engine:8003"

@strawberry.type
class Document:
    id: str
    status: str

@strawberry.type
class AnalyticsDocPerDay:
    day: str
    count: int

@strawberry.type
class Query:
    @strawberry.field
    async def documents(self) -> List[Document]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{INTAKE_GATEWAY_URL}/v2/documents")
            data = resp.json()
            # Заглушка: возвращаем фиктивные данные, если API недоступен
            if isinstance(data, list):
                return [Document(id=d["id"], status=d["status"]) for d in data]
            return [Document(id="1", status="accepted")]

    @strawberry.field
    async def analytics_documents_per_day(self) -> List[AnalyticsDocPerDay]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{ANALYTICS_URL}/analytics/documents-per-day")
            data = resp.json()
            if isinstance(data, list):
                return [AnalyticsDocPerDay(day=d["day"], count=d["count"]) for d in data]
            return [AnalyticsDocPerDay(day="2025-01-01", count=10)]

    @strawberry.field
    async def health(self) -> str:
        return "ok"
