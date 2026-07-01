from fastapi import FastAPI
from .predictor import FailurePredictor
import time

app = FastAPI(title="Predictive Maintenance", version="2.0")
predictor = FailurePredictor()

@app.get("/predict/failure-probability")
async def predict_failure():
    result = await predictor.predict()
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
