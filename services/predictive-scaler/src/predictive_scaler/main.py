from fastapi import FastAPI
from .predictor import predict_load
import asyncio, time

app = FastAPI(title="Predictive Scaler", version="1.0")

@app.get("/predict")
async def get_prediction():
    forecast = predict_load()
    return forecast

@app.get("/health")
async def health():
    return {"status": "ok"}

async def background_scaling():
    while True:
        forecast = predict_load()
        # Здесь будет вызов K8s API для масштабирования
        print(f"Predicted load: {forecast}")
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup():
    asyncio.create_task(background_scaling())
