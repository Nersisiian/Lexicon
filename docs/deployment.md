# Production Deployment

## Prerequisites

- Kubernetes cluster (v1.27+)
- Helm v3.8+
- kubectl configured with appropriate cluster context
- GitHub Container Registry access (image pull secret)

## Deploy

```bash
helm upgrade --install compliance deploy/helm/compliance-platform `
  -f deploy/helm/compliance-platform/values-production.yaml `
  --namespace compliance `
  --create-namespace `
  --set global.imageTag=<your-tag>
````

## Verify

```bash
kubectl get pods -n compliance
kubectl logs -n compliance deployment/intake-gateway
```

## Monitoring

### Grafana

```text
https://grafana.example.com/d/compliance-overview
```

### Metrics

Prometheus targets are registered automatically via ServiceMonitor when Prometheus Operator is installed.

### Alerts

PagerDuty integration is configured through AlertManager.

## Rolling Back

List release revisions:

```bash
helm history compliance -n compliance
```

Rollback to a previous revision:

```bash
helm rollback compliance <REVISION> -n compliance
```

