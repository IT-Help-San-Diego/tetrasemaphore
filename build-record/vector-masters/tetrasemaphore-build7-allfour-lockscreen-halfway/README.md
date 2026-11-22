# Dose 01 · iPhone 17 Pro · the Tetrasemaphore all-four lock screen at the halfway layout (revision 6) — PROPOSAL, 2026-10-22

Carey's phone check of 22 October (decisions-via-Science items 72–73) found the revision-5 all-four lock screen too high under the clock; Science's
fitted mock-up was clear on his phone, and he asked for the master halfway between the two ("hit the halfway point for the master ... take that text
up a hair more, and the four down a tiny little bit more"). Science's FINISH-TODAY update 19 (02:24Z) gives the halfway numbers and the mock-up
`TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MOCKUP-1206x2622.png` (sha256-16 6902002ccfe5fdeb). This folder is that rebuild. Nothing here is final:
Science re-runs its checks on it, then Carey tests it on his phone with the real clock.

| file | sha16 | what |
|---|---|---|
| `dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MASTER.svg` | **c102093af228eb72** | layered vector master, 1206 × 2622 |
| `dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway.png` | **98539d7457697edb** | the phone file (resvg, 1206 px; 300 dpi + sRGB tags) |
| `proofs/TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-preview.png` | see SHA256.txt | revision 5 · revision 6 · Science's mock-up, side by side, reduced |

It replaces, for the phone test, the revision-5 screen of `../tetrasemaphore-build7-j4-screens/` (`…-ALL-FOUR-lockscreen-MASTER.svg` d551d3c339cdd915 /
`.png` c5026f044c48c059, HELD), which stays in that folder as the record of what Carey tested first.

## What changed from revision 5, and nothing else
- **The four coins:** 391.5 px across (scale 0.477439024 = 391.5/820), centred at (375.75, 864.75), (829.25, 864.75), (375.75, 1318.25),
  (829.25, 1318.25): NORMATIVE top-left, NON-NORMATIVE top-right, METACOGNITIVE bottom-left, CRITICAL bottom-right, as before; pitch 453.5 px both
  ways; the grid runs from y 669 to y 1514. Revision 5 had 460.516 px coins from y 481.123.
- **Every text row, both boxes and the divider:** 48 px further down than revision 5, as whole layers (transforms 126.598, 151.32, 176.041, 200.762):
  row 1 at y 1579.598, row 2 at 1752.32, the divider at 1925.041, the sentence baselines 2054.512 / 2124.387 / 2194.262. Strings, sizes and x
  positions unchanged (the four symbols box 692 wide at x 257; the law box 650 wide at x 278; the sentence centred on x 603 to 1/8 px).
- **One number to rule on:** update 19 says "391.5 px across (scale 0.8492 of the built coins)". 0.8492 × 460.516 = 391.07 px, 0.43 px less than
  391.5. The stated diameter was followed (its translates come out on clean values: 180 / 633.5 and 669 / 1122.5); Science may prefer the other.

## Sources (sha256, first 16)
- the four build-7 coin masters, `master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-<STATE>-notation-slot820.svg`: NORMATIVE
  e0b6366d5c032523, NON-NORMATIVE 4ef1de6ae126279e, METACOGNITIVE cccfcff10dc74930, CRITICAL 33413c4af9ec838c (FINAL, 21 Oct);
- the no-title lock-screen master `vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg` 1cf8f0f9f4aa30ea (ground and divider 1);
- the accepted METACOGNITIVE lock screen, build 7, `vector-masters/tetrasemaphore-build7/…-METACOGNITIVE-MASTER.svg` a62a3dd185089960 (rows, transforms);
- the revision-5 all-four lock screen d551d3c339cdd915 (every string, box and size; the screen the new one is measured against);
- the layout: `work/spec-rev6/FINISH-TODAY-update-19.md` 645fbdab25c36d57 (update 19 cut from `TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-FINISH-TODAY.md`,
  f9c4ac07f92cf479 at build time) and the mock-up 6902002ccfe5fdeb; the J4 layout spec revision 5 (c9f6c5f60d354a09) for everything update 19 leaves alone;
- DejaVu Sans Bold 2.34 7e69e81478e233b8 through `vector-masters/work/lockscreen/textlayout.js`, one glyph per code point; resvg-js 2.6.2 through `tools/render.js`.

## Recipe (`work/build-lock-rev6.js`, `work/verify-lock-rev6.py` — copies of the canonical scripts in `vector-masters/work/lockscreen-tetrasemaphore/`)
`build-lock-rev6.js` is `build-five.js` (the sealed J4 generator, af3ab4e85e5b1c1c) with its machinery unchanged — the three regression gates (the σₕ row
byte for byte against the 16 Sep master and the build-7 screen; the motto, ∀n and M := rows byte for byte; divider 1 and the ground identical), the
coin inlining with every id and reference prefixed n- / nn- / m- / c- (J4 spec §2), the row generator (width = advance + 88 to the nearest even px,
text from box x + 43.625) — building only the all-four lock screen with the four transforms and the 48 px row shift above. The scripts refuse to run
from anywhere but their canonical path. Run: `node build-lock-rev6.js` → `node tools/render.js <svg> <png> 1206 none` → `tools/png_tag.py <png>` →
`verify-lock-rev6.py <scratch dir>` (writes `work/verify_report.json` and the preview).

## What was checked (`work/verify_report.json`)
1. The SVG differs from the revision-5 master ONLY in the eight transforms and the metadata (title, desc, labels): with those normalised, the two
   files are byte-identical (11,576,896 bytes each). The transforms equal update 19's numbers exactly. No live text, raster, script or style.
2. The PNG: 1206 × 2622, alpha 255 everywhere, sRGB + 300 dpi tags.
3. The text band: every pixel from y 1560 down equals the revision-5 band moved 48 px, except 5 anti-aliased edge pixels of the first sentence line
   (differences of 12–13 levels out of 255, each a value between the ground and the cream): resvg composes the layer transform in floating point, so
   an integer shift can move an edge pixel by a few levels. The verifier's stated tolerance is 8 px / 16 levels, and every pixel is recorded.
4. Each coin rendered alone over the ground at its transform equals the composite inside its cell, pixel for pixel (0 / 0.000 for all four).
5. Clearances measured on the PNG: the first ink row is 669 (the coin tops), 57 px under the clock digits at y 612 (update 19 expected 56); the grid's
   last row is 1513 and the first text row 1579, 65 px apart (40·φ = 64.72); the last ink row is 2206, 91 px above the buttons at y 2298 (expected 92).
   The one-pixel differences from update 19's expectations are its rounding of 668.6 and 2206.
6. The strings' code points are the J4 spec §8's (σᵥ = U+03C3 U+1D65, σₕ = U+03C3 U+2095, C₂ = U+0043 U+2082, V₄ = U+0056 U+2084).

Proposal, not final; Science checks, then Carey decides on his phone.

## Final (22 October 2026, 06:47Z; decisions item 91)
Carey tested the phone file on his iPhone with the real clock and said, in chat to Claude Code (ledger line TETRASEMAPHORE-CC-LOCKSCREEN-HALFWAY-FINAL,
2026-10-22T06:47:31Z): "The halfway lock screen 98539d7457697edb passes on my phone; record it as final." Science had passed the file at FINISH-TODAY
update 22 (03:51Z). The master c102093af228eb72 and the phone file 98539d7457697edb are FINAL and replace the revision-5 screen
(d551d3c339cdd915 / c5026f044c48c059, held) in the release, as update 22 ruled. The sentences above that say "PROPOSAL" and "Nothing here is final"
record the state at build time and are left as written. This section and the re-sealed SHA256.txt were added by Claude Code thread 18 at the J7
re-seal (thread-18 ledger line TETRASEMAPHORE-CC-J7-RESEAL); no other file in the folder changed.
