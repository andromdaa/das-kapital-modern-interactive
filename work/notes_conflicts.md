# Cross-file conflicts in the rewrite notes (Phase 5 consistency step)

Sources read: `style-bible.md` (v1.0, §0), `work/consistency_todo.md`, all 89 files in `notes/` and `notes/pilot-checkpoint.md`.
No rewrite file was edited. "p" = paragraph ID, "n" = footnote label inside that paragraph's notes block.

**Verification.** For conflicts 1–10, the edit lists were checked with grep against `rewrite/` and `original/`. Any occurrence the notes did not mention is marked **(grep, not in notes)**. Conflicts 11–24 are taken from the notes only. Spot-checks are mentioned where they were made.

**Stale notes.** Some notes describe a state the text no longer has, because a later fix was applied. Do not re-apply these:
- ch18 p008 now reads "a fraction" (the notes say "equal fraction").
- ch24-s4 n35 now reads "aliquot part [fractional part]".
- ch22 n4 "op. cit." has already been reverted to as-printed.
- ch15-s4 n108 now has only the first clause, "[the class of wage workers]".
- ch05 p002: the surplus-value explanation is gone (removed by the g03 reviewer).
- ch10-s3 p053 now has "phthisis [tuberculosis]".

Order: meaning and attribution (1–7), then consistency of terms (8–19), then cosmetic issues (20–24).

---

## 1. "negro" and the slur in Marx's voice (ethnic term; attribution) — USER DECISION for ch24-p072

**Issue.** The bible says to use the neutral modern name in Marx's voice and to keep the original term inside quotations (§4, §0.5). Units chose different renderings, and some of them add a status ("slave", "enslaved") or an origin ("African") that Marx's word does not carry. That breaks §1.1 ("add nothing").

**Variants**
- Black + a neutral noun, with nothing added:
  - ch10-s2 p014: "the labor of Black people" / "the Black worker"
  - ch15-s2 p034: "one Black woman" (for "negress")
  - ch25-s5b p141: "the Black man's friend"
- Black + "slave(s)" where Marx himself writes "negro slave(s)" (correct): ch10-s6a p145, ch15-s3a p040, ch27b n30.
- Status added where Marx has only "Negro":
  - ch19 p012 n8: "the Black slave", and "such a Negro" became "such a slave". The second one loses the racial reference entirely.
- Status and origin added:
  - ch31 p029: "negro trade" became "the trade in enslaved Africans"; "4,800 negroes" became "4,800 enslaved Africans".
  - ch31 p005: "black-skins" became "Black Africans".
- Free indirect speech of a slave-owner, ch24-s3 p072: the slur ×2 became "slaves" (§4, Marx's voice). This removes the owner's vocabulary that the irony depends on (consistency_todo, USER DECISION).
- Inside quotations, kept as printed (correct per §4): ch07-s2 n17 (Olmsted), ch10-s5a p114 (Cairnes), ch33 n4 (Marx's own 1849 text, quoted).

**Resolution.**
- In Marx's voice, render "negro" as an adjective with "Black".
  - The noun becomes "Black man / Black woman / Black people", matching Marx's number and gender ("negress" becomes "Black woman").
  - Add "slave" only where Marx writes "slave".
  - Never add "enslaved" or "African".
- "black-skins" becomes "Black people".
- Text inside quotation marks stays as printed.
- For ch24-p072, §1.2 (free indirect speech keeps the opponent's voice) and §4 point in opposite directions, so the user must choose:
  - (a) keep the current "slaves";
  - (b) keep the owner's word as printed, treating free indirect speech like a quotation;
  - (c) "his Black slaves … more Black slaves". This keeps the racial-property point without reproducing the slur.
  - Suggested default: (c).

**Edits**
- ch19 p012 n8: "the Black slave" → "the Black man"; "such a slave" → "such a Black man".
- ch31 p005: "Black Africans" → "Black people".
- ch31 p029: "the trade in enslaved Africans" → "the trade in Black people"; "4,800 enslaved Africans" → "4,800 Black people".
- ch24-s3 p072: per the user's decision.
- No change: ch10-s2 p014, ch10-s6a p145, ch15-s2 p034, ch15-s3a p040, ch25-s5b p141, ch27b n30, ch07-s2 n17, ch10-s5a p114, ch33 n4.

---

## 2. Other outdated ethnic and collective names in Marx's voice

**Issue.** The same word was modernized in one unit and kept in another.

**Variants**
- **"savages"**
  - Kept: ch03-s1 n2, ch07-s1 p021/n9, ch14-s5 p042, ch25-s4 p061.
  - Changed to "tribal peoples": ch02 p008 n5.
  - The consistency_todo decision is to keep "savages".
- **"races" (= peoples)**
  - Changed to "peoples": ch02 p009 ("Nomad races" → "Nomadic peoples"), ch13b p025.
  - Kept: ch01-s4 p143 ("all civilized races") **(grep, not in notes)**, ch03-s1 n2 ("half-civilized races").
- **"Teutonic / Teutons"**
  - Changed to "Germanic": ch01-s1 p004 n4, ch27a p008.
  - Kept: ch01-s4 p143 n31 ("Teutons", "Teutonic") **(grep, not in notes)**, ch15-s9a p260 ("Teutonic-Christian").
- **"Asiatic"**
  - Changed to "Asian": ch13b p022 ("ancient Asiatics" → "ancient Asian peoples"), ch13b p024 ("Asiatic … kings" → "Asian"), ch15-s7 p191 ("Asiatic markets" → "Asian markets") **(grep, not in notes)**.
  - Kept: ch01-s4 p143 n31 and p145 ("ancient Asiatic … modes of production"), ch14-s4 p037, ch15-s1b p016, ch16 p015 ("Asiatic Archipelago").
- **"Scotch"**
  - Changed to "Scottish" in about 12 places (ch06, ch10-s5a, ch10-s5b, ch20, ch27a, ch27b, ch28); "Scotchman" became "Scot" (ch11).
  - Kept in Marx's voice: ch24-s4 p101, "the Scotch genius MacCulloch" **(grep, not in notes)**.
- Consistent everywhere (no action):
  - "red-skins" → "Native Americans"; Esquimaux → Inuit; Mahometan → Muslim; Tartar → Tatar; "Chinaman" → "Chinese spinner".
  - "Jews" and "shylocks" kept in Marx's voice (ch01-s4, ch04, ch05, ch10-s6b, ch25-s5d). Report this to the user together with conflict 1.
- **"gipsy" (metaphorical)**, ch25-s5e p244/p245: the review changed "Romani" to "vagabond". This is already a USER DECISION; it is listed here only for completeness.

**Resolution.**
- Apply §4 to names of peoples only. "Savages" stays (todo decision). Plural "races" meaning peoples becomes "peoples". "Teutonic/Teutons" becomes "Germanic/Germanic peoples". "Scotch" becomes "Scottish".
- "Asiatic" as an adjective for societies, states, forms and modes of production is Marx's analytic term (as in "Asiatic mode of production"), not a name for a people. Keep it as printed. Only the noun "Asiatics" becomes "Asian peoples".

**Edits**
- ch02 p008 n5: "tribal peoples" → "savages".
- ch01-s4 p143: "civilized races" → "civilized peoples".
- ch03-s1 p005 n2: "half-civilized races" → "half-civilized peoples".
- ch01-s4 p143 n31: "Teutons" → "Germanic peoples"; "Teutonic private property" → "Germanic private property".
- ch15-s9a p260: "Teutonic-Christian" → "Germanic-Christian".
- ch13b p024: "Asian and Egyptian kings" → "Asiatic and Egyptian kings".
- ch15-s7 p191: "Asian markets" → "Asiatic markets".
- ch24-s4 p101: "Scotch genius" → "Scottish genius".
- No change: ch13b p022.

---

## 3. "currency" (Marx's *Umlauf*, the course money takes) replaced by "circulation" (meaning)

**Issue.** The Translator's note at ch03-s2b [^26] says "currency" here means the course money follows from hand to hand, and that this course "is essentially different from circulation". One unit kept the term. Two later units of the same chapter replaced it with "circulation". In ch03-p085 the replacement erases the contrast Marx is drawing: "The circulation of the circulating medium … This connection arises in circulation".

**Variants**
- Kept "currency" throughout: ch03-s2b (p047–p062), ch03-s2c p068.
- Replaced with "circulation / speed of circulation / how fast … circulates": ch03-s3a p072, p080, p085, p086, p088, p092.
- Replaced, **(grep, not in notes)**: ch03-s2c p064, p065 (×2), p066, p067 n36.
- "forced currency" (legal-tender rate) → "forced circulation": ch03-s2c p070.

**Resolution.** Keep "currency" wherever Marx uses it for the movement of money (mention and use, §1.2; the Translator's note governs). No further gloss is needed in Ch. 3, because n26 explains the word. "Forced currency" stays as printed.

**Edits**
- Restore "currency":
  - ch03-s2c: p064 ("While they circulate"), p065 ("The circulation of coins itself", "coin in circulation"), p066 ("In circulation"), p067 n36 ("in circulation"), p070 ("forced circulation" → "forced currency").
  - ch03-s3a: p072 ("restless circulation of money"), p080 ("the circulation of gold and silver coins"), p085 ("how fast the means of payment circulates" → "the rapidity of currency of the means of payment"; "The circulation of the circulating medium" → "The currency of the medium of circulation"), p086 ("speed of circulation"), p088 (×2, "speed of circulation"), p092 ("how fast the means of payment circulates").
- No change: ch03-s2b, ch03-s2c p068, ch15-s5 p117.

---

## 4. §7 terms first met inside a quotation (additions inside someone else's words)

**Issue.** §7.0 (added in Phase 4) says: give a short bracketed gloss using the first clause, then the full explanation at the first use in Marx's own voice. Units did three different things:
- the full wording in the bracket;
- the first clause;
- nothing at all.

**Variants**
- First-clause bracket (correct): ch15-s4 n108 proletariat; ch17 n3 wages (full at p015); ch19 n7 exchange-value (full at p016); ch31 p002 wages; ch33 n4 price.
- Full wording in the bracket: ch03-s1 n4 (circulation, inside Marx's own *Zur Kritik*); ch21 p019 and ch27b p010 (means of subsistence); ch32 n2 (bourgeoisie; Modern Industry). Every one of these §7 entries is a single clause, so "full" and "first clause" are the same text.
- Wording that departs from §7: ch15-s5 n117 "pauperism [dependence on poor relief]".
- Nothing added, although the term is technical and has no explanation anywhere in its chapter:
  - ch07-s1 n10: "Proletarian" in Cherbuliez. The ch15-s4 notes flag this.
  - ch10-s6a p141: "factory system" in the Central Board's quotation. **(grep)** It is never explained in Ch. 10; its first Marx-voice use is ch10-s7 p202.
  - ch23b p019: "surplus-population" in Potter's words. **(grep)** No explanation anywhere in Ch. 23.
- Nothing added, judged an everyday sense (acceptable): ch18 n1 wages (Rodbertus), ch24-s3 n24 ("Roman proletarian").

**Resolution.**
- Follow §7.0.
- Clarification: when the §7 entry is a single clause, the bracket counts as the explanation. Do not repeat it in Marx's voice.
- Bracket glosses use the §7 first clause verbatim.

**Edits**
- ch07-s1 p021 n10: after "Proletarian" add "[a member of the class of wage workers]".
- ch10-s6a p141: add "[production in which a system of machines, driven by a central power source, does the work and workers attend the machines]" after "factory system".
- ch10-s7 p202: add the full §7.3 factory-system wording at its first use in Marx's voice.
- ch23b p019: after "surplus-population" add "[the workers made “surplus” to capital's needs for the time being]".
- ch15-s5 p117 n117: "[dependence on poor relief]" → "[the condition of the lowest layer of the surplus population]".
- No change: ch03-s1 n4, ch21 p019, ch27b p010, ch32 n2, ch31 p002, ch33 n4, ch18 n1.

---

## 5. Third-person "Marx" inside Marx's own voice (§7 wording; attribution)

**Issue.** Several §7 entries contain an attribution: "in Marx's view" (classical political economy), "Marx's name for" (vulgar economics), "Marx also calls it" (rate of surplus-value). Most units dropped or neutralized these phrases as a grammatical adjustment. A few kept them. Keeping them puts an editor's third-person voice inside Marx's first-person text.

**Variants**
- Dropped:
  - "in Marx's view": ch01-s4 n32, ch11 p011, ch18 p003, ch19 p008, ch24-s2 p037, ch25-s1 p006.
  - "Marx's name for": ch01-s3b n21, ch05 p004, ch11 n1, ch19 p008.
  - "Marx also calls it" → "it is also called": ch11 p002, ch12 p001, ch24-s1 p002.
- Kept:
  - ch16 p003 "who, in Marx's view, investigated" **(grep, not in notes)**.
  - ch16 p007 "Marx also calls it" **(grep, not in notes)**.
  - ch24-s3 p066 "Vulgar economics is Marx’s name for…".
  - ch25-s5a p078 "(Marx's name for…)".
  - ch33 p007 n16 "vulgar economics is Marx’s name for…".
- "(Marx says 'so-called')" in primitive accumulation was dropped in every unit (ch27b, ch28, ch30, ch31, ch33). This is consistent; no action.

**Resolution.** Treat removing the third-person "Marx" as the allowed grammatical adjustment (§7.0). In Marx's voice, write "economists who only describe…", "who investigated…", and "it is also called…".

**Edits**
- ch16 p003: delete ", in Marx's view,".
- ch16 p007: "Marx also calls it" → "it is also called".
- ch24-s3 p066: "Vulgar economics is Marx’s name for economists who…" → "Vulgar economics means economists who…".
- ch25-s5a p078: "(Marx's name for economists who…" → "(economists who…".
- ch33 p007 n16: "vulgar economics is Marx’s name for economists who…" → "vulgar economics: economists who…".

---

## 6. Parentheticals of uncertain speaker inside quotations (attribution)

**Issue.**
- §2.1 says to keep bracketed interpolations as printed, and gives "(on the part of the labourers)" as its example.
- §0.9 says Marx's interjections take American spelling and plain style.
- Some units converted ambiguous parentheticals to Marx's voice. Others kept similar ones as printed.
- Separately, the §2.1 example is itself wrong for ch24-p065. In the source, "(on the part of the labourers)" stands between a closing and a reopening quotation mark, so it is Marx's. ch24-s3 was right to apply §0.9.

**Variants**
- Converted although the parenthetical sits inside the quotation marks with no sign of who wrote it **(grep scan of originals)**:
  - ch10-s5b p123 "(i.e., with regard to the statute)"
  - ch10-s6a p144 "(i.e., the factory method)" in Farre
  - ch10-s7 p210 n163 "(the manoeuvres of capital, e.g., …)"
  - ch24-s4 p082 "(by the English agricultural labourer)"
  - ch25-s5d p199 "(the farm labourer’s)"
  - ch25-s5d p200 "(the labourer’s)"
  - ch25-s1 p012 n6 "(viz., by his “Theory of Moral Sentiments”)"
- Converted, with clear signs it is Marx's (fine):
  - outside the quotation marks: ch24-p065, ch25-p186, ch25-s1 n6 "(sc. Hume)"
  - "he means…": ch10-p061, ch23-p020
  - Marx's own terms or sarcasm: ch10-p123 "(… surplus labour)", ch24-p075 "(i.e., exploiting)", ch11-p018 "(i.e., his “hands”)"
- Kept as printed because the speaker is unclear: ch14-s5 n54, ch15-s3c p081 "(query – 1815 or 1825?)", ch25-s5b p146 and p149.

**Resolution.** Convert a parenthetical to Marx's voice only on positive evidence:
- it sits outside the quotation marks;
- it is in Marx's typical form ("he means", "!", "?", "sc.");
- it uses Marx's own categories or irony;
- or MECW attributes it to Marx.

Otherwise keep it exactly as printed (§2.1). Also correct the bible's §2.1 example. That is an orchestrator note; it needs no rewrite edit.

**Edits** (check each against MECW; revert to the printed wording and spelling unless the check confirms Marx):
- ch10-s5b p123 "(i.e., with regard to the statute)"
- ch10-s6a p144
- ch10-s7 p210 n163
- ch24-s4 p082
- ch25-s5d p199, p200
- ch25-s1 p012 n6 "(viz., …)"

---

## 7. §7 explanations shortened, or placed before Marx develops the idea

**Issue.** §7.0 says: verbatim or grammatical adjustment only; never contradict the text. consistency_todo also flags explanations that get ahead of the argument. Units shortened the same entries for different reasons, sometimes only by citing another unit as precedent.

**Variants**
- **working day.** Full wording in 12 units. First clause only in four:
  - ch10-s1 p001: Marx defines it at p004 (justified).
  - ch16 p004: Marx defines necessary and surplus labor in the same paragraph (justified) **(grep, not in notes)**.
  - ch15-s1a p003 and ch23b p012: precedent only.
- **labor-power.** Full in 20 units. First sentence only in:
  - ch01-s1 p013: premature in Ch. 1 (justified).
  - ch19 p006: Ch. 19 argues this exact point (justified).
  - ch28 p009: no reason given.
  - ch26 p001 was reworded, because p003 says "sellers of labour" (justified).
- **rate of surplus-value.** Full in ch11, ch12, ch16, ch24-s1. Shortened in ch13a and ch15-s3b because Marx develops it there (justified). ch24-s1 omits "s/v" (no reason given).
- **Explanations that get ahead of the text** (flagged in the notes; still present):
  - ch01-s3a p039 money form (gold before the universal equivalent is developed)
  - ch03-s1 p004 magnitude of value (before p019)
  - ch15-s3c p071 intensity of labor (before p072)
  - ch33 p001 capital (Marx develops it in p002)
  - ch09-s1 p010 working day (before Marx's definition)

**Resolution.**
- Use the full wording.
- Shorten only when the omitted part would contradict, or say in advance, what Marx defines in the same or the next paragraph. Log the reason; "as unit X did" is not a reason.
- Where the explanation sits right before Marx's own definition, move it to after that definition, or drop it (§7.0 "never contradict the text").

**Edits**
- Restore the full wording: ch15-s1a p003 (working day), ch23b p012 (working day), ch28 p009 (labor-power: add "It is this capacity, not labor itself, that the worker sells to the capitalist."), ch24-s1 p002 (add "s/v").
- Reviewer to judge move or drop: ch01-s3a p039, ch03-s1 p004, ch15-s3c p071, ch33 p001, ch09-s1 p010.

---

## 8. "aliquot part" (glossary changed in Phase 4)

**Issue.** §3.3 now gives "fractional part / share", because Marx uses the phrase loosely. "Equal" should stay only where the parts really are equal.

**Variants (grep)**
- "equal fraction(s)":
  - ch03-s1: p007, p007 n5, p009, p015 (×3), p017
  - ch03-s2a p033 **(not in notes)**
  - ch03-s2b: p062 (×2), p062 n33 (prose "an aliquot part, an equal fraction")
  - ch13a p003 **(not in notes)**
- "fractional part / fraction": ch24-s1 p006, ch18 p008, ch25-s2 p024, ch24-s4 n35 (bracket in a quotation).
- Inside a quotation: ch03-s1 n5 "aliquot [evenly dividing]" (correct).

**Resolution.**
- Use "fractional part" where the parts need not be equal.
- Keep "equal fraction(s)" where Marx means equal subdivisions:
  - ch03-s1: the weight standard divided into legally named units;
  - ch13a p003: 12 equal working days.

**Edits**
- ch03-s2a p033: "an equal fraction" → "a fractional part".
- ch03-s2b p062 (×2): "an equal fraction of the jumble … of the heap" → "a fractional part …".
- ch03-s2b p062 n33: "an aliquot part, an equal fraction," → "an aliquot part, a fractional part,". The formula keeps "aliquot part".
- No change: ch03-s1 (all), ch13a p003, ch18, ch24-s1, ch24-s4, ch25-s2.

---

## 9. "circulating medium" / "means of circulation" → "medium of circulation"

**Issue.** §3.1 gives "medium of circulation". The todo also says to fix ch03-s2b. ch03-s2c normalized these terms, but ch03-s2b, ch03-s3a, ch03-s3b and ch06 kept the printed variants. The notes mention only ch03-s2b and ch06.

**Variants (grep, Marx's voice only; all verified outside quotation marks)**
- ch03-s2b:
  - p049 ("means of circulation")
  - p052 ("means of circulation" ×2, "circulating medium")
  - p054, p056, p056 n30 (×2), p057 (×2), p058 (×2), p059 (×2), p060 (×2), p062 (×2), p062 n32
- ch03-s3a **(not in notes)**:
  - p071 ("as circulating medium")
  - p083, p085, p087
  - p088 ("circulating medium"; "means of circulation")
- ch03-s3b p096 n60 **(not in notes)**
- ch06 p008 ("means of circulation")

**Resolution.** Use "medium of circulation" everywhere in Marx's voice. Change the article where needed ("as the medium of circulation"). Keep the printed form inside quotations and titles.

**Edits.** Every occurrence listed above. That is 19 in ch03-s2b, 6 in ch03-s3a, 1 in ch03-s3b and 1 in ch06.

---

## 10. "subject of labour" → "object of labor"

**Issue.** The glossary was changed in Phase 4 to "object of labor" in Marx's voice. "Subject of labour" stays inside quotations, with "[the material worked on]".

**Variants (grep)**
- "object of labor": ch07-s1, ch07-s2, ch08, ch13a, ch15-s1a, ch15-s1b, ch15-s6 (post-review), ch16 p002, ch24-s4 p089.
- Quotation with gloss (correct): ch16 p001 (Marx quoting Ch. 7), ch23a n5 (Smith).
- Kept "subject" with no gloss: ch01-s2 p022 ("its aim, its way of operating, its subject, its means").

**Resolution.** Follow the glossary.

**Edits**
- ch01-s2 p022: "its subject" → "its object". This is the only remaining occurrence.

---

## 11. "manufacture" / "manufactures" / "manufactory"

**Variants**
- The §7 manufacture explanation:
  - With the dates: ch15-s1a p004, ch28 p001, ch30 p003, ch31 p018.
  - Without the dates: ch14-s1 p001 (Marx gives them there).
  - Explained in Ch. 13 at ch13a p001.
  - Never given in Ch. 10, although ch10-s5b p126 n88 uses the technical sense ("manufacture replaces handicrafts"). ch10-s3 deferred it, and ch10-s5b assumed it had been given.
- Plural "manufactures":
  - Kept: ch15-s5 p116, p117, p120, n113; ch14-s5 p058.
  - Changed to "manufacturing workshops": ch31 p004, p016, p022.
  - Changed to "in manufacture": ch21 p013.
  - Changed to "branches of manufacture": ch14-s4 p034.

**Resolution**
- Add the §7 explanation at ch10-s5b p126 n88.
- Dropping the dates in ch14-s1 is justified, because Marx gives them himself.
- Render the plural by sense:
  - establishments → "manufacturing workshops" (glossary "manufactory");
  - branches of industry → "branches of manufacture";
  - the form of production → "manufacture".

**Edits**
- ch10-s5b p126 n88: add the §7.3 wording.
- Re-check the sense, and render accordingly: ch15-s5 p116, p117, p120, n113; ch14-s5 p058.

---

## 12. "hands" without quotation marks

**Variants**
- Kept as "hands" (judged mockery): ch10-s2 n22, ch23b p017, ch25-s5b p147.
- Kept as "hands" although not mocking: ch25-s4 p056 ("a shortage of hands").
- Changed to "workers": ch08 n5, ch10-s4 p106, ch10-s6a p147, ch10-s6b p186, ch14-s5 p053, ch15-s4 n108, ch15-s8b p227, ch25-s3 p036, ch25-s5e p239, p246.

**Resolution.** Follow §3.1: keep "hands" only inside quotations or where Marx is mocking the employers' word; otherwise use "workers".

**Edits**
- ch25-s4 p056: "a shortage of hands" → "a shortage of workers".

---

## 13. "ideal" / "ideally" in Ch. 3

**Variants**
- Kept with no gloss: ch03-s1 p005, where Marx's "or mental" explains it.
- "(in imagination)" once: ch03-s2a p027.
- Replaced with "expressed in imagination": ch03-s2c p069.
- "(existing only in thought)" and "exists only in idea": ch03-s3a p071, p083.
- Later: ch22 p016 "in the realm of ideas".

**Resolution.**
- Keep the word "ideal(ly)", because it is Marx's term.
- Explain it once per chapter at its first use; in Ch. 3 that is ch03-s1 p005, where Marx's own "or mental" already does the job.
- Do not repeat the gloss or replace the word later in the chapter.

**Edits**
- ch03-s2a p027: delete "(in imagination)".
- ch03-s2c p069: "expressed in imagination" → "ideally expressed".
- ch03-s3a p071: delete "(existing only in thought)".
- ch03-s3a p083: "exists only in idea" → "exists only ideally".

---

## 14. "alienate / alienation"

**Variants**
- Kept, with "that is, part with them": ch02 p008.
- Replaced with "give up / parts with": ch03-s2a.
- "parted with": ch03-s2b p049.
- "handing over": ch03-s3a p073, p081.
- "The handing over (alienation)": ch06 p017.
- "parting with / handed over": ch24-s1 p016.
- "fraudulent transfer": ch27b p018.
- Kept, with "(the selling off)": ch31 p019.

**Resolution.**
- In the legal or sale sense, use "parting with / handing over", and keep "alienation" once per chapter with that gloss where Marx leans on the term (ch02, ch06).
- Check that "fraudulent" in ch27b p018 is in the source. If not, remove it, because it would be an addition.

**Edits**
- ch27b p018: check against the original.
- No other edits; the variants are all synonyms of the allowed rendering.

---

## 15. "op. cit."

**Variants.** The notes say ch22 n4 expanded it, while ch20 n3/n4 kept it. Grep shows that all three occurrences (ch20 n3, ch20 n4, ch22 n4) now read "op. cit.", which matches the consistency_todo decision.

**Resolution.** Keep as printed. **Edits:** none. The ch22 note is stale.

---

## 16. British spelling in formula lines outside ```text blocks

**Variants**
- Kept British: ch18 p009, p014, p020, p022 ("Surplus-labour", "Unpaid labour").
- Changed to American: ch20 p009, ch21 p003 ("labor-power").

**Resolution.** Formula lines outside ```text blocks are in Marx's voice. Use American spelling and glossary hyphenation; numbers and symbols stay exact (§1.4). The ★ check on "labor-power" also requires this.

**Edits**
- ch18 p009, p014, p020, p022: labour → labor in the formula words.

---

## 17. Neutral identifications: evaluative wording, repeats, and differing glosses

**Variants**
- Dogberry:
  - "(the constable in Shakespeare's *Much Ado About Nothing*)": ch01-s4 p152, ch15-s4 n108. ch15-s4 avoided "foolish" on purpose.
  - "(after the foolish constable in Shakespeare)": ch24-s4 p083. "Foolish" is an evaluation, which §1.1(c) forbids.
- Physiocrats:
  - Identified: ch01-s4 p149, ch24-s2 p044.
  - Not identified: ch16 p003/p019, ch19 p008.
  - All of these are acceptable under §0.8 ("only when needed").
- "tautology" glossed twice in Ch. 3: ch03-s1 p018 and ch03-s2a p046 **(grep)**.
- helots (inside quotations): "[slaves of ancient Sparta]" in ch10-s6b p196 n142; "[the serfs of ancient Sparta]" in ch14-s4 p034.
- *peculium*: "[private property]" in ch24-s5 p108 n56; "[a slave's private savings]" in ch25-s1 p013.
- benefices: "[paid church posts]" in ch25-s1 n6; "church livings" in ch25-s4 n27.
- *experimentum / experimenta in corpore vili*: s7 is plural and s9a singular, and so is the Latin. Both translations are correct; no action.

**Resolution.**
- Keep identifications neutral, and give each at most once per chapter (§0.8).
- Use one wording for the same item across the book. Glossary picks:
  - helots → "[state serfs of ancient Sparta]";
  - peculium → "[the small property a slave was allowed to keep]".

**Edits**
- ch24-s4 p083: drop "foolish".
- ch03-s2a p046: drop the second "tautology" gloss.
- ch10-s6b p196 n142 and ch14-s4 p034: use the helots wording above.
- ch24-s5 p108 n56 and ch25-s1 p013: use the peculium wording above.

---

## 18. Foreign tags in Marx's voice: replaced or kept with a bracket

**Issue.** §2.3 says to replace tags with plain English (§3.4) unless they work as a quotation or a famous tag. Units treated the same tags differently.

**Variants**
- *quid pro quo*: kept with a gloss (ch01-s3b p072) vs "a mix-up" (ch05 p005).
- *à la*: kept with a bracket (ch10-s1 n6), kept bare (ch10-s4 n71), replaced (ch10-s5b n88).
- *dramatis personae*: kept + bracket (ch03-s2a p041), "economic characters in the drama" (ch04 p009), "cast of characters" (ch06 p020).
- *par excellence*: "in the fullest sense" (ch03-s1), "above all others" (ch03-s3a, ch14-s3), "In the manufacturing period proper" (ch28 p014).
- *en masse*: "all together" (ch26 n1) vs "in a mass" (ch27a p004, ch28 p001). §3.4 allows both.
- Kept + bracket in Marx's voice although not famous tags: *esprit* (ch24-s5 n50), *pis aller* (ch33 p004), *haute finance* (ch27a p007), *credo* (ch31 p019).

**Resolution.**
- Replace §3.4 items with the listed rendering. Replace other non-famous tags with plain English.
- Keep a tag with a bracket only when Marx plays on it (for example ch15-s9a *nec plus ultra*).

**Edits**
- ch01-s3b p072: *quid pro quo* → "a mix-up".
- ch10-s1 n6 and ch10-s4 n71: "à la X" → "in X's style".
- ch03-s2a p041: *dramatic personae* → "characters".
- ch24-s5 n50: *esprit* → "wit".
- ch33 p004: *pis aller* → "last resort".
- ch27a p007: *haute finance* → "high finance".
- ch31 p019: *credo* → "creed".
- Lower priority; the reviewer may waive any of these.

---

## 19. Foreign titles: translated or not

**Variants**
- Untranslated (citations): ch10-s5b n96, ch10-s7 n158, ch15-s2 n27, ch15-s6 n136, ch25-s5e n108.
- Bracket translation added: ch13b n20 (a citation), ch15-s3a p048, ch25-s5c p156, ch27a p001 (titles in running prose).

**Resolution.**
- In citations, never translate (§2.6).
- A title named in Marx's running prose may take a §2.3 bracket.

**Edits**
- ch13b n20: remove the bracket "[Theory of Civil Laws]".

---

## 20. Abbreviations: "&c." after a title, "Cf.", "I. c.", "Lond." inside quotations, "per cent."

**Variants**
- "&c." just after a title's closing mark: kept in ch15-s6 n134; changed to "etc." in ch19 n2 and ch22 n3.
- "Cf." → "Compare" (ch19 n7) vs "compare" (ch21 n7).
- "I. c." / "1. c." (OCR for l.c.):
  - Expanded: ch05, ch12, ch13a, ch14-s5 n40, ch24-s4 n45.
  - Kept: ch14-s2 n4 ("Bibl. Hist. I. 1. c."), ch14-s5 n56 ("Thuc.: 1, I. c. 41").
  - These two are book/chapter numbers, not l.c., so they are correctly kept.
- "Lond." left inside quotations: ch03-s3a n56, ch14-s5 n54.
- "l.c." inside a garbled table: ch25-s5b n64 (correctly kept).
- "per cent." vs "percent" in Marx's voice: ch25-s2 notes mixed use.
- Italic "*that is*" kept (ch25-s5d p177, n104; ch10-s6a p152 *for example*) vs plain (ch25-s5b and most units).

**Resolution.**
- "&c." that belongs to a title stays; after the title is closed, write "etc." (§2.6).
- "Compare" is capitalized when it starts a citation sentence.
- "Lond." inside a quotation stays as printed.
- Use "percent" in Marx's voice.
- Drop italics on expanded Latin abbreviations, unless the italics mark emphasis in the source.

**Edits**
- ch15-s6 n134 → "etc.".
- ch21 n7: "compare" → "Compare".
- ch25-s5d p177, n104 and ch10-s6a p152: drop the italics.
- "per cent." → "percent" in Marx's voice. This needs a grep over all units, which was not done here.

---

## 21. Typos inside quotations and in figures

**Variants**
- One-reading typos inside quotations fixed: ch10-s3 p063 (pilot), ch15-s7 n150/n165, ch15-s9a n224, ch23b p018/p020, ch27b p011, ch30 n5.
- Similar typos kept: ch15-s9a p262 "unjustice", ch20 n4 "felling", ch33 p009 "is miserable wretch".
- Figures: ch20 p005 "3s." → "3d." was fixed (one-reading unit typo). ch21 p023 "½d." and ch24-s1 p002 "£2,000" were kept (they would need a digit added).

**Resolution.**
- §1.4 and §0.7 apply inside quotations too. The pilot already fixed Otley's quotation.
- Fix a typo when exactly one reading is possible, but not in witnesses' dialect.
- A wrong unit letter may be fixed. A missing or wrong digit stays as printed and is logged.

**Edits**
- ch20 n4 "felling" → "feeling": confirm it is OCR, not the source.
- ch33 p009 "is miserable wretch" → "is a miserable wretch": only if MECW agrees.
- ch15-s9a p262 "unjustice": keep (it may be the witness's word).

---

## 22. Citation-punctuation typos

**Variants**
- "31 st": kept in ch10-s5b n96, fixed in ch10-s7 n160.
- "&c..": kept in ch10-s4 n67, fixed in ch10-s6b n119.
- "(…p. 13 )" stray space: kept in ch10-s6a n107, fixed in ch10-s4 n70.
- "Ch. Empt. Comm." and "pp. xxi.. xxii.": kept in ch15-s8a n166/n181, while similar slips were fixed in ch15-s8b n201/n211.
- "p..22" fixed in ch24-s2 n14.

**Resolution.** The bible's own example ("p. Ixxi" → "p. lxxi") shows that one-reading typos in citations are fixed (§1.4). Stray spaces inside numbers ("319, 222") stay.

**Edits**
- ch10-s5b n96: "31 st" → "31st".
- ch10-s4 n67: "&c.." → "&c.,".
- ch10-s6a n107: remove the stray space.
- ch15-s8a n166: "Empt." → "Empl.".
- ch15-s8a n181: "xxi.. xxii." → "xxi., xxii.".

---

## 23. Quotation-mark normalization and missing full stops

**Variants**
- A straight mark paired with a curly one, normalized: ch10-s4 p089, ch15-s3a p042, ch15-s9a p259, ch19 n6, ch24-s3 p064, ch25-s5e n110, ch32 p001.
- Kept: ch10-s6b p177, ch14-s5 p050, ch15-s9b p292, ch15-s7 p180, ch15-s4 n110, ch25-s5d n85.
- Missing full stop after a footnote marker: added in ch24-s3 p072; left in ch23b p020.

**Resolution.**
- A matched pair with a mixed style has one reading, so normalize it to curly.
- An unmatched mark stays as printed (§1.4).
- Add a missing full stop at the end of a sentence.

**Edits**
- Normalize: ch10-s6b p177, ch14-s5 p050, ch15-s9b p292, ch25-s5d n85. ch15-s7 p180 and ch15-s4 n110: only if they are matched pairs.
- ch23b p020: add the full stop after "twelvemonth[^15]".

---

## 24. Minor wording drift (cosmetic)

**Variants**
- "cyclopean": "giant, Cyclops-like" (ch15-s1a p008) vs "giant, cyclopean" (ch15-s1b p019), within the same chapter.
- "Zenith": "the peak year" (ch15-s5 p122) vs "high point" (ch15-s7 p180).
- "cretinism" → "idiocy": ch15-s6, ch15-s7 (consistent).
- "retort": "(a chemist's distilling vessel)" (ch03-s3a) vs "(glass vessels for distilling)" (ch09-s1). Different chapters, so acceptable.
- Placement of §7 explanations (parentheses vs a following sentence) varies. §7.0 allows both; no action.
- Square brackets used for additions in Marx's voice: ch15-s9a n229 [overgrowth]/[wasting away], ch25-s1 n1 [tubercular], ch07-s2 p045 [frittered away]. Square brackets there can look like Marx's or the editors' interpolations.

**Resolution.**
- Use one rendering per chapter.
- Additions in Marx's voice go in parentheses. Square brackets are reserved for glosses inside quotations, translations, and source or editorial brackets.

**Edits**
- ch15-s1b p019: "giant, cyclopean" → "giant, Cyclops-like" (or the reverse in s1a).
- ch15-s9a n229, ch25-s1 n1, ch07-s2 p045: square brackets → parentheses.
