import strawberry
from typing import List
import httpx

@strawberry.federation.type(keys=["id"])
class Document:
    id: strawberry.ID
    status: str = ""
    @classmethod
    async def resolve_reference(cls, info, id: strawberry.ID):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://intake-gateway:8000/v2/documents/{id}/status")
            data = resp.json()
            return cls(id=id, status=data.get("status", "unknown"))

@strawberry.federation.type(keys=["id"])
class FraudAssessment:
    id: strawberry.ID
    probability: float = 0.0
    @classmethod
    async def resolve_reference(cls, info, id: strawberry.ID):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://fraud-detection:8001/assessment/{id}")
            data = resp.json()
            return cls(id=id, probability=data.get("probability", 0.0))

@strawberry.type
class Query:
    @strawberry.field
    async def documents(self) -> List[Document]:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://intake-gateway:8000/v2/documents")
            data = resp.json()
            return [Document(id=d["id"], status=d["status"]) for d in data]

    @strawberry.field
    async def fraud_assessment(self, doc_id: strawberry.ID) -> FraudAssessment:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://fraud-detection:8001/assessment/{doc_id}")
            data = resp.json()
            return FraudAssessment(id=doc_id, probability=data.get("probability", 0.0))

    @strawberry.field
    async def health(self) -> str:
        return "ok"
