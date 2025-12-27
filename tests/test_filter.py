import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from control.lib.filter import complementary_filter_step

def test_filter_runs():
    angle = complementary_filter_step(acc_angle=10.0, gyro_rate=0.0, dt=0.01, alpha=0.98, prev_angle=0.0)
    assert isinstance(angle, float)
