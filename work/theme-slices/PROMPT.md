# Theme-candidate extraction: one slice of Capital Vol. 1

You are reading ONE slice of Marx's Capital Vol. 1 (Moore/Aveling 1887 translation) in /home/cole/Projects/das-kapital/original/. Read ONLY the files listed for your slice, in full (use Read with offset/limit for long files). NEVER read anything in rewrite/, parallels/, or other slices' outputs. Do not use the web.

Each paragraph is preceded by an ID line like `<!-- ch05-p012 -->`; footnotes follow their paragraph. Cite these IDs as anchors.

## Goal
Find candidate items for a "themes index" that will later be checked against the present day. Return 12-25 candidates, favoring quality and claims that matter over exhaustiveness. Four kinds:
- `theme`: a major theme / mechanism the slice develops (with the anchors where it is argued most directly).
- `forecast`: an explicit claim about how society, politics, technology, work, or human behavior WILL develop (tendencies, "must", "will", "tends to"). Include a short verbatim quote (max 15 words) from the original.
- `implicit_argument`: an argument that is not phrased as a forecast but could be tested against later history (e.g. "machinery lengthens the working day rather than shortening it").
- `opponent_claim`: a notable claim Marx ATTRIBUTES to an opponent (Senior, Ricardo, Malthus, Bastiat, Say, Mill, Ure, McCulloch, etc.) and argues against. List these so they are NOT mistaken for Marx's claims; they will not be researched as the book's claim.

## Attribution discipline (critical)
For every item set `speaker`: "marx" (his own position), "opponent:<Name>" (a view he reports in order to refute or mock), or "source:<Name>" (a factory inspector, Blue Book, witness, etc. whose factual report he uses). Marx often voices an opponent ironically ("the capitalist says...", "our friend Senior..."). If unsure who holds a view, say so in `notes`. Only "marx" items can be forecasts/implicit arguments of the book.

## Per-item rating
- `specificity`: `concrete_forecast` (names a definite future development), `general_warning` (a tendency or danger stated loosely), or `described_pattern` (an analysis of how things work / worked in his time).
- `testable`: `yes` or `no`. `no` = so general or definitional (e.g. the labor theory of value as a definition, dialectical claims) that almost any outcome would fit. Give a one-line `testable_rationale`.

## Output
Write a JSON array to /home/cole/Projects/das-kapital/work/theme-slices/slice-<N>.json with objects:
{"kind": "...", "title": "short title", "claim": "the claim in your own words, 1-3 sentences, faithful to Marx's terms and strength (keep hedges)", "quote": "short verbatim quote <=15 words or empty", "anchors": ["chNN-pNNN", ...], "speaker": "...", "specificity": "...", "testable": "yes|no", "testable_rationale": "...", "notes": "optional: caveats, ambiguity, related passages"}
Validate the file parses as JSON (python3 -c 'import json;json.load(open(...))'). Then reply with just the count of items by kind.
