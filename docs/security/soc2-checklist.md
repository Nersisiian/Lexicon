# SOC2 Compliance Checklist

| Trust Service Criteria | Status | Notes |
|------------------------|--------|-------|
| Security               | ?     | CodeQL, Dependabot, rate limiting, OAuth2 |
| Availability           | ?     | HPA, health checks, ArgoCD GitOps |
| Confidentiality        | ?     | Data encryption in transit (TLS) and at rest (RDS encryption) |
| Processing Integrity   | ?     | Idempotent consumers, DLQ, audit ledger |
| Privacy                | ?     | Data minimization, access controls |
