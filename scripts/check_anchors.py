"""Phase A: verify paragraph IDs in original/ are unique, continuous per chapter, and match anchors.json."""
import json, re, sys, collections
from pathlib import Path
root = Path(__file__).resolve().parent.parent
anchors = json.loads((root / "anchors.json").read_text())
pat = re.compile(r"<!--\s*(ch\d+|front|[a-z0-9]+)-p(\d+)\s*-->")
seen = collections.defaultdict(list)
order = []
natkey = lambda f: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", f.name)]
for f in sorted((root / "original").glob("*.md"), key=natkey):
    for i, line in enumerate(f.read_text().splitlines(), 1):
        m = re.match(r"<!--\s*(\S+)\s*-->", line.strip())
        if m and re.match(r"^[a-z0-9]+-p\d+$", m.group(1)):
            seen[m.group(1)].append((f.name, i)); order.append((m.group(1), f.name))
problems = []
for k, v in seen.items():
    if len(v) > 1: problems.append(f"duplicate {k}: {v}")
bych = collections.defaultdict(list)
for k, _ in order:
    pre, n = k.rsplit("-p", 1); bych[pre].append(int(n))
for pre, nums in bych.items():
    if nums != list(range(1, len(nums) + 1)):
        exp = 1
        for n in nums:
            if n != exp: problems.append(f"{pre}: expected p{exp:03d}, found p{n:03d}"); exp = n
            exp += 1
file_ids, map_ids = set(seen), set(anchors)
for k in sorted(map_ids - file_ids): problems.append(f"in anchors.json but not original/: {k}")
for k in sorted(file_ids - map_ids): problems.append(f"in original/ but not anchors.json: {k}")
for k, v in seen.items():
    if k in anchors and anchors[k]["file"] != v[0][0]: problems.append(f"file mismatch {k}: {anchors[k]['file']} vs {v[0][0]}")
print(f"{len(file_ids)} IDs in original/, {len(map_ids)} in anchors.json, {len(bych)} chapters/prefixes")
print("\n".join(problems) or "OK: no problems")
sys.exit(1 if problems else 0)
