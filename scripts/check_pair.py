"""Mechanical checks on one original/rewrite pair (Phase 4).

Usage: python3 scripts/check_pair.py ch10-s1.md [--json]
Exit status 0 = pass, 1 = failures. Warnings never fail a unit.

Checks:
  1. identical paragraph ID lines, same order
  2. same headings (count, level, order)
  3. same footnote labels, in the same order, each attached to the same paragraph
  4. every number / formula token of each original paragraph (incl. its notes) appears in the rewrite paragraph
  5. table and formula blocks copied verbatim (```text blocks; formula lines with '=')
  6. glossary.json: where an original paragraph uses a glossary term, the rewrite uses the chosen rendering
     (failure for entries with "enforce": true, warning otherwise)
  7. length ratio (warning outside 0.95-1.25x; failure below 0.90x)
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_RE = re.compile(r'^<!-- ((?:ch\d\d|pt\d)-p\d{3}) -->$', re.M)
NOTE_DEF = re.compile(r'^\[\^([^\]]+)\]:', re.M)
NOTE_REF = re.compile(r'\[\^([^\]]+)\](?!:)')
HEAD_RE = re.compile(r'^(#{1,6}) ', re.M)
# numbers: digits with internal , . / and trailing fractions; unicode vulgar fractions; algebra like 2n+2
NUM_RE = re.compile(r'(?<![\w^])(?:\d[\d,]*(?:\.\d+)?(?:\s?[½¼¾⅓⅔⅛⅜⅝⅞])?|[½¼¾⅓⅔⅛⅜⅝⅞])(?!\d)')
FORMULA_RE = re.compile(r"[CMWP](?:['′]?\s?[–—-]{1,6}\s?[CMWP]['′]?)+")


def split_units(text):
    """Return (preamble, [(id, block_text)]) where block_text runs to the next ID."""
    parts = ID_RE.split(text)
    pre = parts[0]
    units = []
    for i in range(1, len(parts), 2):
        units.append((parts[i], parts[i + 1]))
    return pre, units


def strip_notes(block):
    return NOTE_DEF.split(block)[0]


def notes_in(block):
    return NOTE_DEF.findall(block)


def numbers(s):
    s = re.sub(r'\[\^[^\]]+\]', '', s)          # footnote markers
    s = re.sub(r'<!--.*?-->', '', s)
    return Counter(re.sub(r'\s', '', m).rstrip(',') for m in NUM_RE.findall(s))


def formulas(s):
    return Counter(re.sub(r'\s', '', m) for m in FORMULA_RE.findall(s))


def fenced(s):
    return re.findall(r'```text\n(.*?)\n\s*```', s, re.S)


def eq_lines(s):
    """Formula lines: short lines containing '=' outside fenced blocks (normalised: no markup/space)."""
    s = re.sub(r'```text\n.*?```', '', s, flags=re.S)
    out = []
    for ln in s.split('\n'):
        t = re.sub(r'[>*\\`\s]', '', ln)
        if '=' in t and len(t) < 90:
            out.append(t)
    return out


def headings(text):
    return [(m.group(1), text[m.end():text.index('\n', m.end())].strip()) for m in HEAD_RE.finditer(text)]


def words(s):
    s = re.sub(r'<!--.*?-->', '', s)
    return len(s.split())


def load_glossary():
    p = os.path.join(ROOT, 'glossary.json')
    if not os.path.exists(p):
        return []
    return json.load(open(p))


def strip_quoted(s):
    """Drop text inside curly/straight double quotes and citation parentheses (quotations keep old wording)."""
    s = re.sub(r'“[^”]*”', '', s)
    s = re.sub(r'"[^"]*"', '', s)
    return s


def present(pattern, s):
    return re.search(pattern, s, re.I) is not None


def term_pattern(v, stem=False):
    core = re.escape(v).replace(r'\ ', r'[\s-]').replace(r'\-', r'[\s-]')
    return (r'(?<!\w)' if stem else r'(?<![\w-])') + core + ('' if stem else r'(?!\w)')


def check(name, orig_dir='original', rew_dir='rewrite'):
    o = open(os.path.join(ROOT, orig_dir, name)).read()
    r = open(os.path.join(ROOT, rew_dir, name)).read()
    fails, warns = [], []
    opre, ou = split_units(o)
    rpre, ru = split_units(r)
    oids = [i for i, _ in ou]
    rids = [i for i, _ in ru]
    if oids != rids:
        missing = [i for i in oids if i not in rids]
        extra = [i for i in rids if i not in oids]
        fails.append('ID lines differ: missing %s, extra %s%s' % (
            missing[:10], extra[:10], '' if missing or extra else ' (order differs)'))
    oh, rh = headings(o), headings(r)
    if [h[0] for h in oh] != [h[0] for h in rh]:
        fails.append('headings differ: original %d %s, rewrite %d %s' % (
            len(oh), [h[0] for h in oh], len(rh), [h[0] for h in rh]))
    # footnotes
    odefs, rdefs = NOTE_DEF.findall(o), NOTE_DEF.findall(r)
    if odefs != rdefs:
        fails.append('footnote labels differ: original %s / rewrite %s' % (odefs, rdefs))
    orefs = NOTE_REF.findall(NOTE_DEF.sub('', o))
    rrefs = NOTE_REF.findall(NOTE_DEF.sub('', r))
    if Counter(orefs) != Counter(rrefs):
        fails.append('footnote markers differ: missing %s, extra %s' % (
            list((Counter(orefs) - Counter(rrefs)).elements()), list((Counter(rrefs) - Counter(orefs)).elements())))
    gloss = load_glossary()
    rmap = dict(ru)
    for pid, ob in ou:
        rb = rmap.get(pid)
        if rb is None:
            continue
        if notes_in(ob) != notes_in(rb):
            fails.append('%s: notes attached %s, rewrite has %s' % (pid, notes_in(ob), notes_in(rb)))
        # markers per paragraph body
        om = NOTE_REF.findall(strip_notes(ob))
        rm = NOTE_REF.findall(strip_notes(rb))
        if Counter(om) != Counter(rm):
            fails.append('%s: paragraph markers %s, rewrite %s' % (pid, om, rm))
        on, rn = numbers(ob), numbers(rb)
        miss = on - rn
        # a token printed with a letter-for-digit typo ('£4OO') may be corrected; accept containment
        miss = Counter({k: v for k, v in miss.items() if not any(k in t and k != t for t in rn)})
        if miss:
            fails.append('%s: numbers missing in rewrite: %s' % (pid, sorted(miss.elements())[:12]))
        of, rf = formulas(ob), formulas(rb)
        if of - rf:
            fails.append('%s: formulas missing: %s' % (pid, list((of - rf).elements())))
        for blk in fenced(ob):
            if blk not in rb:
                fails.append('%s: table/text block not copied verbatim' % pid)
        reql = rb.replace(' ', '')
        for ln in eq_lines(ob):
            if ln not in re.sub(r'[>*\\`\s]', '', reql):
                fails.append('%s: formula line changed: %s' % (pid, ln[:60]))
        # glossary (heading lines belong to no paragraph: headings keep their printed wording)
        obody = re.sub(r'^#{1,6} .*$', '', ob, flags=re.M)
        rbody = re.sub(r'^#{1,6} .*$', '', rb, flags=re.M)
        for g in gloss:
            if g.get('check') is False:
                continue
            if g.get('mode') == 'avoid':
                # citations (quoted titles, notes) keep abbreviations as printed: check the paragraph prose only
                prose = strip_quoted(strip_notes(rbody))
                prose = re.sub(r'```.*?```', '', prose, flags=re.S)
                left = [v for v in g['variants'] if v.lower() in prose.lower()]
                if left:
                    warns.append('%s: archaic "%s" still in rewrite (use "%s")' % (pid, left[0], g['rendering']))
                continue
            hit = [v for v in g['variants'] if present(term_pattern(v), obody)]
            if not hit:
                continue
            ok = present(term_pattern(g['rendering'], stem=True), rbody) or any(
                present(term_pattern(a, stem=True), rbody) for a in g.get('also_ok', []))
            if not ok:
                msg = '%s: glossary "%s" -> "%s" not used (original has %s)' % (pid, g['term'], g['rendering'], hit[0])
                (fails if g.get('enforce') else warns).append(msg)
    ow, rw = words(o), words(r)
    ratio = rw / ow if ow else 0
    if ratio < 0.90:
        fails.append('length ratio %.2f (rewrite shorter than original: likely lost content)' % ratio)
    elif not 0.95 <= ratio <= 1.25:
        warns.append('length ratio %.2f outside 0.95-1.25' % ratio)
    return dict(file=name, ok=not fails, ratio=round(ratio, 3), orig_words=ow, rewrite_words=rw,
                failures=fails, warnings=warns)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    res = check(args[0])
    if '--json' in sys.argv:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        print('%s: %s  ratio %.2f (%d -> %d words)' % (res['file'], 'PASS' if res['ok'] else 'FAIL',
                                                     res['ratio'], res['orig_words'], res['rewrite_words']))
        for f in res['failures']:
            print('  FAIL', f)
        for w in res['warnings']:
            print('  warn', w)
    sys.exit(0 if res['ok'] else 1)
