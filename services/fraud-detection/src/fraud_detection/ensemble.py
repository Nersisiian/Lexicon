import pickle
import structlog

logger = structlog.get_logger(__name__)

class FraudEnsemble:
    def __init__(self, path: str):
        with open(path, "rb") as f:
            self._model = pickle.load(f)

    def predict_risk(self, features: dict) -> dict:
        # simple wrapper that expects pre-computed feature vector
        # In production, this would be a more sophisticated pipeline.
        return {"probability": 0.0, "flags": []}
