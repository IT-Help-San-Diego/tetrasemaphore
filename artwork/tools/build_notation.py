#!/usr/bin/env python3
"""build_notation.py [--config JSON] [--work-dir DIR] [--skip-check] [--skip-measure]
The notation-edition generator (PROPOSAL stage). For each state in the config it takes the APPROVED owl state master
(read-only), locates the exact byte range of its <g id="owl-placement">…</g> node (depth-counted text splice, so no other
byte moves) and replaces it with a <g id="glyph-placement"> node built from the state's glyph source. The V4 operator is
the identity for every state (each notation glyph is already invariant under exactly its own element — Science's
05-METACOGNITIVE-NOTATION.md "trap"); the mark is centred on (410,410) by its bbox, gold included.

Verification, all inside this script and all printed:
 (a) c14n of the new file with glyph-placement removed == c14n of the owl master with owl-placement removed (root child
     index from the config), plus the stricter byte test (old bytes minus the owl node == new bytes minus the glyph node);
 (b) tools/build_states.py --check afterwards: GUARD PASS and all four owl masters IDENTICAL (nothing else touched);
 (c) resvg preview at preview_px and mark size / clearances on the render;
 (d) print floors at print_mm_per_px on the glyph node rendered alone: thinnest stroke (skeleton ridge, taper-excluded,
     and the inscribed-disc width), gold over ink px, clear ground ink->gold, stabiliser IoUs of the mark alone.
     The disc window is sized in MILLIMETRES (common.measure_window_mm, default 0.10; it was a fixed 7 px = 0.14 mm until
     2026-10-04), and the Fix mark (the gold bar or dot) is measured too: its size and its smaller dimension against the floor.
     Optional per state (2026-10-05, the finals): "symmetry_marks" adds a sibling group <g id="symmetry-marks"> after the glyph
     node — two bars across each mirror line at both ends (ISO 128-3 convention; sizes in mm from the config), placed from the
     mark's own extent along the line; the identity checks then treat glyph node + marks group as the swapped content, the ring
     clearance is taken with the marks included, and the gap between the mark and its first bar is measured on the render.
     own_op "identity" (NORMATIVE) is measured too: all three moves must keep the mark.
Every number comes from this run; they are written to <out_dir>/notation-measurements.json.
"""
import argparse, hashlib, json, math, os, re, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)
NS = {'svg': 'http://www.w3.org/2000/svg', 'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
      'xlink': 'http://www.w3.org/1999/xlink'}
for k, v in NS.items():
    ET.register_namespace('' if k == 'svg' else k, v)

def sha16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def fnum(x, nd=6):
    s = f'{x:.{nd}f}'.rstrip('0').rstrip('.')
    return '0' if s in ('', '-0') else s

# ---------------------------------------------------------------- affine + path geometry (for the fit rule) --------
def mat_mul(A, B):  # A∘B : apply B first, then A ; matrices as (a,b,c,d,e,f)
    a, b, c, d, e, f = A; a2, b2, c2, d2, e2, f2 = B
    return (a*a2 + c*b2, b*a2 + d*b2, a*c2 + c*d2, b*c2 + d*d2, a*e2 + c*f2 + e, b*e2 + d*f2 + f)
def parse_transform(t):
    M = (1, 0, 0, 1, 0, 0)
    if not t: return M
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', t):
        v = [float(x) for x in re.split(r'[\s,]+', args.strip()) if x]
        if name == 'translate': m = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == 'scale': m = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == 'matrix': m = tuple(v)
        elif name == 'rotate':
            r = math.radians(v[0]); cs, sn = math.cos(r), math.sin(r); m = (cs, sn, -sn, cs, 0, 0)
            if len(v) == 3: m = mat_mul(mat_mul((1, 0, 0, 1, v[1], v[2]), m), (1, 0, 0, 1, -v[1], -v[2]))
        else: raise ValueError('unsupported transform ' + name)
        M = mat_mul(M, m)
    return M
def apply(M, x, y): a, b, c, d, e, f = M; return (a*x + c*y + e, b*x + d*y + f)

_TOK = re.compile(r'[MmLlHhVvCcSsQqTtZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')
def path_points(d, n=48):
    """Sample every segment of an SVG path (M L H V C S Q T Z, absolute or relative) densely; returns list of (x,y)."""
    toks = _TOK.findall(d); i = 0; pts = []; cur = (0.0, 0.0); start = cur; cmd = None; prev_c = None
    def num():
        nonlocal i; v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]): cmd = toks[i]; i += 1
        rel = cmd.islower(); C = cmd.upper()
        if C == 'M':
            x, y = num(), num(); cur = (cur[0] + x, cur[1] + y) if rel else (x, y); start = cur; pts.append(cur); cmd = 'l' if rel else 'L'; prev_c = None
        elif C == 'L':
            x, y = num(), num(); cur = (cur[0] + x, cur[1] + y) if rel else (x, y); pts.append(cur); prev_c = None
        elif C == 'H':
            x = num(); cur = (cur[0] + x if rel else x, cur[1]); pts.append(cur); prev_c = None
        elif C == 'V':
            y = num(); cur = (cur[0], cur[1] + y if rel else y); pts.append(cur); prev_c = None
        elif C in 'CSQT':
            if C == 'C': p1 = (num(), num()); p2 = (num(), num()); p3 = (num(), num())
            elif C == 'S':
                p2 = (num(), num()); p3 = (num(), num())
                p1r = (2*cur[0] - prev_c[0], 2*cur[1] - prev_c[1]) if prev_c else cur
            elif C == 'Q': p1 = (num(), num()); p3 = (num(), num())
            else:
                p3 = (num(), num()); p1r = (2*cur[0] - prev_c[0], 2*cur[1] - prev_c[1]) if prev_c else cur
            if rel:
                if C in 'CQ': p1 = (cur[0] + p1[0], cur[1] + p1[1])
                if C in 'CS': p2 = (cur[0] + p2[0], cur[1] + p2[1])
                p3 = (cur[0] + p3[0], cur[1] + p3[1])
            if C == 'S': p1 = p1r
            if C == 'T': p1 = p1r
            for k in range(1, n + 1):
                t = k / n; u = 1 - t
                if C in 'CS':
                    x = u**3*cur[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
                    y = u**3*cur[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
                else:
                    x = u*u*cur[0] + 2*u*t*p1[0] + t*t*p3[0]; y = u*u*cur[1] + 2*u*t*p1[1] + t*t*p3[1]
                pts.append((x, y))
            prev_c = p2 if C in 'CS' else p1; cur = p3
        elif C == 'Z':
            cur = start; pts.append(cur); prev_c = None
            if i < len(toks) and not re.match(r'[A-Za-z]', toks[i]): cmd = 'l' if rel else 'L'
        else: raise ValueError('unsupported path command ' + cmd)
    return pts

def elem_bbox(el, M, ids, acc):
    """Accumulate transformed geometry points of an element tree (g/path/rect/polygon/circle/use) into acc."""
    tag = el.tag.split('}')[-1]
    M = mat_mul(M, parse_transform(el.get('transform')))
    if tag == 'g' or tag == 'svg':
        for ch in el: elem_bbox(ch, M, ids, acc)
    elif tag == 'defs': return
    elif tag == 'use':
        href = el.get('{%s}href' % NS['xlink']) or el.get('href'); ref = ids[href.lstrip('#')]
        M2 = mat_mul(M, (1, 0, 0, 1, float(el.get('x', 0)), float(el.get('y', 0))))
        elem_bbox(ref, M2, ids, acc)
    elif tag == 'path':
        acc.extend(apply(M, x, y) for x, y in path_points(el.get('d')))
    elif tag == 'rect':
        x, y, w, h = (float(el.get(k, 0)) for k in ('x', 'y', 'width', 'height'))
        acc.extend(apply(M, px, py) for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)))
    elif tag == 'polygon':
        v = [float(t) for t in re.split(r'[\s,]+', el.get('points').strip())]
        sw = float(el.get('stroke-width', 0)) / 2  # stroke half-width, as a square margin (bbox only)
        for k in range(0, len(v), 2):
            for dx in (-sw, sw):
                for dy in (-sw, sw): acc.append(apply(M, v[k] + dx, v[k+1] + dy))
    elif tag == 'circle':
        cx, cy, r = (float(el.get(k, 0)) for k in ('cx', 'cy', 'r'))
        for a in range(0, 360, 5): acc.append(apply(M, cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a))))
    else: raise ValueError('unsupported element ' + tag)
def bbox(acc):
    xs = [p[0] for p in acc]; ys = [p[1] for p in acc]; return (min(xs), min(ys), max(xs), max(ys))

def attrs(tag_text): return dict(re.findall(r'([\w:.-]+)="([^"]*)"', tag_text))

# ---------------------------------------------------------------- text splice --------------------------------------
def node_range(s, node_id):
    """Byte range [start, end) of <g id="node_id" …>…</g> found by depth-counting <g …> / </g> tags."""
    key = f'<g id="{node_id}"'; assert s.count(key) == 1, (node_id, s.count(key))
    start = s.index(key); depth = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[start:]):
        if m.group(0) == '</g>':
            depth -= 1
            if depth == 0: return start, start + m.end()
        else:
            gt = s.index('>', start + m.start())
            if s[gt - 1] != '/': depth += 1
    raise ValueError('unbalanced <g> for ' + node_id)

def c14n_without(path, idx, expect_id, also=()):
    root = ET.parse(path).getroot(); kids = list(root); ch = kids[idx]
    assert ch.get('id') == expect_id, (path, idx, ch.get('id'))
    for extra in kids[idx + 1:]:
        if extra.get('id') in also: root.remove(extra)
    root.remove(ch)
    return ET.canonicalize(ET.tostring(root, encoding='unicode'), strip_text=False)

# ---------------------------------------------------------------- glyph nodes ---------------------------------------
def glyph_node_sigma(st, cfg, src_text, src_root, ids, log):
    """σₕ-style source: <defs><g id="tok">…</g></defs>, two <use>, one gold <rect>. Fit rule height_slot_units."""
    defs = re.search(r'<defs>.*?</defs>', src_text, re.S).group(0)
    uses = re.findall(r'<use\b[^>]*/>', src_text); assert len(uses) == 2, uses
    rect = attrs(re.search(r'<rect\b[^>]*/>', src_text, re.S).group(0))
    acc = []; elem_bbox(src_root, (1, 0, 0, 1, 0, 0), ids, acc); x0, y0, x1, y1 = bbox(acc)
    w, h = x1 - x0, y1 - y0; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fit = st['fit']; assert fit['rule'] == 'height_slot_units'
    s = fit['value'] / h; C = cfg['centre']
    tf = f'translate({C[0]} {C[1]}) scale({fnum(s)}) translate({fnum(-cx, 4)} {fnum(-cy, 4)})'
    log.update(source_bbox=[round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)], source_size=[round(w, 4), round(h, 4)],
               bbox_centre=[round(cx, 4), round(cy, 4)], scale=round(s, 6), placement_transform=tf,
               mark_size_slot_units_vector=[round(w*s, 3), round(h*s, 3)])
    ra = {k: rect.get(k) for k in ('x', 'y', 'width', 'height')}
    fix = (f'<rect id="glyph-fix" inkscape:label="4b Fix({st["symbol"]}): {st["fix_desc"]}, gold" '
           + ' '.join(f'{k}="{v}"' for k, v in ra.items()) + f' fill="{cfg["gold_hex"]}"/>')
    body = (f'<g id="glyph-body" inkscape:groupmode="layer" inkscape:label="4 {st["symbol"]}: one token, {st["op_kind"]} as a transform" fill="{st["hex"]}">\n'
            + defs + '\n' + '\n'.join(uses) + '\n</g>')
    label = f'4a glyph placement: {st["symbol"]} centred ({C[0]},{C[1]}) by its bbox (gold included), mark height {fit["value"]} slot units; {fit.get("note","")}; V4 operator = identity'
    return tf, label, body, fix

def glyph_node_identity(st, cfg, src_text, src_root, ids, log):
    """I source: <defs><g id="tok">…</g></defs>, ONE <use>, no separate Fix element: Fix(I) is every point, so the body itself
    carries the Fix gold. Fit rule height_slot_units. (Added 2026-10-01 for the NORMATIVE coin; the I convention is Carey's open call.)"""
    defs = re.search(r'<defs>.*?</defs>', src_text, re.S).group(0)
    fit = st['fit']
    if fit['rule'] == 'as_is':
        # diamond-style source: a glyph-placement group with defs and <g fill> groups of uses; every stroke and fill becomes the Fix gold
        defs = re.sub(r'stroke="#[0-9A-Fa-f]{6}"', f'stroke="{cfg["gold_hex"]}"', defs)
        use_groups = re.findall(r'<g fill="#[0-9A-Fa-f]{6}">(.*?)</g>', src_text, re.S); assert use_groups, 'no use groups'
        uses_txt = '\n'.join(u.strip() for u in use_groups); tf = fit['transform']
        gp = ids['glyph-placement']; acc = []; elem_bbox(gp, parse_transform(tf), ids, acc); x0, y0, x1, y1 = bbox(acc)
        log.update(placement_transform=tf, mark_bbox_slot_units_vector=[round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
                   mark_size_slot_units_vector=[round(x1 - x0, 3), round(y1 - y0, 3)])
        body = (f'<g id="glyph-body" inkscape:groupmode="layer" inkscape:label="4 {st["symbol"]}: the identity; Fix({st["symbol"]}) is {st["fix_desc"]}, so the whole glyph carries the Fix gold" fill="{cfg["gold_hex"]}">\n'
                + defs + '\n' + uses_txt + '\n</g>')
        C = cfg['centre']; label = f'4a glyph placement: {st["symbol"]} centred ({C[0]},{C[1]}); {fit.get("note","")}; V4 operator = identity'
        return tf, label, body, ''
    uses = re.findall(r'<use\b[^>]*/>', src_text); assert len(uses) == 1, uses
    acc = []; elem_bbox(src_root, (1, 0, 0, 1, 0, 0), ids, acc); x0, y0, x1, y1 = bbox(acc)
    w, h = x1 - x0, y1 - y0; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    assert fit['rule'] == 'height_slot_units'
    s = fit['value'] / h; C = cfg['centre']
    tf = f'translate({C[0]} {C[1]}) scale({fnum(s)}) translate({fnum(-cx, 4)} {fnum(-cy, 4)})'
    log.update(source_bbox=[round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)], source_size=[round(w, 4), round(h, 4)],
               bbox_centre=[round(cx, 4), round(cy, 4)], scale=round(s, 6), placement_transform=tf,
               mark_size_slot_units_vector=[round(w*s, 3), round(h*s, 3)])
    body = (f'<g id="glyph-body" inkscape:groupmode="layer" inkscape:label="4 {st["symbol"]}: one token, the identity; Fix({st["symbol"]}) is {st["fix_desc"]}, so the whole glyph carries the Fix gold" fill="{cfg["gold_hex"]}">\n'
            + defs + '\n' + uses[0] + '\n</g>')
    label = f'4a glyph placement: {st["symbol"]} centred ({C[0]},{C[1]}) by its bbox, mark height {fit["value"]} slot units; {fit.get("note","")}; V4 operator = identity'
    return tf, label, body, ''

def glyph_node_c2(st, cfg, src_text, src_root, ids, log):
    """C₂ triangle source: carry its glyph-placement group as is minus the background rect; re-label to the id scheme."""
    g = re.search(r'<g id="glyph-placement"[^>]*transform="([^"]*)"[^>]*>', src_text)
    tf = g.group(1) if g else st['fit']['transform']   # the source group carries no transform on disk: the config supplies the convention
    log['placement_transform_from'] = 'source file' if g else 'config fit.transform'
    defs = re.search(r'<defs>.*?</defs>', src_text, re.S).group(0)
    hexes = set(re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', defs))
    log['source_ink_hexes_in_defs'] = sorted(hexes)
    defs = re.sub(r'stroke="#[0-9A-Fa-f]{6}"', f'stroke="{st["hex"]}"', defs)  # the triangle outline is a stroke: state colour
    circ = attrs(re.search(r'<circle\b[^>]*/>', src_text).group(0))
    use_groups = re.findall(r'<g fill="#[0-9A-Fa-f]{6}">(.*?)</g>', src_text, re.S); assert len(use_groups) == 2, len(use_groups)
    uses = '\n'.join(u.strip() for u in use_groups)
    ca = {k: circ.get(k) for k in ('cx', 'cy', 'r')}
    fix = (f'<circle id="glyph-fix" inkscape:label="4b Fix({st["symbol"]}): {st["fix_desc"]}, gold" '
           + ' '.join(f'{k}="{v}"' for k, v in ca.items()) + f' fill="{cfg["gold_hex"]}"/>')
    body = (f'<g id="glyph-body" inkscape:groupmode="layer" inkscape:label="4 {st["symbol"]}: one token, {st["op_kind"]} as a transform" fill="{st["hex"]}">\n'
            + defs + '\n' + uses + '\n</g>')
    gp = ids['glyph-placement']; acc = []; elem_bbox(gp, parse_transform(tf) if not g else (1, 0, 0, 1, 0, 0), ids, acc); x0, y0, x1, y1 = bbox(acc)
    C = cfg['centre']; log.update(placement_transform=tf, mark_bbox_slot_units_vector=[round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
                                  mark_size_slot_units_vector=[round(x1 - x0, 3), round(y1 - y0, 3)],
                                  mark_bbox_centre_slot_units_vector=[round((x0 + x1)/2, 3), round((y0 + y1)/2, 3)])
    label = f'4a glyph placement: {st["symbol"]} centred ({C[0]},{C[1]}); {st["fit"].get("note","")}; V4 operator = identity'
    return tf, label, body, fix

def marks_node(st, cfg, log):
    """<g id="symmetry-marks">: at both ends of each mirror line, two bars across the line (len x thick mm), the first off_mm beyond
    the mark's extent along the line, then gap_mm, then the second. Axis v = the vertical line (bars above and below the mark),
    axis h = the horizontal line (bars left and right). Extent: half the mark's bbox along the line (extent bbox), or given in
    glyph units from the glyph centre (extent_glyph_units, times the placement scale) where a stroke's miter tip is the extent."""
    sm = st.get('symmetry_marks')
    if not sm or not sm.get('axes'): return ''
    U = cfg['medallion_units']; k = U / cfg['print_mm']; C = cfg['centre']
    L, T, O, G = (sm[x] * k for x in ('len_mm', 'thick_mm', 'offset_mm', 'gap_mm'))
    sc = float(re.findall(r'scale\(([-\d.]+)\)', log['placement_transform'])[-1])
    rects, ext_log = [], {}
    for ax in sm['axes']:
        if sm.get('extent_glyph_units'): e = sm['extent_glyph_units'][ax] * sc
        else:
            w, h = log['source_size']; e = (h if ax == 'v' else w) / 2 * sc
        ext_log[ax] = round(e, 4)
        for sign in (-1, 1):
            for j in (0, 1):
                inner = e + O + j * (T + G)            # distance from the centre to the bar's inner edge
                lo = C[0 if ax == 'h' else 1] + (inner if sign > 0 else -(inner + T))
                if ax == 'h': rects.append((lo, C[1] - L / 2, T, L))
                else: rects.append((C[0] - L / 2, lo, L, T))
    log['symmetry_marks'] = dict(axes=sm['axes'], extent_slot_units=ext_log, bar_slot_units=[round(L, 3), round(T, 3)],
                                 first_bar_inner_edge_mm={a: round((ext_log[a] + O) / k, 3) for a in ext_log},
                                 outer_edge_mm={a: round((ext_log[a] + O + 2 * T + G) / k, 3) for a in ext_log}, count=len(rects))
    lab = (f'6 symmetry marks: two bars across each mirror line of the mark at both ends ({sm["len_mm"]} x {sm["thick_mm"]} mm; the first {sm["offset_mm"]} mm '
           f'beyond the mark, then {sm["gap_mm"]} mm, then the second), the coin colour; the drafting convention for a line of symmetry (ISO 128-3), proportions ours')
    body = ''.join(f'<rect x="{fnum(x, 3)}" y="{fnum(y, 3)}" width="{fnum(w_, 3)}" height="{fnum(h_, 3)}"/>' for x, y, w_, h_ in rects)
    return f'<g id="symmetry-marks" inkscape:groupmode="layer" inkscape:label="{lab}" fill="{sm["hex"]}">{body}</g>'

def assemble(tf, label, body, fix, with_body=True, with_fix=True):
    parts = [p for p, on in ((body, with_body), (fix, with_fix)) if on]
    return (f'<g id="glyph-placement" xmlns:xlink="{NS["xlink"]}" inkscape:label="{label}" transform="{tf}">\n'
            + '\n'.join(parts) + '\n</g>')

# ---------------------------------------------------------------- raster measurement ---------------------------------
def render(svg, png, width, bg):
    r = subprocess.run(['node', 'tools/render.js', svg, png, str(width), bg], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
def alpha(png):
    import numpy as np; from PIL import Image
    return np.array(Image.open(png).convert('RGBA'))[..., 3] > 127

def zhang_suen(img):
    import numpy as np
    I = np.pad(img.astype(np.uint8), 1)
    while True:
        changed = False
        for step in (0, 1):
            P2 = I[:-2, 1:-1]; P3 = I[:-2, 2:]; P4 = I[1:-1, 2:]; P5 = I[2:, 2:]; P6 = I[2:, 1:-1]; P7 = I[2:, :-2]; P8 = I[1:-1, :-2]; P9 = I[:-2, :-2]
            seq = [P2, P3, P4, P5, P6, P7, P8, P9, P2]
            B = sum(p.astype(np.int16) for p in seq[:8])
            A = sum(((seq[k] == 0) & (seq[k+1] == 1)).astype(np.int16) for k in range(8))
            cond = ((P2*P4*P6 == 0) & (P4*P6*P8 == 0)) if step == 0 else ((P2*P4*P8 == 0) & (P2*P6*P8 == 0))
            m = (I[1:-1, 1:-1] == 1) & (B >= 2) & (B <= 6) & (A == 1) & cond
            if m.any(): I[1:-1, 1:-1][m] = 0; changed = True
        if not changed: break
    return I[1:-1, 1:-1].astype(bool)

def stroke_floors(body, mm_per_px, k_px_per_unit, x_off, y_off, win_px=7):
    """Thinnest stroke of a binary ink mask: skeleton ridge width (2*EDT on the skeleton) with a taper exclusion of one
    median ridge width around every skeleton endpoint, and the inscribed-disc width (EDT snapped to its local maximum
    inside a win_px window; the caller sizes that window in millimetres)."""
    import numpy as np; from scipy import ndimage as ndi
    edt = ndi.distance_transform_edt(body)
    sk = zhang_suen(body)
    nb = ndi.convolve(sk.astype(np.int16), np.ones((3, 3), np.int16), mode='constant') - sk.astype(np.int16)
    ends = sk & (nb <= 1)
    w_all = 2 * edt[sk]; med = float(np.median(w_all))
    d_end = ndi.distance_transform_edt(~ends) if ends.any() else np.full(body.shape, np.inf)
    keep = sk & (d_end > med)
    if not keep.any(): keep = sk
    disc = 2 * ndi.maximum_filter(edt, size=win_px)
    ridge_w = 2 * edt[keep]; disc_w = disc[keep]
    ys, xs = np.nonzero(keep); i_r = int(np.argmin(ridge_w)); i_d = int(np.argmin(disc_w))
    lab, n = ndi.label(body)
    per = []
    for c in range(1, n + 1):
        m = keep & (lab == c)
        if not m.any(): continue
        cy, cx = np.nonzero(lab == c)
        per.append(dict(component=c, area_px=int((lab == c).sum()),
                        centre_slot=[round(float((cx.mean() + 0.5)/k_px_per_unit + x_off), 1), round(float((cy.mean() + 0.5)/k_px_per_unit + y_off), 1)],
                        thinnest_ridge_mm=round(float(2*edt[m].min()*mm_per_px), 3), thinnest_disc_mm=round(float(disc[m].min()*mm_per_px), 3)))
    return dict(skeleton_px=int(sk.sum()), endpoints=int(ends.sum()), median_ridge_width_mm=round(med*mm_per_px, 3),
                thinnest_ridge_mm=round(float(ridge_w[i_r]*mm_per_px), 3),
                thinnest_ridge_at_slot=[round(float((xs[i_r] + 0.5)/k_px_per_unit + x_off), 1), round(float((ys[i_r] + 0.5)/k_px_per_unit + y_off), 1)],
                thinnest_disc_mm=round(float(disc_w[i_d]*mm_per_px), 3),
                thinnest_disc_at_slot=[round(float((xs[i_d] + 0.5)/k_px_per_unit + x_off), 1), round(float((ys[i_d] + 0.5)/k_px_per_unit + y_off), 1)],
                per_component=per)

def measure(st, cfg, node_parts, work, out_dir, proposal_svg, marks=''):
    import numpy as np; from scipy import ndimage as ndi; from scipy.spatial import cKDTree
    U = cfg['medallion_units']; mm_u = cfg['print_mm'] / U; C = cfg['centre']; res = {}
    head = f'<svg xmlns="{NS["svg"]}" xmlns:inkscape="{NS["inkscape"]}" width="{U}" height="{U}" viewBox="0 0 {U} {U}">\n'
    variants = {'full': assemble(*node_parts), 'body': assemble(*node_parts, with_fix=False), 'fix': assemble(*node_parts, with_body=False)}
    paths = {}
    for v, node in variants.items():
        p = os.path.join(work, f'{st["name"]}-glyph-{v}.svg'); open(p, 'w', encoding='utf-8').write(head + node + '\n</svg>\n'); paths[v] = p
    # (c) preview + clearances at preview_px
    W = cfg['preview_px']; k = W / U
    preview = os.path.join(out_dir, st['out'].replace('.svg', '-preview.png')); render(proposal_svg, preview, W, cfg.get('preview_bg', '#1A1020'))
    png = os.path.join(work, f'{st["name"]}-glyph-full-{W}.png'); render(paths['full'], png, W, 'none'); A = alpha(png)
    ys, xs = np.nonzero(A); X = (xs + 0.5) / k; Y = (ys + 0.5) / k
    x0, x1, y0, y1 = X.min() - 0.5/k, X.max() + 0.5/k, Y.min() - 0.5/k, Y.max() + 0.5/k
    r = np.hypot(X - C[0], Y - C[1]); th = (np.degrees(np.arctan2(Y - C[1], X - C[0])) + 360) % 360
    ring_clear = cfg['ring_inner_edge_r'] - r.max()
    a0, a1 = st['plaque_span']; ri, ro = cfg['plaque_inner_r'], cfg['plaque_outer_r']
    ang = np.radians(np.arange(a0, a1 + 1e-9, 0.02)); rad = np.arange(ri, ro + 1e-9, 0.05)
    Bp = np.concatenate([np.c_[C[0] + ri*np.cos(ang), C[1] + ri*np.sin(ang)], np.c_[C[0] + ro*np.cos(ang), C[1] + ro*np.sin(ang)],
                         np.c_[C[0] + rad*math.cos(math.radians(a0)), C[1] + rad*math.sin(math.radians(a0))],
                         np.c_[C[0] + rad*math.cos(math.radians(a1)), C[1] + rad*math.sin(math.radians(a1))]])
    edge = A & ~ndi.binary_erosion(A); ey, ex = np.nonzero(edge)
    dmin, _ = cKDTree(Bp).query(np.c_[(ex + 0.5)/k, (ey + 0.5)/k]); plaque_clear = float(dmin.min())
    res['preview_png'] = preview; res['preview_sha16'] = sha16(preview)
    res['mark_bbox_slot_units'] = [round(float(v), 2) for v in (x0, y0, x1, y1)]
    res['mark_size_slot_units'] = [round(float(x1 - x0), 2), round(float(y1 - y0), 2)]
    res['mark_size_mm'] = [round(float((x1 - x0)*mm_u), 2), round(float((y1 - y0)*mm_u), 2)]
    res['mark_bbox_centre_slot_units'] = [round(float((x0 + x1)/2), 2), round(float((y0 + y1)/2), 2)]
    res['ink_centroid_slot_units'] = [round(float(X.mean()), 2), round(float(Y.mean()), 2)]
    res['ring_clearance_slot_units'] = round(float(ring_clear), 2); res['ring_clearance_mm'] = round(float(ring_clear*mm_u), 2)
    res['ring_clearance_at_deg'] = round(float(th[np.argmax(r)]), 1)
    res['plaque_span_deg'] = [a0, a1]; res['plaque_clearance_slot_units'] = round(plaque_clear, 2); res['plaque_clearance_mm'] = round(plaque_clear*mm_u, 2)
    # (d) print floors
    Wp = int(round(cfg['print_mm'] / cfg['print_mm_per_px'])); mm_px = cfg['print_mm'] / Wp; kp = Wp / U
    masks = {}
    for v in variants:
        pp = os.path.join(work, f'{st["name"]}-glyph-{v}-{Wp}.png'); render(paths[v], pp, Wp, 'none'); masks[v] = alpha(pp)
    full, body, fix = masks['full'], masks['body'], masks['fix']
    mk = None
    if marks:
        pm = os.path.join(work, f'{st["name"]}-marks.svg'); open(pm, 'w', encoding='utf-8').write(head + marks + '\n</svg>\n')
        pp = os.path.join(work, f'{st["name"]}-marks-{Wp}.png'); render(pm, pp, Wp, 'none'); mk = alpha(pp)
    whole = full | mk if mk is not None else full          # what a move has to keep: the mark and its symmetry marks
    ious = {}
    for op, T in (('sigma_h', lambda a: a[::-1, :]), ('sigma_v', lambda a: a[:, ::-1]), ('c2', lambda a: a[::-1, ::-1])):
        t = T(whole); ious[op] = round(float((whole & t).sum() / (whole | t).sum()), 4)
    yy, xx = np.nonzero(full); pad = 8
    y0p, y1p, x0p, x1p = max(yy.min() - pad, 0), min(yy.max() + pad + 1, Wp), max(xx.min() - pad, 0), min(xx.max() + pad + 1, Wp)
    bc, fc = body[y0p:y1p, x0p:x1p], fix[y0p:y1p, x0p:x1p]
    win_mm = cfg.get('measure_window_mm', 0.10); win_px = max(3, int(round(win_mm / mm_px)) | 1)   # odd window, sized in mm
    t0 = time.time(); fl = stroke_floors(bc, mm_px, kp, x0p / kp, y0p / kp, win_px); fl['skeleton_seconds'] = round(time.time() - t0, 1)
    fl['window_mm'] = round(win_px * mm_px, 4); fl['window_px'] = win_px
    gold_over_ink = int((bc & fc).sum())
    d_ink = ndi.distance_transform_edt(~bc); clear = float(d_ink[fc].min()) if fc.any() else None
    if mk is not None:   # the symmetry marks: each bar's size, the gap from the mark to the nearest bar, and the ring clearance with them
        d_full = ndi.distance_transform_edt(~full); lab_m, n_m = ndi.label(mk); bars = []
        for c in range(1, n_m + 1):
            my, mx = np.nonzero(lab_m == c); bars.append([round(float((mx.max() - mx.min() + 1) * mm_px), 3), round(float((my.max() - my.min() + 1) * mm_px), 3)])
        res['symmetry_marks'] = dict(bars=n_m, bar_sizes_mm=bars, gap_mark_to_nearest_bar_mm=round(float(d_full[mk].min() * mm_px), 3),
                                     marks_over_mark_px=int((full & mk).sum()))
    wy, wx = np.nonzero(whole); r_all = np.hypot((wx + 0.5) / kp - C[0], (wy + 0.5) / kp - C[1]).max()   # farthest ink, marks included, at print resolution
    res['print'] = dict(render_px=Wp, mm_per_px=round(mm_px, 6), mark_size_mm=[round(float((xx.max() - xx.min() + 1)*mm_px), 2), round(float((yy.max() - yy.min() + 1)*mm_px), 2)],
                        ink_px=int(bc.sum()), gold_px=int(fc.sum()), gold_over_ink_px=gold_over_ink,
                        clear_ground_mm=(None if clear is None else round(clear*mm_px, 3) if gold_over_ink == 0 else 0.0), iou=ious, floors=fl)
    if st['own_op'] == 'identity': own = min(ious.values()); others = []          # the identity mark is kept by all three moves
    else: own = ious[st['own_op']]; others = [ious[o] for o in ious if o != st['own_op']]
    cg_ok = True if clear is None else res['print']['clear_ground_mm'] >= cfg['floor_mm']
    floor_ring = cfg.get('ring_clearance_floor_mm')
    rc = round(float((cfg['ring_inner_edge_r'] - r_all) * mm_u), 3)
    ring_ok = True if floor_ring is None else rc >= floor_ring
    res['print']['ring_clearance_all_ink_mm'] = rc; res['print']['ring_clearance_floor_mm'] = floor_ring; res['print']['ring_clearance_ok'] = bool(ring_ok)
    thin = fl['thinnest_disc_mm']
    res['print']['thinnest_mm'] = thin   # the quoted figure: inscribed-disc width (the ridge reads low, c2 README refuter note 2)
    fix_ok = True
    if fc.any():   # the Fix mark (gold bar or dot): its size, and its smaller dimension (bar thickness / dot diameter) against the floor
        fy, fx = np.nonzero(fc); fw, fh = (fx.max() - fx.min() + 1) * mm_px, (fy.max() - fy.min() + 1) * mm_px
        res['print']['fix_mark_size_mm'] = [round(float(fw), 3), round(float(fh), 3)]
        res['print']['fix_mark_min_mm'] = round(float(min(fw, fh)), 3)
        fix_ok = bool(min(fw, fh) >= cfg['floor_mm'])
    res['print']['floor_margin_mm'] = round(thin - cfg['floor_mm'], 3)
    res['print']['floor_margin_indeterminate'] = bool(abs(thin - cfg['floor_mm']) < 0.1)   # Science's calibration note: < 0.1 mm is not a pass or a fail
    res['print']['pass'] = bool(thin >= cfg['floor_mm'] and fix_ok and gold_over_ink == 0 and cg_ok and ring_ok
                                and own >= cfg['iou_own_min'] and all(o <= cfg['iou_other_max'] for o in others))
    res['print']['pass_rule'] = (f'thinnest (inscribed disc in a {fl["window_mm"]} mm window, taper-excluded) >= {cfg["floor_mm"]} mm, Fix mark smaller dimension >= {cfg["floor_mm"]} mm, gold over ink == 0, clear ground >= {cfg["floor_mm"]} mm, '
                                 f'IoU own >= {cfg["iou_own_min"]}, others <= {cfg["iou_other_max"]} (identity: all three >= own), '
                                 f'closest ink to the ring (marks included) >= {floor_ring} mm; a margin under 0.1 mm is flagged indeterminate')
    return res

# ---------------------------------------------------------------- main ------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='master/states/proposals/notation/notation-config.json')
    ap.add_argument('--work-dir', default=None); ap.add_argument('--skip-check', action='store_true'); ap.add_argument('--skip-measure', action='store_true')
    a = ap.parse_args()
    CFG = json.load(open(a.config, encoding='utf-8')); cfg = CFG['common']; out_dir = cfg['out_dir']; os.makedirs(out_dir, exist_ok=True)
    work = a.work_dir or tempfile.mkdtemp(prefix='notation-'); os.makedirs(work, exist_ok=True)
    SC = json.load(open(cfg['states_config'], encoding='utf-8')); sc_states = {s['name']: s for s in SC['states']}
    guarded = [SC['guard']['out']] + [f'master/states/MASTER-medallion-{s["name"]}-slot820.svg' for s in SC['states']]
    before = {p: sha16(p) for p in guarded}
    report = dict(config=os.path.abspath(a.config), work_dir=os.path.abspath(work), approved_masters_before=before, states=[])
    for st in CFG['states']:
        sc = sc_states[st['name']]; st['hex'] = sc['owl_hex']; st['plaque_span'] = [SC['common'][sc['keys']]['a0'], SC['common'][sc['keys']]['a1']]
        log = dict(name=st['name'], symbol=st['symbol'], state_hex=st['hex'], gold_hex=cfg['gold_hex'], owl_master=st['owl_master'],
                   owl_master_sha16=sha16(st['owl_master']), glyph_source=st['glyph_source'], glyph_source_sha16=sha16(st['glyph_source']), fit=st['fit'])
        src_text = open(st['glyph_source'], encoding='utf-8').read(); src_root = ET.fromstring(src_text)
        ids = {e.get('id'): e for e in src_root.iter() if e.get('id')}
        parts = (glyph_node_identity if st.get('op_kind') == 'identity' else glyph_node_sigma if st['fit']['rule'] == 'height_slot_units' else glyph_node_c2)(st, cfg, src_text, src_root, ids, log)
        node = assemble(*parts); marks = marks_node(st, cfg, log)
        M = open(st['owl_master'], encoding='utf-8').read(); s0, e0 = node_range(M, cfg['owl_node_id'])
        assert M[s0-1] == '\n' and M[e0] == '\n', 'unexpected bytes around the owl node'
        new = M[:s0] + node + ('\n' + marks if marks else '') + M[e0:]
        out = os.path.join(out_dir, st['out']); open(out, 'w', encoding='utf-8', newline='\n').write(new)
        # (a) verification: byte splice and c14n (with symmetry marks, glyph node + marks group are the swapped content)
        s1, e1 = node_range(new, cfg['glyph_node_id'])
        if marks:
            sm_, em_ = node_range(new, 'symmetry-marks'); assert new[e1:sm_] == '\n', 'the marks group must follow the glyph node'; e1 = em_
        log['byte_identical_outside_swapped_node'] = (M[:s0] + M[e0:]) == (new[:s1] + new[e1:])
        log['c14n_identical'] = c14n_without(st['owl_master'], cfg['swapped_node_index'], cfg['owl_node_id']) == c14n_without(out, cfg['swapped_node_index'], cfg['glyph_node_id'], also=('symmetry-marks',))
        log['owl_node_bytes'] = e0 - s0; log['glyph_node_bytes'] = e1 - s1; log['out'] = os.path.abspath(out); log['out_sha16'] = sha16(out); log['out_bytes'] = len(new.encode('utf-8'))
        log['exactness_grep'] = dict(tok_defs=len(re.findall(r'<g id="tok[C]?"', node)), uses=len(re.findall(r'<use\b', node)),
                                     scale_1_m1=node.count('scale(1 -1)'), rotate_180=node.count('rotate(180'), glyph_fix=node.count('id="glyph-fix"'))
        print(f'{st["name"]}: wrote {out} sha16 {log["out_sha16"]}  placement {log["placement_transform"]}  '
              f'c14n_identical={log["c14n_identical"]} byte_identical={log["byte_identical_outside_swapped_node"]}')
        if not a.skip_measure:
            log['measure'] = measure(st, cfg, parts, work, out_dir, out, marks)
            m = log['measure']; p = m['print']; f = p['floors']
            print(f'  size {m["mark_size_slot_units"]} slot = {m["mark_size_mm"]} mm; ring clearance {m["ring_clearance_mm"]} mm @ {m["ring_clearance_at_deg"]} deg; '
                  f'plaque clearance {m["plaque_clearance_mm"]} mm; print: thinnest ridge {f["thinnest_ridge_mm"]} / disc {f["thinnest_disc_mm"]} mm at {f["thinnest_disc_at_slot"]}, '
                  f'Fix mark {p.get("fix_mark_size_mm", "none")} mm, gold over ink {p["gold_over_ink_px"]} px, clear ground {p["clear_ground_mm"]} mm, IoU {p["iou"]}, '
                  f'closest ink to the ring {p["ring_clearance_all_ink_mm"]} mm (floor {p["ring_clearance_floor_mm"]}), marks {m.get("symmetry_marks", "none")}, '
                  f'PASS={p["pass"]} (margin {p["floor_margin_mm"]} mm{", INDETERMINATE" if p["floor_margin_indeterminate"] else ""})')
        report['states'].append(log)
    # (b) the owl edition must be untouched
    if not a.skip_check:
        r = subprocess.run([sys.executable, 'tools/build_states.py', '--check'], capture_output=True, text=True)
        report['build_states_check'] = dict(returncode=r.returncode, stdout=r.stdout.strip(), guard_pass='GUARD PASS' in r.stdout, identical=r.stdout.count(' IDENTICAL'))
        print(r.stdout.strip())
    report['approved_masters_after'] = {p: sha16(p) for p in guarded}
    report['approved_masters_unchanged'] = report['approved_masters_after'] == before
    assert report['approved_masters_unchanged'], 'an approved master changed!'
    jp = os.path.join(out_dir, 'notation-measurements.json'); json.dump(report, open(jp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('approved masters unchanged:', report['approved_masters_unchanged'], '| report', jp)
    ok = all(s['c14n_identical'] and s['byte_identical_outside_swapped_node'] for s in report['states']) and \
         (a.skip_check or (report['build_states_check']['guard_pass'] and report['build_states_check']['identical'] == len(SC['states'])))
    sys.exit(0 if ok else 1)

if __name__ == '__main__': main()
