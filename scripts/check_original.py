"""Check original/*.md: IDs unique/continuous per chapter, every marker has a note in the same file and vice versa,
note labels sequential per chapter. Prints a per-file table (TSV) and problems."""
import glob, json, os, re, sys
from collections import defaultdict
root = sys.argv[1] if len(sys.argv) > 1 else 'original'
ids_by_ch = defaultdict(list)
labels_by_ch = defaultdict(list)
problems = []
rows = []
def order(f):
    m = re.match(r'ch(\d+)(?:-s(\d+))?([a-z]?)\.md', os.path.basename(f))
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3))


for f in sorted(glob.glob(os.path.join(root, 'ch*.md')), key=order):
    t = open(f).read()
    name = os.path.basename(f)
    ch = int(name[2:4])
    ids = re.findall(r'<!-- ((?:ch\d\d|pt\d)-p\d{3}) -->', t)
    defs = re.findall(r'^\[\^([^\]]+)\]:', t, re.M)
    body = re.sub(r'^\[\^[^\]]+\]:.*$', '', t, flags=re.M)
    refs = re.findall(r'\[\^([^\]]+)\](?!:)', body)
    for r in refs:
        if r not in defs: problems.append('%s: marker [^%s] has no note in file' % (name, r))
    for d in defs:
        if d not in refs: problems.append('%s: note [^%s] has no marker in file' % (name, d))
    ids_by_ch[ch] += [i for i in ids if i.startswith('ch')]
    labels_by_ch[ch] += defs
    words = len(re.sub(r'<!--.*?-->', '', t).split())
    rows.append((name, words, len(ids), len(defs)))
for ch, ids in ids_by_ch.items():
    nums = [int(i.split('-p')[1]) for i in ids]
    if nums != list(range(1, len(nums) + 1)):
        problems.append('ch%02d: paragraph IDs not continuous' % ch)
    labs = [l for l in labels_by_ch[ch] if not l.startswith('*')]
    nums = [int(re.match(r'\d+', l).group(0)) for l in labs]
    for a, b in zip(nums, nums[1:]):
        if b not in (a, a + 1):
            problems.append('ch%02d: note numbering jumps %d -> %d' % (ch, a, b))
    if nums and nums[0] != 1:
        problems.append('ch%02d: notes start at %d' % (ch, nums[0]))
for r in rows: print('\t'.join(map(str, r)))
print('TOTAL\t%d\t%d\t%d' % (sum(r[1] for r in rows), sum(r[2] for r in rows), sum(r[3] for r in rows)))
print('PROBLEMS', len(problems))
for p in problems: print('  ' + p)
