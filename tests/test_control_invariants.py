"""Control-theoretic stability and disturbance-rejection invariants for PID vs. LQR."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.control.lqr import LQRController
from src.control.pid import PIDController


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def _simulate_impulse(
    controller: PIDController | LQRController, a: np.ndarray, b: np.ndarray, ts: float
) -> tuple[np.ndarray, np.ndarray]:
    x = np.zeros((4, 1), dtype=np.float64)
    thetas: list[float] = []
    controls: list[float] = []
    for k in range(int(6.0 / ts)):
        t = k * ts
        if abs(t - 2.0) < ts / 2.0:
            x[2, 0] += 0.1
        u = np.asarray(controller.compute_control(x.flatten()), dtype=np.float64).reshape(1, 1)
        x = x + ts * (a @ x + b @ u)
        thetas.append(float(x[2, 0]))
        controls.append(float(u[0, 0]))
    return np.asarray(thetas), np.asarray(controls)


def test_open_loop_unstable_and_lqr_stabilizes_pendulum_modes() -> None:
    plant = _load_json(ROOT / "config" / "plant.json")
    lqr_cfg = _load_json(ROOT / "config" / "lqr.json")
    a = np.asarray(plant["A"], dtype=np.float64)
    b = np.asarray(plant["B"], dtype=np.float64)

    open_poles = np.linalg.eigvals(a)
    assert float(np.max(np.real(open_poles))) > 3.0, "Open-loop inverted pendulum must have unstable RHP pole"

    ctrl = LQRController.from_config(a, b, lqr_cfg)
    closed_poles = np.linalg.eigvals(a - b @ ctrl.K)
    real_parts = np.sort(np.real(closed_poles))
    # All controllable modes (rank 3 due to shared unit input channel on v and theta_dot) lie in open LHP
    assert float(np.max(real_parts)) < 1e-9
    assert int(np.sum(real_parts < -0.05)) == 3


def test_lqr_achieves_lower_effort_and_tighter_settling_than_pid() -> None:
    plant = _load_json(ROOT / "config" / "plant.json")
    pid_cfg = _load_json(ROOT / "config" / "pid.json")
    lqr_cfg = _load_json(ROOT / "config" / "lqr.json")
    a = np.asarray(plant["A"], dtype=np.float64)
    b = np.asarray(plant["B"], dtype=np.float64)
    ts = float(plant["sampling_time"])  # type: ignore[arg-type]

    pid = PIDController.from_config(pid_cfg, ts)
    lqr = LQRController.from_config(a, b, lqr_cfg)

    th_pid, u_pid = _simulate_impulse(pid, a, b, ts)
    th_lqr, u_lqr = _simulate_impulse(lqr, a, b, ts)

    assert abs(th_lqr[-1]) < abs(th_pid[-1]) < 0.01
    assert float(np.sum(u_lqr**2)) < float(np.sum(u_pid**2))
    assert float(np.sum(th_lqr**2)) < float(np.sum(th_pid**2))
