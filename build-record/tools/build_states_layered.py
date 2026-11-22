#!/usr/bin/env python3
"""build_states_layered.py --config <states-config-layered.json> --outdir <dir>
LAYERED state masters for the Tetrasemaphore finals (2026-10-05; Science build sheet sections 5-8). Same sealed parts as
build_states.py / build_states_proposal.py (compose.py, the ring recipe, legend.js), assembled in a different layer order:

  field  ·  finalA5-rings  ·  finalA5-geometry  ·  finalA5-finish  [·  finalA5-litedge, build 6 (build 7: with the bow-tie guard): the lit edges, when the ring carries them]  (the UNCUT ring, all 24 keys)
         ·  one legend pair per language: legend-plaque-<lang> + legend-text-<lang>  ·  owl-placement (swapped for the mark later)

- field: one disc in the coin's own dark tint, the bottom layer; its edge lies under the outer coloured ring.
- The ring is uncut, so hiding the legend layers leaves a whole meander and another language's legend can be laid on it.
- Each language's plaque and lettering come from the sealed legend.js, run on a scratch copy and lifted out as two groups; every
  legend id gets the language suffix. Languages other than common.default_language are hidden (style display:none).
- A plaque laid straight onto an uncut ring leaves a lighter patch on the rails wherever a hidden key joins them (measured
  2026-10-05). So each plaque layer ends with its own WINDOW RAILS: the approved cut ring for that window (geometry + finish, its
  ids suffixed), clipped to the window sector and drawn over the plaque, which is the approved stacking (plaque, rails, lettering).
  Under the plaque goes a FLOOR in the coin's field tint, the exact channel sector between the rails: the plaque's rounded
  corners would otherwise leave gaps where the uncut ring's hidden keys show (two slivers per coin, found by the refuter).
  With the legend shown the coin renders as approved; with the legend layers hidden the whole meander shows.
- <title> per state; label 1 says centre mark; the 5a/5b labels record the keys covered and the typeface, size and tracking.
No sealed tool is edited. Prints the root child index of owl-placement (the notation generator's swapped_node_index).

Config switches added 2026-10-05 for build 3 (all default off: a config without them gives the same four SVGs byte for byte;
the JSON report gains lines):
- common.stamp = "cut-in" (Science build sheet section 15): the stamp is cut into the ring. The plate and its seams take the coin's
  field tint (legend.js --plaque <field>), and every depth effect is left out: the three clipped plaque-edge strokes, the cast
  shadow, the bevel, and the defs only they used (five blur filters, two gradients, two clip paths). Floor, window rails and the
  letters stay.
- common.edition = "owl" (section 14): the same packaging for the owl coins themselves; the title says Owl Semaphore and label 1 says owl.
- common.out_suffix: the word in the output file name (default "layered").
- state.mark_hex (optional): the colour of the notation centre mark where it is not the state colour (NORMATIVE: the Fix gold), so
  label 1 names the right colour. Without it label 1 names owl_hex, as before.
- With stamp = cut-in the rails label names the ring file by its path (the seam-fixed cut ring), not by its base name alone.
- An unknown key in "common" stops the build (a mistyped switch would otherwise build the old plaque silently).
- The report records, per legend, the ink's measured clearance to both rails and the plate left at both ends of the word, from the
  outlines; legend.js's own figure (cap height against the channel, capitals only, at its 0.0847 mm per print pixel) is kept
  under capitals_clearance_to_rails_mm_nominal.

Per-legend knobs added 2026-10-09 for build 5 (Science's CRÍTICO ruling C, Carey's choice; both default off: a legend without them is set
exactly as before, byte for byte):
- legend.<lang>.radial_shift_units: every glyph of that word moves this far outward (negative: inward) along its own radial line from the
  centre (410, 410); its rotation does not change. Science: 5.904 units (0.740 mm) for CRÍTICO, so the word is centred by its full height,
  accent included, instead of by its capitals.
- legend.<lang>.accent = {"glyph": i, "lift_units": u, "stroke_width": w}: the sub-contour(s) of glyph i that lie wholly above the cap line
  (local y < -cap/2) leave that glyph's path and become one path of their own at the end of the group, id legend-accent-<lang>, with the
  glyph's transform followed by translate(0 -u) (a lift along the letter's own up axis) and a round-joined stroke of width w in the letters'
  colour, so the mark prints at weight. Science: u 2.2338 (0.28 mm), w 1.6753 (0.21 mm). The report then measures the accent too:
  ink clearances include it with its stroke, and accent_* lines give its gap to the letter and its nominal thickness."""
import argparse, hashlib, json, os, re, shlex, subprocess, tempfile
import xml.etree.ElementTree as ET
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(D)
ap = argparse.ArgumentParser(); ap.add_argument('--config', required=True); ap.add_argument('--outdir', required=True); a = ap.parse_args()
C = json.load(open(a.config, encoding='utf-8')); common = C['common']; os.makedirs(a.outdir, exist_ok=True)
APPROVED_OWL, APPROVED_RING = '#B498E6', '#8C4191'   # colours carried by the owl source file (pre-legend approved master)
CUT_IN = common.get('stamp') == 'cut-in'; OWL = common.get('edition') == 'owl'; SUFFIX = common.get('out_suffix', 'layered')
assert common.get('stamp') in (None, 'cut-in') and common.get('edition') in (None, 'owl')
KNOWN = {'owl_source', 'ring', 'legend_knobs', 'legend_typeface', 'print_mm', 'field_r', 'languages', 'default_language', 'keys6', 'keys4', 'window_pad_deg', 'window_r', 'stamp', 'edition', 'out_suffix'}
assert set(common) <= KNOWN, f'unknown key(s) in common: {sorted(set(common) - KNOWN)}'
def sh(*x):
    r = subprocess.run(x, capture_output=True, text=True); assert r.returncode == 0, (x, r.stderr); return r.stdout
def sha16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def block(s, gid):
    """[start, end) of <g id="gid" ...>...</g> by depth-counting."""
    key = f'<g id="{gid}"'; assert s.count(key) == 1, (gid, s.count(key)); i = s.index(key); d = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        if m.group(0) == '</g>':
            d -= 1
            if d == 0: return i, i + m.end()
        else:
            gt = s.index('>', i + m.start())
            if s[gt - 1] != '/': d += 1
    raise ValueError('unbalanced ' + gid)

def window_rails(st, lang):
    """The approved CUT ring for this window (geometry + finish and the defs they use), ids suffixed, clipped to the window sector."""
    import math
    k = common[st['keys']]; c = open(k['ring_cut'], encoding='utf-8').read(); tag = f'-win-{lang}'
    d0, d1 = c.index('<defs>'), c.index('</defs>') + len('</defs>'); assert c.count('<defs>') == 1
    g0, g1 = block(c, 'finalA5-geometry'); f0, f1 = block(c, 'finalA5-finish')
    body = c[d0:d1] + '\n' + c[g0:g1] + '\n' + c[f0:f1]
    if '<g id="finalA5-litedge"' in c: l0, l1 = block(c, 'finalA5-litedge'); body += '\n' + c[l0:l1]     # build 6: the lit edges travel with the rails (build 7: the guarded layer, the same way)
    ids = set(re.findall(r'\bid="([^"]+)"', body))
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{m.group(1)}{tag}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{m.group(1)}{tag})' if m.group(1) in ids else m.group(0), body)
    body = re.sub(r'(xlink:href|href)="#([^"]+)"', lambda m: f'{m.group(1)}="#{m.group(2)}{tag}"' if m.group(2) in ids else m.group(0), body)
    body = re.sub(r' inkscape:groupmode="layer"', '', body)            # sub-groups of the plaque layer, not layers of their own
    a0, a1 = k['a0'] - common['window_pad_deg'], k['a1'] + common['window_pad_deg']; r0, r1 = common['window_r']
    XY = lambda a, r: f'{410 + r*math.cos(math.radians(a)):.3f} {410 + r*math.sin(math.radians(a)):.3f}'
    sector = f'M{XY(a0, r0)} A{r0} {r0} 0 0 1 {XY(a1, r0)} L{XY(a1, r1)} A{r1} {r1} 0 0 0 {XY(a0, r1)} Z'
    lab = (f'5a-rails window rails ({lang}): the approved cut ring {os.path.basename(k["ring_cut"])} clipped to {a0}-{a1} deg, r {r0}-{r1}, '
           f'drawn over the plaque so the rails beside the legend are the clean rails of the approved coin')
    if CUT_IN:
        lab = (f'5a-rails window rails ({lang}): the seam-fixed cut ring {k["ring_cut"]} clipped to {a0}-{a1} deg, r {r0}-{r1}, '
               f'drawn over the plate so the rails beside the legend are clean rails' + (' (with their lit edges, build 7)' if '<g id="finalA5-litedge"' in c else ''))
    return (f'<g id="legend-rails-{lang}" inkscape:label="{lab}"><defs><clipPath id="legend-window-clip-{lang}" clipPathUnits="userSpaceOnUse"><path d="{sector}"/></clipPath></defs>'
            f'<g clip-path="url(#legend-window-clip-{lang})">\n{body}\n</g></g>')

def ink_extents(glyphs_group):
    """(r_min, r_max, angle_min, angle_max) of the letters' ink in slot units / degrees, from the outlines (quadratic and cubic curves sampled)."""
    import math
    rs, angs = [], []
    for pid, tf, d, sw in re.findall(r'<path(?: id="([^"]*)")? transform="([^"]*)" d="([^"]*)"(?: stroke="#DEC875" stroke-width="([\d.]+)" stroke-linejoin="round")?/>', glyphs_group):
        m = re.fullmatch(r'translate\((-?[\d.]+) (-?[\d.]+)\) rotate\((-?[\d.]+)\)(?: translate\(0 (-?[\d.]+)\))?', tf); assert m, tf
        tx, ty, rot = float(m.group(1)), float(m.group(2)), math.radians(float(m.group(3))); co, si = math.cos(rot), math.sin(rot)
        dy = float(m.group(4) or 0); half = float(sw) / 2 if sw else 0.0
        tok = re.findall(r'[MLQCZ]|-?\d+\.?\d*', d); i = 0; cur = (0.0, 0.0); pts = []; cmd = None
        while i < len(tok):
            if tok[i].isalpha(): cmd = tok[i]; i += 1
            if cmd == 'Z': continue
            n = {'M': 1, 'L': 1, 'Q': 2, 'C': 3}[cmd]; q = [(float(tok[i + 2*j]), float(tok[i + 2*j + 1])) for j in range(n)]; i += 2*n
            if n == 1: pts.append(q[0])
            else:
                ctrl = [cur] + q
                for t in (u/24 for u in range(1, 25)):
                    b = ctrl
                    while len(b) > 1: b = [((1 - t)*b[j][0] + t*b[j + 1][0], (1 - t)*b[j][1] + t*b[j + 1][1]) for j in range(len(b) - 1)]
                    pts.append(b[0])
            cur = q[-1]
        for x, y in pts:
            y = y + dy; X, Y = tx + co*x - si*y - 410, ty + si*x + co*y - 410; R = math.hypot(X, Y); A = math.degrees(math.atan2(Y, X))
            rs += [R - half, R + half]; angs += [A - math.degrees(half / R), A + math.degrees(half / R)]   # a stroked path reaches half its width further
    return min(rs), max(rs), min(angs), max(angs)

def cut_in(plaque, text):
    """Sheet section 15: no depth effects. From the legend.js groups drop the three clipped plaque-edge strokes, the cast shadow, the bevel,
    and the defs only they used. What is left: the seams and the plate (already in the field tint) and the letters."""
    for part in (plaque, text): assert part.count('<defs>') == 1 and part.count('</defs>\n') == 1
    plaque = plaque[:plaque.index('<defs>')] + plaque[plaque.index('</defs>\n') + len('</defs>\n'):]
    plaque, n = re.subn(r'<g clip-path="url\(#legend-plaque-clip\)">.*?</g>\n', '', plaque, count=1, flags=re.S); assert n == 1
    text = text[:text.index('<defs>')] + text[text.index('</defs>\n') + len('</defs>\n'):]
    for gid in ('legend-cast-shadow', 'legend-bevel'):
        b0, b1 = block(text, gid); assert text[b1] == '\n'; text = text[:b0] + text[b1 + 1:]
    for part in (plaque, text): assert not re.search(r'filter|Gradient|clip|<defs|stroke|opacity', part), re.search(r'filter|Gradient|clip|<defs|stroke|opacity', part)
    assert plaque.count('<path') == 2 and text.count('<g ') == 2 and text.count('</g>') == 2
    return plaque, text

GLYPH = re.compile(r'<path transform="translate\((-?[\d.]+) (-?[\d.]+)\) rotate\((-?[\d.]+)\)" d="([^"]*)"/>')
def num(x):
    """legend.js's number format: round to 3 decimals, drop trailing zeros."""
    t = f'{x:.3f}'.rstrip('0').rstrip('.'); return '0' if t in ('', '-0') else t
def contours(d):
    """Split a legend.js path (absolute M L Q C Z; a negative number may follow the previous one with no space) into its closed
    sub-contours, each with its list of coordinate pairs (control points included)."""
    parts = [c + 'Z' for c in d.split('Z') if c.strip()]; out = []
    for c in parts:
        nums = [float(t) for t in re.findall(r'-?\d+\.?\d*', c)]; assert len(nums) % 2 == 0, c
        pts = list(zip(nums[0::2], nums[1::2])); assert pts, c; out.append((c, pts))
    return out
def set_word(group, L, lang, cap_slot, mmu):
    """Build 5 knobs (see the module doc): radial shift of every glyph, and the accent split into its own stroked path. Returns the new
    group text and the accent facts (None when there is no accent knob)."""
    import math
    paths = GLYPH.findall(group); assert group.count('<path') == len(paths), 'unexpected element in the glyph group'
    shift = float(L.get('radial_shift_units', 0) or 0); acc = L.get('accent'); out = []; accent_path = ''; facts = None
    for i, (tx, ty, rot, d) in enumerate(paths):
        x, y = float(tx), float(ty)
        if shift:
            r = math.hypot(x - 410, y - 410); x, y = 410 + (x - 410) * (r + shift) / r, 410 + (y - 410) * (r + shift) / r
        tr = f'translate({num(x)} {num(y)}) rotate({rot})'
        if acc and i == acc['glyph']:
            cs = contours(d); above = [c for c, pts in cs if all(py < -cap_slot / 2 for px, py in pts)]; rest = [c for c, pts in cs if c not in above]
            assert len(above) == 1 and rest, (len(above), len(rest))
            u, w = float(acc['lift_units']), float(acc['stroke_width']); apts = [p for c, pts in cs if c in above for p in pts]
            num4 = lambda v: (f'{v:.4f}'.rstrip('0').rstrip('.'))                                     # the knob values as Science gave them
            accent_path = (f'<path id="legend-accent-{lang}" transform="{tr} translate(0 {num4(-u)})" d="{"".join(above)}" '
                           f'stroke="#DEC875" stroke-width="{num4(w)}" stroke-linejoin="round"/>')
            top_of_letter = min(py for c, pts in cs if c in rest for px, py in pts)                      # the stem's top edge (local y, up is negative)
            gap = top_of_letter - (max(py for px, py in apts) - u + w / 2)                               # from the stroked accent's lowest point to the stem
            xs = [px for px, py in apts]; ys = [py for px, py in apts]
            # nominal thickness of the acute across its slant: the outline's area over the length of its longest edge, plus the stroke
            # (half of it each side). The print-weight figure is measured on the render by the refuters; this is the outline's own number.
            area = abs(sum(apts[j][0] * apts[(j + 1) % len(apts)][1] - apts[(j + 1) % len(apts)][0] * apts[j][1] for j in range(len(apts)))) / 2
            edge = max(math.hypot(apts[j][0] - apts[(j + 1) % len(apts)][0], apts[j][1] - apts[(j + 1) % len(apts)][1]) for j in range(len(apts)))
            facts = dict(accent_glyph=acc['glyph'], accent_lift_units=u, accent_stroke_units=w, accent_to_letter_mm=round(gap * mmu, 3),
                         accent_thickness_mm_nominal=round((area / edge + w) * mmu, 3), accent_height_units=round(max(ys) - min(ys), 3))
            d = ''.join(rest)
        out.append(f'<path transform="{tr}" d="{d}"/>')
    head = group[:group.index('>') + 1]; assert group.endswith('</g>')
    return head + ''.join(out) + accent_path + '</g>', facts

def legend_pair(base_svg, st, lang, work):
    """Run the sealed legend.js for one language on a scratch copy; return (plaque_group, text_group, facts)."""
    L = st['legend'][lang]; k = common[st['keys']]; out = os.path.join(work, f'{st["name"]}-{lang}.svg')
    knobs = shlex.split(common['legend_knobs'])
    if CUT_IN: i = knobs.index('--plaque'); knobs[i + 1] = st['field_hex']      # the plate is the coin's own field
    info = json.loads(sh('node', 'tools/legend.js', base_svg, out, '--word', L['word'], '--a0', str(k['a0']), '--a1', str(k['a1']),
                         '--track', str(L['track']), *knobs))
    s = open(out, encoding='utf-8').read()
    p0, p1 = block(s, 'legend-plaque'); plaque = s[p0:p1]
    t0, t1 = block(s, 'legend-text'); text = s[t0:t1]
    text = re.sub(r'<path transform="[^"]*" d=""/>', '', text); plaque = re.sub(r'<path transform="[^"]*" d=""/>', '', plaque)   # a space has no outline
    if CUT_IN: plaque, text = cut_in(plaque, text)
    suffix = lambda b: re.sub(r'(id="|url\(#)(legend-[a-z-]+)', lambda m: f'{m.group(1)}{m.group(2)}-{lang}', b)
    plaque, text = suffix(plaque), suffix(text)
    accent_facts = None
    if L.get('radial_shift_units') or L.get('accent'):
        g0, g1 = block(text, f'legend-glyphs-{lang}'); new, accent_facts = set_word(text[g0:g1], L, lang, info['cap_slot_px'], common['print_mm'] / 820)
        text = text[:g0] + new + text[g1:]
    import math
    r0, r1 = info['rIn'] - 1.0, info['rOut'] + 1.0    # one unit under each rail, like the plaque's own seam strip; the window rails cover it
    XY = lambda a_, r: f'{410 + r*math.cos(math.radians(a_)):.3f} {410 + r*math.sin(math.radians(a_)):.3f}'
    floor = (f'<path id="legend-floor-{lang}" d="M{XY(k["a0"], r0)} A{r0:.3f} {r0:.3f} 0 0 1 {XY(k["a1"], r0)} L{XY(k["a1"], r1)} A{r1:.3f} {r1:.3f} 0 0 0 {XY(k["a0"], r1)} Z" fill="{st["field_hex"]}"/>\n')
    key = f'<path id="legend-plaque-seams-{lang}"'; assert plaque.count(key) == 1; plaque = plaque.replace(key, floor + key)
    assert plaque.rstrip().endswith('</g>'); plaque = plaque.rstrip()[:-len('</g>')] + window_rails(st, lang) + '\n</g>'
    hide = '' if lang == common['default_language'] else ' style="display:none"'
    lab5a = (f'5a legend plaque ({lang}): inlaid channel on the uncut ring, over keys {k["keys"]} ({k["a0"]}-{k["a1"]} deg): a floor in the field tint, the plaque, then its window rails on top; '
             f'fill {re.search(r"--plaque (#[0-9A-Fa-f]{6})", common["legend_knobs"]).group(1)}')
    if CUT_IN:
        lab5a = (f'5a legend plate ({lang}): the stamp cut into the uncut ring, over keys {k["keys"]} ({k["a0"]}-{k["a1"]} deg): floor, seams and plate all in the field tint '
                 f'{st["field_hex"]}, the same dark as the gaps of the meander; no edge strokes, no shadow; then its window rails on top')
    plaque, n = re.subn(r'(<g id="legend-plaque-%s" inkscape:groupmode="layer") inkscape:label="[^"]*"' % lang, lambda m: f'{m.group(1)} inkscape:label="{lab5a}"{hide}', plaque, count=1); assert n == 1
    pt = info['fontSize_slot'] * common['print_mm'] / 820 / 25.4 * 72
    lab5b = (f'5b legend ({lang}) {L["word"]}: {common["legend_typeface"]}, as outlines; cap height {info["cap_mm"]} mm on the channel mid-radius, '
             f'font size {info["fontSize_slot"]} slot units = {pt:.1f} pt at {common["print_mm"]} mm, tracking {L["track"]}; fill #DEC875, ring bevel recipe'
             + (f'; {L["status"]}' if L.get('status') else ''))
    if CUT_IN: assert lab5b.count('ring bevel recipe') == 1; lab5b = lab5b.replace('ring bevel recipe', 'flat: no cast shadow, no bevel')
    assert '"' not in lab5b and '"' not in lab5a
    text, n = re.subn(r'(<g id="legend-text-%s" inkscape:groupmode="layer") inkscape:label="[^"]*"' % lang, lambda m: f'{m.group(1)} inkscape:label="{lab5b}"{hide}', text, count=1); assert n == 1
    g0, g1 = block(text, f'legend-glyphs-{lang}'); rmin, rmax, amin, amax = ink_extents(text[g0:g1]); mmu = common['print_mm'] / 820
    facts = dict(lang=lang, word=L['word'], track=L['track'], word_span_deg=info['word_span_deg'], margin_each_deg=info['margin_each_deg'],
                 margin_each_mm=info['margin_each_mm'], cap_mm=info['cap_mm'], font_size_slot=info['fontSize_slot'], font_size_pt=round(pt, 2),
                 capitals_clearance_to_rails_mm_nominal=info.get('clearance_to_rails_mm'),
                 ink_clearance_inner_rail_mm=round((rmin - info['rIn'])*mmu, 3), ink_clearance_outer_rail_mm=round((info['rOut'] - rmax)*mmu, 3),
                 ink_gap_to_window_end_deg=[round(k['a1'] - amax, 3), round(amin - k['a0'], 3)],
                 ink_note='measured on the outlines at print_mm; the first gap is before the first letter, the second after the last; margin_each_* is the advance box, which is what the spacing rule centres',
                 hidden=bool(hide))
    if L.get('radial_shift_units'): facts['radial_shift_units'] = float(L['radial_shift_units']); facts['radial_shift_mm'] = round(float(L['radial_shift_units']) * mmu, 3)
    if accent_facts: facts.update(accent_facts)
    return plaque, text, facts

def build(st, out, work):
    tmp = os.path.join(work, st['name'] + '.composed.svg')
    sh('python3', 'tools/compose.py', common['ring'], common['owl_source'], tmp)
    s = open(tmp, encoding='utf-8').read()
    assert s.count(f'fill="{APPROVED_OWL}"') == 2; s = s.replace(f'fill="{APPROVED_OWL}"', f'fill="{st["owl_hex"]}"')
    m = re.search(r'(<g id="finalA5-rings"[^>]*>)(.*?)(</g>)', s, re.S); head, inner = m.group(1), m.group(2)
    assert inner.count(f'stroke="{APPROVED_RING}"') == 2
    head = re.sub(r'inkscape:label="1 [^"]*"', f'inkscape:label="1 {st["name"]} rings {st["ring_hex"]} (state colour; {"owl" if OWL else "centre mark"} {st["owl_hex"] if OWL else st.get("mark_hex", st["owl_hex"])})"', head)
    s = s[:m.start()] + head + inner.replace(f'stroke="{APPROVED_RING}"', f'stroke="{st["ring_hex"]}"') + m.group(3) + s[m.end():]
    if st.get('operator'):
        old = re.search(r'<g id="owl-placement" inkscape:label="[^"]*" transform="([^"]*)">', s); assert old
        s = s[:old.start()] + f'<g id="owl-placement" inkscape:label="4a owl placement: V4 operator for {st["name"]} about the medallion centre (410,410), then the approved placement" transform="{st["operator"]} {old.group(1)}">' + s[old.end():]
    assert APPROVED_RING not in s
    t = re.findall(r'<title>.*?</title>', s, re.S); assert len(t) == 1
    s = s.replace(t[0], f'<title>{"Owl Semaphore" if OWL else "Tetrasemaphore"} {st["name"]} medallion — layered vector master (field + rings + uncut meander with glints + legends {" / ".join(common["languages"])} + {"owl" if OWL else "centre mark"}), slot820</title>')
    open(tmp, 'w', encoding='utf-8').write(s)
    pairs, facts = [], []
    for lang in common['languages']:
        p, t_, f = legend_pair(tmp, st, lang, work); pairs += [p, t_]; facts.append(f)
    ri = s.index('<g id="finalA5-rings"'); oi = s.index('<g id="owl-placement"')
    assert s[oi - 1] == '\n'
    fl = (f'0 field: {st["name"]} tint {st["field_hex"]}, the dark ground the colours were chosen against (one lightness and one chroma for all four coins, '
          f'hue from the coin colour); a disc to r {common["field_r"]}, its edge under the outer ring; outside the coin stays transparent')
    field = f'<g id="field" inkscape:groupmode="layer" inkscape:label="{fl}"><circle cx="410" cy="410" r="{common["field_r"]}" fill="{st["field_hex"]}"/></g>\n'
    s = s[:ri] + field + s[ri:oi] + '\n'.join(pairs) + '\n' + s[oi:]
    open(out, 'w', encoding='utf-8', newline='').write(s)
    root = ET.parse(out).getroot(); kids = [c.get('id') or c.tag.split('}')[-1] for c in root]
    want = ['field', 'finalA5-rings', 'finalA5-geometry', 'finalA5-finish'] + (['finalA5-litedge'] if '<g id="finalA5-litedge"' in s else []) + [f'legend-{k}-{l}' for l in common['languages'] for k in ('plaque', 'text')] + ['owl-placement']
    assert kids[-len(want):] == want, kids
    ids = [e.get('id') for e in root.iter() if e.get('id')]; assert len(ids) == len(set(ids)), 'duplicate ids'
    return dict(name=st['name'], out=out, sha16=sha16(out), root_children=kids, owl_index=kids.index('owl-placement'), legends=facts)

work = tempfile.mkdtemp(prefix='layered-')
report = dict(config=os.path.abspath(a.config), stamp=common.get('stamp', 'plaque with depth effects (legend.js as sealed)'), edition=common.get('edition', 'notation base'), ring=common['ring'], ring_sha16=sha16(common['ring']), owl_source=common['owl_source'],
              owl_source_sha16=sha16(common['owl_source']), states=[])
for st in C['states']:
    r = build(st, os.path.join(a.outdir, f'MASTER-medallion-{st["name"]}-{SUFFIX}-slot820.svg'), work); report['states'].append(r)
    print(r['name'], r['sha16'], 'owl-placement is root child', r['owl_index'], '|', '; '.join(f'{f["lang"]} {f["word"]} track {f["track"]} span {f["word_span_deg"]} margin {f["margin_each_deg"]} deg' for f in r['legends']))
json.dump(report, open(os.path.join(a.outdir, 'layered-build.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
