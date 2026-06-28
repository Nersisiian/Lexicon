# Zero?Trust Architecture with Istio

## Overview
All inter?service communication in Lexicon is encrypted and authenticated using Istio Service Mesh.

## Components
- **PeerAuthentication**: strict mTLS for the entire `compliance` namespace.
- **AuthorizationPolicy**: granular access control between services.
- **DestinationRule**: enforces ISTIO_MUTUAL mode for all traffic.

## Deployment
```bash
kubectl apply -f deploy/istio/
Verification
bash
istioctl authn tls-check | grep compliance
