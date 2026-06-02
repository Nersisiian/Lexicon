# AI Document Compliance Platform

**Internal platform for automated processing, validation, and human‑review of regulatory filings.**  
Used by the financial regulator’s supervisory technology division.

---

## Overview

The platform ingests scanned and native‑electronic regulatory documents, extracts text and entities, classifies document types, validates completeness against jurisdictional rules, screens for fraud indicators, applies LLM‑based risk reasoning, and orchestrates human review workflows. Every action is recorded in an immutable audit ledger.

The system is designed for **multi‑team ownership**, **independent deployability**, and **production observability** from day one.

---

## Architecture at a Glance

| Bounded Context          | Service                          | Interface  | State                |
|--------------------------|----------------------------------|------------|----------------------|
| Document Ingestion       | `intake‑gateway`                 | HTTP/FastAPI | PostgreSQL (own DB) |
| OCR Extraction           | `ocr‑pipeline`                   | Kafka consumer | MinIO (raw + processed) |
| Document Classification  | `document‑classifier`            | Kafka consumer | – |
| Regulatory Evaluation    | `compliance‑engine`              | Kafka consumer | – |
| Fraud Detection          | `fraud‑detection`                | Kafka consumer | – |
| LLM Reasoning            | `reasoning‑service`              | Kafka consumer | – |
| Immutable Audit Logging  | `audit‑ledger`                   | HTTP/Kafka | PostgreSQL (own DB) |
| Human Review             | `review‑workbench`               | HTTP        | PostgreSQL (own DB) |
| Notifications            | `notification‑orchestrator`      | Kafka consumer | – |
| **Shared SDK**           | `compliance‑sdk`                 | Library     | – |

All inter‑service communication goes through **Apache Kafka** (see [ADR‑001](docs/adr/001-kafka-over-rabbitmq.md)).  
The platform uses **async Python** (FastAPI, aiokafka, asyncpg) and a hybrid model‑serving strategy (embedded + dedicated inference).

---

## Repository Structure
.
├── .github/workflows/ # CI/CD (PR checks, main build, security scans)
├── deploy/
│ ├── docker‑compose/ # Local development stack
│ ├── helm/ # Kubernetes deployment charts
│ ├── kubernetes/ # Kustomize overlays
│ └── observability/ # OTel Collector, Prometheus, Grafana configs
├── docs/adr/ # Architecture Decision Records
├── packages/
│ ├── compliance‑sdk/ # Shared observability, Kafka, domain primitives
│ └── compliance‑testkit/ # Test harness for integration tests
├── scripts/ # Bootstrap, migrations, seed data
├── services/ # 9 independently deployable services
└── Makefile # Top‑level build, test, lint, run commands


---

## Quick Start (Local Development)

### Prerequisites
- Docker Desktop 4.x+ (with Docker Compose v2)
- Python 3.12 + Poetry (for running tests outside containers)

### 1. Clone and Bootstrap

```bash
git clone https://github.com/Nersisiian/Lexicon.git
cd Lexicon
make run        # starts infrastructure + all services

2. Verify
bash
curl -X POST http://localhost:8000/v2/documents \
  -F "file=@sample.pdf"
Open:

Intake Gateway → http://localhost:8000
  
Audit Ledger → http://localhost:8001

Review Workbench → http://localhost:8002

MinIO Console → http://localhost:9001 (minioadmin / minioadmin

3. Stop
bash
docker compose -f deploy/docker-compose/docker-compose.infra.yml -f deploy/docker-compose/docker-compose.services.yml down
CI/CD
GitHub Actions workflows are located in .github/workflows/.

Workflow	Trigger	Purpose
ci-pr.yml	Pull Request → main	Lint (ruff), unit + integration tests
ci-main.yml	Push to main	Build all Docker images, run security scan (Trivy)
release-service.yml	Manual dispatch	Build and push a single service image to registry
All workflows use the repository root as Docker build context and reference Dockerfiles via -f services/<name>/Dockerfile.

Observability
Every service is instrumented with OpenTelemetry (traces), Prometheus (metrics), and structlog (JSON logs). Correlation is done via W3C TraceContext propagated through Kafka headers.

Traces: exported to the OTel Collector → Jaeger (see deploy/observability/opentelemetry-collector-config.yaml)

Metrics: exposed on /metrics on each HTTP service, scraped by Prometheus

Dashboards: Grafana dashboard compliance-overview.json contains key panels: ingestion rate, consumer lag, processing duration histograms, circuit breaker state

Alerts: defined in deploy/observability/prometheus/alerting_rules.yml (consumer lag > 5000, Redis memory pressure, OCR p99 latency > 45s)

Key Design Decisions (ADRs)
All significant architectural choices are documented as Architecture Decision Records:

ADR‑001 – Why Kafka instead of RabbitMQ

ADR‑002 – Why we avoided full event sourcing

ADR‑003 – Why OCR is isolated from compliance evaluation

ADR‑004 – Why PostgreSQL was chosen over MongoDB

ADR‑005 – Reasoning behind the async Python stack

ADR‑006 – Hybrid model serving strategy

ADR‑007 – Immutable audit trail requirements and implementation

Incident Postmortems
Real‑world operational learnings are captured in postmortems.
Example: INC-2025-08-14 – OCR ingestion backlog and downstream pipeline stall (cascading failure due to vector‑heavy PDF batch, Redis retry amplification).

Platform Conventions
Bounded contexts: each service owns its data and public API; cross‑service joins are prohibited.

Event schema evolution: Kafka messages carry a type header; consumers ignore unknown fields (forward‑compatible).

Retries & DLQ: The ResilientConsumer in compliance‑sdk implements per‑message retry budget and dead‑letter routing after exhaustion.

Idempotency: Consumers use document_id as a dedup key in Redis (TTL 90 days).

Configuration: 12‑factor app; environment variables defined in .env files, overridden by Helm values per environment.

Migrations: Each stateful service manages its own Alembic migrations; applied automatically in staging, manually approved in production.

Contributing
Create a feature branch from main.

Implement changes, add/update tests.

Run make lint and make test locally.

Open a PR – CI will run linting, tests, and security scan.

At least one approving review from the owning team is required before merge.

Team ownership is defined in CODEOWNERS.

Production Deployment
Use the Helm chart:

bash
helm upgrade --install compliance deploy/helm/compliance-platform \
  -f deploy/helm/compliance-platform/values-production.yaml \
  --namespace compliance --create-namespace
Refer to deploy/helm/compliance-platform/values.yaml for all configurable parameters.

Support & Operations
Runbook: docs/runbooks/incident-response.md

Dashboard: Grafana “Compliance Platform Overview”

Alerting: PagerDuty integration via Prometheus AlertManager

Platform SRE Slack: #platform-sre

Maintained by the RegTech Platform Engineering division. Internal use only.

