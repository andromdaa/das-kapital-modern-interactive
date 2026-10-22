#!/usr/bin/env python3
"""Check the built site in site/public/.

1. Every anchor in parallels/*.json resolves to a paragraph element in the generated chapter page.
2. Every internal link (href="page.html#id") in the generated site points at an existing page and id.
Exits non-zero on any failure.
"""
import glob
import json
import os
import re
import sys
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "public")

ids, paras = {}, {}
for f in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
    text = open(f, encoding="utf-8").read()
    rel = os.path.relpath(f, OUT)
    ids[rel] = set(re.findall(r'\sid="([^"]+)"', text))
    paras[rel] = set(re.findall(r'<div class="para[^"]*" id="([^"]+)"', text))
para_page = {pid: page for page, s in paras.items() for pid in s}

errors = []
n_anchor = 0
for f in sorted(glob.glob(os.path.join(ROOT, "parallels", "*.json"))):
    p = json.load(open(f, encoding="utf-8"))
    for a in p.get("anchors", []):
        n_anchor += 1
        if a not in para_page:
            errors.append(f"{p['id']}: anchor {a} has no paragraph in the built site")

n_links = 0
for page, _ in ids.items():
    text = open(os.path.join(OUT, page), encoding="utf-8").read()
    for href in re.findall(r'href="([^"]+)"', text):
        u = urlsplit(href)
        if u.scheme or href.startswith("//") or u.path.endswith(".css"):
            continue
        n_links += 1
        target = os.path.normpath(os.path.join(os.path.dirname(page), u.path)) if u.path else page
        if target not in ids:
            errors.append(f"{page}: link to missing page {href}")
        elif u.fragment and u.fragment not in ids[target]:
            errors.append(f"{page}: link to missing id {href}")

for e in errors:
    print(e)
print(f"{n_anchor} parallel anchors and {n_links} internal links checked; {len(errors)} problem(s)")
sys.exit(1 if errors else 0)
