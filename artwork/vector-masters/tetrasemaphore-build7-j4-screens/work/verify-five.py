# Verify the five J4 Tetrasemaphore screens (build-five.js, 2026-10-21) with the eleven checks of Science's layout spec §11
# (TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md, revision 4, a2131c898acbb0e8). The expected strings, code points and numbers are read from the spec
# file itself (hash-checked), not from the generator; the generator's layout_report.json is checked against them, and the SVGs and PNGs are
# checked against both. Writes work/verify_report.json and proofs/TETRASEMAPHORE-J4-FIVE-SCREENS-preview.png in the output folder.
# Usage: ~/.cache/dose01-toolchain/venv/bin/python verify-five.py <scratch dir>   (exit 0 only if every check passes)
import re, sys, os, json, hashlib, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lxml import etree
from fontTools.ttLib import TTFont
ROOT = '/Users/careybalboa/Downloads/dose-01-meander-v2'; VM = ROOT + '/vector-masters'; O = os.environ.get('J4_OUT') or VM + '/tetrasemaphore-build7-j4-screens'
HERE = VM + '/work/lockscreen-tetrasemaphore'; NOT = ROOT + '/master/states/proposals/notation/final-masters-2026-10-05/'
CANON = HERE + '/verify-five.py'
if os.path.abspath(__file__) != CANON: sys.exit('run verify-five.py from its canonical path ' + CANON + ' (the copy in work/ is the record, not a runnable; lane rule after the 21 Oct skeptic panel, R1)')
SPEC = '/Users/careybalboa/Downloads/TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md'; FONT = '/Users/careybalboa/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf'
PY = os.path.expanduser('~/.cache/dose01-toolchain/venv/bin/python'); SCR = sys.argv[1]; os.makedirs(SCR, exist_ok=True)
SVG = 'http://www.w3.org/2000/svg'; INK = 'http://www.inkscape.org/namespaces/inkscape'; XL = 'http://www.w3.org/1999/xlink'
h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
assert h16(SPEC) == 'a2131c898acbb0e8', 'spec is not revision 4'
GROUND = (0x1D, 0x25, 0x2D); EPS = 0.0005
SCREENS = ['NORMATIVE', 'NON-NORMATIVE', 'CRITICAL', 'ALL-FOUR-flashcard', 'ALL-FOUR-lockscreen']
FILE = {k: f'dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-{k}-flashcard-MASTER' for k in SCREENS[:3]}
# the PNG is the phone file, not a master: named as build 7 names its PNG (…-METACOGNITIVE.png beside …-METACOGNITIVE-MASTER.svg)
PNG = lambda k: FILE[k].replace('-MASTER', '') + '.png'
FILE.update({k: f'dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-{k}-MASTER' for k in SCREENS[3:]})
COIN16 = {'NORMATIVE': 'e0b6366d5c032523', 'NON-NORMATIVE': '4ef1de6ae126279e', 'METACOGNITIVE': 'cccfcff10dc74930', 'CRITICAL': '33413c4af9ec838c'}
# ------------------------------------------------------------------ the spec, parsed
spec = open(SPEC, encoding='utf-8').read()
def section(n):
    m = re.search(rf'^## {n}\. .*?(?=^## |\Z)', spec, re.S | re.M); assert m, f'no §{n}'; return m.group(0)
def sub(sec, head):
    m = re.search(rf'^### {re.escape(head)}.*?(?=^### |\Z)', sec, re.S | re.M); assert m, head; return m.group(0)
clean = lambda c: c.replace('**', '').replace('`', '').strip()
def rows(txt):
    out = []
    for ln in txt.splitlines():
        if not ln.startswith('|'): continue
        cells = [clean(c) for c in ln.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?', c) for c in cells if c): continue
        out.append(cells)
    return out
num = lambda s: float(re.search(r'-?\d+(?:\.\d+)?', s).group(0))
S1, S2, S3, S4, S5, S8 = section(1), section(2), section(3), section(4), section(5), section(8)
P1 = {r[0]: r[1] for r in rows(S1) if len(r) == 2}
GOLD = re.search(r'#[0-9A-F]{6}', P1['gold']).group(0); CREAM = re.search(r'cream (#[0-9A-F]{6})', P1['text colour']).group(1)
GROW = {r[0]: num(r[1]) for r in rows(S1) if len(r) == 3 and re.match(r'(row|divider|line)', r[0]) and re.search(r'\d', r[1])}
DECK = {'row1': GROW['row 1 — operator row / the four symbols'], 'row2': GROW['row 2 — rule box / the law'], 'div': GROW['divider'],
        'line1': GROW['line 1 of the motto / the sentence']}
IDTAB = {r[1]: {'prefix': r[2], 'ids': int(r[3]), 'refs': int(r[4])} for r in rows(S2) if len(r) == 5 and r[0] in ('top-left', 'top-right', 'bottom-left', 'bottom-right')}
# §8 strings and code points
S8STR = {}; cur = None
for r in rows(S8):
    if len(r) != 3 or r[0] == 'screen': continue
    cur = r[0] or cur; S8STR.setdefault(cur, []).append((r[1], ['%04X' % int(x, 16) for x in re.findall(r'U\+([0-9A-F]{4,5})', r[2])]))
SPEC_STRINGS = {'NORMATIVE': S8STR['NORMATIVE'], 'NON-NORMATIVE': S8STR['NON-NORMATIVE'], 'CRITICAL': S8STR['CRITICAL'],
                'ALL-FOUR-flashcard': S8STR['(b) and (c)'], 'ALL-FOUR-lockscreen': S8STR['(b) and (c)']}
# §3 tables
op_sec = sub(S3, 'Operator row'); ru_sec = sub(S3, 'Rule box'); dv_head = re.search(r'^### Divider \(row 3, y ([\d.]+)\): rule (\d+), ([\d.]+), (\d+) × (\d+); diamond centre \((\d+), ([\d.]+)\), ±([\d.]+)', S3, re.M)
mo_sec = sub(S3, 'Motto')
oph = re.search(r'Operator row \(row 1, y ([\d.]+), baseline ([\d.]+)\)', op_sec); ruh = re.search(r'Rule box \(row 2, y ([\d.]+), baseline ([\d.]+)\)', ru_sec)
coin3 = re.search(r'The coin: `(translate\([^`]*\))` on all three', S3).group(1)
EXP = {}
for r in rows(op_sec):
    if r[0] in ('NORMATIVE', 'NON-NORMATIVE', 'CRITICAL'):
        g = re.match(r'(#[0-9A-F]{6}) \((\d) chars?\)', r[7])
        EXP[r[0]] = {'coins': [(r[0], coin3, None)], 'rows': [{'string': r[1], 'advance': num(r[2]), 'w': num(r[3]), 'bx': num(r[4]), 'by': float(oph.group(1)), 'tx': num(r[5]),
                     'base': float(oph.group(2)), 'stroke': r[6], 'glyph': g.group(1), 'split': int(g.group(2))}], 'lines': []}
for r in rows(ru_sec):
    if r[0] in EXP:
        EXP[r[0]]['rows'].append({'string': r[1], 'advance': num(r[2]), 'w': num(r[3]), 'bx': num(r[4]), 'by': float(ruh.group(1)), 'tx': num(r[5]), 'base': float(ruh.group(2)), 'stroke': GOLD, 'glyph': None, 'split': 0})
cur = None
for r in rows(mo_sec):
    if len(r) == 6 and r[1].isdigit():
        cur = r[0] or cur; EXP[cur]['lines'].append({'string': r[2], 'advance': num(r[3]), 'x': num(r[4]), 'base': num(r[5])})
for k in ('NORMATIVE', 'NON-NORMATIVE', 'CRITICAL'):
    EXP[k]['divider'] = {'row_y': float(dv_head.group(1)), 'rule_x': float(dv_head.group(2)), 'rule_y': float(dv_head.group(3)), 'rule_w': float(dv_head.group(4)), 'rule_h': float(dv_head.group(5)),
                         'cx': float(dv_head.group(6)), 'cy': float(dv_head.group(7)), 'hd': float(dv_head.group(8))}
# §4 / §5 tables
def four(sec, key):
    e = {'coins': [], 'rows': [], 'lines': []}
    for r in rows(sec):
        if r[0] in ('top-left', 'top-right', 'bottom-left', 'bottom-right') and len(r) == 4: e['coins'].append((r[1], r[2], r[3]))
        elif r[0] in ('the four symbols', 'the law'):
            if len(r) == 8: e['rows'].append({'string': r[1], 'advance': num(r[2]), 'w': num(r[3]), 'bx': num(r[4]), 'by': num(r[5]), 'tx': num(r[6]), 'base': num(r[7]), 'stroke': GOLD, 'glyph': None, 'split': 0})
            else: e['rows'].append({'string': r[1], 'advance': None, 'w': num(r[2]), 'bx': num(r[3]), 'by': num(r[4]), 'tx': num(r[5]), 'base': num(r[6]), 'stroke': GOLD, 'glyph': None, 'split': 0})
        elif r[0] == 'divider':
            d = next(c for c in r if c.startswith('rule ')); m = re.match(r'rule (\d+), ([\d.]+), (\d+) × (\d+); diamond \((\d+), ([\d.]+)\) ±([\d.]+)', d)
            ry = next(num(c) for c in r[r.index(d) + 1:] if re.fullmatch(r'[\d.]+', c))
            e['divider'] = {'row_y': ry, 'rule_x': float(m.group(1)), 'rule_y': float(m.group(2)), 'rule_w': float(m.group(3)), 'rule_h': float(m.group(4)), 'cx': float(m.group(5)), 'cy': float(m.group(6)), 'hd': float(m.group(7))}
        elif re.fullmatch(r'\d', r[0]) and len(r) == 5: e['lines'].append({'string': r[1], 'advance': num(r[2]), 'x': num(r[3]), 'base': num(r[4])})
        elif r[0].startswith('sentence line'): e['lines'].append({'string': r[1], 'advance': None, 'x': num(r[3]), 'base': num(r[6])})
    return e
EXP['ALL-FOUR-flashcard'] = four(S4, 'card'); EXP['ALL-FOUR-lockscreen'] = four(S5, 'lock')
for i, L in enumerate(EXP['ALL-FOUR-lockscreen']['lines']): L['advance'] = EXP['ALL-FOUR-flashcard']['lines'][i]['advance']
for i, R_ in enumerate(EXP['ALL-FOUR-lockscreen']['rows']): R_['advance'] = EXP['ALL-FOUR-flashcard']['rows'][i]['advance']
for k in SCREENS: assert len(EXP[k]['rows']) == 2 and EXP[k]['lines'] and 'divider' in EXP[k] and EXP[k]['coins'], f'spec parse {k}'
# the tables of §3–§5 must carry exactly the §8 strings of their screen
for k in SCREENS:
    tab = [r['string'] for r in EXP[k]['rows']] + [L['string'] for L in EXP[k]['lines']]; assert tab == [s for s, _ in SPEC_STRINGS[k]], f'§3–§5 vs §8 strings differ on {k}: {tab}'
LAY = json.load(open(O + '/work/layout_report.json', encoding='utf-8'))
RES = {'spec': {'file': SPEC, 'sha16': h16(SPEC), 'revision': 4}, 'layout_report_sha16': h16(O + '/work/layout_report.json'), 'checks': {}}
def put(check, screen, ok, **kw):
    RES['checks'].setdefault(check, {})[screen] = dict(pass_=bool(ok), **kw)
    print(('PASS ' if ok else 'FAIL ') + f'{check:<26} {screen:<20} ' + json.dumps(kw, ensure_ascii=False)[:400])
# ------------------------------------------------------------------ the node helper: fresh textlayout.js runs (stock and one glyph per code point)
HELPER = r'''
const T=require('/Users/careybalboa/Downloads/dose-01-meander-v2/vector-masters/work/lockscreen/textlayout.js'); const fs=require('fs');
function cp(fn){ const f=T.font, own=Object.prototype.hasOwnProperty.call(f,'stringToGlyphs'), orig=f.stringToGlyphs;
  f.stringToGlyphs=function(s){ return Array.from(s).map(c=>f.charToGlyph(c)); }; try{ return fn(); } finally{ if(own) f.stringToGlyphs=orig; else delete f.stringToGlyphs; } }
const req=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
console.log(JSON.stringify(req.map(r=>({stock:T.run(r.text,58,r.x,r.y,0).parts, cp:cp(()=>T.run(r.text,58,r.x,r.y,0)).parts,
  stock_glyphs:T.font.stringToGlyphs(r.text).map(g=>g.name), cp_glyphs:cp(()=>T.font.stringToGlyphs(r.text)).map(g=>g.name),
  adv_stock:T.advance(r.text,58,0), adv_cp:cp(()=>T.advance(r.text,58,0)), ink:cp(()=>T.inkBox(r.text,58,r.x,r.y,0))}))));
'''
open(SCR + '/runs-helper.js', 'w').write(HELPER)
def runs(reqs):
    p = SCR + '/runs-req.json'; json.dump(reqs, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return json.loads(subprocess.run(['node', SCR + '/runs-helper.js', p], capture_output=True, text=True, check=True).stdout)
# ------------------------------------------------------------------ parse the five SVGs
PARSER = etree.XMLParser(huge_tree=True)
DOC = {}; TXT = {}
for k in SCREENS:
    TXT[k] = open(O + '/' + FILE[k] + '.svg', encoding='utf-8').read(); DOC[k] = etree.fromstring(TXT[k].encode('utf-8'), PARSER)
byid = lambda root, i: root.xpath('//*[@id=$i]', i=i)[0]
def ty(el):
    m = re.fullmatch(r'translate\(0 (-?[\d.]+)\)', el.get('transform') or ''); assert m, el.get('id'); return float(m.group(1))
def local(el): return etree.QName(el).localname if isinstance(el.tag, str) else 'comment'
URL = re.compile(r'url\(\s*#([^)\s]+)\s*\)'); IDREF = ('begin', 'end', 'aria-labelledby', 'aria-describedby')
def refs_of(el):
    out = []
    for k_, v in el.attrib.items():
        out += URL.findall(v)
        if k_ in ('href', f'{{{XL}}}href'):
            assert v.startswith('#'), 'reference outside the document: ' + v; out.append(v[1:])
        if k_ in IDREF: out += [t.split('.')[0] for t in re.split(r'[\s;]+', v) if t]
    if local(el) == 'style' and el.text: out += URL.findall(el.text)
    return out
def coin_groups(k):
    r = DOC[k]
    if k in SCREENS[:3]: return [(EXP[k]['coins'][0][0], None, byid(r, 'medallion-slot820'))]
    return [(st, pre, byid(r, pre + 'medallion-slot820')) for st, tr, pre in EXP[k]['coins']]
# ------------------------------------------------------------------ fresh runs at the spec's own numbers
REQ = []; IDX = {}
for k in SCREENS:
    st = DOC[k]; lay = {i: ty(byid(st, i)) for i in ('operator', 'forall', 'cogito')}
    for j, R_ in enumerate(EXP[k]['rows']):
        IDX[(k, 'row', j)] = len(REQ); REQ.append({'text': R_['string'], 'x': R_['tx'], 'y': round(R_['base'] - lay['operator' if j == 0 else 'forall'], 6)})
    for j, L in enumerate(EXP[k]['lines']):
        IDX[(k, 'line', j)] = len(REQ); REQ.append({'text': L['string'], 'x': L['x'], 'y': round(L['base'] - lay['cogito'], 6)})
OUTR = runs(REQ)
# ------------------------------------------------------------------ check 1: strings
for k in SCREENS:
    rep = LAY['screens'][k]; built = [r['string'] for r in rep['rows']] + [L['string'] for L in rep['lines']]; want = SPEC_STRINGS[k]
    cps_ok = all(['%04X' % ord(c) for c in s] == cp for s, cp in want)
    rep_cp_ok = all([c.replace('U+', '') for c in r['code_points']] == ['%04X' % ord(ch) for ch in r['string']] for r in rep['rows'] + rep['lines'])
    hyphen = any('-' in s for s in built)
    # every drawn string as path data: the SVG path(s) of each run equal a fresh run of that string at the spec's x and baseline
    st = DOC[k]; op = byid(st, 'operator'); fa = byid(st, 'forall'); cg = byid(st, 'cogito'); paths_ok = []; notes = []
    for j, layer in enumerate((op, fa)):
        o = OUTR[IDX[(k, 'row', j)]]; ps = [p for p in layer if local(p) == 'path']; sp = EXP[k]['rows'][j]['split']
        want_d = [''.join(o['cp'][:sp]), ''.join(o['cp'][sp:])] if sp else [''.join(o['cp'])]
        paths_ok.append([p.get('d') for p in ps] == want_d)
        if o['stock'] != o['cp']: notes.append(f"{EXP[k]['rows'][j]['string']}: textlayout.js stock run uses glyphs {o['stock_glyphs']}")
    lp = [p for p in cg if local(p) == 'path']; paths_ok.append(len(lp) == len(EXP[k]['lines']))
    for j, p in enumerate(lp):
        o = OUTR[IDX[(k, 'line', j)]]; paths_ok.append(p.get('d') == ''.join(o['cp']))
        if o['stock'] != o['cp']:
            notes.append(f"{EXP[k]['lines'][j]['string']!r}: textlayout.js stock run would draw {len(o['stock_glyphs'])} glyphs for {len(o['cp_glyphs'])} code points ({[g for g in o['stock_glyphs'] if g not in o['cp_glyphs']]}), advance {o['adv_stock']:.3f} against the spec's {o['adv_cp']:.3f}; the SVG carries the code-point run")
    # nothing else on the screen: root children, stack contents
    root = DOC[k]; kids = [(local(c), c.get('id')) for c in root]
    fig = 'medallion' if k in SCREENS[:3] else 'figure'
    kids_ok = kids == [('title', None), ('desc', None), ('g', 'ground'), ('g', fig), ('g', 'stack')]
    stack = byid(root, 'stack'); sk = [(local(c), c.get('id')) for c in stack]
    stack_ok = sk == [('g', 'operator'), ('g', 'forall'), ('g', 'divider-1'), ('g', 'cogito')]
    tags_outside = sorted(set(local(e) for e in stack.iter())); stack_paths = len(stack.xpath('.//svg:path', namespaces={'svg': SVG}))
    exp_paths = (2 if EXP[k]['rows'][0]['split'] else 1) + 1 + len(EXP[k]['lines'])
    ground = byid(root, 'ground'); ground_ok = len(ground) == 1 and local(ground[0]) == 'rect'
    no_text = not root.xpath('//svg:text|//svg:image|//svg:foreignObject|//svg:tspan|//svg:textPath', namespaces={'svg': SVG})
    ok = built == [s for s, _ in want] and cps_ok and rep_cp_ok and not hyphen and all(paths_ok) and kids_ok and stack_ok and stack_paths == exp_paths and ground_ok and no_text and set(tags_outside) <= {'g', 'rect', 'path', 'polygon'}
    put('1_strings', k, ok, strings=len(built), code_points_match_s8=cps_ok, hyphen_minus=hyphen, path_data_equals_fresh_run=all(paths_ok), stack_paths=stack_paths, expected_paths=exp_paths,
        root_children_ok=kids_ok, stack_layers_ok=stack_ok, elements_outside_coins=tags_outside, no_text_or_image=no_text, notes=notes)
# ------------------------------------------------------------------ check 2: glyph coverage
tt = TTFont(FONT); cmap = tt.getBestCmap(); allcp = sorted({ord(c) for k in SCREENS for s, _ in SPEC_STRINGS[k] for c in s})
missing = [hex(c) for c in allcp if c not in cmap]
for k in SCREENS:
    names_ok = True
    for key, o in ((kk, OUTR[i]) for kk, i in IDX.items() if kk[0] == k):
        s = (EXP[k]['rows'] if key[1] == 'row' else EXP[k]['lines'])[key[2]]['string']
        names_ok &= [cmap.get(ord(c)) for c in s] == o['cp_glyphs']
    cps = sorted({ord(c) for s, _ in SPEC_STRINGS[k] for c in s})
    put('2_glyphs', k, not [c for c in cps if c not in cmap] and names_ok, font_sha16=h16(FONT), distinct_code_points=len(cps), missing=[hex(c) for c in cps if c not in cmap], cmap_glyph_is_the_drawn_glyph=names_ok)
RES['glyph_coverage'] = {'font_sha16': h16(FONT), 'distinct_code_points_all_five': len(allcp), 'missing': missing, 'code_points': ['U+%04X' % c for c in allcp]}
# ------------------------------------------------------------------ check 3: coins element for element; check 4: ids and references
def strip_master(path):
    m = etree.parse(path, PARSER).getroot(); kids = [c for c in m if local(c) not in ('title', 'desc')]
    return m, kids
def prefixed_attrs(el, pre):
    a = {}
    for k_, v in el.attrib.items():
        if k_.startswith(f'{{{INK}}}'): continue
        if pre:
            if k_ == 'id': v = pre + v
            v = URL.sub(lambda mm: f'url(#{pre}{mm.group(1)})', v)
            if k_ in ('href', f'{{{XL}}}href') and v.startswith('#'): v = '#' + pre + v[1:]
            if k_ in IDREF: v = ' '.join(pre + t for t in v.split())
        a[k_] = v
    return a
def flat(children):
    out = []
    for c in children: out += list(c.iter())
    return out
RAW = {st: open(NOT + f'MASTER-medallion-{st}-notation-slot820.svg', encoding='utf-8').read() for st in COIN16}
def string_inner(st, pre):
    s = re.search(r'<svg[^>]*>(.*)</svg>\s*$', RAW[st], re.S).group(1)
    s = re.sub(r'<desc>.*?</desc>', '', re.sub(r'<title>.*?</title>', '', re.sub(r'\s+inkscape:[a-z-]+="[^"]*"', '', s), count=1, flags=re.S), count=1, flags=re.S)
    if pre: s = re.sub(r'(\sid=")', r'\g<1>' + pre, s); s = re.sub(r'url\(#', 'url(#' + pre, s); s = re.sub(r'(\s(?:xlink:)?href="#)', r'\g<1>' + pre, s)
    return s
COINREP = {}
for k in SCREENS:
    root = DOC[k]; allids = root.xpath('//@id'); dup = sorted({i for i in allids if allids.count(i) > 1}); idset = set(allids)
    allrefs = [r for e in root.iter() if isinstance(e.tag, str) for r in refs_of(e)]; unresolved = sorted({r for r in allrefs if r not in idset})
    coin_ok4 = True; per = {}; ok3 = True; per3 = {}
    for st, pre, g in coin_groups(k):
        assert h16(NOT + f'MASTER-medallion-{st}-notation-slot820.svg') == COIN16[st]
        m, mk = strip_master(NOT + f'MASTER-medallion-{st}-notation-slot820.svg'); me = flat(mk); se = [e for e in g.iter()][1:]
        n_master_all = sum(1 for _ in m.iter()) - 1
        tags_eq = [local(e) for e in me] == [local(e) for e in se]
        attrs_eq = len(me) == len(se) and all(prefixed_attrs(a, pre) == dict(b.attrib) for a, b in zip(me, se))
        text_eq = len(me) == len(se) and all((a.text or '') == (b.text or '') and (a.tail or '') == (b.tail or '') for a, b in zip(me, se))
        nattr = sum(len(dict(b.attrib)) for b in se)
        # the bytes: the wrapper's content in the screen file equals the master's root content, stripped (and prefixed by this independent rewrite)
        inner = string_inner(st, pre); tr = g.get('transform'); opn = (f'<g id="medallion-slot820" transform="{tr}">' if pre is None else None)
        pos = TXT[k].find(opn) + len(opn) if opn else TXT[k].find('>', TXT[k].find(f'id="{pre}medallion-slot820"')) + 1
        bytes_eq = TXT[k][pos:pos + len(inner)] == inner and TXT[k][pos + len(inner):pos + len(inner) + 4] == '</g>'
        mt = re.fullmatch(r'translate\((-?[\d.]+) (-?[\d.]+)\) scale\(([\d.]+)\)', tr or ''); uniform = bool(mt)
        anc = [g] + list(g.iterancestors()); clip = [(local(a), at) for a in anc for at in ('clip-path', 'mask', 'filter', 'opacity', 'style', 'viewBox') if a is not root and a.get(at) is not None]
        sc = float(mt.group(3)); x0, y0 = float(mt.group(1)), float(mt.group(2)); inside = x0 >= 0 and y0 >= 0 and x0 + 820 * sc <= 1206 and y0 + 820 * sc <= 2622
        txtimg = sum(1 for e in se if local(e) in ('text', 'image', 'foreignObject'))
        c_ok = tags_eq and attrs_eq and text_eq and bytes_eq and uniform and not clip and inside and txtimg == 0
        ok3 &= c_ok
        per3[st] = {'master_elements_excl_root': n_master_all, 'master_elements_after_title_desc_strip': len(me), 'inlined_elements': len(se), 'tag_sequence_equal': tags_eq,
                    'attribute_values_equal': attrs_eq, 'attributes_compared': nattr, 'text_and_tails_equal': text_eq, 'bytes_equal_to_stripped_master': bytes_eq,
                    'transform': tr, 'uniform_scale': sc if uniform else None, 'clip_mask_filter_on_coin_or_ancestors': clip, 'cell_inside_canvas': inside, 'text_image': txtimg}
        # check 4, per coin
        gids = [e.get('id') for e in g.iter() if isinstance(e.tag, str) and e.get('id')]; grefs = [r for e in g.iter() if isinstance(e.tag, str) for r in refs_of(e)]
        if pre: p_ok = all(i.startswith(pre) for i in gids) and all(r.startswith(pre) for r in grefs)
        else: p_ok = True
        inside_ok = all(r in set(gids) for r in grefs)
        spec_counts = IDTAB.get(st, {}) if pre else {}
        cnt_ok = (not pre) or (len(gids) == spec_counts['ids'] and len(grefs) == spec_counts['refs'] and spec_counts['prefix'] == pre)
        coin_ok4 &= p_ok and inside_ok and cnt_ok
        per[st] = {'prefix': pre, 'ids': len(gids), 'references': len(grefs), 'all_carry_prefix': p_ok, 'resolve_inside_own_coin': inside_ok,
                   'spec_ids_refs': [spec_counts.get('ids'), spec_counts.get('refs')] if pre else None}
    alpha = np.asarray(Image.open(O + '/' + PNG(k)).convert('RGBA'))[..., 3]; a255 = bool((alpha == 255).all())
    put('3_coins_element_for_element', k, ok3 and a255, alpha_all_255=a255, coins=per3)
    put('4_ids_and_references', k, not dup and not unresolved and coin_ok4, ids=len(allids), unique=not dup, duplicates=dup, references=len(allrefs), unresolved=unresolved, coins=per)
    COINREP[k] = per3
# ------------------------------------------------------------------ check 5: per-coin render check
REN = ['node', ROOT + '/tools/render.js']
def png(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.int16)
lv = {}
for k in SCREENS:
    comp = png(O + '/' + PNG(k)); per = {}
    for st, pre, g in coin_groups(k):
        tr = g.get('transform'); raw = re.search(r'<svg[^>]*>(.*)</svg>\s*$', RAW[st], re.S).group(1)
        solo = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="{INK}" width="1206" height="2622" viewBox="0 0 1206 2622">'
                f'<rect x="0" y="0" width="1206" height="2622" fill="#1D252D"/><g transform="{tr}">{raw}</g></svg>')
        sp = f'{SCR}/solo-{k}-{st}.svg'; pp = sp[:-4] + '.png'; open(sp, 'w', encoding='utf-8').write(solo)
        subprocess.run(REN + [sp, pp, '1206', 'none'], check=True, capture_output=True)
        a = png(pp); mt = re.fullmatch(r'translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+)\)', tr); x0, y0, sc = map(float, mt.groups()); side = 820 * sc
        X0, Y0, X1, Y1 = int(np.floor(x0)) - 8, int(np.floor(y0)) - 8, int(np.ceil(x0 + side)) + 8, int(np.ceil(y0 + side)) + 8
        d = np.abs(comp[Y0:Y1, X0:X1, :3] - a[Y0:Y1, X0:X1, :3])
        per[st] = {'max': int(d.max()), 'mean': round(float(d.mean()), 3), 'px_differing': int((d.max(-1) > 0).sum()), 'crop': [X0, Y0, X1, Y1], 'solo_png_sha16': h16(pp)}
    lv[k] = per
single_level = max(v['max'] for k in SCREENS[:3] for v in lv[k].values())
for k in SCREENS:
    put('5_per_coin_render', k, all(v['max'] <= single_level for v in lv[k].values()) and all(v['max'] == 0 and v['mean'] == 0 for v in lv[k].values()),
        single_coin_level=single_level, coins={s: [v['max'], v['mean'], v['px_differing']] for s, v in lv[k].items()})
RES['per_coin_render'] = lv
# ------------------------------------------------------------------ check 6: geometry; check 9: deck alignment
pnum = lambda s: [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]
GEO = {}
for k in SCREENS:
    root = DOC[k]; E = EXP[k]; devs = []; fails = []; adv_devs = []; pos_devs = []
    def cmp(name, got, want):
        dv = abs(got - want); devs.append(dv); (adv_devs if 'advance' in name else pos_devs).append(dv)
        if dv > EPS: fails.append(f'{name}: built {got}, spec {want}')
    for j, lid in enumerate(('operator', 'forall')):
        L = byid(root, lid); t = ty(L); rc = [c for c in L if local(c) == 'rect']; assert len(rc) == 1; rc = rc[0]; R_ = E['rows'][j]
        cmp(f'{lid} box x', float(rc.get('x')) - 2, R_['bx']); cmp(f'{lid} box y', float(rc.get('y')) - 2 + t, R_['by']); cmp(f'{lid} box w', float(rc.get('width')) + 4, R_['w'])
        cmp(f'{lid} box h', float(rc.get('height')) + 4, 108); cmp(f'{lid} rx', float(rc.get('rx')), 26); cmp(f'{lid} stroke-width', float(rc.get('stroke-width')), 4)
        if rc.get('stroke') != R_['stroke'] or rc.get('fill') != 'none': fails.append(f'{lid} stroke {rc.get("stroke")} / fill {rc.get("fill")}, spec {R_["stroke"]} / none')
        ps = [c for c in L if local(c) == 'path']; fills = [p.get('fill') for p in ps]; want_f = [R_['glyph'], CREAM] if R_['split'] else [CREAM]
        if fills != want_f: fails.append(f'{lid} fills {fills}, spec {want_f}')
        rep = LAY['screens'][k]['rows'][j]; cmp(f'{lid} report text x', rep['text_x'], R_['tx']); cmp(f'{lid} report baseline', rep['baseline'], R_['base'])
        cmp(f'{lid} report box y', rep['box']['y'], R_['by']); cmp(f'{lid} report advance', rep['advance'], R_['advance'])
        cmp(f'{lid} fresh-run advance', OUTR[IDX[(k, 'row', j)]]['adv_cp'], R_['advance'])
    D = byid(root, 'divider-1'); t = ty(D); rr = D.xpath('.//svg:rect', namespaces={'svg': SVG})[0]; pg = D.xpath('.//svg:polygon', namespaces={'svg': SVG})[0]; dv_ = E['divider']
    cmp('divider rule x', float(rr.get('x')), dv_['rule_x']); cmp('divider rule y', float(rr.get('y')) + t, dv_['rule_y']); cmp('divider rule w', float(rr.get('width')), dv_['rule_w']); cmp('divider rule h', float(rr.get('height')), dv_['rule_h'])
    pts = pnum(pg.get('points')); xs, ys = pts[0::2], pts[1::2]; cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2 + t
    cmp('diamond cx', cx, dv_['cx']); cmp('diamond cy', cy, dv_['cy']); cmp('diamond half-diagonal x', (max(xs) - min(xs)) / 2, dv_['hd']); cmp('diamond half-diagonal y', (max(ys) - min(ys)) / 2, dv_['hd'])
    cmp('divider row y', float(rr.get('y')) - 8 + t, dv_['row_y'])
    if rr.get('fill') != GOLD or pg.get('fill') != GOLD: fails.append('divider colour')
    C = byid(root, 'cogito'); tc = ty(C)
    for j, L in enumerate(E['lines']):
        rep = LAY['screens'][k]['lines'][j]; cmp(f'line {j+1} report x', rep['x'], L['x']); cmp(f'line {j+1} report baseline', rep['baseline'], L['base'])
        cmp(f'line {j+1} layer baseline + ty', rep['baseline_in_layer'] + tc, L['base']); cmp(f'line {j+1} fresh-run advance', OUTR[IDX[(k, 'line', j)]]['adv_cp'], L['advance'])
    for (st, pre, g), (st2, tr_spec, pre2) in zip(coin_groups(k), E['coins']):
        a, b = pnum(g.get('transform')), pnum(tr_spec)
        if st != st2 or len(a) != 3 or len(b) != 3 or (pre or None) != (pre2 or None) and k in SCREENS[3:]: fails.append(f'coin cell {st}/{st2} {pre}/{pre2}')
        for nm, x_, y_ in zip(('tx', 'ty', 'scale'), a, b): cmp(f'{st} transform {nm}', x_, y_)
    # the text x and baseline of every run: its path data equals a fresh run at the spec's numbers (check 1), so the drawn glyphs sit there
    GEO[k] = {'row1': round(float(byid(root, 'operator')[0].get('y')) - 2 + ty(byid(root, 'operator')), 3), 'row2': round(float(byid(root, 'forall')[0].get('y')) - 2 + ty(byid(root, 'forall')), 3),
              'div': round(float(rr.get('y')) - 8 + t, 3), 'line1': round(LAY['screens'][k]['lines'][0]['baseline_in_layer'] + tc, 3)}
    put('6_geometry', k, not fails, values_compared=len(devs), max_deviation=round(max(devs), 6), max_deviation_positions=round(max(pos_devs), 6), max_deviation_advances_vs_spec_3dp=round(max(adv_devs), 6), fails=fails, path_data_at_spec_x_and_baseline=RES['checks']['1_strings'][k]['path_data_equals_fresh_run'])
deck = [GEO[k] for k in SCREENS[:4]]; deck_ok = all(d == deck[0] for d in deck) and all(abs(deck[0][q] - DECK[q]) < EPS for q in DECK)
for k in SCREENS[:4]: put('9_deck_alignment', k, deck_ok, **GEO[k], spec=DECK)
RES['checks']['9_deck_alignment']['ALL-FOUR-lockscreen'] = {'pass_': None, 'not_applicable': True, 'note': 'check 9 does not apply: not on the deck grid by design (§5: rows 202.877 px lower); its four row positions are compared with §5 under 6_geometry', **GEO['ALL-FOUR-lockscreen']}
# ------------------------------------------------------------------ check 7: bands; check 8: overlap and containment
for k in SCREENS:
    a = np.asarray(Image.open(O + '/' + PNG(k)).convert('RGB')); ink = (a != np.array(GROUND, np.uint8)).any(-1)
    top = int(ink[0:451].sum()); bot = int(ink[2360:2622].sum()); rows_ = np.nonzero(ink.any(1))[0]; cols_ = np.nonzero(ink.any(0))[0]
    put('7_bands', k, top == 0 and bot == 0, ink_px_y_0_450=top, ink_px_y_2360_2622=bot, first_ink_row=int(rows_.min()), last_ink_row=int(rows_.max()),
        clearance_below_clock_band=int(rows_.min()) - 450, clearance_above_bottom_band=2360 - int(rows_.max()) - 1)
    # geometry: predicted ink extents, top to bottom
    E = EXP[k]; G = []
    cells = []
    for st, pre, g in coin_groups(k):
        x0, y0, sc = pnum(g.get('transform')); cells.append((x0, y0, x0 + 820 * sc, y0 + 820 * sc, st))
    for yv in sorted({c[1] for c in cells}): G.append(('coins', min(c[0] for c in cells if c[1] == yv), yv, max(c[2] for c in cells if c[1] == yv), max(c[3] for c in cells if c[1] == yv)))
    for j, R_ in enumerate(E['rows']): G.append(('box ' + R_['string'], R_['bx'], R_['by'], R_['bx'] + R_['w'], R_['by'] + 108))
    dv_ = E['divider']; G.append(('divider', dv_['rule_x'], dv_['cy'] - dv_['hd'], dv_['rule_x'] + dv_['rule_w'], dv_['cy'] + dv_['hd']))
    texts = []
    for j, L in enumerate(E['lines']):
        ib = OUTR[IDX[(k, 'line', j)]]['ink']; t_ = ty(byid(DOC[k], 'cogito')); bx = (ib['x1'], ib['y1'] + t_, ib['x2'], ib['y2'] + t_); G.append(('line ' + L['string'], *bx)); texts.append(('line ' + L['string'], *bx))
    rowtext = []
    for j, R_ in enumerate(E['rows']):
        ib = OUTR[IDX[(k, 'row', j)]]['ink']; t_ = ty(byid(DOC[k], 'operator' if j == 0 else 'forall')); bx = (ib['x1'], ib['y1'] + t_, ib['x2'], ib['y2'] + t_); texts.append(('text ' + R_['string'], *bx))
        rowtext.append({'string': R_['string'], 'left': round(bx[0] - R_['bx'], 2), 'right': round(R_['bx'] + R_['w'] - bx[2], 2), 'top': round(bx[1] - R_['by'], 2), 'bottom': round(R_['by'] + 108 - bx[3], 2)})
    inter = lambda p, q: p[1] < q[3] and q[1] < p[3] and p[2] < q[4] and q[2] < p[4]
    hits = [(t[0], c[4]) for t in texts for c in cells if inter(t, (None, *c[:4]))]
    meets = [(p[0], q[0]) for i, p in enumerate(texts) for q in texts[i + 1:] if inter(p, q)]
    gmeets = [(p[0], q[0]) for i, p in enumerate(G) for q in G[i + 1:] if inter(p, q)]
    inside_box = all(r['left'] > 4 and r['right'] > 4 and r['top'] > 4 and r['bottom'] > 4 for r in rowtext)
    canvas = all(0 <= g_[1] and g_[3] <= 1206 and 0 <= g_[2] and g_[4] <= 2622 for g_ in G + texts)
    gaps_geo = [round(G[i + 1][2] - G[i][4], 2) for i in range(len(G) - 1)]
    # the PNG: runs of ink rows, one per predicted element, each inside its prediction
    rr_ = ink.any(1); segs = []; y = 0
    while y < 2622:
        if rr_[y]:
            y1 = y
            while y < 2622 and rr_[y]: y += 1
            segs.append((y1, y - 1))
        else: y += 1
    seg_ok = len(segs) == len(G) and all(np.floor(g_[2]) - 1 <= s[0] and s[1] <= np.ceil(g_[4]) + 1 for s, g_ in zip(segs, G))
    gaps_png = [segs[i + 1][0] - segs[i][1] - 1 for i in range(len(segs) - 1)]
    colsep = []
    if len(cells) == 4:
        for yv in sorted({c[1] for c in cells}):
            l, r_ = [c for c in cells if c[1] == yv]; band = ink[int(np.ceil(yv)):int(np.floor(l[3])), int(np.ceil(l[2])):int(np.floor(r_[0]))]; colsep.append(int(band.sum()))
    edges = int(ink[0].sum() + ink[-1].sum() + ink[:, 0].sum() + ink[:, -1].sum())
    ok = not hits and not meets and not gmeets and inside_box and canvas and seg_ok and edges == 0 and all(c == 0 for c in colsep)
    put('8_overlap_containment', k, ok, text_in_coin_box=hits, text_meets_text=meets, elements_meet=gmeets, formula_text_inside_box_margins_px=rowtext, all_ink_in_canvas_geometry=canvas,
        png_ink_row_runs=len(segs), predicted_elements=len(G), runs_inside_predictions=seg_ok, png_ground_gaps_px=gaps_png, geometry_gaps_px=gaps_geo,
        ink_between_grid_columns=colsep, ink_on_canvas_edge=edges, first_last_ink_col=[int(cols_.min()), int(cols_.max())],
        coin_cells_render_equal_to_solo_coin='see check 5 (0 difference inside every cell means no other ink there)')
# ------------------------------------------------------------------ check 10: tags
pngs = [O + '/' + PNG(k) for k in SCREENS]
tg = subprocess.run([PY, ROOT + '/tools/png_tag.py', '--check'] + pngs, capture_output=True, text=True)
for k, p in zip(SCREENS, pngs):
    line_ = next(l for l in tg.stdout.splitlines() if p in l); put('10_png_tags', k, line_.startswith('ok') and tg.returncode == 0, png_sha16=h16(p), tool=line_.split(': ', 1)[1])
# ------------------------------------------------------------------ check 11: regression gates
gt = subprocess.run(['node', HERE + '/build-five.js', '--gates-only'], capture_output=True, text=True); gj = json.loads(gt.stdout)
for k in SCREENS:
    put('11_regression', k, gt.returncode == 0 and all(v['pass'] for v in gj.values()), sigma_h_row_16_sep=gj['sigma_h_row']['16_sep_identical'], sigma_h_row_build7=gj['sigma_h_row']['build7_identical'],
        motto_cogito=gj['motto_and_rows']['cogito_identical'], forall_row=gj['motto_and_rows']['forall_identical'], m_def_row=gj['motto_and_rows']['m_def_identical'], divider_ground=gj['template_layers']['pass'])
RES['regression_gates'] = gj
# ------------------------------------------------------------------ the preview strip
fnt = ImageFont.truetype(FONT, 22); caps = ['NORMATIVE flashcard', 'NON-NORMATIVE flashcard', 'CRITICAL flashcard', 'ALL-FOUR flashcard', 'ALL-FOUR lock screen (held)']
ims = [Image.open(p).convert('RGB').resize((402, 874), Image.LANCZOS) for p in pngs]; gap, bar = 30, 60
W = sum(i.width for i in ims) + gap * (len(ims) + 1); im = Image.new('RGB', (W, 874 + bar + gap), (14, 14, 18)); dr = ImageDraw.Draw(im); x = gap
for i, c in zip(ims, caps): im.paste(i, (x, bar)); dr.text((x, 20), c, fill=(236, 230, 216), font=fnt); x += i.width + gap
PV = O + '/proofs/TETRASEMAPHORE-J4-FIVE-SCREENS-preview.png'; im.save(PV); subprocess.run([PY, ROOT + '/tools/png_tag.py', PV], check=True, capture_output=True)
# ------------------------------------------------------------------ summary
allpass = all(v['pass_'] for c in RES['checks'].values() for v in c.values() if not v.get('not_applicable'))
RES['checks_counted'] = sum(1 for c in RES['checks'].values() for v in c.values() if not v.get('not_applicable')); RES['checks_not_applicable'] = sum(1 for c in RES['checks'].values() for v in c.values() if v.get('not_applicable'))
RES['files'] = {**{FILE[k] + '.svg': h16(O + '/' + FILE[k] + '.svg') for k in SCREENS}, **{PNG(k): h16(O + '/' + PNG(k)) for k in SCREENS},
                'proofs/TETRASEMAPHORE-J4-FIVE-SCREENS-preview.png': h16(PV), 'work/layout_report.json': h16(O + '/work/layout_report.json'),
                'build-five.js': h16(HERE + '/build-five.js'), 'verify-five.py': h16(os.path.abspath(__file__))}
RES['all_pass'] = allpass
json.dump(RES, open(O + '/work/verify_report.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
shutil.copyfile(CANON, O + '/work/verify-five.py')
print('ALL PASS' if allpass else 'SOME CHECKS FAILED'); sys.exit(0 if allpass else 1)
