"""Phase 5 step 1: for every glossary entry, list places where the original uses the term
and the rewrite paragraph does not use the chosen rendering (or still uses an archaic form).
Also: paragraph-level stats and cross-file checks. Writes work/consistency_glossary.json and prints a summary.
"""
import glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_pair as C

ROOT = C.ROOT


def main():
    gloss = C.load_glossary()
    misses = defaultdict(list)
    per_term = Counter()
    files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'rewrite', 'ch*.md')))
    variants_left = Counter()
    for name in files:
        o = open(os.path.join(ROOT, 'original', name)).read()
        r = open(os.path.join(ROOT, 'rewrite', name)).read()
        _, ou = C.split_units(o)
        rmap = dict(C.split_units(r)[1])
        for pid, ob in ou:
            rb = rmap.get(pid, '')
            ob2 = re.sub(r'^#{1,6} .*$', '', ob, flags=re.M)
            rb2 = re.sub(r'^#{1,6} .*$', '', rb, flags=re.M)
            for g in gloss:
                if g.get('mode') == 'avoid':
                    prose = C.strip_quoted(C.strip_notes(rb2))
                    prose = re.sub(r'```.*?```', '', prose, flags=re.S)
                    for v in g['variants']:
                        if v.lower() in prose.lower():
                            variants_left[g['term']] += 1
                            misses[g['term']].append(dict(file=name, id=pid, kind='archaic left'))
                    continue
                hit = [v for v in g['variants'] if C.present(C.term_pattern(v), ob2)]
                if not hit:
                    continue
                per_term[g['term']] += 1
                ok = C.present(C.term_pattern(g['rendering'], stem=True), rb2) or any(
                    C.present(C.term_pattern(a, stem=True), rb2) for a in g.get('also_ok', []))
                if not ok:
                    misses[g['term']].append(dict(file=name, id=pid, kind='rendering not used', original=hit[0]))
    out = {t: dict(paragraphs_with_term=per_term[t], misses=m) for t, m in misses.items()}
    json.dump(out, open(os.path.join(ROOT, 'work', 'consistency_glossary.json'), 'w'), indent=1)
    print('files checked:', len(files))
    for t, m in sorted(misses.items(), key=lambda x: -len(x[1])):
        print('%-32s %4d miss(es) / %4d paragraphs  e.g. %s' % (t, len(m), per_term.get(t, 0),
                                                               ', '.join(x['id'] for x in m[:4])))


if __name__ == '__main__':
    main()
