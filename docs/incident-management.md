# Incident Management

## Alerting
Alerts are routed to PagerDuty via AlertManager. Critical alerts create high?urgency incidents.

## Response
1. Acknowledge the PagerDuty incident.
2. Follow the runbook: `docs/runbooks/incident-response.md`.
3. After resolution, fill out a post?mortem using `docs/postmortems/template.md`.

## Post?mortems
All incidents with severity Critical or Major require a post?mortem within 48 hours.
