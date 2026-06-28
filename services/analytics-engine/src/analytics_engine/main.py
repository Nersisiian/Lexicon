from fastapi import FastAPI, Query
import duckdb
import pandas as pd
from .config import DATABASE_URL

app = FastAPI(title="Analytics Engine", version="1.0")

@app.on_event("startup")
async def startup():
    # Подключаемся к PostgreSQL через DuckDB
    global conn
    conn = duckdb.connect()
    conn.execute(f"INSTALL postgres; LOAD postgres;")
    conn.execute(f"ATTACH 'dbname=test user=test password=test host=postgres port=5432' AS pg_db (TYPE postgres)")

@app.get("/analytics/documents-per-day")
async def documents_per_day():
    df = conn.execute("""
        SELECT date_trunc('day', created_at) as day, COUNT(*) as count
        FROM pg_db.documents
        GROUP BY day
        ORDER BY day
    """).fetchdf()
    return df.to_dict(orient="records")

@app.get("/analytics/status-breakdown")
async def status_breakdown():
    df = conn.execute("""
        SELECT status, COUNT(*) as count
        FROM pg_db.documents
        GROUP BY status
    """).fetchdf()
    return df.to_dict(orient="records")

@app.get("/analytics/processing-time-p95")
async def processing_time_p95():
    df = conn.execute("""
        SELECT
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (updated_at - created_at))) as p95_seconds
        FROM pg_db.documents
        WHERE status = 'completed'
    """).fetchdf()
    return {"p95_seconds": df.iloc[0, 0] if not df.empty else 0}

@app.get("/health")
async def health():
    return {"status": "ok"}
