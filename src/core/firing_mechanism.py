class FiringSystem:
    def __init__(self, sim=True):
        self.sim = sim
        self.count = 0

    def engage(self):
        # Simülasyon: sayaç artır
        self.count += 1
