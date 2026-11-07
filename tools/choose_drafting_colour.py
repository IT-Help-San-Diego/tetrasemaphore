#!/usr/bin/env python3
"""Choose the datasheets' drafting colour by measurement, colour-blind views
included.

The drafting marks are to read as unlike the art and unlike the text, for a
reader with normal colour vision and for a reader with dichromacy. A candidate
is scored by the smallest CIEDE2000 difference from any colour in the four
semaphores' art and from any text colour, taken across seven views: normal
vision, and protanopia, deuteranopia and tritanopia under two models —

  Machado, G. M., Oliveira, M. M., & Fernandes, L. A. F. (2009). A
  physiologically-based model for simulation of color vision deficiency.
  IEEE TVCG 15(6), 1291-1298.  (severity 1.0 matrices, linear RGB)

  Vienot, F., Brettel, H., & Mollon, J. D. (1999). Digital video colourmaps
  for checking the legibility of displays by dichromats. Color Research &
  Application 24(4), 243-252.  (LMS-plane projection, derived below rather
  than taken as a printed matrix, so the construction is visible; the paper
  covers protanopia and deuteranopia, and the tritanopia case here is the
  plane through white and the red primary, an approximation.)

Both models are applied in linear RGB. A candidate also clears 7:1 against
every ground. CIEDE2000 comes from scikit-image.

Version 5 note: Carey chose ice blue #C3E6FF from a preview on 23 October 2026.
This script reports its values and the ranking it would give; the sheets use
Carey's choice whether or not the search ranks another candidate first.
"""
import json, math
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000

CHOSEN_BY_CAREY = '#C3E6FF'
ART = [h.upper() for h in json.load(open('handoff_art_colours.json'))]
GROUNDS = ['#181403', '#001817', '#17121D', '#1F100E']
TEXT = ['#DEC875', '#F2E4B8', '#C7B469', '#D5AF64', '#4FB5B5', '#B498E6', '#E25C60']
ART_NOT_GROUND = [h for h in ART if h not in GROUNDS]

# ---- Machado, Oliveira & Fernandes 2009, severity 1.0, linear RGB
MACHADO = {
    'protanopia': np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281, 0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    'deuteranopia': np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501, 0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    'tritanopia': np.array([[1.255528, -0.076749, -0.178779],
                            [-0.078411, 0.930809, 0.147602],
                            [0.004733, 0.691367, 0.303900]]),
}

# ---- Vienot 1999: project LMS onto the plane through white and an anchor
LMS_FROM_RGB = np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]])
RGB_FROM_LMS = np.linalg.inv(LMS_FROM_RGB)


def _vienot(missing, anchor_rgb):
    """The replacement plane: the missing cone's response becomes a linear
    combination of the other two, fixed by requiring white and the anchor
    primary to be unchanged."""
    keep = [i for i in range(3) if i != missing]
    A = []
    b = []
    for rgb in (np.array([1.0, 1.0, 1.0]), np.array(anchor_rgb, dtype=float)):
        lms = LMS_FROM_RGB @ rgb
        A.append([lms[keep[0]], lms[keep[1]]])
        b.append(lms[missing])
    co = np.linalg.solve(np.array(A), np.array(b))
    P = np.eye(3)
    P[missing, missing] = 0.0
    P[missing, keep[0]] = co[0]
    P[missing, keep[1]] = co[1]
    return RGB_FROM_LMS @ P @ LMS_FROM_RGB


VIENOT = {'protanopia': _vienot(0, [0, 0, 1]),       # L lost, plane through blue
          'deuteranopia': _vienot(1, [0, 0, 1]),     # M lost, plane through blue
          'tritanopia': _vienot(2, [1, 0, 0])}       # S lost, plane through red
VIEWS = ([('normal', None)]
         + [(f'Machado {k}', v) for k, v in MACHADO.items()]
         + [(f'Vienot {k}', v) for k, v in VIENOT.items()])


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def rgb2hex(c):
    return '#%02X%02X%02X' % tuple(int(round(v * 255)) for v in np.clip(c, 0, 1))


def lum(h):
    c = hex2rgb(h)
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def oklch2srgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bb = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    lin = np.array([r, g, bb])
    if lin.min() < -1e-4 or lin.max() > 1 + 1e-4:
        return None                                   # outside the sRGB gamut
    lin = np.clip(lin, 0, 1)
    return np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)


def to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def from_linear(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate(rgb, mat):
    """rgb in 0-1 sRGB; the model is applied in linear RGB."""
    if mat is None:
        return rgb
    return from_linear(mat @ to_linear(np.asarray(rgb, dtype=float)))


def lab_of(rgbs):
    return rgb2lab(np.asarray(rgbs).reshape(-1, 1, 3)).reshape(-1, 3)


# per view, the Lab of every art and text colour as that view renders it
REF = {}
for name, mat in VIEWS:
    REF[name] = dict(
        art=lab_of([simulate(hex2rgb(h), mat) for h in ART_NOT_GROUND]),
        text=lab_of([simulate(hex2rgb(h), mat) for h in TEXT]))


def per_view(hx):
    out = {}
    for name, mat in VIEWS:
        a = lab_of([simulate(hex2rgb(hx), mat)])[0]
        d_art = deltaE_ciede2000(np.tile(a, (len(ART_NOT_GROUND), 1)), REF[name]['art'])
        d_txt = deltaE_ciede2000(np.tile(a, (len(TEXT), 1)), REF[name]['text'])
        out[name] = dict(min_de_art=round(float(d_art.min()), 2),
                         nearest_art=ART_NOT_GROUND[int(d_art.argmin())],
                         min_de_text=round(float(d_txt.min()), 2),
                         nearest_text=TEXT[int(d_txt.argmin())],
                         min_de=round(float(min(d_art.min(), d_txt.min())), 2))
    return out


def evaluate(hx):
    cg = {g: round(contrast(hx, g), 2) for g in GROUNDS}
    views = per_view(hx)
    worst = min(views.items(), key=lambda kv: kv[1]['min_de'])
    return dict(hex=hx, contrast_ground=cg, min_contrast_ground=round(min(cg.values()), 2),
                views=views, min_de_overall=worst[1]['min_de'], worst_view=worst[0])


if __name__ == '__main__':
    # the Vienot derivation reproduces the paper's printed coefficients
    print("Vienot protanopia, linear-RGB matrix as derived here:")
    print(np.round(VIENOT['protanopia'], 5))
    print("  (the paper's printed form has 0.11238 / 0.88762 on the first rows)")
    print()
    cands = {}
    for L in np.arange(0.60, 0.98, 0.02):
        for C in np.arange(0.02, 0.26, 0.01):
            for H in range(0, 360, 6):
                c = oklch2srgb(float(L), float(C), float(H))
                if c is None:
                    continue
                hx = rgb2hex(c)
                cands.setdefault(hx, (float(L), float(C), float(H)))
    cands.setdefault(CHOSEN_BY_CAREY, None)
    rows = []
    for hx in cands:
        e = evaluate(hx)
        if e['min_contrast_ground'] >= 7.0:
            e['oklch'] = ([round(v, 4) for v in cands[hx]] if cands[hx] else None)
            rows.append(e)
    rows.sort(key=lambda r: -r['min_de_overall'])
    print(f"{len(cands)} candidates in gamut, {len(rows)} clear 7:1 on all four grounds\n")
    print("top 8 by the smallest difference from any art or text colour, over all seven views:")
    for r in rows[:8]:
        print(f"  {r['hex']}  worst-view min dE {r['min_de_overall']:5.2f}  "
              f"({r['worst_view']})  ground {r['min_contrast_ground']:5.2f}:1")
    pick = next((i for i, r in enumerate(rows) if r['hex'] == CHOSEN_BY_CAREY), None)
    ch = rows[pick] if pick is not None else evaluate(CHOSEN_BY_CAREY)
    print(f"\nCarey's choice {CHOSEN_BY_CAREY}: rank "
          f"{pick + 1 if pick is not None else 'not in the qualifying set'} of {len(rows)}; "
          f"worst view {ch['worst_view']} at dE {ch['min_de_overall']}")
    for name, v in ch['views'].items():
        print(f"    {name:22s} art {v['min_de_art']:6.2f} vs {v['nearest_art']}   "
              f"text {v['min_de_text']:6.2f} vs {v['nearest_text']}")
    print(f"    contrast to grounds {ch['contrast_ground']}")
    json.dump(dict(art=ART_NOT_GROUND, grounds=GROUNDS, text=TEXT,
                   chosen=CHOSEN_BY_CAREY, chosen_rank=(pick + 1 if pick is not None else None),
                   qualifying=len(rows), chosen_eval=ch, ranked=rows[:40]),
              open('handoff_drafting_candidates.json', 'w'), indent=1)
