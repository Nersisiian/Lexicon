# API Gateway (Kong)

## Overview
Kong serves as the single entry point for all Lexicon services.

## Routes
- `/api/v2/*` > intake-gateway
- `/analytics/*` > analytics-engine
- `/review/*` > review-workbench
- `/graphql` > graphql-gateway
- `/` > frontend

## Configuration
See `deploy/kong/kong.yml` for declarative configuration.

## Access
After deployment, all services are accessible via `http://localhost:8000`:
```bash
curl http://localhost:8000/api/v2/health
curl http://localhost:8000/analytics/documents-per-day
