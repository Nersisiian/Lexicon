# ADR-004: PostgreSQL as the primary relational database

**Status:** Accepted  
**Date:** 2024-04-20  
**Author:** Data Engineering, Platform SRE  
**Superseded by:** None

## Context

The platform needs to persist structured metadata: document records, extracted entities, audit logs, human review tasks. We needed a database that supports strong consistency, ACID transactions, rich querying (joins, aggregations), and is familiar to our operations team.

## Decision

All stateful services will use **PostgreSQL 16** as their primary datastore. Each service owns its own database within a shared cluster. We use `asyncpg` directly (not SQLAlchemy ORM) for performance and simplicity, with Alembic for schema migrations.

## Rationale

- **Data integrity:** Regulatory data requires referential integrity. PostgreSQL’s foreign keys and check constraints prevent corruption that could happen in document stores.
- **Ad‑hoc reporting:** Compliance officers and auditors run SQL queries via a read‑replica; this is natural for them and avoids building custom reporting APIs.
- **Operational maturity:** Our DBA team has deep PostgreSQL expertise (replication, backup, monitoring). Adding MongoDB would require new operational knowledge and tooling.
- **JSON support:** For semi‑structured data (e.g., extraction results), we use `jsonb` with indexing, giving flexibility while keeping the relational core.

## Consequences

- **Cross‑service joins are prohibited:** Each service owns its data; if the review workbench needs data from the audit ledger, it calls the audit API. This maintains bounded contexts but adds network latency.
- **Schema migrations must be coordinated with deployments.** We use Alembic with a strict rollback plan; in staging, migrations run automatically; in production, a manual approval step is required.
- **No horizontal write scaling:** Writes are single‑master; we accept this because throughput is moderate (peak ~200 writes/sec). If needed, we can shard by regulator ID later.

## Alternatives Considered

- **MongoDB:** Rejected because the domain is highly relational. The initial prototype used MongoDB for document metadata, but compliance reporting needed joins that were inefficient with `$lookup`. Migration from Mongo to Postgres happened in Q3 2023.
- **CockroachDB / distributed SQL:** Considered for multi‑region active‑active, but we operate in a single datacenter and don’t need it yet; the operational complexity is higher.

## Operational Impact

- **Connection pooling:** We use PgBouncer in transaction mode in front of Postgres to handle high connection counts from scaled services.
- **Backups:** Continuous WAL archiving to MinIO, with point‑in‑time recovery tested monthly.
- **Replicas:** A read replica serves the audit ledger’s query endpoint and Grafana dashboards, keeping load off the primary.
- **Monitoring:** `pg_stat_activity` and query latency are exported via `postgres_exporter` to Prometheus. We have alerts for replication lag >5s.