# The tetrasemaphore.systems link-preview card (Open Graph 1200 × 630) — PROPOSAL, 2026-10-22

Science's site rulings item 5 (`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-SITE-RULINGS.md` 412ba93ba0a6979c, 22 Oct 03:12Z): "The card carries the four
build-7 coins, TETRASEMAPHORE and V₄ = {I, σᵥ, σₕ, C₂} (the fifth card's approved line), and nothing else; Claude Code builds it as the sealed master it
proposes; Science checks it; Carey sees it at card 11. Until it is sealed, the pages carry no og:image." This folder is that master. Nothing here is final.

| file | sha16 | what |
|---|---|---|
| `og-card-MASTER.svg` | **0660fd91c2999023** | layered vector master, 1200 × 630 |
| `og-card.png` | **0cf08ac9028fc22d** | resvg render at 1200 px, 300 dpi + sRGB tags |
| `og-card.jpg` | **a175dc759f3a2fd9** | the PNG re-encoded by Pillow (quality 95, 4:4:4, optimize), for the site's `og:image` (image/jpeg) |
| `proofs/og-card-preview.png` | see SHA256.txt | the PNG at half size |

## What is on it, and nothing else
- **Ground** #1D252D, the lock screens' field.
- **The four build-7 coins** in a row, NORMATIVE · NON-NORMATIVE · METACOGNITIVE · CRITICAL, each 220 px (scale 220/820 = 0.268292683), gap 40·φ =
  64.721 px, the row 1074.164 px wide centred on x 600, from y 140 to 360; the masters of `master/states/proposals/notation/final-masters-2026-10-05/`
  (e0b6366d5c032523 / 4ef1de6ae126279e / cccfcff10dc74930 / 33413c4af9ec838c) inlined verbatim with every id and reference prefixed n- / nn- / m- / c-.
- **The word TETRASEMAPHORE**, 58 px, cream #E8E0D2, centred on x 600 by its advance to 1/8 px (x 335.75), baseline 96.
- **The formula V₄ = {I, σᵥ, σₕ, C₂}** in a gold #D4A853 box 692 × 108 at x 254, y 425 (the all-four screens' box: width = advance 603.902 + 88 to the
  nearest even px, centred on x 600, text cream from box x + 43.625, baseline 498.625, stroke 4, radius 28).
- Margins: 52.95 px above the word's ink; 43.18 px from its ink to the coins; 65 px from the coins to the box; 97 px below the box; 62.92 px each side of the row.

## Sources
The four coin masters (above); the ground colour from `vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg` 1cf8f0f9f4aa30ea; DejaVu Sans Bold
2.34 7e69e81478e233b8 through `vector-masters/work/lockscreen/textlayout.js` (opentype.js 1.3.4), one glyph per code point (Science's ruling of 21 Oct);
resvg-js 2.6.2 through `tools/render.js`; `tools/png_tag.py`; the strings: TETRASEMAPHORE (the site's name) and the fifth card's line (J4 spec §8).

## Recipe (`work/build-og-card.js`, `work/verify-og-card.py` — copies of the canonical scripts in `vector-masters/work/lockscreen-tetrasemaphore/`)
`build-og-card.js` is build-five.js's machinery (the coin inlining with prefixed ids, the text engine, the box rule) on a 1200 × 630 canvas; its regression
gate regenerates the 16 Sep master's σₕ row byte for byte before anything is written. `verify-og-card.py` renders the PNG and the JPEG and checks them.
Run: `node build-og-card.js` → `verify-og-card.py <scratch dir>`.

## What was checked (`work/verify_report.json`)
1. The SVG holds exactly eight layers (ground, figure with the four coin layers, title, formula); no live text, raster, script or style; 223 ids unique,
   141 references, each resolving inside its own coin.
2. The PNG: 1200 × 630, alpha 255 everywhere, sRGB + 300 dpi.
3. Each coin rendered alone over the ground at its transform equals the composite inside its cell: 0 differing pixels, all four.
4. The two strings' code points (σᵥ = U+03C3 U+1D65, σₕ = U+03C3 U+2095, C₂ = U+0043 U+2082, V₄ = U+0056 U+2084).
5. The word is advance-centred on x 600 to 1/8 px and the box is centred on x 600 with its text at box x + 43.625 (the record's rules); the ink centres,
   597.98 and 596.09, sit left of the axis by the glyphs' side bearings, as on the screens.
6. The JPEG decodes to the PNG within 22 levels at the worst pixel, 0.76 on average.
7. The PNG has exactly three ink bands on the ground (rows 53–96, 140–359, 425–532): the word, the coins, the box; nothing else.

Proposal, not final; Science checks; Carey sees it at card 11.
