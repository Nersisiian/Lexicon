# ADR-003: Isolate OCR processing from compliance evaluation

**Status:** Accepted  
**Date:** 2024-04-05  
**Author:** OCR Team, Compliance Team  
**Superseded by:** None

## Context

The platform must extract text from scanned documents (OCR) and then evaluate that text against regulatory rules. These two phases have fundamentally different resource profiles: OCR is CPU/GPU‑intensive, bursty, and sensitive to document size and quality; compliance rule evaluation is I/O‑bound (external API calls) and quick per document. If both ran within the same service, a spike in complex PDFs would starve compliance checks of resources.

## Decision

The **OCR pipeline** is deployed as an independent service, communicating with other services exclusively through Kafka topics. It consumes `document.ingested` events, performs optical character recognition, and publishes `document.ocr.completed` events. The **compliance engine** is a separate service that listens to `document.classified` (classification) and `document.ocr.completed` and never processes raw binary content.

## Rationale

- **Resource isolation:** OCR pods can be scheduled on nodes with GPUs (or large CPU) and scaled independently. Compliance pods run on standard compute nodes.
- **Failure boundaries:** Transient OCR failures (e.g., malformed PDF, timeout) are contained; the compliance engine is not affected and can proceed with documents that were already OCR’d successfully.
- **Independent evolution:** The OCR team can swap engines (currently PaddleOCR with a legacy Tesseract fallback for CAD diagrams) without touching the compliance codebase.
- **Security:** Raw documents never leave the object store (MinIO); the OCR service retrieves them using pre‑signed URLs. The compliance engine only sees extracted text, reducing sensitive data exposure.

## Consequences

- **Added latency:** The OCR hop adds 2–5 seconds typical, but because the pipeline is asynchronous end‑to‑end, users do not notice.
- **Idempotency requirement:** OCR must be deterministic for the same input to allow safe reprocessing. We enforce this by caching extracted text keyed by `sha256(raw_content)` in Redis (TTL 90 days).
- **Dead‑letter queue:** A separate DLQ topic (`document.ocr.dlq`) receives messages that fail after 3 retries. The OCR team monitors this topic and manually investigates.

## Alternatives Considered

- **Embedded OCR within the compliance service:** Rejected after the June 2023 spike where a batch of CAD‑generated PDFs brought down the entire compliance evaluation pipeline because CPU contention blocked external API calls.
- **Separate OCR as a synchronous HTTP API:** Would couple the compliance engine to OCR availability; downtime would block all processing. Kafka decouples them and provides buffering.

## Operational Impact

- **Scaling:** OCR consumer group can be scaled horizontally during filing season (Q1, Q3). We use KEDA to autoscale based on consumer lag >2000.
- **Monitoring:** OCR processing duration p99 is tracked; after INC-2025-08-14 we added a per‑document‑type dimension so we can distinguish normal PDFs from CAD rips.
- **GPU scheduling:** In production, OCR runs on a dedicated node pool with T4 GPUs. The pod resource requests are tuned to avoid OOM (see incident postmortem).