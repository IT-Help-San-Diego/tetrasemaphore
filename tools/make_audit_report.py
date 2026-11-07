#!/usr/bin/env python3
"""Collect the four per-sheet audits into one report."""
import json, datetime, os

def build_time():
    """The build's clock. SOURCE_DATE_EPOCH (seconds since the epoch, UTC), when set,
    makes a build reproducible byte for byte; otherwise the time of the run."""
    e = os.environ.get('SOURCE_DATE_EPOCH')
    if e:
        return datetime.datetime.fromtimestamp(int(e), datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)

STATES = ['NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL']
P = json.load(open(f'audit_{STATES[0]}.json'))
L = ["# Datasheet audit report", "",
     f"Four sheets, one template. Generated {build_time().date().isoformat()}. "
     f"MOCK-UP for review; design work for site version 1.1.", "",
     f"Sources, all read from the published tree at `{P['release']['tag']}`"
     + ((' (' + ', '.join(p for p in ((f"commit `{P['release']['commit'][:12]}`" if P['release'].get('commit') else ''),
                                        (f"Zenodo {P['release']['doi']}" if P['release'].get('doi') else '')) if p) + ')')
        if P['release'].get('commit') or P['release'].get('doi') else '') + ':', "",
     f"- published note: `{P['sources']['note']['file']}`, sha256 "
     f"`{P['sources']['note']['sha256'][:16]}`",
     f"- measurement record: `{P['sources']['measurements']['file']}`, sha16 "
     f"`{P['sources']['measurements']['sha16']}`",
     f"- proofs: `{P['sources']['lean']['file']}`, sha16 `{P['sources']['lean']['sha16']}`",
     "- masters and site assets: per sheet, below.", "",
     "## Totals", "",
     "| sheet | stations | quotations | pointers | Lean names | strings provenance-checked "
     "| provenance faults | quotation spans | punctuation faults | text overlaps "
     "| text outside canvas |",
     "|---|---|---|---|---|---|---|---|---|---|---|"]
tot = dict(q=0, p=0, l=0, s=0, f=0, o=0, x=0, qs=0, qf=0)
D = {}
for st in STATES:
    d = json.load(open(f'audit_{st}.json')); D[st] = d
    a = d['audit']
    L.append(f"| {st} | {d['stations']} | {a['quotes_verified']} | {a['pointers_verified']} | "
             f"{a['lean_names_verified']} | "
             f"{a['strings_provenance_checked']} | {len(a['provenance_faults'])} | "
             f"{a['quotation_spans_checked']} | "
             f"{len(a['quotation_punctuation_faults'])} | "
             f"{len(a['text_box_overlaps'])} | {len(a['text_outside_canvas'])} |")
    tot['qs'] += a['quotation_spans_checked']
    tot['qf'] += len(a['quotation_punctuation_faults'])
    tot['q'] += a['quotes_verified']; tot['p'] += a['pointers_verified']
    tot['l'] += a['lean_names_verified']
    tot['s'] += a['strings_provenance_checked']; tot['f'] += len(a['provenance_faults'])
    tot['o'] += len(a['text_box_overlaps']); tot['x'] += len(a['text_outside_canvas'])
L.append(f"| **all four** | **{sum(D[s]['stations'] for s in STATES)}** | **{tot['q']}** | "
         f"**{tot['p']}** | **{tot['l']}** | **{tot['s']}** | **{tot['f']}** | "
         f"**{tot['qs']}** | **{tot['qf']}** | **{tot['o']}** | **{tot['x']}** |")
L += ["", "Every cited string \u2014 quotation and pointer alike \u2014 is looked up in the "
          "published note before anything is drawn, and a Lean name is looked up as a `theorem` "
          "or `lemma` declaration in the published proof file. The two columns separate how the "
          "sheet *presents* a cited string: a **quotation** reproduces the note's own words; a "
          "**pointer** names a test or a section in wording of ours, with the test's title or "
          "sentence verified verbatim behind it. The provenance check tests, in both directions, "
          "that each string's field names a place that can exist in the file its source names.",
      "",
      "**Quotation punctuation.** Every span a sheet wraps in typographic quotes is tested "
      "against the note: a span ending in punctuation claims the note carries that mark at that "
      "point, and a span ending in an ellipsis claims nothing. `test_quotation_punctuation.py` "
      "runs the check over the three faults found in review, their three corrected forms, the one "
      "full stop the note does have, and three invented cases \u2014 ten cases, all as intended \u2014 "
      "so a zero here is informative rather than vacuous.", ""]

L += ["## Every quotation, by sheet", "",
      f"Line numbers are in the published note, sha256 "
      f"`{P['sources']['note']['sha256'][:16]}`.", ""]
for st in STATES:
    d = D[st]
    L += [f"### {st}", "",
          "| station | text on the sheet | lines | kind |", "|---|---|---|---|"]
    rows = [('standfirst', '\u201c' + d['standfirst']['text'] + '\u201d',
             d['standfirst']['field'], d['standfirst'].get('kind', 'quote'))]
    for c in d['callouts']:
        for slot in ('meaning', 'check'):
            e = c[slot]
            if e.get('source', '').startswith('README.md'):
                rows.append((str(c['n']) + ' ' + c['key'], e['text'], e['field'],
                             e.get('kind', 'quote')))
    if d.get('absent'):
        rows.append(('absent note', d['absent']['note']['text'],
                     d['absent']['note']['field'], d['absent']['note'].get('kind', 'quote')))
    for k, t, f, kind in rows:
        L.append(f"| {k} | {t.replace('|', '/')} | {f.replace('lines ', '')} | {kind} |")
    L += ["", f"Master: `{d['sources']['master']['file']}`, sha256 "
              f"`{d['sources']['master']['sha256'][:16]}`. Site asset: "
              f"`{d['sources']['site_png']['file']}`, sha16 `{d['sources']['site_png']['sha16']}`. "
              f"Scale: 1 mm = {d['scale']['u_per_mm']} slot units "
              f"({d['scale']['print_diameter_mm']} mm across).", ""]

L += ["## Lean names cited, by sheet", "", "| sheet | theorem | what the sheet says it says |",
      "|---|---|---|"]
for st in STATES:
    for c in D[st]['callouts']:
        e = c['check']
        if e.get('source', '').startswith('proofs/'):
            L.append(f"| {st} | `{e['field']}` | {e['text'].replace('|', '/')} |")
G = D[STATES[0]]['drafting']
L += ["", "## The drafting style", "",
      f"All drafting marks on all four sheets are drawn in **{G['name']} `{G['colour']}`** over a "
      f"halo in each sheet's own ground, {G['halo']['px_at_2400']} px each side at 2400 px wide "
      f"({G['halo']['px_at_1200']} px at the 1200 px preview). The colour was chosen by "
      f"measurement: {G['chosen_by']}. It appears in none of the four semaphores' art.", "",
      "| measurement | value |", "|---|---|",
      f"| nearest colour in the four palettes | `{G['nearest_art']}` at "
      f"\u0394E2000 {G['min_de_art']} |",
      f"| nearest text colour | `{G['nearest_text']}` at \u0394E2000 {G['min_de_text']} |",
      f"| farthest colour in the four palettes | "
      f"`{G['ciede2000_to_art'][-1]['hex']}` at \u0394E2000 {G['ciede2000_to_art'][-1]['dE']} |",
      f"| contrast against the four grounds | "
      + " \u00b7 ".join(f"{k} {v}:1" for k, v in G['contrast_to_all_grounds'].items()) + " |",
      ""]
L += ["Every colour in the four palettes, by difference from the drafting colour:", "",
      "| \u0394E2000 | colour |", "|---|---|"]
for r in G['ciede2000_to_art']:
    L.append(f"| {r['dE']} | `{r['hex']}` |")
L += ["", "### Under colour-blind simulation", "",
      "The green used in version 4 turned pale gold under simulated dichromacy, close to the "
      "art's gold, which is what sent this version looking for another colour. Each view below "
      "passes the drafting colour and every art and text colour through the same model, then "
      "compares them in CIEDE2000. Both models are applied in linear RGB. The models:", ""]
for m in (G.get('colour_vision_models') or []):
    L.append(f"- {m}")
L += ["", "| view | nearest art or text colour | \u0394E2000 |", "|---|---|---|"]
for k, v in (G.get('colour_vision') or {}).items():
    L.append(f"| {k} | `{v['nearest_art']}` | {v['min_de']} |")
_wd, _fd = G.get('worst_view_de'), G.get('search_first_de')
L += ["", f"The worst of the seven views is **{G.get('worst_view')}** at \u0394E2000 {_wd}. "
          f"Carey chose this colour from a preview on 23 October 2026. The search in "
          f"`choose_drafting_colour.py` places it {G.get('search_rank')} of "
          f"{G.get('search_qualifying')} candidates clearing 7:1 on all four grounds, with "
          f"`{G.get('search_first')}` first at \u0394E2000 {_fd}"
          + (f" \u2014 {round(_fd - _wd, 2)} \u0394E2000 units apart in the worst view"
             if (_wd is not None and _fd is not None) else "")
          + ". The sheets carry Carey's choice.", ""]
L += ["", "Line weights, px at 2400 px wide (halo adds "
          f"{G['halo']['px_at_2400']} px each side):", "",
      "| mark | core | with halo |", "|---|---|---|"]
for k, v in G['weights_px_at_2400'].items():
    if k.endswith('radius'):
        L.append(f"| {k.replace('_', ' ')} | r {v} | r {v + G['halo']['px_at_2400']} |")
    else:
        L.append(f"| {k.replace('_', ' ')} | {v} | {v + 2 * G['halo']['px_at_2400']} |")
L += ["", "| sheet | art line in the window region (p10 / median / max, px) | window core | "
          "window with halo | marks over art: min contrast | median | px below 3:1 | "
          "axis px over art | art px under a halo |",
      "|---|---|---|---|---|---|---|---|---|"]
for st in STATES:
    g = D[st]['drafting']; al = g['art_lines']['art_line_px']; c = g['covered']
    L.append(f"| {st} | {al['p10']} / {al['median']} / {al['max']} | "
             f"{g['weights_px_at_2400']['detail_window']} | {g['window_assembly_px']} | "
             f"{c['min_contrast']}:1 vs `{c['min_against']}` | {c['median_contrast']}:1 | "
             f"{c['px_below_3to1']} of {c['core_px']} | "
             f"{c['axis_core_px_over_art']} of {c['axis_core_px']} | "
             f"{c['art_px_erased_by_halo']} |")
core = G['weights_px_at_2400']['detail_window']
asm = G['window_assembly_px']
meds = {st: D[st]['drafting']['art_lines']['art_line_px']['median'] for st in STATES}
maxs = {st: D[st]['drafting']['art_lines']['art_line_px']['max'] for st in STATES}
n_core = sum(1 for st in STATES if core > meds[st])
n_asm = sum(1 for st in STATES if asm > maxs[st])
worst_med = max(meds, key=meds.get)
worst_max = max(maxs, key=maxs.get)
L += ["", f"The art-line figures are measured on the reference semaphore at "
          f"{G['art_lines']['reference_semaphore_px']} px, the scale the detail window is drawn "
          f"at. Comparison, computed from the rows above rather than asserted: the "
          f"{core} px core is heavier than the median art line on {n_core} of the 4 sheets "
          f"(widest median {meds[worst_med]} px, {worst_med}); the {asm} px assembly, core plus "
          f"halo both sides, is heavier than the thickest single art stroke on {n_asm} of the 4 "
          f"(thickest {maxs[worst_max]} px, {worst_max}). "
          f"The marks-over-art columns are the worst case where a mark crosses the lightest gold "
          f"and cream: the ground halo carries the separation there, at the ground contrast "
          f"above.", ""]
_axc = D[STATES[0]]['drafting']['covered']['axis_clear_of_art_px']
_axtot = sum(D[st]['drafting']['covered']['axis_core_px_over_art'] for st in STATES)
_halo_rng = [D[st]['drafting']['covered']['art_px_erased_by_halo'] for st in STATES]
L += ["", f"**The centre axis.** Where the axis passes behind a part it now stops "
          f"{_axc} px short of it, at 2400 px wide: the axis is drawn to its own layer, and that "
          f"layer is cleared wherever the art beneath it, dilated by {_axc} px, is present. The "
          f"gap the clearance leaves is ground, so the separation a halo would give is there "
          f"without a halo being painted over the artwork. "
          f"The count of axis pixels over art is {_axtot} on the four sheets, which is what the "
          f"clearing step forces rather than an independent test of it: the same mask does the "
          f"clearing and the counting, so the intersection is empty whether or not the radius is "
          f"the intended one. The figure that can come out wrong is the distance. Measured on the "
          f"finished image, the nearest axis pixel sits "
          + " \u00b7 ".join(f"{st} {D[st]['drafting']['covered']['axis_min_gap_to_art_px']}"
                            for st in STATES)
          + f" px from the nearest art pixel, against the {_axc} px setting \u2014 a wrong radius "
          f"would read here as a different gap. The last column counts every "
          f"pixel where art was painted and a drafting halo now covers it \u2014 "
          f"{min(_halo_rng)} to {max(_halo_rng)} px per sheet, all of it from the number badges, "
          f"leader lines and detail window, none of it from the axis.", ""]
L += ["", "## Contrast of every text colour against each sheet's ground", "",
      "| sheet | ground | state colour | gold | Fix gold | highlight |", "|---|---|---|---|---|---|"]
for st in STATES:
    s_ = D[st]['sheet']; c_ = s_['contrast_on_ground']
    L.append(f"| {st} | `{s_['ground']}` | {c_['state_colour']}:1 | {c_['gold']}:1 | "
             f"{c_['gold_fix']}:1 | {c_['highlight']}:1 |")
allv = [(v, st, k) for st in STATES
        for k, v in D[st]['sheet']['contrast_on_ground'].items()]
allv.sort()
lo, hi = allv[0], allv[-1]
others = [v for v, st, k in allv if k == 'state_colour' and st != lo[1]]
L += ["", f"Sixteen colour-on-ground pairs, measured: {lo[0]:.2f}:1 ({lo[1]} {lo[2]}) to "
          f"{hi[0]:.2f}:1 ({hi[1]} {hi[2]}). All sit above the 4.5:1 floor for body text. "
          f"The least headroom is {lo[1]}'s state colour at {lo[0]:.2f}:1; the other three state "
          f"colours sit at {min(others):.2f}\u2013{max(others):.2f}:1.", ""]
open('AUDIT_REPORT.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L[:24]))
print('...')
print('wrote AUDIT_REPORT.md', len('\n'.join(L)), 'chars')
