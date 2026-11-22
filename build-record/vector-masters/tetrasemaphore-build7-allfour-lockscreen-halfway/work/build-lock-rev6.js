// build-lock-rev6.js (2026-10-22): the fifth lock screen, all four states, at the HALFWAY layout Carey chose on 22 Oct (FINISH-TODAY update 19,
// 02:24Z, "spec revision 6"; his words, decisions-via-Science item 73: "hit the halfway point for the master ... take that text up a hair more, and
// the four down a tiny little bit more"; mock-up TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MOCKUP-1206x2622.png 6902002ccfe5fdeb).
// Derived from build-five.js (the sealed J4 generator, af3ab4e85e5b1c1c): every mechanism unchanged (the regression gates, the coin inlining with
// prefixed ids, the row generator, the layer swap on the 16 Sep no-title master); only the four coin transforms and the stack's dy differ:
//   1. each coin 391.5 px across, centred at (375.75, 864.75), (829.25, 864.75), (375.75, 1318.25), (829.25, 1318.25) (NORMATIVE, NON-NORMATIVE,
//      METACOGNITIVE, CRITICAL); scale 391.5/820 = 0.477439024 (= 0.8501 of the built 460.516 px coins; update 19's "scale 0.8492" would give
//      391.07 px, 0.43 px smaller: the stated diameter 391.5 px is followed, and the difference is reported for Science to rule);
//   2. every text row, both boxes and the divider +48 px from the built screen (dy 202.877 + 48 = 250.877): strings, sizes, x unchanged.
// Usage: node build-lock-rev6.js            (gates, then the SVG + work/layout_report.json)
//        node build-lock-rev6.js --gates-only
const fs=require('fs'), crypto=require('crypto'), path=require('path'); const T=require('../lockscreen/textlayout.js'); const n=T.n;
const ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2', VM=ROOT+'/vector-masters', OUT=process.env.J4R6_OUT||VM+'/tetrasemaphore-build7-allfour-lockscreen-halfway';
const CANON=VM+'/work/lockscreen-tetrasemaphore/build-lock-rev6.js'; if(path.resolve(__filename)!==CANON) throw new Error('run build-lock-rev6.js from its canonical path '+CANON+' (the copy in work/ is the record, not a runnable)');
const SPEC=VM+'/work/lockscreen-tetrasemaphore/spec-rev6/FINISH-TODAY-update-19.md', SPEC16='645fbdab25c36d57';
const MOCK='/Users/careybalboa/Downloads/TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MOCKUP-1206x2622.png', MOCK16='6902002ccfe5fdeb';
const FT='/Users/careybalboa/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-FINISH-TODAY.md';
const SRC=VM+'/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg', SRC16='1cf8f0f9f4aa30ea';
const TPL=VM+'/tetrasemaphore-build7/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE-MASTER.svg', TPL16='a62a3dd185089960';
const PREV=VM+'/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-MASTER.svg', PREV16='d551d3c339cdd915';
const NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/', FONT16='7e69e81478e233b8';
const GATES_ONLY=process.argv.includes('--gates-only');
const sha16=b=>crypto.createHash('sha256').update(b).digest('hex').slice(0,16);
const must=(c,m)=>{ if(!c) throw new Error(m); };
must(sha16(fs.readFileSync(SPEC))===SPEC16,'spec record is not update 19 (645fbdab25c36d57)');
must(sha16(fs.readFileSync(MOCK))===MOCK16,'mock-up is not 6902002ccfe5fdeb');
must(sha16(fs.readFileSync(SRC))===SRC16,'no-title lock-screen master moved');
must(sha16(fs.readFileSync(TPL))===TPL16,'build-7 METACOGNITIVE template moved');
must(sha16(fs.readFileSync(PREV))===PREV16,'the built (revision 5) lock screen moved');
must(sha16(fs.readFileSync(T.FONT))===FONT16,'font is not 7e69e81478e233b8');
const FT16=sha16(fs.readFileSync(FT));
const COINS={
 'NORMATIVE':    {hash:'e0b6366d5c032523',ring:'#D5AF64',glyph:'#C7B469',field:'#181403',prefix:'n-'},
 'NON-NORMATIVE':{hash:'4ef1de6ae126279e',ring:'#4FB5B5',glyph:'#4FB5B5',field:'#001817',prefix:'nn-'},
 'METACOGNITIVE':{hash:'cccfcff10dc74930',ring:'#B498E6',glyph:'#B498E6',field:'#17121D',prefix:'m-'},
 'CRITICAL':     {hash:'33413c4af9ec838c',ring:'#E25C60',glyph:'#E25C60',field:'#1F100E',prefix:'c-'},
};
const SIZE=58, AXIS=603, PAD=43.625, SW=4, R=28, BOXH=108, CREAM='#E8E0D2', GOLD='#D4A853', PITCH=69.875;
const BOXY1=1453, BASE1=1526.625, BOXY2=1601, BASE2=1674.625, DIVCY=1759, MOT1=1853.75;
const TY={operator:-124.279, forall:-99.557, 'divider-1':-74.836, cogito:-50.115}, LOCK_DY=202.877, SHIFT=48, DY=LOCK_DY+SHIFT;
// ---- text (build-five.js, verbatim): one glyph per code point
function cp(fn){ const f=T.font, own=Object.prototype.hasOwnProperty.call(f,'stringToGlyphs'), orig=f.stringToGlyphs;
  f.stringToGlyphs=function(s){ return Array.from(s).map(c=>f.charToGlyph(c)); }; try{ return fn(); } finally{ if(own) f.stringToGlyphs=orig; else delete f.stringToGlyphs; } }
const run=(t,x,y)=>cp(()=>T.run(t,SIZE,x,y,0)), adv=t=>cp(()=>T.advance(t,SIZE,0)), ink=(t,x,y)=>cp(()=>T.inkBox(t,SIZE,x,y,0));
const ligs=t=>{ const a=T.font.stringToGlyphs(t).map(g=>g.index).join(','), b=cp(()=>T.font.stringToGlyphs(t)).map(g=>g.index).join(','); return a===b?null:T.font.stringToGlyphs(t).filter(g=>g.unicode&&g.unicode>=0xFB00&&g.unicode<=0xFB06).map(g=>'U+'+g.unicode.toString(16).toUpperCase()); };
const r3=v=>Math.round(v*1000)/1000;
function boxGeom(text){ const a=adv(text); const w=Math.round((a+88)/2)*2; const bx=AXIS-w/2; return {adv:a,w,bx,tx:bx+PAD}; }
const rectSvg=(bx,by,w,stroke)=>`<rect x="${n(bx+SW/2)}" y="${n(by+SW/2)}" width="${n(w-SW)}" height="${n(BOXH-SW)}" rx="${n(R-SW/2)}" fill="none" stroke="${stroke}" stroke-width="${SW}"/>`;
function boxRow(text,split,stroke,glyph,boxy,base,txOverride){ const g=boxGeom(text); const tx=txOverride===undefined?g.tx:txOverride; const r=run(text,tx,base);
  must(r.parts.length===Array.from(text).length,'glyph count ≠ code point count: '+text);
  const paths=split?[[glyph,r.parts.slice(0,split).join('')],[CREAM,r.parts.slice(split).join('')]]:[[CREAM,r.parts.join('')]];
  const svg=rectSvg(g.bx,boxy,g.w,stroke)+paths.map(([f,d])=>`<path fill="${f}" d="${d}"/>`).join('');
  const tl=T.run(text,SIZE,tx,base,0); const same=tl.parts.join('')===r.parts.join('');
  return {svg,adv:g.adv,w:g.w,bx:g.bx,tx,split,paths:paths.map(p=>p[0]),textlayout_identical:same,textlayout_advance:T.advance(text,SIZE,0),ink:ink(text,tx,base)}; }
const centreX=text=>Math.round((AXIS-adv(text)/2)*8)/8;
function line(text,base,xOverride){ const x=xOverride===undefined?centreX(text):xOverride; const r=run(text,x,base); must(r.parts.length===Array.from(text).length,'glyph count ≠ code point count: '+text);
  const tl=T.run(text,SIZE,x,base,0);
  return {svg:`<path fill="${CREAM}" d="${r.parts.join('')}"/>`,x,adv:adv(text),textlayout_identical:tl.parts.join('')===r.parts.join(''),textlayout_advance:T.advance(text,SIZE,0),ink:ink(text,x,base)}; }
// ---- layer surgery (verbatim)
function span(s,id){ const k=s.indexOf(`<g inkscape:groupmode="layer" id="${id}"`); must(k>=0,'no layer '+id); const re=/<g\b|<\/g>/g; re.lastIndex=k; let d=0,m;
  while((m=re.exec(s))){ d+=m[0]==='</g>'?-1:1; if(d===0) return [k,re.lastIndex]; } throw new Error('unclosed layer '+id); }
const layer=(s,id)=>{ const [a,b]=span(s,id); return s.slice(a,b); };
const openTag=l=>l.slice(0,l.indexOf('>')+1), innerOf=l=>l.slice(l.indexOf('>')+1,l.length-4);
const src=fs.readFileSync(SRC,'utf8'), tpl=fs.readFileSync(TPL,'utf8');
// ---- regression gates (verbatim from build-five.js)
const G={};
{ const L=layer(src,'sigma-h'); must(openTag(L)==='<g inkscape:groupmode="layer" id="sigma-h" transform="translate(0 -124.279)" inkscape:label="σₕ box">','σₕ layer open tag');
  const reg=boxRow('σₕ : (x, y) → (x, −y)',2,'#8C4191','#B498E6',BOXY1,BASE1); const ok=reg.svg===innerOf(L);
  const L7=layer(tpl,'operator'); const reg7=boxRow('σₕ : (x, y) → (x, −y)',2,'#B498E6','#B498E6',BOXY1,BASE1); const ok7=reg7.svg===innerOf(L7);
  G.sigma_h_row={pass:ok&&ok7&&reg.textlayout_identical,'16_sep_identical':ok,'build7_identical':ok7,w:reg.w,box_x:reg.bx,text_x:reg.tx,advance:r3(reg.adv)}; }
{ const C=innerOf(layer(tpl,'cogito')), F=innerOf(layer(tpl,'forall')), M=innerOf(layer(src,'m-def')), M7=innerOf(layer(tpl,'m-def'));
  const c1=line('I metacognize; therefore,',MOT1,185.875), c2=line('I am again and again.',MOT1+PITCH,248.375);
  const fa=boxRow('∀n. M(Iₙ) ⊢ Iₙ₊₁',0,GOLD,null,BOXY2,BASE2,360), md=boxRow('M := λx.Think(Think(x))',0,GOLD,null,2037,2110.625,217.125);
  const motto_ok=(c1.svg+c2.svg)===C, forall_ok=fa.svg===F, mdef_ok=md.svg===M&&M===M7;
  G.motto_and_rows={pass:motto_ok&&forall_ok&&mdef_ok&&c1.textlayout_identical&&c2.textlayout_identical&&fa.textlayout_identical&&md.textlayout_identical,cogito_identical:motto_ok,forall_identical:forall_ok,m_def_identical:mdef_ok}; }
{ const ok=layer(src,'divider-1')===layer(tpl,'divider-1')&&layer(src,'ground')===layer(tpl,'ground'); G.template_layers={pass:ok}; }
// the built (revision 5) lock screen must regenerate byte for byte from this generator's machinery before the new one is written
if(GATES_ONLY){ console.log(JSON.stringify(G,null,1)); process.exit(Object.values(G).every(g=>g.pass)?0:1); }
for(const [k,g] of Object.entries(G)) must(g.pass,'regression gate failed: '+k+' '+JSON.stringify(g));
console.log('regression: σₕ row byte for byte (16 Sep and build 7), motto + ∀n + M := byte for byte, divider 1 + ground identical');
// ---- coins (verbatim)
function coinInner(st){ const C=COINS[st]; const cb=fs.readFileSync(NOT+`MASTER-medallion-${st}-notation-slot820.svg`); const h=sha16(cb); must(h===C.hash,`${st} coin is ${h}, expected ${C.hash}`);
  const coin=cb.toString('utf8');
  must(coin.includes(`inkscape:label="1 ${st} rings ${C.ring} `),`${st}: ring colour ${C.ring} not the coin's`);
  must(new RegExp(`<g id="glyph-body"[^>]*fill="${C.glyph}">`).test(coin),`${st}: glyph colour ${C.glyph} not the coin's`);
  must(coin.includes(`0 field: ${st} tint ${C.field}`),`${st}: field ${C.field} not the coin's`);
  must(coin.includes('more than 170 deg'),`${st}: the coin does not carry the build-7 guard label`);
  const mm=coin.match(/<svg[^>]*>([\s\S]*)<\/svg>\s*$/); must(mm,'no svg root');
  return mm[1].replace(/\s+inkscape:[a-z-]+="[^"]*"/g,'').replace(/<title>[\s\S]*?<\/title>/,'').replace(/<desc>[\s\S]*?<\/desc>/,''); }
const IDREF_ATTRS=['begin','end','aria-labelledby','aria-describedby'];
function prefixIds(inner,p){ const ids=new Set([...inner.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]));
  let out=inner.replace(/(\sid=")([^"]+)"/g,(m,a,v)=>`${a}${p}${v}"`)
    .replace(/url\(\s*#([^)\s]+)\s*\)/g,(m,v)=>`url(#${p}${v})`)
    .replace(/(\s(?:xlink:)?href=")#([^"]+)"/g,(m,a,v)=>`${a}#${p}${v}"`);
  for(const at of IDREF_ATTRS) out=out.replace(new RegExp(`(\\s${at}=")([^"]*)"`,'g'),(m,a,v)=>a+v.split(/(\s+|;)/).map(tok=>{ if(/^\s*$|^;$/.test(tok)) return tok; const q=tok.match(/^([A-Za-z_][\w-]*)(\..*)?$/); return q&&ids.has(q[1])?p+tok:tok; }).join('')+'"');
  return out; }
function refsOf(s){ const r=[]; for(const m of s.matchAll(/url\(\s*#([^)\s]+)\s*\)/g)) r.push(m[1]); for(const m of s.matchAll(/\s(?:xlink:)?href="([^"]*)"/g)){ must(m[1].startsWith('#'),'reference outside the document: '+m[1]); r.push(m[1].slice(1)); }
  for(const at of IDREF_ATTRS) for(const m of s.matchAll(new RegExp(`\\s${at}="([^"]*)"`,'g'))) for(const tok of m[1].split(/[\s;]+/).filter(Boolean)) r.push(tok.split('.')[0]); return r; }
const idsOf=s=>[...s.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]);
// ---- the strings and their spec numbers (J4 spec §4/§5/§8, unchanged by update 19)
const FOUR={sym:{text:'V₄ = {I, σᵥ, σₕ, C₂}',adv:603.902,w:692,bx:257,tx:300.625}, law:{text:'∀g ∈ V₄. g ∘ g = I',adv:561.592,w:650,bx:278,tx:321.625},
  sentence:[['Four boxes;',383.032,411.500],['one move between any two;',923.384,141.250],['the way back is the same move.',1047.512,79.250]]};
const ORDER=['NORMATIVE','NON-NORMATIVE','METACOGNITIVE','CRITICAL'], CELLNAME=['top-left','top-right','bottom-left','bottom-right'];
// ---- revision 6 (update 19): the coins and the rows
const DIAM=391.5, SCALE='0.477439024', CENTRES=[[375.75,864.75],[829.25,864.75],[375.75,1318.25],[829.25,1318.25]];
const sc=+SCALE; const box=820*sc; must(Math.abs(box-DIAM)<0.001,'scale does not give 391.5 px: '+box);
const cells=CENTRES.map(([cx,cy])=>[n(cx-DIAM/2),n(cy-DIAM/2)]);
const PREV_LOCK={row1:1531.598,base1:1605.223,row2:1704.320,base2:1777.945,div:1877.041,rule_y:1885.041,dcy:1887.041,lines:[2006.512,2076.387,2146.262]}; // the built screen (revision 5)
const X={}; for(const k of Object.keys(PREV_LOCK)) X[k]=Array.isArray(PREV_LOCK[k])?PREV_LOCK[k].map(v=>r3(v+SHIFT)):r3(PREV_LOCK[k]+SHIFT);
const near=(a,b,m)=>must(Math.abs(a-b)<0.0005,`${m}: built ${a}, spec ${b}`);
const DIV1=layer(src,'divider-1'); must(openTag(DIV1)==='<g inkscape:groupmode="layer" id="divider-1" transform="translate(0 -74.836)" inkscape:label="divider 1">','divider-1 open tag');
const head=src.slice(0,src.indexOf('<g inkscape:groupmode="layer" id="medallion"')); const GROUND=layer(src,'ground');
must(head.endsWith(GROUND+'\n'),'header layout'); const ROOTTAG=head.slice(0,head.indexOf('\n<title>'));
must(ROOTTAG==='<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1206" height="2622" viewBox="0 0 1206 2622">','root tag');
const SPECREF=`Science's FINISH-TODAY update 19 of 22 Oct 2026, 02:24Z (the halfway layout, spec revision 6; record copy work/spec-rev6/FINISH-TODAY-update-19.md sha256-16 ${SPEC16}, cut from TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-FINISH-TODAY.md ${FT16} at build time; mock-up 6902002ccfe5fdeb), on the J4 layout spec revision 5 (c9f6c5f60d354a09) for every string, box and size`;
const FONTREF=`DejaVu Sans Bold 2.34 (dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf, sha256-16 ${FONT16}) at 58 px, outlined as paths by vector-masters/work/lockscreen/textlayout.js (opentype.js 1.3.4, kerning on) with its stringToGlyphs shadowed by a per-code-point cmap mapping (one glyph per code point, as Science ruled 21 Oct); no live text, no raster`;
const safe=s=>{ must(!/[<>&"]/.test(s),'unsafe metadata text: '+s); return s; };
fs.mkdirSync(OUT+'/work',{recursive:true}); fs.mkdirSync(OUT+'/proofs',{recursive:true}); fs.mkdirSync(OUT+'/work/spec-rev6',{recursive:true});
const report={generator:'vector-masters/work/lockscreen-tetrasemaphore/build-lock-rev6.js',date:'2026-10-22',spec:{update_19_record:SPEC,sha16:SPEC16,finish_today_sha16_at_build:FT16,mockup:MOCK,mockup_sha16:MOCK16,j4_spec_revision_5:'c9f6c5f60d354a09'},
  sources:{no_title_master:{file:SRC,sha16:SRC16},template:{file:TPL,sha16:TPL16},previous_lock_screen_revision_5:{file:PREV,sha16:PREV16},font:{file:T.FONT,sha16:FONT16}},regression_gates:G,
  glyph_mapping:'one glyph per code point (cmap)',screens:{}};
function stackLayers(rows,dy,labels){ const tr=id=>n(TY[id]+dy);
  const op=`<g inkscape:groupmode="layer" id="operator" transform="translate(0 ${tr('operator')})" inkscape:label="${safe(labels.operator)}">${rows.operator}</g>`;
  const fa=`<g inkscape:groupmode="layer" id="forall" transform="translate(0 ${tr('forall')})" inkscape:label="${safe(labels.forall)}">${rows.forall}</g>`;
  const dv=DIV1.replace('transform="translate(0 -74.836)"',`transform="translate(0 ${tr('divider-1')})"`);
  const cg=`<g inkscape:groupmode="layer" id="cogito" transform="translate(0 ${tr('cogito')})" inkscape:label="${safe(labels.cogito)}">${rows.cogito}</g>`;
  return `<g inkscape:groupmode="layer" id="stack" inkscape:label="${safe(labels.stack)}">${op}${fa}${dv}${cg}</g>`; }
function finish(name,file,title,desc,figure,stack,rep){
  const out=`${ROOTTAG}\n<title>${safe(title)}</title>\n<desc>${safe(desc)}</desc>\n${GROUND}\n${figure}\n\n${stack}\n</svg>`;
  const ids=idsOf(out); const dup=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))]; must(!dup.length,name+' duplicate ids '+dup);
  const idset=new Set(ids); const refs=refsOf(out); const bad=refs.filter(r=>!idset.has(r)); must(!bad.length,name+' unresolved references '+bad);
  must(!/<text\b|<image\b|<foreignObject\b|<script\b|<style\b/.test(out),name+': text/image/script/style');
  fs.writeFileSync(OUT+'/'+file,out); rep.file=file; rep.sha16=sha16(fs.readFileSync(OUT+'/'+file)); rep.bytes=Buffer.byteLength(out); rep.ids=ids.length; rep.references=refs.length;
  report.screens[name]=rep; console.log(name.padEnd(28),rep.sha16,file); }
const lineRep=(L,text,base_wt,ty,sx,sb)=>({string:text,code_points:Array.from(text).map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')),advance:r3(L.adv),textlayout_ligature:ligs(text),textlayout_identical:L.textlayout_identical,
    x:L.x,baseline:r3(base_wt+ty),baseline_in_layer:base_wt,layer_ty:ty,fill:CREAM,spec:{advance:sx[0],x:sx[1],baseline:sb},ink:{x1:r3(L.ink.x1),y1:r3(L.ink.y1+ty),x2:r3(L.ink.x2),y2:r3(L.ink.y2+ty)}});
const rowRep=(B,text,ty,boxy,base,stroke,role)=>({role,string:text,code_points:Array.from(text).map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')),advance:r3(B.adv),textlayout_ligature:ligs(text),textlayout_identical:B.textlayout_identical,
  box:{x:B.bx,y:r3(boxy+ty),w:B.w,h:BOXH,rx:R,stroke_width:SW,stroke},text_x:B.tx,baseline:r3(base+ty),baseline_in_layer:base,layer_ty:ty,path_fills:B.paths,glyph_split_code_points:B.split,ink:{x1:r3(B.ink.x1),y1:r3(B.ink.y1+ty),x2:r3(B.ink.x2),y2:r3(B.ink.y2+ty)}});
const divRep=dy=>({layer_ty:r3(TY['divider-1']+dy),rule:{x:503,y:r3(1757+TY['divider-1']+dy),w:200,h:4,fill:GOLD},diamond:{cx:603,cy:r3(DIVCY+TY['divider-1']+dy),half_diagonal:r3(14/Math.SQRT2),fill:GOLD},row_y:r3(1749+TY['divider-1']+dy)});
// ---- the screen
{ const dy=DY;
  const sym=boxRow(FOUR.sym.text,0,GOLD,null,BOXY1,BASE1), law=boxRow(FOUR.law.text,0,GOLD,null,BOXY2,BASE2);
  for(const [B,E] of [[sym,FOUR.sym],[law,FOUR.law]]){ near(B.adv,E.adv,'advance '+E.text); near(B.w,E.w,'w '+E.text); near(B.bx,E.bx,'x '+E.text); near(B.tx,E.tx,'text x '+E.text); }
  near(BOXY1+TY.operator+dy,X.row1,'row 1 y'); near(BASE1+TY.operator+dy,X.base1,'row 1 baseline'); near(BOXY2+TY.forall+dy,X.row2,'row 2 y'); near(BASE2+TY.forall+dy,X.base2,'row 2 baseline');
  near(1749+TY['divider-1']+dy,X.div,'divider y'); near(1757+TY['divider-1']+dy,X.rule_y,'rule y'); near(DIVCY+TY['divider-1']+dy,X.dcy,'diamond y');
  const SL=FOUR.sentence.map(([t,a,x],i)=>{ const L=line(t,MOT1+i*PITCH); near(L.adv,a,'sentence advance '+t); near(L.x,x,'sentence x '+t); near(MOT1+i*PITCH+TY.cogito+dy,X.lines[i],'sentence baseline'); return L; });
  const coinsRep=[]; const groups=ORDER.map((st,i)=>{ const C=COINS[st]; const [tx,ty]=cells[i]; const tr=`translate(${tx} ${ty}) scale(${SCALE})`;
    const inner=coinInner(st); const pin=prefixIds(inner,C.prefix); const cid=C.prefix+'medallion-slot820';
    const own=idsOf(pin), refs=refsOf(pin); must(own.every(x=>x.startsWith(C.prefix)),st+': unprefixed id'); must(refs.every(r=>r.startsWith(C.prefix)&&own.includes(r)),st+': reference outside its coin');
    must(idsOf(inner).length===own.length&&refsOf(inner).length===refs.length,st+': prefixing changed the id/reference count');
    must(pin.replace(new RegExp(`(\\sid="|url\\(#|href="#)${C.prefix.replace('-','\\-')}`,'g'),'$1')===inner,st+': prefixing changed something other than ids and references');
    coinsRep.push({cell:CELLNAME[i],state:st,master:`MASTER-medallion-${st}-notation-slot820.svg`,sha16:C.hash,transform:tr,translate:[+tx,+ty],scale:sc,box_px:r3(box),centre:CENTRES[i],prefix:C.prefix,ids:own.length+1,references:refs.length,group_id:cid});
    return `<g inkscape:groupmode="layer" id="${cid}" transform="${tr}" inkscape:label="${safe(`${CELLNAME[i]}: the Tetrasemaphore ${st} coin (linked master ${C.hash}, build 7), inlined verbatim with every id and reference prefixed ${C.prefix}; centre (${CENTRES[i][0]}, ${CENTRES[i][1]})`)}">${pin}</g>`; });
  const pitchX=CENTRES[1][0]-CENTRES[0][0], pitchY=CENTRES[2][1]-CENTRES[0][1];
  const fig=`<g inkscape:groupmode="layer" id="figure" inkscape:label="${safe(`figure: the four Tetrasemaphore coins of build 7, 2 × 2 (NORMATIVE top-left, NON-NORMATIVE top-right, METACOGNITIVE bottom-left, CRITICAL bottom-right), scale ${SCALE}, coin ${r3(box)} px, centres (375.75, 864.75) (829.25, 864.75) (375.75, 1318.25) (829.25, 1318.25), pitch ${r3(pitchX)} px, the halfway layout of 22 Oct`)}">${groups.join('')}</g>`;
  const sentTxt=FOUR.sentence.map(m=>m[0]).join(' / ');
  const labels={stack:`type stack (no title; the built lock screen's rows moved a further ${SHIFT} px down as whole layers, ${r3(DY)} px below the card grid; gaps 40·φ = 64.72): the four symbols · the law · divider · the sentence`,
    operator:`the four symbols: ${FOUR.sym.text}; box ${sym.w} × 108 at x ${sym.bx}, y ${X.row1}, stroke gold ${GOLD}, all text cream ${CREAM}; text x ${sym.tx}, baseline ${X.base1}`,
    forall:`the law: ${FOUR.law.text}; box ${law.w} × 108 at x ${law.bx}, y ${X.row2}, stroke gold ${GOLD}, text cream ${CREAM}; text x ${law.tx}, baseline ${X.base2}`,
    cogito:`the sentence (three lines on its own semicolons, unboxed, cream, centred on x 603): ${sentTxt}; baselines ${X.lines.join(', ')}`};
  const stack=stackLayers({operator:sym.svg,forall:law.svg,cogito:SL.map(L=>L.svg).join('')},dy,labels);
  const NAME='ALL-FOUR-lockscreen-halfway';
  const title=`Dose 01 · iPhone 17 Pro lock screen · Tetrasemaphore fifth lock screen, all four states (build-7 coins), the halfway layout of 22 Oct · layered vector master (1206 × 2622) · proposal`;
  const cellTxt=coinsRep.map(c=>`${c.cell} ${c.state} (${c.sha16}) at ${c.transform}, centre (${c.centre[0]}, ${c.centre[1]}), ids prefixed ${c.prefix}`).join('; ');
  const desc=`The Tetrasemaphore fifth lock screen, all four states, rebuilt 2026-10-22 at the halfway layout Carey chose on his phone (${SPECREF}). It replaces the revision-5 screen ${PREV16} (held, then found to sit too high under the clock, 22 Oct 02:18Z). Rows, top to bottom: the four coins 2 × 2, the four symbols, the law, a divider, the sentence; no title, no label, no caption (the coins carry their own legends). Built by vector-masters/work/lockscreen-tetrasemaphore/build-lock-rev6.js, build-five.js's machinery unchanged, as a layer swap on the no-title lock-screen master vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg (sha256-16 ${SRC16}), the build-meta7.js recipe of the accepted METACOGNITIVE screen (${TPL16}): the ground is byte-identical to that master and divider 1 is its divider-1 layer with only its transform changed; every row is the revision-5 screen's moved ${SHIFT} px further down as a whole layer (transforms ${n(TY.operator+dy)}, ${n(TY.forall+dy)}, ${n(TY['divider-1']+dy)}, ${n(TY.cogito+dy)}): row 1 y ${X.row1}, row 2 y ${X.row2}, divider ${X.div}, sentence baselines ${X.lines.join(' / ')}; strings, sizes and x positions unchanged. Figure: the four build-7 coin masters of master/states/proposals/notation/final-masters-2026-10-05/ (sha256-16 NORMATIVE e0b6366d5c032523, NON-NORMATIVE 4ef1de6ae126279e, METACOGNITIVE cccfcff10dc74930, CRITICAL 33413c4af9ec838c), each root content inlined verbatim (title, desc and inkscape attributes stripped; no recolouring, no clip, no crop) under one uniform scale ${SCALE} (coin ${r3(box)} px across, update 19's stated diameter; its scale 0.8492 of the built coins would give 391.07 px, 0.43 px less, so the stated diameter was followed; the pitch is ${r3(pitchX)} px both ways): ${cellTxt}. Per the J4 spec §2 every id of a coin and every reference to it carries that coin's prefix, so each coin resolves inside itself. Both boxes gold ${GOLD}, all text cream ${CREAM}: ${FOUR.sym.text} (box ${sym.w} at x ${sym.bx}) and ${FOUR.law.text} (box ${law.w} at x ${law.bx}); width = text advance + 88 to the nearest even px, centred on x 603, text from box x + 43.625, stroke 4, radius 28. The sentence, unboxed, cream, each line centred on x 603 to 1/8 px: ${sentTxt} ${FONTREF}. Proposal, not final; Carey decides.`;
  finish(NAME,`dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-${NAME}-MASTER.svg`,title,desc,fig,stack,{kind:'fifth lock screen (all four), halfway layout, revision 6',spec_section:'FINISH-TODAY update 19',
    grid:{scale:sc,diameter_px:DIAM,centres:CENTRES,translates:cells.map(c=>c.map(Number)),pitch_x:r3(pitchX),pitch_y:r3(pitchY),top:r3(CENTRES[0][1]-DIAM/2),bottom:r3(CENTRES[2][1]+DIAM/2),
      update_19_scale_note:{stated_diameter:DIAM,stated_scale_of_built:0.8492,built_rev5_diameter:460.516,diameter_from_stated_scale:r3(460.516*0.8492),used_scale_of_built:r3(DIAM/460.516),difference_px:r3(DIAM-460.516*0.8492)},
      expected_clearances:{clock_digits_y612_to_coin_top:r3(CENTRES[0][1]-DIAM/2-612),update_19_expected:56,grid_bottom_to_row1:r3(X.row1-(CENTRES[2][1]+DIAM/2)),phi_gap:r3(40*(1+Math.sqrt(5))/2),last_baseline_to_buttons_y2298:r3(2298-X.lines[2]),update_19_expected_above_buttons:92}},
    coins:coinsRep,layers:{ground:'byte-identical to '+SRC16,figure:'four coin sub-layers',operator:r3(TY.operator+dy),forall:r3(TY.forall+dy),'divider-1':r3(TY['divider-1']+dy),cogito:r3(TY.cogito+dy)},
    rows:[rowRep(sym,FOUR.sym.text,TY.operator+dy,BOXY1,BASE1,GOLD,'the four symbols'),rowRep(law,FOUR.law.text,TY.forall+dy,BOXY2,BASE2,GOLD,'the law')],divider:divRep(dy),
    lines:SL.map((L,i)=>lineRep(L,FOUR.sentence[i][0],MOT1+i*PITCH,TY.cogito+dy,[FOUR.sentence[i][1],FOUR.sentence[i][2]],X.lines[i]))}); }
fs.writeFileSync(OUT+'/work/layout_report.json',JSON.stringify(report,null,1)+'\n');
fs.copyFileSync(CANON,OUT+'/work/build-lock-rev6.js'); fs.copyFileSync(SPEC,OUT+'/work/spec-rev6/FINISH-TODAY-update-19.md');
console.log('wrote the halfway lock screen and work/layout_report.json');
