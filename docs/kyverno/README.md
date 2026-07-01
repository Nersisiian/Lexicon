# Kyverno Policy Engine

## Overview
Kyverno enforces security, compliance, and best practices on Kubernetes resources.

## Policies
- `require-app-label`: All pods must have `app` label
- `disallow-latest-tag`: Images cannot use `latest` tag

## Deploy Kyverno
```bash
kubectl apply -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml
Apply Policies
bash
kubectl apply -f deploy/kyverno/
Verify
bash
kubectl get clusterpolicies
kubectl get policyreport
