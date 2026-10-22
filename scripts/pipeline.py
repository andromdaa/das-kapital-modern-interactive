"""Phase 4 pipeline bookkeeping (state lives in status.json; groups in work/groups.json).

  python3 scripts/pipeline.py init            # build review groups (~5 consecutive units) and unit contexts
  python3 scripts/pipeline.py start <file>    # mark a unit as being rewritten
  python3 scripts/pipeline.py rewritten <file># run check_pair; PASS -> checked, FAIL -> prints failures
  python3 scripts/pipeline.py review <gid>    # mark a group as under review
  python3 scripts/pipeline.py reviewed <gid>  # re-run checks on the group; PASS -> fixed
  python3 scripts/pipeline.py next [cap]      # what to launch now, given cap on agents in flight (default 9)
  python3 scripts/pipeline.py summary
Unit states: pending -> rewriting -> checked -> reviewing -> fixed. Pilot units are already fixed.
"""
import json, os, re, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'status.json')
GP = os.path.join(ROOT, 'work', 'groups.json')


def order(f):
    m = re.match(r'ch(\d+)(?:-s(\d+))?([a-z]?)\.md', f)
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3)) if m else (0, 0, '')


def load():
    return json.load(open(SP))


def save(s):
    json.dump(s, open(SP, 'w'), indent=1)


def setstate(s, f, st, **kw):
    u = s['units'][f]
    u['state'] = st
    u.setdefault('history', []).append([st, time.strftime('%Y-%m-%dT%H:%M:%S')])
    u.update(kw)


def check(f):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'check_pair.py'), f, '--json'],
                       capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout)


def init():
    s = load()
    units = sorted([f for f in s['units'] if f.startswith('ch') and s['units'][f]['state'] == 'pending'], key=order)
    groups, cur, w = [], [], 0
    for f in units:
        uw = s['units'][f]['words']
        if cur and (len(cur) >= 5 or w + uw > 24000):
            groups.append(cur); cur, w = [], 0
        cur.append(f); w += uw
    if cur:
        groups.append(cur)
    g = {'g%02d' % (i + 1): dict(files=fs, state='open') for i, fs in enumerate(groups)}
    json.dump(g, open(GP, 'w'), indent=1)
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'unit_context.py')] + units, cwd=ROOT,
                   capture_output=True)
    print(len(units), 'units in', len(g), 'groups')


def nxt(cap):
    s = load(); g = json.load(open(GP))
    U = s['units']
    inflight = sum(1 for u in U.values() if u['state'] == 'rewriting') + \
        sum(1 for x in g.values() if x['state'] == 'reviewing')
    free = cap - inflight
    out = {'in_flight': inflight, 'reviews': [], 'rewrites': []}
    for gid, x in g.items():
        if free <= 0:
            break
        if x['state'] == 'open' and all(U[f]['state'] == 'checked' for f in x['files']):
            out['reviews'].append(gid); free -= 1
    pend = sorted([f for f, u in U.items() if u['state'] == 'pending' and f.startswith('ch')], key=order)
    out['rewrites'] = pend[:max(0, free)]
    print(json.dumps(out))


def main():
    cmd = sys.argv[1]
    if cmd == 'init':
        return init()
    if cmd == 'next':
        return nxt(int(sys.argv[2]) if len(sys.argv) > 2 else 9)
    s = load()
    if cmd == 'start':
        for f in sys.argv[2:]:
            setstate(s, f, 'rewriting')
        save(s); print('started', ' '.join(sys.argv[2:]))
    elif cmd == 'rewritten':
        f = sys.argv[2]
        r = check(f)
        if r['ok']:
            setstate(s, f, 'checked', ratio=r['ratio'])
            print('PASS', f, r['ratio'], '| warnings:', len(r['warnings']))
        else:
            setstate(s, f, 'rewriting', last_fail=r['failures'][:20])
            print('FAIL', f); [print('  ', x) for x in r['failures'][:20]]
        save(s)
    elif cmd == 'review':
        g = json.load(open(GP)); gid = sys.argv[2]
        g[gid]['state'] = 'reviewing'
        for f in g[gid]['files']:
            setstate(s, f, 'reviewing')
        json.dump(g, open(GP, 'w'), indent=1); save(s); print('reviewing', gid, g[gid]['files'])
    elif cmd == 'reviewed':
        g = json.load(open(GP)); gid = sys.argv[2]
        bad = []
        for f in g[gid]['files']:
            r = check(f)
            rv = os.path.join(ROOT, 'work', 'reviews', f + '.json')
            verdict = json.load(open(rv)).get('verdict') if os.path.exists(rv) else 'MISSING'
            if r['ok'] and verdict != 'MISSING':
                setstate(s, f, 'fixed', ratio=r['ratio'], review=verdict)
            else:
                bad.append((f, verdict, r['failures'][:5]))
        g[gid]['state'] = 'done' if not bad else 'reviewing'
        json.dump(g, open(GP, 'w'), indent=1); save(s)
        print(gid, 'done' if not bad else 'PROBLEMS', bad)
    elif cmd == 'summary':
        from collections import Counter
        c = Counter(u['state'] for f, u in s['units'].items() if f.startswith('ch'))
        print(dict(c))


if __name__ == '__main__':
    main()
