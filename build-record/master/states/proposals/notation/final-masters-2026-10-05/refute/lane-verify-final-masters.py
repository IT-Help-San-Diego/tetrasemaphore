#!/usr/bin/env python3
"""Lane's own vector check of the four final masters against the build sheet and Science's reference files (run from the repo root)."""
import re, math, hashlib, sys
import xml.etree.ElementTree as ET
F='master/states/proposals/notation/final-masters-2026-10-05'; REF='/Users/careybalboa/Downloads/TETRASEMAPHORE-SCIENCE-REFERENCE-%s.svg'
MMU=102.785/820; R_RING=291.745; C=410.0
sha16=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
def node(s, gid):
    i=s.index(f'id="{gid}"'); i=s.rfind('<g',0,i); d=0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        if m.group(0)=='</g>':
            d-=1
            if d==0: return s[i:i+m.end()]
        else:
            gt=s.index('>', i+m.start())
            if s[gt-1]!='/': d+=1
rects=lambda g: sorted(tuple(round(float(v),3) for v in r) for r in re.findall(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', g))
ok=True
def check(name, cond, detail=''):
    global ok; ok&=bool(cond); print(('PASS' if cond else 'FAIL'), name, detail)
ORDER=['field','finalA5-rings','finalA5-geometry','finalA5-finish','finalA5-litedge','legend-plaque-en','legend-text-en','legend-plaque-es','legend-text-es','glyph-placement','symmetry-marks']   # finalA5-litedge since build 6 (2026-10-10): the lit edge, one layer above the finish
FIELD={'NORMATIVE':'#181403','NON-NORMATIVE':'#001817','METACOGNITIVE':'#17121D','CRITICAL':'#1F100E'}
G={}
for st in ('NORMATIVE','NON-NORMATIVE','METACOGNITIVE','CRITICAL'):
    p=f'{F}/MASTER-medallion-{st}-notation-slot820.svg'; s=open(p,encoding='utf-8').read(); ref=open(REF%st,encoding='utf-8').read()
    root=ET.fromstring(s); kids=[c.get('id') for c in root if c.get('id')]
    want=[o for o in ORDER if not (o=='symmetry-marks' and st=='CRITICAL')]
    print(f'\n== {st} {sha16(p)}  ({len(s.encode())} bytes)')
    check('layer order', kids==want, str(kids))
    check('zero raster images / live text / font refs', not re.search(r'<image|<text|<tspan|font-family|data:', s))
    ids=[e.get('id') for e in root.iter() if e.get('id')]; check('ids unique', len(ids)==len(set(ids)), f'{len(ids)} ids')
    refs=set(re.findall(r'url\(#([^)]+)\)', s))|set(re.findall(r'href="#([^"]+)"', s)); check('every url(#…)/href target exists', refs<=set(ids), str(sorted(refs-set(ids)))[:200])
    f=re.search(r'<g id="field"[^>]*><circle cx="410" cy="410" r="([\d.]+)" fill="(#[0-9A-Fa-f]{6})"/></g>', s); rf=re.search(r'<g id="field"><circle cx="410" cy="410" r="([\d.]+)" fill="(#[0-9A-Fa-f]{6})"/></g>', ref)
    check('field tint and radius = sheet and reference', f and f.group(2)==FIELD[st] and f.groups()==rf.groups(), f.groups() if f else 'none')
    check('Spanish legend layers hidden, English shown', s.count('style="display:none"')==2 and 'id="legend-plaque-en" inkscape:groupmode="layer" inkscape:label' in s)
    check('title names the state; no owl anywhere', re.search(r'<title>Tetrasemaphore %s medallion'%re.escape(st), s) and 'owl' not in s)
    g=node(s,'glyph-placement'); gr=node(ref,'glyph-placement'); G[st]=g
    tf=re.search(r'transform="([^"]*)"', g[:g.index('>')]).group(1)
    sc=math.prod(float(x) for x in re.findall(r'scale\(([\d.]+)\)', tf)); tfr=re.search(r'transform="([^"]*)"', gr[:gr.index('>')]).group(1); scr=math.prod(float(x) for x in re.findall(r'scale\(([\d.]+)\)', tfr))
    check('glyph placement scale vs reference', abs(sc/scr-1)<2e-5, f'ours {sc:.6f}  reference {scr:.6f}  (ratio {sc/scr:.6f})')
    pth=lambda x: re.findall(r'<path d="([^"]*)"', x)
    if st!='NORMATIVE': check('glyph path data identical to the reference', pth(g)==pth(gr), f'{len(pth(g))} paths')
    else: check('I path identical to the reference; outline is one path M L T R B Z M L R', pth(g)[0]==pth(gr)[0] and pth(g)[1]=='M465.65 700.5L700.5 293.73L935.35 700.5L700.5 1107.27ZM465.65 700.5L935.35 700.5', pth(g)[1])
    if st!='CRITICAL':
        m=node(s,'symmetry-marks'); mr=node(ref,'symmetry-marks'); a,b=rects(m),rects(mr)
        dmax=max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb)) if len(a)==len(b) else 9
        check('symmetry marks: count and positions vs reference', len(a)==len(b) and dmax<=0.012, f'{len(a)} bars, largest coordinate difference {dmax:.4f} slot units = {dmax*MMU:.4f} mm')
        fill=re.search(r'fill="(#[0-9A-Fa-f]{6})"', m[:m.index('>')]).group(1); check('marks colour = reference', fill==re.search(r'fill="(#[0-9A-Fa-f]{6})"', mr[:mr.index('>')]).group(1), fill)
        far=max(math.hypot(max(abs(x-C),abs(x+w-C)), max(abs(y-C),abs(y+h-C))) for x,y,w,h in a)
        print(f'     marks: farthest corner {far*MMU:.4f} mm from the centre -> {(R_RING-far)*MMU:.4f} mm from the ring')
        G[st+'-marks-clear']=(R_RING-far)*MMU
# CRITICAL triangle tip (the floor): polygon points in glyph units, stroke 21.7, miter; glyph transform scale 0.575388 about 700.5
g=G['CRITICAL']; pts=re.search(r'<polygon points="([^"]*)"', g).group(1); P=[tuple(map(float,q.split(','))) for q in pts.split()]
sw=float(re.search(r'stroke-width="([\d.]+)"', g).group(1)); far=0
for i,v in enumerate(P):
    a_,b_=P[i-1],P[(i+1)%3]; u1=(a_[0]-v[0],a_[1]-v[1]); u2=(b_[0]-v[0],b_[1]-v[1]); n1=math.hypot(*u1); n2=math.hypot(*u2)
    half=math.acos((u1[0]*u2[0]+u1[1]*u2[1])/(n1*n2))/2; bis=((u1[0]/n1+u2[0]/n2),(u1[1]/n1+u2[1]/n2)); nb=math.hypot(*bis)
    tip=(v[0]-bis[0]/nb*(sw/2)/math.sin(half), v[1]-bis[1]/nb*(sw/2)/math.sin(half))
    for sgn in (1,-1):   # the triangle and its half turn about (700.5,700.5)
        t=(700.5+sgn*(tip[0]-700.5), 700.5+sgn*(tip[1]-700.5)); far=max(far, math.hypot(t[0]-700.5,t[1]-700.5))
# the second triangle is the half turn of the first about the glyph centre, so the same radius; but the pair is offset: use the uses' transforms
uses=re.findall(r'<use[^>]*xlink:href="#tri[^"]*"[^>]*/>', g); print('     CRITICAL triangle uses:', [re.sub(r'xlink:href','h',u)[:110] for u in uses])
crit_clear=(R_RING-far*0.575388)*MMU; print(f'     CRITICAL: farthest outer miter tip {far*0.575388*MMU:.4f} mm from the centre -> {crit_clear:.4f} mm from the ring (the floor; sheet says 2.316)')
# twins
gm,gn=G['METACOGNITIVE'],G['NON-NORMATIVE']; num=lambda rx,x: [float(v) for v in re.search(rx,x).groups()]
sm=re.search(r'scale\(([\d.]+)\)', gm).group(1); sn=re.search(r'scale\(([\d.]+)\)', gn).group(1); k=float(sm)*MMU
check('\nTWINS: same placement scale string', sm==sn=='0.918549', f'{sm} / {sn}; sigma ink height {484*0.3*k:.3f} mm')
pm=re.findall(r'<path d="([^"]*)"', gm); pn=re.findall(r'<path d="([^"]*)"', gn); check('TWINS: same sigma path; token transforms equal', pm[0]==pn[0] and re.findall(r'<g transform="([^"]*)">', gm)==re.findall(r'<g transform="([^"]*)">', gn))
rm=dict(zip('xywh',num(r'<rect id="glyph-fix"[^>]*x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', gm))); rn=dict(zip('xywh',num(r'<rect id="glyph-fix"[^>]*x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', gn)))
Yh=abs(float(re.search(r'<use[^>]*transform="translate\(0 (-?[\d.]+)\)"', gm).group(1))); X=abs(float(re.search(r'<use[^>]*transform="translate\((-?[\d.]+) [\d.]+\)"', gn).group(1))); Yb=float(re.search(r'<use[^>]*transform="translate\(-?[\d.]+ ([\d.]+)\)"', gn).group(1))
line=(rm['h'],rn['w']); air=(Yh-63-rm['h']/2, X-284.25-rn['w']/2); over=(10.5-rm['x'], rm['x']+rm['w']-296.01, (Yb-141.3)-rn['y'], rn['y']+rn['h']-(Yb+64.26))
check('TWINS: gold line weight identical (9.3307 units)', line[0]==line[1]==9.3307, f'{line[0]*k:.4f} mm')
check('TWINS: air identical', abs(air[0]-air[1])<1e-6, f'{air[0]*k:.4f} / {air[1]*k:.4f} mm')
check('TWINS: overhang identical at all four ends', max(over)-min(over)<1e-6, f'{[round(o*k,4) for o in over]} mm')
mk=lambda st: rects(node(open(f'{F}/MASTER-medallion-{st}-notation-slot820.svg',encoding='utf-8').read(),'symmetry-marks'))
a=mk('METACOGNITIVE'); b=sorted((y,x,h,w) for x,y,w,h in mk('NON-NORMATIVE'))   # quarter-turn the vertical-line marks onto the horizontal line
dm=max(abs(p-q) for ra,rb in zip(a,b) for p,q in zip(ra,rb)); gapm=[(x-C if x>C else C-(x+w)) for x,y,w,h in a]; gapn=[(y-C if y>C else C-(y+h)) for x,y,w,h in mk('NON-NORMATIVE')]
print(f'     marks: METACOGNITIVE inner edges {sorted(set(round(v*MMU,3) for v in gapm))} mm from the centre (line end {168.105*k:.3f}); NON-NORMATIVE {sorted(set(round(v*MMU,3) for v in gapn))} (line end {128.13*k:.3f})')
check('TWINS: marks the same size and the same distance beyond each line end', {(w,h) for x,y,w,h in a}=={(h,w) for x,y,w,h in mk('NON-NORMATIVE')} and abs((min(gapm)-168.105*float(sm))-(min(gapn)-128.13*float(sn)))<2e-3, f'offset beyond the line end {(min(gapm)-168.105*float(sm))*MMU:.4f} / {(min(gapn)-128.13*float(sn))*MMU:.4f} mm')
# clearance of the sigma-v outer sigma: sample the sigma outline (font units) -> slot units
def bez(d):
    t=re.findall(r'[MLHVCZ]|-?\d+\.?\d*', d); i=0; cur=(0,0); pts=[]; cmd=None
    while i<len(t):
        if t[i].isalpha(): cmd=t[i]; i+=1
        if cmd=='M' or cmd=='L': cur=(float(t[i]),float(t[i+1])); i+=2; pts.append(cur)
        elif cmd=='H': cur=(float(t[i]),cur[1]); i+=1; pts.append(cur)
        elif cmd=='V': cur=(cur[0],float(t[i])); i+=1; pts.append(cur)
        elif cmd=='C':
            p=[cur]+[(float(t[i+2*j]),float(t[i+2*j+1])) for j in range(3)]; i+=6
            for q in range(1,201):
                u=q/200; pts.append(tuple(sum(c*v for c,v in zip(((1-u)**3,3*(1-u)**2*u,3*(1-u)*u*u,u**3),[pp[a] for pp in p])) for a in (0,1)))
            cur=p[3]
        elif cmd=='Z': pass
    return pts
far=0
for (px,py) in bez(pn[0]):                       # sigma in font units, y up; token: scale 0.30, flipped; left copy at translate(-X, Yb)
    x=-X+0.30*px; y=Yb-0.30*py; far=max(far, math.hypot(x,y)*float(sn))
for (px,py) in bez(pn[1]):                       # v.ssty at translate(163.5,-63) scale 0.21
    x=-X+163.5+0.21*px; y=Yb-(-63+0.21*py); far=max(far, math.hypot(x,y)*float(sn))
sv_clear=(R_RING-far)*MMU; print(f'     NON-NORMATIVE: farthest letter ink {far*MMU:.4f} mm from the centre -> {sv_clear:.4f} mm from the ring')
check('CLEARANCE: every coin, marks included, at least the CRITICAL tip distance', min(sv_clear, G['NORMATIVE-marks-clear'], G['NON-NORMATIVE-marks-clear'], G['METACOGNITIVE-marks-clear'])>=crit_clear-1e-9,
      f'floor {crit_clear:.4f}; NON-NORMATIVE letters {sv_clear:.4f}; NORMATIVE marks {G["NORMATIVE-marks-clear"]:.4f}')
print('\nALL PASS' if ok else '\nSOMETHING FAILED'); sys.exit(0 if ok else 1)
