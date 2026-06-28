from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="External Gateway", version="1.0")

# Заглушка API для проверки контрагента по санкционным спискам
@app.get("/sanctions/check")
async def sanctions_check(name: str):
    # В реальном проекте здесь запрос к внешнему API (например, OpenSanctions)
    # Пока возвращаем статический ответ
    if "sanctioned" in name.lower():
        return {"name": name, "sanctioned": True, "details": "Appears on sanctions list"}
    return {"name": name, "sanctioned": False}

# Заглушка для загрузки отчёта из внешней системы
@app.post("/reports/fetch")
async def fetch_report(report_type: str, identifier: str):
    # В production здесь будет вызов внешнего API
    # Возвращаем имитацию успешной загрузки
    return {
        "report_type": report_type,
        "identifier": identifier,
        "status": "fetched",
        "url": f"https://reports.internal/{identifier}.pdf"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
