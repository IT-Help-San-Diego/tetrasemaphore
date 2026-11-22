# Verify the build-7 METACOGNITIVE lock screen against the 16 Sep master, the build-7 coin and the build-6 screen; cut the proof pictures.
# Usage: verify-meta7.py <scratch dir holding old-1206.png (the 16 Sep master rendered at 1206) and set-METACOGNITIVE-3618.png>
import re, sys, json, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2'; O=ROOT+'/vector-masters/tetrasemaphore-build7'; O6=ROOT+'/vector-masters/tetrasemaphore-build6'; S=sys.argv[1]
NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/'
h16=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
old=open(ROOT+'/vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg',encoding='utf-8').read()
st='METACOGNITIVE'
def strip(s):
    a=s.index('<g inkscape:groupmode="layer" id="medallion"'); b=s.index('<g inkscape:groupmode="layer" id="stack"'); s=s[:a]+s[b:]
    s=re.sub(r'<desc>.*?</desc>','',re.sub(r'<title>.*?</title>','',s,flags=re.S),flags=re.S)
    m=re.search(r'<g inkscape:groupmode="layer" id="(sigma-h|operator)"[^>]*>.*?</g>',s,flags=re.S); return s[:m.start()]+'@ROW@'+s[m.end():]
MARK='<g id="medallion-slot820" transform="translate(312 684) scale(0.708536585)">'
def inner(s): a=s.index(MARK)+len(MARK); b=s.index('</g></g>\n\n<g inkscape:groupmode="layer" id="stack"'); return s[a:b]
o=np.asarray(Image.open(S+'/old-1206.png').convert('RGBA')).astype(int); yy,xx=np.mgrid[0:2622,0:1206]; r=np.hypot(xx+0.5-602.5,yy+0.5-974.5)
band=(yy>=1325)&(yy<=1440); outside=(r>292)&~band
f=O+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}-MASTER.svg'; s=open(f,encoding='utf-8').read()
f6=O6+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}-MASTER.svg'; s6=open(f6,encoding='utf-8').read()
coin=open(NOT+f'MASTER-medallion-{st}-notation-slot820.svg',encoding='utf-8').read()
cin=re.search(r'<svg[^>]*>(.*)</svg>\s*$',coin,re.S).group(1); cin=re.sub(r'<desc>.*?</desc>','',re.sub(r'<title>.*?</title>','',re.sub(r'\s+inkscape:[a-z-]+="[^"]*"','',cin),flags=re.S),flags=re.S)
a=np.asarray(Image.open(O+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}.png').convert('RGBA')).astype(int)
a6=np.asarray(Image.open(O6+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}.png').convert('RGBA')).astype(int)
d=np.abs(o-a).max(-1); ys,xs=np.nonzero(d*band); d6=np.abs(a6-a).max(-1); y6,x6=np.nonzero(d6)
rect=re.search(r'id="operator"[^>]*>(<rect[^>]*>)',s).group(1); bx=float(re.search(r' x="([\d.]+)"',rect).group(1))-2; bw=float(re.search(r'width="([\d.]+)"',rect).group(1))+4
# the build-6 and build-7 screens: identical text outside the medallion, the title and the desc (the row is the same bytes)
t7=re.sub(r'<desc>.*?</desc>','',re.sub(r'<title>.*?</title>','',s,flags=re.S),flags=re.S); t6=re.sub(r'<desc>.*?</desc>','',re.sub(r'<title>.*?</title>','',s6,flags=re.S),flags=re.S)
m7=re.search(r'<g inkscape:groupmode="layer" id="medallion".*?</g></g>\n\n',t7,re.S); m6=re.search(r'<g inkscape:groupmode="layer" id="medallion".*?</g></g>\n\n',t6,re.S)
R={'sha16':h16(f),'coin_sha16':h16(NOT+f'MASTER-medallion-{st}-notation-slot820.svg'),'build6_screen_sha16':h16(f6),
   'text_identical_outside_medallion_and_row_vs_16_sep_master':strip(old)==strip(s),'coin_inlined_verbatim':inner(s)==cin,
   'text_identical_to_build6_screen_outside_medallion_title_desc':(t7[:m7.start()]+t7[m7.end():])==(t6[:m6.start()]+t6[m6.end():]),
   'px_differing_outside_coin_and_row_band_vs_16_sep_render':int((d[outside]>0).sum()),'row_band_diff_bbox':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None,
   'px_differing_vs_build6_screen':int((d6>0).sum()),'max_level_vs_build6':int(d6.max()),'vs_build6_bbox':[int(x6.min()),int(y6.min()),int(x6.max()),int(y6.max())] if len(x6) else None,
   'px_differing_vs_build6_outside_coin':int((d6[r>292]>0).sum()),
   'box':{'x':bx,'w':bw,'centre':bx+bw/2},'alpha_all_255':bool((a[...,3]==255).all()),'ids':len(re.findall(r'\bid="',s)),'dup_ids':len(re.findall(r'\bid="',s))-len(set(re.findall(r'\bid="([^"]+)"',s)))}
print(json.dumps(R,indent=1)); open(O+'/work/verify-meta7-run.json','w').write(json.dumps(R,indent=1)+'\n')
fnt=lambda sz: ImageFont.truetype('/Users/careybalboa/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf',sz)
def strip_(ims,caps,out,gap=40,bar=90,bg=(14,14,18)):
    W=sum(i.width for i in ims)+gap*(len(ims)+1); H=max(i.height for i in ims)+bar+gap; im=Image.new('RGB',(W,H),bg); dr=ImageDraw.Draw(im); ft=fnt(max(22,W//90)); x=gap
    for i,c in zip(ims,caps): im.paste(i,(x,bar)); dr.text((x,gap//2),c,fill=(236,230,216),font=ft); x+=i.width+gap
    im.save(out)
P=O+'/proofs'
strip_([Image.open(O6+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}.png').convert('RGB'),Image.open(O+f'/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-{st}.png').convert('RGB')],['METACOGNITIVE, build 6 (accepted by eye, 11 Oct)','METACOGNITIVE, build 7 (the guarded lit edge)'],P+'/TETRASEMAPHORE-LOCKSCREEN-METACOGNITIVE-build6-vs-build7-1206.png')
strip_([Image.open(S+f'/set-{st}-3618.png').convert('RGB').crop((450,2000,3170,4420))],['METACOGNITIVE, build 7: the coin and its operator row, three times screen size'],P+'/TETRASEMAPHORE-LOCKSCREEN-METACOGNITIVE-build7-coin-and-row-3x.png')
print('pictures done')
