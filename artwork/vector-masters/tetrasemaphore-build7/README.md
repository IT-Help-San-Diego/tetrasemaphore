# Dose 01 · iPhone 17 Pro lock screen · the METACOGNITIVE Tetrasemaphore coin, build 7 — PROPOSAL, 2026-10-14

Science's wake-up packet J2 (11 Oct): "the METACOGNITIVE lock screen regenerated from the build-7 coin (build-four.js, METACOGNITIVE only)". Carey accepted
the build-6 METACOGNITIVE screen by eye on 11 October (card 16: "looks awesome … exactly what you should have done"); on 14 October, on the page, under the
held lock-screen card: "That looks good to me." The three withdrawn screens (NORMATIVE, NON-NORMATIVE, CRITICAL) are not rebuilt; their replacements are the
flashcards of card 23 (decided 11 Oct) and the fifth, all-four card (card 25, yes 14 Oct), both waiting for Science's layout spec.

| file | sha16 | what |
|---|---|---|
| `dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE-MASTER.svg` | **a62a3dd185089960** | layered vector master, 1206 × 2622 |
| `dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE.png` | **f2e7dee3412f5b92** | the phone file (resvg, 1206 px; 300 dpi + sRGB tags) |

## Sources (sha256, first 16)
- lock-screen master, no title, 16 Sep: `../dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg` 1cf8f0f9f4aa30ea (its resvg render at 1206 px = `../../share/dose-01-iphone-17-pro-lockscreen-1206x2622-v3.png` 5264ef2273e51318, byte for byte, re-checked today)
- the build-7 METACOGNITIVE coin: `master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-METACOGNITIVE-notation-slot820.svg` **cccfcff10dc74930** (build 6's was 79fd3f8291b39900)
- the operator and its mapping: the Owl Semaphore's own table, σₕ (x, y) → (x, −y); the box in the coin's ring colour #B498E6, the glyph in #B498E6, the rest cream #E8E0D2; the ∀n line, the motto and M := as on the build-6 screen.

## Recipe (`work/build-meta7.js` = `../work/lockscreen-tetrasemaphore/build-four.js` of build 6, METACOGNITIVE only, reading the build-7 coin)
The 16 Sep `assemble.js` medallion step as a layer swap on the no-title master: the coin's root content inlined verbatim at `translate(312 684) scale(0.708536585)`
(centre (602.5, 974.5), a 581 px box), editor attributes, title and desc stripped; the σₕ row replaced by the operator row (box width = text advance + 88 to the
nearest even px = 702, text from box x + 43.625 = 295.625, baseline 1526.625 in with-title coordinates; the generator reproduces the 16 Sep σₕ row byte for
byte as its regression gate). `META7_SHA16=cccfcff10dc74930 node ../work/lockscreen-tetrasemaphore/build-meta7.js`, then `node tools/render.js <svg> <png> 1206 none`,
then `tools/png_tag.py` on the PNGs.

## What was checked (`work/verify-meta7.py`, run in `work/verify-meta7-run.json`)
- text identical to the 16 Sep master outside the medallion layer and the operator row; the coin inlined verbatim (element for element = the build-7 master);
- against the 16 Sep render at 1206 px: 0 pixels differ outside the coin (r 292) and the row band, so the alignment on Carey's phone is the one in his screenshot;
- against the build-6 screen (b27d3f74029358e5 / 5e065f0dd429e4fe): identical text outside the medallion, the title and the desc; 10 pixels differ, at most
  5 levels, all inside the coin (the hairpins of the inner rail where the guard removed the bow-ties), 0 outside it;
- no live text, no raster, no duplicate ids; alpha 255 everywhere.
Pictures: `proofs/TETRASEMAPHORE-LOCKSCREEN-METACOGNITIVE-build6-vs-build7-1206.png`, `proofs/…-build7-coin-and-row-3x.png`. Hashes: `SHA256.txt`.

## At final (Carey's word), Hermes
Copy by hash: the master beside the 16 Sep master in `vector-masters/`, the PNG to `share/` and `~/Downloads/printful-mockups/live-master/`, never over an old file.
Claude Code then adds the README/SHA256 lines in `vector-masters/` and re-seals.
