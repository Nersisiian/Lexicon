# KEDA Autoscaling

## Overview
KEDA scales OCR pipeline and document classifier based on Kafka consumer lag.

## Deploy KEDA
```bash
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.14/keda-2.14.0.yaml
Apply ScaledObjects
bash
kubectl apply -f deploy/keda/
How it works
When Kafka topic lag exceeds 100, KEDA increases replicas up to 10.

When lag drops, replicas scale back down.

Works alongside HPA for comprehensive scaling.
