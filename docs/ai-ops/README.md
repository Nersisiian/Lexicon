# AI-Ops Predictive Scaling

## Overview
ML model predicts load 30 minutes ahead and scales services proactively.

## How it works
1. Background task fetches Prometheus metrics every 60s.
2. Model predicts future load.
3. If load exceeds threshold, KEDA/HPA is triggered early.

## Endpoints
- GET /predict – returns predicted load (0.0–1.0)
