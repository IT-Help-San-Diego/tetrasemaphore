# Build 7 rings (2026-10-14): the lit edge with Science's bow-tie guard

Build 7 = build 6 + one line in `tools/litedge.js` (Science's diff `~/Downloads/TETRASEMAPHORE-SCIENCE-build7-litedge-guard.diff`, bf7d5264f178d5f1,
tested by Science on copies on 11 October; ordered in `TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-7-AND-CARDS.md`): no strip spans a join that turns
more than 170°. Why: at a 179° join the two samples sit on one point with nearly opposite tangents, so the zero-length step between them made a
sliver through the edge point (the bow-tie that thread 10's refuters found: 24 strips on the r 342.854 rail). Science counted the outline's joins by
angle: 708 under 1°, 12 at 1–10°, none at 10–170°, 48 at about 179°, all on the 342.854-unit rail; so 170° catches exactly the hairpins. Build 6's
litedge.js is sealed as `tools/sealed/litedge.js.build6-d1082feb366e17b7`; the new file is 88bfd9d7787af720 (the guard line plus the labels saying
build 7). Nothing else changed: same knobs, same opacity law, same 2.2–4.8 px zone, same 65 levels.

The three `*-litedge-guard-slot820.svg` rings beside the build-6 `*-litedge-slot820.svg` rings (kept: the superseded-build-6 configs read them).
Commands (all with `--seamFix 1 --knobs finish/finish7-knobs-noflecks.txt --litEdge 0.65`): UNCUT = `--legendKeys none`; keys21-2 = `--legendKeys
21,22,23,0,1,2`; keys22-1 = `--legendKeys 22,23,0,1`. Uncut: 11,475 strips (build 6: 11,497), 65 levels; keys21-2 8,702; keys22-1 9,622.

Lane check before the build (`refute/lane-verify-build7.py --stage A`, matching Science's dry run to the decimal): lit pixels within 0.16 mm of the
ink's edge above 0.02: 91 → **0**; pixels above 0.67: 20, peak 0.784 (accepted by Science as strip overlaps, not bow-ties; their positions are in the
report); the layer alone against Science's alpha reference at 1298 px: mean |Δα| 0.0060, 99th percentile 0.114 (unchanged); each ring at 1298 px against
its build-6 ring: at most 6 levels, 18–19 px over 2, none over 8. Without `--litEdge` ring_build.js still reproduces the build-5 ring byte for byte.
