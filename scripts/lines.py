"""Stage 1: parse pdftohtml -xml output into positioned lines.

Each line: page, top, bottom, left, right, size (dominant font size), kind flags,
and a list of segments (text, size, italic, bold, sup).
"""
import html
import re
import sys
import json

TEXT_RE = re.compile(r'<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*?)</text>')
FONT_RE = re.compile(r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)"')
PAGE_RE = re.compile(r'<page number="(\d+)"')


def parse_inline(raw, base_italic, base_bold):
    """Split the inner markup of a <text> element into (text, italic, bold) runs."""
    runs = []
    italic, bold = 0, 0
    pos = 0
    for m in re.finditer(r'</?[ib]>', raw):
        if m.start() > pos:
            runs.append((html.unescape(raw[pos:m.start()]), base_italic or italic > 0, base_bold or bold > 0))
        tag = m.group(0)
        if tag == '<i>': italic += 1
        elif tag == '</i>': italic -= 1
        elif tag == '<b>': bold += 1
        elif tag == '</b>': bold -= 1
        pos = m.end()
    if pos < len(raw):
        runs.append((html.unescape(raw[pos:]), base_italic or italic > 0, base_bold or bold > 0))
    return runs


SYMBOL_GREEK = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'αβχδεφγηιϕκλμνοπθρστυϖωξψζΑΒΧΔΕΦΓΗΙϑΚΛΜΝΟΠΘΡΣΤΥςΩΞΨΖ'))


def symbol_to_greek(text):
    """Symbol-font text arrives as Private Use Area code points (U+F0xx); map to Greek letters.
    Accents and breathings are not recoverable from the Symbol font."""
    out = []
    for ch in text:
        c = ord(ch)
        if 0xF020 <= c <= 0xF0FF:
            ch = chr(c - 0xF000)
        out.append(SYMBOL_GREEK.get(ch, ch))
    return ''.join(out)


def load(path):
    xml = open(path, encoding='utf-8').read()
    fonts = {}
    elems = []
    page = 0
    for line in xml.split('\n'):
        m = PAGE_RE.search(line)
        if m:
            page = int(m.group(1))
        for fm in FONT_RE.finditer(line):
            fonts[fm.group(1)] = (int(fm.group(2)), fm.group(3))
        for tm in TEXT_RE.finditer(line):
            top, left, width, height = map(int, tm.group(1, 2, 3, 4))
            size, fam = fonts[tm.group(5)]
            runs = parse_inline(tm.group(6), 'Italic' in fam, 'Bold' in fam)
            if fam == 'Symbol':
                runs = [(symbol_to_greek(t), i, b) for t, i, b in runs]
            elems.append(dict(page=page, top=top, left=left, width=width, height=height,
                              size=size, fam=fam, runs=runs))
    return elems


def is_sup(e):
    txt = ''.join(r[0] for r in e['runs']).strip()
    return e['size'] <= 12 and e['height'] <= 11 and len(txt) <= 6


def build_lines(elems):
    pages = {}
    for e in elems:
        pages.setdefault(e['page'], []).append(e)
    out = []
    for pno in sorted(pages):
        es = pages[pno]
        # drop running header (page no / chapter label at top ~116) and footer blank
        es = [e for e in es if not (e['top'] < 128 and e['size'] <= 14) and not (e['top'] >= 1050 and not ''.join(r[0] for r in e['runs']).strip())]
        normal = [e for e in es if not is_sup(e)]
        sups = [e for e in es if is_sup(e)]
        # cluster normal elements by baseline
        normal.sort(key=lambda e: (e['top'] + e['height'], e['left']))
        lines = []
        for e in normal:
            base = e['top'] + e['height']
            for ln in lines:
                if abs(ln['base'] - base) <= 4 and not any(e['left'] < x['left'] + x['width'] - 2 and e['left'] + e['width'] > x['left'] + 2
                                                           for x in ln['elems']):
                    ln['elems'].append(e)
                    ln['left'] = min(ln['left'], e['left'])
                    ln['right'] = max(ln['right'], e['left'] + e['width'])
                    break
            else:
                lines.append(dict(base=base, top=e['top'], left=e['left'], right=e['left'] + e['width'], elems=[e]))
        # attach superscripts to nearest line whose vertical span contains them
        for s in sups:
            best = None
            for ln in lines:
                lt = min(x['top'] for x in ln['elems'])
                if lt - 6 <= s['top'] <= ln['base']:
                    d = abs(s['top'] - lt)
                    if best is None or d < best[0]:
                        best = (d, ln)
            if best is None:
                lines.append(dict(base=s['top'] + s['height'], top=s['top'], left=s['left'],
                                  right=s['left'] + s['width'], elems=[s], suponly=True))
            else:
                ln = best[1]
                ln['elems'].append(s)
                ln['left'] = min(ln['left'], s['left'])
                ln['right'] = max(ln['right'], s['left'] + s['width'])
        lines.sort(key=lambda l: (l['base'], l['left']))
        for ln in lines:
            ln['elems'].sort(key=lambda e: e['left'])
            segs = []
            sizes = {}
            text_tops = [x['top'] for x in ln['elems'] if not is_sup(x)]
            ltop = min(text_tops) if text_tops else ln['top']
            lbase = ln['base']
            for e in ln['elems']:
                sup = is_sup(e)
                # small digits sitting low on the line are subscripts (e.g. C4H8O2), not note markers
                sub = sup and text_tops and e['top'] + e['height'] >= lbase - 1 and e['top'] > ltop + 4
                for text, it, bd in e['runs']:
                    segs.append(dict(t=re.sub(r'<[^>]+>', '', text), it=it, b=bd, sup=sup and not sub, sub=bool(sub),
                                     size=e['size'], left=e['left'], width=e['width'], fam=e['fam']))
                    if not sup and text.strip():
                        sizes[e['size']] = sizes.get(e['size'], 0) + len(text.strip())
            size = max(sizes, key=sizes.get) if sizes else 0
            fams = {e['fam'] for e in ln['elems'] if not is_sup(e) and ''.join(r[0] for r in e['runs']).strip()}
            out.append(dict(page=pno, top=ln['top'], base=ln['base'], left=ln['left'], right=ln['right'],
                            size=size, fams=sorted(fams), segs=segs,
                            nelems=len([e for e in ln['elems'] if not is_sup(e) and ''.join(r[0] for r in e['runs']).strip()])))
    return out


def plain(line):
    return ''.join(s['t'] for s in line['segs'])


if __name__ == '__main__':
    lines = build_lines(load(sys.argv[1]))
    json.dump(lines, open(sys.argv[2], 'w'), ensure_ascii=False)
    print(len(lines), 'lines')
