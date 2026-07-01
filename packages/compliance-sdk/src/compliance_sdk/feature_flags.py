import httpx

FEATURE_FLAGS_URL = "http://feature-flags:8013"

async def is_enabled(flag_name: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{FEATURE_FLAGS_URL}/flags/{flag_name}")
            data = resp.json()
            return data.get(flag_name, False)
    except:
        return False
