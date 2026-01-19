import numpy as np

class PIDController:
    def __init__(self, kp, ki, kd, dt, deriv_filter_tau=0.02,
                 output_limits=(-12,12), integral_limits=(-2,2),
                 angle_index=2, ang_vel_index=3):
        self.kp = kp; self.ki = ki; self.kd = kd
        self.dt = dt; self.tau = deriv_filter_tau
        self.output_limits = tuple(output_limits)
        self.integral_limits = tuple(integral_limits)
        self.angle_index = angle_index; self.ang_vel_index = ang_vel_index
        self.integral = 0.0
        self.last_error = 0.0
        self.last_deriv = 0.0

    @classmethod
    def from_config(cls, cfg, dt):
        return cls(cfg['kp'], cfg['ki'], cfg['kd'], dt,
                   cfg.get('deriv_filter_tau', 0.02),
                   tuple(cfg.get('output_limits', [-12,12])),
                   tuple(cfg.get('integral_limits', [-2,2])))

    def compute_control(self, x):
        theta = float(x[self.angle_index])
        error = -theta
        self.integral += error * self.dt
        self.integral = max(self.integral_limits[0], min(self.integral_limits[1], self.integral))
        raw_deriv = (error - self.last_error) / self.dt
        alpha = self.tau / (self.tau + self.dt)
        deriv = alpha * self.last_deriv + (1 - alpha) * raw_deriv
        u = self.kp*error + self.ki*self.integral + self.kd*deriv
        u = max(self.output_limits[0], min(self.output_limits[1], u))
        self.last_error = error
        self.last_deriv = deriv
        return np.array([[u]])
