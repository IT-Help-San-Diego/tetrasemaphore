# Build 6 rings (2026-10-10): the lit edge (gold version 3)

Carey, 9 October, judging Science's large METACOGNITIVE picture: "Three flecks off and lit edges in the ring's own gold." Science's spec:
~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-RULINGS-2026-10-09.md, update 3 (5182233203276df1).

The three `*-litedge-slot820.svg` files beside the build-4 and build-5 rings are the build-5 (no-flecks) rings plus one layer, `finalA5-litedge`,
drawn directly above `finalA5-finish`: the ridge zone 2.2–4.8 print px inside every edge of the ink, in the ring's highlight gold #F2E4B8 at
opacity 0.65 × max(0, n·L)², n = that edge's outward unit normal, L = the sweep A axis toward the top of the coin (83.094°; (-0.12024, -0.99274)).
Pure vector (`tools/litedge.js`, called by `tools/ring_build.js --litEdge 0.65`): every line and arc of the outline is sampled (chord error
≤ 0.05 slot units, ≤ 10° of turn and < 0.02 of opacity per sample), each sample run with one opacity (quantised to 0.01) becomes one strip from
the 2.2 px offset to the 4.8 px offset; strips at opacity 0 are left out. The uncut ring: 11,497 strips in 65 levels. finish7.js is untouched;
without `--litEdge` ring_build.js still reproduces the build-5 rings byte for byte.

Commands (all with `--seamFix 1 --knobs finish/finish7-knobs-noflecks.txt --litEdge 0.65`): UNCUT = `--legendKeys none`;
keys21-2 = `--legendKeys 21,22,23,0,1,2`; keys22-1 = `--legendKeys 22,23,0,1`.

Science's acceptance test, run before the build on the uncut ring (the layer alone, white on transparent, against
~/Downloads/TETRASEMAPHORE-SCIENCE-lit-edge-alpha-reference-2460.png c73e53800548c001, both at 1298 px): mean |Δα| 0.0060 over the gold
(limit 0.01), 99th percentile 0.114 (limit 0.15), largest 0.25 at corners (allowed). Against build 5 each ring differs in the `<desc>` line and
the inserted layer only. The window rails beside the legend carry the lit edge too (the plate hides the rest), so the lit rail runs unbroken
past the stamp; Science's raster preview could not do that, and that is the one place a build-6 coin differs from its option-3 reference.
Science checked build 6 and ruled on 10 October (`~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-6-CHECKED.md` 966a51a8e1212a52): pass;
the window rails stay lit, as built. `seam-fix/README.md` and `seam-fix/refute/` describe the build-4 rings and do not mention these files (nor the
build-5 `-noflecks-` ones: `NOTE-build5-noflecks.md`).
