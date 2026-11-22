#!/usr/bin/env python3
"""Lane's own check of BUILD 3 (run from the dose-01-meander-v2 folder). Build 3 = build 2 with the stamp cut into the ring (sheet section 15),
INFORMATIVO on NON-NORMATIVE's Spanish layer (section 16), and the owl edition in the same packaging (section 14). So:
 A. every notation master equals its build-2 file outside the four legend layers, byte for byte — except one hidden label on NORMATIVE
    (the rings layer named the centre mark #D5AF64; it is #C7B469, and the label now says so);
 B. inside the legend layers only what the sheet names has changed: plate and seams take the field tint, the depth effects and their defs are gone;
    floor, window rails and every letter outline are the build-2 bytes (except the one Spanish word, and the rails' label, which now
    names the ring file by its path);
 C. the Spanish set is NORMATIVO / INFORMATIVO / CRITICO with its accent / METACOGNITIVO and NO NORMATIVO appears nowhere;
 D. each owl coin equals the notation base it shares a config with except the title and label 1, carries the same field tint, and its owl block
    and English lettering are the bytes of the classic owl final (which were the bytes of the approved coin)."""
import re, hashlib, sys, json, glob
import xml.etree.ElementTree as ET
P = 'master/states/proposals'; F = f'{P}/notation/final-masters-2026-10-05'; B2 = f'{F}/superseded-build-2'; OWL = f'{P}/owl-finals-2026-10-05'
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')
FIELD = {'NORMATIVE': '#181403', 'NON-NORMATIVE': '#001817', 'METACOGNITIVE': '#17121D', 'CRITICAL': '#1F100E'}
ES = {'NORMATIVE': 'NORMATIVO', 'NON-NORMATIVE': 'INFORMATIVO', 'METACOGNITIVE': 'METACOGNITIVO', 'CRITICAL': 'CRÍTICO'}
EN = {s: s for s in STATES}
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
ok = True; n = 0
def check(name, cond, detail=''):
    global ok, n; ok &= bool(cond); n += 1; print(('PASS' if cond else 'FAIL'), name, detail)
def block(s, gid, tag='g'):
    key = f'<{tag} id="{gid}"'; assert s.count(key) == 1, (gid, s.count(key)); i = s.index(key)
    if tag != 'g': return s[i:s.index('/>', i) + 2]
    d = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        if m.group(0) == '</g>':
            d -= 1
            if d == 0: return s[i:i + m.end()]
        else:
            gt = s.index('>', i + m.start())
            if s[gt - 1] != '/': d += 1
def top(s):
    """root children as (id-or-tag, text) in order, by depth-counting on the serialised text"""
    root = ET.fromstring(s); return [c.get('id') or c.tag.split('}')[-1] for c in root]
LEG = ['legend-plaque-en', 'legend-text-en', 'legend-plaque-es', 'legend-text-es']
def strip_legends(s):
    for g in LEG: b = block(s, g); s = s.replace(b, f'[[{g}]]')
    return s
def glyph_paths(s, lang): return re.findall(r'<path transform="([^"]*)" d="([^"]*)"/>', block(s, f'legend-glyphs-{lang}'))
def legend_checks(tag, s, st, old=None):
    for lang, word in (('en', EN[st]), ('es', ES[st])):
        pl = block(s, f'legend-plaque-{lang}'); tx = block(s, f'legend-text-{lang}'); rails = block(s, f'legend-rails-{lang}'); own = pl.replace(rails, '')
        kids = re.findall(r'<(?:path|g) id="([^"]+)"', own)
        check(f'{tag} {lang}: plate layer holds only floor, seams, plate (+ rails)', kids == [f'legend-plaque-{lang}', f'legend-floor-{lang}', f'legend-plaque-seams-{lang}', f'legend-plaque-fill-{lang}'], str(kids))
        fills = re.findall(r'<path id="legend-(?:floor|plaque-seams|plaque-fill)-%s" d="[^"]*" fill="(#[0-9A-Fa-f]{6})"/>' % lang, own)
        check(f'{tag} {lang}: floor, seams and plate all in the field tint {FIELD[st]}', fills == [FIELD[st]] * 3, str(fills))
        bare = re.sub(r' inkscape:label="[^"]*"', '', own)      # the label says in words that there are no strokes; test the markup
        check(f'{tag} {lang}: no depth effect left in the plate layer (filter, gradient, clip, stroke, opacity)', not re.search(r'filter|Gradient|clip|stroke|opacity|<defs', bare))
        check(f'{tag} {lang}: lettering layer holds only the letters, fill #DEC875', re.fullmatch(r'<g id="legend-text-%s" inkscape:groupmode="layer" inkscape:label="[^"]*"(?: style="display:none")?>\n<g id="legend-glyphs-%s" fill="#DEC875">(?:<path transform="[^"]*" d="[^"]*"/>)+</g>\n</g>' % (lang, lang), tx) is not None)
        gp = glyph_paths(s, lang); check(f'{tag} {lang}: one outline per letter of {word}', len(gp) == len(word.replace(' ', '')), f'{len(gp)} outlines')
        lab = re.search(r'inkscape:label="5b legend \(%s\) ([^:]*):' % lang, tx).group(1); check(f'{tag} {lang}: label names the word', lab == word, lab)
        hidden = 'style="display:none"' in tx[:tx.index('>')] and 'style="display:none"' in pl[:pl.index('>')]
        check(f'{tag} {lang}: {"hidden" if lang == "es" else "shown"}', hidden == (lang == 'es'))
        if old is not None:
            check(f'{tag} {lang}: floor path = build 2', block(s, f'legend-floor-{lang}', 'path') == block(old, f'legend-floor-{lang}', 'path'))
            d = lambda x, i: re.search(r' d="([^"]*)"', block(x, f'legend-{i}-{lang}', 'path')).group(1)
            check(f'{tag} {lang}: plate and seam outlines = build 2 (colour only changed)', d(s, 'plaque-fill') == d(old, 'plaque-fill') and d(s, 'plaque-seams') == d(old, 'plaque-seams'))
            nolab = lambda x: re.sub(r'(<g id="legend-rails-%s") inkscape:label="[^"]*"' % lang, r'\1', x, count=1)
            check(f'{tag} {lang}: window rails = build 2 bytes (label aside)', nolab(rails) == nolab(block(old, f'legend-rails-{lang}')) and rails != nolab(rails), f'{len(nolab(rails))} bytes')
            check(f'{tag} {lang}: rails label names the ring file by path', 'the seam-fixed cut ring finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys' in rails[:400])
            if not (lang == 'es' and st == 'NON-NORMATIVE'):
                check(f'{tag} {lang}: letter outlines = build 2 bytes', block(s, f'legend-glyphs-{lang}') == block(old, f'legend-glyphs-{lang}'))
            else:
                check(f'{tag} es: the word changed (11 outlines now, 11 before for NO NORMATIVO without its space)', gp != glyph_paths(old, 'es'), f'{len(glyph_paths(old, "es"))} before')
    ids = [e.get('id') for e in ET.fromstring(s).iter() if e.get('id')]
    leg_defs = sorted(i for i in ids if i.startswith('legend-') and re.search(r'blur|grad|clip|shadow|bevel', i))
    check(f'{tag}: the only legend defs left are the two window clips', leg_defs == ['legend-window-clip-en', 'legend-window-clip-es'], str(leg_defs))
    refs = set(re.findall(r'url\(#([^)]+)\)', s)) | set(re.findall(r'href="#([^"]+)"', s)); check(f'{tag}: ids unique, every reference resolves', len(ids) == len(set(ids)) and refs <= set(ids))
    check(f'{tag}: no raster, live text or font reference', not re.search(r'<image|<text|<tspan|font-family|data:', s))
    check(f'{tag}: NO NORMATIVO nowhere in the file', 'NO NORMATIVO' not in s)

print('=== A-C. NOTATION MASTERS against build 2')
for st in STATES:
    p = f'{F}/MASTER-medallion-{st}-notation-slot820.svg'; s = open(p, encoding='utf-8').read(); old = open(f'{B2}/MASTER-medallion-{st}-notation-slot820.svg', encoding='utf-8').read()
    print(f'\n== {st}  build 3 {sha16(p)}  build 2 {sha16(B2 + "/MASTER-medallion-" + st + "-notation-slot820.svg")}')
    check(f'{st}: same root layers in the same order', top(s) == top(old), str(top(s)))
    a_, b_ = strip_legends(s), strip_legends(old)
    if st == 'NORMATIVE':      # one hidden label corrected: the centre mark's colour in the rings layer's label
        fixed, wrong = '(state colour; centre mark #C7B469)', '(state colour; centre mark #D5AF64)'
        check('NORMATIVE: the rings label now names the mark colour that is in the file', a_.count(fixed) == 1 and b_.count(wrong) == 1 and 'fill="#C7B469"' in block(s, 'glyph-placement'))
        a_ = a_.replace(fixed, wrong)
    check(f'{st}: outside the four legend layers the file is build 2, byte for byte' + (' (after that one label)' if st == 'NORMATIVE' else ''), a_ == b_, f'{len(a_)} bytes compared')
    legend_checks(st, s, st, old)

print('\n=== D. OWL EDITION')
for st in STATES:
    p = f'{OWL}/MASTER-medallion-{st}-owl-slot820.svg'; s = open(p, encoding='utf-8').read(); base = open(f'{P}/layered/MASTER-medallion-{st}-layered-slot820.svg', encoding='utf-8').read()
    classic = open(f'{OWL}/classic/MASTER-medallion-{st}-slot820.svg', encoding='utf-8').read(); approved = open(f'master/states/MASTER-medallion-{st}-slot820.svg', encoding='utf-8').read()
    print(f'\n== OWL {st}  {sha16(p)}')
    a, b = s.split('\n'), base.split('\n'); diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    check(f'owl {st}: equals the notation base except the title line and label 1', len(a) == len(b) and len(diff) == 2 and '<title>Owl Semaphore' in a[diff[0]] and '(state colour; owl ' in a[diff[1]], f'{len(diff)} differing lines')
    check(f'owl {st}: layers', top(s)[-9:] == ['field', 'finalA5-rings', 'finalA5-geometry', 'finalA5-finish'] + LEG + ['owl-placement'], str(top(s)))
    f = re.search(r'<g id="field"[^>]*><circle cx="410" cy="410" r="([\d.]+)" fill="(#[0-9A-Fa-f]{6})"/></g>', s); check(f'owl {st}: field tint {FIELD[st]}, r 403.678', f and f.group(2) == FIELD[st] and f.group(1) == '403.678')
    ob = lambda x: x[x.index('<g id="owl-placement"'):x.rindex('</svg>')]
    check(f'owl {st}: owl block (with its V4 operator) = classic final = approved coin, byte for byte', ob(s) == ob(classic) == ob(approved), f'{len(ob(s))} bytes')
    old_letters = re.findall(r'<path transform="([^"]*)" d="([^"]*)"/>', block(approved, 'legend-glyphs'))
    check(f'owl {st}: English letter outlines = approved coin', glyph_paths(s, 'en') == old_letters, f'{len(old_letters)} letters')
    legend_checks(f'owl {st}', s, st)

print('\n=== E. words outside the SVGs')
for pat in (f'{F}/README.md', f'{F}/MANIFEST.json', f'{OWL}/README.md', f'{OWL}/MANIFEST.json', f'{P}/layered/states-config-layered.json', f'{OWL}/states-config-owl-layered.json'):
    for q in glob.glob(pat):
        t = open(q, encoding='utf-8').read(); bad = [m.start() for m in re.finditer('NO NORMATIVO', t)]
        # the README may name the replaced word once, as history
        check(f'{q.split("/")[-1]} ({q.split("/")[-2]}): NO NORMATIVO only as history', len(bad) <= (2 if q.endswith('README.md') else 0), f'{len(bad)} mention(s)')
        check(f'{q.split("/")[-1]} ({q.split("/")[-2]}): no unaccented semaforo / CRITICO as the Spanish word', not re.search(r'[Ss]emaforo\b|\bCRITICO\b', t))
print(f'\n{n} checks:', 'ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)
