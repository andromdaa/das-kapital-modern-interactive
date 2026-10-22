"""Stage 3: write original/*.md, anchors.json and status.json from work/doc.json."""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 6500          # split a chapter (and then a section) above this many words incl. notes
HLEVEL = dict(part='#', chapter='##', section='###', sub1='####', sub2='#####')


def words(s):
    return len(re.findall(r"\S+", s))


def render_para(b):
    k, t = b['kind'], b['text']
    if k == 'table':
        return '```text\n' + t + '\n```'
    if k in ('verse', 'lines'):
        ls = t.split('\n')
        body = '\\\n'.join(ls)
        return '> ' + body.replace('\n', '\n> ') if k == 'verse' else body
    if k == 'quote':
        return '> ' + t
    return t


def render_note(label, paras):
    out = []
    for n, p in enumerate(paras):
        t = p['text']
        if p['kind'] == 'table':
            t = '```text\n' + t + '\n```'
        elif p['kind'] == 'quote':
            t = '> ' + t
        if n == 0:
            out.append('[^%s]: %s' % (label, t))
        else:
            out.append('\n'.join('    ' + x for x in t.split('\n')))
    return '\n\n'.join(out)


def main():
    D = json.load(open(os.path.join(ROOT, 'work/doc.json')))
    odir = os.path.join(ROOT, 'original')
    os.makedirs(odir, exist_ok=True)
    for f in os.listdir(odir):
        os.remove(os.path.join(odir, f))
    anchors = {}
    files = []          # (name, text, meta)
    split_log = []

    # ---------------- front matter
    front = ['# Capital: A Critique of Political Economy', '',
             '<!-- front: title page and contents as printed in the source PDF -->', '']
    fl = D['front']
    toc_start = next(i for i, x in enumerate(fl) if x.startswith('Table of Contents'))
    front += ['## Title page', '']
    front += [x + '\\' if x else '' for x in fl[:toc_start] if x]
    front[-1] = front[-1].rstrip('\\')
    front += ['', '## Table of Contents', '']
    toc = []
    for x in fl[toc_start + 1:]:
        if not x:
            continue
        if toc and not re.search(r'\.{3,}\s*\d+$|\s\d+$', toc[-1]):
            toc[-1] += ' ' + x
        else:
            toc.append(x)
    for x in toc:
        x = re.sub(r'\s*\.{3,}\s*', ' … ', x)
        ind = '  ' if x.startswith('Section') else ''
        front.append(ind + '- ' + x)
    front += ['']
    files.append(('00-front.md', '\n'.join(front) + '\n', dict(chapter=0, kind='front')))

    # ---------------- chapters
    containers = D['chapters']
    pending_part = None
    for c in containers:
        if c['kind'] == 'part':
            pending_part = c
            continue
        num = c['num']
        cid = 'ch%02d' % num
        # units of text: list of items (heading / para) in order, with ids
        items = []
        if pending_part:
            items.append(dict(type='heading', level='part', text=pending_part['title'], markers=[]))
            pidx = 0
            for b in pending_part['blocks']:
                if b['type'] == 'heading':
                    items.append(b); continue
                pidx += 1
                items.append(dict(b, id='pt%d-p%03d' % (pending_part['num'], pidx), notes_src=pending_part))
            pending_part = None
        items.append(dict(type='heading', level='chapter', text=c['title'], markers=c['heading_markers']))
        pidx = 0
        for b in c['blocks']:
            if b['type'] == 'heading':
                items.append(b); continue
            pidx += 1
            items.append(dict(b, id='%s-p%03d' % (cid, pidx), notes_src=c))
        # attach notes: each label to first paragraph citing it (heading markers -> next paragraph)
        carried = []
        seen = set()
        for it in items:
            if it['type'] == 'heading':
                carried += it.get('markers', [])
                continue
            labs = carried + it['markers']
            carried = []
            it['note_labels'] = [l for l in labs if not (l in seen or seen.add(l))]
        for it in items:
            if it['type'] == 'para':
                src = it['notes_src']
                it['words'] = words(it['text']) + sum(words(p['text']) for l in it['note_labels']
                                                      for p in src['notes'].get(l, []))
        total = sum(it.get('words', 0) for it in items)
        # ---------------- split into units
        units = []
        if total <= LIMIT:
            units.append((cid, items))
        else:
            # split at section headings
            secs = []
            cur = []
            for it in items:
                if it['type'] == 'heading' and it['level'] == 'section' and any(x['type'] == 'para' for x in cur):
                    secs.append(cur); cur = []
                cur.append(it)
            secs.append(cur)
            if len(secs) == 1:
                units += [('%s%s' % (cid, suf), part) for suf, part in split_long(secs[0], cid, split_log, '')]
            else:
                for n, sec in enumerate(secs, 1):
                    name = '%s-s%d' % (cid, n)
                    sw = sum(it.get('words', 0) for it in sec)
                    if sw <= LIMIT:
                        units.append((name, sec))
                    else:
                        units += [('%s%s' % (name, suf), part) for suf, part in split_long(sec, name, split_log, '')]
        for name, its in units:
            fname = name + '.md'
            out = []
            sect = None
            for it in its:
                if it['type'] == 'heading':
                    marks = ''.join('[^%s]' % m for m in it.get('markers', []))
                    out.append('%s %s%s' % (HLEVEL[it['level']], strip_marks(it['text']), marks))
                    out.append('')
                    if it['level'] == 'section':
                        sect = strip_marks(it['text'])
                    continue
                out.append('<!-- %s -->' % it['id'])
                out.append(render_para(it))
                out.append('')
                src = it['notes_src']
                for l in it['note_labels']:
                    out.append(render_note(l, src['notes'][l]))
                    out.append('')
                anchors[it['id']] = dict(chapter=num, file=fname, section=sect,
                                         index=int(it['id'].split('-p')[1]),
                                         kind=it['kind'], footnotes=it['note_labels'], pdf_page=it['page'])
            files.append((fname, '\n'.join(out).rstrip() + '\n', dict(chapter=num, kind='chapter')))

    status = {}
    for fname, text, meta in files:
        open(os.path.join(odir, fname), 'w').write(text)
        status[fname] = dict(state='pending', chapter=meta['chapter'], words=words(re.sub(r'<!--.*?-->', '', text)))
    json.dump(anchors, open(os.path.join(ROOT, 'anchors.json'), 'w'), indent=1, ensure_ascii=False)
    sp = os.path.join(ROOT, 'status.json')
    old = json.load(open(sp)) if os.path.exists(sp) else {}
    for k, v in status.items():
        if k in old and old[k].get('state') != 'pending':
            v['state'] = old[k]['state']
    json.dump(dict(units=status, splits=split_log), open(sp, 'w'), indent=1)
    print(len(files), 'files', len(anchors), 'paragraphs')
    for s in split_log:
        print(s)


def strip_marks(t):
    return re.sub(r'\[\^[^\]]+\]', '', t).strip()


def split_long(items, name, log, _):
    """Split a too-long run of items: first at sub-section headings (A., B., ...), merging small
    neighbours; any piece still too long is split in balanced parts at paragraph boundaries."""
    groups = []
    cur = []
    for it in items:
        if it['type'] == 'heading' and it['level'] == 'sub1' and any(x['type'] == 'para' for x in cur):
            groups.append(cur); cur = []
        cur.append(it)
    groups.append(cur)
    gw = lambda g: sum(x.get('words', 0) for x in g)
    merged = []
    for g in groups:
        if merged and gw(merged[-1]) + gw(g) <= 6000:
            merged[-1] = merged[-1] + g
        else:
            merged.append(g)
    # a short lead-in (e.g. a section's opening paragraphs) travels with the next group
    k = 0
    while k < len(merged) - 1:
        if gw(merged[k]) < 1000:
            merged[k:k + 2] = [merged[k] + merged[k + 1]]
        else:
            k += 1
    pieces = []
    for g in merged:
        if gw(g) <= LIMIT:
            pieces.append((g, 'sub-section heading'))
        else:
            pieces += [(p, 'paragraph boundary') for p in split_paras(g)]
    parts = []
    for k, (p, how) in enumerate(pieces):
        suf = chr(ord('a') + k)
        first = next(x for x in p if x['type'] == 'para')
        last = [x for x in p if x['type'] == 'para'][-1]
        log.append('%s%s.md: %s..%s (%d words), starts at %s' %
                   (name, suf, first['id'], last['id'], gw(p),
                    'the section start' if k == 0 else
                    ('a %s heading' % ('sub-section' if p[0]['level'] == 'sub1' else 'sub-sub-section'))
                    if p[0]['type'] == 'heading' else 'a paragraph boundary'))
        parts.append((suf, p))
    return parts


def split_paras(items):
    """Balanced split at paragraph boundaries, never right after a lead-in ending in ':' or a dash."""
    total = sum(it.get('words', 0) for it in items)
    n = math.ceil(total / 6000)
    cum = []
    acc = 0
    for it in items:
        acc += it.get('words', 0)
        cum.append(acc)
    cuts = []
    for k in range(1, n):
        target = total * k / n
        best = None
        for i in range(1, len(items)):
            it, prev = items[i], items[i - 1]
            if prev['type'] == 'heading':
                continue
            if it['type'] == 'para' and prev['type'] == 'para' and prev['text'].rstrip().endswith((':', '–', '—')):
                continue
            d = abs(cum[i - 1] - target)
            if it['type'] == 'heading':
                d *= 0.5      # prefer sub-heading boundaries
            if best is None or d < best[0]:
                best = (d, i)
        cuts.append(best[1])
    parts = []
    prev = 0
    for c in cuts + [len(items)]:
        parts.append(items[prev:c])
        prev = c
    return parts


if __name__ == '__main__':
    main()
