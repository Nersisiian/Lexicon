from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OpenFeature Service", version="1.0")

flags = {
    "new_dashboard": {"enabled": True, "percentage": 50},
    "experimental_ui": {"enabled": False, "percentage": 0},
    "shap_explanations": {"enabled": True, "percentage": 100}
}

class EvaluationRequest(BaseModel):
    flag_key: str
    targeting_key: str = ""

@app.post("/evaluate")
async def evaluate(req: EvaluationRequest):
    flag = flags.get(req.flag_key, {"enabled": False, "percentage": 0})
    return {
        "enabled": flag["enabled"],
        "percentage": flag["percentage"],
        "reason": "static"
    }

@app.get("/flags")
async def get_flags():
    return flags

@app.post("/flags/{name}")
async def set_flag(name: str, enabled: bool, percentage: int = 0):
    flags[name] = {"enabled": enabled, "percentage": percentage}
    return {name: flags[name]}

@app.get("/health")
async def health():
    return {"status": "ok"}
