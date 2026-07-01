from fastapi import FastAPI
import httpx, time

app = FastAPI(title="Cost Monitor", version="1.0")
BUDGET_LIMIT = 1000.0  # USD

@app.get("/costs/current")
async def current_costs():
    # Заглушка: реальные данные будут из облачного API
    costs = {
        "compute": 450.0,
        "storage": 120.0,
        "network": 80.0,
        "database": 200.0,
        "total": 850.0,
        "timestamp": time.time(),
        "budget_remaining": BUDGET_LIMIT - 850.0
    }
    return costs

@app.get("/costs/forecast")
async def cost_forecast():
    return {
        "projected_total": 920.0,
        "budget_exceeded_at": None,
        "recommendation": "Current usage is within budget"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
