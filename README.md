# Capital, Volume I: a plain-language reader

A static website that presents a plain-language rewrite of Marx's *Capital*, Volume I, alongside the 1887 English text. Some paragraphs also carry dated present-day parallels. There is no backend, so it can be hosted on GitHub Pages, Netlify or any static file host.

The whole site is generated from the project's data files. When you re-run the rewrite or the research, rebuild the site and the changes appear with no manual edits.

## What the site contains

| Page | Built from |
|---|---|
| Reader (`read/chNN.html`), one page per chapter with section links, footnotes as expandable notes, an original-text toggle per paragraph or per chapter, text size and font controls, and ◇ margin markers that open the parallel panel | `rewrite/*.md`, `original/*.md`, `anchors.json`, `parallels/*.json` |
| Front matter (`read/front.html`) | `original/00-front.md` (or `rewrite/00-front.md` once it exists) |
| Contents (`index.html`): front matter, 8 parts, 33 chapters and their sections | headings in the text files |
| Themes and claims (`themes.html`), filterable by verdict and specificity | `themes-index.json` (falls back to `themes-index.md`), `parallels/*.json` |
| Start from today (`today.html`), present-day topics that jump into the reader with a step-through bar | `present_day_topics` in `parallels/*.json` |
| About (`about.html`): fidelity rules, how parallels were researched, verdict definitions | written in `site/build.py` (the `ABOUT` text) |

## Rebuild

Requires Python 3.9+ and `markdown-it-py`:

```bash
pip install markdown-it-py
```

Build the site into `site/public/`:

```bash
python3 site/build.py
```

Check the result. This confirms that every anchor in `parallels/` resolves to a paragraph in the built pages and that every internal link and `#id` exists. It exits non-zero on any failure.

```bash
python3 site/check_site.py
```

Preview it locally at http://127.0.0.1:8765:

```bash
python3 -m http.server 8765 --directory site/public --bind 127.0.0.1
```

### Build options

- `--chapters 10,15`: build only these chapters (handy for quick previews). Links to other chapters are marked "not in this build".
- `--strict`: exit non-zero if any anchor in `parallels/` or the themes index doesn't resolve to a paragraph. The deploy configs below use it.
- `--today 2027-06-01`: pretend today is that date, to test the "older than 6 months" note on parallels.
- `--no-stub`: don't insert a placeholder parallel when `parallels/` is empty.
- `--out DIR`: write somewhere other than `site/public/`.

### Partial data

The build works at any stage of the project. A missing input is skipped with a `warning:` line rather than failing the build:

- A missing `rewrite/` file (or paragraph) falls back to the original text, labelled as such.
- A missing or empty `parallels/` gets one clearly labelled stub parallel so the layout can still be checked.
- If `themes-index.json` is missing, the build reads `themes-index.md`.
- Invalid JSON files are skipped with a warning.

### After a research refresh

The research is meant to be refreshed about every six months (see Step 4 in `runbook.md`). Once `parallels/*.json` is updated, run the build and the check again. The "as of" dates, verdicts, topic list and staleness notes all update automatically. The staleness note is worked out in the reader's browser from `researched_on`, so a parallel gets flagged once it is more than 6 months old even if nobody rebuilds the site.

## Deploy

`site/public/` is the whole site: plain HTML, CSS and JS with relative links, so it works from a domain root or a sub-path. It isn't committed (see `.gitignore`); each deploy builds it fresh.

**GitHub Pages:** `.github/workflows/pages.yml` builds, checks and deploys on every push to `main` or `master`. In the repository settings, under Pages, set Source to "GitHub Actions".

**Netlify:** `netlify.toml` sets the build command and the publish directory (`site/public`). Connect the repository and deploy; no other settings are needed.

**Anywhere else:** run the build and upload the contents of `site/public/`.

## Files

```
site/build.py        generator (all pages, from the data files)
site/check_site.py   post-build check: parallel anchors and internal links
site/assets/         style.css, reader.js, themes.js, today.js (copied into the build)
site/public/         build output (not committed)
```

## Privacy and accessibility

- There are no analytics, tracking scripts or cookies. The only outside request is for the fonts (Literata and Atkinson Hyperlegible) from Google Fonts.
- Reader preferences (text size, font, show original) are kept in the browser's localStorage.
- Every control is a native button, input or link, so the whole site works from the keyboard. Esc closes the parallel panel and returns focus to its marker. There is a skip link on every page.
- The layout works down to phone width, and dark mode follows the system setting.
