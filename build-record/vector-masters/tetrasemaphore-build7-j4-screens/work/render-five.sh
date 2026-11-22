#!/bin/bash
# render-five.sh: the five J4 PNGs from the five SVG masters (resvg via tools/render.js at 1206 px, then the 300 dpi + sRGB tags), so the PNG step is
# scripted and repeatable (21 Oct skeptic panel, R3). Usage: J4_OUT=<folder> render-five.sh   (default folder = vector-masters/tetrasemaphore-build7-j4-screens)
set -euo pipefail
ROOT=/Users/careybalboa/Downloads/dose-01-meander-v2; O=${J4_OUT:-$ROOT/vector-masters/tetrasemaphore-build7-j4-screens}; PY=~/.cache/dose01-toolchain/venv/bin/python
cd "$ROOT"
for n in NORMATIVE-flashcard NON-NORMATIVE-flashcard CRITICAL-flashcard ALL-FOUR-flashcard ALL-FOUR-lockscreen; do
  svg="$O/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-$n-MASTER.svg"; png="$O/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-$n.png"
  node tools/render.js "$svg" "$png" 1206 none >/dev/null; $PY tools/png_tag.py "$png" | tail -1
  echo "$(shasum -a 256 "$png" | cut -c1-16)  $(basename "$png")"
done
