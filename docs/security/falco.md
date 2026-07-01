# Falco Threat Detection

## Overview
Falco monitors Linux kernel system calls for suspicious activity in containers.

## Rules
- **Suspicious Shell Spawn** – detects when a shell (bash, sh) is started in a container
- **Unexpected Network Connection** – alerts on outbound connections to non-standard ports
- **File Access in Sensitive Directory** – monitors access to /etc and /var

## Deployment
```bash
kubectl apply -f deploy/falco/
Requires Falco installed in the cluster.

Integration
Alerts are forwarded to PagerDuty via AlertManager webhook.
