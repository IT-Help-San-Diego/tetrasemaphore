# TETRASEMAPHORE — THE FOUR FINAL MASTERS (Claude Code lane, build 7, 2026-10-14)

Built to Science's build sheet `~/Downloads/TETRASEMAPHORE-SCIENCE-BUILD-SHEET-finals.md` (9e021adbe53cb849 was the 5 October sheet build 3 was built to; on disk now is v4, 891b0e7f167bdf66, with Science's 8 October rulings). PROPOSALS until Carey says final
and Hermes moves them. Nothing approved was changed: the shirt master `master/MASTER-medallion-METACOGNITIVE-slot820.svg` is d4054fa6e02e66e4 (the
guard) and the four approved owl coins in `master/states/` are d9d6336b0c9450ac / e1d83bb7e4b6017d / 055655372b21da5c / 3a8a7459bb1782d1, as sealed.

| coin | master (layered SVG, vector only) | sha16 |
|---|---|---|
| NORMATIVE — I | `MASTER-medallion-NORMATIVE-notation-slot820.svg` | **e0b6366d5c032523** |
| NON-NORMATIVE — σᵥ | `MASTER-medallion-NON-NORMATIVE-notation-slot820.svg` | **4ef1de6ae126279e** |
| METACOGNITIVE — σₕ | `MASTER-medallion-METACOGNITIVE-notation-slot820.svg` | **cccfcff10dc74930** |
| CRITICAL — C₂ | `MASTER-medallion-CRITICAL-notation-slot820.svg` | **33413c4af9ec838c** |

Files with these same names exist in older folders (`../`, `../finals/`, `superseded-build-1/`, `-2/`, `-3/`, `-4/`, `-5/`, `-6/`, and loose in `~/Downloads`).
Only the hash tells them apart: copy by hash.

Pictures: `proofs/TETRASEMAPHORE-FINAL-MASTERS-set.png`, `…-on-white.png`, `…-spanish-and-uncut.png`, `proofs/TETRASEMAPHORE-BUILD3-stamp-before-after.png`,
build 6's lit-edge pictures (`TETRASEMAPHORE-BUILD6-lit-edge-before-after.png`, `TETRASEMAPHORE-BUILD6-window-end.png`) in `superseded-build-6/proofs/`. Build 5's pictures (CRÍTICO before/after, the
flecks before/after) are in `superseded-build-5/proofs/`; build 4's in `superseded-build-4/proofs/`.
Full hashes: `MANIFEST.json`. These four files hold no owl, so the owl's licence does not restrict them.

## Build 7 (2026-10-14): Science's bow-tie guard on the lit edge; 300 dpi + sRGB on every PNG
Ordered by Science on 11 October (`~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-7-AND-CARDS.md` 8f2960032bc5b45f, reversing "no build 7 this
week"; wake-up packet J2). Build 6 (0f1498c8755fa563 / 153e5aae141ce46e / 79fd3f8291b39900 / e31ec0a46ab97939) is in `superseded-build-6/`, with its
litedge.js (`litedge.js.build6-d1082feb366e17b7`, also sealed in `tools/sealed/`).

**What changed: one line in `tools/litedge.js`, nothing else in the recipe.** Science's diff (`~/Downloads/TETRASEMAPHORE-SCIENCE-build7-litedge-guard.diff`
bf7d5264f178d5f1, tested by Science on copies): no strip spans a join that turns more than 170°. At a 179° join the two samples sit on one point with
nearly opposite tangents, so the zero-length step between them made a sliver through the edge point (the bow-tie thread 10's refuters found: 24 strips
on the r 342.854 rail). Science counted the outline's joins by angle: 708 under 1°, 12 at 1–10°, none at 10–170°, 48 at about 179°, all on the
342.854-unit rail, so 170° catches exactly the hairpins. The three rings were rebuilt as `*-litedge-guard-slot820.svg` beside the build-6 rings
(`finish/proposals/NOTE-build7-litedge-guard.md`: uncut 11,475 strips, build 6 had 11,497; 65 levels), the layered bases, the owl four and the four
notation masters were rebuilt from them exactly as build 6 was (`build/build7.sh`, its log and hashes in `build/build7-record/`), and every PNG of
both sets (107 files) carries a 300 dpi pHYs chunk and an sRGB chunk (plus gAMA and cHRM as the PNG spec recommends beside sRGB), pixels byte for
byte as rendered (`tools/png_tag.py`). litedge.js's label and `<desc>` say build 7 and name the guard; the rails labels say "(with their lit edges, build 7)".

Lane check (`refute/lane-verify-build7.py`, 203 checks, all pass, `lane-verify-build7-output.txt` and `-report.json` beside it), matching Science's
dry run to the decimal: lit pixels within 0.16 mm of the ink's edge above opacity 0.02 at 4920 px: **0** (Science's dry run of build 6: 91); pixels
above 0.67: 20, peak 0.784 (Science: strip overlaps beside five hairpins, not bow-ties, accepted; their positions are in the report); the layer alone
against Science's alpha reference at 1298 px: mean |Δα| 0.0060, 99th percentile 0.114 (unchanged); each ring at 1298 px against its build-6 ring: at
most 6 levels, 18–19 px over 2, none over 8; every master equals its build-6 file after exactly the allowed differences (the three `finalA5-litedge*`
layers' contents, the ring's `<desc>` sentence, the two rails labels, the ring file name); the 1298 px exports against build 6's: at most 8 levels
anywhere (the report has each count); the builder's report equals build 6's (the legends did not move; `owl-placement` root child 12); the approved
masters and the guard untouched. The stamp-floor check passes as before. The METACOGNITIVE lock screen was regenerated from the build-7 coin
(`vector-masters/tetrasemaphore-build7/`). Science's six checks are asked for in `~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-7-BUILT.md`. Not final.

## Build 6 (2026-10-10): the lit edge — gold version 3, Carey's pick
Carey, 9 October, judging Science's large METACOGNITIVE picture: "Three flecks off and lit edges in the ring's own gold." Science wrote the
construction (`~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-RULINGS-2026-10-09.md`, update 3, 5182233203276df1) and checked build 5 (pass).
Build 5 (dd09d1ef6095fbfc / f19256894cc29343 / 9c55197b5d58cf5f / e8dc6ed29d30655c) is in `superseded-build-5/`.

**What changed: one layer, nothing else.** Every ring copy in every master (the ring itself and the two window-rails copies inside the legend
layers) gained `finalA5-litedge` directly above `finalA5-finish`: the ridge zone 2.2–4.8 print px inside every edge of the ink, filled with the
ring's highlight gold #F2E4B8 at opacity 0.65 × max(0, n·L)², n = that edge's outward normal, L = the sweep A axis pointing to the top of the coin
(83.094°). So every edge that faces the light is lit all the way round, and no edge that faces away; the rim and the dark gaps are untouched
(nothing within 0.18 mm of an edge changes). Pure vector: `tools/litedge.js` (new) samples every line and arc of the meander outline, offsets each
sample inward, and makes one strip per run of equal opacity (quantised to 0.01); the uncut ring carries 11,497 strips in 65 levels. Made through
the recipe: `tools/ring_build.js --litEdge 0.65` on the build-5 knobs → the three `*-litedge-slot820.svg` rings beside the older ones
(`finish/proposals/NOTE-build6-litedge.md`); `finish7.js` is untouched and without `--litEdge` the build-5 rings still reproduce byte for byte.
The layer builder carries the new layer with the ring and into the window rails, so the lit rail runs unbroken past the stamp (the one place a
build-6 coin differs from Science's raster reference, which stops at the plate; Science checked build 6 on 10 October, pass, and ruled the rails stay
lit as built: `~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-6-CHECKED.md` 966a51a8e1212a52); the notation config's `swapped_node_index` is 12 now (one more
root layer before the mark). Science's acceptance test, the layer alone against its alpha reference at the 1298 px print size: mean |Δα| 0.0060
(limit 0.01), 99th percentile 0.114 (limit 0.15); the whole METACOGNITIVE coin against its option-3 reference differs outside the window by a
mean of 1.5 levels of 255. Flecks stay off; CRÍTICO stays as build 5. Every master's hash changed (the layer is in each) but outside the three
inserted layers, the ring's `<desc>` sentence and the two rails labels every file is byte-identical to build 5 (`refute/lane-verify-build6.py`).
Not final.

## Build 5 (2026-10-09, evening): the gold without its bright flecks, and CRÍTICO's accent at print weight
Two changes (`~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-RULINGS-2026-10-09.md`, then 3bb184acf4f6ee61; 5182233203276df1 since update 3): CRÍTICO per Science's ruling C,
which Carey chose; and the gold's bright flecks off, which is Science's recommendation and the direction Carey approved with Science ("it can't
become gray") — **but, at the time of build 5, not yet his pick: he was judging three versions of the gold by eye (1 as built, 2 flecks off, 3 flecks off plus lit edges; he chose 3 the same night, see Build 6),
and Science's note says "do not change the grain" until he does.** Build 5 carries version 2 ahead of that pick, as a proposal: three ring paths in each of the two
configs (`ring`, `keys6.ring_cut`, `keys4.ring_cut`, back to the build-4 rings) and a rebuild revert it to 1, and 3 was expected to come from the recipe's edge catch-light
knobs, widened to print; Science's update 3 ruled that those knobs do not give version 3, and build 6 used the new `tools/litedge.js` instead. Build 4 (43d28fb463bbfcd3 / 90bed40bf62098a3 / 760b8058524cbc6f / bda63a306c6450dc; Science checked it: pass) is in
`superseded-build-4/`.

1. **The bright flecks are off.** The speckle Carey never liked on the lower sides of the gold is the fleck step of the grain filter (sparse pale
   specks, a median 0.11 mm across). Science measured it and recommended removing only that step; Carey approved the direction on 9 October (evening)
   with his condition that the gold must not go grey (Science: the change is 0.3 ΔE at most, chroma unchanged); his pick among the three versions was open at the time (he chose 3 the same night; build 6 carries it).
   Done through the recipe, not on the masters: `finish/finish7-knobs-noflecks.txt` is the build-4 knobs line plus `--fleckOp 0`;
   `tools/ring_build.js --seamFix 1 --knobs finish/finish7-knobs-noflecks.txt` rebuilt the uncut ring and the two window rings as
   `finish/proposals/uncut/…-UNCUT-seamfix-noflecks-slot820.svg` and `finish/proposals/seam-fix/…-keys21-2-noflecks-slot820.svg`, `…-keys22-1-noflecks-slot820.svg`
   (the build-4 rings stay beside them and still reproduce from the recipe without `--knobs`, checked byte for byte). In every master the change is
   one number in three places (the ring's grain filter and its two window-rails copies: `<feFuncA type="linear" slope="0.22"/>` → `slope="0"`), the
   ring's `<desc>` line, and the two rails labels, which name the ring file. The mottle Carey likes at the top is untouched; nothing else moves.
2. **CRÍTICO per Science's ruling C** (Carey: "C for the critical"). The word is centred by its full height, accent included, instead of by its
   capitals: every glyph moves 5.904 slot units (0.74 mm) outward along its own radial line; the Í's accent leaves the letter and becomes its own
   path (`legend-accent-es`), lifted 2.2338 units (0.28 mm) along the letter's up axis, with a round-joined stroke of 1.6753 units (0.21 mm) in the
   letters' colour, so it prints at weight. Measured by the builder on the outlines at 102.785 mm: 0.769 mm from the ink to each rail (the accent
   with its stroke on the inner side, the capitals on the outer), 0.591 mm from the accent to the I; at Carey's 109.9 mm print size that is
   0.82 / 0.82 / 0.63 mm, Science's figures (0.82 / 0.82 / 0.64, with the accent 0.80 mm thick, up from 0.58). Science's reference file
   `~/Downloads/TETRASEMAPHORE-SCIENCE-CRITICO-accent-C-reference.svg` (9e8f7d33137c8ecc) is matched within 0.001 slot unit (0.00012 mm) on every transform, the
   outlines identical. Built through two new per-legend knobs in `tools/build_states_layered.py` (`radial_shift_units`, `accent`; both default off:
   the unchanged build-4 configs still give build 4's eight bases byte for byte, checked) — no sealed tool was edited; `legend.js` is untouched.
   Only CRITICAL's Spanish layer changed; its English layer and the three other coins' legends are the build-4 bytes.

Result: all twelve masters have new hashes (the fleck number is in every one), but outside the three fleck lines, the desc, the two rails labels
and CRITICAL's Spanish glyph group and label, every file is byte-identical to build 4 (`refute/lane-verify-build5.py`). Not final.

## Build 4 (2026-10-09): one word's spacing
Carey answered the decision page on 9 October (`~/Downloads/TETRASEMAPHORE-CAREY-DECISIONS-2026-10-09.md`): keep the cut-in stamp; the owl coins on
their fields; the four Spanish words; and for INFORMATIVO his choice B, **tracking 1.10 like METACOGNITIVE** instead of the rule's 1.2796, which
spread the short word across its window. Only NON-NORMATIVE changed (notation bfe8267ac6992f46 → 90bed40bf62098a3; owl 8b6c4eee9168fb8c →
8799b25060aa3735; base 9126ca72859045d0 → 8f5e2b6db2cff7d4): the eleven Spanish outlines and their label. The other three coins came out of the
same run byte-identical to build 3. Build 3 is in `superseded-build-3/`. Carey's other calls that touch these files: print size 109.9 mm; the camera
test waits for four isolated cards (`~/Downloads/TETRASEMAPHORE-CAMERA-CARDS/`); the shirt stays as it is; not final yet.

## What build 3 changed against build 2
Build 2 (335128d15f109192 / 0550b036663cf380 / a2fc2582d5a7aca5 / b81e23701a90671c; built the evening of 4 October local time) passed Science's
acceptance checks 9.1–9.5; it is in `superseded-build-2/`. The camera test (9.6) has not been run on any build.

1. **The stamp is cut into the ring** (sheet section 15). The plate under the word and its seams are now the coin's own field colour, the same dark
   that shows through every gap of the meander. Gone: the brown plate (#221B12), the three shaded edge strokes, the shadow under the letters, the
   bevel inside them, and the five blur filters they used. Also gone, because nothing uses them any more: the two gradients and two clip paths of
   those effects. Kept: the floor, the window rails, the letters (#DEC875).
2. **Spanish for NON-NORMATIVE is INFORMATIVO** (sheet section 16), not NO NORMATIVO. The Spanish set: NORMATIVO · INFORMATIVO · CRÍTICO ·
   METACOGNITIVO.
3. **Hidden layer labels** (they do not render): the labels of the four legend layers describe the new stamp; the rails label names its ring file
   by path; and on NORMATIVE the rings layer's label now gives the centre mark's colour as it is in the file, #C7B469 (it said #D5AF64, the rings'
   colour, since build 1).

Everything else is build 2, byte for byte: outside the four legend layers each file equals its build-2 file (centre mark, symmetry marks, field,
rings, uncut meander), apart from that one label on NORMATIVE. Inside them, the floor, the plate's outline, the window rails and every letter
outline are the build-2 bytes, except the eleven letters of the one changed word.

## What is in each file — layers, bottom to top
`field` · `finalA5-rings` · `finalA5-geometry` · `finalA5-finish` · `finalA5-litedge` · `legend-plaque-en` · `legend-text-en` · `legend-plaque-es` ·
`legend-text-es` · `glyph-placement` · `symmetry-marks` (CRITICAL has no mirror line, so no marks group). Root children 0–2 are `title`, `desc`, `defs`,
so the mark is root child 12.

- **field** — one disc in the coin's own dark tint (r 403.678 units, its edge under the outer ring); outside the coin is transparent.
  NORMATIVE `#181403`, NON-NORMATIVE `#001817`, METACOGNITIVE `#17121D`, CRITICAL `#1F100E`.
- **rings** — the two rings in the coin's colour.
- **geometry + finish** — the meander, UNCUT: all 24 keys, seam fix on. The same ring on all four coins
  (since build 6 `finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-slot820.svg` 91d1a01b8e1392c0; build 5's `-noflecks-` f21db7ab012500c8 and build 4's `…-seamfix-slot820.svg` 901fd319c2b7e30a stay beside it; the window rails likewise use the `-litedge-` cut rings 9af6030e1fe28c27 / b809ccf6c6784407).
- **lit edges** (`finalA5-litedge`, build 6) — the ridge zone 2.2–4.8 print px inside every edge of the ink, `#F2E4B8` at 0.65 × max(0, n·L)², one
  strip per run of equal opacity (quantised to 0.01): 11,497 strips in 65 levels in the ring. A copy sits inside each `legend-rails-<lang>` as
  `finalA5-litedge-win-<lang>` (8,719 strips on the six-key window, 9,641 on the four-key), so the lit rails run past the stamp.
- **legend pairs** — the stamp, one pair per language. English is shown; Spanish is in the file, hidden (`style="display:none"`).
  Each `legend-plaque-<lang>` layer holds: a **floor** (the channel between the rails over the window) · the plate's **seams** · the **plate** — all
  three in the field tint — and `legend-rails-<lang>`: the cut ring for that window, clipped to the window and drawn on top, so the rails beside
  the word are clean rails. That cut ring is the seam-fixed one with its lit edge, `finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-litedge-slot820.svg`
  9af6030e1fe28c27 or `…keys22-1-litedge-slot820.svg` b809ccf6c6784407 (build 6; the build-4 `…keys21-2-slot820.svg` 45dafb97a8a077a1 / `…keys22-1-slot820.svg`
  06454b6df0e80ef4 and build-5 `-noflecks-` 6086dba12965b210 / e0a648d4451dd778 rings of the same windows stay beside them; the corner fix is the one Carey
  told the lane to go ahead with on 1 October, a proposal, not yet sealed; the sealed ring of the same name in `finish/` has the old corners).
  Each `legend-text-<lang>` layer holds only the letters. Hide all four legend layers and the whole meander
  shows, ready for another language.
- **glyph-placement** — the centre mark (flat letters). **symmetry-marks** — two bars across each mirror line at both ends.

To recolour a coin's ground, change seven fills: the field disc, and the floor, seams and plate of each language. If the `field` layer alone is
hidden, a field-coloured band stays under the word (the floor and plate are the field); hide the legend layers too.

## The centre marks (unchanged from build 2)
| coin | mark | size | closest ink to the ring |
|---|---|---|---|
| NORMATIVE | ONE outline through the diamond's four vertices plus the shared line (`M L T R B Z M L R`, stroke 21.7, sharp joins), I twice, all gold `#C7B469`; scaled 0.9478 about the centre (0.545353) | I 14.71 mm tall | 2.321 mm (outer mark corners) |
| NON-NORMATIVE | σ + v.ssty (70 %), upright token and its exact left–right mirror, gold vertical line | σ 16.718 mm | 2.330 mm (outer σ) |
| METACOGNITIVE | σ + h.ssty (70 %), token and its exact top–bottom mirror, gold horizontal line | σ 16.718 mm | 8.583 mm |
| CRITICAL | as accepted — glyph node byte-identical to `../finals/` af4373975fc5f063 | C 10.96 mm | 2.315 mm (triangle points) — the floor |

**Twins** (METACOGNITIVE / NON-NORMATIVE): one placement scale 0.918549; gold line 9.3307 units = 1.0743 mm; air between line and letters 1.9696 mm;
the line overhangs the letters' ink by 2.9187 mm at every end; identical marks. **Symmetry marks:** bars 4.0 × 0.9 mm; the first 1.5 mm beyond the
mark along the line, then 1.6 mm, then the second; the coin's colour. **Floor:** nothing is closer to the ring than CRITICAL's triangle points.

## The legends
Typeface DejaVu Sans Bold 2.34 (`05-DejaVuSans-Bold.ttf` 7e69e81478e233b8), stored as outlines, flat, fill `#DEC875`. Font size 47.83 slot units =
17.0 pt at 102.785 mm. Cap height 4.38 mm at 102.785 mm (the legend generator calls it 4.4 mm, at its own scale of 0.0847 mm per print pixel).
Contrast of the letters on the plate: 11.04–11.09 to 1. No kerning: spacing is the font's advance widths times the tracking.

Spacing rule, read off the approved English legends: the word's advance box is centred on the bottom of the coin with 4.812° of plate left each
side, never tighter than tracking 1.0.

| coin | window | English (track; plate each side of the box) | Spanish (track; plate each side of the box) |
|---|---|---|---|
| NORMATIVE | keys 22-1, 60–120° | NORMATIVE (1.0; 3.42°) | NORMATIVO (1.0; 2.76°) |
| NON-NORMATIVE | keys 21-2, 45–135° | NON-NORMATIVE (1.0526; 4.81°) | INFORMATIVO (1.10; 10.45°, Carey's B) |
| METACOGNITIVE | keys 21-2, 45–135° | METACOGNITIVE (1.1; 4.81°) | METACOGNITIVO (1.0805; 4.81°) |
| CRITICAL | keys 22-1, 60–120° | CRITICAL (1.2578; 4.81°) | CRÍTICO (1.4141; 4.81°) |

Measured on the outlines (`../../layered/layered-build.json`):
- The rule centres the advance box, not the ink. The ink's two end gaps differ by 0.03–0.24° (at most 0.2 mm); the approved English legends are
  built the same way (CRITICAL 5.95° / 5.75°).
- Capitals clear both rails by 1.51–1.53 mm, except CRÍTICO since build 5: its ink is 0.769 mm from each rail (the accent with its stroke on the
  inner side, the capitals on the outer) and the accent is 0.591 mm above the I (0.82 / 0.82 / 0.63 at 109.9 mm; the refuters re-measured
  0.818 / 0.821 / 0.63 on 8192 px renders, accent 0.800 mm thick); the accent is its own stroked path. Build 3's 0.41 mm figures are history.
  The 0.591 mm gap between the accent and the I and the 0.769 mm to each rail are what the print test must keep (if they fill, the word loses its accent, which is a misspelling).
- INFORMATIVO is a short word in the six-key window (62.8° at normal spacing, too long for the four-key window's 60°; windows are symmetric about
  the bottom, so they are four or six keys). The rule would spread it to 1.2796; Carey chose 1.10, METACOGNITIVE's spacing, with 10.45° of plate
  each side (build 4).

The word was chosen by usage (sheet section 16): Colombia's ICONTEC and Spain's UNE print (Normativo) / (Informativo) on their annexes; Mexico's
NMX and Mercosur's AMN use the same pair of words (Mexico of an *apéndice*). The lane's memo `~/Downloads/TETRASEMAPHORE-RESEARCH-SPANISH-TERMS-MEMO.md`
was written when NO NORMATIVO was still the built word.

## Renders
`png/TETRASEMAPHORE-<STATE>-<en|es>-<px>.png` — flattened, field included, transparent outside the coin: 2460, 1298 (300 dpi at 109.9 mm), 1214
(300 dpi at 102.785 mm), 1024, 512. The print file is the 1298 px export; 512 and 1024 px are screen sizes, not for print (every PNG is tagged 300 dpi since build 7; Science, 21 October). New in build 3: the Spanish coins at every size. **Renderer: resvg-js 2.6.2 (`tools/render.js`)** for every
picture this lane has made; Science's previews are its own composites. Other renderers draw the ring's grain differently; the plate came out in the
field tint in Inkscape, Chromium and Firefox as well. `proofs/` — the sheets, the stamp before/after, and each coin with the legend layers hidden.
`scan-cards/` — caption-free images for the camera test (the four `readable-half` cards are byte-identical to build 2's: the marks did not change).

## How it was built
1. `python tools/build_states_layered.py --config master/states/proposals/layered/states-config-layered.json --outdir master/states/proposals/layered`
   — field, rings, uncut meander, legend pairs from the sealed `legend.js`; the config's `stamp: cut-in` gives the plate the field tint and leaves
   the effects out; centre still the owl placeholder. Bases (build 6): NORMATIVE b00c2f3cd58b011f, NON-NORMATIVE 852920b55ea19371, CRITICAL a9175a311b37520f, METACOGNITIVE 4f0c153ee6d14dca (build 5's e721a06135882bdb / 63dfc6d22a3dc700 / cb647435d7bd7332 / fff1eb7ed22eb17c in superseded-build-5/; builds 3 and 4's in superseded-build-3/ and -4/; the next line's hashes are build 3's, kept as history:) NORMATIVE d947161c314cff34, NON-NORMATIVE 9126ca72859045d0, CRITICAL d52c54a4312f00ae,
   METACOGNITIVE e11647a0b8c1b843. **The bases contain the owl: they are build inputs for the private register, not for a public repo.**
2. `python tools/build_notation.py --config master/states/proposals/notation/notation-config-final-masters.json` — the centre marks and symmetry
   marks. This config is build 2's with one change for build 6: `swapped_node_index` 12, the mark's root index now that the lit layer sits before
   the legends (62df33b01c9e0f9b; build 5's, index 11, is `superseded-build-5/notation-config-final-masters-build5.json`, byte-identical to build 2's
   9024cdc4e115a311). Its `_doc` names the build sheet by an older hash, 6213318c73663f63: `superseded-build-2/README-build-2.md` gives that hash for
   the sheet build 2 was built to, `superseded-build-3/README-build-3.md` gives 9e021adbe53cb849 for build 3's, and the file on disk today is v4,
   891b0e7f167bdf66 (its own header says v4, 8 Oct; shasum 10 Oct).
3. `python tools/export_set.py --dir master/states/proposals/notation/final-masters-2026-10-05 --kind notation --glyph-dir <work dir of step 2>` — every PNG.

No sealed tool was edited. `build_states_layered.py` gained config switches (`stamp`, `edition`, `out_suffix`, a state's `mark_hex`), all off by
default: with build 2's config it still gives build 2's four bases byte for byte (checked; its JSON report gains lines). Its previous bytes are
`tools/sealed/build_states_layered.py.before-cut-in-9ecd029d3f637b44`. The sealed `render.js` and `legend.js` load their node modules from a path
under `/private/tmp` that is a link to `~/.cache/dose01-toolchain/node/node_modules`; if `/private/tmp` has been cleared, remake the link first.

## Checks
- `refute/lane-verify-final-masters.py` (the vector check of build 2, run again): ALL PASS — layers, no rasters, ids, field, scales and path data
  against Science's references, marks, twins, clearance.
- `refute/lane-verify-build7.py` (current): build 7 against build 6 — see Build 7 above: 203 checks, all pass (`lane-verify-build7-output.txt`, `lane-verify-build7-report.json`).
- `refute/lane-verify-build6.py` (historical: its output is the run on build 6): build 6 against build 5 — every master (notation, owl, layered) byte-identical after the allowed differences
  (the three inserted `finalA5-litedge*` layers, the ring's `<desc>` sentence, and the two rails labels, each changed in two spots: the ring file name
  and the appended "(with their lit edges, build 6)") — the lit layer against Science's alpha reference, the three rings, the builder's report
  (`owl-placement` root child 12), layers, words, guard, exports: 144 checks, all pass (`lane-verify-build6-output.txt` beside it).
- `refute/lane-verify-build5.py` (historical: its output is the run on build 5): build 5 against build 4 (only the allowed differences), CRÍTICO against Science's reference, the rings, the report, layers, words, guard, exports: 148 checks, all pass (output beside it).
- `refute/lane-verify-build3.py` (historical: last run on build 4; on build 5 its ring and CRÍTICO tests fail by design): what changed against build 2 and what did not, and the owl set; 221 checks on build 4, all pass (its
  "letters = build 2" test on NON-NORMATIVE's Spanish expects a difference, which build 4 also has).
- `refute/lane-stamp-floor.py` (`lane-stamp-floor.json`): each coin rendered with its letters hidden, both languages, both sets; the plate, taken
  from 0.38 mm inside each rail and 1.5° inside each end of the window, is the field tint on every pixel (169,116 or 258,114 pixels per coin at
  2460 px; none differs at all).
- Close-ups of both ends of the window: `refute/window-ends-build3-resvg-4920.png`, `refute/window-end-METACOGNITIVE-left-inkscape.png`.
- **Independent refuters** (`refute/refute-build3.json`): five, each with its own code, then a second agent on every finding, then a critic.
  122 checks. No wrong artwork and no wrong word in any deliverable. Among what they measured themselves: the plate is the field tint right up to
  the rails and the window's ends in resvg, Inkscape, Chromium and Firefox; no trace of a hidden key; every difference from build 2 lies in the
  legend window; Science's checks 9.1–9.4 still hold; each Spanish word matched letter by letter to the font and read back by two text readers;
  all eight masters and every PNG rebuilt byte for byte from the commands above; build 3 agrees with the picture Carey said yes to, within that overlay's own noise.
  They examined the first pass of build 3 (hashes in the record). `refute/labels-only-diff.py` shows the delivered files differ from those only
  in layer-label text and that every coin PNG is byte-identical (14 checks, all pass).

## What the refuters found, and what was done
- Two wrong words in hidden labels (NORMATIVE's mark colour; "approved cut ring" for the seam-fixed ring): corrected in the generator, rebuilt.
- The build report gave every legend 1.605 mm of rail clearance, a capitals-only design figure: it now records the measured clearance per word
  (CRÍTICO's accent was 0.414 mm in build 3; 0.769 in build 5) and keeps the old figure under a name that says what it is.
- An owl sheet caption with a missing character; a proof picture no script produced: both fixed in `tools/export_set.py`.
- Loose sentences in this note (standards bodies, the renderer, "approved", "one line in a config", 8.59 mm, "the same day"): rewritten above.
- Records that moved without their paths: stated in `superseded-build-2/SUPERSEDED.md` and in the owl folder's `classic/NOTE.md`.
- Not changed, stated: the rails in the window sector are drawn twice (the cut ring over the uncut ring), so their outermost edge pixel is slightly
  brighter there (about 20 levels on one pixel; not visible at size; the same in build 2). Three stray edge pixels, at most 11 levels off the
  tint, at one end of the four-key windows at 2460 px. NORMATIVE's letters sit as close as 0.37 mm to each other (approved spacing, no kerning).
  Text readers given the whole coin misread the tilted end letters of the long legends at some sizes, in both languages and on the approved
  English too (a straightened crop reads right); it matters only if the camera test is also meant to read the legend.

## Known, stated
- Carey's three calls behind this build reached this lane through Science's reading of him (the stamp: "Okay, yeah, that looks better";
  INFORMATIVO; the owl edition packaged the same way). Any of them can be reversed, but that is a new build: a config change, then the eight
  masters and their pictures again.
- No shirt file carries this build. The shirt master (`master/MASTER-medallion-METACOGNITIVE-slot820.svg`) and the garment version in the owl
  folder still have the brown plate and no field; the print file is Hermes's. Whether the stamp and the field go onto the shirt is Carey's call.
- NORMATIVE's scale is 0.9478 as the sheet says (0.545353); Science's reference file has 0.94779 — 0.0003 mm apart.
- CRITICAL's 2 has a 0.527 mm thin line (accepted; the generator's 0.60 mm floor is an unmeasured assumption, so it prints PASS=False for CRITICAL).
- Renderers disagree on the ring's grain (Inkscape against resvg at 1024 px: more than 16 levels on about 1.35 % of pixels, measured on build 2).
- Since build 7 every PNG carries a 300 dpi pHYs chunk and an sRGB chunk (before build 7 they carried neither; read them as sRGB). 300 dpi on every size, as built (Science's ruling, 21 October 2026): each export prints at its pixel width ÷ 300, so 1298 px = 109.9 mm (the shirt print file), 1214 px = 102.785 mm (the master size), 2460 px = 208 mm; 1024 px and 512 px are screen sizes, not for print.
  PRINT SIZE is still open (102.785 or 109.9 mm).
- `notation-measurements.json` holds run timings and work-folder paths, so a rerun matches it in every measured value but not in its hash.
- For Science: sheet lines build 3 has overtaken (section 8 "on plaque #221B12"; section 14 "Owl finals: do not comply yet" and the four specks;
  section 15's heading "awaiting his yes"; section 2's 8.56 mm for METACOGNITIVE, vector 8.583); and section 2 words survival as a share of the
  mark's ink, while its numbers are overlap over union (as a share, three coins exceed 0.25; as overlap over union everything passes).
- DONE since build 5: Science checked build 5 (pass) and build 6 (pass, 10 October, `~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-6-CHECKED.md`
  966a51a8e1212a52: all eight hashes match, the alpha gate 0.0060 / 0.114 reproduced, the lit window rails ruled to stay as built); Carey picked gold
  version 3 (decision card 12). NOT DONE: calibration tile 2 (Science cut it, `~/Downloads/TETRASEMAPHORE-calibration-tile-2-build6-10x6in-300dpi.png`
  c9a88d3436b15bff, guide beside it; Carey prints and reads it); the camera test (Carey's; images in `scan-cards/`); the public note (card 13); Carey's word
  "final"; the repo (Hermes's PR #1 still carries older files).
- The owl coins in the same packaging: `master/states/proposals/owl-finals-2026-10-05/` (README there).

## Correction, 22 October 2026 (J7, Science's ruling 2): the glyph sources ship inside this set
At Carey's final, Science ruled (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-J7-RULINGS.md f06cf207c3574bc4, ruling 2) that the four glyph sources the centre-mark
generator read at build time ship with this set, byte-identical, under `glyphs/` at the dose-01-meander-v2 root, and that the two files which cited them by an
absolute path on the build machine cite them at `glyphs/<name>` instead. Done by Claude Code thread 18:
- `glyphs/identity_diamond_one_outline.svg` e5401609bd7e1a36 (NORMATIVE), `glyphs/sigma_v_twin_look2.svg` 401f32832d833b47 (NON-NORMATIVE),
  `glyphs/sigma_h_twin_look2.svg` 924510f313db0728 (METACOGNITIVE), `glyphs/tri_solid_A_U85_FINAL_G0.575388.svg` 6a439aa605cd2098 (CRITICAL): the same
  bytes the sealed manifest already listed for them, now at a path inside the set (notation geometry only; Science checked).
- `master/states/proposals/notation/notation-config-final-masters.json` (e6be78f7eb9d4a40 → fa8a842b07fdd9d6) and `notation-measurements.json`
  (6f2e5705e8a521fa → 24c49d6bafacdaf5): the four `glyph_source` strings now read `glyphs/<name>`; nothing else in either file changed.
- `make_manifest.py` (56eab5a799942f3a → e92cea4d4240c57e): its glyph constant and the four glyph entries point at `glyphs/`.
- `MANIFEST.json` regenerated: 131 entries as before; the seal 61cf7a5cce723ae9 → cdb83f85645e00fd. Entry by entry against the old seal: the four
  glyph entries carry their old hashes at the new paths; the two configs above are the only entries whose hash changed; the other 125, the four masters
  (e0b6366d5c032523 / 4ef1de6ae126279e / cccfcff10dc74930 / 33413c4af9ec838c), the 40 exports, the proofs, the camera cards, the rings and the tools
  included, are unchanged by hash. The owl-finals manifest the same script writes is byte-identical before and after (dc9d5b292c5472e7).
No master, export or picture was touched. The record of this correction is this section and the ledger line TETRASEMAPHORE-CC-J7-RESEAL-RULING-2.
