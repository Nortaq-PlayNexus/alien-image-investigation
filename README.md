# alien-image-investigation

**A source-traced audit of the "alien imagery and footage" question.**

> **Verdict: no verified image or video of a non-human craft has ever been authenticated.**
> That is not the interesting finding. The interesting finding is *why a belief this
> thoroughly evidenced against has survived sixty years of free, primary, citable documents.*

This repository is a document audit, not a claims site. It does not argue that anyone is lying
about what they saw. It traces every circulating claim to the primary document that supposedly
contradicts it, and reports what those documents actually say â€” in both directions.

**Read this first: [`poster/POSTER.pdf`](poster/POSTER.pdf)** â€” a 4-page 24Ã—36in poster set with
the full findings. Also as [`POSTER.html`](poster/POSTER.html) (self-contained, images embedded) and
as four 2400Ã—3600 PNGs.

---

## What is in here

| Path | What it is |
|---|---|
| `poster/` | The poster set â€” PDF, self-contained HTML, four full-res PNGs, and the three source charts |
| `analysis/FINAL-REPORT.md` | The main written report, including the full correction log |
| `analysis/WINDOW2-VERDICT.md` | The birds-eye synthesis and the scored hypotheses |
| `analysis/WINDOW2-STRESS-TEST.md` | 34 numbered findings, ~160KB, with verbatim quotes |
| `analysis/EVIDENCE-LEDGER.md` | ~180KB of case-by-case source-tracing from the first 56 rounds |
| `analysis/AARO-PRIMARY-SOURCE-FINDINGS.md` | The AARO report read directly, term-swept, and analysed |
| `analysis/LIPF-CLAIM-CHART.md` | Seven falsifiers for a decoy hypothesis nobody has tested |
| `analysis/STANDOFF-BUDGET.md` | The physics of the directed-energy question, with a correction |
| `primary-sources/` | The AARO Historical Record Report Vol. 1 (PDF + extracted text) |
| `corpus/` | 32 content-addressed fetched documents, tier-tagged |
| `custody/` | Append-only fetch log: URL, status, byte count, SHA-256 for every document retrieved |
| `tools/` | The extraction script, so the key finding can be reproduced in one command |

## How to reproduce the load-bearing finding

The claim that AARO's own historical report does not address the Manzano 1980 case:

```bash
pip install pymupdf
python tools/extract_aaro_text.py primary-sources/AARO_HRR_Vol1_2024.pdf
# PAGES=63  CHARS=163120
#   Manzano          0
#   Kirtland         0
#   electronical     0
#   undisclosed      0
#   unidentified     49
```

Verified SHA-256 of the source PDF:
`6e9689dead22aa8be9fb1d22838767c127246db9ec6243c2450fe06b1437dce0`

---

## The seven claims, and what the documents say

| Circulating claim | The primary document |
|---|---|
| "They recovered non-human biologics." | *"no extraterrestrial craft or bodies were ever collected â€” this material was only **assumed to exist** by KONA BLUE advocatesâ€¦ The SAP was never approved or stood up."* â€” AARO HRR Vol. 1, p. 35 |
| "The 1948 metal is a superalloy." | *"**mostly composed of magnesium**."* And the false memory has a documented cause: an organisation *"fabricated a replica"* then *"attempted to replicate the sample at the same specific location."* â€” p. 33 |
| "There are secret programmes they won't name." | The word *"undisclosed"* appears **zero times** in 163,120 characters. Authentic programmes were *"appropriately reported to either or both the congressional defense and intelligence committees."* â€” p. 34 |
| "Dozens of insiders have come forward." | AARO interviewed *"approximately 30 people"* total. Two anchors of the claim network *"never formally sat down with AARO."* â€” pp. 30, 36 |
| "A real programme exists â€” it just isn't disclosed." | One such programme is documented: expanded in 2021 *"despite the lack of any evidence or mission need,"* reported to Congress, recovered nothing, *"disestablished due to its inactivity, absence of mission need, and lack of merit."* â€” p. 35 |
| "The 2026 releases prove something is up there." | The release is **~85% grainy video by volume** â€” 14.2 GB against 2.4 GB of reports. It includes a 74-year-old film of birds and some computer-generated content. |
| "Other governments are hiding it too." | The British programme closed *"and therefore reaped a saving in staff time."* â€” Hansard, 26 March 2007 |

## The three numbers

- **The unexplained rate is a measurement of our intake filters.** It ranges from **0% to 99.3%**
  across six programmes in four countries. It fell from over 20% to a few percent *immediately after
  the 1953 Robertson Panel* â€” it fell when they stopped asking. AARO reported 0%, then 64%, then 40%
  unresolved across consecutive reports in the same year.
- **Every measured object is human-scale; every narrated object is a football field.** The only
  dimensions in the official record are 1â€“2 metres and "six small spheres." The cultural image is
  30â€“100 metres. Nothing in the record has been measured inside that band.
- **The 2026 disclosure is ~85% grainy video.** 14.2 GB of footage against 2.4 GB of actual reports,
  never independently inventoried by anyone.

## Six open experiments

A negative result is only worth publishing if it comes with instructions.

1. **The 1966 tree.** Two bark samples from one trunk â€” one blackened, one normal â€” taken the same
   day in 1966, still unanalysed in a private garage. Comparative gamma spectrometry. Two days.
   The mundane candidate is 1960s weapons-test fallout, and the design is a matched pair, so the
   comparison is decisive either way. **Needs one lab. No permission. No argument.**
2. **The footage nobody watched.** 14.2 GB never independently inventoried. One clip purports to show
   a UAP being shot down. **Needs a clock and a caliper.**
3. **The audio test.** Multi-station blind listening â€” the Stargate method â€” on any of the thousands
   of "sound with no source" reports. Cheap, decisive, and apparently never run. **Needs two
   microphones and a friend who doesn't hear it.**
4. **Six questions for AARO**, answerable from files they already hold.
5. **The British working papers** â€” "UAP effects on Humans" and "Potential for Exploitation of
   UAP-associated effects." Free, in the National Archives, unread in public for 20 years.
6. **The waveform comparison.** The optoacoustic hypothesis specifies a waveform and a power. Both are
   computable against the case reports. **Needs no belief at all.**

## Corrections â€” five, published

Three of them killed findings I was proud of. They are listed in full in
[`analysis/FINAL-REPORT.md`](analysis/FINAL-REPORT.md) and summarised here because a source-traced
review that hides its own errors is just another claim.

1. Overstated the governance line on a 2026 advisory body. One inferential step too far.
2. **Falsified my own nuclear-cluster hypothesis.** It is a selection effect in the reporting
   apparatus, not in the sky.
3. Mis-stated a physics figure and repeated it. The paper says 500â€“900 MW, not 500â€“1,400.
4. **Withdrew a number I had asserted from memory and repeated without checking** â€” the same
   credibility-laundering mechanism this review criticises, operating on me.
5. **Claimed a provenance analysis did not exist. It did.** AARO did it, in print, in March 2024,
   numbering its sources and cross-referencing them against participation lists. I also claimed the
   projection/parallax problem was unexamined; AARO lists "optical effects â€” such as parallax" in its
   own prosaic explanations. Both of my "novel" contributions were already in the report.

## Known weaknesses

- The **Manzano 1980** case and the phrase *"a type unknown to their electronical equipment"* are
  **absent from AARO's historical report.** That file remains unread by anyone outside a classified
  room. This is the single most important thing I could not resolve.
- The **Release 02 "shot down" video** was never analysed by me. `war.gov` returns 403 to non-browser
  clients and I could not identify which file it is.
- The **Institute 22** Soviet case rests on one tertiary source and a one-citation encyclopedia
  article that opens with *"this article needs more citations."*
- The **Iran drone shootdown** has no dedicated encyclopedia article, so one claim about reference
  coverage rests on absence of coverage.
- The **Condign volume titles** are verifiable; specific neuro-anatomical quotations attributed to it
  by a partisan source were **not** independently confirmed. The executive-summary statement was
  confirmed, at lower resolution.
- The Haynesville bark samples are **not in my possession** and I cannot test them.

## Provenance and honesty notes

- Every factual claim in the poster is quoted to a source that is **public and free**. The sources
  are listed on the poster itself.
- Where a source was a **machine-generated transcript or an AI-generated blog**, that is disclosed
  in the text, and the primary document was retrieved and read directly instead. See
  `analysis/FINAL-REPORT.md`.
- Access difficulties are disclosed rather than hidden: `aaro.mil` returns HTTP 403 to non-browser
  clients; Wikimedia rate-limits at HTTP 429 and required a backoff. Neither restricts the document.
- `custody/custody-log.jsonl` is an append-only record of every fetch made during the investigation:
  timestamp, tier, URL, HTTP status, byte count, and SHA-256. `corpus/` holds the retrieved
  documents, content-addressed, so the research is auditable rather than merely asserted.
- **This work was assembled with substantial AI assistance** and is disclosed as such for the same
  reason the sources above are disclosed. Two of the sources used were themselves instances of the
  phenomenon under study. The primary documents were pulled, hashed, and read directly.

## What would change the verdict

Any one of these would:

1. Comparative gamma spectrometry showing a genuine radionuclide enrichment on the 1966 bark.
2. A trajectory reconstruction of the "shot down" video consistent with a physical object.
3. Any physical object with a documented chain of custody and a composition consistent with
   non-terrestrial origin.
4. A technosignature detected under a **handshake** rather than a **beacon** model. The
   beacon-model negative â€” 250 million channels, 100,000 galaxies, photographed libration points â€”
   is one of the strongest results in science, and it has been ignored by both camps. It is also
   conditional, and the alternative model has never been searched.

## Licence

Original analysis, writing, charts and poster: [MIT](LICENSE).

Third-party and government material in `primary-sources/` and `corpus/` is **not** covered by that
licence. It is reproduced for research and verification, with attribution, under the terms noted in
[`NOTICE`](NOTICE). The AARO Historical Record Report is a work of the United States government and
is in the public domain.

