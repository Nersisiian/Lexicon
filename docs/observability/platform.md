# Observability 2.0

## Overview
Unified dashboards with logs (Loki), traces (Tempo), and metrics (Prometheus).

## Components
- **Loki**: collects and indexes logs from all services
- **Tempo**: receives and stores distributed traces
- **Grafana**: unified dashboard with all three data sources

## Deployment
```bash
kubectl apply -f deploy/observability/
Access
Grafana: http://localhost:3000 (default admin/admin)
