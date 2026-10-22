"""Stage 2: turn positioned lines (work/lines.json) into a structured document (work/doc.json).

Structure: front-matter lines, then chapters. Each chapter holds an ordered list of blocks
(heading / para) and a dict of endnotes keyed by label ("1", "26a", "*1").
"""
import json
import re
import sys

BODY_LEFT = (130, 142)
QUOTE_LEFT = (175, 200)
GAP_PARA = 21.5          # baseline delta above this starts a new paragraph (body)
FULL_RIGHT = 772         # a body line reaching this is justified, i.e. the paragraph continues
TERMINAL = tuple('.!?:”"’)];')


def text_of(line):
    return ''.join(s['t'] for s in line['segs'])


def fam(line):
    return line['fams'][0] if line['fams'] else ''


def is_blank(line):
    return not text_of(line).strip()


def is_separator(line):
    return is_blank(line) and line['right'] - line['left'] > 150


def mark_heading_sups(segs, size):
    """In headings, a trailing run of small digits is a note marker, not text."""
    out = []
    for s in segs:
        if not s['sup'] and re.fullmatch(r'\s*\d+[a-z]?\s*', s['t']) and s.get('size', 99) <= size * 0.7:
            s = dict(s, sup=True)
        out.append(s)
    return out


def heading_level(line):
    f, size = fam(line), line['size']
    if size >= 30 and line['page'] > 5 and ('Bold' in f or 'Century' in f):
        return 'part'
    if 'Bookman' in f and size >= 20:
        return 'chapter'
    if 'Garamond' in f and 'Bold' in f and size == 24:
        return 'section'
    if f == 'Arial' and size == 21:
        return 'sub1'
    if f.startswith('Arial,Bold') and size == 18:
        return 'sub2'
    return None


def gap_line(line):
    """True if the line has a wide horizontal gap between pieces of text (table / diagram)."""
    segs = [s for s in line['segs'] if s['t'].strip() and not s['sup']]
    pieces = {}
    for s in segs:
        pieces.setdefault(s['left'], s)
    xs = sorted(pieces.values(), key=lambda s: s['left'])
    for a, b in zip(xs, xs[1:]):
        if b['left'] - (a['left'] + a['width']) > 25:
            return True
    return False


def starts_note(line):
    segs = merge_sups([s for s in line['segs'] if s['t'].strip()])
    return bool(segs) and segs[0]['sup'] and line['left'] <= 142 and \
        bool(re.fullmatch(r'(\d+[a-z]?|\*+|1\\7)', segs[0]['t'].strip()))


def in_rng(x, r):
    return r[0] <= x <= r[1]


# ---------------------------------------------------------------- inline rendering

def merge_sups(segs):
    """Adjacent superscript pieces belong to one label (e.g. '4 ' + '3b' -> '43b')."""
    out = []
    for s in segs:
        if s['sup'] and out and out[-1]['sup'] and s['t'].strip():
            out[-1] = dict(out[-1], t=out[-1]['t'].strip() + s['t'].strip())
        else:
            out.append(dict(s))
    return out


def render_segments(segs, ctx):
    """Render segments to markdown. ctx collects footnote markers: list of labels in order."""
    segs = merge_sups(segs)
    out = []  # list of (text, italic, bold) with markers already rendered
    for s in segs:
        t = s['t']
        if s.get('sub'):
            out.append(('<sub>' + t.strip() + '</sub>', False, False, True))
            continue
        if s['sup']:
            tt = t.strip()
            if not tt:
                continue
            if re.fullmatch(r'\d+[a-z]?', tt):
                ctx['markers'].append(tt)
                out.append(('[^' + tt + ']', False, False, True))
            elif re.fullmatch(r'\*+', tt):
                ctx['star'] += 1
                lab = '*%d' % ctx['star']
                ctx['markers'].append(lab)
                out.append(('[^' + lab + ']', False, False, True))
            else:
                ctx['odd_sups'].append(tt)
                out.append(('<sup>' + tt + '</sup>', False, False, True))
            continue
        out.append((t, s['it'], s['b'], False))
    return out


def runs_to_md(runs, keep_bold=True):
    """Join (text, italic, bold, atomic) runs, collapsing whitespace and wrapping emphasis."""
    # character-level emphasis then regroup
    chars = []
    for t, it, b, atomic in runs:
        if atomic:
            chars.append((t, it, b))
        else:
            for ch in t:
                chars.append((ch, it, b))
    # regroup into spans
    spans = []
    for ch, it, b in chars:
        key = (it, b and keep_bold)
        if spans and spans[-1][0] == key:
            spans[-1][1].append(ch)
        else:
            spans.append([key, [ch]])
    res = []
    for (it, b), cs in spans:
        txt = ''.join(cs)
        if not (it or b) or not txt.strip():
            res.append(txt)
            continue
        lead = txt[:len(txt) - len(txt.lstrip())]
        trail = txt[len(txt.rstrip()):]
        core = txt.strip()
        mark = ('**' if b else '') + ('*' if it else '')
        res.append(lead + mark + core + mark[::-1] + trail)
    s = ''.join(res)
    s = re.sub(r'[ \t ]+', ' ', s)
    # merge emphasis split across adjacent spans: "*a* *b*" -> "*a b*"
    s = re.sub(r'(?<=\w)\* \*(?=\w)', ' ', s)
    # note markers attach to the preceding word or punctuation (spaces there are layout artifacts)
    s = re.sub(r'(?<=\S)\s+(\[\^[^\]]+\])', r'\1', s)
    return s.strip()


def join_lines(line_runs):
    """Join per-line run lists into one paragraph run list (hyphen-aware)."""
    runs = []
    for i, lr in enumerate(line_runs):
        if i > 0:
            prev = ''.join(r[0] for r in runs).rstrip()
            if prev.endswith('-') and not prev.endswith('--') and not prev.endswith(' -'):
                # real compound hyphen at line end (source has no soft hyphenation): no space
                # strip trailing whitespace from runs
                while runs and not runs[-1][0].strip():
                    runs.pop()
                if runs:
                    t, a, b, c = runs[-1]
                    runs[-1] = (t.rstrip(), a, b, c)
            else:
                runs.append((' ', False, False, False))
        runs.extend(lr)
    return runs


# ---------------------------------------------------------------- main pass

def main(src, dst):
    L = json.load(open(src))
    front = []
    chapters = []
    part = None
    ch = None
    mode = 'front'
    i = 0
    pending_heading = None

    def new_ctx():
        return dict(markers=[], star=0, odd_sups=[])

    while i < len(L):
        ln = L[i]
        hl = heading_level(ln)
        # a lone small number printed just before a heading is that heading's note marker
        if ln['page'] > 5 and re.fullmatch(r'\s*\d+[a-z]?\s*', text_of(ln)) and i + 1 < len(L) \
                and heading_level(L[i + 1]) and L[i + 1]['page'] == ln['page'] \
                and abs(L[i + 1]['base'] - ln['base']) < 25 and L[i + 1]['size'] > ln['size']:
            L[i + 1] = dict(L[i + 1], segs=L[i + 1]['segs'] + [dict(s, sup=True) for s in ln['segs']])
            i += 1
            continue
        if ln['page'] <= 5:
            front.append(text_of(ln).strip())
            i += 1
            continue
        if hl == 'part':
            txt = [text_of(ln).strip()]
            j = i + 1
            while j < len(L) and heading_level(L[j]) == 'part' and L[j]['page'] == ln['page']:
                txt.append(text_of(L[j]).strip()); j += 1
            part = re.sub(r'\s+', ' ', ' '.join(txt))
            # a Part may open with its own introduction (Part 7 does); keep it in a part container
            pnum = int(re.match(r'Part (\d+)', part).group(1))
            ch = dict(kind='part', num=pnum, title=part, part=part, blocks=[], notes={}, note_order=[],
                      ctx=new_ctx(), notes_raw=[], pages=[ln['page'], ln['page']], heading_markers=[])
            chapters.append(ch)
            mode = 'body'
            i = j
            continue
        if hl == 'chapter':
            j = i
            segs = []
            while j < len(L) and heading_level(L[j]) == 'chapter' and L[j]['page'] == ln['page']:
                if segs:
                    segs.append(dict(t=' ', it=False, b=False, sup=False))
                segs.extend(L[j]['segs']); j += 1
            ctx = new_ctx()
            title = runs_to_md(render_segments(mark_heading_sups(segs, ln['size']), ctx), keep_bold=False)
            m = re.match(r'Chapter (\d+)', title)
            num = int(m.group(1))
            ch = dict(kind='chapter', num=num, title=title, part=None, blocks=[], notes={}, note_order=[],
                      ctx=new_ctx(), notes_raw=[], pages=[ln['page'], ln['page']], heading_markers=ctx['markers'])
            ch['ctx']['star'] = ctx['star']
            if part:
                ch['part'] = part
                part = None
            chapters.append(ch)
            mode = 'body'
            i = j
            continue
        if ch is None:
            i += 1
            continue
        ch['pages'][1] = ln['page']
        if mode == 'body' and is_separator(ln):
            j = i + 1
            while j < len(L) and is_blank(L[j]):
                j += 1
            if j < len(L) and starts_note(L[j]):
                mode = 'notes'
            i += 1
            continue
        if mode == 'notes':
            if not is_blank(ln):
                ch['notes_raw'].append(ln)
            i += 1
            continue
        # ---- body mode
        if is_blank(ln):
            i += 1
            continue
        if hl in ('section', 'sub1', 'sub2'):
            j = i
            segs = []
            while j < len(L) and heading_level(L[j]) == hl and (j == i or L[j]['base'] - L[j - 1]['base'] < 30) \
                    and L[j]['page'] == ln['page']:
                if segs:
                    segs.append(dict(t=' ', it=False, b=False, sup=False))
                segs.extend(L[j]['segs']); j += 1
            # sub2 headings sometimes continue with a BoldItalic line
            before = len(ch['ctx']['markers'])
            title = runs_to_md(render_segments(mark_heading_sups(segs, ln['size']), ch['ctx']), keep_bold=False)
            title = re.sub(r'\s+', ' ', title)
            ch['blocks'].append(dict(type='heading', level=hl, text=title, page=ln['page'],
                                     markers=ch['ctx']['markers'][before:]))
            i = j
            continue
        ch['blocks'].append(dict(type='line', line=ln))
        i += 1

    # ---------------- group body lines into paragraphs per chapter
    for ch in chapters:
        ch['blocks'] = group_body(ch)
        ch['notes'], ch['note_order'], ch['note_problems'] = group_notes(ch)
        del ch['notes_raw']
        ch['odd_sups'] = ch['ctx']['odd_sups']
        del ch['ctx']

    json.dump(dict(front=front, chapters=chapters), open(dst, 'w'), ensure_ascii=False, indent=1)
    print('chapters', len(chapters))


def line_kind(ln):
    if gap_line(ln):
        return 'table'
    if ln['left'] > 175 and ln['right'] < 560 and not in_rng(ln['left'], QUOTE_LEFT):
        return 'other'
    if in_rng(ln['left'], BODY_LEFT):
        return 'body'
    if 142 < ln['left'] < 175 and ln['right'] >= 740:
        return 'body'        # first line of a paragraph with a first-line indent
    if 200 < ln['left'] < 240 and ln['right'] >= 700:
        return 'quote'       # first-line indent inside a block quotation
    if in_rng(ln['left'], QUOTE_LEFT):
        return 'quote'
    return 'other'


def group_body(ch):
    items = ch['blocks']
    # mark table regions: seed with gap lines, extend over adjacent non-prose lines
    lines = [b['line'] for b in items if b['type'] == 'line']
    kinds = {id(l): line_kind(l) for l in lines}
    # stacked short indented lines (fractions, formulas, verse) form one block whatever their indent
    def short_ind(l):
        return l['left'] > 140 and l['right'] < 560 and kinds[id(l)] != 'table'
    for k, l in enumerate(lines):
        if not short_ind(l):
            continue
        for nb in (k - 1, k + 1):
            if 0 <= nb < len(lines):
                o = lines[nb]
                if o['page'] == l['page'] and abs(o['base'] - l['base']) <= 25 and short_ind(o):
                    kinds[id(l)] = 'other'
    idx = {id(l): k for k, l in enumerate(lines)}
    table = set(id(l) for l in lines if kinds[id(l)] == 'table')
    changed = True
    while changed:
        changed = False
        for k, l in enumerate(lines):
            if id(l) in table:
                continue
            for nb in (k - 1, k + 1):
                if 0 <= nb < len(lines) and id(lines[nb]) in table:
                    o = lines[nb]
                    near = o['page'] == l['page'] and abs(o['base'] - l['base']) <= 26
                    prose = l['right'] >= 690 and kinds[id(l)] in ('body', 'quote')
                    leadin = text_of(l).rstrip().endswith((':', '–', '—', '-')) and kinds[id(l)] in ('body', 'quote')
                    # the short last line of a prose paragraph stays with its paragraph
                    above = lines[k - 1] if k > 0 else None
                    tail = above is not None and id(above) not in table and above['page'] == l['page'] \
                        and kinds[id(above)] == kinds[id(l)] and kinds[id(l)] in ('body', 'quote') \
                        and above['right'] >= 690 and l['base'] - above['base'] <= GAP_PARA
                    if near and not prose and not leadin and not tail and (kinds[id(l)] == 'other' or l['right'] < 560):
                        table.add(id(l)); changed = True
                        break
    out = []
    cur = None  # dict(kind, lines)

    def flush():
        nonlocal cur
        if cur:
            out.append(finish_para(cur, ch))
        cur = None

    for b in items:
        if b['type'] == 'heading':
            flush()
            out.append(b)
            continue
        l = b['line']
        kind = 'table' if id(l) in table else kinds[id(l)]
        if kind == 'table':
            pass
        if cur is None:
            cur = dict(kind=kind, lines=[l])
            continue
        prev = cur['lines'][-1]
        same_kind = cur['kind'] == kind
        if not same_kind:
            flush(); cur = dict(kind=kind, lines=[l]); continue
        if kind == 'table':
            # tables continue unless a big gap
            if prev['page'] == l['page'] and l['base'] - prev['base'] > 60:
                flush(); cur = dict(kind=kind, lines=[l]); continue
            if prev['page'] != l['page']:
                pass
            cur['lines'].append(l); continue
        indent = (kind == 'body' and l['left'] > 142) or (kind == 'quote' and l['left'] > 200)
        if indent:
            flush(); cur = dict(kind=kind, lines=[l]); continue
        if prev['page'] == l['page']:
            limit = 32 if kind == 'other' else GAP_PARA
            if l['base'] - prev['base'] > limit:
                flush(); cur = dict(kind=kind, lines=[l]); continue
            cur['lines'].append(l); continue
        # page break: continue only if previous line looked justified/unfinished
        ptxt = text_of(prev).rstrip()
        if kind == 'body':
            cont = prev['right'] >= FULL_RIGHT
        elif kind == 'quote':
            cont = prev['right'] >= 700 or (prev['right'] >= 600 and not ptxt.endswith(TERMINAL))
        else:
            cont = False
        if cont:
            cur['lines'].append(l)
            cur.setdefault('page_joins', []).append(l['page'])
        else:
            flush(); cur = dict(kind=kind, lines=[l])
    flush()
    return out


def render_table(lines, ctx):
    rows = []
    for l in lines:
        row = ''
        for sg in merge_sups(sorted(l['segs'], key=lambda x: x['left'])):
            if not sg['t'].strip() and not row:
                continue
            col = max(0, round((sg['left'] - 135) / 6.5))
            if sg['sup'] or sg.get('sub'):
                row += render_segments([sg], ctx)[0][0] if sg['t'].strip() else ''
                continue
            t = re.sub(r'\s+', ' ', sg['t'])
            if len(row.rstrip()) + 1 < col and row.strip():
                row = row.rstrip().ljust(col)
            elif not row:
                row = ' ' * col
            row += t
        rows.append(row.rstrip())
    ind = min((len(r) - len(r.lstrip()) for r in rows if r.strip()), default=0)
    return '\n'.join(r[ind:] for r in rows)


def table_members(lines):
    """Seed with lines that have wide column gaps, then absorb adjacent short lines (wrapped cells)."""
    table = set(k for k, l in enumerate(lines) if gap_line(l))
    changed = True
    while changed:
        changed = False
        for k, l in enumerate(lines):
            if k in table:
                continue
            for nb in (k - 1, k + 1):
                if nb in table and lines[nb]['page'] == l['page'] and abs(lines[nb]['base'] - l['base']) <= 26 \
                        and l['right'] < 560 and not text_of(l).rstrip().endswith((':', '—', '–')):
                    table.add(k); changed = True
                    break
    return table


def finish_para(cur, ch):
    kind = cur['kind']
    lines = cur['lines']
    ctx = ch['ctx']
    before = len(ctx['markers'])
    if kind == 'table':
        text = render_table(lines, ctx)
        return dict(type='para', kind='table', text=text, markers=ctx['markers'][before:],
                    page=lines[0]['page'])
    line_runs = [render_segments(l['segs'], ctx) for l in lines]
    short_block = kind in ('other', 'quote', 'body') and len(lines) > 1 and all(l['right'] < 560 for l in lines)
    if kind == 'other' or short_block:
        # formula / verse style: keep line breaks
        text = '\n'.join(runs_to_md(r) for r in line_runs)
        k = 'verse' if text.lstrip('*').startswith(('“', '‘', '"')) else 'lines'
        if kind == 'body' and short_block or '=' in text:
            k = 'lines'      # formulas and equation lists keep their line breaks but are not quotations
        return dict(type='para', kind=k, text=text, markers=ctx['markers'][before:], page=lines[0]['page'],
                    lefts=sorted({l['left'] for l in lines}))
    text = runs_to_md(join_lines(line_runs))
    return dict(type='para', kind=kind, text=text, markers=ctx['markers'][before:], page=lines[0]['page'],
                page_joins=cur.get('page_joins', []))


def group_notes(ch):
    """Endnotes: a note starts at a line whose first visible segment is a superscript label."""
    notes = {}
    order = []
    problems = []
    star = 0
    cur = None
    for l in ch['notes_raw']:
        if starts_note(l):
            msegs = merge_sups(l['segs'])
            k = next(n for n, s in enumerate(msegs) if s['t'].strip())
            first = msegs[k]
            lab = first['t'].strip()
            if lab.startswith('*'):
                star += 1
                lab = '*%d' % star
            if lab == '1\\7':
                problems.append('note label printed as "1\\7" in source; read as 17')
                lab = '17'
            rest = msegs[k + 1:]
            cur = dict(label=lab, lines=[(l, rest)])
            if lab in notes:
                problems.append('duplicate note label %s' % lab)
            notes[lab] = cur
            order.append(lab)
            continue
        if cur is None:
            problems.append('text before first note on p%d: %s' % (l['page'], text_of(l)[:60]))
            continue
        cur['lines'].append((l, l['segs']))
    out = {}
    for lab, n in notes.items():
        paras = []
        para = []
        prev = None
        ctx = dict(markers=[], star=0, odd_sups=[])
        tmem = table_members([l for l, _ in n['lines']])
        for k, (l, segs) in enumerate(n['lines']):
            l = dict(l, _tab=k in tmem)
            if prev is not None:
                newp = False
                if l['_tab'] != prev['_tab']:
                    newp = True
                elif l['_tab']:
                    para.append((l, segs)); prev = l
                    continue
                if prev['page'] == l['page'] and l['base'] - prev['base'] > GAP_PARA:
                    newp = True
                if in_rng(l['left'], QUOTE_LEFT) != in_rng(prev['left'], QUOTE_LEFT) and prev['page'] == l['page']:
                    newp = True

                if newp:
                    paras.append(para); para = []
            para.append((l, segs))
            prev = l
        paras.append(para)
        rendered = []
        for p in paras:
            if p[0][0]['_tab']:
                rendered.append(dict(kind='table', text=render_table([dict(l, segs=segs) for l, segs in p], ctx)))
                continue
            line_runs = [render_segments(segs, ctx) for l, segs in p]
            q = all(in_rng(l['left'], QUOTE_LEFT) for l, _ in p)
            rendered.append(dict(kind='quote' if q else 'body', text=runs_to_md(join_lines(line_runs))))
        if ctx['markers']:
            problems.append('note %s contains sup markers %s' % (lab, ctx['markers']))
        out[lab] = rendered
    return out, order, problems


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
