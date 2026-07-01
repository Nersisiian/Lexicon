# Multi-Cluster Deployment

## Overview
Lexicon supports deployment across multiple geographic regions for high availability and disaster recovery.

## Configuration
Regional values are stored in `deploy/multi-cluster/`:
- `values-us-east.yaml` — US East configuration
- `values-eu-west.yaml` — EU West configuration

## Deploying
1. Add `KUBE_CONFIG_US_EAST` and `KUBE_CONFIG_EU_WEST` secrets to GitHub.
2. Push to `main` — the `Multi-Cluster Deploy` workflow will deploy to both regions sequentially.

## Verification
```bash
kubectl --context us-east get pods -n compliance
kubectl --context eu-west get pods -n compliance
