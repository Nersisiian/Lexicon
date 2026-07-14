import random

def predict_load() -> float:
    # ¬ production здесь будет модель, обученна€ на Prometheus?метриках
    return round(random.uniform(0.1, 0.9), 2)
