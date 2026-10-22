"""Phase 6: assemble modern-vol-1.md from 00-front.md and rewrite/*.md in book order.

Footnote labels restart in every chapter, so in the single combined file each label is
prefixed with its chapter ([^12] in ch10 -> [^10.12]; [^*1] -> [^10.*1]); paragraph ID comments are kept.
Prints word counts against the original.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def order(f):
    m = re.match(r'ch(\d+)(?:-s(\d+))?([a-z]?)\.md', f)
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3))


def words(s):
    return len(re.sub(r'<!--.*?-->', '', s).split())


def main():
    files = sorted([f for f in os.listdir(os.path.join(ROOT, 'rewrite')) if f.startswith('ch')], key=order)
    front = open(os.path.join(ROOT, 'original', '00-front.md')).read().rstrip()
    out = [front, '']
    ow = words(front)
    rw = ow
    for f in files:
        ch = order(f)[0]
        t = open(os.path.join(ROOT, 'rewrite', f)).read().rstrip()
        t = re.sub(r'\[\^([^\]]+)\]', lambda m: '[^%d.%s]' % (ch, m.group(1)), t)
        out += [t, '']
        ow += words(open(os.path.join(ROOT, 'original', f)).read())
        rw += words(t)
    text = '\n'.join(out) + '\n'
    # sanity: footnote definitions unique and every marker defined
    defs = re.findall(r'^\[\^([^\]]+)\]:', text, re.M)
    refs = set(re.findall(r'\[\^([^\]]+)\](?!:)', re.sub(r'^\[\^[^\]]+\]:', '', text, flags=re.M)))
    dup = {d for d in defs if defs.count(d) > 1}
    missing = refs - set(defs)
    open(os.path.join(ROOT, 'modern-vol-1.md'), 'w').write(text)
    print('units:', len(files))
    print('original words: %d  rewrite words: %d  ratio: %.3f' % (ow, rw, rw / ow))
    print('footnotes:', len(defs), 'duplicates:', len(dup), 'undefined markers:', len(missing))
    print('paragraph IDs:', len(re.findall(r'<!-- (?:ch\d\d|pt\d)-p\d{3} -->', text)))


if __name__ == '__main__':
    main()
