# Pilot checkpoint (Phase 3)

## What was rewritten and why

| Unit | Why it was picked | Script check | Review |
|---|---|---|---|
| `ch01-s4.md`: Ch. 1 §4, fetishism of commodities | The densest abstraction in the book, with Robinson Crusoe, Aristotle, and attacks on Bailey, Bastiat, and the "economic discoverers" | PASS, ratio 1.02 | minor fixes: 1 medium + 2 low fidelity, 4 low drift. All applied. |
| `ch10-s3.md`: Ch. 10 §3, industries without legal limits | Heaviest testimony in Ch. 10 (pottery children, match-makers, bakers, Mary Anne Walkley, railway men), inspectors' Blue Book quotations, and sustained irony | PASS, ratio 1.03 | minor fixes: 4 low fidelity, 2 low drift. All applied. |
| `ch15-s6.md`: Ch. 15 §6, the compensation theory | Polemic against James Mill, MacCulloch, Torrens, Senior, and J. S. Mill; free indirect speech for the "bourgeois economist"; Bill Sykes's invented speech; census table; 14 footnotes | PASS, ratio 1.01 | minor fixes: 3 low fidelity, 1 low drift. All applied. |

Each unit went through the full Phase 4 procedure: an Opus rewriter, the script check, a fresh Opus reviewer, and targeted fixes applied by the original rewriter. The status of each is `fixed` in status.json.

## Judgment calls the draft bible didn't cover

1. **Length target.** The faithful rewrites run 1.01–1.03×, not 1.2–1.5×. Splitting sentences and swapping archaic words does not add words. The reviewers found nothing dropped. **Proposal:** change §8 to ~0.95–1.25×, and flag units above 1.3× as padding and below 0.95× as lost content.
2. **Readability versus fidelity.** Ch. 1 §4 still averages about 21–26 words per sentence, and some sentences run over 45 words where splitting would resolve an ambiguity (e.g. the "therefore" clause in ch01-p136). The rewriters chose to keep the ambiguity. **Decision needed:** confirm that ambiguity beats sentence length when the two conflict.
3. **Ordinary vs technical sense of a §7 term.** "manufacture" (the making of matches, wallpaper) in Ch. 10, and "metamorphosis" (the switch to machinery) in Ch. 15, appeared first in their ordinary sense. The rewriters gave no technical explanation or only the general part of it. The context script cannot tell the senses apart. **Proposal:** add a rule to §7.0 to explain only at the first *technical* use.
4. **Neutral identifications (§1.1 c) are used a lot:**
   - lucifer matches, wallpaper, the Borough, assizes, the carrying trades, navvies
   - Bill Sykes "(the murderer in Dickens's *Oliver Twist*)", Dogberry "(the constable in Shakespeare's …)"
   - Physiocrats, suzerains, tithe
   - corporate character "(its organization as a guild)"

   They help, but they add up. **Decision needed:** keep this level, or limit identifications to one per term per chapter and never in quotations.
5. **Medical and technical words inside testimony:** "phthisis" → "tuberculosis" and "dyspepsia" → "indigestion" (Dr. Arledge, ch10-p053), while "scrofula" and "consumption" were kept. The reviewer accepted this under §2.1. **Decision needed:** replace inside quotations, or keep the original word with a bracketed gloss ("phthisis [tuberculosis]")? The gloss form is the safer choice for fidelity.
6. **Mention versus use.** When Marx comments on an English word itself, the word stays even though the glossary has a rendering. Examples: "sophisticated" goods with a pun on "sophistry" (ch10-p066), and ironic "liberated"/"sets free" (ch15-p149). **Proposal:** add this as a general rule.
7. **Scare quotes.** The draft §3.3 told rewriters to put "setting free" and "temporary inconvenience" in quotes everywhere, and one rewriter added quotation marks Marx doesn't use. The reviewer caught it. §3.3 is already corrected: quotation marks only where Marx uses them.
8. **Typo fixes beyond characters:** a stray word "in" in Otley's quotation (ch10-p063), and a stray comma in ch15-p156. **Proposal:** allow these one-reading fixes, logged in notes.
9. **Stray punctuation in the source:** an unmatched closing quotation mark in ch01 n. 31 was kept, and "319, 222" in ch15 n. 137 was kept as printed. **Proposal:** keep both, log them, and do not guess.
10. **Outdated ethnic names:** "American red-skins" → "the Native Americans" in Marx's voice (ch10-p040), while the quoted text keeps its wording. "Like Jews in the pores of Polish society" (ch01-p145) was kept unchanged. **Decision needed:** confirm the §4 default.
11. **Marx's interjections inside quotations,** e.g. "(he means his 'hands'…)", "(iterum Crispinus)". Interjections take American spelling; the quoted words keep British. **Proposal:** add this to §1.5.
12. **The word "economy"** means the science in "bourgeois economy" and "classical economy", which became "economics". It means the economic system elsewhere, where it stays "economy". **Proposal:** add this to the glossary.
13. **Glosses for foreign set phrases not in §3.4:** *Nota bene* → "Note well"; *cultus* [worship]; Intermundia [the spaces between the worlds]; Tagwanne [a day's work]. The reviewer corrected a first guess, "day's winnowing". **Proposal:** when unsure of a foreign gloss, write the safest literal gloss and log it.
14. **Italics in a quotation's citation, and "&c." inside truncated titles,** stay as printed. The script warns on these; the warnings are expected. **Proposal:** make the checker ignore "&c." inside quotation marks and notes' citation parentheses.

## Every place where simplifying risked changing the meaning, and how it was handled

### ch01-s4

- **n. 34:** the pairing "here politics, and there Catholicism" was first rewritten so that it **reversed** Marx's pairing. The reviewer caught it, and it was fixed to "politics … in the ancient world, and Catholicism in the middle ages". *This was the only medium-severity error in the pilot.*
- **p136:** "…an established social fact, and therefore the private useful labour … ranks on an equality". The "therefore" could be part of the condition or a consequence. Kept so that both readings remain, and the 50-word sentence was left unsplit on purpose.
- **p138:** the bare "And why?" was kept, because it could ask about either of two things.
- **p152:** "belongs to them" could mean belongs to the objects or to the men. Kept ambiguous, because this is the economists' inverted view, which Marx mocks.
- **p141:** "moderate" was first rewritten as "modest", which changes the trait. Fixed to "Frugal".
- **p148:** "course of exchange" → "exchange rate". The 19th-century sense is the exchange rate, so the risk is low; logged.
- **n. 31:** this is a quotation from Marx's own *Zur Kritik*. It had been reworded too freely and was restored to near-verbatim.
- **n. 29:** Engels's "by periodical revolutions" had been changed to "through". It was restored word for word.
- **n. 32/33:** the §7 gloss for "classical political economy" was put in n. 32, although Marx defines the term himself in n. 33. Borderline but defensible; the reviewer accepted it.

### ch10-s3

- **p040:** "the tendency to the extension of the working day" had been made stronger ("drive"). Fixed back to "tendency".
- **p072:** "it will be understood that the Report classes bakers…" had become "why", which added a reason. Fixed back to "that".
- **p077:**
  - "torpor" → "numbness" had narrowed the meaning. Fixed to "a stupor".
  - "The negligence of the employee" was kept singular, although three men stand trial. It may be the official formula, so it was left ambiguous.
- **n. 43:** scare quotes had been added around "genuine". Removed.
- **p053:** in Dr. Arledge's testimony, "phthisis" and "dyspepsia" were replaced with modern words (decision 5 above).
- **p071:** "corporate character" could be misread as a modern business corporation. A short gloss was added: "(its organization as a guild)".
- **p061:** Marx's mocking interjections inside Mr. Smith's quotation were all kept in place, so the reader can tell his voice from Smith's.

### ch15-s6

- **p153:** the four "since…" premises belong to the bourgeois economist, but he is named only at the end of the sentence. They were kept in one sentence of short clauses so they don't read as Marx's own assertions.
- **p154:**
  - The conclusion "whoever exposes… is an enemy of social progress!" is the economist's, given in free indirect speech. "by his reasoning" was added so that it can't be read as Marx's claim.
  - "festive board" → "dinner table" had lost the mock-pompous tone. Fixed to "feast table".
- **p159:** the rewrite had made growing wealth the cause of the new luxurious wants. In the original it supplies only the means to satisfy them. Fixed.
- **p148, p154:** scare quotes Marx doesn't use had been added. Removed, and the bible corrected.
- **p146:** "metamorphosis" is used here in the ordinary sense, so only the general part of the §7 gloss was used.
- **n. 139:** "operative iron founders" was rendered as "working iron founders", not the glossary's "factory workers". The glossary rendering would have been wrong.

## Tooling fixes made during the pilot

- **Number checker:** it counted trailing commas as part of a number, which forced needless rephrasing in ch15-s6. Fixed.
- **Bible §3.3:** the scare-quote wording was corrected.
