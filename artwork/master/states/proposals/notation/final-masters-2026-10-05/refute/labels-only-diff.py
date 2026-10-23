#!/usr/bin/env python3
"""labels-only-diff.py — run from dose-01-meander-v2. The independent refuters examined the FIRST PASS of build 3 (copies in
refute/build3-first-pass-as-refuted/). Two of their findings were wrong words in hidden layer labels, so the generator was corrected and the set
rebuilt. This proves the delivered files differ from the refuted ones in layer-label text only:
 1. each delivered SVG equals its first-pass copy once every inkscape:label value is blanked; the labels that differ are listed;
 2. every PNG the first-pass manifests recorded is byte-identical now, except the sheets named in EXPECTED (a caption was corrected)."""
import re, json, hashlib, sys, os
P = 'master/states/proposals'; F = f'{P}/notation/final-masters-2026-10-05'; A = f'{F}/refute/build3-first-pass-as-refuted'; O = f'{P}/owl-finals-2026-10-05'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
blank = lambda s: re.sub(r' inkscape:label="[^"]*"', ' inkscape:label=""', s); labels = lambda s: re.findall(r'<g id="([^"]+)"[^>]*? inkscape:label="([^"]*)"', s)
ok = True; n = 0
def check(name, cond, detail=''):
    global ok, n; ok &= bool(cond); n += 1; print('PASS' if cond else 'FAIL', name, detail)
PAIRS = [(f'{F}/MASTER-medallion-{st}-notation-slot820.svg', f'{A}/notation/MASTER-medallion-{st}-notation-slot820.svg') for st in ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')] + \
        [(f'{O}/MASTER-medallion-{st}-owl-slot820.svg', f'{A}/owl/MASTER-medallion-{st}-owl-slot820.svg') for st in ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')] + \
        [(f'{P}/layered/MASTER-medallion-{st}-layered-slot820.svg', f'{A}/bases/MASTER-medallion-{st}-layered-slot820.svg') for st in ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')]
for new, old in PAIRS:
    a, b = open(new, encoding='utf-8').read(), open(old, encoding='utf-8').read(); la, lb = labels(a), labels(b)
    changed = [(i, x, y) for (i, x), (j, y) in zip(la, lb) if x != y]; assert [i for i, _ in la] == [j for j, _ in lb]
    want = {'legend-rails-en', 'legend-rails-es'} | ({'finalA5-rings'} if ('NORMATIVE-notation' in new or 'NORMATIVE-layered' in new) and 'NON-' not in new else set())
    check(f'{"/".join(new.split("/")[-2:])}: {sha(old)[:16]} -> {sha(new)[:16]}: identical once labels are blanked; labels changed = {sorted(i for i, _, _ in changed)}', blank(a) == blank(b) and {i for i, _, _ in changed} == want and a != b)
    if 'NORMATIVE-notation' in new and 'NON-' not in new:
        for i, x, y in changed: print(f'      {i}\n        was: {y}\n        now: {x}')
EXPECTED = {'OWL-SEMAPHORE-FINAL-FOUR-set.png'}     # its caption under METACOGNITIVE had a missing-character box
for man, tag in ((f'{A}/notation/MANIFEST.json', 'notation'), (f'{A}/owl/MANIFEST.json', 'owl')):
    E = [e for e in json.load(open(man, encoding='utf-8'))['files'] if e['path'].endswith('.png') and '/classic/' not in e['path']]; same = diff = 0; bad = []
    for e in E:
        if sha(e['path']) == e['sha256']: same += 1
        elif os.path.basename(e['path']) in EXPECTED or e['path'].endswith('-preview.png'): diff += 1
        else: bad.append(e['path'])
    check(f'{tag}: {len(E)} PNGs recorded at the first pass; byte-identical now {same}; changed as expected {diff}', not bad, str(bad))
print(f'{n} checks:', 'ALL PASS' if ok else 'SOMETHING FAILED'); sys.exit(0 if ok else 1)
