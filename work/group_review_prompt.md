You are a fresh reviewer for a plain-English rewrite of Marx's *Capital*, Vol. 1. You did not write the rewrite. Project root: /home/cole/Projects/das-kapital. Your unit(s): **{FILES}**.

Read `style-bible.md` in full. Then, for each unit, read `original/<file>` and `rewrite/<file>` and compare them paragraph by paragraph, using the `<!-- chNN-pNNN -->` IDs. Include the footnotes. Also read `notes/<file>-notes.md` if it exists. It records the rewriter's judgment calls; check that they are sound.

You do one read with two outputs.

**A. Fidelity (meaning only). This outranks everything else.** For each paragraph and footnote, look for:
- a lost claim, example, argument step, number, name, or qualification;
- an added claim, example, interpretation, or logical link;
- a strengthened or weakened qualification ("may" → "will", "some" → "all", a hedge dropped, an emphasis added);
- an ambiguity that Marx leaves open, resolved;
- an inaccurate or inconsistent concept explanation (compare with style bible §7 and with how Marx uses the term in this passage);
- **an opponent's claim that now reads as Marx's own, or the reverse.** This includes lost attribution tags, lost quotation marks or scare quotes, free indirect speech made neutral, and irony made literal (or literal made ironic);
- a quotation paraphrased beyond what §2 allows, or a foreign text altered or mistranslated.

**B. Drift (against the style bible).** Look for:
- the reading level is too hard (long sentences, jargon left unexplained, archaic words left in) or padded;
- voice and tone flattened (irony or polemic lost) or exaggerated;
- quotations treated inconsistently with §2;
- glossary renderings (§3) not used;
- §7 explanation wording not used, or used for a term that was already explained earlier in the chapter (see `work/context/<file>`);
- American spelling not applied outside quotations;
- structural problems the script would not catch.

Report only real problems. Do not rewrite whole paragraphs and do not polish style for its own sake. Each finding must point to a specific paragraph ID, quote the problematic rewrite words, and give the original words they correspond to.

Write `work/reviews/<file>.json` for each unit, exactly in this shape:

```json
{"file": "<file>", "verdict": "ok | minor fixes | major fixes | redo",
 "findings": [
   {"id": "ch10-p045", "kind": "fidelity | drift", "severity": "high | medium | low",
    "category": "lost content | added content | strength changed | ambiguity resolved | attribution | concept explanation | quotation | glossary | register | tone | spelling | structure",
    "original": "exact original words", "rewrite": "exact rewrite words",
    "problem": "one sentence", "fix": "the replacement text, or precise instruction"}
 ],
 "notes_review": "one or two sentences on whether the rewriter's logged judgment calls are sound",
 "summary": "two sentences: overall fidelity and readability"}
```

Fidelity findings outrank readability findings. When in doubt about meaning, flag it as fidelity.

After writing all the review JSON files, **apply the fixes yourself**:
- Make targeted edits to `rewrite/<file>` for every finding. Do not re-rewrite whole paragraphs unless the verdict is "redo".
- Run `python3 scripts/check_pair.py <file>` for each unit until it passes.
- Append one line to `notes/<file>-notes.md`: "Review fixes applied (N findings) by group reviewer."

Do not edit `original/`, `style-bible.md`, or `glossary.json`.

Reply with one line per unit: the path, the verdict, counts of fidelity and drift findings by severity, and the final check_pair result line.
