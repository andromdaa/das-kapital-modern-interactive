# Style Bible: Plain-English *Capital*, Vol. 1

Status: **FINAL v1.0** (finalized after the pilot checkpoint; the decisions taken at the checkpoint are in §0). Rewrite agents must read this whole file before starting. Do not edit it. Record new decisions in `notes/<filename>-notes.md`.

---

## 0. Decisions taken at the pilot checkpoint (summary)

1. **Length target** is ~0.95–1.25× (§8). Faithful plain rewrites barely add words.
2. **Technical explanations** go only at the first *technical* use of a term in a chapter, not at an everyday use of the same word (§7.0).
3. **Mention vs use.** When Marx talks *about* a word (puns on it, mocks it, quotes it as someone's term), the word itself stays, even if the glossary has another rendering (§1.2).
4. **Inside quotations, obsolete words are glossed, not replaced.** Keep the original word and add a bracketed plain word: "phthisis [tuberculosis]" (§2.1, §2.2).
5. **Outdated ethnic and religious names** follow the §4 default: neutral modern name in Marx's voice, original wording inside quotations.
6. **Ambiguity beats sentence length.** If splitting a sentence would settle an ambiguity Marx leaves open, leave it long and log it.
7. **One-reading typos** (a stray letter, word, or punctuation mark with only one possible correction) may be fixed and must be logged. Unclear oddities stay as printed and are logged (§1.4).
8. **Neutral identifications** (§1.1 c): at most once per item per chapter, never inside a quotation (use a bracket after the quoted word instead), and only when the passage cannot be followed without it.
9. **Marx's interjections inside quotations** (his parenthetical remarks) are Marx's voice: American spelling, plain style. The quoted words around them keep their wording and spelling.
10. **"economy"** meaning the science (bourgeois economy, classical economy, vulgar economy) → "economics". Meaning the economic system → "economy" (§3.1).
11. **Unsure foreign glosses:** give the safest literal gloss and log it. Never guess an etymology.

---

## 1. Target register and fidelity rules

### 1.1 Fidelity comes first

Fidelity outranks readability, every time.

- **Keep everything.** Every claim, argument step, example, qualification, hedge, number, name, date, and footnote stays. Shorten *wording*, never *content*. Repeated ideas stay repeated: Marx often repeats on purpose.
- **Keep strength exactly.** "may" stays "may" (not "will"). "some" stays "some" (not "all"). "as a rule" stays "as a rule". "almost" stays "almost". "it appears" stays "it appears". "tends to" stays "tends to". A rhetorical question stays a question. An exclamation stays an exclamation.
- **Add nothing.** No opinions, no modern examples, no interpretation, no "in other words, Marx means…", no summaries, no transitions that make a logical link the original does not make. If Marx writes "Hence" or "therefore", keep the inference. If he does not, do not add one.
- **Keep ambiguity.** Where Marx is ambiguous, stay ambiguous. If you cannot tell which of two readings he means, choose wording that allows both. Never quietly pick one.
- **Allowed additions:** only (a) the plain explanation of a technical term the first time it appears in a chapter (§7 wording, verbatim or near-verbatim), (b) a bracketed translation of foreign-language text (§2.3), and (c) a few neutral words that name an institution or obsolete thing a modern reader cannot know (e.g. "the Corn Laws (the tariffs on imported grain)"). Each addition must be short, factual, and free of evaluation. Add a neutral identification at most once per item per chapter, only when the passage cannot be followed without it, and never inside a quotation: there, use a bracketed gloss after the word instead.

### 1.2 Who is speaking

Marx constantly states an opponent's view before answering it, often in that opponent's own words or in mocking paraphrase. The reader must always be able to tell who is speaking.

- Keep every attribution ("says Senior", "according to Mill", "our friend Moneybags thinks", "the apologist replies"). If a long sentence must be split, repeat the attribution in the new sentence ("Senior goes on…", "Mill claims…").
- Keep every quotation mark, including Marx's ironic scare quotes ("abstinence", "free" labourer, "hands", "the sacred rights of property"). Scare quotes are how Marx signals that a word is the opponent's, not his.
- **Free indirect speech.** Sometimes Marx voices an opponent without quotation marks ("What, exclaimed one of their spokesmen, Mr. Malthus preaches high rents…!"). Keep it clearly marked as the opponent's speech. Keep the tag ("exclaimed one of their spokesmen") next to it. Never smooth it into a neutral statement that could read as Marx's own claim.
- **Irony.** Never turn ironic praise into literal praise, or literal praise into irony. "Our friend", "the worthy", "this excellent man", "the millennium", "the sycophant" are mockery and stay mockery. Keep the mocking tone, but do not explain the joke.
- **Hypotheticals.** Hypotheticals and assumptions stay marked as such ("Let us suppose…", "Assume that…", "if, as the economists claim…").
- **Mention versus use.** When Marx comments on an English word itself (puns on it, mocks it, or marks it as someone else's term), that word stays as printed, even if the glossary gives another rendering. Examples: "sophisticated" goods with the pun on "sophistry"; the economists' "liberated"/"sets free"; "abstinence". You may add the plain sense next to it if Marx does not already give it.
- **Ambiguity beats sentence length.** If splitting a long sentence would force one reading of a clause Marx leaves open, keep the sentence long and log it in notes.
- **Paragraph layout.** The `>` at the start of a paragraph reproduces the source's **indented layout**. It does **not** say who is speaking. Some indented paragraphs are Marx's own narration, or mix narration with testimony (e.g. "Fifteen hours of labour for a child 7 years old! J. Murray, 12 years of age, says: …"). Keep the `>` exactly where it is, and work out the speaker from the quotation marks and attributions.

### 1.3 Register

The reader has a high-school reading level and no background in economics. They should be able to follow every paragraph on a first read.

- Use everyday words, short sentences, and active voice. Aim for about 15–22 words per sentence on average. Split Marx's long periodic sentences into several sentences, but keep every clause's content and the logical connectors between them ("because", "but", "so", "although", "on the other hand").
- Turn passive voice into active when the agent is stated or obvious from the same sentence. If the original hides the agent, do not invent one: keep the passive.
- Turn abstract nouns into verbs where the meaning stays the same ("the conversion of money into capital" → "turning money into capital").
- Spell out Latin abbreviations in Marx's voice (§3.4).
- **Tone.** Keep Marx's irony, sarcasm, indignation, metaphors, and images: werewolf ("were-wolf"), vampire, Juggernaut, "stands on its head", "dripping from head to foot, from every pore, with blood and dirt". Plain does not mean flat. If a metaphor is clear, keep it word for word. If an image depends on a lost reference, keep the image and add a few neutral words of identification only if needed (§1.1 c).
- **Setting.** Keep the 19th-century setting: shillings, quarters of wheat, factory inspectors, the Poor Law, steam-engines. Do not modernize the world, only the language.

### 1.4 Structure

These are checked by script, and a unit that fails goes back to the rewriter.

- **One paragraph in, one paragraph out.** Each original paragraph becomes exactly one rewritten paragraph, which may be longer. Never merge or split paragraphs.
- **ID lines.** Copy every `<!-- chNN-pNNN -->` line exactly, in the same order, directly above its paragraph.
- **Footnotes.** Keep every footnote marker `[^N]` (also `[^26a]`, `[^*1]`) in the same paragraph, at the matching point in the sentence. Keep each `[^N]: …` notes block directly after the same paragraph, with the same label. Rewrite footnote prose in the same plain style (§2.6).
- **Headings.** Keep every heading with the same `#` level. Heading wording stays as printed, with only American spelling applied ("Labour" → "Labor", "Colonisation" → "Colonization").
- **Markup.** Keep `>` block-quote markers, `\` hard line breaks in formulas and verse, `*italics*`, `**bold**`, `<sub>` and `<sup>`.
- **Tables and diagrams.** Copy every ` ```text ` block **exactly**, character for character, including any spelling errors.
- **Formulas and figures.**
  - Copy every number, formula, and unit **exactly**: `C–M–C`, `M–C–M′`, `20 yards of linen = 1 coat`, `s/v`, `£1 9s. 0d.`, `10½`, `1/20`, `27 working days`.
  - Do not turn digits into words, or words into digits.
  - Do not round, convert, or "correct" arithmetic or facts.
  - **One-reading typos** may be fixed and must be logged in your notes file: a character typo (`£4OO` → `£400`, "p. Ixxi" → "p. lxxi"), a stray word ("9 p.m. in would suit us"), or a stray comma. Anything with more than one possible reading stays as printed and is logged: an unmatched quotation mark, a number with a stray space ("319, 222"), or an odd figure in a table.

### 1.5 Spelling

Use American spelling in Marx's voice and in footnote prose: labor, labor-power, worker, center, realize, civilization, color, favor, program, jail, wagon, defense.

Keep the original spelling in three places:
- inside direct quotations, which are another person's words;
- inside titles of books and documents;
- in keep-list items (§4).

So a quoted inspector still writes "labour". Marx's own interjections inside a quotation, such as "(he means his 'hands')", are his voice and take American spelling; the quoted words around them keep theirs.

---

## 2. Quotation rules

Every quotation keeps its quotation marks and its attribution, so the reader always knows who is speaking. Quotations sit in their paragraph exactly where they are. Marx's comment is never merged into a quotation, and a quotation is never merged into Marx's comment.

### 2.1 Long quotations from Blue Books, factory inspectors, commissioners, doctors, and witnesses

These are evidence. Keep them **near-verbatim**.

- **Allowed changes:**
  - **Gloss, don't replace.** For a word a modern reader cannot decode at all (obsolete, medical, technical, or dialect), keep the original word and add the plain word in square brackets right after it: "phthisis [tuberculosis]", "dyspepsia [indigestion]", "victuals [food]", "hinds [farm laborers]". Gloss each word once per quotation. Trade words and the keep-list (§4) stay unglossed unless they are unreadable. Words that are merely old-fashioned but clear ("overlooker", "masters") stay unglossed.
  - Split a very long sentence at a natural break.
  - Modernize punctuation.
- **Not allowed:** summarizing, compressing, or dropping any fact, name, age, hour, wage, place, date, or question number ("(ns. 115, 116)", "Evidence, p. 16"). Keep the order of statements.
- **Children's and workers' testimony** keeps its own plain, broken, or dialect voice ("gi'en over", "I have not been in bed since the night before last"). Do not tidy it into educated English. If a dialect word cannot be understood, add the plain word in square brackets right after it: "gi'en [given] over".
- **Ellipses.** Keep the source's ellipses (`...` or `....`) and bracketed interpolations ("[sic.!]"). Note: a parenthesis that sits *outside* the quotation marks is Marx's own remark, not the quoted writer's.
- **Spelling.** Keep British spelling inside the quotation (§1.5).

### 2.2 Quotations from economists and other writers (Senior, Ricardo, Smith, Mill, Malthus, Ure, Bastiat, Proudhon, Say, Roscher, etc.)

Keep these **near-verbatim**. Marx often attacks the exact words, so the words must survive.

- **Change only:**
  - a sentence order that hides the meaning.
  - For an archaic word a modern reader cannot decode, keep it and add a bracketed gloss, as in §2.1.
- **Never change** a word that Marx mocks, repeats, or argues with ("abstinence", "the last hour", "labour fund", "remuneration", "the natural price of labour").
- If the quotation is already readable, leave it word for word, apart from punctuation.
- Keep attribution tags, and repeat them when splitting.

### 2.3 Foreign-language quotations (Latin, Greek, French, German, Italian, Spanish)

- Keep the foreign text **exactly as printed**, including accents, and including the defective Symbol-font Greek in Ch. 3 n. 16 and Ch. 14 nn. 55–57.
- Give a plain English translation in square brackets right after it: *Non olet* [It does not smell].
- If the source already gives a bracketed translation, keep the foreign text and rewrite only the bracketed translation into plain English.
- Translate literally. If the foreign text says something slightly different from Marx's paraphrase of it, translate what it says, not what Marx says about it.
- If you are unsure of a word, give the safest literal gloss and log it. Never guess from an etymology.
- **Foreign tags in Marx's own voice** are single words or set phrases used as ordinary vocabulary: *caeteris paribus*, *pari passu*, *quâ*, *vice versâ*, *pro tanto*, *en masse*, *post festum*, *ad libitum*, *voilà tout*.
  - Replace them with plain English (§3.4 list), unless they work as a quotation or a famous tag.
  - Famous tags and mottos stay in the original with a bracketed translation: *Hic Rhodus, hic salta!*, *De te fabula narratur*, *auri sacra fames*, *Non olet*, *Determinatio est negatio*, *Après moi le déluge!*, *Accumulate, accumulate! That is Moses and the prophets!*. The last one is English and stays verbatim.
- German technical words Marx quotes (e.g. *Tagwerk*, *Wertsein*) stay, with a bracketed gloss.

### 2.4 Personified figures

Keep personifications and their tone. Do not turn them into plural abstractions ("capitalists in general").

| Original | Rendering |
|---|---|
| Mr. Moneybags, "our friend Moneybags" | Mr. Moneybags, our friend Moneybags |
| "the capitalist", "our capitalist" | the capitalist, our capitalist |
| "the labourer", "our labourer" | the worker, our worker |
| capital as vampire, were-wolf | keep the image word for word |
| commodities that "speak", "love money", "go to market" | keep: commodities speak, flirt, go to market |
| the weaver, the linen-weaver, the Bible-seller, the distiller | keep |
| "the economist", "the vulgar economist", "the apologist" | keep |

If a figure "speaks" in Marx's invented dialogue (e.g. the capitalist's speech in Ch. 7 §2, or the worker's speech in Ch. 10 §1), keep the dialogue form and its quotation marks. Keep the speaker clear at every turn.

### 2.5 Verse

- **English verse:** keep it verbatim, with its line breaks. That covers Shakespeare, Goethe in English, Hood, the Bible, and old ballads. Add a bracketed plain gloss only for a word a modern reader cannot decode at all.
- **Foreign verse:** follow §2.3. Keep the original lines, then give a bracketed translation.

### 2.6 Footnotes

- Rewrite footnote **prose** (Marx's or Engels' comments, and arguments carried on in notes) by the same rules as the main text.
- Keep **citations exactly as printed**: author, title, place, year, volume, page, and edition. Titles are not modernized or translated, apart from expanding the abbreviations listed in §3.4 when they stand outside a title.
- Expand these abbreviations outside titles:
  - "l.c." / "l. c." → "cited above"
  - "ib." / "ibid." → "same source"
  - "Lond." → "London"
  - "sq." / "sqq." / "seq." → "and following"
  - "Conf." / "Cf." → "Compare"
  - "&c." → "etc."
  - "p." and "pp." stay.
- Editorial notes stay attributed exactly: "[Engels, 4th German Edition]", "F. E.", "– Note by editors of MECW", "Note by the Institute of Marxism-Leninism…", "Translator's note". So do the editors' bracketed glosses inside the text ("[the Royal “we”…]"). Never let an editor's note read as Marx's.

---

## 3. Glossary: one rendering each

Use these renderings **verbatim**. The machine-readable copy is `glossary.json`; the script checks the starred (★) entries and fails a unit that misses them. Inside direct quotations and titles the original wording is allowed (§1.5).

### 3.1 Core technical terms (★ = enforced by script)

| Original (variants) | Rendering | Note |
|---|---|---|
| labour (the activity), Labour | **labor** | American spelling; not "work" when Marx means labour as a category |
| labour-power, labour power ★ | **labor-power** | always hyphenated; never "labor" alone when the original says labour-power |
| value ★ | **value** | |
| use-value, use value, value in use ★ | **use-value** | |
| exchange-value, exchange value ★ | **exchange-value** | |
| surplus-value ★ | **surplus-value** | |
| surplus labour, surplus-labour ★ | **surplus labor** | |
| necessary labour ★ | **necessary labor** | |
| labour-time, labour time ★ | **labor-time** | |
| socially necessary labour-time ★ | **socially necessary labor-time** | |
| working-time | **working time** | |
| labour-process ★ | **labor process** | |
| working day, working-day ★ | **working day** | |
| constant capital ★ | **constant capital** | |
| variable capital ★ | **variable capital** | |
| rate of surplus-value ★ | **rate of surplus-value** | |
| absolute / relative surplus-value ★ | **absolute / relative surplus-value** | |
| means of production ★ | **means of production** | |
| means of subsistence ★ | **means of subsistence** | |
| mode of production ★ | **mode of production** | |
| commodity, commodities ★ | **commodity, commodities** | |
| magnitude of value ★ | **magnitude of value** | Keep: "magnitude" is defined in §7 |
| form of value, value-form, value form | **form of value** | |
| relative form (of value) ★ | **relative form of value** | |
| equivalent form ★ | **equivalent form** | |
| universal equivalent ★ | **universal equivalent** | |
| money-form, money form | **money form** | |
| price-form | **price form** | |
| abstract human labour, human labour in the abstract, abstract labour ★ | **abstract human labor** | |
| subject of labour (the material worked on), instruments of labour | **object of labor**, **instruments of labor** | Added in Phase 4: "subject" misleads modern readers. Keep "subject of labour" inside quotations. |
| useful labour, concrete labour | **useful labor**, **concrete labor** (as printed) | |
| metamorphosis, metamorphoses ★ | **metamorphosis, metamorphoses** | |
| circulation (of commodities) ★ | **circulation** | |
| medium of circulation | **medium of circulation** | |
| measure of value(s) | **measure of value** | |
| standard of price | **standard of price** | |
| means of payment ★ | **means of payment** | |
| hoard, hoarding, hoarder | **hoard, hoarding, hoarder** | |
| universal money, world money | **world money** | |
| capital | **capital** | |
| the capitalist | **the capitalist** | |
| the labourer, labourers ★ | **the worker, workers** | |
| workman, workmen, workpeople | **worker(s)** | |
| operative(s), factory operative(s) | **factory worker(s)** | |
| "hands" | **"hands"** inside quotations and when Marx is mocking the employers' word; otherwise **workers** | |
| wage-labourer | **wage worker** | |
| wage-labour | **wage labor** | |
| the working class, working-class ★ | **the working class**, **working-class** (adjective) | |
| the labouring class(es), labouring population | **the working class**, **the working population** | |
| productiveness of labour ★ | **productivity of labor** | |
| productive power(s) of labour | **productive power of labor** | |
| intensity of labour | **intensity of labor** | |
| value of labour-power ★ | **value of labor-power** | |
| price of labour, value of labour | **price of labor**, **value of labor** | Keep exactly: Marx calls these expressions irrational |
| wages, time-wage(s), piece-wage(s) | **wages, time wages, piece wages** | |
| nominal / real wages | **nominal / real wages** | |
| paid / unpaid labour | **paid / unpaid labor** | |
| dead labour / living labour | **dead labor / living labor** | |
| value-product | **value-product** | |
| self-expansion (of value / of capital) | **self-expansion** | |
| the circuit M–C–M | **the circuit M–C–M** | |
| co-operation ★ | **cooperation** | |
| division of labour ★ | **division of labor** | |
| manufacture (the period / form, Part 4) ★ | **manufacture** | The ordinary verb "to manufacture" is fine |
| manufactory | **manufacturing workshop** | |
| detail labourer ★ | **detail worker** | |
| collective labourer ★ | **collective worker** | |
| handicraft, handicraftsman | **handicraft, craftsman** | |
| Modern Industry, modern industry ★ | **modern industry** | |
| the factory system | **the factory system** | |
| machinery, machine, motor mechanism, transmitting mechanism, working machine (tool or machine) | as printed | |
| relay system, shift system | **relay system, shift system** | |
| domestic industry, home-work | **domestic industry** | |
| accumulation (of capital) ★ | **accumulation** | |
| simple reproduction ★ | **simple reproduction** | |
| reproduction on a progressive / extended scale | **reproduction on an extended scale** | |
| concentration / centralisation (of capital) ★ | **concentration / centralization** | |
| composition of capital (technical, value-, organic) ★ | **technical / value / organic composition of capital** | |
| relative surplus population, surplus-population ★ | **relative surplus population** | |
| industrial reserve army ★ | **industrial reserve army** | |
| floating, latent, stagnant (forms of surplus population) | **floating, latent, stagnant** | |
| pauperism | **pauperism** | |
| primitive accumulation ★ | **primitive accumulation** | Keep "so-called" where Marx writes it |
| expropriation | **expropriation** | |
| fetishism (of commodities) ★ | **fetishism of commodities** | |
| political economy, Political Economy | **political economy** | |
| economy (meaning the science: bourgeois / classical / vulgar / modern economy) | **economics** | When "economy" means the economic system, keep **economy** |
| classical political economy | **classical political economy** | |
| vulgar economy, vulgar economist(s) ★ | **vulgar economics**, **vulgar economist(s)** | |
| bourgeois (economy, economist, society) | **bourgeois** | |
| proletariat, proletarian | **proletariat, proletarian** | |
| revenue | **revenue** | Keep. Marx flags its double sense in Ch. 24 n. 19 |
| abstinence (Senior) | **"abstinence"** | Always keep the word, usually in quotation marks |
| labour fund | **labor fund** | Keep "so-called" |
| corvée | **corvée** | |
| truck system | **truck system** | |
| gang-system, gang-master | **gang system, gang-master** | |

### 3.2 Hegelian and philosophical vocabulary

Translate the sense. Never add Hegelian jargon that is not there.

| Original | Rendering |
|---|---|
| moment (Hegelian sense: an element, phase, or aspect of a process) | **element** or **phase**, whichever fits. Choose by context and keep one choice within a paragraph. The ordinary sense ("at this moment") stays "moment". |
| phenomenal form, form of appearance, form of manifestation | **form of appearance** |
| immanent | **built-in** ("immanent laws" → "the built-in laws") |
| antithesis, antagonism | **opposition**, **antagonism** (keep "antagonism" for class antagonism) |
| contradiction | **contradiction** |
| reflex, reflex categories | **reflection**, **reflex categories** (with the king-and-subjects example kept intact) |
| negation of the negation | **negation of the negation** (keep; it is a quoted Hegelian formula) |
| transubstantiation, metempsychosis, chrysalis, *salto mortale* | keep the image; gloss once in plain words if needed ("*salto mortale* [death-defying leap]") |
| personification, personified | **personification, personified** |
| subjective factor / objective factor (of the labor process) | **subjective factor / objective factor** |
| determination (quantitative determination of value) | **determining**, **fixing** ("the quantitative determination of value" → "how the amount of value is fixed") |
| social hieroglyphic | **social hieroglyph** |
| *a priori* / *a posteriori* | **in advance** / **after the fact** |

### 3.3 Archaic words and recurring phrases

These are not script-enforced; reviewers check them. Trade and institution words in §4 stay.

| Original | Rendering |
|---|---|
| corn (= grain in general) | **grain**. Keep "corn" in "Corn Laws", in "corn-dealer" etc. inside quotations, and in fixed units ("a quarter of corn" → "a quarter of grain") |
| commerce | **trade** |
| intercourse (social / commercial) | **dealings**, **exchange**, or **trade**, as fits |
| whilst | **while** |
| hitherto | **until now** / **so far** |
| nay | **indeed**, or **even** |
| so soon as | **as soon as** |
| in so far as | **to the extent that** / **insofar as** |
| the former / the latter | name the thing again whenever that is clearer |
| it is evident that, it is plain that | **clearly** (the claim's strength must not change) |
| quantum | **amount** |
| aliquot part | **fractional part** / **share** (corrected in Phase 4: Marx often uses it loosely for parts that are not equal) |
| sophisticated (of bread etc.) | **adulterated** |
| masters | **employers** (keep "masters" inside quotations) |
| overlooker | **overseer** |
| hind(s) | **farm laborer(s)** |
| cot / cottage | **cottage** |
| privy | **outdoor toilet** |
| gaol | **jail** |
| turned off (dismissed) | **dismissed** |
| bagmen, hawkers (as jibes) | **traveling salesmen**, **peddlers** (keep the sneer) |
| the apologists | **the apologists** (defenders of the system) |
| setting free (of workers by machines) | **setting free**. Use quotation marks only where Marx uses them; never add scare quotes he does not use. |
| temporary inconvenience | **temporary inconvenience**. Use quotation marks only where Marx uses them. |
| the lion's share | **the lion's share** |

### 3.4 Latin and other abbreviations and tags (in Marx's own voice and in footnote prose)

| Original | Rendering |
|---|---|
| &c. | **etc.** |
| viz. | **namely** |
| i.e. | **that is** |
| e.g. | **for example** |
| l.c., l. c. | **cited above** |
| ib., ibid. | **same source** |
| sq., sqq., seq. | **and following** |
| cf., conf. | **compare** |
| *quâ* | **as** / **in its capacity as** |
| *vice versâ* | **the other way round** |
| *pro tanto* | **to that extent** |
| *caeteris paribus* | **other things being equal** |
| *pari passu* | **at the same pace** |
| *en masse* | **all together**, **in a mass** |
| *post festum* | **after the event** |
| *ad libitum* | **at will** |
| *gratis* | **free of charge** |
| *per diem / per annum* | **per day / per year** |
| *quid pro quo* (= mix-up) | **mix-up**, or **one thing taken for another** |
| *nec plus ultra* | **the very height** |
| *in propriâ personâ* | **in person** |
| *mutatis mutandis* | **with the necessary changes** |
| *voilà tout* | keep, with [that's all] |
| *faux frais* | **overhead costs** (keep *faux frais* only when quoted) |

---

## 4. Keep-list (do not modernize, convert, or translate)

- **Currency:**
  - £, s., d., "sh.", "pounds", "shillings", "pence", "farthing", "guinea", "sovereign", "crown", "florin"
  - francs (fr.), centimes, thalers, groschen, livres, sous, marks, rupees, dollars
  - Keep the original notation: "£1 9s. 0d.", "3s. 6d.", "4½d.", "fr. 1,068".
- **Units:**
  - quarter (of wheat/grain), bushel, peck, ell, yard, foot (ft.), inch, mile, acre, rood, perch, lb., ounce (oz.), cwt. (hundredweight), ton, stone
  - grain (unit of weight), pint, gallon, hogshead, horse-power, spindle, loom
  - Keep the abbreviations as printed.
- **Institutions, laws, and offices:**
  - Parliament, House of Commons, House of Lords, Privy Council, Home Secretary, Chancellor of the Exchequer
  - Factory Acts (and named Acts: Ten Hours' Bill / Act, Printworks' Act, Bleaching and Dyeing Works Act, Mines Act, Bank Act of 1844)
  - Factory Inspectors, sub-inspectors, Children's Employment Commission, Royal Commission, Select Committee
  - Blue Books, Reports of the Inspectors of Factories, Public Health Reports, Medical Officer of the Privy Council
  - Poor Law, workhouse, Board of Guardians, parish, poor-rates, overseers of the poor, settlement and chargeability
  - Corn Laws, Statute of Labourers, enclosure, commons, copyhold, freehold, yeomanry, tithe, quit-rent, demesne
  - Star Chamber, justices of the peace, magistrates, the Great Unpaid
  - Bank of England, Lombard Street, the Funds, the National Debt, Inland Revenue, income-tax Schedules A–E
  - Chartism / Chartists, Tories, Whigs, Free-traders, Anti-Corn-Law League, trades' unions, Exeter Hall
  - *Règlement organique*, Boyards, corvée
- **Titles and forms of address:** Mr., Mrs., Dr., Sir, Lord, Lady, Earl, Duke, Duchess, Rev., M.P., Esq., Professor, Bishop, King, Queen.
- **Places and period names, as printed:** the Potteries, Staffordshire, Lancashire, the Black Country, East End, Hindostan/India (as printed), Danubian Principalities, the Highlands, Ireland, the middle ages, the manufacturing period, the Restoration, the "Glorious Revolution", the Reformation, the Anti-Jacobin War.
- **Trade and machine names:** mule, self-acting mule ("self-actor"), throstle, power-loom, hand-loom, jenny, piecer, scavenger, jigger, mould-runner, dipper, fustian-cutting, lace-finishing, straw-plaiting, scutching mill, puddler, navvy, truck shop.
- **Outdated ethnic and religious names** (confirmed at the checkpoint): keep the term **inside quotations**. In Marx's own voice, use the neutral modern name and log it in notes: "red-skins" → "Native Americans", "Hindoos" → "Hindus", "Mahometan" → "Muslim", "Esquimaux" → "Inuit". Never change the claim made about the group.

---

## 5. People and sources

How each recurring figure is treated decides the tone. These treatments describe how *Marx* treats them; the rewrite must keep that treatment and never strengthen or soften it.

### 5.1 Economists and theorists

| Name | Who | Marx's treatment |
|---|---|---|
| Adam Smith | Scottish classical economist, *Wealth of Nations* (1776) | Respected founder of classical political economy. Praised for real insights, criticized sharply for errors (e.g. "Adam Smith's dogma" on the price of commodities). |
| David Ricardo | English classical economist, *Principles* (1817) | Treated with great respect as a scientific economist. Criticized for not asking where surplus-value comes from and for treating capitalism as natural. Defended against Bailey. |
| Thomas Robert Malthus | Parson-economist, *Essay on Population* | Opponent. Treated with contempt as a plagiarist and an apologist for landlords and the rich. Sometimes quoted as a useful witness. |
| Nassau W. Senior | Oxford professor | **Prime target of irony.** "Senior's last hour" (Ch. 9), "abstinence" (Ch. 24). His own words are quoted and then demolished. |
| John Stuart Mill | *Principles of Political Economy* | Opponent and target of irony: "as much at home in absurd contradictions, as he feels at sea in the Hegelian contradiction" (Ch. 24 n. 28). Quoted as raising an honest doubt about machinery (Ch. 15). |
| James Mill | Ricardian | Opponent (compensation theory, wages fund). |
| J. R. McCulloch (MacCulloch) | Ricardian popularizer | Target of irony ("the Scotch genius MacCulloch"). |
| Col. Robert Torrens | Economist | Opponent, mocked. |
| J. B. Say | French economist | Target of irony. |
| Frédéric Bastiat | French free-trade economist | Target of irony, called a "bagman" of free trade. |
| Wilhelm Roscher | German "historical" economist | Target of ridicule ("Herr Roscher"). |
| Pierre-Joseph Proudhon | French socialist | Opponent; his "eternal justice" and schemes are mocked. |
| Samuel Bailey | Critic of Ricardo | Opponent on value. |
| Destutt de Tracy | French philosopher-economist | Called "the fish-blooded bourgeois doctrinaire"; target. |
| Henry C. Carey | American economist | Target ("Mr. Carey and other harmonisers", "H. Carey, the Yankee"). |
| Andrew Ure | *Philosophy of Manufactures* (1835) | Apologist for the factory system. **Quoted as a witness against itself**, with heavy irony ("the Pindar of the automatic factory"). |
| Charles Babbage | Mathematician, *Economy of Machinery* | Neutral or authoritative source. |
| Henry Fawcett | Cambridge professor | Target of irony. |
| E. G. Wakefield | Theorist of "systematic colonization" | Ch. 33 target. Marx uses him as a witness who unwittingly reveals the truth about capital. |
| Sir F. M. Eden | *The State of the Poor* (1797) | Source of facts, and target of irony for his complacency. |
| Rev. J. Townsend, Bernard de Mandeville, Storch, Sismondi, Steuart, Petty, Barbon, Locke, North, Galiani, Verri, Quesnay, Mercier de la Rivière, Le Trosne, Condillac, Turgot, Boisguillebert, Vanderlint, Postlethwayt, Ferguson, Dugald Stewart, Garnier, R. Jones, Ramsay, Cherbuliez, Rossi, Hodgskin, Dunning | Earlier economists and writers | Mostly cited as sources or witnesses. Treatment varies by passage: keep whatever the passage shows (praise for Petty and Sismondi; irony for Mandeville's frankness and Townsend's "parson" logic). |

### 5.2 Officials, investigators, and politicians

| Name | Who | Marx's treatment |
|---|---|---|
| Leonard Horner | Factory Inspector | **Ally and authority**, praised for honesty. |
| Alexander Redgrave, Robert Baker, Sir John Kincaid, R. J. Saunders, Howell | Factory Inspectors | Authorities, quoted as evidence. Occasionally ironic when they echo the employers. |
| Dr. John Simon, Dr. Greenhow, Dr. Julian Hunter, Dr. Edward Smith, Dr. Richardson, Dr. Lee, H. S. Tremenheere, J. E. White, F. D. Longe, Scriven | Medical officers and commissioners | Authorities, quoted at length as evidence. |
| Lord Ashley (Earl of Shaftesbury) | Tory factory reformer | Treated as a reformer, but with irony where his philanthropy serves Tory interests. |
| John Bright, Richard Cobden | Free-trade leaders | Targets of irony ("perjured Free-traders"). |
| W. E. Gladstone | Chancellor of the Exchequer | Target. His budget speeches are quoted against him. |
| Sir Robert Peel | Prime Minister, Bank Act 1844 | Neutral or ironic. |
| Edmund Burke, Lord Macaulay | Writer / historian | Targets ("the sycophant", "systematic falsifier"). |
| Edmund Potter | Manchester manufacturer | Target, quoted at length (Ch. 23). |
| E. F. Sanderson, Naylor & Vickers, J. Ellis, "Mr. Smith" of Manchester | Employers | Their own testimony is quoted against them, with irony. |
| Duchess of Sutherland, Lord Dufferin | Landowners | Targets. |

### 5.3 Witnesses and allies

| Name | Who | Marx's treatment |
|---|---|---|
| Child and adult witnesses (William Wood, J. Murray, Fernyhough, Mary Anne Walkley, etc.) | Witnesses in the official reports | Quoted with sympathy. Their words are evidence; keep them near-verbatim (§2.1). |
| Frederick Engels | Marx's collaborator | Ally. *The Condition of the Working Class in England* is cited as an authority. His editorial notes are signed "F. E." or "[Engels…]" and must stay attributed. |
| Robert Owen, Fourier, Saint-Simon | Socialists | Treated with respect, though not uncritically. |
| Aristotle, Hegel, Spinoza, Plato, Xenophon, Thucydides, Luther | Philosophers and writers | Cited as thinkers. Aristotle is praised ("the great thinker"). Plato is treated with mild irony in Ch. 14. |

### 5.4 Official sources

| Source | Description |
|---|---|
| "Reports of the Inspectors of Factories" ("Reports, &c.") | Half-yearly official reports. Keep citation forms exactly. |
| "Children's Employment Commission" ("Ch. Empl. Comm."), First to Sixth Reports (1863–67) | Keep citation forms exactly. |
| "Public Health" Reports (Privy Council), Census of England and Wales, Inland Revenue reports, Agricultural Statistics (Ireland) | Keep citation forms exactly. |
| *The Times*, *Morning Star*, *Daily Telegraph*, *Reynolds' Newspaper*, *The Economist*, *Standard*, *Spectator* | Newspapers. Keep names in italics or quotation marks as printed. |

---

## 6. Worked examples

The examples below show the target. Notice what does *not* change: numbers, IDs, footnote labels, quotation marks, attributions, citation details, foreign text, and the strength of every claim.

### 6(a) Descriptive / historical paragraph: Ch. 10, ch10-p156

**Original**

```
<!-- ch10-p156 -->
The years 1846-47 are epoch-making in the economic history of England. The Repeal of the Corn Laws, and of the duties on cotton and other raw material; Free-trade proclaimed as the guiding star of legislation; in a word, the arrival of the millennium. On the other hand, in the same years, the Chartist movement and the 10 hours’ agitation reached their highest point. They found allies in the Tories panting for revenge. Despite the fanatical opposition of the army of perjured Free-traders, with Bright and Cobden at their head, the Ten Hours’ Bill, struggled for so long, went through Parliament.
```

**Rewrite**

```
<!-- ch10-p156 -->
The years 1846-47 opened a new era in the economic history of England. In those years the Corn Laws (the tariffs on imported grain) were repealed, along with the duties on cotton and other raw materials. Free trade was proclaimed the guiding star of all legislation. In a word, the millennium had arrived. On the other hand, in those same years the Chartist movement and the agitation for a 10-hour day reached their highest point. They found allies in the Tories, who were hungry for revenge. The army of Free-traders, oath-breakers with Bright and Cobden at their head, opposed the bill fanatically. Despite them, the Ten Hours' Bill, fought for over so long, passed through Parliament.
```

**Why**
- "the arrival of the millennium" is irony and stays irony. It is not explained.
- "perjured" becomes "oath-breakers": plainer, with the same accusation.
- The only addition is the neutral gloss on the Corn Laws (§1.1 c).
- "Tories panting for revenge" keeps its sneer. The rewrite does **not** say what they wanted revenge for, because Marx does not say.
- "10" and "1846-47" are copied as digits.

### 6(b) Passage with a long quotation and an opponent's voice: Ch. 24 §3, ch24-p062 to ch24-p063, ch24-p067 to ch24-p068

**Original**

```
<!-- ch24-p062 -->
The capitalists having long been good livers and men of the world, uttered loud cries. What, exclaimed one of their spokesmen, a disciple of Ricardo, Mr. Malthus preaches high rents, heavy taxes, &c., so that the pressure of the spur may constantly be kept on the industrious by unproductive consumers! By all means, production, production on a constantly increasing scale, runs the shibboleth; but

<!-- ch24-p063 -->
> “production will, by such a process, be far more curbed in than spurred on. Nor is it quite fair thus to maintain in idleness a number of persons, only to pinch others, who are likely, from their characters, if you can force them to work, to work with success.”[^26]

[^26]: “An Inquiry into those Principles Respecting the Nature of Demand, &c.,” p. 67.

<!-- ch24-p067 -->
> “I substitute,” he proudly says, “for the word capital, considered as an instrument of production, the word abstinence.”

<!-- ch24-p068 -->
An unparalleled sample this, of the discoveries of vulgar economy! It substitutes for an economic category, a sycophantic phrase – *voilà tout.* [that’s all]
```

**Rewrite**

```
<!-- ch24-p062 -->
The capitalists had long since become men of the world who liked to live well, and they raised a loud outcry. One of their spokesmen, a follower of Ricardo, cried out: What! Mr. Malthus preaches high rents, heavy taxes, etc., so that unproductive consumers can keep the spur constantly pressed into the side of the industrious! By all means production, production on an ever-growing scale, so goes the slogan; but

<!-- ch24-p063 -->
> “production will, by such a process, be held back far more than it is spurred on. Nor is it quite fair to keep a number of persons idle in this way, only to pinch others, who are likely, from their characters, if you can force them to work, to work with success.”[^26]

[^26]: “An Inquiry into those Principles Respecting the Nature of Demand, &c.,” p. 67.

<!-- ch24-p067 -->
> “I substitute,” he proudly says, “for the word capital, considered as an instrument of production, the word abstinence.”

<!-- ch24-p068 -->
Here is a matchless sample of the discoveries of vulgar economics! It puts a fawning phrase in the place of an economic category – *voilà tout* [that’s all].
```

**Why**
- **Who speaks in p062:** first Marx (the capitalists' outcry), then the Ricardian spokesman in free indirect speech. The tag "cried out" keeps him clearly marked. His sentence runs on into the quotation in p063, so p062 must still end with "but" and no full stop. Never "fix" this.
- **The quotation (p063)** is near-verbatim. Only "curbed in" and "maintain in idleness" were loosened; "pinch" stays. Its spelling and its quotation marks stay.
- **Senior's sentence (p067)** is already plain and contains the word Marx attacks ("abstinence"), so it stays word for word.
- **Footnote [^26]:** its citation is copied exactly, "&c." included, because it is inside a title. It stays attached after the same paragraph.
- **p068:** "vulgar economy" → "vulgar economics" (glossary). In the full chapter, its §7 explanation is added the first time the term appears in Ch. 24. *voilà tout* stays, with its bracket.

### 6(c) Dense abstract passage: Ch. 1 §4 (fetishism), ch01-p137 with footnote 28

**Original**

```
<!-- ch01-p137 -->
Hence, when we bring the products of our labour into relation with each other as values, it is not because we see in these articles the material receptacles of homogeneous human labour. Quite the contrary: whenever, by an exchange, we equate as values our different products, by that very act, we also equate, as human labour, the different kinds of labour expended upon them. We are not aware of this, nevertheless we do it.[^28] Value, therefore, does not stalk about with a label describing what it is. It is value, rather, that converts every product into a social hieroglyphic. Later on, we try to decipher the hieroglyphic, to get behind the secret of our own social products; for to stamp an object of utility as a value, is just as much a social product as language. The recent scientific discovery, that the products of labour, so far as they are values, are but material expressions of the human labour spent in their production, marks, indeed, an epoch in the history of the development of the human race, but, by no means, dissipates the mist through which the social character of labour appears to us to be an objective character of the products themselves. The fact, that in the particular form of production with which we are dealing, viz., the production of commodities, the specific social character of private labour carried on independently, consists in the equality of every kind of that labour, by virtue of its being human labour, which character, therefore, assumes in the product the form of value – this fact appears to the producers, notwithstanding the discovery above referred to, to be just as real and final, as the fact, that, after the discovery by science of the component gases of air, the atmosphere itself remained unaltered.

[^28]: When, therefore, Galiani says: Value is a relation between persons – “La Ricchezza e una ragione tra due persone,” – he ought to have added: a relation between persons expressed as a relation between things. (Galiani: Della Moneta, p. 221, V. III. of Custodi’s collection of “Scrittori Classici Italiani di Economia Politica.” Parte Moderna, Milano 1803.)
```

**Rewrite**

```
<!-- ch01-p137 -->
So when we bring the products of our labor into relation with each other as values, it is not because we see these things as mere material containers of uniform human labor. Quite the opposite. Whenever we exchange our different products and so treat them as equal values, by that very act we also treat the different kinds of labor spent on them as equal, as human labor. We are not aware of this, but we do it.[^28] Value, then, does not walk around with a label saying what it is. Rather, it is value that turns every product into a social hieroglyph, a sign whose meaning is hidden. Later on, we try to decode the hieroglyph and get behind the secret of our own social products. For stamping a useful object as a value is just as much a social product as language is. Science has recently discovered that the products of labor, so far as they are values, are only the material expressions of the human labor spent in producing them. This discovery does mark an epoch in the history of human development. But it by no means clears away the mist through which the social character of labor looks to us like a property of the products themselves. In the particular form of production we are dealing with, namely the production of commodities, private labor is carried on independently, and its specific social character consists in the equality of every kind of such labor as human labor; in the product, this character therefore takes the form of value. To the producers, despite the discovery just mentioned, this fact seems just as real and final as another fact: that after science discovered the gases that make up air, the air itself stayed exactly as it was.

[^28]: So when Galiani says that value is a relation between persons – “La Ricchezza e una ragione tra due persone” [“Wealth is a relation between two persons”] – he ought to have added: a relation between persons expressed as a relation between things. (Galiani: Della Moneta, p. 221, V. III. of Custodi’s collection of “Scrittori Classici Italiani di Economia Politica.” Parte Moderna, Milano 1803.)
```

**Why**
- **Sentence by sentence:** one 100-word sentence became three. Every element survives: the specific form of production, independent private labor, equality as human labor, value as the product's form, the producers' view, "despite the discovery", and the air analogy. The analogy keeps its exact logical role: the producers' view is compared with a *fact* (the air stays unchanged), not with a mistake.
- **Hedges kept:** "so far as they are values" and "by no means" survive. "We are not aware of this, but we do it" keeps Marx's flat, unhedged claim.
- **Term handling:** "social hieroglyphic" is glossed once, in plain words, as an image. It is not turned into a theory.
- **Footnote [^28]:** the Italian is kept exactly, with a literal bracketed translation. The translation says "Wealth" because the Italian says *Ricchezza*, even though Marx paraphrases it as "value". The citation is untouched.
- **First use in the chapter:** in a full chapter rewrite, "value", "use-value", "abstract human labor", and "commodity" would already have been explained earlier in Ch. 1. In ch01-s4 (a separate file), add the §7 explanations at the first appearance of any term not yet explained in that chapter's *earlier files*. See §7.0.

---

## 7. Concepts list

### 7.0 How to use this list

- **First technical use only.** Many listed words also have everyday senses: "manufacture" (making something), "metamorphosis" (any change), "circulation", "accumulation", "capital" (a capital city), "value" (worth in general). Explain a term only at its first use in the **technical sense** Marx gives it. An everyday use earlier in the chapter does not count, and gets no explanation. The context file lists terms by word-matching, so it may list an everyday use: check the sense yourself.
- **First use in each chapter.** The first time a listed term appears in its technical sense in a chapter, explain it using the wording below, verbatim or with only grammatical adjustment. Work it into the sentence, or add a short sentence right after. If a chapter is split into several files, "first time in the chapter" means the first file of that chapter in which the term appears. A rewriter working on a later file reads the earlier files' originals to check, and if unsure, explains again.
- **Terms first met inside a quotation.** If a §7 term's first technical use in a chapter is inside someone else's quotation, do not add the full explanation there. Add a short bracketed gloss after the word, using the first clause of the §7 wording ("proletariat [the class of wage workers]"). Then give the full explanation at the term's first use in Marx's own voice. (Added in Phase 4 for consistency.)
- **Never contradict the text.** If Marx is defining or developing the term in that very passage, do not add the explanation, because his own words are the definition.
- **These explanations are tools, not interpretations.** Do not extend them.

### 7.1 Commodities, value, and money

| Term | Plain explanation |
|---|---|
| **commodity** | a thing produced in order to be exchanged (sold), not for the producer's own use |
| **use-value** | the usefulness of a thing: what it can be used for, which comes from its physical properties |
| **exchange-value** | the proportion in which one commodity trades for others, e.g. how many coats a quantity of linen trades for |
| **value** | what commodities have in common that lets them be exchanged as equals: the human labor spent on them, counted by labor-time |
| **magnitude of value** | how much value a commodity has, measured by the socially necessary labor-time needed to produce it |
| **socially necessary labor-time** | the time needed to produce an article under the normal conditions of production of the day, with the average skill and intensity of labor |
| **useful labor / concrete labor** | labor of a particular kind, such as tailoring or weaving, that makes a particular useful thing |
| **abstract human labor** | labor counted simply as the spending of human effort (brain, muscle, nerve), whatever particular kind it is |
| **simple (average) labor** | the labor that an average person without special training can do; skilled labor counts as a multiple of it |
| **form of value** | the way the value of one commodity is expressed in another commodity |
| **relative form of value / equivalent form** | in "20 yards of linen = 1 coat", the linen's value is expressed (it is in the relative form) and the coat serves as the material that expresses it (it is in the equivalent form) |
| **universal equivalent** | a single commodity in which all other commodities express their values |
| **money form** | the form of value in which one commodity, gold, has become the universal equivalent |
| **price** | the money name of the value (the labor) embodied in a commodity |
| **fetishism of commodities** | the way social relations between people, who work for one another, appear to them as relations between things, as if the things had value by nature |
| **circulation (of commodities)** | the exchange of commodities through money: selling and buying |
| **metamorphosis** | a change of form: a commodity changing into money (sale, C–M) or money changing into a commodity (purchase, M–C) |
| **C–M–C** | Commodity–Money–Commodity: selling in order to buy |
| **M–C–M′** | Money–Commodity–more Money: buying in order to sell dearer; the general formula of capital |
| **measure of value** | money's function of expressing the values of all commodities as amounts of gold |
| **standard of price** | a fixed weight of gold used as a unit (e.g. the pound sterling) for measuring prices |
| **medium of circulation** | money in its role of passing from hand to hand to carry out sales and purchases |
| **hoard** | money withdrawn from circulation and kept as a store of value |
| **means of payment** | money used to settle a debt after goods have changed hands on credit |
| **world money** | gold and silver used as money between nations |

### 7.2 Capital and surplus-value

| Term | Plain explanation |
|---|---|
| **capital** | value that is used to make more value: money that is advanced in order to come back larger |
| **labor-power** | a person's capacity to work: the mental and physical abilities a human being uses when producing anything. It is this capacity, not labor itself, that the worker sells to the capitalist. |
| **value of labor-power** | the value of the means of subsistence needed to keep the worker (and to raise the next generation of workers) able to work |
| **means of subsistence** | the food, clothing, housing, and other necessities a person needs to live |
| **means of production** | the tools, machines, buildings, and raw materials used in producing things |
| **labor process** | the process of work itself, in which people use tools on materials to make useful things |
| **surplus-value** | the extra value that workers produce beyond the value of their own labor-power, which the capitalist keeps without paying for it |
| **necessary labor (-time)** | the part of the working day in which the worker produces the equivalent of the value of their own labor-power, i.e. of their wages |
| **surplus labor (-time)** | the part of the working day beyond necessary labor, in which the worker produces surplus-value for the capitalist |
| **constant capital** | the part of capital spent on means of production. Its value is passed on to the product but does not grow. |
| **variable capital** | the part of capital spent on labor-power. It reproduces its own value and also produces surplus-value, so its size varies. |
| **rate of surplus-value** | the ratio of surplus-value to variable capital (s/v), i.e. of surplus labor to necessary labor; Marx also calls it the degree of exploitation of labor-power |
| **absolute surplus-value** | surplus-value obtained by making the working day longer |
| **relative surplus-value** | surplus-value obtained by shortening necessary labor-time (by making workers' necessities cheaper through higher productivity), so that more of a working day of given length is surplus labor |
| **working day** | the total hours a worker works in a day: necessary labor plus surplus labor |
| **value-product** | the new value created by labor in a given period, as distinct from the old value transferred from the means of production |
| **productivity of labor** | how much a given amount of labor produces in a given time |
| **intensity of labor** | how much labor is packed into a given time, i.e. how hard and fast people must work |
| **dead labor / living labor** | labor already embodied in means of production / the labor of workers now at work |

### 7.3 Cooperation, manufacture, and modern industry

| Term | Plain explanation |
|---|---|
| **cooperation** | many workers working together, side by side, in the same or connected processes, under one capitalist's command |
| **division of labor (in manufacture)** | the splitting of the making of one product into many separate tasks, each done by a specialized worker |
| **manufacture** | the stage and form of capitalist production, roughly from the mid-16th to the late 18th century, based on handicraft work divided among many workers in one workshop |
| **detail worker** | a worker who spends their whole working life performing one small part of a larger process |
| **collective worker** | the whole body of workers, combined, treated as one productive mechanism |
| **modern industry** | large-scale production based on machinery and the factory system |
| **factory system** | production in which a system of machines, driven by a central power source, does the work and workers attend the machines |

### 7.4 Wages, accumulation, and primitive accumulation

| Term | Plain explanation |
|---|---|
| **wages** | the price paid for labor-power, which appears, wrongly, as the price of labor itself |
| **time wages / piece wages** | wages paid by the hour, day, or week / wages paid per piece of work done |
| **accumulation of capital** | turning surplus-value back into capital, so that capital grows |
| **simple reproduction** | production repeated on the same scale, with the capitalist consuming all the surplus-value |
| **composition of capital** | the proportion between constant and variable capital (value composition), which reflects the proportion between means of production and the labor needed to use them (technical composition); the value composition, insofar as it reflects the technical, Marx calls the organic composition |
| **concentration of capital** | growth of individual capitals through accumulation |
| **centralization of capital** | the joining of already existing capitals into fewer, bigger ones |
| **relative surplus population** / **industrial reserve army** | the workers made "surplus" to capital's needs for the time being, who serve as a reserve of available labor and press down on the employed |
| **pauperism** | the condition of the lowest layer of the surplus population, unable to find work and dependent on poor relief |
| **primitive accumulation** | the historical process (Marx says "so-called") that separated the producers from their means of production, above all by driving peasants off the land, and so created the conditions for capitalism |
| **expropriation** | taking away people's property (here, land and means of production) |

### 7.5 Economists' schools and labels

| Term | Plain explanation |
|---|---|
| **political economy** | the science of economics as it was then called |
| **classical political economy** | the economists from Petty to Ricardo who, in Marx's view, investigated the real relations of production |
| **vulgar economics** | Marx's name for economists who only describe and defend the surface appearances of the system, without investigating its real relations |
| **bourgeois** | belonging to the capitalist class, or to society and thinking shaped by it |
| **proletariat** | the class of wage workers, who own nothing they can live by except their labor-power |
| **corvée** | forced unpaid labor that peasants had to perform for a lord |
| **relay system** | a system of shifts in which workers, especially children, were switched in and out at different times, which made the legal hours hard to check |
| **truck system** | paying workers in goods, or in vouchers for the employer's own shop, instead of money |

---

## 8. Expected length

- **Target.** A faithful plain rewrite mostly splits sentences and swaps words, so it runs at about **0.95–1.25×** the original's word count, counting the whole file including notes. The pilot units ran 1.01–1.03×.
- **Below 0.95×:** likely lost content. Below 0.90× is a script failure.
- **Above 1.25×:** check for added explanation or padding.
- Either way, the script reports the ratio for every unit and the reviewer checks any unit outside the range.
- **Padding is a fault.** The aim is a text that is easier to read, not a longer one.
