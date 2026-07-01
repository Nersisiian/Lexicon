from fastapi import FastAPI, UploadFile, File
import httpx, os

app = FastAPI(title="Edge Agent", version="1.0")
CENTRAL_GATEWAY = os.getenv("CENTRAL_GATEWAY", "http://intake-gateway:8000")

@app.post("/process-local")
async def process_local(file: UploadFile = File(...)):
    # Локальная OCR (заглушка)
    content = await file.read()
    result = {"filename": file.filename, "status": "processed", "text_length": len(content)}
    # Отправка результата в центральный шлюз
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{CENTRAL_GATEWAY}/v2/documents", json=result)
    except Exception as e:
        result["sync_error"] = str(e)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
