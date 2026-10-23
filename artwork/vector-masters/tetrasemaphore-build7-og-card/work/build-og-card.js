// build-og-card.js (2026-10-22): the tetrasemaphore.systems link-preview card as a sealed master, per Science's site rulings item 5
// (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-SITE-RULINGS.md 412ba93ba0a6979c, 22 Oct 03:12Z): "the four build-7 coins, TETRASEMAPHORE and
// V₄ = {I, σᵥ, σₕ, C₂} (the fifth card's approved line), and nothing else". 1200 × 630 (the Open Graph size the site already declares).
// build-five.js's machinery (the sealed J4 generator): the coins inlined verbatim with every id and reference prefixed n- / nn- / m- / c-,
// DejaVu Sans Bold outlined one glyph per code point, the boxed row rule (width = advance + 88 to the nearest even px, text from box x + 43.625,
// stroke 4, radius 28), the screens' ground #1D252D, gold #D4A853 and cream #E8E0D2. Layout: the word TETRASEMAPHORE at 58 px, cream, centred on
// x 600, baseline 96; the four coins in a row, 220 px each (scale 220/820), gap 40·φ, the row centred on x 600, top y 140; the formula in a gold
// box (692 × 108, as on the all-four screens) centred on x 600 at y 425. No other mark, word or line.
// Usage: node build-og-card.js   (gates, then og-card-MASTER.svg + work/layout_report.json)
const fs=require('fs'), crypto=require('crypto'), path=require('path'); const T=require('../lockscreen/textlayout.js'); const n=T.n;
const ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2', VM=ROOT+'/vector-masters', OUT=process.env.OG_OUT||VM+'/tetrasemaphore-build7-og-card';
const CANON=VM+'/work/lockscreen-tetrasemaphore/build-og-card.js'; if(path.resolve(__filename)!==CANON) throw new Error('run build-og-card.js from its canonical path '+CANON);
const RUL='/Users/careybalboa/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-SITE-RULINGS.md', RUL16='412ba93ba0a6979c';
const SRC=VM+'/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg', SRC16='1cf8f0f9f4aa30ea';
const NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/', FONT16='7e69e81478e233b8';
const sha16=b=>crypto.createHash('sha256').update(b).digest('hex').slice(0,16);
const must=(c,m)=>{ if(!c) throw new Error(m); };
must(sha16(fs.readFileSync(RUL))===RUL16,'site rulings file is not 412ba93ba0a6979c');
must(sha16(fs.readFileSync(SRC))===SRC16,'no-title lock-screen master moved');
must(sha16(fs.readFileSync(T.FONT))===FONT16,'font is not 7e69e81478e233b8');
const COINS={
 'NORMATIVE':    {hash:'e0b6366d5c032523',ring:'#D5AF64',glyph:'#C7B469',field:'#181403',prefix:'n-'},
 'NON-NORMATIVE':{hash:'4ef1de6ae126279e',ring:'#4FB5B5',glyph:'#4FB5B5',field:'#001817',prefix:'nn-'},
 'METACOGNITIVE':{hash:'cccfcff10dc74930',ring:'#B498E6',glyph:'#B498E6',field:'#17121D',prefix:'m-'},
 'CRITICAL':     {hash:'33413c4af9ec838c',ring:'#E25C60',glyph:'#E25C60',field:'#1F100E',prefix:'c-'},
};
const W=1200, H=630, SIZE=58, PAD=43.625, SW=4, R=28, BOXH=108, CREAM='#E8E0D2', GOLD='#D4A853', GROUNDC='#1D252D';
function cp(fn){ const f=T.font, own=Object.prototype.hasOwnProperty.call(f,'stringToGlyphs'), orig=f.stringToGlyphs;
  f.stringToGlyphs=function(s){ return Array.from(s).map(c=>f.charToGlyph(c)); }; try{ return fn(); } finally{ if(own) f.stringToGlyphs=orig; else delete f.stringToGlyphs; } }
const run=(t,x,y)=>cp(()=>T.run(t,SIZE,x,y,0)), adv=t=>cp(()=>T.advance(t,SIZE,0)), ink=(t,x,y)=>cp(()=>T.inkBox(t,SIZE,x,y,0));
const r3=v=>Math.round(v*1000)/1000;
function boxGeom(text,axis){ const a=adv(text); const w=Math.round((a+88)/2)*2; const bx=axis-w/2; return {adv:a,w,bx,tx:bx+PAD}; }
const rectSvg=(bx,by,w,stroke)=>`<rect x="${n(bx+SW/2)}" y="${n(by+SW/2)}" width="${n(w-SW)}" height="${n(BOXH-SW)}" rx="${n(R-SW/2)}" fill="none" stroke="${stroke}" stroke-width="${SW}"/>`;
function boxRow(text,axis,boxy,base){ const g=boxGeom(text,axis); const r=run(text,g.tx,base); must(r.parts.length===Array.from(text).length,'glyph count ≠ code point count: '+text);
  const svg=rectSvg(g.bx,boxy,g.w,GOLD)+`<path fill="${CREAM}" d="${r.parts.join('')}"/>`; const tl=T.run(text,SIZE,g.tx,base,0);
  return {svg,adv:g.adv,w:g.w,bx:g.bx,tx:g.tx,textlayout_identical:tl.parts.join('')===r.parts.join(''),ink:ink(text,g.tx,base)}; }
const centreX=(text,axis)=>Math.round((axis-adv(text)/2)*8)/8;
function line(text,axis,base){ const x=centreX(text,axis); const r=run(text,x,base); must(r.parts.length===Array.from(text).length,'glyph count ≠ code point count: '+text);
  const tl=T.run(text,SIZE,x,base,0); return {svg:`<path fill="${CREAM}" d="${r.parts.join('')}"/>`,x,adv:adv(text),textlayout_identical:tl.parts.join('')===r.parts.join(''),ink:ink(text,x,base)}; }
// ---- regression gate: the σₕ row of the 16 Sep master regenerates byte for byte (the text engine and the box rule are the sealed ones)
function span(s,id){ const k=s.indexOf(`<g inkscape:groupmode="layer" id="${id}"`); must(k>=0,'no layer '+id); const re=/<g\b|<\/g>/g; re.lastIndex=k; let d=0,m;
  while((m=re.exec(s))){ d+=m[0]==='</g>'?-1:1; if(d===0) return [k,re.lastIndex]; } throw new Error('unclosed layer '+id); }
const layer=(s,id)=>{ const [a,b]=span(s,id); return s.slice(a,b); }; const innerOf=l=>l.slice(l.indexOf('>')+1,l.length-4);
const src=fs.readFileSync(SRC,'utf8');
{ const L=innerOf(layer(src,'sigma-h')); const g=boxGeom('σₕ : (x, y) → (x, −y)',603); const r=run('σₕ : (x, y) → (x, −y)',g.tx,1526.625);
  const reg=rectSvg(g.bx,1453,g.w,'#8C4191')+`<path fill="#B498E6" d="${r.parts.slice(0,2).join('')}"/><path fill="${CREAM}" d="${r.parts.slice(2).join('')}"/>`;
  must(reg===L,'regression gate failed: the σₕ row does not regenerate byte for byte'); console.log('regression: σₕ row byte for byte (16 Sep master)'); }
// ---- coins (build-five.js, verbatim)
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
  let out=inner.replace(/(\sid=")([^"]+)"/g,(m,a,v)=>`${a}${p}${v}"`).replace(/url\(\s*#([^)\s]+)\s*\)/g,(m,v)=>`url(#${p}${v})`).replace(/(\s(?:xlink:)?href=")#([^"]+)"/g,(m,a,v)=>`${a}#${p}${v}"`);
  for(const at of IDREF_ATTRS) out=out.replace(new RegExp(`(\\s${at}=")([^"]*)"`,'g'),(m,a,v)=>a+v.split(/(\s+|;)/).map(tok=>{ if(/^\s*$|^;$/.test(tok)) return tok; const q=tok.match(/^([A-Za-z_][\w-]*)(\..*)?$/); return q&&ids.has(q[1])?p+tok:tok; }).join('')+'"');
  return out; }
function refsOf(s){ const r=[]; for(const m of s.matchAll(/url\(\s*#([^)\s]+)\s*\)/g)) r.push(m[1]); for(const m of s.matchAll(/\s(?:xlink:)?href="([^"]*)"/g)){ must(m[1].startsWith('#'),'reference outside the document: '+m[1]); r.push(m[1].slice(1)); }
  for(const at of IDREF_ATTRS) for(const m of s.matchAll(new RegExp(`\\s${at}="([^"]*)"`,'g'))) for(const tok of m[1].split(/[\s;]+/).filter(Boolean)) r.push(tok.split('.')[0]); return r; }
const idsOf=s=>[...s.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]);
const safe=s=>{ must(!/[<>&"]/.test(s),'unsafe metadata text: '+s); return s; };
// ---- layout
const AXIS=600, TITLE='TETRASEMAPHORE', TITLE_BASE=96, COIN=220, SCALE='0.268292683', GAP=40*(1+Math.sqrt(5))/2, COIN_TOP=140, BOXY=425, BASE=BOXY+73.625;
const FORMULA='V₄ = {I, σᵥ, σₕ, C₂}';
must(Math.abs(820*(+SCALE)-COIN)<0.001,'scale does not give 220 px');
const ORDER=['NORMATIVE','NON-NORMATIVE','METACOGNITIVE','CRITICAL'];
const rowW=4*COIN+3*GAP, left=(W-rowW)/2; const xs=ORDER.map((_,i)=>r3(left+i*(COIN+GAP)));
const title=line(TITLE,AXIS,TITLE_BASE); const row=boxRow(FORMULA,AXIS,BOXY,BASE);
must(row.w===692,'formula box width changed: '+row.w); // the all-four screens' box, 692 wide
const coinsRep=[]; const groups=ORDER.map((st,i)=>{ const C=COINS[st]; const tr=`translate(${n(xs[i])} ${COIN_TOP}) scale(${SCALE})`;
  const inner=coinInner(st); const pin=prefixIds(inner,C.prefix); const cid=C.prefix+'medallion-slot820';
  const own=idsOf(pin), refs=refsOf(pin); must(own.every(x=>x.startsWith(C.prefix)),st+': unprefixed id'); must(refs.every(r=>r.startsWith(C.prefix)&&own.includes(r)),st+': reference outside its coin');
  must(idsOf(inner).length===own.length&&refsOf(inner).length===refs.length,st+': prefixing changed the id/reference count');
  must(pin.replace(new RegExp(`(\\sid="|url\\(#|href="#)${C.prefix.replace('-','\\-')}`,'g'),'$1')===inner,st+': prefixing changed something other than ids and references');
  coinsRep.push({state:st,master:`MASTER-medallion-${st}-notation-slot820.svg`,sha16:C.hash,transform:tr,translate:[xs[i],COIN_TOP],scale:+SCALE,box_px:COIN,centre:[r3(xs[i]+COIN/2),COIN_TOP+COIN/2],prefix:C.prefix,ids:own.length+1,references:refs.length,group_id:cid});
  return `<g inkscape:groupmode="layer" id="${cid}" transform="${tr}" inkscape:label="${safe(`the Tetrasemaphore ${st} coin (linked master ${C.hash}, build 7), inlined verbatim with every id and reference prefixed ${C.prefix}`)}">${pin}</g>`; });
const ROOTTAG=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`;
const ground=`<g inkscape:groupmode="layer" id="ground" inkscape:label="ground ${GROUNDC} (the lock screens' field)"><rect x="0" y="0" width="${W}" height="${H}" fill="${GROUNDC}"/></g>`;
const fig=`<g inkscape:groupmode="layer" id="figure" inkscape:label="${safe(`figure: the four Tetrasemaphore coins of build 7 in a row (NORMATIVE, NON-NORMATIVE, METACOGNITIVE, CRITICAL), scale ${SCALE}, coin ${COIN} px, gap 40·φ = ${r3(GAP)} px, row ${r3(rowW)} px centred on x 600 from y ${COIN_TOP}`)}">${groups.join('')}</g>`;
const tl=`<g inkscape:groupmode="layer" id="title" inkscape:label="${safe(`the word ${TITLE} at 58 px, cream ${CREAM}, centred on x 600 to 1/8 px (x ${title.x}), baseline ${TITLE_BASE}`)}">${title.svg}</g>`;
const fr=`<g inkscape:groupmode="layer" id="formula" inkscape:label="${safe(`the formula ${FORMULA}; box ${row.w} × 108 at x ${row.bx}, y ${BOXY}, stroke gold ${GOLD}, text cream ${CREAM}; text x ${row.tx}, baseline ${BASE}`)}">${row.svg}</g>`;
const TITLE_T=`Tetrasemaphore link-preview card (Open Graph 1200 × 630): the four build-7 coins, the word TETRASEMAPHORE and the formula · layered vector master · proposal`;
const DESC=`The link-preview card for tetrasemaphore.systems, built 2026-10-22 by vector-masters/work/lockscreen-tetrasemaphore/build-og-card.js as Science's site rulings item 5 says (TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-SITE-RULINGS.md ${RUL16}, 22 Oct 03:12Z): the four build-7 coins, the word TETRASEMAPHORE and the fifth card's approved line ${FORMULA}, and nothing else. Ground ${GROUNDC}, the lock screens' field. Figure: the four coin masters of master/states/proposals/notation/final-masters-2026-10-05/ (sha256-16 NORMATIVE e0b6366d5c032523, NON-NORMATIVE 4ef1de6ae126279e, METACOGNITIVE cccfcff10dc74930, CRITICAL 33413c4af9ec838c), each root content inlined verbatim (title, desc and inkscape attributes stripped; no recolouring, no clip, no crop) in a row under one uniform scale ${SCALE} (coin ${COIN} px, gap 40·φ = ${r3(GAP)} px, the row ${r3(rowW)} px wide centred on x 600, top y ${COIN_TOP}): ${coinsRep.map(c=>`${c.state} at ${c.transform}, ids prefixed ${c.prefix}`).join('; ')}. Per the J4 spec §2 every id of a coin and every reference to it carries that coin's prefix. The word ${TITLE}: 58 px, cream ${CREAM}, centred on x 600 to 1/8 px (x ${title.x}), baseline ${TITLE_BASE}. The formula ${FORMULA}: a gold ${GOLD} box ${row.w} × 108 at x ${row.bx}, y ${BOXY} (width = text advance ${r3(row.adv)} + 88 to the nearest even px, the all-four screens' box), text cream from x ${row.tx}, baseline ${BASE}, stroke 4, radius 28. DejaVu Sans Bold 2.34 (dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf, sha256-16 ${FONT16}) at 58 px, outlined as paths by vector-masters/work/lockscreen/textlayout.js (opentype.js 1.3.4, kerning on) with its stringToGlyphs shadowed by a per-code-point cmap mapping; no live text, no raster. Proposal, not final; Science checks, Carey sees it at card 11.`;
const out=`${ROOTTAG}\n<title>${safe(TITLE_T)}</title>\n<desc>${safe(DESC)}</desc>\n${ground}\n${fig}\n${tl}\n${fr}\n</svg>`;
const ids=idsOf(out); const dup=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))]; must(!dup.length,'duplicate ids '+dup);
const idset=new Set(ids); const refs=refsOf(out); const bad=refs.filter(r=>!idset.has(r)); must(!bad.length,'unresolved references '+bad);
must(!/<text\b|<image\b|<foreignObject\b|<script\b|<style\b/.test(out),'text/image/script/style');
fs.mkdirSync(OUT+'/work',{recursive:true}); fs.mkdirSync(OUT+'/proofs',{recursive:true});
const FILE='og-card-MASTER.svg'; fs.writeFileSync(OUT+'/'+FILE,out);
const cps=t=>Array.from(t).map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0'));
const report={generator:'vector-masters/work/lockscreen-tetrasemaphore/build-og-card.js',date:'2026-10-22',ruling:{file:RUL,sha16:RUL16,item:5},
  sources:{font:{file:T.FONT,sha16:FONT16},ground_from:{file:SRC,sha16:SRC16,colour:GROUNDC}},canvas:[W,H],
  file:FILE,sha16:sha16(fs.readFileSync(OUT+'/'+FILE)),bytes:Buffer.byteLength(out),ids:ids.length,references:refs.length,
  coins:coinsRep,title:{string:TITLE,code_points:cps(TITLE),x:title.x,baseline:TITLE_BASE,advance:r3(title.adv),textlayout_identical:title.textlayout_identical,ink:{x1:r3(title.ink.x1),y1:r3(title.ink.y1),x2:r3(title.ink.x2),y2:r3(title.ink.y2)}},
  formula:{string:FORMULA,code_points:cps(FORMULA),box:{x:row.bx,y:BOXY,w:row.w,h:BOXH,rx:R,stroke_width:SW,stroke:GOLD},text_x:row.tx,baseline:BASE,advance:r3(row.adv),textlayout_identical:row.textlayout_identical,ink:{x1:r3(row.ink.x1),y1:r3(row.ink.y1),x2:r3(row.ink.x2),y2:r3(row.ink.y2)}},
  margins:{top_to_title_ink:r3(title.ink.y1),title_ink_bottom_to_coins:r3(COIN_TOP-title.ink.y2),coins_bottom_to_box:r3(BOXY-(COIN_TOP+COIN)),box_bottom_to_edge:r3(H-(BOXY+BOXH)),row_left:r3(left),row_right:r3(W-left-rowW)}};
fs.writeFileSync(OUT+'/work/layout_report.json',JSON.stringify(report,null,1)+'\n'); fs.copyFileSync(CANON,OUT+'/work/build-og-card.js');
console.log(FILE,report.sha16,'ids',ids.length,'refs',refs.length,'margins',JSON.stringify(report.margins));
