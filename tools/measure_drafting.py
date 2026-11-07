#!/usr/bin/env python3
"""The drafting style's measurements, written once for the four audits."""
import json, importlib.util, sys
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000
from scipy import ndimage
from skimage.morphology import skeletonize

spec = importlib.util.spec_from_file_location('mk', 'make_anatomy_plate.py')
mk = importlib.util.module_from_spec(spec); sys.modules['mk'] = mk; spec.loader.exec_module(mk)
cspec = importlib.util.spec_from_file_location('cd', 'choose_drafting_colour.py')
cd = importlib.util.module_from_spec(cspec); sys.modules['cd'] = cspec and cd
cspec.loader.exec_module(cd)
DRAFT = mk.DRAFT_C
ART = [h.upper() for h in json.load(open('handoff_art_colours.json'))]
GROUNDS = ['#181403', '#001817', '#17121D', '#1F100E']
TEXT = {'values': '#DEC875', 'body': '#F2E4B8', 'sources and checks': '#C7B469',
        'titles NORMATIVE': '#D5AF64', 'titles NON-NORMATIVE': '#4FB5B5',
        'titles METACOGNITIVE': '#B498E6', 'titles CRITICAL': '#E25C60'}
ART_ONLY = [h for h in ART if h not in GROUNDS]


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def lab1(h):
    return rgb2lab(hex2rgb(h).reshape(1, 1, 3)).reshape(3)


def de(a, b):
    return float(deltaE_ciede2000(lab1(a).reshape(1, 3), lab1(b).reshape(1, 3))[0])


art_tbl = sorted(((round(de(DRAFT, h), 2), h) for h in ART_ONLY))
txt_tbl = sorted(((round(de(DRAFT, h), 2), k, h) for k, h in TEXT.items()))
gnd_tbl = {g: round(mk.contrast(DRAFT, g), 2) for g in GROUNDS}
gnd_de = sorted(((round(de(DRAFT, g), 2), g) for g in GROUNDS))

COIN_PX = 428
lines = {}
for st in ['NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL']:
    m = mk.Master(st)
    if m.fix is not None and m.fix['kind'] == 'rect':
        x0, y0 = m.to_slot(m.fix['x'], m.fix['y'])
        x1, y1 = m.to_slot(m.fix['x'] + m.fix['width'], m.fix['y'] + m.fix['height'])
        horiz = m.fix['width'] > m.fix['height']
        wu, hu = (170., 94.) if horiz else (94., 170.)
        wc, hc = ((x1 + 2.6, 410.) if horiz else (410., y1 + 2.6))
    elif m.fix is not None:
        wu, hu = 170., 94.; wc, hc = m.to_slot(m.fix['cx'], m.fix['cy'])
    else:
        far = [b for b in m.marks if b['height'] > b['width'] and b['x'] > 410]
        wu, hu = 170., 94.
        wc = (min(b['x'] for b in far) + max(b['x'] + b['width'] for b in far)) / 2; hc = 410.
    vis = {'glyph-placement'} | ({'symmetry-marks'} if m.marks else set())
    a = np.array(m.render(vis, COIN_PX))[:, :, 3] > 40
    k = COIN_PX / 820.0
    sub = a[int((hc - hu / 2) * k):int((hc + hu / 2) * k),
            int((wc - wu / 2) * k):int((wc + wu / 2) * k)]
    dt = ndimage.distance_transform_edt(sub)
    sk = skeletonize(sub)
    w = 2 * dt[sk] if sk.any() else np.array([0.0])
    lines[st] = dict(reference_semaphore_px=COIN_PX,
                     window_px=[round(wu * k, 1), round(hu * k, 1)],
                     art_line_px=dict(p10=round(float(np.percentile(w, 10)), 2),
                                      median=round(float(np.median(w)), 2),
                                      p90=round(float(np.percentile(w, 90)), 2),
                                      max=round(float(w.max()), 2)))

views = cd.per_view(DRAFT)
cand = json.load(open('handoff_drafting_candidates.json'))
out = dict(
    colour=DRAFT, name=mk.DRAFT_NAME,
    colour_vision_views=views,
    worst_view=min(views.items(), key=lambda kv: kv[1]['min_de'])[0],
    worst_view_de=min(v['min_de'] for v in views.values()),
    models=["Machado, Oliveira & Fernandes 2009, severity 1.0, linear RGB",
            "Vienot, Brettel & Mollon 1999, LMS-plane projection derived in "
            "choose_drafting_colour.py; its tritanopia case is the plane through white and the "
            "red primary, an approximation"],
    chosen_by_carey=True, search_rank=cand.get('chosen_rank'),
    search_qualifying=cand.get('qualifying'),
    search_first=(cand['ranked'][0]['hex'] if cand.get('ranked') else None),
    search_first_de=(cand['ranked'][0]['min_de_overall'] if cand.get('ranked') else None),
    axis_clear_of_art_px=mk.Draft.CLEAR_OF_ART,
    rule="largest minimum CIEDE2000 difference from the four semaphores' art and from the text "
         "colours, taken as the worst of seven views - normal vision and protanopia, deuteranopia "
         "and tritanopia under two models - among candidates clearing 7:1 on all four grounds; "
         "the colour in use is Carey's pick from a preview, 20th of 8486 qualifying candidates",
    ciede2000_to_art=[dict(dE=d, hex=h) for d, h in art_tbl],
    min_de_art=art_tbl[0][0], nearest_art=art_tbl[0][1],
    ciede2000_to_text=[dict(dE=d, role=k, hex=h) for d, k, h in txt_tbl],
    min_de_text=txt_tbl[0][0], nearest_text=txt_tbl[0][2],
    ciede2000_to_grounds=[dict(dE=d, hex=h) for d, h in gnd_de],
    contrast_to_grounds=gnd_tbl, min_contrast_to_ground=min(gnd_tbl.values()),
    line_weights_px_at_2400=dict(detail_window=mk.Draft.W_WINDOW,
                                 corner_brackets=mk.Draft.W_BRACKET,
                                 panel_frame=mk.Draft.W_FRAME,
                                 leader_lines=mk.Draft.W_LEADER, box_rules=mk.Draft.W_RULE,
                                 centre_axis=mk.Draft.W_AXIS, halo_each_side=mk.Draft.HALO),
    art_lines=lines)
json.dump(out, open('drafting_measurements.json', 'w'), indent=1)
print(f"{DRAFT} ({mk.DRAFT_NAME})")
print(f"  nearest art colour  {art_tbl[0][1]}  dE2000 {art_tbl[0][0]}")
print(f"  nearest text colour {txt_tbl[0][2]} ({txt_tbl[0][1]})  dE2000 {txt_tbl[0][0]}")
print(f"  farthest art colour {art_tbl[-1][1]}  dE2000 {art_tbl[-1][0]}")
print(f"  contrast to grounds {gnd_tbl}")
print("  CIEDE2000 to the nearest art or text colour, by view:")
for k, v in views.items():
    print(f"    {k:22s} {v['min_de']:6.2f}  (nearest {v['nearest_art']})")
print(f"  art line width in the window region, px at a {COIN_PX} px semaphore:")
for st, d in lines.items():
    print(f"    {st:15s} window {d['window_px']}  p10 {d['art_line_px']['p10']}  "
          f"median {d['art_line_px']['median']}  max {d['art_line_px']['max']}")
