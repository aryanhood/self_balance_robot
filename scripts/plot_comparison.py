import csv, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'plots'

def load(p):
    t=[]; th=[]; u=[]
    with open(p) as f:
        for r in csv.DictReader(f):
            t.append(float(r['t'])); th.append(float(r['theta'])); u.append(float(r['u']))
    return np.array(t),np.array(th),np.array(u)

pt,ptheta,pu = load(P/'pid_log.csv')
lt,ltheta,lu = load(P/'lqr_log.csv')

plt.figure()
plt.plot(pt,ptheta,label='PID')
plt.plot(lt,ltheta,label='LQR')
plt.axvline(2,ls='--',label='Disturbance')
plt.legend(); plt.xlabel('Time'); plt.ylabel('Angle (rad)')
plt.title('Disturbance Rejection')
plt.savefig(P/'pid_vs_lqr_theta.png',dpi=200)

plt.figure()
plt.plot(pt,pu,label='PID')
plt.plot(lt,lu,label='LQR')
plt.legend(); plt.xlabel('Time'); plt.ylabel('Control')
plt.title('Control Effort')
plt.savefig(P/'pid_vs_lqr_u.png',dpi=200)

print('Plots saved')