from fastapi import FastAPI

app = FastAPI(title="Feature Flags", version="1.0")

flags = {
    "new_dashboard": True,
    "experimental_ui": False,
    "shap_explanations": True
}

@app.get("/flags")
async def get_flags():
    return flags

@app.get("/flags/{name}")
async def get_flag(name: str):
    return {name: flags.get(name, False)}

@app.post("/flags/{name}")
async def set_flag(name: str, value: bool):
    flags[name] = value
    return {name: value}

@app.get("/health")
async def health():
    return {"status": "ok"}
