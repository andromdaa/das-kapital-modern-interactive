# Consistency report (Phase 5)

**Scope:** 89 rewritten units in `rewrite/`, checked against `original/`, `style-bible.md` (v1.0 plus the Phase 4 additions listed below) and `glossary.json`.

**Bottom line:**
- **Script checks:** every unit passes the Phase 4 checks after all fixes, with 0 failures. The checks cover IDs, headings, footnotes, numbers, formulas, tables, glossary terms and length.
- **Paragraphs and footnotes:** all 1,823 paragraph IDs and all 1,110 footnotes are in place in the assembled book. There are no duplicate or undefined labels.
- **Review findings:**
  - A fresh reviewer, not the rewriter, read every unit for fidelity and drift. Reviewers found 104 problems: 67 fidelity and 37 drift.
  - None was high severity, and 17 were medium. All were fixed.
  - A further 24 cross-file conflicts were resolved by targeted edits, with 245 edits across 66 files.
- **Open items:** none. Every decision is closed (§6).

---

## 1. Glossary check (script: `scripts/consistency.py` → `work/consistency_glossary.json`)

For every glossary entry, the script searched `original/` and `rewrite/` paragraph by paragraph. It flags any place where the original uses the term and the rewrite doesn't use the chosen rendering, and any place where an archaic form remains in Marx's own prose.

| Entry | Misses | Status |
|---|---|---|
| operatives → factory workers | 5 / 73 paragraphs | **All deliberate and logged.** ch15-p027 and p077: "operative machines" means *working machines*. ch15-p060 and p116: medieval or manufacturing-period workers, where "factory" would be an anachronism. ch15-p156 (n. 139): "operative iron founders" means *working* founders. |
| &c. → etc. | 2 | **Deliberate.** ch01-p095 and p096: inside the value-form formula lines, which are copied exactly. |
| manufactory → manufacturing workshop | 1 / 26 | **Deliberate.** ch14-p030: inside the literal translation of Skarbek's French ("établissements"). |

All 45 enforced (★) entries are used wherever they are required. Five earlier false positives came from bugs in the checker, which were fixed during Phase 4:
- trailing commas counted as part of a number;
- "operative" matching inside "co-operative";
- heading text counted as part of the paragraph before it;
- "&c." flagged inside citation titles;
- the length thresholds.

## 2. Notes conflicts (full write-up: `work/notes_conflicts.md`)

A fresh agent read all 90 notes files plus the orchestrator's running list (`work/consistency_todo.md`) and found **24 places where units decided the same question differently**. Each was given one resolution grounded in the style bible. Six fixer agents then applied the resolutions to non-overlapping file ranges, searching each file for instances that the notes had missed.

| # | Conflict | Resolution applied |
|---|---|---|
| 1 | The ethnic term "negro" in Marx's voice was rendered differently, and some renderings added "enslaved" or "African" | "Black man / woman / people"; add "slave" only where Marx says slave. Fixed in ch19 n8 and ch31 p005, p029. **ch24-p072 is left for your decision** (§6). |
| 2 | Other outdated collective names ("savages", "races", "Teutonic", "Asiatic", "Scotch") | Applied the §4 rule consistently. "Savages" is kept as printed (a period term, not the name of a group). ch02 n5 reverted. |
| 3 | "currency" (*Umlauf*) had been replaced by "circulation" | Restored "currency" in Ch. 3, as Marx's own translator's note (ch03 n26) requires. |
| 4 | §7 terms first met inside a quotation | A bracketed first-clause gloss in the quotation, then the full explanation at the first use in Marx's voice (new rule in bible §7.0). |
| 5 | Third-person "Marx" left inside Marx's own voice ("in Marx's view…") | Removed: ch16, ch24-s3, ch25-s5a, ch33. |
| 6 | Parentheticals of uncertain speaker inside quotations, converted to Marx's voice | Reverted to the printed wording unless there is positive evidence the parenthetical is Marx's. |
| 7 | §7 explanations shortened, or placed before Marx develops the idea | Moved or dropped case by case (e.g. ch05-p002 surplus-value, ch15-p071 intensity, ch09-p010 working day). |
| 8 | "aliquot part": the glossary rendering "equal fraction" was wrong | Glossary changed to "fractional part / share"; earlier units fixed. |
| 9 | "circulating medium" / "means of circulation" | "medium of circulation" everywhere in Marx's voice. |
| 10 | "subject of labour" | "object of labor" (a glossary addition made in Phase 4). |
| 11 | "manufactures" (plural) | Rendered by sense: "branches of manufacture", "manufacturing workshops", or "manufacture". |
| 12 | "hands" without scare quotes | "workers", except inside quotations or where Marx is mocking the employers' word. |
| 13 | "ideal / ideally" in Ch. 3 | Kept, with a short gloss at first use ("existing only in thought"). |
| 14 | "alienate / alienation" | Sale sense glossed; separation sense kept as printed. |
| 15 | "op. cit." | Kept as printed. |
| 16 | British spelling in formula lines outside ```text blocks | American spelling (these lines are Marx's voice); numbers and symbols kept exactly. |
| 17 | Neutral identifications repeated, or worded evaluatively | Once per chapter, neutral wording only. |
| 18 | Foreign tags in Marx's voice | Replaced with plain English unless they are a famous tag or a quoted term. |
| 19 | Foreign titles | Kept untranslated (§2.6). |
| 20 | "&c." after a closed title, "per cent.", italic "that is" | "etc.", "percent" (Marx's voice only), roman type. |
| 21 | Typos inside quotations and in figures | Fixed only where there is one possible reading; otherwise kept and logged. |
| 22 | Typos in citation punctuation | Fixed (one reading). |
| 23 | Mixed straight and curly quotation marks; missing full stops | Normalized. |
| 24 | Minor wording drift ("Cyclops-like", "peak") | Harmonized. |

**Closed by policy** (each logged in that unit's notes; no further action planned):

- **Uncertain parentheticals.** Some parentheticals inside quotations may be Marx's interpolations. **Closed:** the source of record is the 1887 translation in the PDF, so they keep its printed wording and stay inside the quotation, exactly as printed. No MECW comparison will be made. Affected: ch10-s4 p093, ch10-s5b p123, ch10-s6a p144, ch10-s7 n163, ch24-s4 p101, ch25-s1 n6, ch25-s5d p200, n99.
- **Source oddities kept as printed.** **Closed:** these are features of the source text, and fixing them would mean guessing (bible §1.4). Each is logged in its unit's notes. They are kept as printed because more than one reading is possible: "felling" (ch20 n4), "is miserable wretch" (ch33 p009), "unjustice" (ch15-p262), unmatched quotation marks in about 12 notes, and number mismatches between the text and its tables. The last group includes the 29,211 vs 28,211 grains in ch25, the 160,605 vs 166,605 qrs. in ch25, "28,8211" and "122,8501", the £2,000 vs £12,000 implied in ch24-p002, "½d." vs 1½d. in ch21-p023, and "13⅔ lbs." in ch09-p036.
- **Latin and French terms kept with their brackets** because they work as quoted technical terms or famous tags: *differentia specifica*, *nexus rerum*, *terminus medius*, *nec plus ultra*, *pour le roi de Prusse*, *quand même* and similar.

## 3. Fidelity and drift review (per group of ~5 consecutive units)

Each unit was read by a fresh Opus reviewer, never its own rewriter, against the original and the style bible. The review covered fidelity and drift together (one read, two outputs), and the reviewer then applied targeted fixes. 18 groups covered 86 units; the 3 pilot units had their own reviewers at the checkpoint.

| Verdict | Units |
|---|---|
| ok | 32 |
| minor fixes | 57 |
| major fixes / redo | 0 |

**Findings by kind and severity:**

| Kind | High | Medium | Low |
|---|---|---|---|
| Fidelity | 0 | 13 | 54 |
| Drift | 0 | 4 | 33 |

**Findings by category:** strength changed 27, added content 15, lost content 9, ambiguity resolved 9, concept explanation 9, structure 7, quotation 6, tone 5, register 5, glossary 5, spelling 4, attribution 3.

The usual failure was splitting a long sentence, which then weakened or strengthened Marx's qualifier, or attached his "Hence" to the wrong clause. No reviewer found an opponent's claim presented as Marx's after the rewriters' own self-checks. The 3 attribution findings were cases where a split loosened who was speaking, and all were fixed.

**All 17 medium findings (all fixed):**
- **ch01 n34:** the pairing "politics / Catholicism" with the ancient world / middle ages had been reversed.
- **ch02 n13:** "it appears" had been hardened to "shows".
- **ch03-p048, ch07-p025, ch14-p028, ch14-p055:** a missing §7 explanation at the term's first technical use.
- **ch05-p002:** the surplus-value explanation gave away the answer to the question Marx leaves open in that chapter.
- **ch10-p115:** "alone" had shifted scope ("Great Britain alone" instead of "just the town centers").
- **ch13-p027:** "a necessary concomitant" had lost "necessary".
- **ch14-p034:** "together with others" had been made to mean other producers instead of other industries.
- **ch15-p036:** a hypothetical ("even if … remains") had been stated as fact.
- **ch15-p119:** "Hence" had been attached to the wrong clause.
- **ch24-p072:** the ironic "in the same way that the slave-owner was delivered by abolition" had been lost in a sentence split.
- **ch25-p244, p245:** the metaphor "gipsy life" had been turned into a claim about the Romani people.
- **ch29-p001:** "the greatest landed proprietors" had been weakened to "great".
- **ch33-p010:** a clause of Marx's mock-prescription had been split off so it read as a statement of fact.

**Drift (reading level, voice, quotations, tone):**
- **Sentence length:** the reviewers asked for further splitting of over-long sentences only in Ch. 1; elsewhere they found sentence length in range.
- **Ambiguity over shorter sentences:** where splitting would have resolved an ambiguity, the sentence was left long and logged (bible §0.6).
- **Quotations:** treatment was consistent. Testimony is kept near-verbatim with bracketed glosses for obsolete words, and economists' wording is kept where Marx attacks it.
- **Tone:** irony and polemic are intact. Reviewers restored the bite in several places ("declamations", "twitting", "exported to Canada", "decaying").

## 4. Changes to the rules during the run

These were found during Phase 4 and recorded in `style-bible.md` and `glossary.json`:

1. "subject of labour" → **object of labor** (a recurring term; "subject" misleads modern readers).
2. "aliquot part" → **fractional part / share**. The old rendering "equal fraction" made claims Marx doesn't make.
3. **§7.0:** a term first met inside a quotation gets a short bracketed gloss there, and the full explanation at its first use in Marx's voice.
4. **§3.3:** scare quotes only where Marx uses them, never added.
5. **§2.1:** a parenthesis outside the quotation marks is Marx's, not the quoted writer's. The bible's own example was corrected.

## 5. Final script re-run (after all Phase 5 edits)

- **check_pair on all 89 units:** 89 PASS, 0 FAIL. The 8 warnings are all the deliberate glossary exceptions listed in §1.
- **Length ratios** run from 0.99 to 1.22 per unit, all inside the 0.95–1.25 target. The whole book comes to **1.036×**.
- **Structure check on rewrite/:** 1,823 IDs, continuous in every chapter; 1,110 footnotes, all matched.
  - The one flag is ch31's notes starting at 2. That is a source quirk: the first note there is the unnumbered `*` note.

## 6. Decisions (all closed)

1. **ch24-p072, a racial slur in free indirect speech.** **Decided by the user:** Marx's printed word is restored in both places. It is used to make the ironic point about the slave-owner, not to discriminate.
2. **Outdated ethnic names elsewhere in Marx's own voice.** **Decided by the user:** the other units stay as they are, under the §4 rule (neutral modern name in Marx's voice; original wording inside quotations). ch24-p072 is the only exception.
3. **Front matter.** **Decided by the user:** prefaces and afterwords are intentionally excluded. `00-front.md` holds the title page and contents only.
