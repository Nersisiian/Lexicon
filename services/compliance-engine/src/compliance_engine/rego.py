import httpx
import json

OPA_URL = "http://localhost:8181/v1/data/compliance/allow"

async def evaluate_opa(input_data: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(OPA_URL, json={"input": input_data})
            result = resp.json()
            return result.get("result", False)
    except Exception:
        # Если OPA недоступен, разрешаем
        return True
