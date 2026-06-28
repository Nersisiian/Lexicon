from fastapi import FastAPI
from .predictor import FailurePredictor
import time

app = FastAPI(title="Predictive Maintenance", version="1.0")
predictor = FailurePredictor()

@app.get("/predict/failure-probability")
async def predict_failure():
    prob = predictor.predict()
    return {"failure_probability": prob, "timestamp": time.time()}

@app.get("/health")
async def health():
    return {"status": "ok"}
