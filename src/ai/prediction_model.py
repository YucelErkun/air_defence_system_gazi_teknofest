from collections import deque

class MotionPredictor:
    def __init__(self, history_len=30):
        self.history = deque(maxlen=history_len)

    def predict(self, target: dict) -> dict:
        if target is None:
            return {"center": (0.0, 0.0)}
        self.history.append(target["center"])
        # Basit: son konumu döndür (ileride Kalman, sabit hız modeli eklenebilir)
        return target
