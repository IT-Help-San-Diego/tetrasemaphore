#!/usr/bin/env python3
"""
make_anatomy_plate.py — build one semaphore DATASHEET for the Tetrasemaphore site.

MOCK-UP for review: design work for site version 1.1. It reads the published
v1.0.0 tree and writes nothing back to it.

The honesty rule this script carries:
  every number, value, tick and label on the sheet is read out of the semaphore's
  master SVG, out of the measurement record generated from it, or quoted from the
  published note (README.md at v1.0.0), and each one carries its source
  (file + sha16 + the field or line it came from) into its callouts JSON.
  Two kinds of mark are drawn that are not data, and the footnote names both:
  the drafting marks (leader lines, number badges, caption boxes, the centre
  axis, the direction arrow, the detail frame), and the field plate's edge,
  stroked at the disc's own measured radius so a dark disc is visible on a sheet
  of the same dark colour.

One template, four instances: --state NORMATIVE | NON-NORMATIVE | METACOGNITIVE
| CRITICAL. The four differ in ways the template reads from the files rather
than assuming: the gold Fix element is the whole mark (I), a vertical bar (σᵥ),
a horizontal bar (σₕ) or a dot (C₂); NORMATIVE carries no separate Fix layer and
CRITICAL no symmetry-mark layer, so those two sheets have six stations instead
of seven and a short note in the vacated slot says what is absent and why.

Landed in the repository for version 1.1, step 1 (Claude Code, 7 November 2026): the
fonts travel with the toolchain (tools/fonts), SOURCE_DATE_EPOCH pins the clock, and
tools/build_datasheets.py stages the inputs from the checkout into ./src and runs the
four states. The drawing code is unchanged from the 23 October 2026 build.
"""
import argparse, hashlib, io, json, math, os, re, sys, datetime
import xml.etree.ElementTree as ET
import cairosvg
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont


def citation_clause():
    """The footer's parenthesis after the tag: the commit and the DOI when they are known, in
    the 1.0.0 form; either alone when only one is; nothing when neither is (never a placeholder)."""
    parts = [p for p in (('commit ' + RELEASE['commit'][:12]) if RELEASE['commit'] else '',
                         ('Zenodo ' + RELEASE['doi']) if RELEASE['doi'] else '') if p]
    return '(' + ', '.join(parts) + '), ' if parts else ''


def build_time():
    """The build's clock. SOURCE_DATE_EPOCH (seconds since the epoch, UTC), when set,
    makes a build reproducible byte for byte; otherwise the time of the run."""
    e = os.environ.get('SOURCE_DATE_EPOCH')
    if e:
        return datetime.datetime.fromtimestamp(int(e), datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)

# ----------------------------------------------------------------- inputs ---
# All copied out of the published tree into ./src by the caller (tools/build_datasheets.py).
# The release the sheets cite and the staged file names are parameters: the environment
# variables below (set by the build driver, read by anything that imports this file, the
# punctuation test included) and the command line (which overrides them). The defaults are
# the 1.0.0 citation. An empty commit means the footer and the audit name no commit: the
# sheets of a release are built before that release's commit exists.
SRC = 'src'
MASTER_DIR = os.path.join(SRC, 'masters')
RELEASE = dict(tag=os.environ.get('DATASHEET_RELEASE_TAG', 'v1.0.0'),
               commit=os.environ.get('DATASHEET_RELEASE_COMMIT', '833c2438fc3e679096816abafead62f83e1aa944'),
               doi=os.environ.get('DATASHEET_RELEASE_DOI', '10.5281/zenodo.23575816'))
NOTE = os.path.join(SRC, os.environ.get('DATASHEET_NOTE_FILE', f"README-{RELEASE['tag']}.md"))
MEASJSON = os.path.join(SRC, 'notation-measurements.json')
LEANFILE = os.path.join(SRC, os.environ.get('DATASHEET_LEAN_FILE', f"TetrasemaphoreAlgebra-{RELEASE['tag']}.lean"))
SITE_DIR = os.path.join(SRC, 'site')

# The fonts travel with the toolchain: tools/fonts, DejaVu Sans 2.37, DejaVu Sans Mono 2.37
# and DejaVu Sans Bold 2.34, the files the 23 October 2026 sheets were set in
# (licence: tools/fonts/LICENSE-DejaVu.txt).
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
F_SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

NS = {'svg': 'http://www.w3.org/2000/svg'}
IK = '{http://www.inkscape.org/namespaces/inkscape}label'

# ---- the drafting style, shared by all four sheets -------------------------
# DRAFT_C was chosen by measurement, not taste: of every candidate clearing
# 4.5:1 on all four grounds, it is the one whose smallest CIEDE2000 difference
# from any colour in the four semaphores' art, and from any text colour, is
# largest (choose_drafting_colour.py). It appears in none of the art.
# Version 5: Carey chose ice blue on 23 October 2026 from a preview. Science's
# check of the version-4 green found it turning pale gold under simulated
# dichromacy, close to the art's gold; ice blue holds its distance in every view
# (choose_drafting_colour.py, Machado 2009 and Vienot 1999, both models).
DRAFT_C = '#C3E6FF'
DRAFT_NAME = 'ice blue'
GOLD = '#DEC875'        # legend lettering fill
GOLD2 = '#C7B469'       # the Fix gold
HI = '#F2E4B8'          # lit-edge highlight cap, used for body text
CONTRAST_FLOOR = 4.5    # WCAG 2.1 AA for normal-size text; the build stops below it
CANVAS = (2400, 1500)
M = 44

NOTA = {'NORMATIVE': ('I', None), 'NON-NORMATIVE': ('\u03c3', 'v'),
        'METACOGNITIVE': ('\u03c3', 'h'), 'CRITICAL': ('C', '2')}
SUB = {'h': '\u2095', 'v': '\u1d65', '2': '\u2082', None: ''}
TWIN = {'METACOGNITIVE': 'NON-NORMATIVE', 'NON-NORMATIVE': 'METACOGNITIVE',
        'NORMATIVE': None, 'CRITICAL': None}
OWN_MOVE = {'NORMATIVE': ('sigma_h', 'sigma_v', 'c2'), 'NON-NORMATIVE': ('sigma_v',),
            'METACOGNITIVE': ('sigma_h',), 'CRITICAL': ('c2',)}


def sha(path, n=None):
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    return h[:n] if n else h


def rgba(hx, a=255):
    return (int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16), int(a))


def contrast(fg, bg):
    def lum(hx):
        c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    a, b = lum(fg), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


# ----------------------------------------------------------- master reader ---
class Master:
    TOP = ['field', 'finalA5-rings', 'finalA5-geometry', 'finalA5-finish', 'finalA5-litedge',
           'legend-plaque-en', 'legend-text-en', 'legend-plaque-es', 'legend-text-es',
           'glyph-placement', 'symmetry-marks']

    def __init__(self, state):
        self.state = state
        self.path = os.path.join(MASTER_DIR, f"MASTER-medallion-{state}-notation-slot820.svg")
        self.sha256 = sha(self.path)
        self.sha16 = self.sha256[:16]
        self.root = ET.parse(self.path).getroot()
        self.desc = (self.root.find('svg:desc', NS).text or '').strip()
        self.labels = {g.get('id'): g.get(IK) for g in self.root
                       if g.tag.endswith('}g') and g.get(IK)}
        f = self.root.find("./svg:g[@id='field']/svg:circle", NS)
        self.field = dict(fill=f.get('fill'), r=float(f.get('r')),
                          cx=float(f.get('cx')), cy=float(f.get('cy')))
        self.rings = [dict(r=float(c.get('r')), stroke=c.get('stroke'),
                           w=float(c.get('stroke-width')))
                      for c in self.root.findall("./svg:g[@id='finalA5-rings']/svg:circle", NS)]
        self.colour = self.rings[0]['stroke']
        gp = self.root.find("./svg:g[@id='glyph-placement']", NS)
        self.glyph_label = gp.get(IK) or ''
        self.glyph_transform = gp.get('transform')
        self.glyph_scale = float(self.glyph_transform.split('scale(')[1].split(')')[0])
        _tr = [p.split(')')[0] for p in self.glyph_transform.split('translate(')[1:]]
        self._t0, self._t1 = [tuple(float(v) for v in t.replace(',', ' ').split()) for t in _tr]
        gb = gp.find("./svg:g[@id='glyph-body']", NS)
        self.glyph_fill = gb.get('fill')
        self.glyph_body_label = gb.get(IK) or ''
        fx = gp.find("./svg:rect[@id='glyph-fix']", NS)
        if fx is None:                      # a childless Element is falsy: test `is None`
            fx = gp.find("./svg:circle[@id='glyph-fix']", NS)
        self.fix = None
        if fx is not None:
            self.fix = dict(kind=fx.tag.split('}')[-1], fill=fx.get('fill'),
                            label=fx.get(IK) or '',
                            **{k: float(v) for k, v in fx.attrib.items()
                               if k in ('x', 'y', 'width', 'height', 'cx', 'cy', 'r')})
        sm = self.root.find("./svg:g[@id='symmetry-marks']", NS)
        self.marks, self.marks_fill, self.marks_label = [], None, ''
        if sm is not None:
            self.marks_fill = sm.get('fill')
            self.marks_label = sm.get(IK) or ''
            self.marks = [{k: float(v) for k, v in c.attrib.items()
                           if k in ('x', 'y', 'width', 'height')} for c in sm]
        self.litedge_n = len(self.root.findall("./svg:g[@id='finalA5-litedge']/svg:g", NS))
        lt = self.root.find("./svg:g[@id='legend-text-en']/svg:g", NS)
        self.legend_fill = lt.get('fill') if lt is not None else None
        # mm scale, derived from the master's own statement of the bars in both
        # slot units and mm; the three states that carry bars all state 4.0 x 0.9 mm
        self.u_per_mm = 31.911 / 4.0
        self.scale_note = ("g#symmetry-marks label gives the bar as 31.911 x 7.18 slot units "
                           "and as 4.0 x 0.9 mm")
        if self.marks:
            self.u_per_mm = max(self.marks[0]['width'], self.marks[0]['height']) / 4.0
        self.print_mm = 820.0 / self.u_per_mm

    def mm(self, u, nd=3):
        return round(u / self.u_per_mm, nd)

    def to_slot(self, x, y):
        s = self.glyph_scale
        return (self._t0[0] + s * (x + self._t1[0]), self._t0[1] + s * (y + self._t1[1]))

    def render(self, visible, px, hide_fix=False, only_fix=False, field_edge=False):
        r = ET.parse(self.path).getroot()
        for gid in self.TOP:
            g = r.find(f"./svg:g[@id='{gid}']", NS)
            if g is None:
                continue
            if gid not in visible:
                g.set('style', 'display:none')
            else:
                g.set('style', (g.get('style', '') or '').replace('display:none', '').strip('; '))
        if 'glyph-placement' in visible:
            gp = r.find("./svg:g[@id='glyph-placement']", NS)
            gb = gp.find("./svg:g[@id='glyph-body']", NS)
            gf = gp.find("./svg:rect[@id='glyph-fix']", NS)
            if gf is None:
                gf = gp.find("./svg:circle[@id='glyph-fix']", NS)
            if hide_fix and gf is not None:
                gf.set('style', 'display:none')
            if only_fix and gb is not None:
                gb.set('style', 'display:none')
        png = cairosvg.svg2png(bytestring=ET.tostring(r, encoding='utf-8'),
                               output_width=px, output_height=px)
        im = Image.open(io.BytesIO(png)).convert('RGBA')
        if field_edge:
            d = ImageDraw.Draw(im)
            k = px / 820.0
            rr, cx, cy = self.field['r'] * k, self.field['cx'] * k, self.field['cy'] * k
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      outline=rgba(self.colour, 150), width=max(2, int(round(px / 220))))
        return im


# --------------------------------------------------------------- text kit ---
class Draft:
    """Every drafting mark: a core stroke in the drafting colour over a halo in
    the sheet's own ground, so the mark separates from whatever it crosses.
    Marks are collected and drawn last, haloes first, then cores."""
    HALO = 4          # px at 2400 wide, so 2 px at the 1200 px preview
    # the window and frame cores sit above the widest median art line measured in
    # the window region on any of the four sheets (8.0 px, CRITICAL)
    W_WINDOW, W_BRACKET, W_FRAME, W_LEADER, W_RULE, W_AXIS = 9, 9, 9, 3, 4, 2

    CLEAR_OF_ART = 3     # px at 2400 wide: the axis stops this far short of a part

    def __init__(self, colour, ground):
        self.c, self.g, self.ops, self.axis_ops = colour, ground, [], []

    def axis(self, pts, w):
        self.axis_ops.append(('line', [tuple(q) for q in pts], w))

    def line(self, pts, w):
        self.ops.append(('line', [tuple(q) for q in pts], w))

    def rect(self, box, w):
        self.ops.append(('rect', list(box), w))

    def poly(self, pts, w):
        self.ops.append(('poly', [tuple(q) for q in pts], w))

    def disc(self, xy, r):
        self.ops.append(('disc', list(xy), r))

    def brackets(self, box, length, w):
        x0, y0, x1, y1 = box
        for sx, x in ((1, x0), (-1, x1)):
            for sy, y in ((1, y0), (-1, y1)):
                self.line([(x - sx * length, y), (x, y)], w)
                self.line([(x, y - sy * length), (x, y)], w)

    def flush(self, dr):
        for core in (False, True):
            col, pad = (self.c, 0) if core else (self.g, self.HALO)
            for kind, a, w in self.ops:
                if kind == 'line':
                    dr.line(a, fill=col, width=int(w + 2 * pad), joint='curve')
                elif kind == 'poly':
                    dr.polygon(a, fill=col) if core else dr.polygon(
                        [(x + (pad if i else -pad), y + (pad if i else -pad))
                         for i, (x, y) in enumerate(a)], fill=col)
                    if not core:
                        dr.line(a + [a[0]], fill=col, width=int(2 * pad), joint='curve')
                elif kind == 'rect':
                    b = [a[0] - pad, a[1] - pad, a[2] + pad, a[3] + pad]
                    dr.rectangle(b, outline=col, width=int(w + 2 * pad))
                elif kind == 'disc':
                    r = w + pad          # the radius travels in w, not in a
                    dr.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], fill=col)


class Text:
    def __init__(self, draw):
        self.d = draw
        self.boxes = []
        self._f = {}

    def font(self, path, size):
        k = (path, size)
        if k not in self._f:
            # the basic layout engine, explicitly: Raqm shaping (on whenever a libfribidi is
            # loadable) changes every width and line break; see tools/datasheets-environment/README.md
            self._f[k] = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.BASIC)
        return self._f[k]

    def width(self, s, path, size):
        return self.d.textlength(s, font=self.font(path, size))

    def draw(self, xy, s, path, size, fill, tag='', anchor='la'):
        if not s:
            return 0
        f = self.font(path, size)
        self.d.text(xy, s, font=f, fill=fill, anchor=anchor)
        self.boxes.append((tag, s, self.d.textbbox(xy, s, font=f, anchor=anchor)))
        return size

    def wrap(self, s, path, size, maxw):
        lines, cur = [], ''
        for w in s.split():
            t = (cur + ' ' + w).strip()
            if self.width(t, path, size) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def para(self, xy, s, path, size, fill, maxw, lh, tag=''):
        x, y = xy
        for ln in self.wrap(s, path, size, maxw):
            self.draw((x, y), ln, path, size, fill, tag)
            y += lh
        return y


# ----------------------------------------------------------- source kit ----
class Sources:
    """Quotes are looked up in the published note before anything is drawn;
    Lean names are looked up in the published proof file."""

    def __init__(self, master):
        self.master = master
        raw = open(NOTE, encoding='utf-8').read()
        self.note_sha256 = sha(NOTE)
        self.note_sha16 = self.note_sha256[:16]
        self.note_flat = ' '.join(raw.replace('**', '').split())
        self.meas = json.load(open(MEASJSON))
        self.meas_sha16 = sha(MEASJSON, 16)
        self.lean = open(LEANFILE, encoding='utf-8').read()
        self.lean_sha16 = sha(LEANFILE, 16)
        self.verified, self.failed = [], []

    def m(self, field):
        return dict(source=os.path.basename(self.master.path), sha16=self.master.sha16,
                    field=field)

    def q(self, text, lines, kind='quote'):
        """Looks the exact string up in the published note. `kind` records how the
        sheet presents it: a quotation, or a pointer whose wording is ours."""
        flat = ' '.join(text.split())
        if flat not in self.note_flat:
            self.failed.append(('note', flat[:70]))
            raise AssertionError(f"string not in the published note: {flat[:90]!r}")
        self.verified.append(('note', kind, flat[:60]))
        return dict(source='README.md at ' + RELEASE['tag'], sha16=self.note_sha16,
                    field=f"lines {lines}", kind=kind)

    def j(self, field):
        return dict(source=os.path.basename(MEASJSON), sha16=self.meas_sha16, field=field)

    def thm(self, name):
        if not re.search(rf'^\s*(theorem|lemma)\s+{re.escape(name)}\b', self.lean, re.M):
            self.failed.append(('lean', name))
            raise AssertionError(f"theorem not in the published proof file: {name}")
        self.verified.append(('lean', 'declaration', name))
        return dict(source='proofs/TetrasemaphoreAlgebra.lean at ' + RELEASE['tag'],
                    sha16=self.lean_sha16, field=name)

    QMARKS = '\u201c\u201d'
    TERMINALS = '.,;:!?'

    def quotation_punctuation(self, display):
        """Every span the sheet wraps in typographic quotes is checked against the
        note: a span that ends in punctuation claims the note has that mark at
        that point, and a span that ends in an ellipsis claims nothing. Returns
        (spans_checked, faults)."""
        spans = re.findall('\u201c(.+?)\u201d', display, re.S)
        faults = []
        for span in spans:
            body = ' '.join(span.split())
            claim = None
            if body.endswith('\u2026'):
                body = body[:-1].rstrip()
            elif body and body[-1] in self.TERMINALS:
                claim, body = body[-1], body[:-1].rstrip()
            core = ' '.join(body.split('\u2026')[-1].split()).lstrip()
            if not core:
                continue
            at = self.note_flat.find(core)
            if at < 0:
                faults.append(dict(span=span[:70], fault='span not found in the note',
                                   claimed=claim, source_has=None))
                continue
            nxt = self.note_flat[at + len(core):at + len(core) + 1]
            if claim is not None and nxt != claim:
                faults.append(dict(span=span[:70],
                                   fault='quotation ends in punctuation the note does not '
                                         'have at that point',
                                   claimed=claim, source_has=nxt))
        return len(spans), faults

    def ms(self, state=None):
        st = state or self.master.state
        return next(s for s in self.meas['states'] if s['name'] == st)


# ------------------------------------------------- the note's own sentences --
# Each entry is (text, line range in README.md at v1.0.0, sha c98c3ee4a94a3dae).
STANDFIRST = {
    'NORMATIVE': ("NORMATIVE keeps its stance and looks at its object: what has been tested and "
                  "holds, for now.", "12\u201313"),
    'NON-NORMATIVE': ("NON-NORMATIVE mirrors its stance and looks at its object: exploration that "
                      "stands alongside the standard without claiming to replace it.", "13\u201314"),
    'METACOGNITIVE': ("METACOGNITIVE keeps its stance but turns its look back to its own frame, "
                      "the way you can keep your feet planted and look back between your legs; "
                      "this is thinking about thinking.", "14\u201315"),
    'CRITICAL': ("CRITICAL does both at once: it turns over the framework a claim rests on, "
                 "treating every baseline assumption as possibly wrong.", "15\u201316"),
}
# Each clause ends as the source does: the first three are followed by a comma in
# the note, so the quotation stops with an ellipsis and adds no punctuation of its
# own; C2's clause ends the sentence, so its full stop is the source's.
GOLD_CLAUSE = {'NORMATIVE': 'the whole figure for I \u2026',
               'NON-NORMATIVE': 'a vertical line for \u03c3\u1d65 \u2026',
               'METACOGNITIVE': 'a horizontal line for \u03c3\u2095 \u2026',
               'CRITICAL': 'a single point for C\u2082.'}
FIX_THM = {'NORMATIVE': 'T4_fix_I', 'NON-NORMATIVE': 'T4_fix_sv',
           'METACOGNITIVE': 'T4_fix_sh', 'CRITICAL': 'T4_fix_C2'}
MARK_THM = {'NON-NORMATIVE': 'S2_mark_sv_exact', 'METACOGNITIVE': 'S2_mark_sh_exact',
            'CRITICAL': 'S2_mark_C2_exact', 'NORMATIVE': 'S2_markAll_invariant'}
FIX_SAYS = {'NORMATIVE': 'I fixes every point of the plane',
            'NON-NORMATIVE': '\u03c3\u1d65 fixes (x, y) exactly when x = 0 \u2014 the vertical axis',
            'METACOGNITIVE': '\u03c3\u2095 fixes (x, y) exactly when y = 0 \u2014 the horizontal axis',
            'CRITICAL': 'C\u2082 fixes (x, y) exactly when x = 0 and y = 0 \u2014 the centre alone'}
MARK_SAYS = {'NON-NORMATIVE': 'the mark is invariant under k exactly when k is I or \u03c3\u1d65',
             'METACOGNITIVE': 'the mark is invariant under k exactly when k is I or \u03c3\u2095',
             'CRITICAL': 'the mark is invariant under k exactly when k is I or C\u2082',
             'NORMATIVE': 'the I mark is invariant under every move'}


# -------------------------------------------------------------- stations ---
def build_stations(m, S):
    """Stations run bottom of the stack to top, numbered in the order the
    semaphore is drawn. Returns (stations, absent_note)."""
    ms = S.ms()
    meas = ms['measure']
    eg = ms['exactness_grep']
    base, sub = NOTA[m.state]
    nota = base + SUB[sub]
    ring_outer = m.rings[-1]['r'] + m.rings[-1]['w'] / 2
    ri, ro = m.rings[0], m.rings[-1]
    st = []

    st.append(dict(key='field', title='The ground',
        layer=dict(visible={'field'}, field_edge=True),
        anchor=(410 + m.field['r'] * math.cos(math.radians(38)),
                410 + m.field['r'] * math.sin(math.radians(38))),
        values=[
            dict(text=f"{m.field['fill']} \u00b7 disc r {m.field['r']:g} slot units "
                      f"= {m.mm(m.field['r'], 2):g} mm",
                 src=S.m("g#field/circle/@fill,@r")),
            dict(text=f"edge sits under the outer ring (its outer edge: {ring_outer:g})",
                 src=S.m("g#field/circle/@r vs g#finalA5-rings/circle[2]")),
        ],
        meaning=dict(text="The dark ground the colours were chosen against: one lightness and "
                          "one chroma for all four semaphores, hue from the semaphore's colour.",
                     src=S.m("g#field/@inkscape:label"), kind='close paraphrase'),
        check=dict(text="The four masters' field fills: "
                        "#181403 \u00b7 #001817 \u00b7 #17121D \u00b7 #1F100E.",
                   src=S.m("g#field/circle/@fill, all four masters"))))

    st.append(dict(key='rings', title='The state colour',
        layer=dict(visible={'finalA5-rings'}),
        anchor=(410 + ro['r'] * math.cos(math.radians(42)),
                410 + ro['r'] * math.sin(math.radians(42))),
        values=[
            dict(text=f"inner ring r {ri['r']:g}, stroke {ri['w']:g} slot units "
                      f"({m.mm(ri['w'], 2):g} mm)", src=S.m("g#finalA5-rings/circle[1]")),
            dict(text=f"outer ring r {ro['r']:g}, stroke {ro['w']:g} = {m.mm(ro['w'], 2):g} mm "
                      f"\u00b7 both {ro['stroke']}", src=S.m("g#finalA5-rings/circle[2]")),
        ],
        meaning=dict(text="\u201cColour comes second. Shape carries every state.\u201d",
                     src=S.q("Colour comes second. Shape carries every state.", "100")),
        check=dict(text="Note, test 3 \u2014 take the colour away: in greyscale all four can "
                        "still be told apart by shape.",
                   src=S.q("Take the colour away.", "122", kind='pointer, paraphrased'))))

    geo = m.desc.split('Finish:')[0].replace('Geometry:', '').strip().rstrip('.')
    st.append(dict(key='meander', title='The ring of keys, and its gold finish',
        layer=dict(visible={'finalA5-geometry', 'finalA5-finish', 'finalA5-litedge'}),
        anchor=(410 + 350 * math.cos(math.radians(36)), 410 + 350 * math.sin(math.radians(36))),
        values=[
            dict(text=geo, src=S.m("svg/desc")),
            dict(text=f"lit edges: {m.litedge_n} opacity levels, ridge zone 2.2\u20134.8 print px "
                      f"\u00b7 sweep A axis 83.094\u00b0",
                 src=S.m("g#finalA5-litedge/@inkscape:label")),
        ],
        meaning=dict(text="\u201cThe ring's keys all turn one way, so a mirror reverses them, "
                          "while a half-turn leaves the ring as it was.\u201d",
                     src=S.q("The ring's keys all turn one way, so a mirror reverses them, while "
                             "a half-turn leaves the ring as it was.", "91")),
        check=dict(text="Note, Reading the semaphores \u2014 \u201cCheck the mark, not the "
                        "ring.\u201d",
                   src=S.q("Check the mark, not the ring.", "91",
                           kind='pointer with verbatim quotation'))))

    st.append(dict(key='legend', title='The plate cut into the ring, and the word',
        layer=dict(visible={'legend-plaque-en', 'legend-text-en'}),
        anchor=(520, 745),
        values=[
            dict(text=f"plate over keys 21\u20132 (45\u2013135\u00b0) \u00b7 floor, seams and plate "
                      f"all in the field tint {m.field['fill']} \u00b7 no edge strokes",
                 src=S.m("g#legend-plaque-en/@inkscape:label")),
            dict(text=f"DejaVu Sans Bold 2.34 as outlines \u00b7 cap height 4.4 mm \u00b7 17.0 pt "
                      f"at {m.print_mm:.1f} mm \u00b7 tracking 1.1 \u00b7 {m.legend_fill}",
                 src=S.m("g#legend-text-en/@inkscape:label")),
        ],
        meaning=dict(text="\u201c\u2026 each semaphore states it, with its word and with the gold "
                          "line that shows its mirror.\u201d",
                     src=S.q("each semaphore states it, with its word and with the gold line that "
                             "shows its mirror.", "188\u2013189")),
        check=dict(text="Note, test 5 \u2014 cover the words, then ask which state each print is.",
                   src=S.q("Cover the words, then show them twenty prints", "129",
                           kind='pointer, paraphrased'))))

    # ---- the mark
    mk = ms['mark_size_slot_units_vector']
    if m.state == 'NORMATIVE':
        v1 = dict(text=f"one outline plus the shared line \u00b7 {eg['uses']} uses, "
                       f"{eg['tok_defs']} token definitions, {eg['glyph_fix']} Fix elements",
                  src=S.j(f"states[{m.state}].exactness_grep"))
        title5 = "I: the identity, drawn as one outline"
        anchor5 = (410, 560)
    elif m.state == 'CRITICAL':
        v1 = dict(text=f"defined once, used {eg['uses']} times; {eg['rotate_180']} of them "
                       f"rotate(180) \u2014 a half-turn, not a redrawn copy",
                  src=S.j(f"states[{m.state}].exactness_grep"))
        title5 = f"{nota}: one token, and its half-turn"
        anchor5 = (300, 480)
    else:
        v1 = dict(text=f"defined once, used {eg['uses']} times; the second use is scale(1 -1) "
                       f"\u2014 a mirror, not a redrawn copy",
                  src=S.j(f"states[{m.state}].exactness_grep"))
        title5 = f"{nota}: one token, and its exact mirror"
        anchor5 = (330, 560) if m.state == 'METACOGNITIVE' else (410, 560)
    vals5 = [v1, dict(text=f"mark {mk[0]:g} \u00d7 {mk[1]:g} slot units = {m.mm(mk[0], 2):g} "
                           f"\u00d7 {m.mm(mk[1], 2):g} mm, gold included \u00b7 placement scale "
                           f"{m.glyph_scale:g}",
                      src=S.m("g#glyph-placement/@transform, @inkscape:label"))]
    if TWIN[m.state]:
        vals5.append(dict(text=f"twin of {TWIN[m.state]}: the two masters are byte-identical "
                               f"outside the one swapped glyph node (c14n identical: "
                               f"{str(ms['c14n_identical']).lower()})",
                          src=S.j(f"states[{m.state}].byte_identical_outside_swapped_node, "
                                  f".c14n_identical")))
    st.append(dict(key='mark', title=title5,
        layer=dict(visible={'glyph-placement'}, hide_fix=True), anchor=anchor5, values=vals5,
        meaning=dict(text="\u201cEach semaphore's mark is built to survive its own move "
                          "\u2026\u201d",
                     src=S.q("Each semaphore's mark is built to survive its own move",
                             "22\u201323")),
        check=dict(text=f"Lean {MARK_THM[m.state]}: {MARK_SAYS[m.state]}. Note, test 1.",
                   src=S.thm(MARK_THM[m.state]))))

    # ---- the gold Fix element, where the master carries one as its own layer
    s = m.glyph_scale
    if m.fix is not None:
        if m.fix['kind'] == 'rect':
            horiz = m.fix['width'] > m.fix['height']
            thick = m.fix['height'] if horiz else m.fix['width']
            x0, y0 = m.to_slot(m.fix['x'], m.fix['y'])
            x1, y1 = m.to_slot(m.fix['x'] + m.fix['width'], m.fix['y'] + m.fix['height'])
            anchor6 = (x1, (y0 + y1) / 2) if horiz else ((x0 + x1) / 2, y1)
            title6 = 'The gold line: the mirror line itself'
            vals6 = [
                dict(text=f"{m.mm(thick * s, 4):g} mm thick ({thick:g} token units \u00d7 {s:g} "
                          f"= {thick * s:.4f} slot units) \u00b7 {m.fix['fill']}",
                     src=S.m("g#glyph-placement/rect#glyph-fix/@width,@height,@fill; @transform")),
                dict(text=f"{m.mm(17.1062 * s, 4):g} mm of air each side \u00b7 overhangs the ink "
                          f"by {m.mm(25.35 * s, 3):g} mm at both ends",
                     src=S.m("g#glyph-placement/@inkscape:label")),
            ]
        else:
            r_slot = m.fix['r'] * s
            anchor6 = m.to_slot(m.fix['cx'], m.fix['cy'])
            title6 = 'The gold dot: the one point the half-turn holds'
            vals6 = [
                dict(text=f"radius {m.fix['r']:g} token units \u00d7 {s:g} = {r_slot:.3f} slot "
                          f"units = {m.mm(r_slot, 3):g} mm \u00b7 {m.fix['fill']}",
                     src=S.m("g#glyph-placement/circle#glyph-fix/@r,@fill; @transform")),
                dict(text=f"centred on ({anchor6[0]:g}, {anchor6[1]:g}) \u2014 the centre of the "
                          f"slot, where the two triangles meet",
                     src=S.m("g#glyph-placement/circle#glyph-fix/@cx,@cy; @transform")),
            ]
        vals6.append(dict(text=f"{meas['print']['gold_over_ink_px']} px of gold drawn over ink, "
                               f"measured at {meas['print']['render_px']} px "
                               f"({meas['print']['mm_per_px']:g} mm/px)",
                          src=S.j(f"states[{m.state}].measure.print.gold_over_ink_px, "
                                  f".render_px")))
        st.append(dict(key='fix', title=title6,
            layer=dict(visible={'glyph-placement'}, only_fix=True), anchor=anchor6, values=vals6,
            meaning=dict(text="\u201cGold shows what the semaphore's move leaves in place: "
                              "\u2026 " + GOLD_CLAUSE[m.state] + "\u201d",
                         src=S.q("Gold shows what the semaphore's move leaves in place: the whole "
                                 "figure for I, a vertical line for \u03c3\u1d65, a horizontal "
                                 "line for \u03c3\u2095, a single point for C\u2082.",
                                 "95\u201396")),
            check=dict(text=f"Lean {FIX_THM[m.state]}: {FIX_SAYS[m.state]}.",
                       src=S.thm(FIX_THM[m.state]))))

    # ---- the symmetry marks, where the master carries them
    if m.marks:
        b = m.marks[0]
        smj = meas['symmetry_marks']
        axes = 'two axes' if len(m.marks) == 8 else 'one axis'
        far = [bb for bb in m.marks if bb['height'] > bb['width'] and bb['x'] > 410] or m.marks
        anchor7 = (max(bb['x'] for bb in far) + 4, 410) if far[0]['height'] > far[0]['width'] \
            else (410, max(bb['y'] for bb in far) + 4)
        st.append(dict(key='marks',
            title=('Two bars across each line, at both ends' if len(m.marks) == 8
                   else 'Two bars across the line, at each end'),
            layer=dict(visible={'symmetry-marks'}), anchor=anchor7,
            values=[
                dict(text=f"{len(m.marks)} bars on {axes}, {b['width']:g} \u00d7 {b['height']:g} "
                          f"slot units = {m.mm(b['width'], 2):g} \u00d7 {m.mm(b['height'], 2):g} "
                          f"mm each \u00b7 {m.marks_fill}",
                     src=S.m("g#symmetry-marks/rect/@width,@height; g#symmetry-marks/@fill")),
                dict(text="the first 1.5 mm beyond the mark, then 1.6 mm, then the second",
                     src=S.m("g#symmetry-marks/@inkscape:label")),
                dict(text=f"measured gap mark \u2192 nearest bar "
                          f"{smj['gap_mark_to_nearest_bar_mm']:g} mm \u00b7 "
                          f"{smj['marks_over_mark_px']} px over the mark",
                     src=S.j(f"states[{m.state}].measure.symmetry_marks")),
            ],
            meaning=dict(text="The drafting convention for a line of symmetry (ISO 128-3); the "
                              "proportions are ours.",
                         src=S.m("g#symmetry-marks/@inkscape:label"), kind='close paraphrase'),
            check=dict(text="The note does not yet explain these bars to a reader \u2014 open "
                            "question 1 in the spec.",
                       src=S.m("g#symmetry-marks/@inkscape:label"))))

    for i, c in enumerate(st, start=1):
        c['n'] = i

    # ---- what this semaphore does not carry, where a station is absent
    absent = None
    if m.fix is None:
        absent = dict(title='No separate gold layer here',
                      text="Fix(I) is every point, so the whole mark carries the Fix gold: the "
                           "mark in station 5 is itself the gold, filled " + m.glyph_fill + ".",
                      src=S.m("g#glyph-body/@inkscape:label, @fill"), kind='close paraphrase',
                      note=dict(text="\u201c\u2026 the whole figure for I \u2026\u201d",
                                src=S.q("the whole figure for I", "95")))
    elif not m.marks:
        absent = dict(title='No symmetry marks here',
                      text="This master carries no symmetry-mark layer. The bars on the other "
                           "three cross a mirror line. Our reading of why: a point has no line "
                           "to cross.",
                      src=S.m("g#symmetry-marks absent from the file"),
                      kind='observed absence, with our reading of why',
                      note=dict(text="\u201c\u2026 a single point for C\u2082.\u201d",
                                src=S.q("a single point for C\u2082", "95\u201396")))
    return st, absent


# --------------------------------------------------------------- compose ---
def compose(state, outdir='.'):
    m = Master(state)
    S = Sources(m)
    ST, absent = build_stations(m, S)
    ms = S.ms()
    base, sub = NOTA[state]
    nota = base + SUB[sub]
    CC = m.colour
    GROUND = m.field['fill']

    W, H = CANVAS
    img = Image.new('RGB', (W, H), GROUND)
    dr = ImageDraw.Draw(img, 'RGBA')
    T = Text(dr)
    DR = Draft(DRAFT_C, GROUND)
    BADGES, TAGS, LATE = [], [], []
    LEFT_X0, LEFT_X1 = M, 636
    BOX_X0, BOX_X1 = 1450, W - M
    PLATE, PITCH, BOX_H = 300, 158, 148
    SLOTS = [(920 + i * 28, 1256 - i * PITCH) for i in range(7)]
    PC = SLOTS[:len(ST)]

    # ------------------------------------------------------------- header
    T.draw((M, 36), f"{state} datasheet", F_BOLD, 40, CC, 'title')
    T.draw((M, 92), "The Tetrasemaphore \u00b7 the semaphore taken apart, layer by layer",
           F_SANS, 18, GOLD2, 'subtitle')
    DR.rect([BOX_X0, 30, BOX_X1, 150], Draft.W_RULE)
    yy = T.para((BOX_X0 + 14, 42), "HOW TO READ THIS SHEET", F_BOLD, 16, GOLD,
                BOX_X1 - BOX_X0 - 28, 21, 'howto')
    T.para((BOX_X0 + 14, yy + 2),
           "Read the stack from the bottom up \u2014 the order the semaphore is drawn in. Every "
           "value, tick and label here is read from the master file, from the measurement record "
           "made from it, or quoted from the published note, and each one carries its source. The "
           "numbers, leader lines, boxes, centre axis and arrow are drafting marks, not data: "
           f"they are drawn in {DRAFT_NAME} with a dark outline, and everything in the "
           "semaphore's own colours is the semaphore.",
           F_SANS, 15, HI, BOX_X1 - BOX_X0 - 28, 20, 'howto')

    # --------------------------------------------------------- left column
    sf_text, sf_lines = STANDFIRST[state]
    sf_src = S.q(sf_text, sf_lines)
    y = T.para((LEFT_X0, 164), "\u201c" + sf_text + "\u201d", F_SANS, 19, HI,
               LEFT_X1 - LEFT_X0, 25, 'standfirst')
    T.draw((LEFT_X0, y + 2),
           f"published note, sha {S.note_sha16[:8]}, {sf_src['field']} \u00b7 its move is {nota}",
           F_SANS, 14, GOLD2, 'standfirst-src')

    coin_px, coin_xy = 428, (LEFT_X0 + 22, 288)
    site = os.path.join(SITE_DIR, f"TETRASEMAPHORE-{state}-en-1298.png")
    coin = Image.open(site).convert('RGBA').resize((coin_px, coin_px), Image.LANCZOS)
    img.paste(coin, coin_xy, coin)
    ck = coin_px / 820.0
    T.para((LEFT_X0, coin_xy[1] + coin_px + 12),
           f"The semaphore as the site shows it — site/assets/TETRASEMAPHORE-{state}-en-1298"
           f".png at {RELEASE['tag']}, sha {sha(site, 8)}.",
           F_SANS, 14, GOLD2, LEFT_X1 - LEFT_X0, 19, 'coin-cap')

    # ---- detail: the window covers the same area in mm on all four sheets and
    # its centre moves to this semaphore's Fix. A portrait window (the vertical
    # mirror) fits the box by its height, so its magnification comes out lower;
    # each sheet prints the magnification it actually used.
    det_y0 = 832
    det_box = (LEFT_X0 + 16, det_y0, LEFT_X0 + 16 + 540, det_y0 + 298)
    fixst = next((c for c in ST if c['key'] == 'fix'), None)
    vertical = m.fix is not None and m.fix['kind'] == 'rect' and m.fix['height'] > m.fix['width']
    if vertical:
        wu, hu = 94.0, 170.0
        wc, hc = 410.0, fixst['anchor'][1] + 2.6
    elif fixst is not None and m.fix['kind'] == 'rect':
        wu, hu = 170.0, 94.0
        wc, hc = fixst['anchor'][0] + 2.6, 410.0
    elif fixst is not None:
        wu, hu = 170.0, 94.0
        wc, hc = fixst['anchor']
    else:                                   # NORMATIVE: the far bar pair on the h axis
        far = [b for b in m.marks if b['height'] > b['width'] and b['x'] > 410]
        wu, hu = 170.0, 94.0
        wc, hc = (min(b['x'] for b in far) + max(b['x'] + b['width'] for b in far)) / 2, 410.0
    vis = {'glyph-placement'} | ({'symmetry-marks'} if m.marks else set())
    big_px = 4000
    big = m.render(vis, big_px)
    kb = big_px / 820.0
    crop = big.crop((int((wc - wu / 2) * kb), int((hc - hu / 2) * kb),
                     int((wc + wu / 2) * kb), int((hc + hu / 2) * kb)))
    bw, bh = det_box[2] - det_box[0], det_box[3] - det_box[1]
    scl = min(bw / crop.width, bh / crop.height)
    crop = crop.resize((int(crop.width * scl), int(crop.height * scl)), Image.LANCZOS)
    cx0 = det_box[0] + (bw - crop.width) // 2
    cy0 = det_box[1] + (bh - crop.height) // 2
    img.paste(crop, (cx0, cy0), crop)
    DR.rect([cx0, cy0, cx0 + crop.width, cy0 + crop.height], Draft.W_FRAME)
    det_mag = (crop.width / wu) / ck
    T.draw((LEFT_X0, det_y0 - 26), "DETAIL A \u2014 where the gold meets the mark", F_BOLD, 17,
           GOLD, 'detail-title')
    T.para((LEFT_X0, det_box[3] + 10),
           f"Enlarged {det_mag:.1f}\u00d7 from the semaphore above. The area shown is "
           f"{m.mm(wu, 1):g} \u00d7 {m.mm(hu, 1):g} mm of a {m.print_mm:.1f} mm semaphore. Mark "
           f"and bars only.",
           F_SANS, 14, GOLD2, LEFT_X1 - LEFT_X0, 19, 'detail-cap')
    rx0, ry0 = coin_xy[0] + (wc - wu / 2) * ck, coin_xy[1] + (hc - hu / 2) * ck
    rx1, ry1 = coin_xy[0] + (wc + wu / 2) * ck, coin_xy[1] + (hc + hu / 2) * ck
    DR.rect([rx0, ry0, rx1, ry1], Draft.W_WINDOW)
    DR.brackets([rx0, ry0, rx1, ry1], 16, Draft.W_BRACKET)
    # window and panel are paired by letter rather than by a line: at this weight
    # a connector ran across the caption between them
    DR.disc((rx1 + 26, ry0 - 6), 15)
    TAGS.append((rx1 + 26, ry0 - 7, 'A'))

    # ---- the one measurement
    iou = ms['measure']['print']['iou']
    own = OWN_MOVE[state]
    rows = [('top-to-bottom flip  \u03c3\u2095', 'sigma_h'),
            ('left-to-right flip  \u03c3\u1d65', 'sigma_v'),
            ('half-turn  C\u2082', 'c2')]
    rows.sort(key=lambda r: (r[1] not in own,))
    cy = 1196
    T.draw((LEFT_X0, cy), "DOES THE MARK SURVIVE ITS OWN MOVE?", F_BOLD, 17, GOLD, 'chart-title')
    cy += 30
    bar_x0, bar_w = LEFT_X0 + 232, 268
    for lbl, key in rows:
        v, is_own = iou[key], key in own
        T.draw((LEFT_X0, cy + 1), lbl, F_SANS, 16, HI if is_own else GOLD2, 'chart-row')
        dr.rectangle([bar_x0, cy + 3, bar_x0 + bar_w, cy + 17], outline=rgba(GOLD2, 90), width=1)
        dr.rectangle([bar_x0, cy + 3, bar_x0 + max(2, int(bar_w * v)), cy + 17],
                     fill=rgba(CC, 255 if is_own else 110))
        T.draw((bar_x0 + bar_w + 10, cy + 1), f"{v:.4f}", F_MONO, 15,
               HI if is_own else GOLD2, 'chart-val')
        cy += 26
    T.para((LEFT_X0, cy + 6),
           f"Overlap of the mark with itself after each move, measured on this master at "
           f"{ms['measure']['print']['render_px']} px "
           f"({ms['measure']['print']['mm_per_px']:g} mm/px). 1.0000 is a perfect match. "
           f"notation-measurements.json, sha {S.meas_sha16[:8]}, "
           f"states[{state}].measure.print.iou.",
           F_SANS, 14, GOLD2, LEFT_X1 - LEFT_X0, 19, 'chart-src')

    # ------------------------------------------------------- centre: stack
    ax0, ay0 = PC[0][0], PC[0][1] + PLATE * 0.62
    ax1, ay1 = PC[-1][0], PC[-1][1] - PLATE * 0.62
    L = math.hypot(ax1 - ax0, ay1 - ay0)
    ux, uy = (ax1 - ax0) / L, (ay1 - ay0) / L
    t, i, pattern = 0.0, 0, [24, 7, 5, 7]          # ISO 128 long-dash-dot
    while t < L:
        ln = pattern[i % 4]
        if i % 2 == 0:
            DR.axis([(ax0 + ux * t, ay0 + uy * t),
                      (ax0 + ux * min(t + ln, L), ay0 + uy * min(t + ln, L))], Draft.W_AXIS)
        t += ln
        i += 1
    for c, (px, py) in zip(ST, PC):
        lay = m.render(c['layer']['visible'], PLATE * 3,
                       hide_fix=c['layer'].get('hide_fix', False),
                       only_fix=c['layer'].get('only_fix', False),
                       field_edge=c['layer'].get('field_edge', False)
                       ).resize((PLATE, PLATE), Image.LANCZOS)
        img.paste(lay, (int(px - PLATE / 2), int(py - PLATE / 2)), lay)
    for px, py in PC:
        DR.line([(px - 9, py), (px + 9, py)], Draft.W_AXIS)
        DR.line([(px, py - 9), (px, py + 9)], Draft.W_AXIS)
    axx = 700
    arr_top = PC[-1][1] + 10
    DR.line([(axx, 1300), (axx, arr_top + 18)], Draft.W_LEADER)
    DR.poly([(axx, arr_top), (axx - 9, arr_top + 24), (axx + 9, arr_top + 24)], 0)
    lab = Image.new('RGBA', (300, 26), (0, 0, 0, 0))
    ImageDraw.Draw(lab).text((0, 0), "the order it is drawn", font=T.font(F_SANS, 16),
                             fill=DRAFT_C)
    lab = lab.rotate(90, expand=True)
    LATE.append((lab, (axx - 30, 640)))

    # ----------------------------------------------------- right: callouts
    def box_frame(y0):
        DR.line([(BOX_X0, y0), (BOX_X0, y0 + BOX_H)], Draft.W_RULE)

    for c, (px, py) in zip(ST, PC):
        y0 = py - BOX_H / 2
        box_frame(y0)
        axp = px + (c['anchor'][0] - 410) * PLATE / 820.0
        ayp = py + (c['anchor'][1] - 410) * PLATE / 820.0
        DR.line([(axp, ayp), (BOX_X0 - 74, py), (BOX_X0 - 10, py)], Draft.W_LEADER)
        DR.disc((axp, ayp), 5)
        bxx, byy = axp + 26, ayp - 22
        DR.disc((bxx, byy), 16)
        BADGES.append((bxx, byy, str(c['n'])))
        tx, yy = BOX_X0 + 16, y0 + 4
        T.draw((tx, yy), f"{c['n']}  {c['title']}", F_BOLD, 22, CC, 'box-title')
        hexes, seen = [], set()
        for v in c['values']:
            for h in re.findall(r'#[0-9A-Fa-f]{6}', v['text']):
                if h.upper() not in seen:
                    seen.add(h.upper())
                    hexes.append(h)
        for k, h in enumerate(reversed(hexes)):
            sx = BOX_X1 - 10 - (k + 1) * 24
            dr.rectangle([sx, yy + 3, sx + 18, yy + 21], fill=h, outline=rgba(GOLD2, 150), width=1)
        yy += 27
        for v in c['values']:
            yy = T.para((tx, yy), v['text'], F_MONO, 14, GOLD, BOX_X1 - tx - 8, 18, 'box-val')
        yy = T.para((tx, yy + 3), c['meaning']['text'], F_SANS, 15, HI, BOX_X1 - tx - 8, 19,
                    'box-meaning')
        T.para((tx, yy + 2), c['check']['text'], F_SANS, 14, GOLD2, BOX_X1 - tx - 8, 18,
               'box-check')

    if absent is not None:                     # the vacated slot, same pitch and sizes
        py = SLOTS[len(ST)][1]
        y0 = py - BOX_H / 2
        DR.line([(BOX_X0, y0), (BOX_X0, y0 + BOX_H)], Draft.W_RULE)
        tx, yy = BOX_X0 + 16, y0 + 4
        T.draw((tx, yy), absent['title'], F_BOLD, 22, GOLD2, 'absent-title')
        yy = T.para((tx, yy + 29), absent['text'], F_SANS, 15, HI, BOX_X1 - tx - 8, 19, 'absent')
        yy = T.para((tx, yy + 3), absent['note']['text'], F_SANS, 15, HI, BOX_X1 - tx - 8, 19,
                    'absent-note')
        T.para((tx, yy + 2), f"published note, {absent['note']['src']['field']}; and this master, "
                             f"{absent['src']['field']}.",
               F_SANS, 14, GOLD2, BOX_X1 - tx - 8, 18, 'absent-src')

    # -------------------------------------------------------------- footer
    foot = (
        f"Generated from {os.path.basename(m.path)} at {RELEASE['tag']} "
        f"{citation_clause()}sha256 {m.sha256}. "
        f"Rendered with cairosvg {cairosvg.__version__}; cairosvg renders no SVG filters, so the "
        f"foil grain (feTurbulence) and the organic band displacement are absent from the "
        f"{len(ST)} layer renders \u2014 the semaphore at upper left is the site's own PNG. "
        f"Scale: 1 mm = {m.u_per_mm:.4f} slot units (820 units = {m.print_mm:.3f} mm), derived "
        f"from this master ({m.scale_note}). Set in DejaVu Sans / DejaVu Sans Mono. Leader lines, "
        f"number badges, caption boxes, the centre axis and the direction arrow are drafting "
        f"marks, not data; the field plate's edge is stroked at its own measured radius so a "
        f"{GROUND} disc is visible on a {GROUND} sheet. "
        f"MOCK-UP for review, {build_time().date().isoformat()} \u2014 not a release file.")
    T.para((M, 1428), foot, F_SANS, 14, GOLD2, W - 2 * M, 19, 'footer')

    # ---- the drafting marks go on last, over everything they describe
    DM = (json.load(open('drafting_measurements.json'))
          if os.path.exists('drafting_measurements.json') else {})
    base = img.copy()
    DR.flush(dr)
    # the centre axis passes behind the parts: draw it only where it is clear of
    # the art by CLEAR_OF_ART px, so it stops short rather than cutting across
    if DR.axis_ops:
        ax_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ad = ImageDraw.Draw(ax_layer)
        for core_pass in (False, True):
            col = rgba(DR.c, 255) if core_pass else rgba(DR.g, 255)
            pad = 0 if core_pass else Draft.HALO
            for kind, pts, w in DR.axis_ops:
                ad.line(pts, fill=col, width=int(w + 2 * pad), joint='curve')
        bb = np.array(base, dtype=np.int16)
        gq = np.array([int(GROUND[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.int16)
        art = np.abs(bb - gq).max(axis=2) > 10
        keep = ~ndimage.binary_dilation(
            art, structure=np.ones((3, 3), bool), iterations=Draft.CLEAR_OF_ART)
        al = np.array(ax_layer)
        al[:, :, 3] = np.where(keep, al[:, :, 3], 0)
        ax_layer = Image.fromarray(al)
        img.paste(ax_layer, (0, 0), ax_layer)
        _axc = np.array([int(DRAFT_C[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.int16)
        _axm = ((np.abs(al[:, :, :3].astype(np.int16) - _axc).max(axis=2) <= 6)
                & (al[:, :, 3] > 0))
        ax_core_px, ax_over_art = int(_axm.sum()), int((_axm & art).sum())
        # the distance itself, not just an empty intersection: how far the nearest
        # axis pixel ends up from the nearest art pixel. A wrong dilation radius
        # shows up here as a different number, where the count above cannot.
        _dist = ndimage.distance_transform_edt(~art)
        ax_min_gap = round(float(_dist[_axm].min()), 2) if _axm.any() else None
    else:
        ax_core_px, ax_over_art, ax_min_gap = 0, 0, None
    for im_, pos_ in LATE:
        img.paste(im_, pos_, im_)
    for bx_, by_, n_ in BADGES:
        T.draw((bx_, by_ - 1), n_, F_BOLD, 19, GROUND, 'badge', anchor='mm')
    for tx_, ty_, s_ in TAGS:
        T.draw((tx_, ty_), s_, F_BOLD, 19, GROUND, 'tag', anchor='mm')

    # what the marks cover: contrast of the drafting colour against the art and
    # text beneath their footprint, measured on this sheet
    A, B = np.array(img, dtype=np.int16), np.array(base, dtype=np.int16)
    # (the axis has already been composited, so its pixels are in A)
    want = np.array([int(DRAFT_C[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.int16)
    core = (np.abs(A - want).max(axis=2) <= 6)
    under = B[core]
    cov = {}
    if under.size:
        uq = np.unique(under.reshape(-1, 3), axis=0)
        ratios = [contrast('#%02X%02X%02X' % tuple(int(v) for v in u), DRAFT_C) for u in uq]
        counts = {tuple(int(v) for v in u): int((np.abs(under - u).max(axis=1) == 0).sum())
                  for u in uq}
        order = np.argsort(ratios)
        gq2 = np.array([int(GROUND[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.int16)
        art_b = np.abs(B - gq2).max(axis=2) > 10
        halo_now = np.abs(A - gq2).max(axis=2) <= 6
        cov = dict(art_px_erased_by_halo=int((art_b & halo_now).sum()),
                   axis_core_px=int(ax_core_px), axis_core_px_over_art=int(ax_over_art),
                   axis_clear_of_art_px=Draft.CLEAR_OF_ART,
                   axis_min_gap_to_art_px=ax_min_gap,
                   core_px=int(core.sum()), distinct_colours_under=int(len(uq)),
                   min_contrast=round(float(min(ratios)), 2),
                   min_against='#%02X%02X%02X' % tuple(int(v) for v in uq[order[0]]),
                   median_contrast=round(float(np.median(ratios)), 2),
                   px_below_3to1=int(sum(counts[tuple(int(v) for v in uq[i])]
                                         for i in range(len(uq)) if ratios[i] < 3.0)))

    # ----------------------------------------------- checks and the audit --
    # every text colour against this sheet's own ground, tested against the floor
    contrast_faults = [dict(role=k, colour=v, ratio=round(contrast(v, GROUND), 2))
                       for k, v in dict(state_colour=CC, gold=GOLD, gold_fix=GOLD2,
                                        body_and_highlight=HI, drafting=DRAFT_C).items()
                       if contrast(v, GROUND) < CONTRAST_FLOOR]
    if contrast_faults:
        raise AssertionError(f"{state}: text colour below {CONTRAST_FLOOR}:1 on its own "
                             f"ground: {contrast_faults}")
    report = {'overlaps': [], 'outside': []}
    PARA = ('box-val', 'box-meaning', 'box-check', 'howto', 'footer', 'standfirst', 'chart-src',
            'detail-cap', 'coin-cap', 'absent', 'absent-note', 'absent-src')
    bx = T.boxes
    for i, (t1, s1, b1) in enumerate(bx):
        if b1[0] < 0 or b1[1] < 0 or b1[2] > W or b1[3] > H:
            report['outside'].append((t1, s1[:40]))
        for t2, s2, b2 in bx[i + 1:]:
            if t1 == t2 and t1 in PARA:
                continue
            if not (b1[2] <= b2[0] or b2[2] <= b1[0] or b1[3] <= b2[1] or b2[3] <= b1[1]):
                report['overlaps'].append((t1, s1[:28], t2, s2[:28]))

    def provenance_fault(src_name, field):
        f_ = field or ''
        master_shape = ('g#' in f_) or f_.startswith('svg/')
        json_shape = f_.startswith('states[')
        note_shape = f_.startswith('lines ')
        if src_name.startswith('MASTER-'):
            if json_shape:
                return 'master source, measurement-record field'
            if note_shape:
                return 'master source, note field'
            if not master_shape:
                return 'master source, field is not a master XPath'
        elif src_name == os.path.basename(MEASJSON):
            if master_shape:
                return 'measurement-record source, master field'
            if not json_shape:
                return 'measurement-record source, field is not a states[...] path'
        elif src_name.startswith('README.md'):
            if not note_shape:
                return 'note source, field is not a line reference'
        elif src_name.startswith('proofs/'):
            if master_shape or json_shape or note_shape:
                return 'Lean source, field is not a theorem name'
        return None

    # ---- quotation punctuation, over every string the sheet draws
    qp_checked, qp_faults = 0, []
    drawn = ['\u201c' + sf_text + '\u201d']      # the sheet draws the standfirst quoted
    for c in ST:
        drawn += [v['text'] for v in c['values']] + [c['meaning']['text'], c['check']['text']]
    if absent is not None:
        drawn += [absent['text'], absent['note']['text']]
    for d_ in drawn:
        # only spans the sheet already presents inside typographic quotes are
        # quotations; value lines and pointer wording are ours and are not checked
        n_, f_ = S.quotation_punctuation(d_)
        qp_checked += n_
        qp_faults += f_
    report['quotation_punctuation'] = qp_faults
    report['quotation_spans_checked'] = qp_checked

    entries = []
    for c in ST:
        for v in c['values']:
            entries.append(('value', c['n'], v['text'], v['src']))
        entries.append(('meaning', c['n'], c['meaning']['text'], c['meaning']['src']))
        entries.append(('check', c['n'], c['check']['text'], c['check']['src']))
    if absent is not None:
        entries.append(('absent', 0, absent['text'], absent['src']))
        entries.append(('absent-note', 0, absent['note']['text'], absent['note']['src']))
    prov = [dict(station=n, slot=slot, fault=f, source=src.get('source'),
                 field=src.get('field'), text=txt[:80])
            for slot, n, txt, src in entries
            for f in [provenance_fault(src.get('source', ''), src.get('field', ''))] if f]
    report['provenance'] = prov
    report['provenance_checked'] = len(entries)

    os.makedirs(outdir, exist_ok=True)
    stem = f"datasheet_{state}"
    p_full = os.path.join(outdir, stem + ".png")
    img.save(p_full)
    img.resize((1200, 750), Image.LANCZOS).save(os.path.join(outdir, stem + "_1200.png"))

    payload = dict(
        generated=build_time().isoformat(timespec='seconds'),
        kind="MOCK-UP for review; design work for site version 1.1; writes nothing to the release",
        state=state, notation=nota, stations=len(ST),
        release={k: v for k, v in RELEASE.items() if v},
        standfirst=dict(text=sf_text, **sf_src),
        sheet=dict(file=stem + ".png", px=list(CANVAS), ground=GROUND,
                   palette=dict(state_colour=CC, gold=GOLD, gold_fix=GOLD2, highlight=HI),
                   contrast_on_ground={k: round(contrast(v, GROUND), 2) for k, v in
                                       dict(state_colour=CC, gold=GOLD, gold_fix=GOLD2,
                                            highlight=HI).items()},
                   contrast_floor=CONTRAST_FLOOR,
                   contrast_below_floor=contrast_faults),
        sources=dict(
            master=dict(file=os.path.basename(m.path), sha256=m.sha256),
            note=dict(file='README.md at ' + RELEASE['tag'], sha256=S.note_sha256),
            measurements=dict(file=os.path.basename(MEASJSON), sha16=S.meas_sha16),
            lean=dict(file='proofs/TetrasemaphoreAlgebra.lean at ' + RELEASE['tag'],
                      sha16=S.lean_sha16),
            site_png=dict(file=os.path.basename(site), sha16=sha(site, 16)),
        ),
        scale=dict(u_per_mm=round(m.u_per_mm, 4), print_diameter_mm=round(m.print_mm, 3),
                   derived_from=m.scale_note, source=os.path.basename(m.path), sha16=m.sha16),
        callouts=[dict(n=c['n'], key=c['key'], title=c['title'],
                       layer_groups=sorted(c['layer']['visible']),
                       anchor_slot_units=[round(v, 3) for v in c['anchor']],
                       values=[dict(text=v['text'], **v['src']) for v in c['values']],
                       meaning={**c['meaning']['src'], 'text': c['meaning']['text'],
                                'kind': c['meaning'].get('kind')
                                        or c['meaning']['src'].get('kind', 'quote')},
                       check=dict(text=c['check']['text'], **c['check']['src']))
                  for c in ST],
        absent=(None if absent is None else
                dict(title=absent['title'], text=absent['text'], kind=absent['kind'],
                     **{k: v for k, v in absent['src'].items()},
                     note=dict(text=absent['note']['text'], **absent['note']['src']))),
        chart=dict(title="Does the mark survive its own move?",
                   own_move=list(own),
                   rows=[dict(move=l, key=k, iou=iou[k], is_own=(k in own)) for l, k in rows],
                   measured_at_px=ms['measure']['print']['render_px'],
                   mm_per_px=ms['measure']['print']['mm_per_px'],
                   source=os.path.basename(MEASJSON), sha16=S.meas_sha16,
                   field=f"states[{state}].measure.print.iou"),
        drafting=dict(colour=DRAFT_C, name=DRAFT_NAME,
                      chosen_by=DM.get('rule'),
                      colour_vision=DM.get('colour_vision_views'),
                      colour_vision_models=DM.get('models'),
                      worst_view=DM.get('worst_view'), worst_view_de=DM.get('worst_view_de'),
                      chosen_by_carey=DM.get('chosen_by_carey'),
                      search_rank=DM.get('search_rank'),
                      search_qualifying=DM.get('search_qualifying'),
                      search_first=DM.get('search_first'),
                      search_first_de=DM.get('search_first_de'),
                      ciede2000_to_art=DM.get('ciede2000_to_art'),
                      min_de_art=DM.get('min_de_art'), nearest_art=DM.get('nearest_art'),
                      ciede2000_to_text=DM.get('ciede2000_to_text'),
                      min_de_text=DM.get('min_de_text'), nearest_text=DM.get('nearest_text'),
                      contrast_to_ground=round(contrast(DRAFT_C, GROUND), 2),
                      contrast_to_all_grounds=DM.get('contrast_to_grounds'),
                      halo=dict(colour=GROUND, px_at_2400=Draft.HALO, px_at_1200=Draft.HALO // 2),
                      weights_px_at_2400=dict(detail_window=Draft.W_WINDOW,
                                              corner_brackets=Draft.W_BRACKET,
                                              panel_frame=Draft.W_FRAME,
                                              leader_lines=Draft.W_LEADER,
                                              box_rules=Draft.W_RULE,
                                              centre_axis=Draft.W_AXIS,
                                              badge_radius=16, anchor_dot_radius=5),
                      window_assembly_px=Draft.W_WINDOW + 2 * Draft.HALO,
                      bracket_assembly_px=Draft.W_BRACKET + 2 * Draft.HALO,
                      art_lines=DM.get('art_lines', {}).get(state),
                      covered=cov),
        audit=dict(quotes_verified=len([v for v in S.verified
                                        if v[0] == 'note' and v[1] == 'quote']),
                   pointers_verified=len([v for v in S.verified
                                          if v[0] == 'note' and v[1].startswith('pointer')]),
                   lean_names_verified=len([v for v in S.verified if v[0] == 'lean']),
                   failures=S.failed,
                   strings_provenance_checked=len(entries),
                   provenance_faults=prov,
                   quotation_spans_checked=qp_checked,
                   quotation_punctuation_faults=qp_faults,
                   text_box_overlaps=report['overlaps'],
                   text_outside_canvas=report['outside'],
                   contrast_floor=CONTRAST_FLOOR,
                   contrast_faults=contrast_faults),
    )
    with open(os.path.join(outdir, f"audit_{state}.json"), 'w') as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    return p_full, payload, report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--state', default='METACOGNITIVE')
    ap.add_argument('--outdir', default='.')
    ap.add_argument('--release-tag', default=RELEASE['tag'], help='the release the sheet cites (default: DATASHEET_RELEASE_TAG or v1.0.0)')
    ap.add_argument('--release-commit', default=None, help="its commit; pass '' when it does not exist yet, and the footer names none (default: the environment's, or the 1.0.0 commit for the default tag only)")
    ap.add_argument('--release-doi', default=None, help="its DOI, reserved before the build; pass '' to print none (default: the environment's, or the 1.0.0 DOI for the default tag only)")
    ap.add_argument('--note-file', default=None, help='the staged note under src/ (default README-<tag>.md)')
    ap.add_argument('--lean-file', default=None, help='the staged proof file under src/ (default TetrasemaphoreAlgebra-<tag>.lean)')
    a = ap.parse_args()
    # another tag than the one the environment or the defaults name gets no inherited commit or DOI:
    # a stale 1.0.0 citation on other sheets would look right and be wrong
    same_tag = a.release_tag == RELEASE['tag']
    RELEASE.update(tag=a.release_tag,
                   commit=a.release_commit if a.release_commit is not None else (RELEASE['commit'] if same_tag else ''),
                   doi=a.release_doi if a.release_doi is not None else (RELEASE['doi'] if same_tag else ''))
    if a.note_file or not same_tag:
        NOTE = os.path.join(SRC, a.note_file or f"README-{a.release_tag}.md")
    if a.lean_file or not same_tag:
        LEANFILE = os.path.join(SRC, a.lean_file or f"TetrasemaphoreAlgebra-{a.release_tag}.lean")
    p, payload, rep = compose(a.state, a.outdir)
    au = payload['audit']
    print(f"{p}  stations={payload['stations']}")
    print(f"  quotes={au['quotes_verified']} pointers={au['pointers_verified']} "
          f"lean={au['lean_names_verified']} "
          f"failures={len(au['failures'])} | provenance {au['strings_provenance_checked']} checked,"
          f" {len(au['provenance_faults'])} faults | punctuation "
          f"{au['quotation_spans_checked']} spans, {len(au['quotation_punctuation_faults'])} "
          f"faults | overlaps={len(rep['overlaps'])} outside={len(rep['outside'])}")
    for o in rep['quotation_punctuation'][:10]:
        print("   PUNCTUATION", o)
    for o in rep['overlaps'][:10]:
        print("   OVERLAP", o)
    for o in rep['provenance'][:10]:
        print("   PROVENANCE", o)
