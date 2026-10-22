#!/bin/bash
# prepare a group review prompt and mark the group as reviewing
cd "$(dirname "$0")/.."
g=$1
files=$(python3 -c "import json;print(', '.join(json.load(open('work/groups.json'))['$g']['files']))")
sed "s/{FILES}/$files/g" work/group_review_prompt.md > work/reviews/review-$g.prompt
python3 scripts/pipeline.py review $g
python3 - "$g" <<'PY'
import json, sys, os
g = sys.argv[1]
h = json.load(open('work/review_hints.json')) if os.path.exists('work/review_hints.json') else {}
if g in h:
    open('work/reviews/review-%s.prompt' % g, 'a').write('\nExtra points from the orchestrator for this group:\n- ' + h[g] + '\n')
PY
