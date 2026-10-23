#!/usr/bin/env python3
"""lane-stamp-floor.py <scratch dir> — the stamp check of sheet section 15 on the rendered coins (run from dose-01-meander-v2).
For every coin of both sets and both languages: hide the lettering layer on a scratch copy, render at 2460 px (resvg), and look at the plate between
the rails (3 slot units = 0.38 mm in from each rail face, 1.5 deg in from each end of the window). With no letters on it the plate must be the coin's
field tint and nothing else. Also prints the contrast of the letters (#DEC875) on each tint."""
import re, subprocess, sys, json
import numpy as np
from PIL import Image
S = sys.argv[1]; P = 'master/states/proposals'
SETS = {'notation': f'{P}/notation/final-masters-2026-10-05/MASTER-medallion-%s-notation-slot820.svg', 'owl': f'{P}/owl-finals-2026-10-05/MASTER-medallion-%s-owl-slot820.svg'}
FIELD = {'NORMATIVE': '#181403', 'NON-NORMATIVE': '#001817', 'METACOGNITIVE': '#17121D', 'CRITICAL': '#1F100E'}
WIN = {'NORMATIVE': (60, 120), 'NON-NORMATIVE': (45, 135), 'METACOGNITIVE': (45, 135), 'CRITICAL': (60, 120)}
RIN, ROUT, PX = 317.078, 377.469, 2460
def lum(h):
    c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]; c = [v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4 for v in c]; return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def show(s, lang_on, letters):
    def fix(m):
        tag = m.group(0).replace(' style="display:none"', ''); on = m.group(2) == lang_on and (letters or m.group(1) == 'plaque'); return tag if on else tag[:-1] + ' style="display:none">'
    out, n = re.subn(r'<g id="legend-(plaque|text)-([a-z]+)" inkscape:groupmode="layer"[^>]*>', fix, s); assert n == 4; return out
yy, xx = np.mgrid[0:PX, 0:PX]; k = 820/PX; X = (xx + 0.5)*k - 410; Y = (yy + 0.5)*k - 410; R = np.hypot(X, Y); A = np.degrees(np.arctan2(Y, X))
res = []; ok = True
for kind, pat in SETS.items():
    for st in FIELD:
        s = open(pat % st, encoding='utf-8').read(); f = tuple(int(FIELD[st][i:i+2], 16) for i in (1, 3, 5)); a0, a1 = WIN[st]
        region = (R > RIN + 3) & (R < ROUT - 3) & (A > a0 + 1.5) & (A < a1 - 1.5)
        for lang in ('en', 'es'):
            svg = f'{S}/{kind}-{st}-{lang}-noletters.svg'; png = svg[:-3] + 'png'; open(svg, 'w', encoding='utf-8').write(show(s, lang, False))
            subprocess.run(['node', 'tools/render.js', svg, png, str(PX), 'none'], check=True, capture_output=True)
            im = np.array(Image.open(png).convert('RGBA')).astype(int); d = np.abs(im[..., :3] - np.array(f)).max(axis=2)[region]; al = im[..., 3][region]
            r = dict(set=kind, coin=st, lang=lang, field=FIELD[st], pixels=int(region.sum()), off_by_more_than_0=int((d > 0).sum()), off_by_more_than_3=int((d > 3).sum()), largest_difference=int(d.max()), lowest_alpha=int(al.min()),
                     letters_contrast=round((lum('#DEC875') + 0.05)/(lum(FIELD[st]) + 0.05), 2))
            good = r['off_by_more_than_3'] == 0 and r['lowest_alpha'] == 255; ok &= good; res.append(r)
            print('PASS' if good else 'FAIL', kind, st, lang, f"plate {r['pixels']} px: {r['off_by_more_than_0']} off the tint at all, {r['off_by_more_than_3']} by more than 3 levels (largest {r['largest_difference']}); letters {r['letters_contrast']}:1")
json.dump(res, open(f'{P}/notation/final-masters-2026-10-05/refute/lane-stamp-floor.json', 'w'), indent=1); print('ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)
