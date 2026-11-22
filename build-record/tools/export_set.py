#!/usr/bin/env python3
"""export_set.py --dir <set folder> --kind notation|owl [--glyph-dir <build_notation work dir>] [--scratch <dir>] [--sheets-only]
Every picture of a set of four layered masters, from one renderer (tools/render.js = resvg-js 2.6.2), field included, transparent outside the coin:
  png/<PREFIX>-<STATE>-<lang>-<px>.png      English and Spanish, 2460 / 1298 (300 dpi at 109.9 mm) / 1214 (300 dpi at 102.785 mm) / 1024 / 512
  proofs/<PREFIX>-<STATE>-no-legend-uncut-ring-1024.png   all legend layers hidden = the whole meander
  proofs/<PREFIX>-...-set.png, -on-white.png, -spanish-and-uncut.png   sheets
  proofs/TETRASEMAPHORE-BUILD3-stamp-before-after.png (notation only, when superseded-build-2/png is there)   the stamp of build 2 and of this build
  scan-cards/ (notation only)  SCAN-<STATE>-whole-coin.png (2000 px) and, with --glyph-dir, SCAN-<STATE>-readable-half.png (the mark alone on its field)
A language is shown by toggling display:none on the legend layers of a scratch copy; the masters are not touched. Added 2026-10-05 (build 3)."""
import argparse, os, re, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(D)
ap = argparse.ArgumentParser(); ap.add_argument('--dir', required=True); ap.add_argument('--kind', required=True, choices=('notation', 'owl'))
ap.add_argument('--glyph-dir'); ap.add_argument('--scratch'); ap.add_argument('--build', default='build 7'); ap.add_argument('--sheets-only', action='store_true'); a = ap.parse_args()
BUILD = a.build; F = a.dir; S = a.scratch or tempfile.mkdtemp(prefix='export-'); os.makedirs(S, exist_ok=True)
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL'); SIZES = (2460, 1298, 1214, 1024, 512)
FIELD = {'NORMATIVE': '#181403', 'NON-NORMATIVE': '#001817', 'METACOGNITIVE': '#17121D', 'CRITICAL': '#1F100E'}
ES = {'NORMATIVE': 'NORMATIVO', 'NON-NORMATIVE': 'INFORMATIVO', 'METACOGNITIVE': 'METACOGNITIVO', 'CRITICAL': 'CRÍTICO'}
PREFIX, PAT = (('TETRASEMAPHORE', 'MASTER-medallion-{st}-notation-slot820.svg') if a.kind == 'notation' else ('OWL-SEMAPHORE', 'MASTER-medallion-{st}-owl-slot820.svg'))
def render(svg, png, px, bg='none'): subprocess.run(['node', 'tools/render.js', svg, png, str(px), bg], check=True, capture_output=True)
def show(s, lang_on):
    def fix(m):
        tag = m.group(0).replace(' style="display:none"', ''); return tag if m.group(1) == lang_on else tag[:-1] + ' style="display:none">'
    out, n = re.subn(r'<g id="legend-(?:plaque|text)-([a-z]+)" inkscape:groupmode="layer"[^>]*>', fix, s); assert n == 4; return out
for d in ('png', 'proofs') + (('scan-cards',) if a.kind == 'notation' else ()): os.makedirs(f'{F}/{d}', exist_ok=True)
for st in (() if a.sheets_only else STATES):
    src = f'{F}/' + PAT.format(st=st); s = open(src, encoding='utf-8').read(); assert s.count('style="display:none"') == 2
    assert show(s, 'en') == s                                                    # the master's own state is English shown
    es = show(s, 'es'); assert es.count('style="display:none"') == 2 and es != s; open(f'{S}/{st}-es.svg', 'w', encoding='utf-8').write(es)
    un = show(s, 'none'); assert un.count('style="display:none"') == 4; open(f'{S}/{st}-uncut.svg', 'w', encoding='utf-8').write(un)
    for px in SIZES:
        render(src, f'{F}/png/{PREFIX}-{st}-en-{px}.png', px); render(f'{S}/{st}-es.svg', f'{F}/png/{PREFIX}-{st}-es-{px}.png', px)
    render(f'{S}/{st}-uncut.svg', f'{F}/proofs/{PREFIX}-{st}-no-legend-uncut-ring-1024.png', 1024)
    if a.kind == 'notation': render(src, f'{F}/scan-cards/SCAN-{st}-whole-coin.png', 2000)
    print('exported', st)
if a.kind == 'notation' and a.glyph_dir and not a.sheets_only:
    K, M = 4.0, 14; s_, n_ = 0.918549, 0.545353
    def crop(st, box, minw=1600):
        render(f'{a.glyph_dir}/{st}-glyph-full.svg', f'{S}/{st}-glyph.png', 3280, FIELD[st])
        im = Image.open(f'{S}/{st}-glyph.png').convert('RGB'); x0, y0, x1, y1 = [int(round(v*K)) for v in box]; c = im.crop((x0, y0, x1, y1))
        if c.width < minw: c = c.resize((minw, int(round(c.height*minw/c.width))), Image.LANCZOS)
        c.save(f'{F}/scan-cards/SCAN-{st}-readable-half.png')
    crop('METACOGNITIVE', (410+s_*(10.5-153.255)-M, 410+s_*(-84.77155-141.3)-M, 410+s_*(296.01-153.255)+M, 410+s_*(-84.77155+63)+M))
    crop('NON-NORMATIVE', (410+s_*(-306.02155+10.5)-M, 410-s_*102.78-M, 410+s_*(-306.02155+284.25)+M, 410+s_*102.78+M))
    crop('CRITICAL', (126, 226, 394, 594)); crop('NORMATIVE', (410-247.3785*n_-M, 410-428.47*n_-M, 410+247.3785*n_+M, 410-10.85*n_-3)); print('scan cards done')

def font(sz, bold=False):
    for p, idx in (('/System/Library/Fonts/HelveticaNeue.ttc', 1 if bold else 0), ('/System/Library/Fonts/Helvetica.ttc', 1 if bold else 0)):
        try: return ImageFont.truetype(p, sz, index=idx)
        except Exception: pass
    return ImageFont.load_default()
def sheet(out, title, bg, items):
    cols = 2 if len(items) <= 4 else 4
    bgc = tuple(int(bg[i:i+2], 16) for i in (1, 3, 5)); light = sum(bgc) > 380; FG = (30, 30, 30) if light else (240, 232, 214); DIM = (90, 90, 90) if light else (170, 160, 150)
    cell, pad, cap, head = 900, 36, 110, 120; rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (cols*cell + (cols+1)*pad, head + rows*(cell+cap) + pad), bgc); d = ImageDraw.Draw(im); d.text((pad, 36), title, font=font(50, True), fill=FG)
    for i, it in enumerate(items):
        x = pad + (i % cols)*(cell+pad); y = head + (i // cols)*(cell+cap); p = Image.open(it[0]).convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        d.text((x+6, y+cell+8), it[1], font=font(40, True), fill=FG)
        if len(it) > 2: d.text((x+6, y+cell+58), it[2], font=font(26), fill=DIM)
    im.save(out); print('wrote', out, im.size)
P, Q = f'{F}/png', f'{F}/proofs'; en = lambda st: f'{P}/{PREFIX}-{st}-en-1024.png'; es_ = lambda st: f'{P}/{PREFIX}-{st}-es-1024.png'; un_ = lambda st: f'{Q}/{PREFIX}-{st}-no-legend-uncut-ring-1024.png'
if a.kind == 'notation':
    name = 'TETRASEMAPHORE-FINAL-MASTERS'; head = f'Tetrasemaphore — the four masters ({BUILD}, proposals)'
    small = {'NORMATIVE': 'one outline · I twice · marks on both mirror lines', 'NON-NORMATIVE': 'twin of METACOGNITIVE · vertical line', 'METACOGNITIVE': 'twin of NON-NORMATIVE · horizontal line', 'CRITICAL': 'as accepted · no mirror line, so no marks'}
else:
    name = 'OWL-SEMAPHORE-FINAL-FOUR'; head = 'Owl Semaphore — the final four, each on its own field'
    small = {'NORMATIVE': 'the owl as it is', 'NON-NORMATIVE': 'the owl mirrored left to right', 'METACOGNITIVE': 'the owl mirrored top to bottom', 'CRITICAL': 'the owl turned half way'}   # plain words: the caption face has no subscript h
sheet(f'{Q}/{name}-set.png', head, '#0E0E12', [(en(st), st, small[st]) for st in STATES])
sheet(f'{Q}/{name}-on-white.png', 'The same four files on a white page — each coin carries its own field', '#FFFFFF', [(en(st), st) for st in STATES])
sheet(f'{Q}/{name}-spanish-and-uncut.png', 'Hidden layers in the same files: Spanish legends · the uncut ring', '#0E0E12',
      [(es_(st), ES[st], 'Spanish layer shown') for st in STATES] + [(un_(st), 'legend layers hidden', 'the whole meander, 24 keys') for st in STATES])

if a.kind == 'notation' and os.path.exists(f'{F}/superseded-build-2/png/{PREFIX}-METACOGNITIVE-en-2460.png'):
    def legend_crop(p, box=(330, 1700, 2130, 2460)):
        im = Image.open(p).convert('RGBA'); c = im.crop(box); bg = Image.new('RGBA', c.size, (14, 14, 18, 255)); bg.alpha_composite(c); return bg.convert('RGB')
    rows = [('Before (build 2): brown plate with shadow, lip and bevel', legend_crop(f'{F}/superseded-build-2/png/{PREFIX}-METACOGNITIVE-en-2460.png')),
            (f"Now ({BUILD}): the plate is the coin's own field, the same dark as the gaps in the ring; flat gold letters", legend_crop(f'{P}/{PREFIX}-METACOGNITIVE-en-2460.png')),
            ('Spanish layer of NON-NORMATIVE, now INFORMATIVO (was NO NORMATIVO)', legend_crop(f'{P}/{PREFIX}-NON-NORMATIVE-es-2460.png'))]
    pad, cap = 30, 64; W = rows[0][1].width + 2*pad; H = 90 + sum(cap + r[1].height + pad for r in rows)
    im = Image.new('RGB', (W, H), (14, 14, 18)); d = ImageDraw.Draw(im); d.text((pad, 24), 'The stamp, cut into the ring again', font=font(44, True), fill=(240, 232, 214)); y = 90
    for t, c in rows:
        d.text((pad, y + 14), t, font=font(30), fill=(222, 200, 117) if t.startswith('Now') else (200, 192, 180)); y += cap; im.paste(c, (pad, y)); y += c.height + pad
    out = f'{Q}/TETRASEMAPHORE-BUILD3-stamp-before-after.png'; im.save(out); print('wrote', out, im.size)
