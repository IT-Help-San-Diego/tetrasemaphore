# Datasheet HTML pages: browser measurements

Evidence for the pull request "Datasheet HTML pages generated from the audit records". This branch holds
only this file and nine screenshots; it is not meant to be merged, and can be deleted when the pull
request closes.

## What was measured

The four pages as committed in `4bdf0414a06f` on the branch `claude-code/datasheet-html` (unchanged in its second commit, `18543d50e75d`):

| page | sha256, first 16 |
|---|---|
| `site/datasheet-normative.html` | `3187edf4deef931a` |
| `site/datasheet-non-normative.html` | `0ac71ecf81f5f1f1` |
| `site/datasheet-metacognitive.html` | `9e55a4af8d07d93f` |
| `site/datasheet-critical.html` | `8193bdda30b00337` |

Served from the checkout's `site/` folder by `python3 -m http.server` on localhost, so the absolute
`/assets/` addresses resolve as they do on the site. Browser: the built-in browser pane of the Claude
desktop app, Chromium 156.0.8078.75 on macOS, device pixel ratio 2, with its viewport and colour-scheme
emulation. Measured on 15 November 2026 (Los Angeles).

For each page, viewport width and colour scheme, the page ran this in the document:

- `document.documentElement.scrollWidth` and `clientWidth`;
- the largest `getBoundingClientRect().right` over every element in `body` that has a size;
- the smallest computed `font-size` over every text node inside `main`;
- then every `details` element was opened and the first two were measured again.

## After these measurements: the station ids changed, and nothing else

The pages above are those of the branch's first two commits. Its third commit, `0aa71c9aedd9`, gives each
station article the id of its callout's `key` in the record (`#field`, `#rings`, `#meander`, `#legend`,
`#mark`, `#fix`, `#marks`) in place of `#station-<n>`. The four pages at that commit:

| page | sha256, first 16 |
|---|---|
| `site/datasheet-normative.html` | `f5bae98dad7acdbb` |
| `site/datasheet-non-normative.html` | `81571bd522c8f35b` |
| `site/datasheet-metacognitive.html` | `dcc088427d40a87a` |
| `site/datasheet-critical.html` | `8fa7e2f8ec656d4a` |

They differ from the measured ones only in `id` and `aria-labelledby` values, and the style block has no
id selector, so no box can have moved. Measured again all the same, on the new pages, at 320 px with every
source folded and unfolded: `320 / 320 / 320` on all four; and CRITICAL at 1280 px: `1265 / 1265 / 1136.5`.
Opened at `datasheet-normative.html#marks`, `datasheet-non-normative.html#fix`,
`datasheet-metacognitive.html#fix` and `datasheet-critical.html#mark`, each page's `:target` was that
station's article, at the top of the window. The screenshots below were taken before this change; the one
whose name says "station 6" shows the article now addressed as `#fix`.

## Result: no sideways scroll

`scrollWidth / clientWidth / largest right edge`, in CSS px. "Folded" is the page as it loads; "unfolded"
is with every source opened (30 on NORMATIVE and CRITICAL, 34 on the other two).

| width | scheme | NORMATIVE folded | unfolded | NON-NORMATIVE folded | unfolded | METACOGNITIVE folded | unfolded | CRITICAL folded | unfolded |
|---|---|---|---|---|---|---|---|---|---|
| 320 | light | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 |
| 320 | dark | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 | 320 / 320 / 320 |
| 375 | light | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 |
| 375 | dark | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 | 375 / 375 / 375 |
| 390 | light | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 |
| 390 | dark | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 | 390 / 390 / 390 |
| 430 | light | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 |
| 430 | dark | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 | 430 / 430 / 430 |
| 1280 | light | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 |
| 1280 | dark | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 | 1265 / 1265 / 1136.5 |

Eighty measurements, and in every one `scrollWidth` equals `clientWidth` and no element's right edge
passes it. At 1280 the 15 px difference between the window and `clientWidth` is the vertical scrollbar.

## Light and dark

The site has one theme: its style block defines one set of colours and no `prefers-color-scheme` rule,
and the pages copy that block. The computed `body` background is `rgb(7, 9, 13)` under both emulated
schemes, and the widths above are the same in both.

## Type sizes

Smallest computed font size inside `main`: **18 px** on all four pages at every width. By element:
paragraphs, list items, `summary`, `dt` and `dd` 18 px; `code` 18.36 px; `h2` 19.8 px; table cells
21.6 px; station titles (`h3`) 24.3 px; the `h1` 36 px. A folded source line (`summary`) is 30 px high.

Outside `main`, the header and footer are the site's own chrome and keep its sizes: the eyebrow line
13.68 px, the top navigation 15.48 px, the footer 15.12 px. Every page of the site has those.

## The title on a 320 px phone

The longest state name in one piece is NORMATIVE (NON-NORMATIVE breaks after its hyphen, and
METACOGNITIVE is given one break opportunity between META and COGNITIVE). At 320 px the column is
266 px wide. Measured with a canvas at the `h1`'s 36 px bold: NORMATIVE is 238.5 px in Iowan Old Style,
234.7 in Palatino, 246.7 in Georgia and 225.3 in Times New Roman, so it fits with 19 px or more to spare
in each face of the site's serif stack that this machine has. An earlier draft kept the `h1` in the
site header at 40.5 px, where the same word measured 262.9 px in Iowan Old Style (3 px to spare) and
272 px in Georgia (6 px too wide); the `h1` was moved into `main` for that reason.

## Screenshots

Taken in the same browser pane. The 320 and 375 px captures are at one image pixel per CSS pixel; the
1280 px captures are scaled by the pane to 800 px wide.

| file | sha256, first 16 | shows |
|---|---|---|
| `screenshots/320-non-normative-top.jpg` | `f7e4097f05f5d9b6` | 320 px, the top of NON-NORMATIVE: the title's three lines and the semaphore |
| `screenshots/375-metacognitive-top.jpg` | `9baa39c33cf36ab2` | 375 px, the top of METACOGNITIVE |
| `screenshots/375-metacognitive-station-6-source-open.jpg` | `9d74260f1292b2bc` | 375 px, station 6 with one source unfolded: file, sha16, field |
| `screenshots/375-metacognitive-chart.jpg` | `bd25fcbfa5484890` | 375 px, the survival chart as a table, and the start of the scale |
| `screenshots/375-critical-absent-and-chart.jpg` | `275aa1f01ee4187f` | 375 px, CRITICAL opened at `#absent`: the absence box, then the chart |
| `screenshots/375-normative-palette.jpg` | `9777c91e0f9dc407` | 375 px, NORMATIVE opened at `#palette`: swatches and contrast ratios |
| `screenshots/1280-metacognitive-top.jpg` | `ba038419b5e01dcc` | 1280 px, the top of METACOGNITIVE |
| `screenshots/1280-metacognitive-stations.jpg` | `f9de33b77803a659` | 1280 px, the stations in two columns |
| `screenshots/1280-metacognitive-chart-scale.jpg` | `1b97ab8cde155997` | 1280 px, the chart and the scale |

## What this does not cover

One browser engine on one machine. Not measured: Safari on an iPhone, Android's default serif, a screen
reader's actual speech (the accessibility tree was read: banner, navigation, main, one `h1`, the `h2`
and `h3` levels in order, an article per station, lists, tables with scoped headers, the image's
alternative text), and print.
