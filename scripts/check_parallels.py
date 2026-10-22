"""Check parallels/*.json: schema, anchors resolve in anchors.json, every source has a URL and a YYYY-MM-DD date."""
import json, re, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
anchors = json.loads((root / "anchors.json").read_text())
index = {i["id"]: i for i in json.loads((root / "themes-index.json").read_text())["items"]}
KEYS = ["id", "title", "book_claim", "anchors", "specificity", "test", "verdict", "parallel", "reasoning",
        "present_day_topics", "sources", "researched_on"]
SPEC = {"concrete_forecast", "general_warning", "described_pattern"}
VERD = {"holds", "partial", "missed", "too_vague_to_judge"}
date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
problems, n = [], 0
for f in sorted((root / "parallels").glob("*.json")):
    n += 1
    try: d = json.loads(f.read_text())
    except Exception as e: problems.append(f"{f.name}: invalid JSON ({e})"); continue
    for k in KEYS:
        if k not in d: problems.append(f"{f.name}: missing {k}")
    if d.get("id") != f.stem: problems.append(f"{f.name}: id {d.get('id')} != filename")
    if d.get("id") not in index: problems.append(f"{f.name}: id not in themes-index")
    if d.get("specificity") not in SPEC: problems.append(f"{f.name}: bad specificity {d.get('specificity')}")
    if d.get("verdict") not in VERD: problems.append(f"{f.name}: bad verdict {d.get('verdict')}")
    for a in d.get("anchors", []):
        if a not in anchors: problems.append(f"{f.name}: anchor {a} not in anchors.json")
    if not d.get("anchors"): problems.append(f"{f.name}: no anchors")
    if not d.get("sources") and d.get("verdict") != "too_vague_to_judge": problems.append(f"{f.name}: no sources")
    for i, s in enumerate(d.get("sources", [])):
        if not str(s.get("url", "")).startswith("http"): problems.append(f"{f.name}: source {i} has no URL")
        if not date.match(str(s.get("published", ""))): problems.append(f"{f.name}: source {i} bad date {s.get('published')!r}")
        if s.get("published_precision") not in ("day", "month", "year"): problems.append(f"{f.name}: source {i} missing published_precision")
    if not date.match(str(d.get("researched_on", ""))): problems.append(f"{f.name}: bad researched_on")
print(f"{n} parallels files checked")
print("\n".join(problems) or "OK: no problems")
sys.exit(1 if problems else 0)
