import numpy as np
from scipy import linalg

class LQRController:
    def __init__(self, A, B, Q, R):
        self.A = np.array(A)
        self.B = np.array(B)
        self.Q = np.array(Q)
        self.R = np.array(R)
        self.K = self.compute_gain()

    def compute_gain(self):
        P = linalg.solve_continuous_are(self.A, self.B, self.Q, self.R)
        return np.linalg.inv(self.R) @ (self.B.T @ P)

    @classmethod
    def from_config(cls, A, B, cfg):
        return cls(A, B, cfg['Q'], cfg['R'])

    def compute_control(self, x):
        return - self.K @ np.array(x).reshape(-1,1)
