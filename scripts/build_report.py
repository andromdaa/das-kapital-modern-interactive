"""Build research-report.md from parallels/, review/ and themes-index.json."""
import json, re, collections
from pathlib import Path
root = Path(__file__).resolve().parent.parent
idx = json.loads((root / "themes-index.json").read_text())["items"]
PILOT_FIRST = {"T78": "missed"}  # pilot verdict superseded by the post-checkpoint redo
rows, changes = [], []
for it in idx:
    tid = it["id"]
    if it["testable"] == "no":
        rows.append((tid, it["title"], it["specificity"], "too_vague_to_judge", "pre-set (not testable)")); continue
    p = json.loads((root / "parallels" / f"{tid}.json").read_text())
    rv = root / "review" / f"{tid}.md"
    before = after = None
    if rv.exists():
        m = re.match(r"verdict_before:\s*(\S+)\s*\|\s*verdict_after:\s*(\S+)", rv.read_text().splitlines()[0])
        if m: before, after = m.group(1), m.group(2)
    if after and after != p["verdict"]: raise SystemExit(f"{tid}: review says {after}, file says {p['verdict']}")
    if before and before != after:
        why = re.search(r"\*\*Verdict\*\*\s*\n+(.+?)(\n\n|\n#|\n\*\*)", rv.read_text(), re.S)
        changes.append((tid, it["title"], before, after, f"review/{tid}.md"))
    rows.append((tid, it["title"], p["specificity"], p["verdict"], "reviewed" if rv.exists() else "NOT REVIEWED"))
c = collections.Counter(r[3] for r in rows)
bys = collections.defaultdict(collections.Counter)
for r in rows: bys[r[2]][r[3]] += 1
V = ["holds", "partial", "missed", "too_vague_to_judge"]
L = ["# Research report", "", f"Items in themes index: {len(rows)} ({sum(1 for r in rows if r[4]!='pre-set (not testable)')} researched and skeptic-reviewed, "
     f"{sum(1 for r in rows if r[4]=='pre-set (not testable)')} pre-set to too_vague_to_judge as not testable). Opponent claims (O01–O30) are not researched.", "",
     "## Final count per verdict", "", "| Verdict | Count |", "|---|---|"] + [f"| {v} | {c[v]} |" for v in V] + [f"| **total** | {len(rows)} |", "",
     "| Specificity | " + " | ".join(V) + " |", "|---|" + "---|" * len(V)] + \
    [f"| {s} | " + " | ".join(str(bys[s][v]) for v in V) + " |" for s in ("concrete_forecast", "general_warning", "described_pattern")] + \
    ["", "## Verdicts changed in skeptic review", "", "| ID | Item | Before | After | Review |", "|---|---|---|---|---|"] + \
    [f"| {t} | {ti} | {b} | {a} | [{r}]({r}) |" for t, ti, b, a, r in changes] + ["", "## All items", "", "| ID | Item | Specificity | Verdict | Status |", "|---|---|---|---|---|"] + \
    [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
(root / "work" / "report_tables.md").write_text("\n".join(L) + "\n")
print(c, len(changes), [x[0] for x in changes])
