#!/usr/bin/env python3
"""Build the static reading site from the project's data files.

Inputs (all relative to the project root, any of them may be missing or partial):
  rewrite/*.md          plain-language text, one file per chapter or section
  original/*.md         the 1887 English text, same file names
  anchors.json          paragraph id -> chapter/file/section metadata
  themes-index.json     themes and claims (themes-index.md is used if the JSON is missing)
  parallels/*.json      present-day parallels, one per claim

Output: site/public/, a plain static site with no backend.

Missing files are skipped with a warning, so the build works at any stage of the project.
Run `python3 site/build.py --help` for options.
"""

import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import shutil
import sys
from collections import OrderedDict, defaultdict

try:
    from markdown_it import MarkdownIt
except ImportError:  # pragma: no cover
    sys.exit("markdown-it-py is required: pip install markdown-it-py")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
SITE_TITLE = "Capital, Volume I — a plain-language reader"

VERDICTS = OrderedDict([
    ("holds", "Holds"),
    ("partial", "Partly holds"),
    ("missed", "Missed"),
    ("too_vague_to_judge", "Too vague to judge"),
])
SPECIFICITY = OrderedDict([
    ("concrete_forecast", "Concrete forecast"),
    ("general_warning", "General warning"),
    ("described_pattern", "Described pattern"),
])
KINDS = OrderedDict([
    ("forecast", "Forecast"),
    ("implicit_argument", "Implicit argument"),
    ("theme", "Theme"),
])

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print(f"warning: {msg}", file=sys.stderr)


def esc(s):
    return html.escape(s or "", quote=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


MD = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")

# --------------------------------------------------------------------------- parsing

ANCHOR_RE = re.compile(r"^<!--\s*([a-z0-9]+-p\d+)\s*-->\s*$")
COMMENT_RE = re.compile(r"^<!--.*-->\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FNDEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s?(.*)$")
FNREF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")
FENCE_RE = re.compile(r"^(```|~~~)")


def parse_file(path):
    """Split a text file into an ordered list of blocks.

    Block kinds: heading {level, text}, para {id, md}, loose {md}, fn {id, md}.
    """
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    blocks = []
    cur = None  # the block currently collecting lines
    in_fence = False

    def close():
        nonlocal cur
        if cur is not None:
            cur["md"] = "\n".join(cur["lines"]).strip("\n")
            del cur["lines"]
            if cur["kind"] != "loose" or cur["md"].strip():
                blocks.append(cur)
        cur = None

    for line in lines:
        if in_fence:
            cur["lines"].append(line)
            if FENCE_RE.match(line.strip()):
                in_fence = False
            continue
        m = ANCHOR_RE.match(line)
        if m:
            close()
            cur = {"kind": "para", "id": m.group(1), "lines": []}
            continue
        if COMMENT_RE.match(line):
            continue
        m = HEADING_RE.match(line)
        if m and not (cur and cur["kind"] == "fn" and line.startswith("    ")):
            close()
            blocks.append({"kind": "heading", "level": len(m.group(1)), "text": m.group(2)})
            continue
        m = FNDEF_RE.match(line)
        if m:
            close()
            cur = {"kind": "fn", "id": m.group(1), "lines": [m.group(2)]}
            continue
        if cur is None:
            if not line.strip():
                continue
            cur = {"kind": "loose", "lines": []}
        elif cur["kind"] == "fn" and line.strip() and not line.startswith(("    ", "\t")) \
                and cur["lines"] and not cur["lines"][-1].strip():
            # a non-indented line after a blank line ends the footnote
            close()
            cur = {"kind": "loose", "lines": []}
        if FENCE_RE.match(line.strip()):
            in_fence = True
        cur["lines"].append(line[4:] if cur["kind"] == "fn" and line.startswith("    ") else line)
    close()
    return blocks


def file_sort_key(name):
    """ch10-s5a.md -> (10, 5, 'a'); 00-front.md first."""
    m = re.match(r"ch(\d+)(?:-s(\d+))?([a-z]?)", name)
    if not m:
        return (-1, 0, "")
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3))


def chapter_of(name):
    m = re.match(r"ch(\d+)", name)
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------- rendering helpers


def render_md(md_text, fn_prefix):
    """Render markdown, turning [^x] references into links to per-paragraph notes."""
    def ref(m):
        fid = m.group(1)
        target = f"fn-{fn_prefix}-{slug(fid) or 'x'}"
        return (f'<sup class="fnref"><a href="#{target}" data-fn="{target}" '
                f'aria-label="Note {esc(fid)}">{esc(fid)}</a></sup>')
    out = MD.render(FNREF_RE.sub(ref, md_text))
    return out


def render_inline(md_text):
    return MD.renderInline(md_text)


def heading_plain(text):
    return re.sub(r"[*_`]", "", text)


def page(title, body, depth, active="", extra_head="", scripts=(), data=None, body_class=""):
    up = "../" * depth
    nav = [("index.html", "Contents", "contents"), ("themes.html", "Themes & claims", "themes"),
           ("today.html", "Start from today", "today"), ("about.html", "About", "about")]
    nav_html = "".join(
        f'<li><a href="{up}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for href, label, key in nav)
    data_html = ""
    if data is not None:
        data_html = ('<script type="application/json" id="site-data">'
                     + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    script_html = "".join(f'<script src="{up}assets/{s}" defer></script>' for s in scripts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="A plain-language rewrite of Marx's Capital, Volume I, with the 1887 English text alongside and dated present-day parallels.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
<script>(function(){{try{{var r=document.documentElement,s=localStorage.getItem("capital.textSize"),f=localStorage.getItem("capital.font");if(s)r.style.setProperty("--text-size",s+"px");if(f)r.dataset.font=f;}}catch(e){{}}}})();</script>
{extra_head}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <a class="brand" href="{up}index.html">Capital, Vol. I <span>plain-language reader</span></a>
  <nav aria-label="Site"><ul>{nav_html}</ul></nav>
</header>
{body}
<footer class="site-footer">
  <p>The main text is a plain-language rewrite, not Marx's wording. The 1887 Moore–Aveling English translation is available on every page with the “Original” toggle. <a href="{up}about.html">How the rewrite was made</a>.</p>
  <p>No tracking and no cookies. Fonts load from Google Fonts; your text size and font choice are stored only in your browser.</p>
</footer>
{data_html}
{script_html}
</body>
</html>
"""


def verdict_badge(v):
    label = VERDICTS.get(v, "Not yet judged")
    return f'<span class="verdict" data-verdict="{esc(v or "none")}">{esc(label)}</span>'


# --------------------------------------------------------------------------- data loading


def load_json(path, default):
    if not os.path.exists(path):
        warn(f"{os.path.relpath(path, ROOT)} not found; using empty data")
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        warn(f"{os.path.relpath(path, ROOT)} is not valid JSON ({e}); skipped")
        return default


def parse_themes_md(path):
    """Fallback reader for themes-index.md when the JSON version is missing."""
    items = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for chunk in re.split(r"^### ", text, flags=re.M)[1:]:
        head, _, rest = chunk.partition("\n")
        m = re.match(r"([TO]\d+)\s*·\s*(.*)", head)
        if not m or not m.group(1).startswith("T"):
            continue
        meta = re.search(r"`(\w+)`.*?verdict:\s*`?(\w+)?", rest)
        anchors = re.search(r"^Anchors:\s*(.*)$", rest, re.M)
        lines = [l for l in rest.split("\n") if l.strip()]
        items.append({
            "id": m.group(1), "title": m.group(2).strip(), "kind": "",
            "specificity": meta.group(1) if meta else "",
            "verdict": (meta.group(2) if meta and meta.group(2) not in ("none", None) else None),
            "claim": lines[1].strip() if len(lines) > 1 else "",
            "anchors": [a.strip() for a in anchors.group(1).split(",")] if anchors else [],
            "quote": "", "note": "",
        })
    return {"items": items, "opponent_claims": []}


def load_themes():
    jpath = os.path.join(ROOT, "themes-index.json")
    mpath = os.path.join(ROOT, "themes-index.md")
    if os.path.exists(jpath):
        return load_json(jpath, {"items": [], "opponent_claims": []})
    if os.path.exists(mpath):
        warn("themes-index.json not found; reading themes-index.md")
        return parse_themes_md(mpath)
    warn("no themes index found; themes view will be empty")
    return {"items": [], "opponent_claims": []}


def load_parallels(stub):
    files = sorted(glob.glob(os.path.join(ROOT, "parallels", "*.json")))
    out = {}
    for f in files:
        d = load_json(f, None)
        if not d or "id" not in d:
            warn(f"{os.path.relpath(f, ROOT)} has no id; skipped")
            continue
        missing = [k for k in ("anchors", "verdict", "parallel", "researched_on") if not d.get(k)]
        if missing:
            warn(f"{d['id']}: missing {', '.join(missing)}")
        d.setdefault("anchors", [])
        d.setdefault("sources", [])
        d.setdefault("present_day_topics", [])
        out[d["id"]] = d
    if not out:
        warn("no parallels found" + ("; using stub data" if stub else ""))
        if stub:
            out = stub_parallels()
    return out


def stub_parallels():
    return {"STUB1": {
        "id": "STUB1", "title": "Stub parallel (placeholder)", "stub": True,
        "book_claim": "Placeholder until parallels/ is researched.",
        "anchors": ["ch10-p013"], "specificity": "described_pattern",
        "test": "", "verdict": "too_vague_to_judge",
        "parallel": "No research yet. This entry exists so the reader layout can be checked.",
        "reasoning": "", "present_day_topics": ["working hours"], "sources": [],
        "researched_on": "2000-01-01"}}


# --------------------------------------------------------------------------- build


class Book:
    def __init__(self):
        self.anchors = load_json(os.path.join(ROOT, "anchors.json"), {})
        orig_dir, rew_dir = os.path.join(ROOT, "original"), os.path.join(ROOT, "rewrite")
        names = set(os.listdir(orig_dir)) if os.path.isdir(orig_dir) else set()
        if not names:
            warn("original/ is empty or missing")
        rnames = set(os.listdir(rew_dir)) if os.path.isdir(rew_dir) else set()
        if not rnames:
            warn("rewrite/ is empty or missing; showing original text only")
        self.files = sorted((n for n in names | rnames if n.endswith(".md")), key=file_sort_key)
        self.orig, self.rew = {}, {}
        for n in self.files:
            op, rp = os.path.join(orig_dir, n), os.path.join(rew_dir, n)
            if os.path.exists(op):
                self.orig[n] = parse_file(op)
            else:
                warn(f"original/{n} missing")
            if os.path.exists(rp):
                self.rew[n] = parse_file(rp)
            elif n in self.orig and chapter_of(n) is not None:
                warn(f"rewrite/{n} missing; using original text")
        # chapter -> list of files
        self.chapters = OrderedDict()
        for n in self.files:
            c = chapter_of(n)
            if c is not None:
                self.chapters.setdefault(c, []).append(n)
        self.para_page = {}  # paragraph id -> page path relative to site root
        self.para_ids = set()
        self.para_order = {}  # paragraph id -> position in the book
        self.toc = []  # [{part, chapters:[{num,title,sections:[...]}]}]
        self._index()

    def blocks(self, n):
        return self.rew.get(n) or self.orig.get(n) or []

    def _index(self):
        part = None
        for c, files in self.chapters.items():
            entry = {"num": c, "title": f"Chapter {c}", "sections": [], "href": f"read/ch{c:02d}.html"}
            for n in files:
                for b in self.blocks(n):
                    if b["kind"] == "heading":
                        t = heading_plain(b["text"])
                        if b["level"] == 1 and t.lower().startswith("part"):
                            part = {"title": t, "chapters": []}
                            self.toc.append(part)
                        elif b["level"] == 2 and t.lower().startswith("chapter"):
                            entry["title"] = t
                        elif b["level"] == 3:
                            entry["sections"].append({"title": t, "id": slug(t)})
                for src in (self.orig.get(n, []), self.rew.get(n, [])):
                    for b in src:
                        if b["kind"] == "para":
                            self.para_order.setdefault(b["id"], len(self.para_order))
                            self.para_ids.add(b["id"])
                            self.para_page[b["id"]] = entry["href"]
            if part is None:
                part = {"title": "", "chapters": []}
                self.toc.append(part)
            part["chapters"].append(entry)
        for pid, meta in self.anchors.items():
            if pid not in self.para_page and meta.get("chapter"):
                self.para_page[pid] = f"read/ch{int(meta['chapter']):02d}.html"

    def chapter_entry(self, c):
        for p in self.toc:
            for e in p["chapters"]:
                if e["num"] == c:
                    return p, e
        return None, None

    def anchor_label(self, pid):
        meta = self.anchors.get(pid, {})
        c = meta.get("chapter") or chapter_of(pid)
        idx = meta.get("index")
        if idx is None:
            m = re.search(r"-p(\d+)$", pid)
            idx = int(m.group(1)) if m else "?"
        prefix = "Part intro" if pid.startswith("pt") else f"Ch. {c}"
        return f"{prefix}, ¶{idx}"


def paragraph_html(book, n, pid, rblock, oblock, fns_r, fns_o, par_parallels, stem):
    modern_html = render_md(rblock["md"], f"{stem}") if rblock else ""
    orig_html = render_md(oblock["md"], f"{stem}-o") if oblock else ""
    fallback = rblock is None
    if fallback:
        modern_html = orig_html.replace(f"fn-{stem}-o-", f"fn-{stem}-")
    refs = FNREF_RE.findall((rblock or oblock)["md"])
    oref = FNREF_RE.findall(oblock["md"]) if oblock else []

    def notes(ids, fns, prefix, label):
        items = []
        for fid in ids:
            if fid in fns:
                items.append(f'<li id="fn-{prefix}-{slug(fid) or "x"}" tabindex="-1">'
                             f'<span class="fn-num">{esc(fid)}</span>'
                             f'<div>{render_md(FNREF_RE.sub(lambda m: m.group(1), fns[fid]), prefix)}</div></li>')
        if not items:
            return ""
        return (f'<details class="notes"><summary>{label} '
                f'({len(items)})</summary><ol>{"".join(items)}</ol></details>')

    mnotes = notes(refs, fns_r if not fallback else fns_o, stem, "Notes")
    onotes = notes(oref, fns_o, f"{stem}-o", "Original notes")
    kind = book.anchors.get(pid, {}).get("kind", "body")
    marker = ""
    if par_parallels:
        ids = " ".join(par_parallels)
        n_p = len(par_parallels)
        marker = (f'<button class="pmark" type="button" data-parallels="{esc(ids)}" '
                  f'aria-label="{n_p} present-day parallel{"s" if n_p > 1 else ""} for this paragraph" '
                  f'title="Present-day parallel">'
                  f'<span aria-hidden="true">◇</span><span class="pmark-n">{n_p if n_p > 1 else ""}</span></button>')
    tools = ""
    if oblock and not fallback:
        tools = (f'<button class="otoggle" type="button" aria-pressed="false" '
                 f'aria-controls="o-{pid}">Original</button>')
    num = book.anchors.get(pid, {}).get("index", "")
    flag = '<p class="fallback-note">Rewrite not available yet; shown in the original wording.</p>' if fallback else ""
    return f"""<div class="para kind-{esc(kind)}{' has-parallel' if par_parallels else ''}" id="{pid}">
  <div class="gutter">{marker}<a class="pnum" href="#{pid}" aria-label="Link to paragraph {num}">{num}</a></div>
  <div class="cols">
    <div class="modern">{flag}{modern_html}{mnotes}</div>
    <div class="orig" id="o-{pid}" hidden><div class="orig-label">1887 translation</div>{orig_html}{onotes}</div>
  </div>
  <div class="ptools">{tools}</div>
</div>
"""


def build_chapter(book, c, parallels, by_anchor, outdir, today, topics):
    files = book.chapters[c]
    part, entry = book.chapter_entry(c)
    body = []
    for n in files:
        stem = n[:-3]
        rblocks = book.rew.get(n)
        oblocks = book.orig.get(n, [])
        oparas = {b["id"]: b for b in oblocks if b["kind"] == "para"}
        ofns = {b["id"]: b["md"] for b in oblocks if b["kind"] == "fn"}
        src = rblocks if rblocks is not None else oblocks
        rfns = {b["id"]: b["md"] for b in src if b["kind"] == "fn"}
        rparas = {b["id"]: b for b in (rblocks or []) if b["kind"] == "para"}
        for pid in oparas:
            if rblocks is not None and pid not in rparas:
                warn(f"{n}: {pid} missing from rewrite; using original")
        for b in src:
            if b["kind"] == "heading":
                t = b["text"]
                lvl = min(max(b["level"], 1), 5)
                hid = slug(heading_plain(t))
                if lvl == 1:
                    body.append(f'<p id="{hid}" class="part-title">{render_inline(t)}</p>')
                    continue
                tag = {2: "h1", 3: "h2", 4: "h3", 5: "h4"}[lvl]
                body.append(f'<{tag} id="{hid}">{render_inline(t)}</{tag}>')
            elif b["kind"] == "para":
                pid = b["id"]
                rb = rparas.get(pid) if rblocks is not None else None
                body.append(paragraph_html(book, n, pid, rb, oparas.get(pid), rfns, ofns,
                                           by_anchor.get(pid, []), stem))
            elif b["kind"] == "loose":
                body.append(f'<div class="loose">{render_md(b["md"], stem)}</div>')
    # prev / next
    nums = list(book.chapters)
    i = nums.index(c)
    prev_c = nums[i - 1] if i > 0 else None
    next_c = nums[i + 1] if i + 1 < len(nums) else None
    built = BUILT_CHAPTERS

    def chap_link(x, rel):
        if x is None:
            return "<span></span>"
        _, e = book.chapter_entry(x)
        if x not in built:
            return f'<span class="muted">{esc(e["title"])} (not in this build)</span>'
        return f'<a rel="{rel}" href="ch{x:02d}.html">{"← " if rel == "prev" else ""}{esc(e["title"])}{" →" if rel == "next" else ""}</a>'

    sections = "".join(f'<li><a href="#{s["id"]}">{esc(s["title"])}</a></li>' for s in entry["sections"])
    sec_nav = (f'<nav class="sections" aria-label="Sections in this chapter"><h2>In this chapter</h2>'
               f'<ol>{sections}</ol></nav>') if sections else ""
    used = sorted({p for pid_list in by_anchor_for_chapter(book, c, by_anchor) for p in pid_list})
    data = {"parallels": {pid: slim_parallel(parallels[pid], book) for pid in used},
            "verdicts": VERDICTS, "specificity": SPECIFICITY, "today": today,
            "topics": {k: t for k, t in topics.items()
                       if any(ps["href"] == f"read/ch{c:02d}.html" for ps in t["passages"])}}
    controls = """<div class="reader-controls">
  <div class="ctl-group" role="group" aria-label="Reading options">
    <button type="button" id="toggle-all-orig" aria-pressed="false">Show original alongside</button>
    <button type="button" id="toggle-notes" aria-pressed="false">Open all notes</button>
  </div>
  <div class="ctl-group type-controls" role="group" aria-label="Text size and font">
    <button type="button" id="size-down" aria-label="Smaller text">A&minus;</button>
    <input type="range" id="size-range" min="14" max="32" step="1" value="20" aria-label="Text size in pixels">
    <button type="button" id="size-up" aria-label="Larger text">A+</button>
    <output id="size-out" for="size-range">20px</output>
    <label class="font-pick">Font <select id="font-choice">
      <option value="serif">Literata (serif)</option>
      <option value="sans">Atkinson Hyperlegible (sans)</option>
    </select></label>
  </div>
</div>"""
    html_body = f"""<main id="main" class="reader">
<div class="rewrite-banner" role="note">
  <strong>Plain-language rewrite.</strong> This is a modern rewording of the 1887 English translation, not Marx's own words.
  Use “Original” on any paragraph, or the switch below, to read the 1887 text. <a href="../about.html">Fidelity rules</a>.
</div>
<p class="eyebrow">{esc(part["title"]) if part and part["title"] else ""}</p>
{controls}
{sec_nav}
<article class="text">
{''.join(body)}
</article>
<nav class="chapter-nav" aria-label="Chapters">{chap_link(prev_c, "prev")}{chap_link(next_c, "next")}</nav>
</main>
<aside id="panel" class="panel" aria-labelledby="panel-title" hidden tabindex="-1">
  <div class="panel-head"><h2 id="panel-title">Present-day parallel</h2>
  <button type="button" class="panel-close" aria-label="Close panel">Close</button></div>
  <div class="panel-body"></div>
</aside>
<div id="topic-trail" class="topic-trail" hidden></div>
"""
    out = page(f"{entry['title']} — {SITE_TITLE}", html_body, 1, data=data,
               scripts=("reader.js",), body_class="page-reader")
    with open(os.path.join(outdir, "read", f"ch{c:02d}.html"), "w", encoding="utf-8") as f:
        f.write(out)


def by_anchor_for_chapter(book, c, by_anchor):
    for pid, lst in by_anchor.items():
        if book.para_page.get(pid) == f"read/ch{c:02d}.html":
            yield lst


def slim_parallel(p, book):
    d = {k: p.get(k) for k in ("id", "title", "book_claim", "test", "verdict", "specificity", "parallel",
                               "reasoning", "sources", "researched_on", "present_day_topics", "stub")}
    d["passages"] = [{"id": a, "label": book.anchor_label(a), "href": book.para_page.get(a)}
                     for a in p.get("anchors", [])]
    return d


def passage_links(book, anchors, depth):
    up = "../" * depth
    out = []
    for a in anchors:
        href = book.para_page.get(a)
        label = esc(book.anchor_label(a))
        c = int(re.search(r"ch(\d+)", href).group(1)) if href else None
        if href and c in BUILT_CHAPTERS:
            out.append(f'<li><a href="{up}{href}#{a}">{label}</a></li>')
        else:
            note = " (not in this build)" if href else " (unresolved)"
            out.append(f'<li><span class="muted">{label}{note}</span></li>')
    return f'<ul class="passages">{"".join(out)}</ul>'


def build_themes(book, themes, parallels, outdir, today):
    items = themes.get("items", [])
    cards = []
    counts_v = defaultdict(int)
    counts_s = defaultdict(int)
    for it in items:
        p = parallels.get(it["id"])
        v = (p or {}).get("verdict") or it.get("verdict") or "none"
        s = it.get("specificity") or (p or {}).get("specificity") or ""
        counts_v[v] += 1
        counts_s[s] += 1
        anchors = list(OrderedDict.fromkeys((p or {}).get("anchors", []) + it.get("anchors", [])))
        par_html = ""
        if p:
            srcs = "".join(source_li(sr) for sr in p.get("sources", []))
            par_html = f"""<details class="parallel-details">
  <summary>Present-day parallel <span class="asof" data-date="{esc(p.get('researched_on'))}">as of {esc(p.get('researched_on'))}</span></summary>
  {'<p><strong>Test:</strong> ' + esc(p.get('test')) + '</p>' if p.get('test') else ''}
  <p>{esc(p.get('parallel'))}</p>
  <p><strong>Reasoning:</strong> {esc(p.get('reasoning'))}</p>
  {'<h4>Sources</h4><ul class="sources">' + srcs + '</ul>' if srcs else ''}
  <p class="stale" hidden></p>
</details>"""
        elif v == "too_vague_to_judge":
            par_html = '<p class="muted">Not researched: almost any outcome would fit this claim, so it is not tested against the present.</p>'
        quote = ""
        if it.get("quote"):
            quote = f'<blockquote class="quote">“{esc(it["quote"])}” <cite>({esc(book.anchor_label(it.get("quote_anchor", "")))}, 1887 text)</cite></blockquote>'
        topics = (p or {}).get("present_day_topics", [])
        note = f'<p class="note">{esc(it["note"])}</p>' if it.get("note") else ""
        speaker = f' · {esc(it["speaker"])}' if it.get("speaker") and it["speaker"] != "Marx" else ""
        cards.append(f"""<article class="claim" id="{esc(it['id'])}" data-verdict="{esc(v)}" data-specificity="{esc(s)}" data-kind="{esc(it.get('kind',''))}">
  <header><span class="cid">{esc(it['id'])}</span> {verdict_badge(v if v != 'none' else None)}</header>
  <h3>{esc(it['title'])}</h3>
  <p class="meta">{esc(SPECIFICITY.get(s, s))} · {esc(KINDS.get(it.get('kind'), it.get('kind', '')))}{speaker}</p>
  <p>{esc(it.get('claim') or (p or {}).get('book_claim'))}</p>
  {quote}{note}
  {par_html}
  <div class="passages-wrap"><h4>Passages ({len(anchors)})</h4>{passage_links(book, anchors, 0)}</div>
  {'<p class="topics">Topics: ' + ', '.join(esc(t) for t in topics) + '</p>' if topics else ''}
</article>""")

    def checks(name, options, counts):
        boxes = "".join(
            f'<label><input type="checkbox" name="{name}" value="{esc(k)}" checked> {esc(lbl)} '
            f'<span class="count">{counts.get(k, 0)}</span></label>'
            for k, lbl in options.items())
        return boxes

    vopts = OrderedDict(VERDICTS)
    if counts_v.get("none"):
        vopts["none"] = "Not yet judged"
    opps = themes.get("opponent_claims", [])
    opp_cards = "".join(f"""<article class="claim opponent" id="{esc(o['id'])}">
  <header><span class="cid">{esc(o['id'])}</span> <span class="tag">View Marx argues against</span></header>
  <h3>{esc(o['title'])}</h3>
  <p class="meta">Attributed to {esc(o.get('attributed_to', ''))}</p>
  <p>{esc(o.get('marx_response', ''))}</p>
  <div class="passages-wrap"><h4>Passages ({len(o.get('anchors', []))})</h4>{passage_links(book, o.get('anchors', []), 0)}</div>
</article>""" for o in opps)
    body = f"""<main id="main" class="wide">
<h1>Themes and claims</h1>
<p class="lede">Every claim the book makes in Marx's own voice, with how it compares to the present where it can be tested. Verdicts are styled identically on purpose: a miss is as important to see as a hit. Each claim links to the passages that carry it.</p>
<form class="filters" aria-label="Filter claims" onsubmit="return false">
  <fieldset><legend>Verdict</legend>{checks("verdict", vopts, counts_v)}</fieldset>
  <fieldset><legend>Specificity</legend>{checks("specificity", SPECIFICITY, counts_s)}</fieldset>
  <p class="filter-status" aria-live="polite"><span id="shown-count">{len(items)}</span> of {len(items)} claims shown. <button type="button" id="reset-filters">Show all</button></p>
</form>
<section aria-label="Claims" class="claims">{''.join(cards)}</section>
<section aria-labelledby="opp-h" class="opponents">
<h2 id="opp-h">Views the book argues against</h2>
<p class="lede">These are opponents' positions that Marx states in order to answer them. They are listed so they are never read as the book's own claims, and they are not tested against the present.</p>
<div class="claims">{opp_cards or '<p class="muted">None listed.</p>'}</div>
</section>
</main>"""
    data = {"today": today}
    with open(os.path.join(outdir, "themes.html"), "w", encoding="utf-8") as f:
        f.write(page(f"Themes and claims — {SITE_TITLE}", body, 0, active="themes",
                     scripts=("themes.js",), data=data, body_class="page-themes"))
    return counts_v


def source_li(sr):
    pub = sr.get("published", "")
    title = esc(sr.get("title") or sr.get("url"))
    url = sr.get("url")
    link = f'<a href="{esc(url)}" rel="noopener noreferrer">{title}</a>' if url else title
    return f'<li>{link}{" — published " + esc(pub) if pub else ""}</li>'


def build_index(book, outdir):
    parts = []
    for p in book.toc:
        chs = []
        for e in p["chapters"]:
            if e["num"] in BUILT_CHAPTERS:
                secs = "".join(f'<li><a href="{e["href"]}#{s["id"]}">{esc(s["title"])}</a></li>' for s in e["sections"])
            else:
                secs = "".join(f'<li>{esc(s["title"])}</li>' for s in e["sections"])
            if e["num"] in BUILT_CHAPTERS:
                link = f'<a href="{e["href"]}">{esc(e["title"])}</a>'
            else:
                link = f'<span class="muted">{esc(e["title"])} (not in this build)</span>'
            chs.append(f'<li>{link}{"<ol class=secs>" + secs + "</ol>" if secs else ""}</li>')
        parts.append(f'<section><h2>{esc(p["title"])}</h2><ol class="chapters">{"".join(chs)}</ol></section>')
    body = f"""<main id="main">
<h1>Capital: A Critique of Political Economy, Volume I</h1>
<div class="rewrite-banner" role="note"><strong>Plain-language rewrite.</strong> The text here is a modern rewording of the 1887 English translation, made to a strict fidelity standard. The 1887 text is one click away on every paragraph. <a href="about.html">About the rewrite</a>.</div>
<p class="start-links"><a href="today.html">Start from a present-day topic</a> · <a href="themes.html">Browse themes and claims</a></p>
<nav class="toc" aria-label="Table of contents">
<section><h2>Front matter</h2><ol class="chapters"><li>{'<a href="read/front.html">Title page and contents (as printed)</a>' if FRONT_BUILT else '<span class="muted">Not available</span>'}</li></ol></section>
{''.join(parts)}</nav>
</main>"""
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(SITE_TITLE, body, 0, active="contents"))


def collect_topics(book, parallels):
    """present_day_topics from every parallel, merged case-insensitively, passages in book order."""
    topics = {}
    for p in parallels.values():
        if p.get("stub"):
            continue
        for label in p.get("present_day_topics", []):
            key = slug(label)
            if not key:
                continue
            t = topics.setdefault(key, {"label": label, "items": [], "anchors": set()})
            if p["id"] not in t["items"]:
                t["items"].append(p["id"])
            t["anchors"].update(a for a in p.get("anchors", []) if a in book.para_page)
    out = {}
    for key in sorted(topics, key=lambda k: topics[k]["label"].lower()):
        t = topics[key]
        anchors = sorted(t["anchors"], key=lambda a: book.para_order.get(a, 10 ** 9))
        out[key] = {"label": t["label"], "items": sorted(t["items"]),
                    "passages": [{"id": a, "label": book.anchor_label(a), "href": book.para_page[a]}
                                 for a in anchors]}
    return out


def build_front(book, outdir):
    path = os.path.join(ROOT, "original", "00-front.md")
    if not os.path.exists(path):
        warn("original/00-front.md missing; no front matter page")
        return
    rpath = os.path.join(ROOT, "rewrite", "00-front.md")
    use = rpath if os.path.exists(rpath) else path
    with open(use, encoding="utf-8") as f:
        text = re.sub(r"<!--.*?-->", "", f.read(), flags=re.S)
    note = ("" if use == rpath else
            '<p class="fallback-note">The front matter is shown as printed in the source edition '
            '(title page and the original table of contents with its page numbers).</p>')
    body = f"""<main id="main" class="reader">
<div class="rewrite-banner" role="note"><strong>Front matter.</strong> The title page and contents of the source edition. For navigation, use the <a href="../index.html">site contents</a>.</div>
<article class="text front">{note}{MD.render(text)}</article>
<nav class="chapter-nav" aria-label="Chapters"><span></span>{'<a rel="next" href="ch01.html">Chapter 1 →</a>' if 1 in BUILT_CHAPTERS else ''}</nav>
</main>"""
    with open(os.path.join(outdir, "read", "front.html"), "w", encoding="utf-8") as f:
        f.write(page(f"Front matter — {SITE_TITLE}", body, 1, scripts=("reader.js",),
                     data={"parallels": {}, "verdicts": VERDICTS, "today": None}, body_class="page-reader"))
    FRONT_BUILT.append(True)


def topic_href(ps, key, depth):
    return f'{"../" * depth}{ps["href"]}?topic={key}#{ps["id"]}'


def build_today(book, topics, parallels, outdir):
    index = []
    sections = []
    for key, t in topics.items():
        n = len(t["passages"])
        if not n:
            continue
        first = topic_href(t["passages"][0], key, 0)
        index.append(f'<li data-label="{esc(t["label"].lower())}"><a href="{first}">{esc(t["label"])}</a> '
                     f'<span class="count">{n} passage{"s" if n != 1 else ""}</span> '
                     f'<a class="more" href="#{key}" aria-label="Overview of {esc(t["label"])}">overview</a></li>')
        claims = []
        for pid in t["items"]:
            p = parallels[pid]
            claims.append(f'<li>{verdict_badge(p.get("verdict"))} <a href="themes.html#{esc(pid)}">{esc(p.get("title"))}</a> '
                          f'<span class="asof" data-date="{esc(p.get("researched_on"))}">as of {esc(p.get("researched_on"))}</span></li>')
        plinks = "".join(f'<li><a href="{topic_href(ps, key, 0)}">{esc(ps["label"])}</a></li>' for ps in t["passages"])
        sections.append(f"""<section class="topic" id="{key}" data-label="{esc(t["label"].lower())}">
<h2>{esc(t["label"])}</h2>
<p><a class="start" href="{first}">Start reading at the first passage →</a></p>
<h3>Claims</h3><ul class="topic-claims">{''.join(claims)}</ul>
<h3>Passages</h3><ul class="passages">{plinks}</ul>
</section>""")
    body = f"""<main id="main" class="wide">
<h1>Start from today</h1>
<p class="lede">Pick a present-day topic to jump straight into the passages of the book that bear on it. While you read, a bar at the bottom of the page steps you through the rest of that topic's passages. The topics come from the research behind each present-day parallel.</p>
<p><label for="topic-filter">Filter topics</label><br><input id="topic-filter" type="search" autocomplete="off" placeholder="e.g. working hours"></p>
<p class="filter-status" aria-live="polite"><span id="topic-count">{len(index)}</span> topics</p>
<ul class="topic-index">{''.join(index)}</ul>
<div class="topic-sections">{''.join(sections)}</div>
</main>"""
    with open(os.path.join(outdir, "today.html"), "w", encoding="utf-8") as f:
        f.write(page(f"Start from today — {SITE_TITLE}", body, 0, active="today",
                     scripts=("today.js",), body_class="page-today"))


ABOUT = """<main id="main">
<h1>About this edition</h1>

<h2>What you are reading</h2>
<p>The main text on this site is a <strong>plain-language rewrite</strong> of Karl Marx's <cite>Capital: A Critique of Political Economy</cite>, Volume I. It is not Marx's own wording. It rewrites the first English edition of 1887 (translated by Samuel Moore and Edward Aveling, edited by Frederick Engels) for a reader with a high-school reading level and no background in economics.</p>
<p>The 1887 English text is always one click away. Use <strong>Original</strong> on any paragraph, or <strong>Show original alongside</strong> at the top of a chapter, to read the two side by side. The <a href="read/front.html">front matter</a> reproduces the source edition's title page and contents. Paragraph numbers are the same in both versions, so any passage can be checked against the original.</p>
<p>The rewrite and the present-day research were produced with AI models working to the written rules below, then checked by separate review passes that did not do the original work. Treat the rewrite as a reading aid. Quote the 1887 text, not the rewrite.</p>

<h2>Fidelity rules for the rewrite</h2>
<p>Fidelity outranks readability, every time.</p>
<ul>
<li><strong>Keep everything.</strong> Every claim, step in the argument, example, qualification, number, name, date and footnote stays. Only wording is shortened, never content. Ideas Marx repeats stay repeated.</li>
<li><strong>Keep the strength of every statement.</strong> “May” stays “may”, “some” stays “some”, “tends to” stays “tends to”. Questions stay questions.</li>
<li><strong>Add nothing.</strong> No opinions, modern examples, interpretation or summaries, and no logical links the original does not make.</li>
<li><strong>Keep ambiguity.</strong> Where Marx can be read two ways, the rewrite keeps both readings open.</li>
<li><strong>The only additions allowed</strong> are short, neutral explanations of a technical term the first time it appears in a chapter, translations of foreign-language passages in brackets, and a few words identifying an institution or object a modern reader could not know.</li>
<li><strong>Who is speaking stays clear.</strong> Attributions, quotation marks and Marx's ironic scare quotes are kept, so an opponent's view is never presented as Marx's own. Irony stays irony.</li>
<li><strong>The setting stays in the 19th century.</strong> Shillings, factory inspectors and steam-engines stay; only the language is modernized.</li>
</ul>
<p>Each part of the rewrite was reviewed paragraph by paragraph for lost or added claims, strengthened or weakened qualifications, inaccurate explanations of terms, and ambiguity resolved one way.</p>

<h2>Present-day parallels</h2>
<p>A ◇ in the margin of a paragraph means it carries a claim that was compared with the present. The <a href="themes.html">themes page</a> lists every claim, and <a href="today.html">Start from today</a> lets you begin from a current topic.</p>
<ul>
<li>Claims are taken only from the 1887 text and only in Marx's own voice. Views he states in order to answer them are listed separately and are not tested.</li>
<li>Each claim is judged as Marx made it, in his own terms, not as later schools have interpreted it. Every factual statement about the present cites a dated source.</li>
<li>For a concrete forecast, the outcome has to have happened <em>and</em> the evidence has to credit the cause Marx gave. If it happened mainly for other reasons, the verdict is at most “partly holds”.</li>
<li>Each verdict was checked by a separate skeptic review looking for verdicts that were too generous or too harsh, and for obvious counterexamples.</li>
</ul>
<h3>What the verdicts mean</h3>
<dl class="verdict-defs">
<dt><span class="verdict" data-verdict="holds">Holds</span></dt><dd>The present-day evidence matches the claim as stated.</dd>
<dt><span class="verdict" data-verdict="partial">Partly holds</span></dt><dd>Some of the claim matches the evidence and some does not, or it happened for reasons other than the ones Marx gave.</dd>
<dt><span class="verdict" data-verdict="missed">Missed</span></dt><dd>The evidence contradicts the claim as stated.</dd>
<dt><span class="verdict" data-verdict="too_vague_to_judge">Too vague to judge</span></dt><dd>Almost any outcome would fit the claim, so it cannot be meaningfully tested.</dd>
</dl>
<p>All four verdicts are shown in the same style on purpose. A miss is as informative as a hit, and none of them is coloured as good or bad.</p>
<p>Every parallel shows the date it was researched. The present changes, so a note appears on any parallel researched more than six months ago. The research is meant to be refreshed about every six months.</p>

<h2>Privacy</h2>
<p>No tracking scripts, analytics or cookies. Fonts are loaded from Google Fonts. Your text size, font and “show original” choices are stored only in your own browser.</p>
</main>"""


def build_about(outdir):
    with open(os.path.join(outdir, "about.html"), "w", encoding="utf-8") as f:
        f.write(page(f"About this edition — {SITE_TITLE}", ABOUT, 0, active="about"))


def check_anchors(book, parallels, themes):
    bad = []
    for pid, p in parallels.items():
        if p.get("stub"):
            continue
        for a in p.get("anchors", []):
            if a not in book.para_ids:
                bad.append((pid, a))
    for it in themes.get("items", []) + themes.get("opponent_claims", []):
        for a in it.get("anchors", []):
            if a not in book.para_ids:
                bad.append((it["id"], a))
    return bad


BUILT_CHAPTERS = set()
FRONT_BUILT = []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chapters", help="comma-separated chapter numbers to build (default: all)")
    ap.add_argument("--out", default=os.path.join(SITE, "public"), help="output directory")
    ap.add_argument("--no-stub", action="store_true", help="do not add a stub parallel when parallels/ is empty")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD (for testing the stale-date note)")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any anchor fails to resolve")
    args = ap.parse_args()

    today = args.today
    if today:
        dt.date.fromisoformat(today)
    book = Book()
    themes = load_themes()
    parallels = load_parallels(stub=not args.no_stub)

    wanted = set(book.chapters)
    if args.chapters:
        wanted = {int(x) for x in args.chapters.split(",") if x.strip()}
        for w in sorted(wanted - set(book.chapters)):
            warn(f"chapter {w} has no text files; skipped")
        wanted &= set(book.chapters)
    BUILT_CHAPTERS.update(wanted)

    topics = collect_topics(book, parallels)
    by_anchor = defaultdict(list)
    for pid, p in parallels.items():
        for a in p.get("anchors", []):
            by_anchor[a].append(pid)

    out = args.out
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "read"))
    shutil.copytree(ASSETS, os.path.join(out, "assets"))

    for c in sorted(wanted):
        build_chapter(book, c, parallels, by_anchor, out, today, topics)
    build_front(book, out)
    build_index(book, out)
    build_today(book, topics, parallels, out)
    build_about(out)
    counts = build_themes(book, themes, parallels, out, today)

    bad = check_anchors(book, parallels, themes)
    for owner, a in bad:
        warn(f"anchor {a} (from {owner}) does not resolve to a paragraph")
    n_anchor_refs = sum(len(p.get("anchors", [])) for p in parallels.values())
    print(f"built {len(wanted)} chapter page(s), {len(themes.get('items', []))} claims, "
          f"{len(parallels)} parallels ({n_anchor_refs} anchor refs) -> {os.path.relpath(out, ROOT)}")
    print(f"topics: {len(topics)}")
    print("verdicts: " + ", ".join(f"{VERDICTS.get(k, k)} {v}" for k, v in counts.items()))
    print(f"anchors: {len(bad)} unresolved; {len(WARNINGS)} warning(s)")
    if args.strict and bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
