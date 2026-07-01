# Alerting Configuration

## PagerDuty Integration
1. Create a PagerDuty service, get Integration Key.
2. Replace keys in `deploy/observability/alertmanager/alertmanager.yml`.
3. Deploy AlertManager: `kubectl apply -f deploy/observability/alertmanager/alertmanager.yml`

## Prometheus Alerts
HighConsumerLag, OCRProcessingSlow, IntakeGatewayDown
