# Cause-and-outcome re-check of concrete forecasts

New rule (see end of work/RESEARCH_BRIEF.md): a concrete_forecast is judged on the predicted outcome AND the cause Marx gives. "holds" needs the outcome to have happened and the evidence to credit substantially Marx's stated cause; if the outcome happened mainly for other reasons, the verdict is at most "partial". If the outcome did not happen, "missed" stands whatever the mechanism. The rule can only lower a verdict, never raise one.

For each item in your batch:
1. Read parallels/<ID>.json, review/<ID>.md, the item in themes-index.md, and the anchored passages in original/ with their surrounding section (anchor -> file via anchors.json). Never read rewrite/.
2. Identify the cause Marx gives for the forecast, in his words and terms. Update `test` so it names the cause explicitly.
3. Use WebSearch/WebFetch (open every page you cite) to find what the evidence credits for the outcome. Apply the research brief's standards: opened pages only, primary sources for statistics, `published_precision` on every source, and paraphrase only.
4. Edit parallels/<ID>.json if needed: set the verdict, and update `parallel` and `reasoning` so they explain the cause test, including the strongest case on each side.
5. Append a section to review/<ID>.md headed `## Cause re-check (2026-10-22)` stating Marx's cause, what the evidence credits, and the verdict before -> after. If the verdict changes, ALSO change the review's first line to `verdict_before: <original pre-review verdict, unchanged> | verdict_after: <new verdict>`.
6. Run python3 scripts/check_parallels.py and fix any problems in your files.
Stay neutral: don't editorialize for or against the book. Reply with one line per item: ID, verdict before -> after, Marx's cause, and what the evidence credits.
