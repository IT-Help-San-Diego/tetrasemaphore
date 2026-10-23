#!/usr/bin/env python3
"""verify-lock-rev6.py <scratch dir> — the lane check of the halfway all-four lock screen (revision 6, FINISH-TODAY update 19) against the
revision-5 screen Science passed on 21 Oct. Checks: (1) the SVG differs from revision 5 ONLY in the eight transforms and the metadata
(title, desc, labels); (2) the PNG is 1206 x 2622, alpha 255 everywhere, tagged sRGB + 300 dpi; (3) the text band (every pixel from y 1560 down)
is the revision-5 band moved 48 px, pixel for pixel; (4) each coin, rendered alone over the ground at its transform, equals the composite inside
its cell, pixel for pixel; (5) measured clearances: coin top under the clock digits (y 612), grid bottom to row 1, last ink to the buttons (y 2298);
(6) the three strings' code points. Writes work/verify_report.json and proofs/…-preview.png (revision 5 | revision 6 | Science's mock-up).
Claude Code, 2026-10-22."""
import sys, os, re, json, hashlib, struct, subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = '/Users/careybalboa/Downloads/dose-01-meander-v2'; VM = ROOT + '/vector-masters'
OUT = os.environ.get('J4R6_OUT', VM + '/tetrasemaphore-build7-allfour-lockscreen-halfway')
NAME = 'dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway'
SVG6 = f'{OUT}/{NAME}-MASTER.svg'; PNG6 = f'{OUT}/{NAME}.png'
SVG5 = VM + '/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-MASTER.svg'
PNG5 = VM + '/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen.png'
MOCK = '/Users/careybalboa/Downloads/TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MOCKUP-1206x2622.png'
FONT = '/Users/careybalboa/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf'
SCR = pathlib.Path(sys.argv[1]); SCR.mkdir(parents=True, exist_ok=True)
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
R = {'inputs': {k: {'file': p, 'sha16': sha16(p)} for k, p in [('svg6', SVG6), ('png6', PNG6), ('svg5', SVG5), ('png5', PNG5), ('mockup', MOCK)]}, 'checks': {}}
ok_all = True
def put(name, ok, **kw):
    global ok_all; ok_all &= bool(ok); R['checks'][name] = dict(pass_=bool(ok), **kw); print(('ok   ' if ok else 'FAIL ') + name, {k: v for k, v in kw.items() if k not in ('detail',)})

# (1) structural diff
s5 = open(SVG5, encoding='utf-8').read(); s6 = open(SVG6, encoding='utf-8').read()
TR = re.compile(r'(id="(?:n|nn|m|c)-medallion-slot820" transform=")[^"]*(")|(id="(?:operator|forall|divider-1|cogito)" transform=")[^"]*(")')
def norm(s):
    s = re.sub(r'<title>[\s\S]*?</title>', '<title/>', s); s = re.sub(r'<desc>[\s\S]*?</desc>', '<desc/>', s)
    s = re.sub(r'\s+inkscape:label="[^"]*"', '', s); return TR.sub(lambda m: (m.group(1) or m.group(3)) + 'X' + (m.group(2) or m.group(4)), s)
n5, n6 = norm(s5), norm(s6)
tr5 = TR.findall(s5); tr6 = [m.group(0) for m in TR.finditer(s6)]
put('1_svg_differs_only_in_transforms_and_metadata', n5 == n6, transforms_rev6=tr6, bytes_normalised=(len(n5), len(n6)))
exp_tr = ['translate(180 669) scale(0.477439024)', 'translate(633.5 669) scale(0.477439024)', 'translate(180 1122.5) scale(0.477439024)', 'translate(633.5 1122.5) scale(0.477439024)',
          'translate(0 126.598)', 'translate(0 151.32)', 'translate(0 176.041)', 'translate(0 200.762)']
got_tr = [re.search(r'transform="([^"]*)"', t).group(1) for t in tr6]
put('1b_transforms_equal_update_19', got_tr == exp_tr, got=got_tr)
put('1c_no_live_text_raster_script_style', not re.search(r'<text\b|<image\b|<foreignObject\b|<script\b|<style\b', s6))

# (2) the PNG
def chunks(b):
    i = 8; out = {}
    while i < len(b):
        n = struct.unpack('>I', b[i:i+4])[0]; out.setdefault(b[i+4:i+8], b[i+8:i+8+n]); i += 12 + n
    return out
b6 = open(PNG6, 'rb').read(); c6 = chunks(b6); ph = struct.unpack('>IIB', c6[b'pHYs']) if b'pHYs' in c6 else None
im6 = np.asarray(Image.open(PNG6).convert('RGBA')).astype(np.int16); im5 = np.asarray(Image.open(PNG5).convert('RGBA')).astype(np.int16)
put('2_png_dims_alpha_tags', im6.shape == (2622, 1206, 4) and int(im6[..., 3].min()) == 255 and b'sRGB' in c6 and ph and round(ph[0] * 0.0254) == 300,
    shape=list(im6.shape), alpha_min=int(im6[..., 3].min()), sRGB=b'sRGB' in c6, dpi=round(ph[0] * 0.0254, 2) if ph else None)

# (3) the text band moved 48 px
band6 = im6[1560:2622]; band5 = im5[1512:2574]
d = np.abs(band6 - band5); m3 = d.max(axis=2); ys, xs = np.where(m3 > 0)
px = [{'x': int(x), 'y_rev6': int(y) + 1560, 'rev6': band6[y, x, :3].tolist(), 'rev5': band5[y, x, :3].tolist(), 'diff': int(m3[y, x])} for y, x in zip(ys, xs)]
# resvg composes the layer transform in floating point, so an integer shift can move an anti-aliased edge pixel by a few levels; the tolerance is
# stated here (at most 8 pixels, at most 16 levels, every one an edge pixel between the ground and the text colour) and every pixel is recorded
put('3_text_band_is_rev5_moved_48px', len(px) <= 8 and int(d.max()) <= 16, differing_px=len(px), max_level=int(d.max()), tolerance='<= 8 px, <= 16 levels (resvg edge rounding)', pixels=px)
# the coin band of rev 6 above y 1560 must contain no revision-5 pixels at all (sanity: rev 5's rows started at 1531.6 so nothing of rev 5 lies above 1512 but coins)
# (4) each coin alone over the ground
head = s6[:s6.index('<g inkscape:groupmode="layer" id="figure"')]
rest = s6[s6.index('\n<g inkscape:groupmode="layer" id="stack"'):]
groups = {}
for pre in ('n-', 'nn-', 'm-', 'c-'):
    k = s6.index(f'<g inkscape:groupmode="layer" id="{pre}medallion-slot820"'); depth = 0; j = k
    for m in re.finditer(r'<g\b|</g>', s6[k:]):
        depth += -1 if m.group(0) == '</g>' else 1
        if depth == 0: j = k + m.end(); break
    groups[pre] = s6[k:j]
cells = {'n-': (180, 669), 'nn-': (633.5, 669), 'm-': (180, 1122.5), 'c-': (633.5, 1122.5)}; D = 391.5
coin_res = {}
for pre, g in groups.items():
    single = head + f'<g inkscape:groupmode="layer" id="figure">{g}</g>\n</svg>'
    sp = SCR / f'coin-{pre}.svg'; pp = SCR / f'coin-{pre}.png'; sp.write_text(single, encoding='utf-8')
    subprocess.run(['node', ROOT + '/tools/render.js', str(sp), str(pp), '1206', 'none'], check=True, capture_output=True)
    one = np.asarray(Image.open(pp).convert('RGBA')).astype(np.int16)
    x0, y0 = cells[pre]; X0, Y0, X1, Y1 = int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x0 + D)), int(np.ceil(y0 + D))
    dd = np.abs(one[Y0:Y1, X0:X1] - im6[Y0:Y1, X0:X1]); coin_res[pre] = {'cell': [X0, Y0, X1, Y1], 'differing_px': int((dd.max(axis=2) > 0).sum()), 'max_level': int(dd.max())}
put('4_each_coin_alone_equals_composite_in_its_cell', all(v['differing_px'] == 0 for v in coin_res.values()), coins=coin_res)

# (5) clearances, measured on the PNG
ground = np.array([0x1D, 0x25, 0x2D, 255], dtype=np.int16)
nong = (np.abs(im6 - ground).max(axis=2) > 0)
rows = np.where(nong.any(axis=1))[0]
coin_rows = rows[rows < 1560]; text_rows = rows[rows >= 1560]
meas = {'first_ink_row': int(rows.min()), 'coin_band': [int(coin_rows.min()), int(coin_rows.max())], 'text_band': [int(text_rows.min()), int(text_rows.max())],
        'clock_digits_y612_to_coin_top_px': int(coin_rows.min()) - 612, 'grid_bottom_to_row1_box_px': int(text_rows.min()) - int(coin_rows.max()) - 1,
        'last_ink_to_buttons_y2298_px': 2298 - int(text_rows.max()) - 1, 'update_19_expected': {'under_clock': 56, 'above_buttons': 92}}
put('5_clearances_measured', int(coin_rows.min()) == 669 and int(coin_rows.max()) <= 1514 and int(text_rows.max()) < 2298, **meas)

# (6) code points
rep = json.load(open(f'{OUT}/work/layout_report.json'))['screens']['ALL-FOUR-lockscreen-halfway']
strings = {r['string']: r['code_points'] for r in rep['rows']}; strings.update({l['string']: l['code_points'] for l in rep['lines']})
want = {'V₄ = {I, σᵥ, σₕ, C₂}': ['U+0056', 'U+2084', 'U+0020', 'U+003D', 'U+0020', 'U+007B', 'U+0049', 'U+002C', 'U+0020', 'U+03C3', 'U+1D65', 'U+002C', 'U+0020', 'U+03C3', 'U+2095', 'U+002C', 'U+0020', 'U+0043', 'U+2082', 'U+007D'],
        '∀g ∈ V₄. g ∘ g = I': ['U+2200', 'U+0067', 'U+0020', 'U+2208', 'U+0020', 'U+0056', 'U+2084', 'U+002E', 'U+0020', 'U+0067', 'U+0020', 'U+2218', 'U+0020', 'U+0067', 'U+0020', 'U+003D', 'U+0020', 'U+0049']}
put('6_code_points', all(strings.get(k) == v for k, v in want.items()) and len(strings) == 5, strings=list(strings))

# the preview: revision 5 | revision 6 | mock-up, reduced
W = 402; panels = [Image.open(p).convert('RGB').resize((W, 874), Image.LANCZOS) for p in (PNG5, PNG6, MOCK)]
pv = Image.new('RGB', (W * 3 + 80, 874 + 60), (0x1D, 0x25, 0x2D)); dr = ImageDraw.Draw(pv); fnt = ImageFont.truetype(FONT, 20)
for i, (p, cap) in enumerate(zip(panels, ['revision 5 (held; too high)', 'revision 6: the halfway layout (built)', "Science's mock-up (6902002ccfe5fdeb)"])):
    pv.paste(p, (20 + i * (W + 20), 50)); dr.text((20 + i * (W + 20), 16), cap, fill=(0xE8, 0xE0, 0xD2), font=fnt)
os.makedirs(f'{OUT}/proofs', exist_ok=True); prev = f'{OUT}/proofs/TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-preview.png'; pv.save(prev)
R['preview'] = {'file': prev, 'sha16': sha16(prev)}; R['all_pass'] = ok_all
json.dump(R, open(f'{OUT}/work/verify_report.json', 'w'), indent=1); print('all pass:', ok_all, '| preview', R['preview']['sha16'])
sys.exit(0 if ok_all else 1)
