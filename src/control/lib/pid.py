class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt=0.01, integrator_limit=1000.0):
        self.kp = kp; self.ki = ki; self.kd = kd; self.dt = dt
        self.integrator = 0.0; self.prev_error = 0.0
        self.integrator_limit = integrator_limit
    def step(self, setpoint, measurement):
        e = setpoint - measurement
        self.integrator += e * self.dt
        # clamp integrator
        if self.integrator > self.integrator_limit: self.integrator = self.integrator_limit
        if self.integrator < -self.integrator_limit: self.integrator = -self.integrator_limit
        derivative = (e - self.prev_error) / self.dt
        self.prev_error = e
        u = self.kp * e + self.ki * self.integrator + self.kd * derivative
        return u
