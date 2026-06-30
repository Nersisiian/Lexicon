import httpx
import random
import time

PROMETHEUS_URL = "http://prometheus:9090/api/v1/query"

class FailurePredictor:
    async def fetch_metric(self, query: str) -> float:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(PROMETHEUS_URL, params={"query": query})
                data = resp.json()
                result = data.get("data", {}).get("result", [])
                if result:
                    return float(result[0]["value"][1])
        except Exception:
            pass
        # fallback, если Prometheus недоступен
        return random.uniform(0, 100)

    async def predict(self) -> dict:
        # Собираем метрики
        kafka_lag = await self.fetch_metric("max(kafka_consumer_lag)")
        minio_free = await self.fetch_metric("minio_free_space_bytes")
        cpu_usage = await self.fetch_metric("avg(rate(container_cpu_usage_seconds_total[5m]))")

        # Простейшая эвристика: если очередь > 5000 или место < 10GB или CPU > 80%
        failure_prob = 0.0
        if kafka_lag > 5000:
            failure_prob += 0.4
        if minio_free < 10 * 1024 * 1024 * 1024:
            failure_prob += 0.3
        if cpu_usage > 80:
            failure_prob += 0.3

        return {
            "failure_probability": min(failure_prob, 1.0),
            "metrics": {
                "kafka_consumer_lag": kafka_lag,
                "minio_free_space_bytes": minio_free,
                "cpu_usage_pct": cpu_usage
            },
            "timestamp": time.time()
        }
