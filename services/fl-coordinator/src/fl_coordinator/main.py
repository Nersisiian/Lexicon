from fastapi import FastAPI

app = FastAPI(title="FL Coordinator", version="1.0")

@app.post("/fl/join")
async def join_federation(client_id: str):
    return {"status": "joined", "client_id": client_id}

@app.get("/fl/model")
async def get_global_model():
    # В production здесь будет раздача актуальной глобальной модели
    return {"model_version": "v1.0", "url": "http://models.internal/global_model.pkl"}

@app.post("/fl/update")
async def send_update(client_id: str, model_update: dict):
    # Здесь будет агрегация обновлений от клиентов
    return {"status": "accepted", "client_id": client_id}

@app.get("/health")
async def health():
    return {"status": "ok"}
