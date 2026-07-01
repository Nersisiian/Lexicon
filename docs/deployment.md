# Production Deployment

## Prerequisites
- Kubernetes cluster (v1.27+)
- Helm v3.8+
- kubectl configured with the target cluster
- GitHub Container Registry access (image pull secret if private)
- Secrets configured in GitHub Actions: `KUBE_CONFIG`, `SLACK_WEBHOOK_URL`, `SMTP_*` (if using notifications)

# 1. Deploy the stack
helm upgrade --install compliance deploy/helm/compliance-platform \
  -f deploy/helm/compliance-platform/values-production.yaml \
  --namespace compliance --create-namespace \
  --set global.imageTag=<your-tag>

# 2. Verify
kubectl get pods -n compliance
kubectl logs -n compliance deployment/intake-gateway

# 3. Monitoring
# Grafana:
http://<grafana-host>/d/compliance-overview

# Alerts:
# PagerDuty (see deploy/observability/prometheus/README.md)

# 4. Rollback
helm rollback compliance -n compliance
