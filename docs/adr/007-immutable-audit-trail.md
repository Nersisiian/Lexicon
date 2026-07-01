# ADR-007: Immutable audit trails as a platform requirement

**Status:** Accepted  
**Date:** 2024-07-01  
**Author:** Security Architecture, Compliance Domain  
**Superseded by:** None

## Context

As a platform used by a financial regulator, every action on a document (submission, processing stage, human review decision) must be recorded in a tamper‑proof manner that can be presented to external auditors years later. This is required by multiple regulations (eIDAS, FINRA, local central bank rules). Simple database logging with update/delete capabilities is not sufficient.

## Decision

We built a dedicated **audit ledger** service that implements an append‑only immutable log. All significant business events are written to this ledger synchronously via its REST API. The ledger’s underlying PostgreSQL table is configured with `INSERT`‑only permissions for the application user, and no `UPDATE` or `DELETE` operations are allowed at the database level. Each audit record carries a trace ID and a cryptographic hash of its payload. Digital signatures are planned for a future phase.

## Rationale

- **Regulatory compliance:** Auditors require a reliable chain of custody. Immutable logs prove that no tampering occurred post‑factum.
- **Security:** Even if an attacker compromises a service or obtains database credentials, previously written audit entries cannot be altered, limiting the blast radius.
- **Simpler incident investigation:** During an incident, the audit log provides a single authoritative timeline. There is no need to cross‑check multiple service logs that may have different retention.

## Consequences

- **Synchronous write latency:** The audit ledger is called synchronously before a service responds to the caller or commits its own state. This adds 2–5ms to every auditable action. We accept this because compliance requires it and the load is moderate.
- **Critical single point of failure:** If the audit ledger is unavailable, services cannot proceed. The ledger is deployed as a highly available deployment (3 replicas, separate database) and uses an outbox pattern within each service to guarantee at‑least‑once delivery. Services buffer audit events to a local outbox table in their own DB and a background worker forwards them; if the ledger is down, events queue up and processing halts gracefully after a configurable buffer fills.
- **Storage growth:** The audit table grows quickly (~1M events/month in production). We partition by month and archive partitions older than 7 years to WORM‑compliant object storage. Older events remain queryable via a separate archival service.

## Alternatives Considered

- **Kafka as audit store:** Kafka can retain messages indefinitely, but Kafka messages are not individually hashed or signed, and retention policies could be misconfigured. Also, auditors expect a database they can query with SQL.
- **Blockchain:** Overkill; a centralised append‑only database with cryptographic hashes is simpler and accepted by our regulators.
- **App‑level logging only:** Rejected because logs can be altered or deleted by anyone with server access.

## Operational Impact

- **Monitoring:** Audit‑write latency and failure rate are Prometheus metrics. Alert threshold: p99 latency > 20ms.
- **Backups:** WAL‑G backups of the audit database are stored on a separate, encrypted MinIO bucket with legal hold enabled.
- **Integrity checks:** A daily cron job verifies that no rows have been modified by checking a running hash chain. Anomaly triggers an immediate security incident.
- **Outbox processing:** Each service’s outbox processor publishes to Kafka as a fallback if the ledger HTTP call fails; a separate `audit‑forwarder` consumes that topic and writes to the ledger, ensuring eventual consistency. This was added after INC-2024-09-14 where a network partition caused audit loss.