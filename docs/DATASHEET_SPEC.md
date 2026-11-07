# The semaphores' datasheets — spec

**Status: proposal for site version 1.1. The 1.0.0 release is published (Zenodo
10.5281/zenodo.23575816; tag `v1.0.0`, commit `833c2438fc3e`), and these sheets read that tree
and write nothing back to it.** Carey approved the direction on 22 October 2026 and the word
"datasheet" on the same day. The sheets carry a "MOCK-UP … not a release file" line until Science
and Carey approve them as final.

Four sheets are built: `datasheet_NORMATIVE.png`, `datasheet_NON-NORMATIVE.png`,
`datasheet_METACOGNITIVE.png`, `datasheet_CRITICAL.png`, each with a 1200 px preview, from one
template (`make_anatomy_plate.py --state <NAME>`), with one audit JSON per sheet and one combined
`AUDIT_REPORT.md`.

## 1. What a datasheet is here

In electronics every component ships with a datasheet: what the part is, its measured operating
characteristics, its test results, and how it is meant to be used. Gebru et al. carried the word
to datasets ("Datasheets for Datasets", arXiv:1803.09010; *CACM* 64(12):86–92, 2021). A
semaphore's datasheet says the same three things about one semaphore, and nothing beyond them:

1. **what each part is** — read out of that semaphore's master SVG;
2. **its measured values, with units** — read out of the same file, or out of the measurement
   record generated from it;
3. **how a reader checks it** — a numbered test in the published note, or a named theorem in the
   published Lean file.

Where no published text states what a part *means*, the sheet gives what the part is and stops.
Open gaps are listed in §5 for Carey rather than filled in.

## 2. Where they sit

Level 1 is the semaphores, big (on the site now). Level 2 is this: **one datasheet per semaphore,
four in all, each beside its own semaphore** — a reader who wants to go deeper opens the sheet
next to the picture they are already looking at. There is no level 3 in this pass (see §6).

## 3. The one template

### 3.1 Purpose

To let a reader take one semaphore apart, see that every mark on it is a decision with a number
behind it, and check any of those numbers themselves.

### 3.2 Register

The register is an explanatory drawing of the kind a good technical manual or a good explainer
comic uses: a clear reading order, numbered caption boxes, leader lines to the part each box
describes, plain words, flat colour. No starship or HUD effects — no glows, scan lines, reticles,
frame brackets, or readouts that only look like readouts. Storytelling shapes the order a reader
takes through the sheet; it does not add to or bend a fact. Style is carrier colour: welcome where
it is disclosed, out of place where it would change the signal.

### 3.3 Content inventory, with sources

| # | Region | Content | Source |
|---|---|---|---|
| A | Title | `<STATE> datasheet` and one line of orientation | state name from the master's filename |
| B | Orientation box, top right | How to read the sheet; the honesty rule; which marks are drafting marks | this spec |
| C | Standfirst | One sentence on what the state is, quoted | published note, "What it is" |
| D | Reference semaphore, upper left | The semaphore as the site shows it | `site/assets/TETRASEMAPHORE-<STATE>-en-1298.png` at `v1.0.0` |
| E | Detail view | One magnified crop, with its magnification and the real-world size of the area shown | rendered from the master |
| F | One measurement | Overlap of the mark with itself after each of the three moves | `notation-measurements.json`, `states[…].measure.print.iou` |
| G | Exploded stack, centre | The layers rendered separately and stacked along one axis, cavalier oblique, faces undistorted; one ISO 128 long-dash-dot centre axis through every layer's centre; a direction arrow for the drawing order | rendered per layer from the master |
| H | Callout column, right | One numbered box per station: title, measured values, one line of meaning, one line of where to check | §3.4 |
| I | Absence box | On a sheet with six stations, a short note in the vacated slot saying what is absent and why | master + published note |
| J | Footnote | Master filename, release tag, commit, DOI and full sha256; renderer and its limits; the mm scale and how it was derived; the fonts; which marks are drafting marks; the mock-up line | computed at build time |

### 3.4 What one callout box holds

- **Title** — what the part is, in plain words.
- **Two or three value lines** — measured, with units, read from the files at build time. A hex
  colour stated in a value also gets a swatch on the title row, so a stated colour is visible.
- **One line of meaning** — a short quote or close paraphrase of the published note or of the
  master's own layer label, with the line number or field recorded. Elisions are marked `…`; the
  unelided string sits in the audit JSON.
- **One line of where to check** — a numbered test from the note's "How to test it" or "The tests
  in detail", or a theorem name from the published Lean file.

Anything further goes to the audit JSON rather than onto the sheet.

### 3.5 Layout rules

- **Spatial contiguity.** Each box sits at the same vertical centre as the layer it describes, so
  its leader runs nearly horizontally and crosses nothing. (Schroeder & Cenkci 2018, *Educational
  Psychology Review* 30:679–701: g = 0.63 over 58 comparisons.)
- **Reading order is stated rather than assumed.** The stack reads bottom-up because that is the
  order the semaphore is drawn in; the sheet says so and draws a direction arrow.
- **Highlighting is sparse.** The state colour marks numbers, leaders, box rules and titles; gold
  marks measured values; the highlight cream carries body text.
- **Colour comes only from that semaphore's own master.** Ground = its field tint; numbers and
  leaders = its ring colour; values = the legend gold `#DEC875`; the Fix gold `#C7B469`; body text
  = the lit-edge highlight `#F2E4B8`. Measured contrast across the sixteen colour-on-ground pairs
  runs 5.21–14.55:1, all above the 4.5:1 floor (per-sheet figures in `AUDIT_REPORT.md`). The worst
  case is CRITICAL's state colour, `#E25C60` on `#1F100E` at 5.21:1 — the other three state colours
  sit at 7.52–8.90:1, so CRITICAL has the least headroom of the four for the type set in its own
  colour (box titles, badge numbers). Body text on every sheet is the highlight cream at
  14.49–14.55:1.
- **One size ladder for all four sheets**: title 40, box titles 22, body and values 14–15,
  sources 14. Sheet 2400 × 1500 px with a 1200 px preview.

### 3.5a One drafting style, shared by all four

Carey's note of 23 October: the marks were drawn in each semaphore's own colours with a thin line,
so they read as part of the art. A reader is better served when the two are told apart at a
glance, and each sheet already says the numbers, leader lines, boxes, centre axis and arrow are
drafting marks rather than data.

- **Colour: ice blue `#C3E6FF`.** Carey picked it from a preview on 23 October; the measurement
  behind it covers colour-blind readers as well as normal vision. Version 4 used signal green
  `#02FF85`, which measured well under normal vision but turned pale gold under simulated
  dichromacy, close to the art's gold — ΔE2000 to the nearest art colour `#DEC875` of 3.4
  (Machado, Oliveira & Fernandes 2009, severity 1.0) and 3.5 (Viénot, Brettel & Mollon 1999) under
  deuteranopia, 8.8 and 9.4 under protanopia. `choose_drafting_colour.py` now scores every
  candidate across seven views — normal vision, and protanopia, deuteranopia and tritanopia under
  both models, each applied in linear RGB — and keeps those clearing 7:1 on all four grounds.
  Ice blue's smallest difference from any art or text colour is ΔE2000 21.42 under normal vision
  (nearest `#B498E6`) and 15.33 at worst across the six colour-blind views (Machado protanopia,
  nearest `#4FB5B5`); its farthest art colour is `#332A11` at 74.64. It appears in none of the
  art. Contrast against the four grounds runs 14.07–14.12:1. The search ranks it 20th of 8486
  qualifying candidates, with `#CFF2FF` first at 16.31 — 0.98 ΔE2000 units apart in the worst
  view; the sheets carry Carey's choice, and `AUDIT_REPORT.md` prints the ranking so the gap is
  visible rather than hidden.
  The Viénot projection is derived in the script from the plane through white and an anchor
  primary rather than copied as a printed matrix: for protanopia the derivation reproduces that
  paper's published coefficients (0.11238 / 0.88762) to five places, which is the check that the
  construction is right. Its tritanopia case is taken as the plane through white and the red
  primary, an approximation, and the report labels it as one.
- **A halo in the sheet's own ground**, 4 px each side at 2400 px wide (2 px at the 1200 px
  preview), so every mark separates from whatever it crosses. Where a mark passes over the
  lightest gold and cream, mark-to-art contrast falls below 3:1 on 4–9 % of its pixels; the halo
  carries the separation there, at the ground contrast above.
- **The centre axis stops 3 px short of any part it passes behind**, at 2400 px wide. The axis is
  drawn to its own layer and that layer is cleared wherever the art beneath it, dilated by 3 px,
  is present, so the gap is ground and the separation is there without a halo being painted over
  the artwork. Measured on the finished sheets, the nearest axis pixel sits 4.0 px from the
  nearest art pixel on each of the four.
- **Weights, px at 2400 px wide:** detail window 9, corner brackets 9, panel frame 9, leader lines
  3, box rules 4, centre axis 2, badge radius 16, anchor dot radius 5. Measured against the art in
  the window region at the reference semaphore's 428 px: the 9 px core is above the median art
  line on all four sheets (medians 6.00, 6.00, 6.00 and 8.00 px, the widest being CRITICAL's), and
  the 17 px assembly — core plus halo on both sides — is above the thickest single art stroke on
  all four (6.00, 10.00, 12.00 and 12.65 px, the thickest being CRITICAL's). `AUDIT_REPORT.md`
  computes both comparisons from the per-sheet rows rather than restating them.
- **Everything else keeps its colours**: the semaphore art, the stacked layers, the overlap bars
  and all text.
- **The orientation box names the style** in one sentence, so the convention is stated rather than
  left to be worked out.
- **The window and the panel are paired by letter (A)** rather than by connecting lines: at the
  new weight a connector ran across the caption between them.

### 3.6 The honesty rule

Every line, number, tick and label that states a fact is read from the master, from the
measurement record made from it, or quoted from the published note, and carries its source (file,
sha16, and the field or line) into the sheet's audit JSON. No decorative gauges, grids, scan
lines or invented numbers.

Two kinds of mark are drawn that are not data, and each sheet's footnote names both:

1. **Drafting marks** — leader lines, number badges, caption boxes, the centre axis, the direction
   arrow, the detail frame.
2. **The field plate's edge** — stroked at the disc's own measured radius, because a dark disc is
   otherwise invisible on a sheet of the same dark colour.

### 3.7 Checks the build runs

Implemented in `make_anatomy_plate.py`; results for all four in `AUDIT_REPORT.md`.

1. **Every quote is looked up in the published note before anything is drawn.** The build stops if
   a cited string is absent (markdown emphasis normalised away). Result across the four sheets:
   **25 quotations** and **12 pointers** verified, 0 failures. The two counts separate how a sheet
   presents a cited string: a quotation reproduces the note's own words, and stops with an ellipsis
   wherever the source sentence continues, adding no punctuation of its own; a pointer names a test
   or a section in wording of ours, with the test's title or sentence verified verbatim behind it.
   A reading of ours that the note does not state is printed as a reading and labelled as one, as
   in CRITICAL's absence box.
2. **Every Lean name is looked up** as a `theorem` or `lemma` declaration in
   `proofs/TetrasemaphoreAlgebra.lean` at `v1.0.0`. Result: 7 citations verified.
3. **Every value is re-read from the files at build time.** No number is typed into the script.
   The mm scale is itself derived: each master states its symmetry bars as both 31.911 × 7.18 slot
   units and 4.0 × 0.9 mm, giving 1 mm = 7.9778 slot units and a 102.786 mm semaphore; two further
   statements in the same file (first bar inner edge 20.855 mm, outer edge 24.255 mm) reproduce
   that scale exactly.
4. **Text geometry.** Every drawn string is registered and tested for overlap with every other and
   for falling inside the canvas. Result: 0 overlaps, 0 outside, on all four.
5. **Contrast** of every text colour against each sheet's own ground, tested against a 4.5:1 floor
   (WCAG 2.1 AA for normal-size text) rather than only recorded: the build stops if a colour falls
   below it, and the count of colours below the floor goes into each audit JSON. Result: 0 below
   the floor on all four; the range across the 16 pairs is 5.21:1 (CRITICAL's state colour on its
   own ground) to 14.55:1, which `AUDIT_REPORT.md` computes from the table rather than restating.
   An earlier draft of this spec listed contrast among the checks while the script only recorded
   the values — the floor test is what makes the listing true.
6. **Source and field agree — a shape check, run in both directions.** Each string's field names a
   place that can exist in the file its source names: a master source carries a master XPath
   (`g#…`, `svg/…`), a measurement-record source a `states[…]` path, a note source a line
   reference, a Lean source a bare theorem name. Result: 116 strings checked, 0 faults.

   **What this check does not reach.** It tests the shape of the reference, not where a figure came
   from. In the first pass two provenance faults were found by review rather than by this audit: a
   measured pixel count attributed to the master (which the audit now catches by construction), and
   a master-stated bar spacing merged into a value whose source and field were both validly the
   measurement record — nothing about its shape is wrong, so the audit stays silent. The guard for
   that second direction is a different one: **one origin per value string**, checked by eye at
   review. A reader implementing check 6 can expect it to cover one direction only.
7. **The drafting style's measurements.** Per sheet: the drafting colour, its CIEDE2000
   difference from every colour in the four palettes and from every text colour, the same
   difference under each of the six colour-blind views (protanopia, deuteranopia and tritanopia
   under both the Machado 2009 and the Viénot 1999 models, each applied in linear RGB), its
   contrast against the ground, the measured contrast of the marks against the art beneath their
   footprint (minimum, median, and the count of pixels below 3:1), the count of centre-axis pixels
   sitting over art and the count of art pixels now under a drafting halo, the line weights, and
   the art's line widths in the window region. Written into each audit JSON by
   `measure_drafting.py`, except the pixel counts, which the build measures on the finished
   image. The axis figure worth reading is the distance, not the count: the count of axis pixels
   over art is 0 on all four, but the same mask does the clearing and the counting, so that zero
   is forced by construction and a wrong radius would not show in it. The measured gap can come
   out wrong, and does not: the nearest axis pixel on each sheet sits **4.0 px** from the nearest
   art pixel, against the 3 px clearance setting.
8. **Quotation punctuation.** Every span a sheet wraps in typographic quotes is tested against
   the note: a span ending in punctuation claims the note carries that mark at that point, and a
   span ending in an ellipsis claims nothing. Result: 29 spans checked across the four sheets, 0
   faults. `test_quotation_punctuation.py` runs the check over the three faults review found
   (station 5's colon, METACOGNITIVE's gold comma, NORMATIVE's absence-note comma), their three
   corrected forms, the one full stop the note does have (CRITICAL's `a single point for C₂.`) and
   three invented cases (a semicolon the note lacks, a comma in place of its full stop, a span
   absent from the note) — ten cases, all as intended — so a zero here carries information.
9. **Per-state station assertion.** The template reads each master's layer set rather than assuming
   it, and the station count follows from the file (§4). A state with no Fix element or no
   symmetry-mark layer gets six stations and an absence box, in place of a blank plate.

**Phone width, measured in the first pass and unchanged, since the type sizes are unchanged.** The
smallest type is 14 px at 2400 px wide. Scaled to a 430 px phone that is 2.5 px; at the 1200 px
preview it is 7.0 px; it first reaches 11 px at a display width of 1886 px. One wide sheet does not
serve a phone. A reflowed narrow layout — the same callouts, one per screen, each with its own
layer render — is the open piece of work, with the wide sheet kept for desktop and print.

## 4. The four instances

One script, one template; the state is a parameter and the master and its site asset are swapped.
What differs between the four, read from the four masters at `v1.0.0`:

| State | Mark | Gold Fix element | Symmetry bars | Stations | Twin |
|---|---|---|---|---|---|
| NORMATIVE | I | **none as its own layer** — the whole mark is gold (`glyph-body` fill `#C7B469`) | 8, on two axes, gold | 6 | — |
| NON-NORMATIVE | σᵥ | `rect` 9.3307 × 256.26, vertical | 4, on the vertical axis, state colour | 7 | METACOGNITIVE |
| METACOGNITIVE | σₕ | `rect` 336.21 × 9.3307, horizontal | 4, on the horizontal axis, state colour | 7 | NON-NORMATIVE |
| CRITICAL | C₂ | `circle` r 21.9 token units = 1.58 mm — a single point | **no `symmetry-marks` layer** | 6 | — |

This table is the note's own sentence made checkable: "Gold shows what the semaphore's move leaves
in place: the whole figure for I, a vertical line for σᵥ, a horizontal line for σₕ, a single point
for C₂" (note, lines 95–96). The four masters carry it literally.

Two further differences the template reads rather than assumes:

- **The headline measurement differs in shape.** Each semaphore's own move is the one whose overlap
  exceeds 0.99: NORMATIVE 0.9959 / 0.9968 / 0.9928 under all three, NON-NORMATIVE 0.9999 under σᵥ,
  METACOGNITIVE 0.9992 under σₕ, CRITICAL 0.9985 under C₂, with the non-own moves between 0.1437
  and 0.1895. NORMATIVE's sheet marks all three rows as its own, which is the point of I.
- **The mark is assembled differently.** NON-NORMATIVE and METACOGNITIVE define one token and use
  it twice, the second use a `scale(1 -1)` mirror; CRITICAL defines one token and uses it five
  times, two of them `rotate(180)`; NORMATIVE is one outline plus the shared line, four uses and no
  token definition.

## 5. Open questions for Carey

1. **The symmetry bars.** The master says what they are — the drafting convention for a line of
   symmetry, ISO 128-3, proportions ours. The published note still does not explain them to a
   reader. Does the datasheet teach them, or does a later note gain a sentence?
2. **The gold finish, the sweeps and the lit edges.** The master states exactly what they are,
   physically. Nothing published says what they *mean*. Carrier colour, disclosed — or carrying
   something?
3. **The meander.** The note says how the ring behaves under the moves, not why the ring is a Greek
   meander. Is its provenance stated anywhere citable?
4. **The legend plate's position**, over keys 21–2 (45–135°): stated as a fact, with no stated
   reason.
5. **The field tints.** Each master claims "one lightness and one chroma for all four … hue from
   the coin colour". Measured in OKLCh the lightness holds (L 0.1888–0.1938, spread 0.0050); the
   chroma does not (C 0.0230–0.0326, a 42 % relative spread). Provisional: OKLCh only; CIELCh and
   HCT not tested. In which space was the claim made?
6. **Units first.** The sheets give slot units and mm together. For a general reader, should mm
   lead with slot units in brackets?
7. **Showing the twin.** The twin fact means something only as a pair. Should the two σ datasheets
   be linkable side by side?
8. **NORMATIVE's bars are gold, and its label says otherwise.** All four masters carry the same
   symmetry-mark label text, which ends "the coin colour". In NORMATIVE the bars are filled
   `#C7B469`, the Fix gold, while its ring colour is `#D5AF64` — consistent with I holding the
   whole figure, and at odds with the shared label text. The sheets print the fill read from the
   file. Worth a label correction in a later artwork pass?
9. **The word on the sheets.** Prose now says "semaphore" throughout, while the file names of the
   sealed masters keep "medallion" and "coin". The sheets quote those file names as they are.

## 6. Later, not now

A map of all four states and the one move between any two, and a production sheet of brand assets
(colours, fonts with licences, measured minimum print sizes, calibration tiles), were considered
for this pass and set aside: four datasheets from one template, and no more.
