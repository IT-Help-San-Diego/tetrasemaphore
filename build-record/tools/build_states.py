#!/usr/bin/env python3
"""build_states.py [--check] — the ONE generator for the Dose 01 state medallions.
Reads master/states/states-config.json. Guard first: rebuilds the approved METACOGNITIVE shirt master from its config and
requires byte-identity with master/MASTER-medallion-METACOGNITIVE-slot820.svg. Then emits master/states/MASTER-medallion-<STATE>-slot820.svg.
Colours come only from owl_hex / ring_hex in the config; ring and owl labels are generated from them, so no file can carry a stale hex.
--check: build into a temp dir and compare with the files on disk (idempotency); exits 1 on any difference."""
import json, os, re, subprocess, sys, tempfile, hashlib, shlex
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(D)
C=json.load(open('master/states/states-config.json')); common=C['common']
APPROVED_OWL, APPROVED_RING = '#B498E6', '#8C4191'   # colours carried by the owl source file (pre-legend approved master)
def sh(*a): r=subprocess.run(a,capture_output=True,text=True); assert r.returncode==0, (a, r.stderr); return r.stdout
def build(cfg, out, approved_labels=False):
    k=common[cfg['keys']]; tmp=out+'.noplaque.tmp.svg'
    sh('python3','tools/compose.py',k['ring'],common['owl_source'],tmp)
    s=open(tmp).read()
    if not approved_labels:
        assert s.count(f'fill="{APPROVED_OWL}"')==2; s=s.replace(f'fill="{APPROVED_OWL}"', f'fill="{cfg["owl_hex"]}"')
        m=re.search(r'(<g id="finalA5-rings"[^>]*>)(.*?)(</g>)', s, re.S); head,inner=m.group(1),m.group(2)
        assert inner.count(f'stroke="{APPROVED_RING}"')==2
        head=re.sub(r'inkscape:label="1 [^"]*"', f'inkscape:label="1 {cfg["name"]} rings {cfg["ring_hex"]} (state colour; owl {cfg["owl_hex"]})"', head)
        s=s[:m.start()]+head+inner.replace(f'stroke="{APPROVED_RING}"', f'stroke="{cfg["ring_hex"]}"')+m.group(3)+s[m.end():]
        if cfg.get('operator'):
            old=re.search(r'<g id="owl-placement" inkscape:label="[^"]*" transform="([^"]*)">', s); assert old
            s=s[:old.start()]+f'<g id="owl-placement" inkscape:label="4a owl placement: V4 operator for {cfg["name"]} about the medallion centre (410,410), then the approved placement" transform="{cfg["operator"]} {old.group(1)}">'+s[old.end():]
        assert '#8C4191' not in s or cfg['ring_hex']=='#8C4191'
    open(tmp,'w').write(s)
    sh('node','tools/legend.js',tmp,out,'--word',cfg['word'],'--a0',str(k['a0']),'--a1',str(k['a1']),'--track',str(cfg['track']),*shlex.split(common['legend_knobs']))
    os.remove(tmp)
def h(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
check='--check' in sys.argv; outdir=tempfile.mkdtemp() if check else 'master/states'
g=C['guard']; gout=os.path.join(tempfile.mkdtemp(),'guard.svg'); build(g,gout,approved_labels=True)
ok=h(gout)==h(g['out']); print('GUARD', 'PASS' if ok else 'FAIL', h(gout), 'vs', g['out'], h(g['out']))
if not ok: sys.exit(1)
bad=0
for st in C['states']:
    out=os.path.join(outdir,f'MASTER-medallion-{st["name"]}-slot820.svg'); build(st,out)
    if check:
        disk=f'master/states/MASTER-medallion-{st["name"]}-slot820.svg'; same=os.path.exists(disk) and h(out)==h(disk); bad+=not same
        print(st['name'], 'IDENTICAL' if same else 'DIFFERS', h(out))
    else: print(st['name'], h(out), 'owl', st['owl_hex'], 'rings', st['ring_hex'])
sys.exit(1 if bad else 0)
