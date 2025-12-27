#!/usr/bin/env python3
import sys, csv, os
import matplotlib.pyplot as plt

def plot(csv_path, out_path):
    t=[]; angle=[]
    with open(csv_path) as f:
        r=csv.DictReader(f)
        for row in r:
            t.append(float(row['t'])); angle.append(float(row['angle']))
    plt.figure(figsize=(6,3))
    plt.plot(t, angle)
    plt.xlabel('time (s)'); plt.ylabel('angle (deg)'); plt.title('Recovery')
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    print('Saved', out_path)

if __name__=='__main__':
    if len(sys.argv)<3:
        print('Usage: plot_logs.py input.csv output.png')
    else:
        plot(sys.argv[1], sys.argv[2])
