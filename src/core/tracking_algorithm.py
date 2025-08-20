class TargetTracker:
    def __init__(self):
        self.last = None

    def update(self, target: dict) -> dict:
        self.last = target
        return target

    def idle(self):
        pass
