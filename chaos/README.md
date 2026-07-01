# Chaos Engineering with LitmusChaos

## Experiments
- **pod-delete**: Random pod deletion
- **network-loss**: Complete network loss on intake-gateway
- **pod-network-loss**: 50% packet loss on OCR pipeline
- **node-drain**: Node drain simulating AZ failure

## Run Experiment
```bash
kubectl apply -f chaos/experiments/<experiment>.yaml
Observe
Grafana: error rate, latency, pod restarts

HPA/KEDA should scale up replacement pods

Istio should reroute traffic
