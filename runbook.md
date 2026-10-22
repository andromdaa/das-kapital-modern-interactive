# Capital, Vol. 1: Modernization and Parallels Project Runbook

## Overview

The project turns `das-capital-vol-1-original.pdf` (Moore/Aveling 1887 translation, public domain; 526 pages, ~340k words, real text layer, so no OCR) into two things: a faithful plain-English rewrite, and an interactive website that links passages in the book to how its claims compare with the present day. Four Claude Code prompts, run in order:

1. **Rewrite.** Extract the PDF, build a style bible, pilot three files, rewrite the rest in parallel, check, assemble.
2. **Research.** Build the themes index, research each claim against current events, then have independent agents challenge the verdicts. Runs in a separate session, concurrently with Step 1 (see Run order).
3. **Build.** Generate a static website from the data files. The build script is written while the rewrite runs.
4. **Refresh.** Every ~6 months, re-research stale parallels and rebuild.

### Decisions that shape everything

- **Fidelity outranks readability.** Every claim, argument step, example, qualification, hedge, number, and footnote survives at the same strength ("may" stays "may"). No added opinion, modern examples, or interpretation. Rewrites run longer, roughly 1.2–1.5× the original.
- **Whose argument is it.** Marx often works through an opponent's argument (Senior, Ricardo, Bastiat, Proudhon, Malthus…) before answering it. The rewrite must never let an opponent's claim read as Marx's own, or the reverse. Irony and polemic stay; the 19th-century setting stays.
- **The rewrite is built blind to the parallels.** The themes index is created in Step 2 and rewrite agents never see it, so present-day comparisons cannot bend the translation.
- **Misses count as much as hits.** Every claim gets a verdict of holds, partial, missed, or too vague to judge. Most of the book describes mechanisms and history rather than forecasts, so many items will honestly land on "described pattern" or "too vague".
- **Everything is data.** Rewrite, anchors, and parallels are files; the site is generated from them. Updating research never means hand-editing the site.
- **Scripts for mechanics, agents for meaning.** Counts, number checks, footnote checks, and glossary greps are scripts. Agents are used only for judgment about meaning, tone, and sources.
- **Spelling:** American, except in the keep-list and direct quotations. (Change this one line in Step 1 if you prefer British; the source is British.)

### Run order and concurrency

- **Paragraph IDs are assigned in Step 1, Phase 1** (`ch05-p012`) and carried through every rewrite. That lets Step 2 start without waiting for the rewrite.
- **Step 2 starts as soon as Step 1 Phase 1 finishes**, in a separate session. It reads only `original/`, so it runs alongside the style bible, pilot, and full rewrite. Rewrite agents still never see the themes index.
- **Step 3's build script is written during the rewrite**, against `original/` text and a few stub parallels. Real data is swapped in when ready.
- **Cap concurrency at ~8–10 agents.** More just produces rate-limit retries.
- **Resume manifest:** `status.json` holds a state per unit (pending / rewritten / checked / fixed). Agents skip units whose output exists, so a crash costs minutes, not a rerun.
- **Fail fast with scripts.** Paragraph-ID, footnote, and number checks run before any verifier agent; a failing unit goes straight back to its rewriter.
- **Pipeline, don't batch.** Each unit goes rewrite, script checks, fresh reviewer, fix, without waiting for the other units.
- **Models:**

  | Job | Model |
  |---|---|
  | Rewrite, fidelity review, skeptic review | strongest |
  | Web research | mid-tier |
  | Slice-reading for glossary and theme candidates | cheaper |
  | Counts, IDs, numbers, footnotes, glossary grep | scripts, no model |

- **Only three human checkpoints:** the rewrite pilot, the combined themes-index and research pilot, and the one-chapter site preview. Extraction pauses only if it finds real problems.

### Source facts that drive the prompts

- Running headers look like `88 … Chapter 3`; footnote numbers are glued to the text (`crystallisation.47`).
- 8 parts, 33 chapters, ~70 sections. Almost every chapter exceeds 6,000 words (Ch. 10 alone is 30k+), so **the unit of work is the section**, not the chapter.
- There are no scenes, dialogue, or characters. The equivalents are quoted sources (Blue Books, factory inspectors, witnesses), named economists, and personified figures ("Mr. Moneybags", "the capitalist").
- Heavy footnotes with Greek, Latin, French, and German quotations; formulas (M–C–M′); numeric tables; British units (£ s. d., quarters, ells, yards).
- Seven prefaces and afterwords by Marx and Engels, in different voices.

### Checklist

- [ ] Step 1: extraction report reviewed (only if problems found)
- [ ] Step 2 started in a separate session once Step 1 Phase 1 is done
- [ ] Step 1, checkpoint: pilot files reviewed, style bible revised
- [ ] Step 1 complete: `modern-vol-1.md` assembled
- [ ] Step 2, checkpoint: themes index and five pilot parallels reviewed together
- [ ] Step 2 complete: `research-report.md` reviewed
- [ ] Step 3, checkpoint: one-chapter site reviewed in a browser
- [ ] Step 3 complete: site deployed
- [ ] Step 4 scheduled every 6 months

---

## Step 1: Rewrite

Produces the modernized book. One mandatory checkpoint (after the pilot); a second only if extraction shows real problems. Paste the whole block.

```
I want to rewrite Marx's Capital, Volume 1 (Moore/Aveling 1887 translation, public domain) in plain modern English. The source is das-capital-vol-1-original.pdf in this folder: 526 pages, about 340k words, with a real text layer (no OCR needed). Work through the phases in order. Stop only at the checkpoints marked CHECKPOINT.

## Ground rules

- Fidelity outranks readability. Every claim, argument step, example, qualification, hedge, number, and footnote in the original stays, with its strength unchanged ("may" does not become "will", "some" does not become "all"). Do not add opinions, modern examples, or interpretation. Do not cut ideas, even repeated ones: shorten wording, not content. Where Marx is ambiguous, stay ambiguous.
- Whose argument is it? Marx often works through an opponent's argument (Senior, Ricardo, Bastiat, Proudhon, Malthus, and others) before answering it. Keep clear who is speaking: never let an opponent's claim read as Marx's own, or the reverse.
- Tone: keep Marx's irony and polemic; do not flatten it into neutral prose. Keep the 19th-century setting.
- Register: a reader with no background in economics and a high-school reading level should follow every paragraph on first read: everyday words, short sentences, active voice. When an argument depends on a technical term, keep the term and explain it in plain words the first time it appears in each chapter, using the wording from the style bible's concepts list.
- Structure: each original paragraph has exactly one rewritten paragraph (which may be longer). Each footnote stays attached to the same paragraph with the same number. Chapter and section headings stay.
- Spelling: American, except inside the keep-list or direct quotations as noted in the style bible.
- Use scripts, not agents, for anything mechanical (counts, number checks, grep). Use agents for judgment about meaning.
- Paragraph IDs: every paragraph carries a stable ID line (see Phase 1). Rewrites keep each ID line exactly as it appears in the original.
- Concurrency and resume: run at most 8-10 subagents at once. Keep status.json with a state per unit (pending / rewritten / checked / fixed) and skip any unit whose output already exists, so an interrupted run can resume.
- Models: use the strongest model for rewriting and fidelity review; a cheaper model for slice-reading; scripts for anything mechanical.

## Phase 1: Extract and clean

Extract with pdftotext. Remove running headers (e.g. "88 ... Chapter 3"), footers, and page numbers. Rejoin hyphenated words and paragraphs split across pages. Preserve paragraph breaks, section headings, and italics if detectable. Footnote markers are glued to the text (e.g. "crystallisation.47"); convert them to a consistent marker such as [^47] and put the footnote text in a notes block directly after the paragraph that cites it.

Output, in original/:
- 00-front.md: title page, contents, and the seven prefaces/afterwords (Marx and Engels, different dates). Keep each as its own section; do not merge their voices.
- One file per chapter: ch01.md ... ch33.md (the book's own numbering).
- Any chapter over ~6,000 words is also split by its "Section N:" headings (ch10-s1.md, ...). If a single section is still over ~6,000 words, split it at a paragraph boundary and record where. The section file is the unit of work from here on.

Assign every paragraph a stable ID in the form ch05-p012, as an HTML comment on the line before it (<!-- ch05-p012 -->). Number paragraphs continuously through the whole chapter, across its section files, so IDs do not restart at section boundaries. Write anchors.json mapping each ID to its chapter and section file, paragraph index, and footnote numbers. Create status.json listing every file as pending.

Check that footnote numbering restarts correctly per chapter and that every marker has a footnote and vice versa. Preserve formulas, tables, and numeric examples exactly (M-C-M', "20 yards of linen = 1 coat", the working-day tables). Keep Greek, Latin, French, and German quotations intact.

Write extraction-report.md: file list with word counts, total words, paragraph and footnote counts per file, anything about markers, formulas, or tables you weren't sure how to handle, and any pages with suspected text problems.

Continue to Phase 2 unless the report shows real problems (broken footnotes, garbled tables, missing chapters). If it does, stop for my review. When Phase 1 is done, tell me so: I will start the Step 2 research session in parallel.

## Phase 2: Style bible

The book is roughly 450k tokens: do not read it all in one context. Have subagents each read a slice (a Part, or ~50 pages) and return candidate terms, idioms, recurring phrases, numbers/units, named people, and quotation patterns. Use a cheaper model for the slice-reading. Merge the results yourself and check a sample of entries against the text.

Write a draft style-bible.md as soon as the merge is done so the pilot can start from it; finalize it after the pilot checkpoint. Also write glossary.json (term, chosen rendering, variants to search for) from the glossary, so scripts and agents can use it directly. The bible contains:

1. Target register and fidelity rules (as above).
2. Quotation rules. How to treat (a) long quotations from Blue Books, factory inspectors, and witnesses, (b) quotations from economists, (c) foreign-language quotations (translate, and give the original in brackets), (d) personified figures such as Mr. Moneybags, "the capitalist", and "the labourer", and (e) verse. State what is paraphrased and what stays near-verbatim, and how quotes are marked so the reader always knows who is speaking.
3. Glossary: every archaic word, idiom, or recurring phrase used more than once, with ONE chosen modern rendering each. Settle early and fix: labour vs. labour-power; value / use-value / exchange-value; surplus-value; surplus-labour; constant and variable capital; "the labourer"; "the working class"; Hegelian vocabulary; "moment"; "metamorphosis"; and similar.
4. Keep-list: currency (pounds, shillings, pence), units (quarters, ells, yards), institutions, titles, place and period names.
5. People and sources: each named economist, official, or source Marx cites repeatedly, with one line on who they are and how Marx treats them (ally, opponent, authority, target of irony).
6. Three worked examples, each original vs. rewritten: (a) a descriptive or historical paragraph (e.g. from Ch. 10), (b) a passage with a long quotation, (c) the densest abstract passage (e.g. Ch. 1, section 4, fetishism). Show how footnotes are handled.
7. Concepts list: every technical term or idea the argument relies on, with a one- or two-sentence plain explanation checked against how Marx actually uses it. Rewrite agents reuse these wordings so the same idea is explained identically everywhere.
8. Expected length: rewrites should run roughly 1.2-1.5x the original. Flag any section outside that range.

## Phase 3: Pilot

Rewrite three files that stress different things:
- Ch. 1, section 4 (fetishism of commodities): the densest abstraction.
- Ch. 10 (the working day): heavy quotation, testimony, and irony.
- A footnote-heavy, polemical section against other economists (e.g. Ch. 3 or Ch. 15, section 6).

Run the three as parallel subagents using the Phase 4 procedure below (they need only the draft bible). Save to rewrite/.

CHECKPOINT: Stop. Tell me what you picked and why, which judgment calls the style bible didn't cover, and every place where simplifying risked changing the meaning and how you handled it. I'll review and we'll revise the style bible before the full run.

## Phase 4: Full rewrite with parallel subagents

Rewrite all remaining files as a pipeline, not in batches: each unit goes rewrite, script checks, fresh reviewer, fix, independently of the others, up to 8-10 units in flight. Skip units already marked done in status.json. Each rewrite subagent gets a fresh context and these instructions:

- Read style-bible.md in full.
- Read the original file.
- Read the last ~500 words of the previous file's ORIGINAL (not its rewrite) for continuity.
- Rewrite following the style bible exactly. Use glossary renderings verbatim, and the concepts-list explanation the first time each term appears in the chapter.
- Copy numbers, formulas, units, and foreign-language quotations exactly.
- Before saving, compare to the original paragraph by paragraph. Confirm no claim, qualification, or argument step was lost, added, strengthened, or weakened, and that each paragraph keeps its own footnotes. Fix anything that was.
- Write to rewrite/ with the same filename.
- If something comes up that the style bible doesn't cover, make a call and append it to notes/<filename>-notes.md. Do not edit the style bible.

As soon as a unit is written, run a script on that pair: identical paragraph ID lines in the same order, same footnote count and numbering, every number and formula in the original present in the rewrite, glossary.json renderings used. If it fails, send it straight back to its rewriter with the failures before any reviewer sees it. Update status.json.

Then a fresh reviewer (not the rewriter) takes each unit, or groups of ~5 consecutive units, and does the Phase 5 review below while other units are still being written.

## Phase 5: Consistency pass

1. Script: for every glossary entry, grep original/ and rewrite/ and list places where the chosen rendering was not used.
2. Collect notes/ and look for conflicting decisions across files.
3. Combined fidelity and drift review, run per group of ~5 consecutive files by fresh agents that did not do the rewriting (one read, two outputs). Fidelity, paragraph by paragraph for meaning only: lost or added claims, strengthened or weakened qualifications, inaccurate concept explanations, ambiguity resolved, and an opponent's claim attributed to Marx (or the reverse). Drift: reading level, voice, treatment of quotations and opponents' arguments, and tone against the style bible. Fidelity findings outrank readability findings.
4. Write consistency-report.md combining all of the above, then fix flagged passages with targeted edits. Don't re-rewrite whole files unless one is badly off.
5. Re-run the Phase 4 script checks after fixes.

## Phase 6: Assemble

Combine into modern-vol-1.md in order, with front matter and footnotes in place. Report final word count against the original (and against the 1.2-1.5x expectation) and anything unresolved.
```

---

## Step 2: Research parallels

Produces the themes index and one sourced, verdict-rated file per claim. Start as soon as Step 1 Phase 1 (extraction and paragraph IDs) is done, in a **separate session**, so it runs alongside the style bible, pilot, and full rewrite and the themes index never enters the rewrite's context. One checkpoint, after the themes index and five pilot items are ready.

```
The original is in original/ (chapter and section files, with footnotes attached to paragraphs and a paragraph ID line before each paragraph). A rewrite may be in progress in rewrite/ in another session: do not read it. Identify what the book claims and research how each claim holds up against the present day. Use at most 8-10 subagents at once.

Note: Capital is mostly analysis and history, not forecasting. Expect many items to be described patterns or mechanisms, and some to be too vague to judge. That is a valid and useful result.

## Phase A: Anchors

Paragraph IDs (ch05-p012) were assigned in original/ during extraction, and anchors.json already maps them. Verify that every ID is unique and that the IDs run continuously within each chapter. Fix and report any problems. Use these IDs for every reference below.

## Phase B: Themes index

Using subagents that each read a slice of original/ (never the rewrite), write themes-index.md listing:
- Major themes, each with anchor IDs.
- Explicit forecasts or claims about how society, politics, technology, work, or human behavior will develop, quoted from the original (short quotes only) with anchor IDs.
- Implicit arguments that could be tested against later history.
- Claims that are Marx's own versus claims he is attributing to an opponent. Do not list an opponent's argument as the book's claim.

For each item note specificity: concrete_forecast, general_warning, or described_pattern, and testable: yes or no (no = so general that almost any outcome would fit). Give each a stable ID (T01, T02, ...). Merge duplicates found by different slices, and keep the list to roughly 60-80 items. Do not research items marked testable: no; list them in the index with their verdict pre-set to too_vague_to_judge.

Do not stop here. Go straight to Phase C.

## Phase C: Pilot research

Pick 5 testable items: at least one concrete forecast, one general warning, and one described pattern. For each, use web search to research the current state of the world on that topic. Write parallels/<ID>.json:

{
  "id": "T07",
  "title": "short reader-facing title",
  "book_claim": "Marx's claim in your own words",
  "anchors": ["ch05-p012", "ch05-p013"],
  "specificity": "concrete_forecast | general_warning | described_pattern",
  "verdict": "holds | partial | missed | too_vague_to_judge",
  "parallel": "2-4 sentences on how it compares to today, in your own words",
  "reasoning": "why this verdict, including the strongest case against it",
  "present_day_topics": ["short topic labels a reader might start from"],
  "sources": [{"title": "", "url": "", "published": "YYYY-MM-DD"}],
  "researched_on": "YYYY-MM-DD"
}

Rules:
- Every factual claim about the present needs a source with a publication date. Prefer primary sources and established outlets. Open the page you cite; a search snippet is not a source.
- Paraphrase sources. No quotes longer than a short phrase; this will be published.
- "missed" and "too_vague_to_judge" are valid, useful outcomes. Do not stretch a vague claim to fit current events. If a claim would match many possible outcomes, say so.
- Separate what the book says from what you infer it means. Judge the claim as Marx made it, in his terms, not a later school's interpretation of it.
- This is a politically contested subject. Describe the facts and the main positions; don't editorialize, for or against the book.

CHECKPOINT: Stop and show me themes-index.md (count by specificity and testability, and the first 10 entries) together with the 5 pilot files. I'll adjust the standards before the full run.

## Phase D: Full research

Research all remaining testable items using parallel subagents (mid-tier model). Group 3-5 related items by present-day topic per subagent so they share searches and sources; with the instructions and rules above, each item still gets its own parallels file. Each subagent reads themes-index.md, the anchored passages in original/, and nothing from other parallels files.

## Phase E: Skeptic review

Start each review as soon as its research batch finishes, using the strongest model, with subagents that did not do the research. Each reviews a batch of parallels files and, for each: checks that sources support the claims made, checks whether the verdict is too generous (or too harsh), and looks for obvious counterexamples. Write review/<ID>.md. Update the parallels files where the review is right, and list in research-report.md every verdict that changed and why, plus the final count per verdict. Script check: every anchor in parallels/ resolves in anchors.json; every source has a URL and date.
```

---

## Step 3: Build the interactive site

Produces a static website generated from the data files. Write the build script while Steps 1 and 2 are still running, using `original/` text and a few hand-made stub parallels; swap in the real data when it's ready. One checkpoint after a single chapter.

```
Build an interactive reading experience as a static website (no backend, deployable to GitHub Pages or Netlify), in site/. Inputs: rewrite/ and original/ files, anchors.json, themes-index.md, and parallels/*.json. If rewrite/ or parallels/ is incomplete, build against original/ and stub data, and make the build script skip missing files with a warning so it works at any stage.

Features:
1. Reader: the modernized text, chapter by chapter and section by section, with a table of contents covering the front matter, 8 parts, and 33 chapters. Footnotes render inline or as expandable notes next to their paragraph. Paragraphs with linked parallels show a subtle margin marker; clicking opens a side panel with the parallel, verdict, reasoning, sources, and "as of" date.
2. Original toggle: show the original paragraph alongside the modern one, per paragraph or for the whole chapter.
3. Themes view: every theme and claim, filterable by verdict (holds / partial / missed / too vague) and specificity, each linking to its passages.
4. Start from today: a list of present-day topics drawn from present_day_topics; choosing one jumps into the relevant passages.
5. Verdicts must be visually even-handed. Misses get the same prominence as hits. No colors that read as "good" for holds and "bad" for missed.
6. Every parallel shows its researched_on date, and a note when it is older than 6 months.
7. Make clear that the modern text is a plain-language rewrite and link to the original; include a short "about" page stating the fidelity rules.

Generate the site from the data files with a build script, so re-running research and rebuilding updates the site with no manual edits. Readable typography for long-form reading, works on phones, keyboard accessible, no tracking scripts.

CHECKPOINT: Build only the reader for one chapter that has several parallels (e.g. Ch. 10) plus the themes view. Start a local preview server and tell me the URL. Stop and let me review it in a browser before building the rest.

Then complete all features, run the build, and check every anchor in parallels/ resolves to a real paragraph. Write README.md explaining how to rebuild and deploy.
```

---

## Step 4: Refresh

Run every ~6 months (or schedule it). The site already flags parallels older than 6 months; this step clears the flags.

```
Refresh the parallels. For every parallels/*.json whose researched_on is more than 6 months old:
- Re-research the current state of the topic with web search, following the Step 2 rules (dated, opened sources; paraphrase; misses and "too vague" are valid).
- Update parallel, reasoning, sources, and researched_on. If the verdict changed, record the old one in a "history" array with its date and the reason for the change. Do not silently rewrite earlier verdicts.
- Check that every previously cited URL still resolves; replace dead ones.
- Run an independent skeptic pass on any item whose verdict changed.

Then rebuild the site, confirm every anchor still resolves, and write refresh-report.md: items refreshed, verdict changes, dead links fixed, and items that no longer seem testable.
```
