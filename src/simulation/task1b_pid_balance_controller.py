#!/usr/bin/env python3
import csv, math, sys, pathlib

# ---- FIX: make src/ importable ----
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from control.lib.pid import PIDController

T = 5.0
dt = 0.01
t = 0.0
angle = 5.0  # initial tilt (deg)

pid = PIDController(kp=2.0, ki=0.5, kd=0.1, dt=dt)

out_dir = ROOT / "data"
out_dir.mkdir(exist_ok=True)
log_path = out_dir / "sample_logs.csv"

with open(log_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["t", "angle", "u"])
    writer.writeheader()

    while t <= T:
        u = pid.step(0.0, angle)
        angle += -u * dt + 0.01 * math.sin(2 * math.pi * 0.5 * t)
        writer.writerow({"t": round(t, 3), "angle": angle, "u": u})
        t += dt

print("Simulation complete:", log_path)
