import csv, pathlib
p = pathlib.Path(__file__).resolve().parents[1]
log = p / 'data' / 'sample_logs.csv'
times=[]; angles=[]
with open(log) as f:
    r = csv.DictReader(f)
    for row in r:
        times.append(float(row['t'])); angles.append(float(row['angle']))

def test_recovery_time():
    for t,a in zip(times, angles):
        if abs(a) < 2.0:
            assert t < 3.0
            return
    assert False, "Did not recover within 3s"

def test_steady_state_error():
    tail = angles[int(len(angles)*0.8):]
    avg = sum(abs(a) for a in tail)/len(tail)
    assert avg < 1.0
