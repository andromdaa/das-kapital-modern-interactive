# Skeptic review brief

Project: /home/cole/Projects/das-kapital. Today is 2026-10-22. You are a skeptical reviewer of `parallels/<ID>.json` files, each judging how a claim from Marx's Capital Vol. 1 holds up today. You did not do the research. Read `work/RESEARCH_BRIEF.md` (the rules and standards the researcher had to follow), the item's entry in `themes-index.md`, and the anchored passages in `original/` (anchor -> file via `anchors.json`; read the surrounding section for context). NEVER read `rewrite/`. Do not read other items' parallels or reviews.

For EACH item in your batch:
1. **Claim fidelity.** Does `book_claim` and `test` state what Marx actually wrote, in his terms and with his hedges? Is anything an opponent's view or a later school's reading?
2. **Sources.** Open (WebFetch) every cited source. Does each support the specific statement it is used for? Is the date right and the precision honest? Is a statistic cited from its primary body? Flag anything that seems to come from no opened source.
3. **Verdict.** Is it too generous or too harsh? Look actively for obvious counterexamples and the strongest case on each side (use WebSearch). Is "partial" justified as neither holds nor missed? Is a vague claim being stretched to fit?
4. **Neutrality and copyright.** No editorializing for or against the book; no quote longer than a short phrase.

Then:
- Write `review/<ID>.md`: first line exactly `verdict_before: X | verdict_after: Y`, then sections **Fidelity**, **Sources**, **Verdict**, **Changes made** (bullets; "none" if none). Keep it under ~400 words.
- Where you are confident the review is right, EDIT `parallels/<ID>.json` directly: fix claim/test wording, remove or replace unsupported statements and bad sources (only add sources you opened, with `published_precision`), and change the verdict if warranted (update `parallel` and `reasoning` to match). Keep the schema in the research brief. Don't make changes merely of taste.
- Run `python3 scripts/check_parallels.py` and fix any problems in your files.
Reply with one line per item: ID, verdict before -> after, and a one-clause reason.
