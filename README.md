# Lexicon — AI Document Compliance Platform

**Internal platform for automated processing, validation, and human‑review of regulatory filings.**  
Used by the financial regulator’s supervisory technology division.

---

## Overview

The platform ingests scanned and native‑electronic regulatory documents, extracts text and entities, classifies document types, validates completeness against jurisdictional rules, screens for fraud indicators, applies LLM‑based risk reasoning, and orchestrates human review workflows. Every action is recorded in an immutable audit ledger.

Designed for **multi‑team ownership**, **independent deployability**, and **production observability** from day one.

---

## Architecture at a Glance

| Bounded Context          | Service                          | Interface      | State                      |
|--------------------------|----------------------------------|----------------|----------------------------|
| Document Ingestion       | `intake‑gateway`                 | HTTP/FastAPI   | PostgreSQL (own DB)        |
| OCR Extraction           | `ocr‑pipeline`                   | Kafka consumer | MinIO (raw + processed)    |
| Document Classification  | `document‑classifier`            | Kafka consumer | –                          |
| Regulatory Evaluation    | `compliance‑engine`              | Kafka consumer | –                          |
| Fraud Detection          | `fraud‑detection`                | Kafka consumer | –                          |
| LLM Reasoning            | `reasoning‑service`              | Kafka consumer | –                          |
| Immutable Audit Logging  | `audit‑ledger`                   | HTTP/Kafka     | PostgreSQL (own DB)        |
| Human Review             | `review‑workbench`               | HTTP           | PostgreSQL (own DB)        |
| Notifications            | `notification‑orchestrator`      | Kafka consumer | –                          |
| **Shared SDK**           | `compliance‑sdk`                 | Library        | –                          |

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


# Quick Start (Local Development)

## Prerequisites

* Docker Desktop 4.x+ (with Docker Compose v2)
* Python 3.12 + Poetry (optional, for running tests outside containers)

## 1. Clone and Bootstrap

```bash
git clone https://github.com/Nersisiian/Lexicon.git
cd Lexicon

# Start infrastructure and services
docker compose -f deploy/docker-compose/docker-compose.test.yml up -d
```

## 2. Verify Installation

Upload a sample document:

```bash
curl -X POST http://localhost:8000/v2/documents \
  -F "file=@sample.pdf"
```

### Available Services

| Service          | URL                   |
| ---------------- | --------------------- |
| Intake Gateway   | http://localhost:8000 |
| Audit Ledger     | http://localhost:8001 |
| Review Workbench | http://localhost:8002 |
| MinIO Console    | http://localhost:9001 |

**MinIO Credentials**

```text
Username: minioadmin
Password: minioadmin
```

## 3. Stop Environment

```bash
docker compose -f deploy/docker-compose/docker-compose.test.yml down
```

# API Documentation

Interactive Swagger UI is available at:

```text
http://localhost:8000/docs
```

when the **intake-gateway** service is running.

## Core Endpoints

| Method | Endpoint        | Description                                          |
| ------ | --------------- | ---------------------------------------------------- |
| POST   | `/v2/documents` | Upload a document for processing (PDF/JPEG)          |
| GET    | `/health`       | Service health check                                 |
| GET    | `/metrics`      | Prometheus metrics endpoint                          |
| GET    | `/export/csv`   | Export processed documents as CSV (review-workbench) |

### Rate Limiting

Document ingestion is protected by rate limiting:

```text
10 requests/minute per client (default)
```

Implementation is based on **slowapi** middleware.

---

# CI/CD

GitHub Actions workflows are located in:

```text
.github/workflows/
```

| Workflow              | Trigger               | Purpose                                     |
| --------------------- | --------------------- | ------------------------------------------- |
| `ci-pr.yml`           | Pull Request → `main` | Ruff linting, unit tests, integration tests |
| `ci-main.yml`         | Push → `main`         | Docker image build, Trivy security scan     |
| `release-service.yml` | Manual Dispatch       | Build & publish a single service image      |

All workflows use the repository root as the Docker build context and reference Dockerfiles via:

```text
services/<service-name>/Dockerfile
```

---

# Observability

The platform is fully instrumented with:

* OpenTelemetry (Distributed Tracing)
* Prometheus (Metrics)
* Grafana (Dashboards)
* structlog (Structured JSON Logging)

Correlation is implemented through **W3C TraceContext** propagated via Kafka headers.

## Tracing

```text
Service → OTel Collector → Jaeger
```

Configuration:

```text
deploy/observability/opentelemetry-collector-config.yaml
```

## Metrics

Every HTTP service exposes:

```text
/metrics
```

which is scraped by Prometheus.

## Grafana Dashboards

The dashboard `compliance-overview.json` includes:

* Ingestion rate
* Kafka consumer lag
* Processing duration histograms
* Circuit breaker state
* Upload rate
* Processing latency (p95)
* Auto-approval rate
* Manual review queue size

## Alerting

Prometheus alert rules are defined in:

```text
deploy/observability/prometheus/alerting_rules.yml
```

Example alerts:

* Consumer lag > 5000
* Redis memory pressure
* OCR p99 latency > 45s

---

# A/B Testing

Fraud detection supports production A/B testing.

Metric:

```text
fraud_model_used_total
```

tracks model selection for every prediction.

Dashboard:

```text
deploy/monitoring/grafana-fraud-ab.json
```

visualizes live traffic distribution between models.

---

# Architecture Decision Records (ADRs)

Major architectural decisions are documented in ADRs:

* ADR-001 — Kafka vs RabbitMQ
* ADR-002 — Avoiding Full Event Sourcing
* ADR-003 — OCR Isolation Strategy
* ADR-004 — PostgreSQL vs MongoDB
* ADR-005 — Async Python Stack
* ADR-006 — Hybrid Model Serving
* ADR-007 — Immutable Audit Trail

---

# Incident Postmortems

Operational incidents and lessons learned are documented as postmortems.

Example:

```text
INC-2025-08-14
OCR ingestion backlog and downstream pipeline stall
```

Root cause:

* Vector-heavy PDF batch
* Redis retry amplification
* Cascading consumer slowdown

---

# Platform Conventions

## Service Ownership

Each bounded context owns:

* Its database
* Its API
* Its business logic

Cross-service database joins are prohibited.

## Event Schema Evolution

Kafka messages include a type header.

Consumers:

* Ignore unknown fields
* Remain forward compatible

## Retries & Dead Letter Queues

`ResilientConsumer` provides:

* Retry budgets
* Exponential backoff
* Dead-letter routing

## Idempotency

Consumers use:

```text
document_id
```

as a Redis deduplication key.

TTL:

```text
90 days
```

## Configuration

The platform follows the 12-Factor App methodology.

Configuration sources:

1. `.env`
2. Helm values
3. Environment overrides

## Database Migrations

Each service owns its Alembic migrations.

Policy:

* Staging → automatic
* Production → manual approval

---

# Notifications

The `notification-orchestrator` sends status updates through:

* Slack
* Email

Examples:

* Manual review required
* Approval completed
* Processing failed

Required environment variables:

```text
SLACK_WEBHOOK_URL

SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
SMTP_FROM
SMTP_TO
```

Reference configuration:

```text
deploy/helm/compliance-platform/values-production.yaml
```

Integration tests use mock servers to validate both delivery channels.

---

# Autoscaling (HPA)

The following services support Horizontal Pod Autoscaling:

* OCR Pipeline
* Document Classifier

Default configuration:

```text
Min Replicas: 2
Max Replicas: 10
Target CPU: 70%
```

Configuration:

```text
deploy/helm/compliance-platform/values.yaml
```

# Contributing

We welcome contributions that improve reliability, performance, security, and maintainability.

## Development Workflow

1. Create a feature branch from `main`.
2. Implement your changes.
3. Add or update tests where applicable.
4. Run local validation checks:

```bash
make lint
make test
```

5. Open a Pull Request targeting `main`.

## Pull Request Requirements

Before a PR can be merged:

* All CI checks must pass
* Linting must succeed
* Unit and integration tests must pass
* Security scans must report no blocking issues
* At least one approval from the owning team is required

Ownership rules are defined in:

```text
CODEOWNERS
```

---

# Production Deployment

Deploy the platform using the Helm chart:

```bash
helm upgrade --install compliance deploy/helm/compliance-platform \
  -f deploy/helm/compliance-platform/values-production.yaml \
  --namespace compliance \
  --create-namespace
```

For all configurable parameters see:

```text
deploy/helm/compliance-platform/values.yaml
```

---

# Support & Operations

## Operational Resources

| Resource     | Description                            |
| ------------ | -------------------------------------- |
| Runbook      | `docs/runbooks/incident-response.md`   |
| Dashboard    | Grafana – Compliance Platform Overview |
| Alerting     | PagerDuty via Prometheus AlertManager  |
| Team Channel | `#platform-sre`                        |

## Incident Response

Production incidents should be handled according to the documented runbooks and escalation procedures.

Monitoring, alerting, and observability components are designed to provide complete operational visibility across the platform.

---

# Maintainers

Maintained by the **RegTech Platform Engineering Division**.

© 2026. Internal enterprise platform.


## Quick Install via Helm
```bash
helm repo add lexicon https://nersisiian.github.io/Lexicon
helm install compliance lexicon/compliance-platform -n compliance --create-namespace




