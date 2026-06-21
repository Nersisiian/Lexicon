# Chaos Engineering with LitmusChaos

## 1. Install LitmusChaos
```bash
kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v3.0.0.yaml
2. Run Experiment
bash
kubectl apply -f chaos/experiments/pod-delete.yaml
3. Observe
Grafana dashboard: check error rate, latency, pod restarts.

Rate limiting should protect the service.

HPA should scale up if needed.

4. Cleanup
bash
kubectl delete chaosengine lexicon-chaos -n compliance
