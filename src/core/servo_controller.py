class ServoController:
    def __init__(self, sim=True):
        self.sim = sim
        self.pan, self.tilt = 0.0, 0.0  # derece

    def move_relative(self, dx, dy):
        # Basit simülasyon: değerleri biriktir
        self.pan += dx*0.01
        self.tilt += dy*0.01
