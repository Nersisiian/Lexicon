from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import asyncio

app = FastAPI(title="Webhook Dispatcher", version="1.0")

# Хранилище подписок (в production – БД)
subscriptions: List["Subscription"] = []

class Subscription(BaseModel):
    id: Optional[str] = None
    event_type: str          # document.completed, document.failed, alert.triggered
    url: str
    secret: Optional[str] = None   # для HMAC подписи в будущем

@app.get("/subscriptions")
async def list_subscriptions():
    return subscriptions

@app.post("/subscriptions")
async def create_subscription(sub: Subscription):
    sub.id = str(len(subscriptions) + 1)
    subscriptions.append(sub)
    return sub

@app.delete("/subscriptions/{sub_id}")
async def delete_subscription(sub_id: str):
    global subscriptions
    subscriptions = [s for s in subscriptions if s.id != sub_id]
    return {"status": "deleted"}

@app.post("/dispatch/{event_type}")
async def dispatch_event(event_type: str, payload: dict):
    matching = [s for s in subscriptions if s.event_type == event_type]
    if not matching:
        raise HTTPException(404, "No subscriptions for this event type")
    
    async def send(s: Subscription):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(s.url, json=payload, timeout=10.0)
            except Exception as e:
                # Логирование ошибки (в production – DLQ)
                pass

    await asyncio.gather(*[send(s) for s in matching])
    return {"dispatched_to": len(matching)}

@app.get("/health")
async def health():
    return {"status": "ok"}
