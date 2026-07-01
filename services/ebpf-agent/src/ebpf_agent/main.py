from fastapi import FastAPI
import subprocess, json

app = FastAPI(title="eBPF Agent", version="1.0")

@app.get("/metrics/tcp")
async def tcp_connections():
    # Заглушка: в реальности здесь будет вызов eBPF программы
    return {"active_connections": 42, "bytes_sent": 123456}

@app.get("/metrics/http")
async def http_latency():
    return {"p99_latency_ms": 12.5, "request_rate": 100}

@app.get("/health")
async def health():
    return {"status": "ok"}
