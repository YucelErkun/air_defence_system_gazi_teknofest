import time

class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.setpoint = setpoint
        self.last_error = 0.0
        self.integral = 0.0
        self.last_time = time.time()

    def update(self, current_value: float) -> float:
        now = time.time()
        dt = max(1e-6, now - self.last_time)
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        output = self.kp*error + self.ki*self.integral + self.kd*derivative
        self.last_error, self.last_time = error, now
        return float(output)
