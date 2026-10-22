"""Update status.json. Usage: python3 scripts/status.py <file> <state> [key=value ...]
States: pending, rewritten, checked, reviewed, fixed (done)."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'status.json')
s = json.load(open(p))
f, state = sys.argv[1], sys.argv[2]
u = s['units'][f]
u['state'] = state
u.setdefault('history', []).append([state, time.strftime('%Y-%m-%dT%H:%M:%S')])
for kv in sys.argv[3:]:
    k, v = kv.split('=', 1)
    u[k] = v
json.dump(s, open(p, 'w'), indent=1)
print(f, state)
