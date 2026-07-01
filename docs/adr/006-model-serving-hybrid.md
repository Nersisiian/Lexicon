# ADR-006: Hybrid model serving – embedded vs. dedicated inference services

**Status:** Accepted  
**Date:** 2024-06-18  
**Author:** ML Platform Team, OCR Team  
**Superseded by:** None

## Context

The platform uses multiple ML models: document classification (BERT‑base), NER (fine‑tuned BERT), fraud detection (scikit‑learn ensemble), and OCR (PaddleOCR with legacy Tesseract). We needed a serving strategy that balances latency, resource cost, and model lifecycle management.

## Decision

We adopt a **hybrid approach**:

- **Lightweight, stable models** (classification, NER) are embedded directly into their respective service processes using HuggingFace `pipeline`. They run on CPU, with optional GPU nodes for high‑throughput environments.
- **Heavier or frequently updated models** (fraud ensemble, future LLM fine‑tunes) are served via a separate, centralised model server (currently TorchServe) that scales independently.
- **LLM reasoning** is always an external call to an internally hosted LLM service (vLLM on A100s) because the models are too large to embed.

## Rationale

- **Latency:** Embedding small models avoids a network hop; classification with a 512‑token truncation takes ~30ms on CPU.
- **Cost:** Running dedicated GPU pods for classification would be wasteful; embedding on CPU allows us to use cheaper compute.
- **Model lifecycle:** The fraud ensemble is retrained weekly and A/B tested; a central server allows us to swap models without redeploying the fraud service. The classification model is stable (retrained quarterly), so embedding is acceptable.
- **GPU utilisation:** The LLM serving requires expensive A100s; centralising it maximises utilisation and amortises cost.

## Consequences

- **Embedded models increase image size:** The document‑classifier image includes a 400MB model file. We mitigate with a base image that pre‑caches the model and a model registry that pulls at startup (with a local cache).
- **Startup time:** Services with embedded models take ~20s to start on cold nodes because of model loading. Readiness probes are delayed accordingly.
- **GPU scheduling:** The OCR pipeline may use GPU if available; we use a device plugin to schedule GPU‑enabled pods on dedicated nodes. Fallback to CPU is automatic.
- **Central LLM dependency:** If the LLM service is down, the reasoning service publishes a placeholder event (`LLM unavailable`) instead of blocking the pipeline. This avoids dead‑locking the entire document flow.

## Alternatives Considered

- **All models embedded:** Rejected because fraud ensemble updates would force redeployment of the fraud service; LLMs cannot fit in service pods.
- **All models behind a unified prediction API:** Would simplify architecture but add 10–50ms network overhead per prediction, and classification/OCR are used in high‑throughput scenarios where that overhead accumulates. Also a single point of failure.

## Operational Impact

- **Scaling:** Embedded‑model services scale horizontally by increasing replicas; each replica loads the model independently. We avoid GPU nodes for these unless necessary.
- **Monitoring:** Model inference latency and error rates are exported per service. A `model_version` label distinguishes A/B tests.
- **Model versioning:** All models are versioned in MLflow Registry. The classification service queries MLflow on startup if a `MODEL_VERSION` env var is set; otherwise uses a baked‑in default. This caused an incident (INC-2024-12-01) where a new model version increased memory 3x, causing OOM. Now we validate memory footprint in CI before promoting model versions.