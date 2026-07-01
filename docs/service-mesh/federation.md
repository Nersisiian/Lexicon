# Service Mesh Federation

## Overview
Istio meshes from different Kubernetes clusters are federated, allowing services to communicate across clusters with mTLS.

## Configuration
- `service-entry-eu-west.yaml` – Makes services from eu-west cluster discoverable in us-east.
- `destination-rule-cross-cluster.yaml` – Enforces mutual TLS for cross-cluster traffic.

## How it works
1. Istio control planes exchange root certificates.
2. ServiceEntry makes remote services locally addressable.
3. DestinationRule enables mTLS for cross-cluster calls.

## Deployment
```bash
kubectl apply -f deploy/istio-federation/
Requires Istio multi-cluster setup with shared trust domain.
