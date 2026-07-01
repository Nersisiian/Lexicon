# Argo Rollouts – Canary Deployments

## Overview
Argo Rollouts enables safe, gradual rollouts of new service versions.

## Deploy Argo Rollouts
```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
Apply Rollout
bash
kubectl apply -f deploy/argo-rollouts/intake-gateway-rollout.yaml
Promote a new version
bash
kubectl argo rollouts set image intake-gateway intake-gateway=ghcr.io/nersisiian/lexicon/intake-gateway:new-tag
kubectl argo rollouts promote intake-gateway
Monitor
bash
kubectl argo rollouts get rollout intake-gateway --watch
