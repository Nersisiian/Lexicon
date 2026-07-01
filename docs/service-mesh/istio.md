# Service Mesh with Istio

## Overview
Istio provides advanced traffic management, A/B testing, and observability for Lexicon.

## Configuration
- `VirtualService` routes 10% of traffic to experimental version
- `DestinationRule` defines stable and experimental subsets
- Users can opt into experimental features via `x-experimental: true` header

## Deployment
```bash
kubectl apply -f deploy/istio/
A/B Testing
Deploy both stable and experimental versions.

Monitor metrics in Grafana/Kiali.

Adjust weights via kubectl edit virtualservice intake-gateway-ab.
