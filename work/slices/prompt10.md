You are helping prepare a style guide for a plain-modern-English rewrite of Marx's *Capital*, Vol. 1 (Moore/Aveling 1887 translation). You are NOT rewriting anything. Your job is to read one slice of the book carefully and catalogue what a rewriter will need decisions on.

Files are in /home/cole/Projects/das-kapital/original/. Each paragraph is preceded by an ID comment like `<!-- ch05-p012 -->`; footnotes are `[^N]` with text in `[^N]: ...` blocks after the paragraph. Read EVERY file in your slice in full (use the Read tool; read large files in parts if needed), including the footnotes.

Your slice: ch25-s5e.md, ch25-s5f.md, ch26.md, ch27a.md, ch27b.md, ch28.md, ch29.md, ch30.md, ch31.md, ch32.md, ch33.md

Write your findings as a single JSON file to /home/cole/Projects/das-kapital/work/slices/slice10.json with exactly this shape (all lists may be empty; keep every string short):

```json
{
  "slice": 10,
  "files": [...],
  "technical_terms": [
    {"term": "surplus-value", "approx_count": 40, "example_id": "ch07-p031",
     "how_marx_uses_it": "one sentence, from the text itself", "variants_seen": ["surplus value", "surplus-values"]}
  ],
  "archaic_words_and_idioms": [
    {"word": "vice versâ", "approx_count": 3, "example_id": "ch01-p012", "meaning_in_context": "the other way round"}
  ],
  "recurring_phrases": [
    {"phrase": "in the sphere of circulation", "approx_count": 6, "example_id": "ch05-p004", "meaning": "..."}
  ],
  "hegelian_or_philosophical": [
    {"term": "moment", "example_id": "...", "meaning_in_context": "..."}
  ],
  "personified_figures": [
    {"figure": "Mr. Moneybags", "example_id": "...", "note": "how/why Marx uses it"}
  ],
  "people_and_sources": [
    {"name": "N. W. Senior", "who": "one line", "treatment": "opponent|ally|authority|irony target|neutral source",
     "example_id": "...", "approx_count": 5}
  ],
  "currency_units_institutions": [
    {"item": "quarter (of wheat)", "kind": "unit|currency|institution|title|place|period|document", "example_id": "..."}
  ],
  "numbers_formulas_tables": [
    {"example_id": "...", "what": "e.g. 'C–M–C formula', 'working-day table', 'fraction s/v'"}
  ],
  "quotation_patterns": [
    {"pattern": "long Blue Book/inspector testimony as block quote | economist quoted then mocked | witness deposition with names and ages | verse | foreign-language quote with bracketed translation | ...",
     "example_id": "...", "note": "who is speaking and how the reader can tell"}
  ],
  "foreign_language": [
    {"language": "Latin|French|German|Greek|Italian|...", "example_id": "...", "snippet": "first few words", "has_bracketed_translation": true}
  ],
  "voice_attribution_risks": [
    {"example_id": "...", "note": "places where an opponent's view is stated before Marx answers it, or where irony could be misread as Marx's own claim"}
  ],
  "irony_examples": [
    {"example_id": "...", "note": "what the irony is"}
  ],
  "hard_passages": [
    {"example_id": "...", "why": "dense abstraction, ambiguity Marx leaves open, long sentence, etc."}
  ]
}
```

Rules:
- Every `example_id` must be a real paragraph ID that you saw in your slice and that actually contains the item. Accuracy matters more than volume: do not guess IDs.
- `technical_terms`: every economic or philosophical term the argument relies on (e.g. use-value, exchange-value, value, labour-power, abstract labour, socially necessary labour-time, magnitude of value, equivalent form, relative form, money-form, circulation, metamorphosis, capital, surplus-value, constant/variable capital, rate of surplus-value, necessary labour, surplus-labour, relative/absolute surplus-value, organic composition, reserve army, accumulation, etc. — but only those that actually appear in your slice, plus any others you find). Note spelling/hyphenation variants exactly as printed.
- `archaic_words_and_idioms`: words or constructions a modern high-school reader would stumble on ("hereof", "wherewith", "betwixt", "&c.", "l.c.", "viz.", "to wit", "nay", "quâ", "pro tanto", "en masse", "quotum", "aliquot", "procure", obsolete senses like "intercourse", "commerce", "corn" = grain, "hands" = workers, "operative", "manufacture" in the old sense, etc.). Include Latin abbreviations used in footnotes.
- `people_and_sources`: include economists, officials, factory inspectors, commissioners, doctors, witnesses who recur, newspapers, and official reports (Blue Books, Reports of the Inspectors of Factories, Children's Employment Commission, Public Health reports, etc.).
- Be concrete and brief. Do not summarize the book. Do not include anything you did not see in your slice.

When you have written the file, reply with one line: the path and the number of entries in each list.
