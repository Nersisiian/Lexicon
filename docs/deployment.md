# Kubernetes Deployment

## Prerequisites
- Kubernetes cluster (minikube, kind, or cloud)
- kubectl configured
- Helm 3+

## Deploy to cluster
```bash
# Add secrets (example)
kubectl create secret generic compliance-secrets \
  --from-literal=postgres-password=changeme \
  --from-literal=minio-access-key=minioadmin \
  --from-literal=minio-secret-key=minioadmin

# Install chart
helm upgrade --install compliance deploy/helm/compliance-platform \
  -f deploy/helm/compliance-platform/values-production.yaml \
  --namespace compliance --create-namespace
# Port forward intake-gateway
kubectl port-forward svc/intake-gateway 8000:8000 -n compliance

# Or create Ingress (see templates/ingress.yaml)

## Automatic Deployment (CI/CD)
1. Add your Kubernetes config as a GitHub Secret named `KUBE_CONFIG`:
   ```bash
   cat ~/.kube/config | base64 | gh secret set KUBE_CONFIG
Push to main – the workflow will automatically deploy the latest images.
