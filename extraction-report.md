# Extraction report (Phase 1)

Source: `das-capital-vol-1-original.pdf`, 526 pages. It is a Word export of the marxists.org edition (Progress Publishers, "First English edition of 1887 (4th German edition changes included as indicated) with some modernisation of spelling"), with a real text layer.

## How it was extracted

- `pdftohtml -xml` gives every text run with its position, font, size, and italic/bold flags. `scripts/lines.py` rebuilds lines from that, and `scripts/extract.py` turns lines into headings, paragraphs, and endnotes. `scripts/build_files.py` writes `original/`, `anchors.json`, and `status.json`. `scripts/check_original.py` checks the result. The large intermediate files were deleted after the run. To regenerate them: `pdftohtml -xml -i -q das-capital-vol-1-original.pdf work/full && python3 scripts/lines.py work/full.xml work/lines.json && python3 scripts/extract.py work/lines.json work/doc.json` (do not re-run `build_files.py` over the edited `original/00-front.md` without checking the diff).
- **Removed:** running headers (page number + "Chapter N" at the top of each page), blank footers, and Word's endnote separator lines.
- **Paragraphs:** a new paragraph starts where the gap between lines is larger than normal line spacing (23–24 px against 18–20). A paragraph continues across a page break only when the last line on the page is fully justified. Block quotations (indented 51 px) are `> ` paragraphs. Each one is its own paragraph with its own ID, as in the source layout. **Note:** `>` records *indentation in the source layout*, not who is speaking. The PDF also indents some passages where Marx is speaking, and some that mix narration and quotation (e.g. ch10-p044, "Fifteen hours of labour for a child 7 years old! J. Murray, 12 years of age, says: …"). The speaker has to be read from the quotation marks and attributions in the text.
- **Hyphens:** the source has no soft hyphenation, so every hyphen at a line end is a real compound hyphen (`co-operation`, `labour-power`). Lines are joined with the hyphen kept and no space.
- **Italics:** `*…*` (394 spans, taken from the font flags). Bold appears only in a few headings and in table labels.
- **Footnotes:** the source has endnotes at the end of each chapter, numbered from 1 in each chapter. Superscript markers become `[^N]`. Each note's text is placed in a notes block directly after the first paragraph that cites it. Multi-paragraph notes use 4-space continuation indents.
- **Headings:** `#` Part, `##` Chapter, `###` Section, `####` lettered sub-sections (A., B., …), `#####` numbered sub-sub-sections. All were detected from fonts.
- **IDs:** `<!-- chNN-pNNN -->` sits before every paragraph, block quote, table, and formula block. Numbering runs through each whole chapter across its section files. The Part 7 introduction, which comes before Chapter 23, uses `pt7-p001…p005` and sits at the top of `ch23a.md`.

## Integrity checks: all pass

- All 33 chapters are present. There are 1,823 paragraph IDs, continuous within every chapter.
- There are 1,110 footnotes. Every marker has a note in the same file, every note has a marker, and there are no duplicate labels. Numbering starts at 1 in each chapter and runs without gaps, with the one exception listed below.
- A word-inventory comparison against plain `pdftotext` output finds no missing text. The only differences are running headers and hyphen handling.

## Things I was not sure how to handle (decisions made)

1. **Front matter.** By design the source PDF and this project contain no prefaces or afterwords: the PDF runs from the contents (pp. 1–5) straight to Part 1. `00-front.md` holds the title page and contents only.
2. **Tables (38)** are kept as ` ```text ` blocks with their columns rebuilt from positions. All numbers are kept exactly; layout is approximate. Some complex tables (Ch. 25 §5 F tables A–E, the Ch. 10 note 140 Greenhow table, the Ch. 15 §7 import/export tables) have column headers that wrap over several rows. They are readable but not grid-perfect. Rewriters will be told to copy tables unchanged and translate only the prose labels if the bible says so.
3. **Formula and diagram blocks (27)** keep their line breaks (backslash hard breaks). Examples: `20 yards of linen = 1 coat`, form C of value, `C–M–C`, the Ch. 11 formula for S, and the Ch. 18 formulae. Ch. 1's form C and money form are drawn with braces in the source and are kept as text tables. **Fractions** in Ch. 18, 20, and 21 are printed as a numerator over a denominator on two lines. They stay as two stacked lines, e.g. `daily value of labour-power` over `working day of a given number of hours`. Ch. 18 p. 353: one prose line ("From formulae II. we get very differently,") sits between two formula tables and was taken into the table block.
4. **Unnumbered `*` notes** (editorial notes from Engels or marxists.org) become `[^*1]` per chapter: Ch. 1 (first-edition passage), Ch. 17 ("Earlier English translations have '6 sh.'…"), Ch. 31 ("Industrial here in contradistinction to agricultural").
5. **Lettered notes** `26a` (Ch. 1), and `43a` and `43b` (Ch. 3), keep their labels.
6. **Heading notes:** Ch. 33's title carries note 1, and Ch. 3 §2's heading "B. The currency of money" carries note 26 (translator's note). The marker stays in the heading, and the note text goes after the first paragraph under it.
7. **Subscripts** in chemical formulas (C₄H₈O₂ in Ch. 1, CₙH₂ₙ₊₂ in Ch. 11 note) are written as `<sub>…</sub>`.

## Source problems found (not extraction errors)

- **Ch. 3, note 17:** the label is printed as "1\7" in the PDF. It is read as 17 (it is the note to the sentence "the value also of each single yard…", and it is the only note 17).
- **Ch. 31:** notes start at 2. The source's note at the position of 1 is the unnumbered `*` note. This is left as is.
- **Greek in Symbol font (pp. 73, 238–239):** Ch. 3 §2 note 16 (Heraclitus) and Ch. 14 §5 notes 55–57 (Homer, Archilochus, Thucydides, Plato) were typed in the Symbol font. They were decoded to Greek letters, but **accents and breathings are lost**, and the source transcription itself is faulty (`χ` for `κ`, etc.). Other Greek in the book (Aristotle in Ch. 1 and Ch. 4, Ch. 3 note) is proper Unicode and intact.
- **Possible OCR-era typos in tables:** Ch. 25 Table A "28,8211" before note 120 and "122,8501". Each looks like a figure followed by a stray digit. They are kept exactly as printed.
- **Page-boundary paragraph joins to verify** (the last line on the page was full width, so the text was joined): ch01-p093, ch09-p017, ch15-p017, ch33-p006, and the ch10 join at pp. 147–148. In each case the line was justified, so a merge is likely correct, but a sentence ends exactly at the page edge.

## Units over ~6,000 words, and how they were split

The limit used was 6,500 words including notes ("~6,000"). Long chapters were split by "Section N" headings. A section still too long was split at its lettered sub-section headings, with small neighbours merged. A piece still too long was split into balanced parts at a paragraph boundary, never right after a lead-in that ends in ":" or a dash. Splits:

- ch01-s3a.md: ch01-p037..ch01-p066 (3379 words), starts at the section start
- ch01-s3b.md: ch01-p067..ch01-p094 (3527 words), starts at a paragraph boundary
- ch01-s3c.md: ch01-p095..ch01-p130 (3434 words), starts at a sub-section heading
- ch03-s2a.md: ch03-p024..ch03-p046 (4980 words), starts at the section start
- ch03-s2b.md: ch03-p047..ch03-p062 (5403 words), starts at a sub-section heading
- ch03-s2c.md: ch03-p063..ch03-p070 (2395 words), starts at a sub-section heading
- ch03-s3a.md: ch03-p071..ch03-p093 (5764 words), starts at the section start
- ch03-s3b.md: ch03-p094..ch03-p099 (1997 words), starts at a sub-section heading
- ch10-s5a.md: ch10-p110..ch10-p121 (3094 words), starts at the section start
- ch10-s5b.md: ch10-p122..ch10-p134 (3438 words), starts at a paragraph boundary
- ch10-s6a.md: ch10-p135..ch10-p175 (4401 words), starts at the section start
- ch10-s6b.md: ch10-p176..ch10-p200 (4583 words), starts at a paragraph boundary
- ch13a.md: ch13-p001..ch13-p011 (3385 words), starts at the section start
- ch13b.md: ch13-p012..ch13-p028 (3163 words), starts at a paragraph boundary
- ch15-s1a.md: ch15-p001..ch15-p013 (3411 words), starts at the section start
- ch15-s1b.md: ch15-p014..ch15-p024 (3651 words), starts at a paragraph boundary
- ch15-s3a.md: ch15-p037..ch15-p060 (3993 words), starts at the section start
- ch15-s3b.md: ch15-p061..ch15-p070 (2886 words), starts at a sub-section heading
- ch15-s3c.md: ch15-p071..ch15-p096 (4246 words), starts at a sub-section heading
- ch15-s8a.md: ch15-p192..ch15-p222 (4362 words), starts at the section start
- ch15-s8b.md: ch15-p223..ch15-p242 (4837 words), starts at a sub-section heading
- ch15-s9a.md: ch15-p243..ch15-p269 (5610 words), starts at the section start
- ch15-s9b.md: ch15-p270..ch15-p311 (5642 words), starts at a paragraph boundary
- ch23a.md: pt7-p001..ch23-p011 (3394 words), starts at the section start
- ch23b.md: ch23-p012..ch23-p025 (3282 words), starts at a paragraph boundary
- ch25-s5a.md: ch25-p078..ch25-p105 (2361 words), starts at the section start
- ch25-s5b.md: ch25-p106..ch25-p151 (5574 words), starts at a sub-section heading
- ch25-s5c.md: ch25-p152..ch25-p166 (2410 words), starts at a sub-section heading
- ch25-s5d.md: ch25-p167..ch25-p200 (6201 words), starts at a sub-section heading
- ch25-s5e.md: ch25-p201..ch25-p246 (4838 words), starts at a paragraph boundary
- ch25-s5f.md: ch25-p247..ch25-p307 (5556 words), starts at a sub-section heading
- ch27a.md: ch27-p001..ch27-p009 (4138 words), starts at the section start
- ch27b.md: ch27-p010..ch27-p018 (4541 words), starts at a paragraph boundary

Three units are slightly over 6,000 words but under the 6,500 limit, and were left whole: ch01-s4 (fetishism), ch07-s2, and ch25-s5d.

## Files

| File | Words | Paragraphs | Footnotes |
|---|---:|---:|---:|
| 00-front.md | 1320 | – | – |
| ch01-s1.md | 2903 | 19 | 13 |
| ch01-s2.md | 2929 | 17 | 4 |
| ch01-s3a.md | 3422 | 30 | 4 |
| ch01-s3b.md | 3551 | 28 | 4 |
| ch01-s3c.md | 3524 | 36 | 2 |
| ch01-s4.md | 6495 | 22 | 12 |
| ch02.md | 4439 | 16 | 13 |
| ch03-s1.md | 4737 | 23 | 15 |
| ch03-s2a.md | 5023 | 23 | 10 |
| ch03-s2b.md | 5417 | 16 | 8 |
| ch03-s2c.md | 2407 | 8 | 5 |
| ch03-s3a.md | 5800 | 23 | 22 |
| ch03-s3b.md | 2009 | 6 | 8 |
| ch04.md | 4476 | 26 | 14 |
| ch05.md | 5535 | 23 | 25 |
| ch06.md | 4628 | 20 | 14 |
| ch07-s1.md | 3967 | 24 | 10 |
| ch07-s2.md | 6396 | 32 | 9 |
| ch08.md | 5804 | 24 | 8 |
| ch09-s1.md | 3996 | 20 | 9 |
| ch09-s2.md | 1513 | 16 | 0 |
| ch09-s3.md | 2912 | 6 | 3 |
| ch09-s4.md | 395 | 2 | 1 |
| ch10-s1.md | 1883 | 13 | 6 |
| ch10-s2.md | 3640 | 26 | 24 |
| ch10-s3.md | 6192 | 45 | 29 |
| ch10-s4.md | 3988 | 25 | 12 |
| ch10-s5a.md | 3141 | 12 | 11 |
| ch10-s5b.md | 3457 | 13 | 15 |
| ch10-s6a.md | 4457 | 41 | 20 |
| ch10-s6b.md | 4626 | 25 | 33 |
| ch10-s7.md | 2492 | 10 | 16 |
| ch11.md | 4005 | 19 | 8 |
| ch12.md | 4489 | 16 | 8 |
| ch13a.md | 3400 | 11 | 11 |
| ch13b.md | 3175 | 17 | 11 |
| ch14-s1.md | 1399 | 7 | 1 |
| ch14-s2.md | 1357 | 7 | 5 |
| ch14-s3.md | 4015 | 14 | 18 |
| ch14-s4.md | 4224 | 11 | 14 |
| ch14-s5.md | 4732 | 23 | 24 |
| ch15-s1a.md | 3441 | 13 | 14 |
| ch15-s1b.md | 3660 | 11 | 8 |
| ch15-s2.md | 3974 | 12 | 15 |
| ch15-s3a.md | 4049 | 24 | 23 |
| ch15-s3b.md | 2907 | 10 | 14 |
| ch15-s3c.md | 4282 | 26 | 22 |
| ch15-s4.md | 4457 | 12 | 15 |
| ch15-s5.md | 4583 | 36 | 20 |
| ch15-s6.md | 4104 | 20 | 14 |
| ch15-s7.md | 5374 | 27 | 20 |
| ch15-s8a.md | 4442 | 31 | 19 |
| ch15-s8b.md | 4899 | 20 | 29 |
| ch15-s9a.md | 5664 | 27 | 28 |
| ch15-s9b.md | 5660 | 42 | 3 |
| ch15-s10.md | 1231 | 2 | 2 |
| ch16.md | 4767 | 36 | 12 |
| ch17.md | 5080 | 34 | 9 |
| ch18.md | 1496 | 24 | 4 |
| ch19.md | 3421 | 20 | 10 |
| ch20.md | 3775 | 20 | 15 |
| ch21.md | 3968 | 25 | 20 |
| ch22.md | 2106 | 16 | 6 |
| ch23a.md | 3413 | 16 | 7 |
| ch23b.md | 3298 | 14 | 13 |
| ch24-s1.md | 3958 | 36 | 11 |
| ch24-s2.md | 1484 | 9 | 7 |
| ch24-s3.md | 3611 | 28 | 16 |
| ch24-s4.md | 4854 | 29 | 14 |
| ch24-s5.md | 1484 | 6 | 8 |
| ch25-s1.md | 4587 | 15 | 10 |
| ch25-s2.md | 3068 | 17 | 2 |
| ch25-s3.md | 5411 | 21 | 8 |
| ch25-s4.md | 3500 | 24 | 10 |
| ch25-s5a.md | 2401 | 28 | 15 |
| ch25-s5b.md | 5641 | 46 | 28 |
| ch25-s5c.md | 2433 | 15 | 1 |
| ch25-s5d.md | 6257 | 34 | 32 |
| ch25-s5e.md | 4853 | 46 | 12 |
| ch25-s5f.md | 5616 | 61 | 23 |
| ch26.md | 1445 | 9 | 1 |
| ch27a.md | 4167 | 9 | 18 |
| ch27b.md | 4556 | 9 | 15 |
| ch28.md | 3847 | 15 | 7 |
| ch29.md | 1290 | 2 | 3 |
| ch30.md | 1992 | 3 | 8 |
| ch31.md | 4854 | 31 | 15 |
| ch32.md | 1307 | 4 | 2 |
| ch33.md | 4312 | 13 | 23 |
| **Total (90 files)** | **339249** | **1823** | **1110** |

The original PDF has about 340,200 words by `pdftotext` count. The ~1,000-word difference is running headers and page numbers.
