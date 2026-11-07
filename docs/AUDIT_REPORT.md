# Datasheet audit report

Four sheets, one template. Generated 2026-10-23. MOCK-UP for review; design work for site version 1.1.

Sources, all read from the published tree at `v1.0.0` (commit `833c2438fc3e`, Zenodo 10.5281/zenodo.23575816):

- published note: `README.md at v1.0.0`, sha256 `c98c3ee4a94a3dae`
- measurement record: `notation-measurements.json`, sha16 `24c49d6bafacdaf5`
- proofs: `proofs/TetrasemaphoreAlgebra.lean at v1.0.0`, sha16 `f066faf6595d22e9`
- masters and site assets: per sheet, below.

## Totals

| sheet | stations | quotations | pointers | Lean names | strings provenance-checked | provenance faults | quotation spans | punctuation faults | text overlaps | text outside canvas |
|---|---|---|---|---|---|---|---|---|---|---|
| NORMATIVE | 6 | 6 | 3 | 1 | 27 | 0 | 7 | 0 | 0 | 0 |
| NON-NORMATIVE | 7 | 6 | 3 | 2 | 31 | 0 | 7 | 0 | 0 | 0 |
| METACOGNITIVE | 7 | 6 | 3 | 2 | 31 | 0 | 7 | 0 | 0 | 0 |
| CRITICAL | 6 | 7 | 3 | 2 | 27 | 0 | 8 | 0 | 0 | 0 |
| **all four** | **26** | **25** | **12** | **7** | **116** | **0** | **29** | **0** | **0** | **0** |

Every cited string — quotation and pointer alike — is looked up in the published note before anything is drawn, and a Lean name is looked up as a `theorem` or `lemma` declaration in the published proof file. The two columns separate how the sheet *presents* a cited string: a **quotation** reproduces the note's own words; a **pointer** names a test or a section in wording of ours, with the test's title or sentence verified verbatim behind it. The provenance check tests, in both directions, that each string's field names a place that can exist in the file its source names.

**Quotation punctuation.** Every span a sheet wraps in typographic quotes is tested against the note: a span ending in punctuation claims the note carries that mark at that point, and a span ending in an ellipsis claims nothing. `test_quotation_punctuation.py` runs the check over the three faults found in review, their three corrected forms, the one full stop the note does have, and three invented cases — ten cases, all as intended — so a zero here is informative rather than vacuous.

## Every quotation, by sheet

Line numbers are in the published note, sha256 `c98c3ee4a94a3dae`.

### NORMATIVE

| station | text on the sheet | lines | kind |
|---|---|---|---|
| standfirst | “NORMATIVE keeps its stance and looks at its object: what has been tested and holds, for now.” | 12–13 | quote |
| 2 rings | “Colour comes second. Shape carries every state.” | 100 | quote |
| 2 rings | Note, test 3 — take the colour away: in greyscale all four can still be told apart by shape. | 122 | pointer, paraphrased |
| 3 meander | “The ring's keys all turn one way, so a mirror reverses them, while a half-turn leaves the ring as it was.” | 91 | quote |
| 3 meander | Note, Reading the semaphores — “Check the mark, not the ring.” | 91 | pointer with verbatim quotation |
| 4 legend | “… each semaphore states it, with its word and with the gold line that shows its mirror.” | 188–189 | quote |
| 4 legend | Note, test 5 — cover the words, then ask which state each print is. | 129 | pointer, paraphrased |
| 5 mark | “Each semaphore's mark is built to survive its own move …” | 22–23 | quote |
| absent note | “… the whole figure for I …” | 95 | quote |

Master: `MASTER-medallion-NORMATIVE-notation-slot820.svg`, sha256 `e0b6366d5c032523`. Site asset: `TETRASEMAPHORE-NORMATIVE-en-1298.png`, sha16 `eacf65bc9181f649`. Scale: 1 mm = 7.9778 slot units (102.786 mm across).

### NON-NORMATIVE

| station | text on the sheet | lines | kind |
|---|---|---|---|
| standfirst | “NON-NORMATIVE mirrors its stance and looks at its object: exploration that stands alongside the standard without claiming to replace it.” | 13–14 | quote |
| 2 rings | “Colour comes second. Shape carries every state.” | 100 | quote |
| 2 rings | Note, test 3 — take the colour away: in greyscale all four can still be told apart by shape. | 122 | pointer, paraphrased |
| 3 meander | “The ring's keys all turn one way, so a mirror reverses them, while a half-turn leaves the ring as it was.” | 91 | quote |
| 3 meander | Note, Reading the semaphores — “Check the mark, not the ring.” | 91 | pointer with verbatim quotation |
| 4 legend | “… each semaphore states it, with its word and with the gold line that shows its mirror.” | 188–189 | quote |
| 4 legend | Note, test 5 — cover the words, then ask which state each print is. | 129 | pointer, paraphrased |
| 5 mark | “Each semaphore's mark is built to survive its own move …” | 22–23 | quote |
| 6 fix | “Gold shows what the semaphore's move leaves in place: … a vertical line for σᵥ …” | 95–96 | quote |

Master: `MASTER-medallion-NON-NORMATIVE-notation-slot820.svg`, sha256 `4ef1de6ae126279e`. Site asset: `TETRASEMAPHORE-NON-NORMATIVE-en-1298.png`, sha16 `658837bd2d2802b3`. Scale: 1 mm = 7.9778 slot units (102.786 mm across).

### METACOGNITIVE

| station | text on the sheet | lines | kind |
|---|---|---|---|
| standfirst | “METACOGNITIVE keeps its stance but turns its look back to its own frame, the way you can keep your feet planted and look back between your legs; this is thinking about thinking.” | 14–15 | quote |
| 2 rings | “Colour comes second. Shape carries every state.” | 100 | quote |
| 2 rings | Note, test 3 — take the colour away: in greyscale all four can still be told apart by shape. | 122 | pointer, paraphrased |
| 3 meander | “The ring's keys all turn one way, so a mirror reverses them, while a half-turn leaves the ring as it was.” | 91 | quote |
| 3 meander | Note, Reading the semaphores — “Check the mark, not the ring.” | 91 | pointer with verbatim quotation |
| 4 legend | “… each semaphore states it, with its word and with the gold line that shows its mirror.” | 188–189 | quote |
| 4 legend | Note, test 5 — cover the words, then ask which state each print is. | 129 | pointer, paraphrased |
| 5 mark | “Each semaphore's mark is built to survive its own move …” | 22–23 | quote |
| 6 fix | “Gold shows what the semaphore's move leaves in place: … a horizontal line for σₕ …” | 95–96 | quote |

Master: `MASTER-medallion-METACOGNITIVE-notation-slot820.svg`, sha256 `cccfcff10dc74930`. Site asset: `TETRASEMAPHORE-METACOGNITIVE-en-1298.png`, sha16 `0f050e240c74e952`. Scale: 1 mm = 7.9778 slot units (102.786 mm across).

### CRITICAL

| station | text on the sheet | lines | kind |
|---|---|---|---|
| standfirst | “CRITICAL does both at once: it turns over the framework a claim rests on, treating every baseline assumption as possibly wrong.” | 15–16 | quote |
| 2 rings | “Colour comes second. Shape carries every state.” | 100 | quote |
| 2 rings | Note, test 3 — take the colour away: in greyscale all four can still be told apart by shape. | 122 | pointer, paraphrased |
| 3 meander | “The ring's keys all turn one way, so a mirror reverses them, while a half-turn leaves the ring as it was.” | 91 | quote |
| 3 meander | Note, Reading the semaphores — “Check the mark, not the ring.” | 91 | pointer with verbatim quotation |
| 4 legend | “… each semaphore states it, with its word and with the gold line that shows its mirror.” | 188–189 | quote |
| 4 legend | Note, test 5 — cover the words, then ask which state each print is. | 129 | pointer, paraphrased |
| 5 mark | “Each semaphore's mark is built to survive its own move …” | 22–23 | quote |
| 6 fix | “Gold shows what the semaphore's move leaves in place: … a single point for C₂.” | 95–96 | quote |
| absent note | “… a single point for C₂.” | 95–96 | quote |

Master: `MASTER-medallion-CRITICAL-notation-slot820.svg`, sha256 `33413c4af9ec838c`. Site asset: `TETRASEMAPHORE-CRITICAL-en-1298.png`, sha16 `a43da812ca3a7c88`. Scale: 1 mm = 7.9778 slot units (102.786 mm across).

## Lean names cited, by sheet

| sheet | theorem | what the sheet says it says |
|---|---|---|
| NORMATIVE | `S2_markAll_invariant` | Lean S2_markAll_invariant: the I mark is invariant under every move. Note, test 1. |
| NON-NORMATIVE | `S2_mark_sv_exact` | Lean S2_mark_sv_exact: the mark is invariant under k exactly when k is I or σᵥ. Note, test 1. |
| NON-NORMATIVE | `T4_fix_sv` | Lean T4_fix_sv: σᵥ fixes (x, y) exactly when x = 0 — the vertical axis. |
| METACOGNITIVE | `S2_mark_sh_exact` | Lean S2_mark_sh_exact: the mark is invariant under k exactly when k is I or σₕ. Note, test 1. |
| METACOGNITIVE | `T4_fix_sh` | Lean T4_fix_sh: σₕ fixes (x, y) exactly when y = 0 — the horizontal axis. |
| CRITICAL | `S2_mark_C2_exact` | Lean S2_mark_C2_exact: the mark is invariant under k exactly when k is I or C₂. Note, test 1. |
| CRITICAL | `T4_fix_C2` | Lean T4_fix_C2: C₂ fixes (x, y) exactly when x = 0 and y = 0 — the centre alone. |

## The drafting style

All drafting marks on all four sheets are drawn in **ice blue `#C3E6FF`** over a halo in each sheet's own ground, 4 px each side at 2400 px wide (2 px at the 1200 px preview). The colour was chosen by measurement: largest minimum CIEDE2000 difference from the four semaphores' art and from the text colours, taken as the worst of seven views - normal vision and protanopia, deuteranopia and tritanopia under two models - among candidates clearing 7:1 on all four grounds; the colour in use is Carey's pick from a preview, 20th of 8486 qualifying candidates. It appears in none of the four semaphores' art.

| measurement | value |
|---|---|
| nearest colour in the four palettes | `#B498E6` at ΔE2000 21.42 |
| nearest text colour | `#B498E6` at ΔE2000 21.42 |
| farthest colour in the four palettes | `#332A11` at ΔE2000 74.64 |
| contrast against the four grounds | #181403 14.11:1 · #001817 14.07:1 · #17121D 14.1:1 · #1F100E 14.12:1 |

Every colour in the four palettes, by difference from the drafting colour:

| ΔE2000 | colour |
|---|---|
| 21.42 | `#B498E6` |
| 22.06 | `#4FB5B5` |
| 22.74 | `#FFF9E3` |
| 23.38 | `#EBDFC8` |
| 24.36 | `#F0E3C9` |
| 29.27 | `#F2E4B8` |
| 32.83 | `#B29F7B` |
| 37.9 | `#DEC875` |
| 37.99 | `#C7B469` |
| 38.6 | `#D5AF64` |
| 47.6 | `#E25C60` |
| 55.08 | `#6C5324` |
| 55.33 | `#6E5321` |
| 74.64 | `#332A11` |

### Under colour-blind simulation

The green used in version 4 turned pale gold under simulated dichromacy, close to the art's gold, which is what sent this version looking for another colour. Each view below passes the drafting colour and every art and text colour through the same model, then compares them in CIEDE2000. Both models are applied in linear RGB. The models:

- Machado, Oliveira & Fernandes 2009, severity 1.0, linear RGB
- Vienot, Brettel & Mollon 1999, LMS-plane projection derived in choose_drafting_colour.py; its tritanopia case is the plane through white and the red primary, an approximation

| view | nearest art or text colour | ΔE2000 |
|---|---|---|
| normal | `#B498E6` | 21.42 |
| Machado protanopia | `#4FB5B5` | 15.33 |
| Machado deuteranopia | `#4FB5B5` | 16.31 |
| Machado tritanopia | `#4FB5B5` | 17.85 |
| Vienot protanopia | `#4FB5B5` | 15.71 |
| Vienot deuteranopia | `#4FB5B5` | 16.3 |
| Vienot tritanopia | `#4FB5B5` | 17.39 |

The worst of the seven views is **Machado protanopia** at ΔE2000 15.33. Carey chose this colour from a preview on 23 October 2026. The search in `choose_drafting_colour.py` places it 20 of 8486 candidates clearing 7:1 on all four grounds, with `#CFF2FF` first at ΔE2000 16.31 — 0.98 ΔE2000 units apart in the worst view. The sheets carry Carey's choice.


Line weights, px at 2400 px wide (halo adds 4 px each side):

| mark | core | with halo |
|---|---|---|
| detail window | 9 | 17 |
| corner brackets | 9 | 17 |
| panel frame | 9 | 17 |
| leader lines | 3 | 11 |
| box rules | 4 | 12 |
| centre axis | 2 | 10 |
| badge radius | r 16 | r 20 |
| anchor dot radius | r 5 | r 9 |

| sheet | art line in the window region (p10 / median / max, px) | window core | window with halo | marks over art: min contrast | median | px below 3:1 | axis px over art | art px under a halo |
|---|---|---|---|---|---|---|---|---|
| NORMATIVE | 4.0 / 6.0 / 10.0 | 9 | 17 | 1.0:1 vs `#F9E084` | 3.37:1 | 2179 of 45758 | 0 of 1248 | 2357 |
| NON-NORMATIVE | 4.0 / 6.0 / 6.0 | 9 | 17 | 1.04:1 vs `#F7DC80` | 3.32:1 | 1505 of 41470 | 0 of 1551 | 1553 |
| METACOGNITIVE | 4.0 / 6.0 / 12.0 | 9 | 17 | 1.04:1 vs `#F5DD7F` | 3.58:1 | 2610 of 48248 | 0 of 1449 | 2714 |
| CRITICAL | 4.0 / 8.0 / 12.65 | 9 | 17 | 1.0:1 vs `#F8E183` | 3.82:1 | 4093 of 45847 | 0 of 1231 | 3189 |

The art-line figures are measured on the reference semaphore at 428 px, the scale the detail window is drawn at. Comparison, computed from the rows above rather than asserted: the 9 px core is heavier than the median art line on 4 of the 4 sheets (widest median 8.0 px, CRITICAL); the 17 px assembly, core plus halo both sides, is heavier than the thickest single art stroke on 4 of the 4 (thickest 12.65 px, CRITICAL). The marks-over-art columns are the worst case where a mark crosses the lightest gold and cream: the ground halo carries the separation there, at the ground contrast above.


**The centre axis.** Where the axis passes behind a part it now stops 3 px short of it, at 2400 px wide: the axis is drawn to its own layer, and that layer is cleared wherever the art beneath it, dilated by 3 px, is present. The gap the clearance leaves is ground, so the separation a halo would give is there without a halo being painted over the artwork. The count of axis pixels over art is 0 on the four sheets, which is what the clearing step forces rather than an independent test of it: the same mask does the clearing and the counting, so the intersection is empty whether or not the radius is the intended one. The figure that can come out wrong is the distance. Measured on the finished image, the nearest axis pixel sits NORMATIVE 4.0 · NON-NORMATIVE 4.0 · METACOGNITIVE 4.0 · CRITICAL 4.0 px from the nearest art pixel, against the 3 px setting — a wrong radius would read here as a different gap. The last column counts every pixel where art was painted and a drafting halo now covers it — 1553 to 3189 px per sheet, all of it from the number badges, leader lines and detail window, none of it from the axis.


## Contrast of every text colour against each sheet's ground

| sheet | ground | state colour | gold | Fix gold | highlight |
|---|---|---|---|---|---|
| NORMATIVE | `#181403` | 8.9:1 | 11.07:1 | 8.91:1 | 14.53:1 |
| NON-NORMATIVE | `#001817` | 7.53:1 | 11.04:1 | 8.89:1 | 14.49:1 |
| METACOGNITIVE | `#17121D` | 7.52:1 | 11.07:1 | 8.91:1 | 14.52:1 |
| CRITICAL | `#1F100E` | 5.21:1 | 11.09:1 | 8.92:1 | 14.55:1 |

Sixteen colour-on-ground pairs, measured: 5.21:1 (CRITICAL state_colour) to 14.55:1 (CRITICAL highlight). All sit above the 4.5:1 floor for body text. The least headroom is CRITICAL's state colour at 5.21:1; the other three state colours sit at 7.52–8.90:1.

