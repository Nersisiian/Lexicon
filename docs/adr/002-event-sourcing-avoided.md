# ADR-002: Avoid full event sourcing; Kafka as transport only

**Status:** Accepted  
**Date:** 2024-03-10  
**Author:** Compliance Domain Team, Platform Architecture  
**Superseded by:** None

## Context

During the platform’s initial design, the architecture group explored using Kafka not only as a transport layer but also as the primary source of truth for domain state (full event sourcing). In that model, the current state of a document would be derived by replaying all events from the log, and projections would serve query needs.

## Decision

We **reject** event sourcing as the primary persistence mechanism. Each service persists its own current state in a dedicated PostgreSQL database, using Kafka exclusively as an asynchronous transport. Events on Kafka represent *notifications* of state changes; the authoritative record lives in the relational database.

## Rationale

- **Regulatory query requirements:** Compliance officers need ad‑hoc relational queries (e.g., “show all AML hits for filings from jurisdiction X in the last quarter”). Event‑sourced projections would require significant development and would limit the ability to run arbitrary SQL joins.
- **Operational simplicity:** Multiple teams (OCR, compliance, review) are already proficient in SQL and PostgreSQL. Introducing event sourcing would mandate a steep learning curve and new debugging techniques for production incidents.
- **Audit trail separation:** Regulatory auditing demands an immutable, tamper‑proof log. We built a dedicated audit ledger service (see ADR-007) backed by PostgreSQL with append‑only tables, which satisfies this requirement without coupling it to operational eventing.
- **Reprocessing flexibility:** We can still replay events from Kafka for reprocessing (e.g., after model retraining) without treating the log as the system of record. This keeps Kafka as a “dumb pipe” that we can replace if needed.

## Consequences

- Each service owns its schema and can evolve it with database migrations without affecting downstream consumers.
- The event bus remains unopinionated; we can add new consumers without worrying about projection consistency.
- Duplicate detection and idempotency are still required because Kafka delivers at‑least‑once. Consumers use `document_id` as a dedup key in Redis.
- We forego the ability to rebuild arbitrary historical states purely from the log. If we later need point‑in‑time state reconstruction, we would rely on database backups and the audit ledger.

## Alternatives Considered

- **Full event sourcing with CQRS:** Rejected due to complexity, lack of team experience, and the regulatory need for relational ad‑hoc queries.
- **Hybrid approach (Kafka as log + PostgreSQL as snapshot):** Evaluated but added development overhead without clear benefit. Snapshot management is non‑trivial.
- **No event bus at all (synchronous HTTP):** Would couple services and make it impossible to replay events, so it was discarded early.

## Operational Impact

- **Database load:** Each service now has its own database, increasing total DB instances. We mitigated cost by using a shared PostgreSQL cluster with separate databases per service. In production we use Patroni for HA.
- **Event‑to‑state consistency:** During incident response, we often correlate Kafka offset lag with database state; dashboards show both side‑by‑side. A known risk is that a service may crash after consuming a message but before persisting state; we mitigate by making consumers idempotent and re‑driving from Kafka.

## Tradeoffs

We traded the ability to do full‑history reprojection for faster development velocity and simpler operational debugging. The dedicated audit ledger gives us compliance without event sourcing’s complexity.