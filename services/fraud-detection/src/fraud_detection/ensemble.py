"""Fraud risk assessment engine.

Supports both rule?based scoring and trained ensemble models.
"""
from __future__ import annotations
import pickle
import structlog
from pathlib import Path

logger = structlog.get_logger(__name__)

class FraudEnsemble:
    def __init__(self, model_path: str | None = None):
        """Load a trained model if path is provided and valid."""
        self._model = None
        if model_path:
            try:
                with open(model_path, "rb") as f:
                    self._model = pickle.load(f)
                logger.info("fraud_model_loaded", path=model_path)
            except Exception:
                logger.warning("fraud_model_load_failed", path=model_path)

    def predict_risk(self, features: dict) -> dict:
        """Return fraud probability and flags."""
        # Rule?based fallback
        completeness = features.get("completeness", {}).get("score", 1.0)
        aml_hits = features.get("aml_hits", [])
        probability = 0.0
        flags = []

        if completeness < 0.8:
            probability = max(probability, 0.5)
            flags.append("low_completeness")
        if aml_hits:
            probability = max(probability, 0.8)
            flags.append("sanctions_match")

        # Use trained model if available
        if self._model is not None:
            # Placeholder for actual feature vector
            try:
                proba = self._model.predict_proba([list(features.values())])[0][1]
                probability = max(probability, float(proba))
                if proba > 0.7:
                    flags.append("ml_model_flag")
            except Exception:
                logger.warning("ml_model_inference_failed")

        return {"probability": probability, "flags": flags}
