import httpx

COORDINATOR_URL = "http://fl-coordinator:8006"

async def fetch_global_model():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{COORDINATOR_URL}/fl/model")
        return resp.json()

async def send_model_update(client_id: str, update: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{COORDINATOR_URL}/fl/update", json={"client_id": client_id, "model_update": update})
        return resp.json()
