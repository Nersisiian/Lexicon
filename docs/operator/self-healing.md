# Self?Healing Operator

## Overview
Automatically detects unhealthy pods and restarts them.

## How it works
1. Every 60 seconds, operator checks all pods in the cluster.
2. If a pod is not `Running` or doesn't respond, it is deleted.
3. The Deployment controller recreates the pod.

## Deployment
```bash
kubectl apply -f services/self-healing-operator/deployment.yaml
