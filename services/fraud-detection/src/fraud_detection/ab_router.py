import random
from typing import Tuple, Dict, Any
from .config import settings
from .ensemble import FraudEnsemble

class ABRouter:
    def __init__(self):
        self.model_a = FraudEnsemble(settings.MODEL_PATH)
        self.model_b = None
        if settings.AB_ENABLE_MODEL_B:
            self.model_b = FraudEnsemble("/models/fraud_model_b.pkl")  # путь к альтернативной модели
        self.traffic_split = settings.AB_TRAFFIC_SPLIT

    def predict(self, features: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        if self.model_b and random.random() < self.traffic_split:
            return self.model_b.predict_risk(features), "model_b"
        return self.model_a.predict_risk(features), "model_a"
