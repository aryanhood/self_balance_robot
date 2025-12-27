# Two-Wheel Self-Balancing Robot — Interview-Ready

## Problem
Maintain balance of a two-wheel inverted-pendulum robot using microcontroller-level control loop with IMU feedback.

## Quickstart
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
python3 src/simulation/task1b_pid_balance_controller.py
python3 scripts/plot_logs.py data/sample_logs.csv out/plot_recovery.png
