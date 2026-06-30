from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="External Gateway", version="2.0")

OPEN_SANCTIONS_URL = "https://api.opensanctions.org/search/sanctions"

@app.get("/sanctions/check")
async def sanctions_check(name: str):
    params = {"q": name, "limit": 1}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(OPEN_SANCTIONS_URL, params=params, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    return {"name": name, "sanctioned": True, "details": results[0].get("caption", "Sanctioned entity")}
                return {"name": name, "sanctioned": False}
            else:
                raise HTTPException(502, "OpenSanctions API error")
    except Exception as e:
        raise HTTPException(502, f"Sanctions check failed: {str(e)}")

@app.post("/reports/fetch")
async def fetch_report(report_type: str, identifier: str):
    return {
        "report_type": report_type,
        "identifier": identifier,
        "status": "fetched",
        "url": f"https://reports.internal/{identifier}.pdf"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
