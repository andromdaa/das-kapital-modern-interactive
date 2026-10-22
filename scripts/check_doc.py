"""Footnote integrity check on work/doc.json: markers vs notes per chapter."""
import json, sys
from collections import Counter
D = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'work/doc.json'))
tot = 0
for c in D['chapters']:
    paras = [b for b in c['blocks'] if b['type'] == 'para']
    marks = c['heading_markers'] + [m for b in c['blocks'] for m in b.get('markers', [])]
    notes = c['note_order']
    miss = [m for m in marks if m not in c['notes']]
    orphan = [n for n in notes if n not in marks]
    dup = [m for m, k in Counter(marks).items() if k > 1]
    empty = [n for n in notes if not ''.join(p['text'] for p in c['notes'][n]).strip()]
    nums = [int(''.join(ch for ch in n if ch.isdigit())) for n in notes if not n.startswith('*')]
    seq = [a for a, b in zip(nums, nums[1:]) if b not in (a, a + 1)]
    words = sum(len(p['text'].split()) for p in paras)
    tot += words
    print(c['kind'][0] + str(c['num']), 'paras', len(paras), 'words', words, 'notes', len(notes), 'miss', miss, 'orphan', orphan,
          'dup', dup, 'empty', empty, 'seqgap', seq, c['note_problems'], c['odd_sups'])
print('body words', tot)
