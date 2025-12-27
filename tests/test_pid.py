import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from control.lib.pid import PIDController

def test_pid_basic():
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0, dt=0.01)
    u = pid.step(setpoint=0.0, measurement=1.0)
    assert u < 0
