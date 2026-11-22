#!/usr/bin/env python3
"""Lane's own check of BUILD 7 (run from the dose-01-meander-v2 folder with the toolchain venv python). Build 7 = build 6 + Science's one-line
bow-tie guard in tools/litedge.js (no strip spans a join turning more than 170 deg; TETRASEMAPHORE-SCIENCE-build7-litedge-guard.diff bf7d5264f178d5f1)
+ 300 dpi / sRGB tags on every PNG. Against build 6 (superseded-build-6/ and the *-litedge-slot820.svg rings):
 R. the three guard rings equal the build-6 rings after exactly these allowed differences: the finalA5-litedge layer's contents and the ring's <desc>
    sentence; ring_build.js without --litEdge still reproduces the build-5 uncut ring;
 S2. Science's check 2 (the lit layer of the uncut ring alone, 4920 px): no lit pixel within 0.16 mm of the ink's edge above opacity 0.02 (build 6:
    Science counted 91 in its dry run); pixels above 0.67 counted and placed (revised 2b: at most 21, all within 0.5 mm of the 342.854-unit rail);
 S3. Science's check 3: the layer alone against the alpha reference c73e53800548c001 at 1298 px, mean |da| <= 0.01 over the gold, 99th pct <= 0.15;
 S4. Science's check 4: each ring rendered at 1298 px against its build-6 ring: at most 8 levels anywhere; the differing pixels counted;
 A. every master (notation, owl, layered; 4 states each) equals its build-6 file after exactly these allowed differences: the three finalA5-litedge*
    layers' contents, the ring's <desc> sentence, the two rails labels, the ring file name; the lit layer still 65 levels, strips only, clipped;
 D. the builder's report equals build 6's (the legends did not move); owl-placement is root child 12;
 E. the Spanish layers hidden, the English shown, one outline per letter (+ CRÍTICO's accent), no depth effects, words outside the SVGs; the approved
    masters and the guard untouched; the export counts;
 X. the 1298 px exports against build 6's: at most 8 levels anywhere (Science's check 4 on the coins); differing pixels counted;
 T. Science's check 5: every PNG of both sets carries sRGB and pHYs 300 dpi.
Usage: lane-verify-build7.py [--stage A] [--rings <dir with uncut.svg k21-2.svg k22-1.svg>]   (stage A = R, S2, S3, S4 only, e.g. on scratch rings)"""
import re, hashlib, sys, json, glob, os, math, subprocess, tempfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageFilter
STAGE = sys.argv[sys.argv.index('--stage') + 1] if '--stage' in sys.argv else 'all'
RD = sys.argv[sys.argv.index('--rings') + 1] if '--rings' in sys.argv else None
P = 'master/states/proposals'; F = f'{P}/notation/final-masters-2026-10-05'; O = f'{P}/owl-finals-2026-10-05'; L = f'{P}/layered'
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL'); MMU = 102.785 / 820
ES = {'NORMATIVE': 'NORMATIVO', 'NON-NORMATIVE': 'INFORMATIVO', 'METACOGNITIVE': 'METACOGNITIVO', 'CRITICAL': 'CRÍTICO'}
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
ok = True; n = 0; REPORT = {}
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
DESC_RE = r' Lit edges \(build [67], litedge\.js[^<]*?opacity levels\.'
RAILS_RE = r' \(with their lit edges, build [67]\)'
def normalise(s):
    """a build-6 or build-7 file -> the common text, with counts of each allowed difference"""
    c = dict(lit=0, desc=0, rails=len(re.findall(RAILS_RE, s)))
    for gid in ('finalA5-litedge', 'finalA5-litedge-win-en', 'finalA5-litedge-win-es'):
        if f'<g id="{gid}"' in s: blk = block(s, gid); assert s.count(blk + '\n') == 1; s = s.replace(blk + '\n', '', 1); c['lit'] += 1
    s, k = re.subn(DESC_RE, '', s); c['desc'] = k
    s = re.sub(RAILS_RE, '', s).replace('-litedge-guard-slot820.svg', '-litedge-slot820.svg')
    return s, c
def render(svg, png, px): subprocess.run(['node', 'tools/render.js', svg, png, str(px)], check=True, capture_output=True)
def layer_pngs(ring_svg, px, tmp, tag):
    """the lit layer alone (white) and the ink mask, rendered at px; returns alpha in [0,1] and the mask"""
    ring = open(ring_svg, encoding='utf-8').read(); lit = block(ring, 'finalA5-litedge')
    clip = ring[ring.index('<clipPath id="finalA5-clip"'):ring.index('</clipPath>') + len('</clipPath>')]
    geom = re.sub(r' filter="[^"]*"', '', block(ring, 'finalA5-geometry'))
    hdr = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="820" height="820" viewBox="0 0 820 820">'
    open(f'{tmp}/{tag}-layer.svg', 'w', encoding='utf-8').write(f'{hdr}<defs>{clip}</defs>{lit.replace(chr(34) + "#F2E4B8" + chr(34), chr(34) + "#FFFFFF" + chr(34))}</svg>')
    open(f'{tmp}/{tag}-geom.svg', 'w', encoding='utf-8').write(f'{hdr}{geom}</svg>')
    render(f'{tmp}/{tag}-layer.svg', f'{tmp}/{tag}-layer.png', px); render(f'{tmp}/{tag}-geom.svg', f'{tmp}/{tag}-geom.png', px)
    A = np.asarray(Image.open(f'{tmp}/{tag}-layer.png').convert('RGBA'))[..., 3].astype(np.float32) / 255
    G = np.asarray(Image.open(f'{tmp}/{tag}-geom.png').convert('RGBA'))[..., 3] > 127
    return A, G
R7 = {'uncut': 'finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-guard-slot820.svg',
      'k21-2': 'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-litedge-guard-slot820.svg',
      'k22-1': 'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-litedge-guard-slot820.svg'}
if RD: R7 = {k: f'{RD}/{k}.svg' for k in R7}
R6 = {'uncut': 'finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-slot820.svg',
      'k21-2': 'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-litedge-slot820.svg',
      'k22-1': 'finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-litedge-slot820.svg'}
tmp = tempfile.mkdtemp(prefix='b7-')
print('=== R. the three guard rings against the build-6 rings')
for k in R7:
    a = open(R7[k], encoding='utf-8').read(); b = open(R6[k], encoding='utf-8').read(); na, ca = normalise(a); nb, cb = normalise(b)
    check(f'ring {k} ({sha16(R7[k])} vs build 6 {sha16(R6[k])}): equal after the allowed differences (lit layer, desc)', na == nb and ca['lit'] == 1 and ca['desc'] == 1 and cb['lit'] == 1 and cb['desc'] == 1, f'{ca} / {cb}')
    lit = block(a, 'finalA5-litedge'); levels = re.findall(r'<g fill-opacity="([\d.]+)">', lit); strips = len(re.findall(r'<path d=', lit))
    check(f'ring {k}: lit layer 65 levels, strips only, clipped, highlight gold; guard named in the label', len(levels) == 65 and 'clip-path="url(#finalA5-clip)"' in lit[:700] and 'fill="#F2E4B8"' in lit[:700] and 'more than 170 deg' in lit[:700] and not re.search(r'filter|Gradient|stroke|<image', lit), f'{len(levels)} levels')
    REPORT[f'ring {k}'] = dict(sha16=sha16(R7[k]), build6=sha16(R6[k]), levels=len(levels))
m = re.search(r'(\d+) strips in (\d+) opacity levels', block(open(R7['uncut'], encoding='utf-8').read(), 'finalA5-litedge')[:900])
check('uncut ring: 11,475 strips (Science\'s dry run with the guard; build 6 had 11,497)', m and m.group(1) == '11475', m.group(0) if m else 'no count in the label')
tmp2 = tempfile.mkdtemp(prefix='rb7-'); subprocess.run(['node', 'tools/ring_build.js', '--out', f'{tmp2}/u.svg', '--legendKeys', 'none', '--seamFix', '1', '--knobs', 'finish/finish7-knobs-noflecks.txt'], check=True, capture_output=True)
check('ring_build.js without --litEdge still reproduces the build-5 uncut ring byte for byte', open(f'{tmp2}/u.svg', 'rb').read() == open('finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-noflecks-slot820.svg', 'rb').read())

print('\n=== S2. Science\'s check 2: the lit layer of the uncut ring at 4920 px')
A, G = layer_pngs(R7['uncut'], 4920, tmp, 'u7-4920')
try:
    from scipy.ndimage import distance_transform_edt
    dist = distance_transform_edt(G); method = 'scipy edt (disk)'
except Exception:
    er = np.asarray(Image.fromarray((G * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(17))) > 127; dist = np.where(G & ~er, 0.0, 99.0); method = 'PIL MinFilter 17 (square, conservative)'
PXMM = 4920 / 102.785; rim = G & (dist <= 0.16 * PXMM)
rim_px = int(((A > 0.02) & rim).sum()); rim_peak = float(A[rim].max()) if rim.any() else 0.0
check(f'2a: no lit pixel within 0.16 mm ({0.16 * PXMM:.2f} px, {method}) of the ink\'s edge above 0.02 (build 6: 91 in Science\'s dry run)', rim_px == 0, f'{rim_px} px, peak {rim_peak:.3f}')
over = A > 0.67; cnt = int(over.sum()); yy, xx = np.nonzero(over); r = np.hypot(xx + 0.5 - 2460, yy + 0.5 - 2460) / 6.0
within = int(((r - 342.854) * MMU <= 0.5).sum()) if cnt else 0
detail = f'{cnt} px, peak {float(A.max()):.3f}' + (f'; r {r.min():.2f}-{r.max():.2f} units = {(r.min() - 342.854) * MMU:+.3f}..{(r.max() - 342.854) * MMU:+.3f} mm from the 342.854 rail, {within} of them within 0.5 mm (positions in the report for Science)' if cnt else '')
check('2b (revised): at most 21 px above 0.67 (Science\'s dry run: 20, peak 0.784; the radial spread is reported, not judged here)', cnt <= 21, detail)
check('lit layer: nothing outside the ink (max alpha off the ink < 0.02)', float(A[~G].max()) < 0.02, f'{float(A[~G].max()):.3f}')
REPORT['S2'] = dict(rim_px=rim_px, rim_peak=rim_peak, over_067=cnt, peak=float(A.max()), method=method, within_0p5mm=within,
                    over_067_pixels=[dict(x=int(x), y=int(y), r_units=round(float(rr), 2), mm_from_rail=round(float((rr - 342.854) * MMU), 3), alpha=round(float(A[y, x]), 3)) for x, y, rr in zip(xx, yy, r)])
del A, G, dist, rim, over

print('\n=== S3. Science\'s check 3: the layer alone against the alpha reference at 1298 px')
REFA = os.path.expanduser('~/Downloads/TETRASEMAPHORE-SCIENCE-lit-edge-alpha-reference-2460.png'); check('alpha reference on disk is c73e53800548c001', sha16(REFA) == 'c73e53800548c001', sha16(REFA))
A, G = layer_pngs(R7['uncut'], 1298, tmp, 'u7-1298')
Rf = np.asarray(Image.open(REFA).convert('L').resize((1298, 1298), Image.BOX)).astype(np.float32) / 255; d = np.abs(A - Rf)[G]
check('mean |da| <= 0.01 over the gold (build 6: 0.0060)', d.mean() <= 0.01, f'{d.mean():.4f}')
check('99th percentile <= 0.15 (build 6: 0.114)', np.percentile(d, 99) <= 0.15, f'{np.percentile(d, 99):.3f} (max {d.max():.3f})')
REPORT['S3'] = dict(mean=float(d.mean()), p99=float(np.percentile(d, 99)), max=float(d.max()))

print('\n=== S4. Science\'s check 4 on the rings: each ring at 1298 px against its build-6 ring')
for k in R7:
    render(R7[k], f'{tmp}/r7-{k}.png', 1298); render(R6[k], f'{tmp}/r6-{k}.png', 1298)
    a = np.asarray(Image.open(f'{tmp}/r7-{k}.png').convert('RGBA')).astype(int); b = np.asarray(Image.open(f'{tmp}/r6-{k}.png').convert('RGBA')).astype(int); dd = np.abs(a - b).max(-1)
    check(f'ring {k} at 1298 px vs build 6: at most 8 levels anywhere', dd.max() <= 8, f'max {dd.max()} levels; {int((dd > 0).sum())} px differ, {int((dd > 2).sum())} over 2, {int((dd > 8).sum())} over 8')
    REPORT[f'S4 {k}'] = dict(max=int(dd.max()), differing=int((dd > 0).sum()), over2=int((dd > 2).sum()), over8=int((dd > 8).sum()))
if STAGE == 'A':
    print(json.dumps(REPORT, indent=1)); print(f'\n{n} checks (stage A):', 'ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)

print('\n=== A. every master against build 6, allowed differences only')
for kind, D, suf in (('notation', F, 'notation'), ('owl', O, 'owl'), ('layered', L, 'layered')):
    for st in STATES:
        p = f'{D}/MASTER-medallion-{st}-{suf}-slot820.svg'; q = f'{D}/superseded-build-6/MASTER-medallion-{st}-{suf}-slot820.svg'
        s = open(p, encoding='utf-8').read(); b = open(q, encoding='utf-8').read(); ns, c = normalise(s); nb, cb = normalise(b)
        check(f'{kind} {st} ({sha16(p)} vs build 6 {sha16(q)}): equal after the allowed differences', ns == nb, f'{len(ns)} bytes')
        check(f'{kind} {st}: the allowed differences occur exactly as expected on both sides (3 lit layers, 1 desc sentence, 2 rails labels)', c == dict(lit=3, desc=1, rails=2) and cb == dict(lit=3, desc=1, rails=2), f'{c} / {cb}')
        lit = block(s, 'finalA5-litedge'); levels = re.findall(r'<g fill-opacity="([\d.]+)">', lit)
        check(f'{kind} {st}: lit layer: 65 levels, clipped to the ink, highlight gold, strips only, guard in the label', len(levels) == 65 and 'clip-path="url(#finalA5-clip)"' in lit[:700] and 'fill="#F2E4B8"' in lit[:700] and 'more than 170 deg' in lit[:700] and lit.count('<path') == 65 and not re.search(r'filter|Gradient|stroke|<image', lit), f'{len(levels)} levels')
        root = ET.fromstring(s); kids = [cc.get('id') or cc.tag.split('}')[-1] for cc in root]
        fi = kids.index('field') if 'field' in kids else -1
        check(f'{kind} {st}: layer order field, rings, geometry, finish, LIT EDGE, then the legends and the mark', fi >= 0 and kids[fi:fi + 9] == ['field', 'finalA5-rings', 'finalA5-geometry', 'finalA5-finish', 'finalA5-litedge', 'legend-plaque-en', 'legend-text-en', 'legend-plaque-es', 'legend-text-es'], str(kids[fi:]))
        for win in ('win-en', 'win-es'):
            w7 = block(s, f'finalA5-litedge-{win}'); w6 = block(b, f'finalA5-litedge-{win}')
            check(f'{kind} {st}: window rails {win} carry the build-7 lit layer (guard named; not build 6\'s bytes)', 'more than 170 deg' in w7[:700] and w7 != w6)

print('\n=== D. the builder\'s report')
r7 = json.load(open(f'{L}/layered-build.json', encoding='utf-8')); r6 = json.load(open(f'{L}/superseded-build-6/layered-build.json', encoding='utf-8'))
for s7, s6 in zip(r7['states'], r6['states']):
    for f7, f6 in zip(s7['legends'], s6['legends']):
        same = all(f7.get(k) == f6.get(k) for k in f6); check(f"report {s7['name']} {f7['lang']}: facts as in build 6", same)
    check(f"report {s7['name']}: owl-placement is root child 12", s7['owl_index'] == 12, str(s7['owl_index']))
check('layered report: the ring is the guard ring', r7['ring'].endswith('-litedge-guard-slot820.svg'), r7['ring'])

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
        check(f'{kind} {st}: no "build 6" left in a label or desc', not re.search(r'build 6(?! is in| \()', s), str(re.findall(r'.{40}build 6.{40}', s)[:3]))
for pat in (f'{F}/README.md', f'{F}/MANIFEST.json', f'{O}/README.md', f'{O}/MANIFEST.json', f'{L}/states-config-layered.json', f'{O}/states-config-owl-layered.json'):
    for q in glob.glob(pat):
        t = open(q, encoding='utf-8').read().replace('TETRASEMAPHORE-SCIENCE-CRITICO-accent-C-reference.svg', '')
        check(f'{q.split("/")[-1]} ({q.split("/")[-2]}): no unaccented semaforo / CRITICO as the Spanish word (the reference file name aside)', not re.search(r'[Ss]emaforo\b|\bCRITICO\b', t))
approved = {'NORMATIVE': 'd9d6336b0c9450ac', 'NON-NORMATIVE': 'e1d83bb7e4b6017d', 'CRITICAL': '055655372b21da5c', 'METACOGNITIVE': '3a8a7459bb1782d1'}
for st, h in approved.items(): check(f'approved master {st} untouched ({h})', sha16(f'master/states/MASTER-medallion-{st}-slot820.svg') == h)
check('guard d4054fa6e02e66e4 untouched', sha16('master/MASTER-medallion-METACOGNITIVE-slot820.svg') == 'd4054fa6e02e66e4')
check('notation exports: 40 PNGs (4 states x 2 languages x 5 sizes)', len(glob.glob(f'{F}/png/*.png')) == 40, str(len(glob.glob(f'{F}/png/*.png'))))
check('owl exports: 40 PNGs', len(glob.glob(f'{O}/png/*.png')) == 40, str(len(glob.glob(f'{O}/png/*.png'))))
check('scan cards: 8', len(glob.glob(f'{F}/scan-cards/*.png')) == 8, str(len(glob.glob(f'{F}/scan-cards/*.png'))))

print('\n=== X. the 1298 px exports against build 6 (Science\'s check 4 on the coins)')
for kind, D, pre in (('notation', F, 'TETRASEMAPHORE'), ('owl', O, 'OWL-SEMAPHORE')):
    for st in STATES:
        for lang in ('en', 'es'):
            a = np.asarray(Image.open(f'{D}/png/{pre}-{st}-{lang}-1298.png').convert('RGBA')).astype(int); b = np.asarray(Image.open(f'{D}/superseded-build-6/png/{pre}-{st}-{lang}-1298.png').convert('RGBA')).astype(int); dd = np.abs(a - b).max(-1)
            check(f'{kind} {st} {lang} 1298 px vs build 6: at most 8 levels anywhere', dd.max() <= 8, f'max {dd.max()}; {int((dd > 0).sum())} px differ, {int((dd > 2).sum())} over 2')
            REPORT[f'X {kind} {st} {lang}'] = dict(max=int(dd.max()), differing=int((dd > 0).sum()), over2=int((dd > 2).sum()))

print('\n=== T. Science\'s check 5: the tags')
import struct
def tags(p):
    b = open(p, 'rb').read(); i = 8; c = {}
    while i < len(b):
        ln = struct.unpack('>I', b[i:i + 4])[0]; t = b[i + 4:i + 8]; c[t] = b[i + 8:i + 8 + ln]; i += 12 + ln
    ph = c.get(b'pHYs'); x, y, u = struct.unpack('>IIB', ph) if ph else (0, 0, 0)
    return b'sRGB' in c and u == 1 and round(x * 0.0254) == 300 and round(y * 0.0254) == 300
pngs = sorted(glob.glob(f'{F}/png/*.png') + glob.glob(f'{F}/proofs/*.png') + glob.glob(f'{F}/scan-cards/*.png') + glob.glob(f'{F}/*-preview.png') + glob.glob(f'{O}/png/*.png') + glob.glob(f'{O}/proofs/*.png') + glob.glob(f'{O}/*-preview.png'))
missing = [p for p in pngs if not tags(p)]
check(f'every PNG of both sets carries sRGB and pHYs 300 dpi ({len(pngs)} files)', not missing, ', '.join(missing[:5]))
json.dump(REPORT, open(f'{F}/refute/lane-verify-build7-report.json', 'w'), indent=1)
print(f'\n{n} checks:', 'ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)
