"""Build per-unit context for a rewriter: previous unit's original tail (~500 words) and which §7 concept
terms already appeared in earlier files of the same chapter (so they need no new explanation).
Usage: python3 scripts/unit_context.py ch10-s3.md  -> writes work/context/ch10-s3.md"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPTS = {  # concept-list term -> regex over the ORIGINAL wording
    'commodity': r'commodit', 'use-value': r'use[- ]?value|value in use', 'exchange-value': r'exchange[- ]?value',
    'value': r'\bvalues?\b', 'magnitude of value': r'magnitude of value', 'socially necessary labor-time': r'socially necessary',
    'useful labor / concrete labor': r'useful labour|concrete labour', 'abstract human labor': r'labour in the abstract|abstract (human )?labour',
    'simple (average) labor': r'simple labour|average labour', 'form of value': r'form of value|value[- ]form',
    'relative form of value / equivalent form': r'relative form|equivalent form', 'universal equivalent': r'universal equivalent',
    'money form': r'money[- ]form', 'price': r'\bprices?\b', 'fetishism of commodities': r'fetish',
    'circulation (of commodities)': r'circulation', 'metamorphosis': r'metamorphos', 'C–M–C': r'C[–-]M[–-]C',
    'M–C–M′': r"M[–-]C[–-]M", 'measure of value': r'measure of value', 'standard of price': r'standard of price',
    'medium of circulation': r'medium of circulation', 'hoard': r'\bhoard', 'means of payment': r'means of payment',
    'world money': r'universal money|world.money', 'capital': r'\bcapital\b', 'labor-power': r'labour[- ]power',
    'value of labor-power': r'value of labour[- ]power', 'means of subsistence': r'means of subsistence',
    'means of production': r'means of production', 'labor process': r'labour[- ]process', 'surplus-value': r'surplus[- ]value',
    'necessary labor (-time)': r'necessary labour', 'surplus labor (-time)': r'surplus[- ]labour', 'constant capital': r'constant capital',
    'variable capital': r'variable capital', 'rate of surplus-value': r'rate of surplus', 'absolute surplus-value': r'absolute surplus',
    'relative surplus-value': r'relative surplus[- ]value', 'working day': r'working[- ]?day', 'value-product': r'value[- ]product',
    'productivity of labor': r'productiveness of labour|productivity of labour', 'intensity of labor': r'intensity of labour|intensification',
    'dead labor / living labor': r'dead labour|living labour', 'cooperation': r'co-operation', 'division of labor (in manufacture)': r'division of labour',
    'manufacture': r'\bmanufacture\b', 'detail worker': r'detail labourer', 'collective worker': r'collective labourer',
    'modern industry': r'modern industry', 'factory system': r'factory system', 'wages': r'\bwages?\b', 'time wages / piece wages': r'time[- ]wage|piece[- ]wage',
    'accumulation of capital': r'accumulation', 'simple reproduction': r'simple reproduction', 'composition of capital': r'composition of capital',
    'concentration of capital': r'concentration', 'centralization of capital': r'centralis', 'relative surplus population / industrial reserve army': r'surplus[- ]population|reserve army',
    'pauperism': r'pauperism', 'primitive accumulation': r'primitive accumulation', 'expropriation': r'expropriat',
    'political economy': r'political economy', 'classical political economy': r'classical', 'vulgar economics': r'vulgar econom',
    'bourgeois': r'bourgeois', 'proletariat': r'proletari', 'corvée': r'corvée', 'relay system': r'relay', 'truck system': r'truck',
}


def order(f):
    m = re.match(r'ch(\d+)(?:-s(\d+))?([a-z]?)\.md', f)
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3)) if m else (0, 0, '')


def main(name):
    files = sorted([f for f in os.listdir(os.path.join(ROOT, 'original')) if f.startswith('ch')], key=order)
    i = files.index(name)
    ch = order(name)[0]
    prev = files[i - 1] if i > 0 else None
    out = ['# Context for %s' % name, '']
    if prev:
        words = re.sub(r'<!--.*?-->', '', open(os.path.join(ROOT, 'original', prev)).read()).split()
        out += ['## Last ~500 words of the previous file\'s ORIGINAL (%s), for continuity only — do not rewrite it' % prev, '',
                '```', ' '.join(words[-500:]), '```', '']
    earlier = [f for f in files[:i] if order(f)[0] == ch]
    cur = open(os.path.join(ROOT, 'original', name)).read()
    seen, new = [], []
    etext = ' '.join(open(os.path.join(ROOT, 'original', f)).read() for f in earlier)
    for term, rx in CONCEPTS.items():
        if not re.search(rx, cur, re.I):
            continue
        (seen if earlier and re.search(rx, etext, re.I) else new).append(term)
    out += ['## Concept-list terms (style bible §7) in this file', '',
            'Earlier files of this chapter: %s' % (', '.join(earlier) or 'none — this is the first file of the chapter'), '',
            '- **Already appeared earlier in this chapter (no new explanation needed):** %s' % (', '.join(seen) or 'none'),
            '- **First appearance in this chapter is in THIS file (explain at first use, §7 wording, unless Marx is defining it himself right there):** %s' % (', '.join(new) or 'none'), '']
    os.makedirs(os.path.join(ROOT, 'work', 'context'), exist_ok=True)
    open(os.path.join(ROOT, 'work', 'context', name), 'w').write('\n'.join(out))
    print('work/context/' + name, 'seen', len(seen), 'new', len(new))


if __name__ == '__main__':
    for n in sys.argv[1:]:
        main(n)
