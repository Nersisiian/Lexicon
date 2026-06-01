# AI Document Compliance Platform

Internal platform for automated processing, validation, and review of regulatory documents.

## Services

- **intake-gateway** – Document upload and event initiation.
- **ocr-pipeline** – OCR extraction (PaddleOCR with legacy fallback).
- **document-classifier** – Classifies document type via fine-tuned BERT.
- **compliance-engine** – Rule-based completeness and AML checks.
- **fraud-detection** – Ensemble model for fraud flags.
- **reasoning-service** – LLM risk assessment.
- **audit-ledger** – Immutable audit event store.
- **review-workbench** – Human review task management.
- **notification-orchestrator** – Dispatch alerts to Slack, email, etc.

## Quick Start

```bash
make run