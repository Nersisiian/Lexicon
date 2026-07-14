# Production Chaos Platform

## Overview
Safe chaos testing in production with automatic rollback.

## Features
- **Blast Radius Control**: Limits impact to 1 pod or container.
- **Auto?Abort**: Automatically stops experiment if errorRate > 5% or latencyP99 > 2s.
- **Liveness Check**: Verifies service health before and after chaos.

## Deployment
```bash
kubectl apply -f chaos/production/
Run Experiment
bash
kubectl annotate chaosengine production-pod-delete litmuschaos.io/chaos="true" -n compliance
Monitoring
Watch Grafana dashboard during experiment for impact.
