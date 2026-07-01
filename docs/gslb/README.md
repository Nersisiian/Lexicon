# Global Server Load Balancing (GSLB)

## Overview
GSLB automatically routes traffic between Kubernetes clusters in different regions.

## Configuration
- `gateway.yaml` – Gateway for external traffic
- `httproute.yaml` – Weighted routing (80% us-east, 20% eu-west)

## How it works
1. ExternalDNS creates DNS record for `api.lexicon.internal` pointing to the Gateway.
2. Traffic is split 80/20 between clusters.
3. When a cluster becomes unhealthy, weights can be adjusted automatically.

## Deployment
```bash
kubectl apply -f deploy/gslb/
Ensure Gateway API CRDs and ExternalDNS are installed.
