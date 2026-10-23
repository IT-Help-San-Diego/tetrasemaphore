#!/usr/bin/env python3
"""Lane's own check of BUILD 5 (run from the dose-01-meander-v2 folder). Build 5 = build 4 with two changes (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-RULINGS-2026-10-09.md):
CRÍTICO set to Science's ruling C, Carey's choice (the word 5.904 units outward, the accent its own stroked path), and the bright flecks of the
gold off (one number in the grain filter) — Science's recommendation and the direction Carey approved, his pick among three gold versions open. So, against build 4 (superseded-build-4/):
 A. every master (notation, owl, layered; 4 states each) equals its build-4 file byte for byte after exactly these allowed differences:
    the fleck step slope 0.22 -> 0 (three places: the ring and its two window copies), the ring's <desc> line, the two rails labels naming
    the *-noflecks-* ring files, and on CRITICAL only, the Spanish glyph group and the Spanish lettering label;
 B. CRITICAL's Spanish glyph group (notation and owl, identical to each other) matches Science's reference 9e8f7d33137c8ecc within 0.02 mm:
    seven glyph outlines unchanged, every transform moved 5.904 units outward on its own radial, the accent as its own path
    (id legend-accent-es, the I's transform then translate(0 -2.2338), stroke #DEC875 width 1.6753, round joins);
 C. the three no-flecks rings differ from the build-4 rings in exactly two lines each;
 D. the builder's report: CRITICAL es clearances 0.769 mm to each rail and 0.591 mm from the accent to the letter (102.785 mm; x1.0692 at
    109.9 mm = 0.82 / 0.63; Science measured 0.82 / 0.64 with resvg), every other legend's facts as in build 4;
 E. the Spanish layers hidden, the English shown, one outline per letter, no depth effects, words outside the SVGs; the approved masters and
    the guard untouched; the export counts."""
import re, hashlib, sys, json, glob, os, math
import xml.etree.ElementTree as ET
P = 'master/states/proposals'; F = f'{P}/notation/final-masters-2026-10-05'; O = f'{P}/owl-finals-2026-10-05'; L = f'{P}/layered'
REF = os.path.expanduser('~/Downloads/TETRASEMAPHORE-SCIENCE-CRITICO-accent-C-reference.svg')
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL'); MMU = 102.785 / 820
ES = {'NORMATIVE': 'NORMATIVO', 'NON-NORMATIVE': 'INFORMATIVO', 'METACOGNITIVE': 'METACOGNITIVO', 'CRITICAL': 'CRÍTICO'}
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
ok = True; n = 0
def check(name, cond, detail=''):
    global ok, n; ok &= bool(cond); n += 1; print(('PASS' if cond else 'FAIL'), name, detail)
def block(s, gid):
    key = f'<g id="{gid}"'; assert s.count(key) == 1, (gid, s.count(key)); i = s.index(key); d = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        if m.group(0) == '</g>':
            d -= 1
            if d == 0: return s[i:i + m.end()]
        else:
            gt = s.index('>', i + m.start())
            if s[gt - 1] != '/': d += 1
FLECK0, FLECK22 = '<feComponentTransfer in="fleck0" result="fleck"><feFuncA type="linear" slope="0"/>', '<feComponentTransfer in="fleck0" result="fleck"><feFuncA type="linear" slope="0.22"/>'
def normalise(s, st):
    """build 5 -> what build 4 should be, with counts of each allowed difference"""
    c = dict(fleck=s.count(FLECK0), desc=s.count('flecks top ≈2 % @0)'), rails=s.count('-noflecks-slot820.svg'))
    s = s.replace(FLECK0, FLECK22).replace('flecks top ≈2 % @0)', 'flecks top ≈2 % @0.22)').replace('-noflecks-slot820.svg', '-slot820.svg')
    if st == 'CRITICAL':
        g = block(s, 'legend-glyphs-es'); s = s.replace(g, '[[glyphs-es]]')
        s = re.sub(r'(<g id="legend-text-es" inkscape:groupmode="layer") inkscape:label="[^"]*"', r'\1 [[label]]', s, count=1)
    return s, c
def strip_b4(s, st):
    if st == 'CRITICAL':
        g = block(s, 'legend-glyphs-es'); s = s.replace(g, '[[glyphs-es]]')
        s = re.sub(r'(<g id="legend-text-es" inkscape:groupmode="layer") inkscape:label="[^"]*"', r'\1 [[label]]', s, count=1)
    return s
print('=== A. every master against build 4, allowed differences only')
for kind, D, suf in (('notation', F, 'notation'), ('owl', O, 'owl'), ('layered', L, 'layered')):
    for st in STATES:
        p = f'{D}/MASTER-medallion-{st}-{suf}-slot820.svg'; q = f'{D}/superseded-build-4/MASTER-medallion-{st}-{suf}-slot820.svg'
        s = open(p, encoding='utf-8').read(); b = open(q, encoding='utf-8').read(); ns, c = normalise(s, st)
        check(f'{kind} {st} ({sha16(p)} vs build 4 {sha16(q)}): equal after the allowed differences', ns == strip_b4(b, st), f'{len(ns)} bytes')
        check(f'{kind} {st}: the allowed differences occur exactly as expected (3 fleck steps, 1 desc, 2 rails labels)', c == dict(fleck=3, desc=1, rails=2), str(c))
        check(f'{kind} {st}: no fleck step at 0.22 remains', FLECK22 not in s and s.count('slope="0"') == 3)
print('\n=== B. CRITICAL\'s Spanish glyphs against Science\'s reference')
ref = open(REF, encoding='utf-8').read(); check('reference file on disk is 9e8f7d33137c8ecc', sha16(REF) == '9e8f7d33137c8ecc', sha16(REF))
gr = block(ref, 'legend-glyphs-es'); pr = re.findall(r'<path ([^>]*)/>', gr)
attr = lambda a, k: (re.search(r'(?:^| )%s="([^"]*)"' % k, a) or [None, None])[1]
nums = lambda t: [float(x) for x in re.findall(r'-?\d+\.?\d*', t)]
gn = block(open(f'{F}/MASTER-medallion-CRITICAL-notation-slot820.svg', encoding='utf-8').read(), 'legend-glyphs-es')
go = block(open(f'{O}/MASTER-medallion-CRITICAL-owl-slot820.svg', encoding='utf-8').read(), 'legend-glyphs-es')
gl = block(open(f'{L}/MASTER-medallion-CRITICAL-layered-slot820.svg', encoding='utf-8').read(), 'legend-glyphs-es')
check('CRITICAL: notation, owl and layered base carry the same Spanish glyph group', gn == go == gl)
pm = re.findall(r'<path ([^>]*)/>', gn); check('CRITICAL es: eight paths (seven letters + the accent)', len(pm) == 8 and len(pr) == 8, f'{len(pm)} / {len(pr)}')
worst = 0.0
for i, (a, b) in enumerate(zip(pm[:7], pr[:7])):
    ta, tb = nums(attr(a, 'transform')), nums(attr(b, 'transform')); dt = max(abs(x - y) for x, y in zip(ta, tb)) if len(ta) == len(tb) == 3 else 999
    worst = max(worst, dt); check(f'CRITICAL es letter {i}: outline identical to the reference, transform within 0.02 mm', attr(a, 'd') == attr(b, 'd') and dt * MMU <= 0.02, f'{dt * MMU:.4f} mm')
b4 = block(open(f'{F}/superseded-build-4/MASTER-medallion-CRITICAL-notation-slot820.svg', encoding='utf-8').read(), 'legend-glyphs-es'); p4 = re.findall(r'<path ([^>]*)/>', b4)
for i, (a, b) in enumerate(zip(pm[:7], p4)):
    ta, tb = nums(attr(a, 'transform')), nums(attr(b, 'transform')); r5, r4 = math.hypot(ta[0] - 410, ta[1] - 410), math.hypot(tb[0] - 410, tb[1] - 410)
    ang = lambda t: math.degrees(math.atan2(t[1] - 410, t[0] - 410))
    check(f'CRITICAL es letter {i}: 5.904 units further out than build 4 on the same radial, same rotation', abs((r5 - r4) - 5.904) < 0.002 and abs(ang(ta) - ang(tb)) < 0.001 and ta[2] == tb[2], f'dr {r5 - r4:.4f}')
check('CRITICAL es letter 2 (the I): its accent sub-contour has left the letter (build 4 had it)', attr(pm[2], 'd').count('Z') == 1 and attr(p4[2], 'd').count('Z') == 2 and attr(pm[2], 'd') == attr(pr[2], 'd'))
acc, racc = pm[7], pr[7]
check('CRITICAL es accent: id legend-accent-es, round-joined stroke #DEC875, width 1.6753', attr(acc, 'id') == 'legend-accent-es' and attr(acc, 'stroke') == '#DEC875' and attr(acc, 'stroke-width') == '1.6753' and attr(acc, 'stroke-linejoin') == 'round')
check('CRITICAL es accent: outline identical to the reference', attr(acc, 'd') == attr(racc, 'd'), attr(acc, 'd'))
ta, tb = nums(attr(acc, 'transform')), nums(attr(racc, 'transform'))
check('CRITICAL es accent: transform = the I\'s transform then translate(0 -2.2338), within 0.02 mm of the reference', len(ta) == len(tb) == 5 and max(abs(x - y) for x, y in zip(ta, tb)) * MMU <= 0.02 and ta[4] == -2.2338 and ta[:3] == nums(attr(pm[2], 'transform')), str(ta))
print(f'worst transform difference against the reference: {worst * MMU:.4f} mm')
print('\n=== C. the rings')
for name, keys in (('uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix', 'none'), ('seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2', '21-2'), ('seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1', '22-1')):
    a = open(f'finish/proposals/{name}-noflecks-slot820.svg', encoding='utf-8').read().split('\n'); b = open(f'finish/proposals/{name}-slot820.svg', encoding='utf-8').read().split('\n')
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    check(f'ring {keys}: differs from the build-4 ring in exactly two lines (desc, fleck slope)', len(a) == len(b) and len(diff) == 2 and FLECK0 in a[diff[1]] and '@0)' in a[diff[0]], f'{len(diff)} lines; {sha16(f"finish/proposals/{name}-noflecks-slot820.svg")} vs {sha16(f"finish/proposals/{name}-slot820.svg")}')
check('knobs file: finish7-knobs-noflecks.txt = finish7-knobs.txt + --fleckOp 0', open('finish/finish7-knobs-noflecks.txt').read().strip() == open('finish/finish7-knobs.txt').read().strip() + ' --fleckOp 0')
print('\n=== D. the builder\'s report')
r5 = json.load(open(f'{L}/layered-build.json', encoding='utf-8')); r4 = json.load(open(f'{L}/superseded-build-4/layered-build.json', encoding='utf-8'))
for s5, s4 in zip(r5['states'], r4['states']):
    for f5, f4 in zip(s5['legends'], s4['legends']):
        if s5['name'] == 'CRITICAL' and f5['lang'] == 'es':
            check('report CRITICAL es: 0.769 mm to each rail (ink, accent and stroke included), accent 0.591 mm from the letter', abs(f5['ink_clearance_inner_rail_mm'] - 0.769) < 0.002 and abs(f5['ink_clearance_outer_rail_mm'] - 0.769) < 0.002 and abs(f5['accent_to_letter_mm'] - 0.591) < 0.002, f"{f5['ink_clearance_inner_rail_mm']} / {f5['ink_clearance_outer_rail_mm']} / {f5['accent_to_letter_mm']}")
            check('report CRITICAL es: radial shift 5.904 units = 0.74 mm; at 109.9 mm the rail gaps are 0.82 mm', f5['radial_shift_units'] == 5.904 and abs(f5['ink_clearance_inner_rail_mm'] * 1.06922 - 0.82) < 0.005)
        else:
            same = all(f5.get(k) == f4.get(k) for k in f4 if k not in ('ink_note',)); check(f"report {s5['name']} {f5['lang']}: facts as in build 4", same)
print('\n=== E. layers, words, guard, exports')
for kind, D, suf in (('notation', F, 'notation'), ('owl', O, 'owl')):
    for st in STATES:
        s = open(f'{D}/MASTER-medallion-{st}-{suf}-slot820.svg', encoding='utf-8').read()
        for lang in ('en', 'es'):
            tx = block(s, f'legend-text-{lang}'); pl = block(s, f'legend-plaque-{lang}')
            hidden = 'style="display:none"' in tx[:tx.index('>')] and 'style="display:none"' in pl[:pl.index('>')]
            check(f'{kind} {st} {lang}: {"hidden" if lang == "es" else "shown"}', hidden == (lang == 'es'))
            paths = re.findall(r'<path ([^>]*)/>', block(s, f'legend-glyphs-{lang}')); word = (ES[st] if lang == 'es' else st).replace(' ', '')
            letters = [a for a in paths if 'legend-accent' not in a]; check(f'{kind} {st} {lang}: one outline per letter of {word}' + (' plus the accent' if st == 'CRITICAL' and lang == 'es' else ''), len(letters) == len(word) and len(paths) - len(letters) == (1 if st == 'CRITICAL' and lang == 'es' else 0), f'{len(paths)} paths')
            bare = re.sub(r' inkscape:label="[^"]*"', '', pl.replace(block(s, f'legend-rails-{lang}'), ''))
            check(f'{kind} {st} {lang}: no depth effect in the plate layer', not re.search(r'filter|Gradient|clip|stroke|opacity|<defs', bare))
        check(f'{kind} {st}: no raster, live text or font reference', not re.search(r'<image|<text|<tspan|font-family|data:', s))
        check(f'{kind} {st}: NO NORMATIVO nowhere', 'NO NORMATIVO' not in s)
for pat in (f'{F}/README.md', f'{F}/MANIFEST.json', f'{O}/README.md', f'{O}/MANIFEST.json', f'{L}/states-config-layered.json', f'{O}/states-config-owl-layered.json'):
    for q in glob.glob(pat):
        t = open(q, encoding='utf-8').read()
        t_ = t.replace('TETRASEMAPHORE-SCIENCE-CRITICO-accent-C-reference.svg', '')      # Science's reference FILE NAME is unaccented; it is not the word
        check(f'{q.split("/")[-1]} ({q.split("/")[-2]}): no unaccented semaforo / CRITICO as the Spanish word (the reference file name aside)', not re.search(r'[Ss]emaforo\b|\bCRITICO\b', t_))
for st, h in zip(STATES, ('d9d6336b0c9450ac', 'e1d83bb7e4b6017d', '3a8a7459bb1782d1', '055655372b21da5c')):
    pass
approved = {'NORMATIVE': 'd9d6336b0c9450ac', 'NON-NORMATIVE': 'e1d83bb7e4b6017d', 'CRITICAL': '055655372b21da5c', 'METACOGNITIVE': '3a8a7459bb1782d1'}
for st, h in approved.items(): check(f'approved master {st} untouched ({h})', sha16(f'master/states/MASTER-medallion-{st}-slot820.svg') == h)
check('guard d4054fa6e02e66e4 untouched', sha16('master/MASTER-medallion-METACOGNITIVE-slot820.svg') == 'd4054fa6e02e66e4')
check('notation exports: 40 PNGs (4 states x 2 languages x 5 sizes)', len(glob.glob(f'{F}/png/*.png')) == 40, str(len(glob.glob(f'{F}/png/*.png'))))
check('owl exports: 40 PNGs', len(glob.glob(f'{O}/png/*.png')) == 40, str(len(glob.glob(f'{O}/png/*.png'))))
check('scan cards: 8', len(glob.glob(f'{F}/scan-cards/*.png')) == 8, str(len(glob.glob(f'{F}/scan-cards/*.png'))))
print(f'\n{n} checks:', 'ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)
