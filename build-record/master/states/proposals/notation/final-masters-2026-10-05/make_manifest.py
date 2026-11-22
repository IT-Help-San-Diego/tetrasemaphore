#!/usr/bin/env python3
"""make_manifest.py — (re)write MANIFEST.json for the final masters (build 3) and for the owl final four. Run from the dose-01-meander-v2 folder.
README.md and the refuter records are not listed (they change after the build)."""
import hashlib, json, glob
P='master/states/proposals'; F=f'{P}/notation/final-masters-2026-10-05'; O=f'{P}/owl-finals-2026-10-05'; G='glyphs'  # the four glyph sources ship inside this set since the re-seal of 22 October 2026 (Science, J7-RULINGS ruling 2)
STATES=('NORMATIVE','NON-NORMATIVE','METACOGNITIVE','CRITICAL')
def ent(p, role):
    b=open(p,'rb').read(); h=hashlib.sha256(b).hexdigest(); return dict(path=p, role=role, bytes=len(b), sha256=h, sha16=h[:16])
def shared():
    E=[ent('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-guard-slot820.svg','the uncut finished meander ring, seam fix on, bright flecks off, lit edges with the bow-tie guard (ring_build.js --seamFix 1 --knobs finish/finish7-knobs-noflecks.txt --litEdge 0.65; build 7)')]
    for k in ('keys21-2','keys22-1'): E.append(ent(f'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-{k}-litedge-guard-slot820.svg',f'seam-fixed cut ring {k}, bright flecks off, lit edges with the bow-tie guard, used for the window rails of the legend layers (build 7)'))
    E.append(ent('finish/proposals/NOTE-build7-litedge-guard.md','the build-7 rings: the guard, why, exact commands, the lane check numbers'))
    E.append(ent('tools/litedge.js','the lit-edge layer generator (build 7: with Science\'s one-line bow-tie guard; spec Science rulings update 3 + BUILD-7-AND-CARDS)'))
    E.append(ent('tools/sealed/litedge.js.build6-d1082feb366e17b7','litedge.js as it was for build 6 (the superseded-build-6 rings reproduce with it)'))
    E.append(ent('tools/png_tag.py','the PNG tagger (300 dpi pHYs + sRGB, gAMA, cHRM; pixels untouched; build 7)'))
    E.append(ent('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-slot820.svg','build-6 uncut ring, kept; the superseded-build-6 configs read it'))
    for k in ('keys21-2','keys22-1'): E.append(ent(f'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-{k}-litedge-slot820.svg',f'build-6 cut ring {k}, kept; the superseded-build-6 configs read it'))
    E.append(ent('finish/proposals/NOTE-build6-litedge.md','the build-6 rings: why, how, exact commands, the alpha gate result'))
    E.append(ent('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-noflecks-slot820.svg','build-5 uncut ring, kept; the superseded-build-5 configs read it'))
    for k in ('keys21-2','keys22-1'): E.append(ent(f'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-{k}-noflecks-slot820.svg',f'build-5 cut ring {k}, kept; the superseded-build-5 configs read it'))
    E.append(ent('finish/finish7-knobs-noflecks.txt','finish knobs of build 5: finish7-knobs.txt plus --fleckOp 0 (Carey with Science, 9 Oct)'))
    E.append(ent('finish/finish7-knobs.txt','finish knobs of builds 1-4 (kept; reproduces the earlier rings)'))
    E.append(ent('finish/proposals/NOTE-build5-noflecks.md','the build-5 rings: why, how, exact commands'))
    E.append(ent('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-slot820.svg','build-4 uncut ring, kept; the superseded-build-4 configs read it'))
    for k in ('keys21-2','keys22-1'): E.append(ent(f'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-{k}-slot820.svg',f'build-4 cut ring {k}, kept; the superseded-build-4 configs read it'))
    E.append(ent('master/pre-legend/MASTER-medallion-METACOGNITIVE-slot820.svg','owl source (pre-legend approved master)'))
    E.append(ent('/Users/careybalboa/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf','legend typeface file (DejaVu Sans Bold 2.34)'))
    return E
SHEET='TETRASEMAPHORE-SCIENCE-BUILD-SHEET-finals.md (9e021adbe53cb849 for build 3; v4 on disk 891b0e7f167bdf66)'
# --- the four notation masters
E=[]
for st in STATES: E.append(ent(f'{F}/MASTER-medallion-{st}-notation-slot820.svg', f'MASTER {st}: layered vector master (field, rings, uncut meander, legends en + es with the stamp cut in, centre mark, symmetry marks)'))
for p in sorted(glob.glob(f'{F}/MASTER-*-preview.png')): E.append(ent(p,'generator preview, 1640 px'))
for p in sorted(glob.glob(f'{F}/png/*-en-*.png')): E.append(ent(p, 'flattened PNG, field included, English legend; renderer resvg-js 2.6.2 (tools/render.js)'))
for p in sorted(glob.glob(f'{F}/png/*-es-*.png')): E.append(ent(p, 'flattened PNG, field included, Spanish legend; renderer resvg-js 2.6.2 (tools/render.js)'))
for p in sorted(glob.glob(f'{F}/proofs/*.png')): E.append(ent(p, 'proof picture (no legend = the uncut ring / set sheets / stamp before and after)'))
for p in sorted(glob.glob(f'{F}/scan-cards/*.png')): E.append(ent(p, 'caption-free image for the camera test'))
E.append(ent(f'{F}/notation-measurements.json','generator measurements for the four masters (also holds run timings and work-folder paths: a rerun matches every measured value, not this hash)'))
E.append(ent(f'{F}/research/spanish-terms-raw.json','Spanish legend words: raw research record (written before INFORMATIVO was chosen)'))
E.append(ent(f'{P}/notation/notation-config-final-masters.json','generator config: centre marks and symmetry marks; swapped_node_index 12 since build 6 (the lit layer is one more root child before the mark), otherwise build 2 unchanged'))
E.append(ent(f'{P}/layered/states-config-layered.json','generator config: layered base masters (field tints, legends, windows, stamp cut-in)'))
for st in STATES: E.append(ent(f'{P}/layered/MASTER-medallion-{st}-layered-slot820.svg','layered base master (centre still the owl; input to the notation generator; contains the licensed owl vector: private register only)'))
E.append(ent(f'{P}/layered/layered-build.json','generator report for the bases, with the measured clearances of every legend'))
E.append(ent('master/states/states-config.json','config of the approved owl coins (the centre-mark generator reads the state colours and windows from it; the guard uses it)'))
E+=shared()
for p,r in ((f'{G}/identity_diamond_one_outline.svg','glyph source NORMATIVE'),(f'{G}/sigma_v_twin_look2.svg','glyph source NON-NORMATIVE'),(f'{G}/sigma_h_twin_look2.svg','glyph source METACOGNITIVE'),(f'{G}/tri_solid_A_U85_FINAL_G0.575388.svg','glyph source CRITICAL'),
            ('/System/Library/Fonts/Supplemental/STIXTwoMath.otf','notation typeface file (STIX Two Math)')): E.append(ent(p,r))
for t in ('build_notation.py','build_states_layered.py','export_set.py','ring_build.js','legend.js','compose.py','finish7.js','meander3.js','render.js','build_states.py'): E.append(ent(f'tools/{t}','tool'))
E.append(ent('tools/sealed/build_states_layered.py.before-cut-in-9ecd029d3f637b44','build_states_layered.py as it was for build 2'))
for t in ('lane-verify-final-masters.py','lane-verify-build7.py','lane-verify-build7-output.txt','lane-verify-build7-report.json','lane-verify-build6.py','lane-verify-build6-output.txt','lane-verify-build5.py','lane-verify-build5-output.txt','lane-verify-build3.py','lane-stamp-floor.py','lane-stamp-floor.json','labels-only-diff.py','refute-build3.json','window-ends-build3-resvg-4920.png','window-end-METACOGNITIVE-left-inkscape.png'): E.append(ent(f'{F}/refute/{t}','check or check record'))
for st in STATES: E.append(ent(f'{F}/refute/build3-first-pass-as-refuted/notation/MASTER-medallion-{st}-notation-slot820.svg','first pass of build 3, as the independent refuters examined it (differs from the master in layer-label text only)'))
M=dict(_doc=f'Tetrasemaphore proposed masters (BUILD 7, 2026-10-14; build 3 of 2026-10-05 was the first of this set) by the Claude Code lane to Science build sheet {SHEET}. Build 7 = build 6 with Science\'s one-line bow-tie guard in litedge.js (no strip of the lit edge spans a join turning more than 170 deg: the 48 hairpins of the 342.854-unit rail; TETRASEMAPHORE-SCIENCE-build7-litedge-guard.diff bf7d5264f178d5f1, ordered in BUILD-7-AND-CARDS) and 300 dpi + sRGB tags on every PNG (pixels as rendered); build 6 is in superseded-build-6/. Build 6 = build 5 with the lit edge (gold version 3, Carey pick; Science rulings update 3): one vector layer finalA5-litedge above the finish in the ring and in the two window-rails copies of every master, so the lit rails run past the stamp where the raster reference from Science stopped at the plate, the one deliberate difference; Science checked build 6 on 10 Oct (pass) and ruled the rails stay lit as built (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-6-CHECKED.md); build 5 = build 4 with the gold bright flecks off and CRÍTICO per Science ruling C; build 4 = build 3 with INFORMATIVO at 1.10; build 3 = build 2 with the stamp cut into the ring (section 15) and INFORMATIVO (section 16). PROPOSALS until Carey says final and Hermes moves them. Paths are relative to the dose-01-meander-v2 folder unless absolute. Not listed: MANIFEST.json itself, README.md, earlier refuter records in refute/, the rest of refute/build3-first-pass-as-refuted/, superseded-build-1/, superseded-build-2/, superseded-build-3/ to -6/, make_manifest.py.',
       renderer='resvg-js 2.6.2 via tools/render.js (node); 820 slot units = 102.785 mm', files=E)
json.dump(M,open(f'{F}/MANIFEST.json','w',encoding='utf-8'),indent=1,ensure_ascii=False); print('wrote', f'{F}/MANIFEST.json,',len(E),'entries')
# --- the owl final four
E=[]
for st in STATES: E.append(ent(f'{O}/MASTER-medallion-{st}-owl-slot820.svg', f'OWL MASTER {st}: layered vector master (field, rings, uncut meander, legends en + es with the stamp cut in, owl); contains the licensed owl vector: private register only, publish the PNGs'))
for p in sorted(glob.glob(f'{O}/png/*-en-*.png')): E.append(ent(p, 'flattened PNG, field included, English legend; renderer resvg-js 2.6.2 (tools/render.js)'))
for p in sorted(glob.glob(f'{O}/png/*-es-*.png')): E.append(ent(p, 'flattened PNG, field included, Spanish legend; renderer resvg-js 2.6.2 (tools/render.js)'))
for p in sorted(glob.glob(f'{O}/proofs/*.png')): E.append(ent(p, 'proof picture (no legend = the uncut ring / set sheets)'))
E.append(ent(f'{O}/states-config-owl-layered.json','generator config (the notation bases config with edition owl)')); E.append(ent(f'{O}/layered-build.json','generator report'))
E+=shared()
for t in ('build_states_layered.py','export_set.py','ring_build.js','legend.js','compose.py','finish7.js','meander3.js','render.js'): E.append(ent(f'tools/{t}','tool'))
for st in STATES: E.append(ent(f'{F}/refute/build3-first-pass-as-refuted/owl/MASTER-medallion-{st}-owl-slot820.svg','first pass, as the independent refuters examined it (differs from the master in layer-label text only)'))
for st in STATES: E.append(ent(f'{O}/classic/MASTER-medallion-{st}-slot820.svg','first packaging (2026-10-04), kept: the owl block and English letters of the layered master are these bytes'))
M=dict(_doc=f'Owl Semaphore proposed four in the layered packaging (BUILD 7, 2026-10-14; first built 2026-10-05) by the Claude Code lane to Science build sheet {SHEET}, section 14 (field in the state tint, uncut ring, legend pairs) and section 15 (stamp cut in). Build 7 = build 6 with Science\'s one-line bow-tie guard in litedge.js and 300 dpi + sRGB tags on every PNG; build 6 is in superseded-build-6/. Build 6 = build 5 with the lit edge (gold version 3, Carey pick; Science rulings update 3): finalA5-litedge above the finish in the ring and in the two window-rails copies of every master, so the lit rails run past the stamp where the raster reference from Science stopped at the plate, the one deliberate difference; Science checked build 6 on 10 Oct (pass) and ruled the rails stay lit as built (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-BUILD-6-CHECKED.md); build 5 is in superseded-build-5/. PROPOSALS until Carey says final and Hermes moves them. Paths are relative to the dose-01-meander-v2 folder unless absolute. LICENCE: the owl SVGs stay in the private register (master/states/STATES-SPEC.md); the public copies are the PNGs. Not listed: MANIFEST.json itself, README.md, the rest of classic/ (its own MANIFEST.json is there; its transparent and on-dark PNGs are retired, in classic/retired-png-do-not-publish/).',
       renderer='resvg-js 2.6.2 via tools/render.js (node); 820 slot units = 102.785 mm', files=E)
json.dump(M,open(f'{O}/MANIFEST.json','w',encoding='utf-8'),indent=1,ensure_ascii=False); print('wrote', f'{O}/MANIFEST.json,',len(E),'entries')
