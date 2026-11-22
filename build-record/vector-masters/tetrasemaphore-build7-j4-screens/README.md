# Dose 01 · iPhone 17 Pro · the five Tetrasemaphore screens of J4 (build-7 coins) — PROPOSAL, 2026-10-21

Science's layout spec revision 4 (`~/Downloads/TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md`, sha256-16 a2131c898acbb0e8; FINISH-TODAY update 5, 21 Oct 21:37Z),
with Carey's answers of 21 October in its §12 (question 18: the four symbols cream, the names stay on the coins, the coins as large as the safe zones allow with the
text unchanged). Card 23 (11 Oct, option 1) gives the three state cards their rows; card 25 (14 Oct) the fifth card's three lines; Carey asked for a fifth card
AND a fifth lock screen (11 Oct). Nothing here is final; Carey sees these at question 19 of Science's walkthrough, after Science's own check.
**The ALL-FOUR lock screen is HELD for Carey's phone check with the real clock** (Science, update 5: its grid starts 31 px under the clock/date band).

| file | sha16 | what |
|---|---|---|
| `dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NORMATIVE-flashcard-MASTER.svg` | **26c5648afbf9d3f8** | state flashcard (a), layered vector master |
| `dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NORMATIVE-flashcard.png` | **b8e04fd9ad63be7b** | its phone file (resvg, 1206 px; 300 dpi + sRGB tags) |
| `…-NON-NORMATIVE-flashcard-MASTER.svg` / `.png` | **06c8b13bc205a124** / **1ff196ef5092f3ae** | state flashcard (a) |
| `…-CRITICAL-flashcard-MASTER.svg` / `.png` | **7ef95fb6e0aee46e** / **9762a175f02cb364** | state flashcard (a) |
| `…-ALL-FOUR-flashcard-MASTER.svg` / `.png` | **0b83fba14b3c08d6** / **9da7baacc29fdd0a** | the fifth flashcard (b), all four coins |
| `…-ALL-FOUR-lockscreen-MASTER.svg` / `.png` | **d551d3c339cdd915** / **c5026f044c48c059** | the fifth lock screen (c), all four coins, **HELD** |
| `proofs/TETRASEMAPHORE-J4-FIVE-SCREENS-preview.png` | d7de5512907a52d5 | the five side by side, reduced |

## Sources (sha256, first 16)
- the four build-7 coin masters, `master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-<STATE>-notation-slot820.svg`: NORMATIVE e0b6366d5c032523,
  NON-NORMATIVE 4ef1de6ae126279e, METACOGNITIVE cccfcff10dc74930, CRITICAL 33413c4af9ec838c (FINAL by Carey's word, 21 Oct, walkthrough question 2);
- the no-title lock-screen master `vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg` 1cf8f0f9f4aa30ea (ground and divider 1 byte for byte);
- the accepted METACOGNITIVE lock screen, build 7, `vector-masters/tetrasemaphore-build7/…-METACOGNITIVE-MASTER.svg` a62a3dd185089960 (the row grid and layer transforms);
- DejaVu Sans Bold 2.34 `~/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf` 7e69e81478e233b8, outlined by `vector-masters/work/lockscreen/textlayout.js`
  (opentype.js 1.3.4) with its ligature step bypassed (below); resvg-js 2.6.2 through `tools/render.js`.

## Recipe (`work/build-five.js`, `work/render-five.sh`, `work/verify-five.py` — copies of the canonical scripts in `vector-masters/work/lockscreen-tetrasemaphore/`)
The build-meta7.js recipe as a layer swap on the no-title master: each coin's root content inlined verbatim (title, desc, inkscape attributes stripped; no
recolouring, clip or crop); the three state cards at `translate(312 684) scale(0.708536585)` (the owl medallion's registration, centre (602.5, 974.5), a 581 px box)
with the operator row (box stroke = the coin's ring colour, operator glyph = its mark colour), one gold rule box, divider 1 and the motto in the template's own
layers and transforms (−124.279, −99.557, −74.836, −50.115: rows at y 1328.721 / 1501.443 / 1674.164, baselines 1803.635 / 1873.510 / 1943.385); divider 2 and
the M := box dropped. The two all-four screens: the coins 2 × 2 under one uniform scale (card 0.437899692, 359.078 px coins; lock screen 0.561605269, 460.516 px
coins) from y 481.123, every id of each coin and every reference to it prefixed `n-` / `nn-` / `m-` / `c-` (spec §2); the card keeps the deck's row grid, the lock
screen's rows sit 202.877 px lower. Boxes: width = text advance + 88 to the nearest even px, centred on x 603, text from box x + 43.625; unboxed lines centred to
1/8 px. Every string is one of the nineteen of spec §8, code point for code point; the minus is U+2212 everywhere. **Text engine note:** textlayout.js as shipped
sets the fl ligature U+FB02 in "reflect" and "reflection" (advances 718.373 / 941.084); the spec's numbers (720.497 / 943.208) and §8's code points are separate
f and l, so the generator shadows the engine's glyph mapping with a per-code-point one (nothing else changes; every other string is byte-identical either way).
Ruling asked of Science: separate f and l (as built and as the approved mock-up) or the ligature. The scripts refuse to run from anywhere but their canonical
path, so a stray copy can never overwrite this record (the copies in `work/` are the record, not runnables).
Run: `node build-five.js` → `render-five.sh` → `verify-five.py <scratch dir>` (writes `work/verify_report.json` and the preview here) → `lane-check-five.py`.

## What was checked
- **Builder (Opus 5.5 agent, `work/verify-five.py`, `work/verify_report.json`):** the spec's eleven checks on all five screens, 54 counted PASS + 1 not applicable
  (check 9, deck alignment, does not apply to the lock screen by design; its rows are compared with §5 under check 6): strings exact with code points; every
  glyph in the font's cmap; each coin element for element its master (770 / 769 / 771 / 763 elements) once the prefix is applied; ids unique, 141 references
  resolving inside their own coins on the all-four screens; per-coin render check 0 / 0.000 on all eleven placements; geometry at the spec's numbers (positions
  deviate 0.000; advances ≤ 0.0005 against the spec's 3 decimals); 0 ink in y 0–450 and 2360–2622; no overlaps, all ink inside the canvas; deck alignment
  1328.721 / 1501.443 / 1674.164 / 1803.635 on the four cards; PNG tags; both regression gates (the 16 Sep σₕ row and the template's motto / ∀n / M := layers
  byte for byte).
- **Lane check (Claude Code, `work/lane-check-five.py` + `lane-check-paths.js`, written before the builder reported; `work/lane-check-five-run.json`,
  `lane-check-five-out.txt`):** 92 PASS / 0 FAIL — every coin group byte-identical to the stripped master (prefixed where the spec says), every reference inside
  its coin, per-coin render 0 / 0.000 × 11, every box / text x / baseline / divider at the spec's number to 0.000 px (divider 1 byte-identical to the 16 Sep
  layer at translate(0 −74.836) and (0 128.041)), text path data equal to a fresh run of the font at the spec's x and baseline (per code point; the ligature
  form differs only on the two NON-NORMATIVE lines), 0 ink in both bands, alpha 255, the shipped PNGs pixel-identical to a fresh lane render, tags on all five.
- **Skeptic panel (workflow wf_8681fb17-f8f, Opus 5.5: four lenses — geometry+strings, coins+ids, pixels+safety vs Science's mock-ups, records+reproducibility —
  and two skeptics per non-note finding; 10 agents, 0 errors):** no defect in any screen. Three record findings stood and are FIXED in this version (SVG descs
  regenerated, pixels unchanged byte for byte): GS-1 the ligature bypass is now stated in every desc; R1 the scripts copied whichever copy ran over the archived
  ones (now the canonical-path rule, and `render-five.sh` scripts the PNG step, R3); R2 the verifier recorded a constant PASS for the lock screen's check 9 (now
  not applicable, and the counts say 54 + 1); R7 a doubled full stop in every desc. Notes for Science: §1's "outlined … as textlayout.js" and §10's "reproduces
  textlayout.js byte for byte" cannot both hold with §3/§8's per-code-point numbers (R4/GS-1); the template's motto lines sit at x 185.875 / 248.375 where the
  §1 centring rule gives 186.375 / 249.125 (the 16 Sep master was fitted, not ruled; the new screens follow the rule, so §1 misstates the template, not the
  build); 227 ids on each all-four screen, not §10's 230 (219 in the coins + 8 of the screen's own; the 3 are Science's mock-up wrappers); against Science's
  mock-ups the positions of every box, line and coin agree to the pixel, the text differs only by anti-aliasing (≤ 51 levels on 3 px), so §10's "text identical
  between the renderers" is nearly, not exactly, true; the hidden Spanish legend layers stay hidden but, as in the accepted template, are no longer Inkscape
  layers inside the inlined coin.
- Pictures for the decision page: `decision-page/pics-jpg/FINAL-J4-*-603.jpg` (half size), shown only after Science's check (question 19).

## At final (Carey's word), Hermes
Copy by hash: the five masters beside the 16 Sep master in `vector-masters/`, the five PNGs to `share/` and `~/Downloads/printful-mockups/live-master/`, never
over an old file; the ALL-FOUR lock screen only after Carey's phone check. Claude Code then adds the README/SHA256 lines in `vector-masters/` and re-seals.
