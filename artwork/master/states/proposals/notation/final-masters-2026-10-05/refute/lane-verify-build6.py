#!/usr/bin/env python3
"""Lane's own check of BUILD 6 (run from the dose-01-meander-v2 folder). Build 6 = build 5 + the LIT EDGE (gold version 3, Carey's pick 9 Oct;
spec: Science's rulings doorbell update 3): one vector layer finalA5-litedge above finalA5-finish in every ring copy, nothing else. Against build 5
(superseded-build-5/):
 A. every master (notation, owl, layered; 4 states each) equals its build-5 file byte for byte after exactly these allowed differences: the inserted
    finalA5-litedge layer (the ring's and its two window copies, ids suffixed -win-en/-win-es), the ring's <desc> sentence, and the two rails labels;
 B. the lit layer itself: 65 opacity levels of 0.01, strips only, clipped to the ink; the uncut ring's layer alone against Science's alpha reference
    c73e53800548c001 at 1298 px: mean |da| <= 0.01 over the gold, 99th percentile <= 0.15;
 C. the three litedge rings differ from the build-5 (noflecks) rings in the <desc> line and the inserted layer only; ring_build.js without --litEdge
    still reproduces the build-5 rings;
 D. the builder's report equals build 5's (the legends did not move); owl-placement is root child 12;
 E. the Spanish layers hidden, the English shown, one outline per letter (+ CRITICO's accent), no depth effects, words outside the SVGs; the approved
    masters and the guard untouched; the export counts."""
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
LIT = '<g id="finalA5-litedge"'
FLECK0, FLECK22 = '<feComponentTransfer in="fleck0" result="fleck"><feFuncA type="linear" slope="0"/>', '<feComponentTransfer in="fleck0" result="fleck"><feFuncA type="linear" slope="0.22"/>'
def normalise(s, st):
    """build 6 -> what build 5 should be, with counts of each allowed difference"""
    c = dict(lit=0, desc=0, rails=s.count(' (with their lit edges, build 6)'))
    for gid in ('finalA5-litedge', 'finalA5-litedge-win-en', 'finalA5-litedge-win-es'):
        if f'<g id="{gid}"' in s: blk = block(s, gid); assert s.count(blk + '\n') == 1; s = s.replace(blk + '\n', '', 1); c['lit'] += 1
    s, n = re.subn(r' Lit edges \(build 6, litedge\.js\): [^<]*?opacity levels\.', '', s); c['desc'] = n
    s = s.replace(' (with their lit edges, build 6)', '').replace('-litedge-slot820.svg', '-noflecks-slot820.svg')
    return s, c
def strip_b4(s, st): return s
print('=== A. every master against build 5, allowed differences only')
for kind, D, suf in (('notation', F, 'notation'), ('owl', O, 'owl'), ('layered', L, 'layered')):
    for st in STATES:
        p = f'{D}/MASTER-medallion-{st}-{suf}-slot820.svg'; q = f'{D}/superseded-build-5/MASTER-medallion-{st}-{suf}-slot820.svg'
        s = open(p, encoding='utf-8').read(); b = open(q, encoding='utf-8').read(); ns, c = normalise(s, st)
        check(f'{kind} {st} ({sha16(p)} vs build 5 {sha16(q)}): equal after the allowed differences', ns == b, f'{len(ns)} bytes')
        check(f'{kind} {st}: the allowed differences occur exactly as expected (3 lit layers, 1 desc sentence, 2 rails labels)', c == dict(lit=3, desc=1, rails=2), str(c))
        lit = block(s, 'finalA5-litedge'); levels = re.findall(r'<g fill-opacity="([\d.]+)">', lit)
        check(f'{kind} {st}: lit layer: 65 levels, clipped to the ink, highlight gold, strips only', len(levels) == 65 and 'clip-path="url(#finalA5-clip)"' in lit[:600] and 'fill="#F2E4B8"' in lit[:600] and lit.count('<path') == 65 and not re.search(r'filter|Gradient|stroke|<image', lit), f'{len(levels)} levels')
        root = ET.fromstring(s); kids = [cc.get('id') or cc.tag.split('}')[-1] for cc in root]
        fi = kids.index('field') if 'field' in kids else -1
        check(f'{kind} {st}: layer order field, rings, geometry, finish, LIT EDGE, then the legends and the mark', fi >= 0 and kids[fi:fi + 9] == ['field', 'finalA5-rings', 'finalA5-geometry', 'finalA5-finish', 'finalA5-litedge', 'legend-plaque-en', 'legend-text-en', 'legend-plaque-es', 'legend-text-es'], str(kids[fi:]))
print('\n=== B. the lit layer against Science\'s alpha reference (uncut ring, layer alone, 1298 px)')
import subprocess, tempfile, numpy as np
from PIL import Image
REFA = os.path.expanduser('~/Downloads/TETRASEMAPHORE-SCIENCE-lit-edge-alpha-reference-2460.png'); check('alpha reference on disk is c73e53800548c001', sha16(REFA) == 'c73e53800548c001', sha16(REFA))
ring = open('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-slot820.svg', encoding='utf-8').read()
lit = block(ring, 'finalA5-litedge'); clip = ring[ring.index('<clipPath id="finalA5-clip"'):ring.index('</clipPath>') + len('</clipPath>')]
geom = block(ring, 'finalA5-geometry'); geom = re.sub(r' filter="[^"]*"', '', geom)
tmp = tempfile.mkdtemp(prefix='lit6-')
open(f'{tmp}/layer.svg', 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="820" height="820" viewBox="0 0 820 820"><defs>{clip}</defs>{lit.replace("fill=#F2E4B8", "fill=#FFFFFF").replace(chr(34)+"#F2E4B8"+chr(34), chr(34)+"#FFFFFF"+chr(34))}</svg>')
open(f'{tmp}/geom.svg', 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="820" height="820" viewBox="0 0 820 820">{geom}</svg>')
subprocess.run(['node', 'tools/render.js', f'{tmp}/layer.svg', f'{tmp}/layer.png', '1298'], check=True, capture_output=True); subprocess.run(['node', 'tools/render.js', f'{tmp}/geom.svg', f'{tmp}/geom.png', '1298'], check=True, capture_output=True)
A = np.asarray(Image.open(f'{tmp}/layer.png').convert('RGBA'))[..., 3].astype(float) / 255; G = np.asarray(Image.open(f'{tmp}/geom.png').convert('RGBA'))[..., 3] > 127
R = np.asarray(Image.open(REFA).convert('L').resize((1298, 1298), Image.BOX)).astype(float) / 255; d = np.abs(A - R)[G]
check('lit layer vs reference at 1298 px: mean |da| <= 0.01 over the gold', d.mean() <= 0.01, f'{d.mean():.4f}')
check('lit layer vs reference at 1298 px: 99th percentile <= 0.15', np.percentile(d, 99) <= 0.15, f'{np.percentile(d, 99):.3f} (max {d.max():.3f})')
check('lit layer: nothing outside the ink', A[~G].max() < 0.02, f'{A[~G].max():.3f}')
print('\n=== C. the rings')
for name, keys in (('uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix', 'none'), ('seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2', '21-2'), ('seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1', '22-1')):
    a = open(f'finish/proposals/{name}-litedge-slot820.svg', encoding='utf-8').read(); b = open(f'finish/proposals/{name}-noflecks-slot820.svg', encoding='utf-8').read()
    na, c = normalise(a, None); check(f'ring {keys}: = the build-5 ring plus the lit layer and one desc sentence', na == b and c['lit'] == 1 and c['desc'] == 1, f'{sha16(f"finish/proposals/{name}-litedge-slot820.svg")} vs {sha16(f"finish/proposals/{name}-noflecks-slot820.svg")}; {c}')
tmp2 = tempfile.mkdtemp(prefix='rb6-'); subprocess.run(['node', 'tools/ring_build.js', '--out', f'{tmp2}/u.svg', '--legendKeys', 'none', '--seamFix', '1', '--knobs', 'finish/finish7-knobs-noflecks.txt'], check=True, capture_output=True)
check('ring_build.js without --litEdge still reproduces the build-5 uncut ring byte for byte', open(f'{tmp2}/u.svg', 'rb').read() == open('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-noflecks-slot820.svg', 'rb').read())
print('\n=== D. the builder\'s report')
r6 = json.load(open(f'{L}/layered-build.json', encoding='utf-8')); r5 = json.load(open(f'{L}/superseded-build-5/layered-build.json', encoding='utf-8'))
for s6, s5 in zip(r6['states'], r5['states']):
    for f6, f5 in zip(s6['legends'], s5['legends']):
        same = all(f6.get(k) == f5.get(k) for k in f5); check(f"report {s6['name']} {f6['lang']}: facts as in build 5", same)
    check(f"report {s6['name']}: owl-placement is root child 12", s6['owl_index'] == 12, str(s6['owl_index']))
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
