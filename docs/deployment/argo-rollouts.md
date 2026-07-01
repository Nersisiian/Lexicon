# Argo Rollouts

## Overview
Argo Rollouts provides advanced deployment strategies (canary, blue?green) for Lexicon services.

## Deploy Argo Rollouts
```bash
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
Apply Rollout
bash
kubectl apply -f deploy/argo-rollouts/intake-gateway-rollout.yaml
Monitor Rollout
bash
kubectl argo rollouts get rollout intake-gateway -n compliance
kubectl argo rollouts promote intake-gateway -n compliance
Canary Strategy
20% of traffic > wait 60s

50% of traffic > wait 60s

100% of traffic
