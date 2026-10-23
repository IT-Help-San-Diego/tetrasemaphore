#!/usr/bin/env python3
"""check-five.py: Claude Code's INDEPENDENT check of the five J4 screens against Science's spec revision 4 (a2131c898acbb0e8).
Written before the build agent reported; it reads only the output files, the sealed inputs and the spec's numbers typed below."""
import sys,os,re,json,subprocess,hashlib,glob
import numpy as np
from PIL import Image
ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2'; OUTD=ROOT+'/vector-masters/tetrasemaphore-build7-j4-screens'
S=os.path.dirname(os.path.abspath(__file__)); NODE='node'; PY=sys.executable
NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/'
COINS={'NORMATIVE':'e0b6366d5c032523','NON-NORMATIVE':'4ef1de6ae126279e','METACOGNITIVE':'cccfcff10dc74930','CRITICAL':'33413c4af9ec838c'}
MASTER=ROOT+'/vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg'
GROUND=(0x1D,0x25,0x2D); CREAM='#E8E0D2'; GOLD='#D4A853'
def sha16(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
def strip_inner(txt):
    m=re.search(r'<svg[^>]*>([\s\S]*)</svg>\s*$',txt); inner=m.group(1)
    inner=re.sub(r'\s+inkscape:[a-z-]+="[^"]*"','',inner); inner=re.sub(r'<title>[\s\S]*?</title>','',inner,1); inner=re.sub(r'<desc>[\s\S]*?</desc>','',inner,1); return inner
def prefix(inner,p):
    inner=re.sub(r'\bid="',f'id="{p}',inner); inner=inner.replace('url(#',f'url(#{p}'); inner=re.sub(r'(xlink:href|href)="#',lambda m:f'{m.group(1)}="#{p}',inner); return inner
def g_inner(txt,open_pat,start=0):
    i=txt.find(open_pat,start); assert i>=0, 'not found: '+open_pat[:80]
    j=txt.find('>',i)+1; depth=1; k=j; pat=re.compile(r'<g\b|</g>')
    while depth:
        m=pat.search(txt,k); assert m, 'unbalanced'; k=m.end(); depth+=1 if m.group()=='<g' else -1
    return txt[j:m.start()], i, m.end()
A=202.877
CARD=dict(op_y=1328.721,op_bl=1402.346,rule_y=1501.443,rule_bl=1575.068,div_T=-74.836,bl=[1803.635,1873.510,1943.385])
LOCK=dict(op_y=CARD['op_y']+A,op_bl=CARD['op_bl']+A,rule_y=CARD['rule_y']+A,rule_bl=CARD['rule_bl']+A,div_T=CARD['div_T']+A,bl=[b+A for b in CARD['bl']])
T1='translate(312 684) scale(0.708536585)'
SCREENS=[
 dict(name='NORMATIVE-flashcard',rows=CARD,coins=[('NORMATIVE',T1,'')],
      op=dict(text='I : (x, y) → (x, y)',w=604,bx=301.0,tx=344.625,stroke='#D5AF64',glyph='#C7B469',ng=1),
      rule=dict(text='∀g. I ∘ g = g',w=486,bx=360.0,tx=403.625),
      lines=[('I state the standard.',265.750),('It marks epistemic status,',175.375),('not infallibility.',354.125)]),
 dict(name='NON-NORMATIVE-flashcard',rows=CARD,coins=[('NON-NORMATIVE',T1,'')],
      op=dict(text='σᵥ : (x, y) → (−x, y)',w=704,bx=251.0,tx=294.625,stroke='#4FB5B5',glyph='#4FB5B5',ng=2),
      rule=dict(text='det(σᵥ) = −1',w=502,bx=352.0,tx=395.625),
      lines=[('I reflect the standard.',242.750),('It is reflection, not rejection.',131.375)]),
 dict(name='CRITICAL-flashcard',rows=CARD,coins=[('CRITICAL',T1,'')],
      op=dict(text='C₂ : (x, y) → (−x, −y)',w=746,bx=230.0,tx=273.625,stroke='#E25C60',glyph='#E25C60',ng=2),
      rule=dict(text='σᵥ ∘ σₕ = C₂',w=468,bx=369.0,tx=412.625),
      lines=[('I invert the standard.',252.625),('It is structured inversion,',186.125),('not reaction.',392.375)]),
 dict(name='ALL-FOUR-flashcard',rows=CARD,coins=[('NORMATIVE','translate(211.562 481.123) scale(0.437899692)','n-'),('NON-NORMATIVE','translate(635.361 481.123) scale(0.437899692)','nn-'),('METACOGNITIVE','translate(211.562 904.922) scale(0.437899692)','m-'),('CRITICAL','translate(635.361 904.922) scale(0.437899692)','c-')],
      op=dict(text='V₄ = {I, σᵥ, σₕ, C₂}',w=692,bx=257.0,tx=300.625,stroke=GOLD,glyph=CREAM,ng=0),
      rule=dict(text='∀g ∈ V₄. g ∘ g = I',w=650,bx=278.0,tx=321.625),
      lines=[('Four boxes;',411.500),('one move between any two;',141.250),('the way back is the same move.',79.250)]),
 dict(name='ALL-FOUR-lockscreen',rows=LOCK,coins=[('NORMATIVE','translate(110.123 481.123) scale(0.561605269)','n-'),('NON-NORMATIVE','translate(635.361 481.123) scale(0.561605269)','nn-'),('METACOGNITIVE','translate(110.123 1006.361) scale(0.561605269)','m-'),('CRITICAL','translate(635.361 1006.361) scale(0.561605269)','c-')],
      op=dict(text='V₄ = {I, σᵥ, σₕ, C₂}',w=692,bx=257.0,tx=300.625,stroke=GOLD,glyph=CREAM,ng=0),
      rule=dict(text='∀g ∈ V₄. g ∘ g = I',w=650,bx=278.0,tx=321.625),
      lines=[('Four boxes;',411.500),('one move between any two;',141.250),('the way back is the same move.',79.250)]),
]
master=open(MASTER,encoding='utf-8').read(); assert sha16(MASTER)=='1cf8f0f9f4aa30ea'
mdiv,_,_=g_inner(master,'<g inkscape:groupmode="layer" id="divider-1"')
coin_txt={st:open(NOT+f'MASTER-medallion-{st}-notation-slot820.svg',encoding='utf-8').read() for st in COINS}
for st,h in COINS.items(): assert sha16(NOT+f'MASTER-medallion-{st}-notation-slot820.svg')==h, st
coin_inner={st:strip_inner(t) for st,t in coin_txt.items()}
def num(s): return float(s)
def tr_y(tr):
    m=re.search(r'translate\(\s*([-\d.]+)[ ,]+([-\d.]+)\s*\)',tr or ''); return float(m.group(2)) if m else 0.0
def render(svg,png):
    r=subprocess.run([NODE,ROOT+'/tools/render.js',svg,png,'1206','none'],capture_output=True,text=True,cwd=ROOT); assert r.returncode==0, r.stderr[-500:]
    return np.asarray(Image.open(png).convert('RGBA')).astype(np.int16)
results={}; queries=[]; qref=[]
def q(text,x,bl,key): queries.append(dict(text=text,x=x,baseline=bl)); qref.append(key)
parsed={}
for sc in SCREENS:
    svg=f"{OUTD}/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-{sc['name']}-MASTER.svg"
    if not os.path.exists(svg): print('MISSING',svg); continue
    txt=open(svg,encoding='utf-8').read(); R=results[sc['name']]={'svg_sha16':sha16(svg)}
    R['text_or_image']=bool(re.search(r'<text\b|<image\b',txt))
    ids=re.findall(r'\bid="([^"]+)"',txt); dup=sorted({i for i in ids if ids.count(i)>1}); R['ids']=len(ids); R['dup_ids']=dup
    refs=re.findall(r'url\(#([^)]+)\)|(?:xlink:)?href="#([^"]+)"',txt); refs=[a or b for a,b in refs]; idset=set(ids); R['refs']=len(refs); R['unresolved']=sorted({r for r in refs if r not in idset})
    # coins: byte comparison with the master's stripped inner (prefixed as the spec says)
    cres=[]
    for st,tr,p in sc['coins']:
        inner,i0,i1=g_inner(txt,f'transform="{tr}"'); exp=prefix(coin_inner[st],p) if p else coin_inner[st]
        same=inner==exp; d=None
        if not same:
            k=0
            while k<min(len(inner),len(exp)) and inner[k]==exp[k]: k+=1
            d=dict(first_diff=k,len_out=len(inner),len_exp=len(exp),out=inner[max(0,k-50):k+70],exp=exp[max(0,k-50):k+70])
            # is it only a prefix-style difference?
            un=lambda s:re.sub(r'(id="|url\(#|href="#)'+re.escape(p),r'\1',s) if p else s
            d['same_after_unprefix']= un(inner)==coin_inner[st]
        # prefixed ids inside the coin all carry the prefix?
        cids=re.findall(r'\bid="([^"]+)"',inner); crefs=[a or b for a,b in re.findall(r'url\(#([^)]+)\)|(?:xlink:)?href="#([^"]+)"',inner)]
        cres.append(dict(state=st,transform=tr,prefix=p,byte_identical=same,diff=d,ids=len(cids),refs=len(crefs),ids_prefixed=all(i.startswith(p) for i in cids) if p else None,refs_prefixed=all(r.startswith(p) for r in crefs) if p else None, refs_inside=all(r in set(cids) for r in crefs)))
    R['coins']=cres
    # stack rows: layers in document order
    stack,s0,s1=g_inner(txt,re.search(r'<g\b[^>]*\bid="stack"[^>]*>',txt).group(0))
    layers=[]; pos=0
    while True:
        m=re.compile(r'<g\b[^>]*inkscape:groupmode="layer"[^>]*>').search(stack,pos)
        if not m: break
        inner,i0,i1=g_inner(stack,m.group(0),pos); layers.append(dict(open=m.group(0),inner=inner,T=tr_y(re.search(r'transform="([^"]*)"',m.group(0)).group(1) if 'transform=' in m.group(0) else '')) ); pos=i1
    R['layers']=[dict(open=l['open'][:120],T=l['T']) for l in layers]
    if len(layers)!=4: R['layer_count_problem']=len(layers)
    parsed[sc['name']]=(txt,layers)
    rows=sc['rows']
    # expected text runs: op row (local baseline = spec baseline - layer T), rule row, lines
    L=layers
    if len(L)>=4:
        q(sc['op']['text'],sc['op']['tx'],rows['op_bl']-L[0]['T'],(sc['name'],'op'))
        q(sc['rule']['text'],sc['rule']['tx'],rows['rule_bl']-L[1]['T'],(sc['name'],'rule'))
        for i,(t,x) in enumerate(sc['lines']): q(t,x,rows['bl'][i]-L[3]['T'],(sc['name'],'line%d'%i))
# one node call for all expected path data
json.dump(queries,open(S+'/q.json','w')); out=json.loads(subprocess.check_output([NODE,S+'/paths.js',S+'/q.json'],text=True)); exp={k:v['cp'] for k,v in zip(qref,out)}; expliga={k:v['liga'] for k,v in zip(qref,out)}
for sc in SCREENS:
    if sc['name'] not in parsed: continue
    txt,L=parsed[sc['name']]; R=results[sc['name']]; rows=sc['rows']
    if len(L)<4: continue
    def rects(inner): return re.findall(r'<rect ([^>]*)/>',inner)
    def attrs(s): return dict(re.findall(r'([\w:-]+)="([^"]*)"',s))
    def paths(inner): return [attrs(a) for a in re.findall(r'<path ([^>]*)/>',inner)]
    chk={}
    # row 1 (operator / V4)
    for name,li,spec,by,bl,stroke in (('op',0,sc['op'],rows['op_y'],rows['op_bl'],sc['op']['stroke']),('rule',1,sc['rule'],rows['rule_y'],rows['rule_bl'],GOLD)):
        l=L[li]; rs=rects(l['inner']); a=attrs(rs[0]) if rs else {}
        geo=dict(x=num(a.get('x','nan'))-(spec['bx']+2), y=num(a.get('y','nan'))+l['T']-(by+2), w=num(a.get('width','nan'))-(spec['w']-4), h=num(a.get('height','nan'))-104, rx=num(a.get('rx','nan'))-26, sw=num(a.get('stroke-width','nan'))-4) if a else None
        ps=paths(l['inner']); d=''.join(p.get('d','') for p in ps); e=''.join(exp[(sc['name'],name)]['parts'])
        fills=[p.get('fill') for p in ps]
        if name=='op':
            ng=spec['ng']; eg=''.join(exp[(sc['name'],name)]['parts'][:ng]) if ng else ''
            fill_ok=(fills==[spec['glyph'],CREAM] and ps[0].get('d')==eg) if ng else all(f==CREAM for f in fills)
        else: fill_ok=all(f==CREAM for f in fills)
        chk[name]=dict(rects=len(rs),stroke_ok=a.get('stroke')==stroke and a.get('fill')=='none',geo_max_dev=max(abs(v) for v in geo.values()) if geo else None,paths=len(ps),path_data_exact=(d==e),fills=fills,fill_ok=fill_ok,advance=exp[(sc['name'],name)]['advance'])
    # divider: byte-identical to the master's divider-1 layer, at the spec transform
    chk['divider']=dict(byte_identical=L[2]['inner']==mdiv,T=L[2]['T'],T_ok=abs(L[2]['T']-rows['div_T'])<0.0005)
    # lines
    ps=paths(L[3]['inner']); d=''.join(p.get('d','') for p in ps); e=''.join(''.join(exp[(sc['name'],'line%d'%i)]['parts']) for i in range(len(sc['lines'])))
    el=''.join(''.join(expliga[(sc['name'],'line%d'%i)]['parts']) for i in range(len(sc['lines'])))
    chk['lines']=dict(paths=len(ps),path_data_exact=d==e,matches_ligature_form=(d==el),ligature_form_differs=(e!=el),fills_cream=all(p.get('fill')==CREAM for p in ps),rects=len(rects(L[3]['inner'])),adv=[exp[(sc['name'],'line%d'%i)]['advance'] for i in range(len(sc['lines']))],adv_liga=[expliga[(sc['name'],'line%d'%i)]['advance'] for i in range(len(sc['lines']))])
    # anything else in the stack? total path count
    chk['stack_total']=dict(paths=sum(len(paths(l['inner'])) for l in L),rects=sum(len(rects(l['inner'])) for l in L))
    R['rows']=chk
    # renders: my own render vs the agent's PNG; bands; per-coin alone renders
    svg=f"{OUTD}/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-{sc['name']}-MASTER.svg"; png=svg.replace('-MASTER.svg','.png'); png=png if os.path.exists(png) else svg.replace('-MASTER.svg','-MASTER.png')
    mine=render(svg,f"{S}/{sc['name']}-mine.png")
    if os.path.exists(png):
        theirs=np.asarray(Image.open(png).convert('RGBA')).astype(np.int16); R['png_sha16']=sha16(png); R['png_pixels_equal_my_render']=bool(mine.shape==theirs.shape and np.array_equal(mine,theirs))
    g=np.array(GROUND+(255,),dtype=np.int16); nong=lambda a:int(np.any(a!=g,axis=2).sum())
    R['band_ink']=dict(top_0_450=nong(mine[0:450]),bottom_2360_2622=nong(mine[2360:2622]),alpha_min=int(mine[...,3].min()))
    root=re.search(r'<svg[^>]*>',coin_txt['NORMATIVE']).group(0)
    pc=[]
    for st,tr,p in sc['coins']:
        r=re.sub(r'\s(width|height|viewBox)="[^"]*"','',re.search(r'<svg[^>]*>',coin_txt[st]).group(0))[:-1]+' width="1206" height="2622" viewBox="0 0 1206 2622">'
        alone=r+f'<rect x="0" y="0" width="1206" height="2622" fill="#1D252D"/><g transform="{tr}">'+coin_inner[st]+'</g></svg>'
        ap=f"{S}/{sc['name']}-{st}-alone.svg"; open(ap,'w',encoding='utf-8').write(alone); al=render(ap,ap.replace('.svg','.png'))
        m=re.search(r'translate\(([-\d.]+) ([-\d.]+)\) scale\(([-\d.]+)\)',tr); x0,y0,s=float(m.group(1)),float(m.group(2)),float(m.group(3)); side=820*s
        import math; ys=slice(math.floor(y0),math.ceil(y0+side)); xs=slice(math.floor(x0),math.ceil(x0+side))
        diff=np.abs(mine[ys,xs,:3]-al[ys,xs,:3]); pc.append(dict(state=st,max=int(diff.max()),mean=round(float(diff.mean()),6),box=[xs.start,ys.start,xs.stop,ys.stop]))
    R['per_coin_render']=pc
# tags
pngs=sorted(glob.glob(OUTD+'/*.png'))
if pngs:
    r=subprocess.run([PY,ROOT+'/tools/png_tag.py','--check']+pngs,capture_output=True,text=True); results['_tags']=r.stdout.strip().splitlines()[-1]
json.dump(results,open(S+'/check-five-run.json','w'),indent=1,ensure_ascii=False)
# summary
for name,R in results.items():
    if name.startswith('_'): print(name,R); continue
    ok=lambda b:'PASS' if b else 'FAIL'
    print(f"\n== {name}  svg {R['svg_sha16']}  png {R.get('png_sha16','-')}")
    print(f"  text/image {ok(not R['text_or_image'])} | ids {R['ids']} dup {ok(not R['dup_ids'])} | refs {R['refs']} unresolved {ok(not R['unresolved'])} {R['unresolved'][:5]}")
    for c in R['coins']: print(f"  coin {c['state']:14s} {c['prefix'] or '-':3s} byte-identical {ok(c['byte_identical'])}" + ('' if c['byte_identical'] else f" (first diff {c['diff']['first_diff']}, same after unprefix {c['diff']['same_after_unprefix']})") + f" ids {c['ids']} refs {c['refs']} prefixed {c['ids_prefixed']}/{c['refs_prefixed']} inside {ok(c['refs_inside'])}")
    if 'rows' in R:
        for k in ('op','rule'): v=R['rows'][k]; print(f"  {k:5s} rect {v['rects']} stroke {ok(v['stroke_ok'])} geo dev {v['geo_max_dev']} | paths {v['paths']} data {ok(v['path_data_exact'])} fills {ok(v['fill_ok'])} {v['fills']} adv {v['advance']}")
        v=R['rows']['divider']; print(f"  divider byte-identical {ok(v['byte_identical'])} T {v['T']} {ok(v['T_ok'])}")
        v=R['rows']['lines']; print(f"  lines paths {v['paths']} data(code points) {ok(v['path_data_exact'])} ligature-form differs {v['ligature_form_differs']} (matches liga {v['matches_ligature_form']}) cream {ok(v['fills_cream'])} rects {v['rects']} adv {v['adv']} adv_liga {v['adv_liga']}")
        print(f"  stack totals {R['rows']['stack_total']}")
    if 'band_ink' in R: print(f"  bands {R['band_ink']} | png = my render {ok(R.get('png_pixels_equal_my_render'))}")
    for c in R.get('per_coin_render',[]): print(f"  per-coin render {c['state']:14s} max {c['max']} mean {c['mean']}")
print('\nrun json:',S+'/check-five-run.json')
