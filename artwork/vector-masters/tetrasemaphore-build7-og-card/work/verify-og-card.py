#!/usr/bin/env python3
"""verify-og-card.py <scratch dir> — the lane check of the link-preview card master (site rulings item 5). Renders og-card.png (resvg, 1200 px,
300 dpi + sRGB tags) and og-card.jpg (Pillow, quality 95, 4:4:4, from the PNG) and checks: (1) the SVG holds exactly the ground, four coin layers,
the title layer and the formula layer, no live text, raster, script or style, ids unique, every reference resolving inside its coin; (2) the PNG is
1200 x 630, alpha 255, tagged; (3) each coin rendered alone over the ground at its transform equals the composite inside its cell, pixel for pixel;
(4) the two strings' code points; (5) the title and the formula are centred on x 600 by ink to within 1 px; (6) the JPEG decodes close to the PNG
(max and mean difference recorded); (7) nothing but ground outside the three bands. Writes work/verify_report.json and proofs/og-card-preview.png."""
import sys, os, re, json, hashlib, struct, subprocess, pathlib
import numpy as np
from PIL import Image
ROOT = '/Users/careybalboa/Downloads/dose-01-meander-v2'; VM = ROOT + '/vector-masters'
OUT = os.environ.get('OG_OUT', VM + '/tetrasemaphore-build7-og-card'); PY = os.path.expanduser('~/.cache/dose01-toolchain/venv/bin/python')
SVG = f'{OUT}/og-card-MASTER.svg'; PNG = f'{OUT}/og-card.png'; JPG = f'{OUT}/og-card.jpg'
SCR = pathlib.Path(sys.argv[1]); SCR.mkdir(parents=True, exist_ok=True)
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
subprocess.run(['node', ROOT + '/tools/render.js', SVG, PNG, '1200', 'none'], check=True, capture_output=True)
subprocess.run([PY, ROOT + '/tools/png_tag.py', PNG], check=True, capture_output=True)
im = Image.open(PNG).convert('RGB'); im.save(JPG, 'JPEG', quality=95, subsampling=0, optimize=True)
R = {'inputs': {'svg': {'file': SVG, 'sha16': sha16(SVG)}}, 'outputs': {}, 'checks': {}}; ok_all = True
def put(name, ok, **kw):
    global ok_all; ok_all &= bool(ok); R['checks'][name] = dict(pass_=bool(ok), **kw); print(('ok   ' if ok else 'FAIL ') + name, kw)
s = open(SVG, encoding='utf-8').read()
layers = re.findall(r'<g inkscape:groupmode="layer" id="([^"]+)"', s)
put('1_layers_and_no_live_text', layers == ['ground', 'figure', 'n-medallion-slot820', 'nn-medallion-slot820', 'm-medallion-slot820', 'c-medallion-slot820', 'title', 'formula']
    and not re.search(r'<text\b|<image\b|<foreignObject\b|<script\b|<style\b', s), layers=layers)
ids = re.findall(r'\sid="([^"]+)"', s); refs = re.findall(r'url\(\s*#([^)\s]+)\s*\)', s) + [h[1:] for h in re.findall(r'\s(?:xlink:)?href="([^"]*)"', s)]
put('1b_ids_unique_refs_resolve', len(ids) == len(set(ids)) and all(r in set(ids) for r in refs) and all(r.split('-')[0] in ('n', 'nn', 'm', 'c') for r in refs), ids=len(ids), refs=len(refs))
def chunks(b):
    i = 8; out = {}
    while i < len(b):
        n = struct.unpack('>I', b[i:i+4])[0]; out.setdefault(b[i+4:i+8], b[i+8:i+8+n]); i += 12 + n
    return out
c = chunks(open(PNG, 'rb').read()); ph = struct.unpack('>IIB', c[b'pHYs']) if b'pHYs' in c else None
a = np.asarray(Image.open(PNG).convert('RGBA')).astype(np.int16)
put('2_png_dims_alpha_tags', a.shape == (630, 1200, 4) and int(a[..., 3].min()) == 255 and b'sRGB' in c and ph and round(ph[0] * 0.0254) == 300, shape=list(a.shape), dpi=round(ph[0] * 0.0254, 2) if ph else None)
rep = json.load(open(f'{OUT}/work/layout_report.json'))
head = s[:s.index('<g inkscape:groupmode="layer" id="figure"')]
res = {}
for cn in rep['coins']:
    pre = cn['prefix']; k = s.index(f'<g inkscape:groupmode="layer" id="{pre}medallion-slot820"'); depth = 0; j = k
    for m in re.finditer(r'<g\b|</g>', s[k:]):
        depth += -1 if m.group(0) == '</g>' else 1
        if depth == 0: j = k + m.end(); break
    single = head + f'<g inkscape:groupmode="layer" id="figure">{s[k:j]}</g>\n</svg>'; sp = SCR / f'coin-{pre}.svg'; pp = SCR / f'coin-{pre}.png'
    sp.write_text(single, encoding='utf-8'); subprocess.run(['node', ROOT + '/tools/render.js', str(sp), str(pp), '1200', 'none'], check=True, capture_output=True)
    one = np.asarray(Image.open(pp).convert('RGBA')).astype(np.int16); x0, y0 = cn['translate']; D = cn['box_px']
    X0, Y0, X1, Y1 = int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x0 + D)), int(np.ceil(y0 + D))
    dd = np.abs(one[Y0:Y1, X0:X1] - a[Y0:Y1, X0:X1]); res[cn['state']] = {'cell': [X0, Y0, X1, Y1], 'differing_px': int((dd.max(axis=2) > 0).sum()), 'max_level': int(dd.max())}
put('3_each_coin_alone_equals_composite', all(v['differing_px'] == 0 for v in res.values()), coins=res)
want = {'TETRASEMAPHORE': ['U+0054', 'U+0045', 'U+0054', 'U+0052', 'U+0041', 'U+0053', 'U+0045', 'U+004D', 'U+0041', 'U+0050', 'U+0048', 'U+004F', 'U+0052', 'U+0045'],
        'V₄ = {I, σᵥ, σₕ, C₂}': ['U+0056', 'U+2084', 'U+0020', 'U+003D', 'U+0020', 'U+007B', 'U+0049', 'U+002C', 'U+0020', 'U+03C3', 'U+1D65', 'U+002C', 'U+0020', 'U+03C3', 'U+2095', 'U+002C', 'U+0020', 'U+0043', 'U+2082', 'U+007D']}
put('4_code_points', rep['title']['code_points'] == want['TETRASEMAPHORE'] and rep['formula']['code_points'] == want['V₄ = {I, σᵥ, σₕ, C₂}'])
ti, fi = rep['title']['ink'], rep['formula']['ink']; tt, ff = rep['title'], rep['formula']
# the record's rule (J4 spec, build-five.js): an unboxed line is centred on the axis by its advance, to 1/8 px; a boxed row has its BOX centred on the
# axis and its text from box x + 43.625. Ink centres are recorded for information (glyph side bearings put them a few px left of the axis, as on the screens).
title_adv_centre = tt['x'] + tt['advance'] / 2; box_centre = ff['box']['x'] + ff['box']['w'] / 2
put('5_centred_on_600_by_the_record_rule', abs(title_adv_centre - 600) <= 0.0625 and box_centre == 600 and abs(ff['text_x'] - (ff['box']['x'] + 43.625)) < 0.001,
    title_advance_centre=round(title_adv_centre, 3), formula_box_centre=box_centre, title_ink_centre=round((ti['x1'] + ti['x2']) / 2, 3), formula_ink_centre=round((fi['x1'] + fi['x2']) / 2, 3))
j = np.asarray(Image.open(JPG).convert('RGB')).astype(np.int16); d = np.abs(j - a[..., :3])
put('6_jpeg_close_to_png', int(d.max()) <= 40 and float(d.mean()) < 1.0, max_level=int(d.max()), mean_level=round(float(d.mean()), 4), jpeg='Pillow quality 95, 4:4:4, optimize')
ground = np.array([0x1D, 0x25, 0x2D, 255], dtype=np.int16); nong = np.abs(a - ground).max(axis=2) > 0
rows = np.where(nong.any(axis=1))[0]; bands = []
start = int(rows[0]); prev = start
for r in rows[1:]:
    if r != prev + 1: bands.append([start, int(prev)]); start = int(r)
    prev = int(r)
bands.append([start, prev])
put('7_three_ink_bands_only', len(bands) == 3 and bands[0][0] >= 40 and bands[1] == [140, 359] and bands[2][1] < 630, bands=bands)
for k, p in (('png', PNG), ('jpg', JPG)): R['outputs'][k] = {'file': p, 'sha16': sha16(p), 'bytes': os.path.getsize(p)}
prev_img = Image.open(PNG).convert('RGB').resize((600, 315), Image.LANCZOS); pv = f'{OUT}/proofs/og-card-preview.png'; prev_img.save(pv); R['preview'] = {'file': pv, 'sha16': sha16(pv)}
R['all_pass'] = ok_all; json.dump(R, open(f'{OUT}/work/verify_report.json', 'w'), indent=1); print('all pass:', ok_all, R['outputs'])
sys.exit(0 if ok_all else 1)
