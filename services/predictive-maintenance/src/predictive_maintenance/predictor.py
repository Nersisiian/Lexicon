import random

class FailurePredictor:
    def predict(self) -> float:
        # ¬ production здесь будет модель, обученна€ на реальных метриках
        # —ейчас возвращаем случайное значение дл€ демонстрации
        return round(random.uniform(0.0, 0.3), 3)
