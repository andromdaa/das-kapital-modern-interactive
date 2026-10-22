# Research brief: one parallels file per themes-index item

Project: /home/cole/Projects/das-kapital. You research how claims in Marx's Capital Vol. 1 hold up against the present day. Today is 2026-10-22.

## What to read
- `themes-index.md` (your item's entry: claim, anchors, notes) and `themes-index.json`.
- The anchored paragraphs in `original/` (look up each anchor's file in `anchors.json`; grep for `<!-- chNN-pNNN -->`). Read them and their footnotes so you judge what Marx actually wrote.
- NEVER read `rewrite/`, other files in `parallels/`, or `review/`.

## Research
Use WebSearch to find, and WebFetch to OPEN, every source you cite (a search snippet is not a source). Prefer primary sources (statistical agencies, ILO, OECD, FAO, central banks, peer-reviewed papers, official reports) and established outlets. Every factual claim about the present needs a source with a publication date. Aim for 3-6 good sources; include at least one that cuts against the verdict where one exists.

## Standards (adopted after the pilot; mandatory)
1. **Read the context and state the test first.** Before searching, read the whole section(s) containing your anchors, not just the anchored paragraphs, so you know what Marx means in that chapter (e.g. in ch33 "promised land" means a place where wage workers can escape into independent production on free land). Write the test in Marx's terms in the `test` field before you research.
2. **Opened pages only.** Any fact you did not read on a page you opened is cut, not kept with a flag. Do not write "I could not verify" claims into the file.
3. **Primary sources for statistics.** When a number comes from a statistical agency, international body or central bank (ONS, BLS, Census, ILO, OECD, FAO, World Bank, Fed, ECB...), cite that body's own page or release, not a news report of it.
4. **Honest dates.** `published` is YYYY-MM-DD; add `published_precision`: "day", "month" or "year". If the page gives only a month or year, use the first day and set the precision accordingly. If you cannot find any date, do not use the source.
5. **Justify "partial".** If the verdict is partial, `reasoning` must say explicitly why it is neither holds nor missed.

## Output: parallels/<ID>.json
{
  "id": "T07",
  "title": "short reader-facing title",
  "book_claim": "Marx's claim in your own words",
  "anchors": ["ch05-p012", "ch05-p013"],
  "specificity": "concrete_forecast | general_warning | described_pattern",
  "test": "the test in Marx's terms: what would count as the claim holding or failing today",
  "verdict": "holds | partial | missed | too_vague_to_judge",
  "parallel": "2-4 sentences on how it compares to today, in your own words",
  "reasoning": "why this verdict, including the strongest case against it",
  "present_day_topics": ["short topic labels a reader might start from"],
  "sources": [{"title": "", "url": "", "published": "YYYY-MM-DD", "published_precision": "day | month | year"}],
  "researched_on": "2026-10-22"
}
Anchors must be IDs that exist in anchors.json (use the index's anchors, trimmed to the ones that actually carry the claim). Specificity should match the index unless you have a strong reason (say so in reasoning).

## Rules
- Paraphrase sources. No quotes longer than a short phrase; this will be published.
- "missed" and "too_vague_to_judge" are valid, useful outcomes. Do not stretch a vague claim to fit current events. If a claim would match many possible outcomes, say so.
- Separate what the book says (book_claim) from what you infer it means (reasoning). Judge the claim as Marx made it, in his terms and with his hedges, not as a later school (Leninist, Marxian economists, critics) interprets it. Note when a claim was about his own time and whether it is being judged as a continuing tendency.
- Politically contested subject: describe the facts and the main positions; don't editorialize for or against the book.
- Verdict guide: holds = the claim as stated describes the present well; partial = true in some important respects or places, false in others; missed = the present clearly contradicts it; too_vague_to_judge = it fits too many outcomes.
- Validate the JSON parses. Reply with: ID, verdict, one-line why, and any doubts.

## Rule added after review: forecasts are judged on cause as well as outcome
For a concrete_forecast, the verdict covers both the predicted outcome AND the cause or mechanism Marx gives for it. "holds" requires that the outcome happened and that the evidence credits substantially Marx's stated cause. If the outcome happened mainly for other reasons, the verdict is at most "partial". If the outcome did not happen, the verdict is "missed" (or "too_vague_to_judge") whatever the mechanism. State the cause explicitly in `test`.
