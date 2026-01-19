import json, csv
import numpy as np
from pathlib import Path
from src.control.pid import PIDController
from src.control.lqr import LQRController

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'config'
PLOTS = ROOT / 'plots'
PLOTS.mkdir(exist_ok=True)

def load(p):
    with open(p) as f: return json.load(f)

plant = load(CONFIG/'plant.json')
A = np.array(plant['A'])
B = np.array(plant['B'])
Ts = plant['sampling_time']

pid = PIDController.from_config(load(CONFIG/'pid.json'), Ts)
lqr = LQRController.from_config(A, B, load(CONFIG/'lqr.json'))

def simulate(ctrl):
    x = np.zeros((4,1))
    log = []
    for k in range(int(6/Ts)):
        t = k*Ts
        if abs(t-2.0) < Ts/2:
            x[2,0] += 0.1
        u = ctrl.compute_control(x.flatten())
        x = x + Ts*(A@x + B@u)
        log.append((t,float(x[2,0]),float(u)))
    return log

for name,ctrl in [('pid',pid),('lqr',lqr)]:
    with open(PLOTS/f"{name}_log.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(['t','theta','u']); w.writerows(simulate(ctrl))

print("Simulation complete")