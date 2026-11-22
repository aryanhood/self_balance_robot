# Self-Balancing Control System — Engineering Validation

## Overview

This repository demonstrates a simple, reproducible control-systems validation for an unstable system analogous to a self-balancing robot (inverted pendulum). The project compares **PID** and **LQR** controllers using a linearized plant model and simulation-based analysis.

The focus is on **what was done, how it was validated, and what the results show**.

---

## What is implemented

* Linearized self-balancing plant model (config-driven)
* PID controller (classical feedback baseline)
* LQR controller (optimal state-feedback)
* Time-domain simulation with impulse disturbance
* Logged results and comparison plots

---

## How to run

From the repository root:

```bash
python -m src.simulation.compare_pid_vs_lqr
python scripts/plot_comparison.py
```

This generates simulation logs and the plots shown below.

---

## Results

### Disturbance rejection (angle vs time)

![Disturbance Rejection](plots/pid_vs_lqr_theta.png)

* Both controllers stabilize the system after a 0.1 rad disturbance.
* PID shows overshoot and oscillatory recovery.
* LQR returns the system to equilibrium smoothly with faster settling.

---

### Control effort (control input vs time)

![Control Effort](plots/pid_vs_lqr_u.png)

* PID produces large, oscillatory control inputs.
* LQR achieves stabilization with smoother and lower control effort.

---

## Quantitative Summary (0.1 rad Disturbance at t = 2.0 s)

| Controller | Settling Final `theta` (t = 6 s) | Squared Angle Error `sum(theta^2)` | Squared Control Effort `sum(u^2)` |
|---|---:|---:|---:|
| PID (`kp=20, kd=2`) | 0.00183 rad | 0.2748 | 253.28 |
| LQR (`CARE Q, R`) | **0.00164 rad** | **0.1731** (`-37.0%`) | **172.20** (`-32.0%`) |

> **Plant Modeling Note:** `config/plant.json` uses a unit-coupled surrogate `B = [0, 1, 0, 1]^T` (controllability rank 3), which stabilizes the pendulum and velocity dynamics cleanly in the left half-plane while leaving an uncoupled marginal integrator mode near `0` on cart position `x`.

---

## Conclusion

* PID provides a simple and robust baseline but results in oscillatory transients.
* LQR delivers better damping and control efficiency when an accurate plant model is available.

This comparison reflects trade-offs between classical and optimal control approaches.

---

## Reference Papers

* Jian Fang, The LQRController Design of Two‑Wheeled Self‑Balancing Robot Based on the Particle Swarm Optimization Algorithm (2014).

* Huaqiang Zhang & Norzalilah MohamadNor, Control Strategies for Two‑Wheeled Self‑Balancing Robotic Systems: A Comprehensive Review.

---

## License

MIT License
