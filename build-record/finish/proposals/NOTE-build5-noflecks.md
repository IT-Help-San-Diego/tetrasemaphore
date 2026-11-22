# Build 5 rings (2026-10-09, evening): the bright flecks off

Science (9 Oct) recommends the flecks off: the pale specks on the lower sides of the gold are the fleck step of the grain filter. Carey approved
the direction with Science ("it can't become gray") but has not picked among three gold versions (1 as built · 2 flecks off · 3 flecks off +
lit edges); these rings are AHEAD of that pick. Science's recommendation and measurements: ~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-RULINGS-2026-10-09.md section 3 and update 2.

The exact commands (all with `--seamFix 1 --knobs finish/finish7-knobs-noflecks.txt`): UNCUT = `--legendKeys none`; keys21-2 = `--legendKeys 21,22,23,0,1,2`;
keys22-1 = `--legendKeys 22,23,0,1`.

The three `*-noflecks-slot820.svg` files beside the build-4 rings were made by `tools/ring_build.js --seamFix 1 --knobs finish/finish7-knobs-noflecks.txt`
(the build-4 knobs plus `--fleckOp 0`). Against the build-4 ring with the same keys each differs in exactly two lines: the `<desc>` text
(`flecks top ≈2 % @0.22` → `@0`) and the fleck step of the grain filter (`<feFuncA type="linear" slope="0.22"/>` → `slope="0"`). The build-4
rings stay here unchanged and still reproduce from `tools/ring_build.js` with no `--knobs` argument (checked byte for byte on 9 Oct).
`seam-fix/README.md` and `refute/` describe the build-4 rings and do not mention these files.
