# ADR-005: Async Python as the primary application stack

**Status:** Accepted  
**Date:** 2024-05-12  
**Author:** Backend Team, Platform SRE  
**Superseded by:** None

## Context

All backend services must handle high concurrency I/O (Kafka, HTTP, Postgres, Redis). Early prototypes used Flask with Gunicorn threads, but we experienced thread‑pool exhaustion under moderate load (50 concurrent uploads). We needed a more efficient concurrency model that our team, mostly Python developers, could adopt.

## Decision

We use **async Python** (asyncio) with FastAPI for HTTP services, `aiokafka` for Kafka, `asyncpg` for Postgres, and `httpx` for outbound HTTP. CPU‑bound ML inference is offloaded to separate processes or `run_in_executor` for lightweight models.

## Rationale

- **I/O throughput:** Async scales to thousands of concurrent connections on a small process, avoiding thread‑safety issues and high memory overhead.
- **Ecosystem alignment:** The ML ecosystem (transformers, PyTorch) is native to Python; using Go would split the stack and create friction for ML engineers.
- **Production readiness:** `structlog`, `aiokafka`, `asyncpg`, and `tenacity` provide mature async support. FastAPI offers auto‑generated OpenAPI docs and dependency injection.

## Consequences

- **CPU‑bound work must be isolated:** We delegate model inference to separate worker pods or use `run_in_executor` with a thread pool for lightweight models. If a developer accidentally blocks the event loop, the whole service stalls; we enforce `asyncio_mode=strict` in dev and use `loop.slow_callback_duration` alerting.
- **Debugging complexity:** Stack traces across async boundaries can be confusing. We invest in structured logging with trace IDs and `dict_tracebacks`.
- **Learning curve:** New engineers unfamiliar with `async/await` may introduce subtle bugs (e.g., missing `await`). We’ve built linting rules and pre‑commit hooks to catch common patterns.

## Alternatives Considered

- **Synchronous Python with multiple workers (Gunicorn):** Simpler but limited to ~1000 concurrent connections per worker before thread‑pool saturation; during INC-2023-11-07 the ingress gateway needed 40 workers to handle upload spike, causing OOM.
- **Go:** Better concurrency primitives and static typing, but our team lacks Go experience and the ML libraries are weaker.
- **Rust:** Even larger learning curve; not feasible for the entire team.

## Operational Impact

- **Event loop health:** We export `asyncio` metrics (pending tasks, callback execution time) via a custom Prometheus exporter. We have alerts for callback durations >100ms.
- **Connection pools:** Async drivers require connection pools that are sized appropriately; we default to `min_size=2, max_size=10` per pod.
- **Graceful shutdown:** FastAPI + `aiokafka` require careful shutdown ordering to avoid lost messages; our consumer entry points follow a consistent pattern of stopping Kafka consumer then the producer.

## Tradeoffs

Async Python is not the most performant choice (Go would be faster), but it hits the sweet spot between team capability, library ecosystem, and sufficient performance for our throughput needs.