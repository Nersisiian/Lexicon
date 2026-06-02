import pickle
import structlog

logger = structlog.get_logger(__name__)

class FraudEnsemble:
    def __init__(self, path: str):
        # In production, load a trained model. Here we use a simple heuristic.
        self._path = path

    def predict_risk(self, features: dict) -> dict:
        # Rule-based demo: flag if completeness < 0.8 or aml_hits present
        completeness = features.get("completeness", {}).get("score", 1.0)
        aml_hits = features.get("aml_hits", [])
        probability = 0.0
        flags = []
        if completeness < 0.8:
            probability = 0.5
            flags.append("low_completeness")
        if aml_hits:
            probability = max(probability, 0.8)
            flags.append("sanctions_match")
        return {"probability": probability, "flags": flags}
