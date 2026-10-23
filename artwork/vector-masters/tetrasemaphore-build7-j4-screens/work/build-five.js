// J4: the five Tetrasemaphore phone screens (2026-10-21), as Science's layout spec says (TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md, revision 4,
// sha256-16 a2131c898acbb0e8): the three state flashcards (§3), the fifth all-four flashcard (§4), the fifth all-four lock screen (§5, held for
// Carey's phone check). One generator, five outputs, the build-meta7.js recipe: a layer swap on the 16 Sep no-title lock-screen master
// (1cf8f0f9f4aa30ea), the build-7 coins inlined verbatim (root content; inkscape:* attributes, <title>, <desc> stripped; no recolouring, no clip,
// no crop), the rows at the build-7 METACOGNITIVE screen's own layer transforms (a62a3dd185089960), divider 1 byte for byte, divider 2 and M := dropped.
// On the two all-four screens each coin's ids carry its own prefix (n- nn- m- c-) and every reference is rewritten with it (spec §2).
// Glyphs: DejaVu Sans Bold through textlayout.js's own run/advance/kerning, one glyph per code point (opentype.js's stringToGlyphs would set the
// U+FB02 fl ligature in "reflect"/"reflection"; the spec's numbers are those of the code points, so the cmap glyph of each code point is used;
// every other string comes out byte-identical either way, and that is asserted).
// Usage: node build-five.js            (gates, then the five SVGs + work/layout_report.json)
//        node build-five.js --gates-only (the regression gates only, as JSON on stdout; writes nothing)
const fs=require('fs'), crypto=require('crypto'), path=require('path'); const T=require('../lockscreen/textlayout.js'); const n=T.n;
const ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2', VM=ROOT+'/vector-masters', OUT=process.env.J4_OUT||VM+'/tetrasemaphore-build7-j4-screens';
const CANON=VM+'/work/lockscreen-tetrasemaphore/build-five.js'; if(path.resolve(__filename)!==CANON) throw new Error('run build-five.js from its canonical path '+CANON+' (the copy in work/ is the record, not a runnable; lane rule after the 21 Oct skeptic panel, R1)');
const SPEC='/Users/careybalboa/Downloads/TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md', SPEC16='a2131c898acbb0e8';
const SRC=VM+'/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg', SRC16='1cf8f0f9f4aa30ea';
const TPL=VM+'/tetrasemaphore-build7/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE-MASTER.svg', TPL16='a62a3dd185089960';
const NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/', FONT16='7e69e81478e233b8';
const GATES_ONLY=process.argv.includes('--gates-only');
const sha16=b=>crypto.createHash('sha256').update(b).digest('hex').slice(0,16);
const must=(c,m)=>{ if(!c) throw new Error(m); };
must(sha16(fs.readFileSync(SPEC))===SPEC16,'spec is not revision 4 (a2131c898acbb0e8)');
must(sha16(fs.readFileSync(SRC))===SRC16,'no-title lock-screen master moved');
must(sha16(fs.readFileSync(TPL))===TPL16,'build-7 METACOGNITIVE template moved');
must(sha16(fs.readFileSync(T.FONT))===FONT16,'font is not 7e69e81478e233b8');
const COINS={
 'NORMATIVE':    {hash:'e0b6366d5c032523',ring:'#D5AF64',glyph:'#C7B469',field:'#181403',op:'I', map:' : (x, y) → (x, y)',  opname:'I, the identity',          glyphname:'the Fix gold',   prefix:'n-'},
 'NON-NORMATIVE':{hash:'4ef1de6ae126279e',ring:'#4FB5B5',glyph:'#4FB5B5',field:'#001817',op:'σᵥ',map:' : (x, y) → (−x, y)', opname:'σᵥ, the left-right mirror',glyphname:'the mark colour',prefix:'nn-'},
 'METACOGNITIVE':{hash:'cccfcff10dc74930',ring:'#B498E6',glyph:'#B498E6',field:'#17121D',op:'σₕ',map:' : (x, y) → (x, −y)', opname:'σₕ, the top-bottom mirror',glyphname:'the mark colour',prefix:'m-'},
 'CRITICAL':     {hash:'33413c4af9ec838c',ring:'#E25C60',glyph:'#E25C60',field:'#1F100E',op:'C₂',map:' : (x, y) → (−x, −y)',opname:'C₂, the half-turn',        glyphname:'the mark colour',prefix:'c-'},
};
const SIZE=58, AXIS=603, PAD=43.625, SW=4, R=28, BOXH=108, CREAM='#E8E0D2', GOLD='#D4A853', PITCH=69.875;
// with-title coordinates inside the layers (the layers carry the φ-rhythm transforms of build-notitle-phi.js)
const BOXY1=1453, BASE1=1526.625, BOXY2=1601, BASE2=1674.625, DIVCY=1759, MOT1=1853.75;
const TY={operator:-124.279, forall:-99.557, 'divider-1':-74.836, cogito:-50.115}, LOCK_DY=202.877;
// ---- text: textlayout.js's run/advance/inkBox with one glyph per code point (its stringToGlyphs shadowed by the cmap mapping, nothing else changed)
function cp(fn){ const f=T.font, own=Object.prototype.hasOwnProperty.call(f,'stringToGlyphs'), orig=f.stringToGlyphs;
  f.stringToGlyphs=function(s){ return Array.from(s).map(c=>f.charToGlyph(c)); }; try{ return fn(); } finally{ if(own) f.stringToGlyphs=orig; else delete f.stringToGlyphs; } }
const run=(t,x,y)=>cp(()=>T.run(t,SIZE,x,y,0)), adv=t=>cp(()=>T.advance(t,SIZE,0)), ink=(t,x,y)=>cp(()=>T.inkBox(t,SIZE,x,y,0));
const ligs=t=>{ const a=T.font.stringToGlyphs(t).map(g=>g.index).join(','), b=cp(()=>T.font.stringToGlyphs(t)).map(g=>g.index).join(','); return a===b?null:T.font.stringToGlyphs(t).filter(g=>g.unicode&&g.unicode>=0xFB00&&g.unicode<=0xFB06).map(g=>'U+'+g.unicode.toString(16).toUpperCase()); };
const r3=v=>Math.round(v*1000)/1000;
function boxGeom(text){ const a=adv(text); const w=Math.round((a+88)/2)*2; const bx=AXIS-w/2; return {adv:a,w,bx,tx:bx+PAD}; }
const rectSvg=(bx,by,w,stroke)=>`<rect x="${n(bx+SW/2)}" y="${n(by+SW/2)}" width="${n(w-SW)}" height="${n(BOXH-SW)}" rx="${n(R-SW/2)}" fill="none" stroke="${stroke}" stroke-width="${SW}"/>`;
// a boxed row: split = number of leading code points in `glyph` (0: the whole line one cream path, as assemble.js's single-segment rows)
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
// ---- layer surgery on the masters
function span(s,id){ const k=s.indexOf(`<g inkscape:groupmode="layer" id="${id}"`); must(k>=0,'no layer '+id); const re=/<g\b|<\/g>/g; re.lastIndex=k; let d=0,m;
  while((m=re.exec(s))){ d+=m[0]==='</g>'?-1:1; if(d===0) return [k,re.lastIndex]; } throw new Error('unclosed layer '+id); }
const layer=(s,id)=>{ const [a,b]=span(s,id); return s.slice(a,b); };
const openTag=l=>l.slice(0,l.indexOf('>')+1), innerOf=l=>l.slice(l.indexOf('>')+1,l.length-4);
const src=fs.readFileSync(SRC,'utf8'), tpl=fs.readFileSync(TPL,'utf8');
// ---- regression gates, before anything is written
const G={};
{ const L=layer(src,'sigma-h'); must(openTag(L)==='<g inkscape:groupmode="layer" id="sigma-h" transform="translate(0 -124.279)" inkscape:label="σₕ box">','σₕ layer open tag');
  const reg=boxRow('σₕ : (x, y) → (x, −y)',2,'#8C4191','#B498E6',BOXY1,BASE1); const ok=reg.svg===innerOf(L);
  const L7=layer(tpl,'operator'); const reg7=boxRow('σₕ : (x, y) → (x, −y)',2,'#B498E6','#B498E6',BOXY1,BASE1); const ok7=reg7.svg===innerOf(L7);
  G.sigma_h_row={pass:ok&&ok7&&reg.textlayout_identical,'16_sep_sigma_h_layer_bytes':innerOf(L).length,'16_sep_identical':ok,'build7_operator_layer_bytes':innerOf(L7).length,'build7_identical':ok7,w:reg.w,box_x:reg.bx,text_x:reg.tx,advance:r3(reg.adv)}; }
{ const C=innerOf(layer(tpl,'cogito')), F=innerOf(layer(tpl,'forall')), M=innerOf(layer(src,'m-def')), M7=innerOf(layer(tpl,'m-def'));
  const c1=line('I metacognize; therefore,',MOT1,185.875), c2=line('I am again and again.',MOT1+PITCH,248.375);
  const fa=boxRow('∀n. M(Iₙ) ⊢ Iₙ₊₁',0,GOLD,null,BOXY2,BASE2,360), md=boxRow('M := λx.Think(Think(x))',0,GOLD,null,2037,2110.625,217.125);
  const motto_ok=(c1.svg+c2.svg)===C, forall_ok=fa.svg===F, mdef_ok=md.svg===M&&M===M7;
  G.motto_and_rows={pass:motto_ok&&forall_ok&&mdef_ok&&c1.textlayout_identical&&c2.textlayout_identical&&fa.textlayout_identical&&md.textlayout_identical,
    cogito_layer_bytes:C.length,cogito_identical:motto_ok,forall_layer_bytes:F.length,forall_identical:forall_ok,m_def_layer_bytes:M.length,m_def_identical:mdef_ok,
    note:'rects from the box rule (width = advance + 88 to the nearest even px, x = 603 − w/2) and glyphs from run() at the 16 Sep master\'s own text x; the 16 Sep text x values were fitted to the Claude Design reference, so the rule gives different x for these four lines (see rule_x)',
    lines:[{text:'I metacognize; therefore,',advance:r3(c1.adv),x_in_master:185.875,rule_x:centreX('I metacognize; therefore,')},{text:'I am again and again.',advance:r3(c2.adv),x_in_master:248.375,rule_x:centreX('I am again and again.')}],
    rows:[{text:'∀n. M(Iₙ) ⊢ Iₙ₊₁',w:fa.w,box_x:fa.bx,text_x_in_master:360,rule_text_x:fa.bx+PAD,advance:r3(fa.adv)},{text:'M := λx.Think(Think(x))',w:md.w,box_x:md.bx,text_x_in_master:217.125,rule_text_x:md.bx+PAD,advance:r3(md.adv)}]}; }
{ const ok=layer(src,'divider-1')===layer(tpl,'divider-1')&&layer(src,'ground')===layer(tpl,'ground'); G.template_layers={pass:ok,divider_1_and_ground_identical_16_sep_vs_build7:ok}; }
if(GATES_ONLY){ console.log(JSON.stringify(G,null,1)); process.exit(Object.values(G).every(g=>g.pass)?0:1); }
for(const [k,g] of Object.entries(G)) must(g.pass,'regression gate failed: '+k+' '+JSON.stringify(g));
console.log('regression: σₕ row byte for byte (16 Sep and build 7), motto + ∀n + M := byte for byte, divider 1 + ground identical');
// ---- coins
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
// ---- the five screens (numbers transcribed from the spec's tables; every computed value is asserted equal to them to 0.001 px)
const STATE=[
 {st:'NORMATIVE',    op:{adv:515.062,w:604,bx:301,tx:344.625}, rule:{text:'∀g. I ∘ g = g',adv:398.920,w:486,bx:360,tx:403.625},
  motto:[['I state the standard.',674.448,265.750],['It marks epistemic status,',855.132,175.375],['not infallibility.',497.645,354.125]]},
 {st:'NON-NORMATIVE',op:{adv:616.307,w:704,bx:251,tx:294.625}, rule:{text:'det(σᵥ) = −1',adv:413.760,w:502,bx:352,tx:395.625},
  motto:[['I reflect the standard.',720.497,242.750],['It is reflection, not rejection.',943.208,131.375]]},
 {st:'CRITICAL',     op:{adv:658.646,w:746,bx:230,tx:273.625}, rule:{text:'σᵥ ∘ σₕ = C₂',adv:379.464,w:468,bx:369,tx:412.625},
  motto:[['I invert the standard.',700.645,252.625],['It is structured inversion,',833.778,186.125],['not reaction.',421.293,392.375]]},
];
const FOUR={sym:{text:'V₄ = {I, σᵥ, σₕ, C₂}',adv:603.902,w:692,bx:257,tx:300.625}, law:{text:'∀g ∈ V₄. g ∘ g = I',adv:561.592,w:650,bx:278,tx:321.625},
  sentence:[['Four boxes;',383.032,411.500],['one move between any two;',923.384,141.250],['the way back is the same move.',1047.512,79.250]]};
const ORDER=['NORMATIVE','NON-NORMATIVE','METACOGNITIVE','CRITICAL'], CELLNAME=['top-left','top-right','bottom-left','bottom-right'];
const GRID={card:{scale:'0.437899692',cells:[['211.562','481.123'],['635.361','481.123'],['211.562','904.922'],['635.361','904.922']],dy:0},
            lock:{scale:'0.561605269',cells:[['110.123','481.123'],['635.361','481.123'],['110.123','1006.361'],['635.361','1006.361']],dy:LOCK_DY}};
const SPECX={ card:{row1:1328.721,base1:1402.346,row2:1501.443,base2:1575.068,div:1674.164,rule_y:1682.164,dcy:1684.164,lines:[1803.635,1873.510,1943.385]},
              lock:{row1:1531.598,base1:1605.223,row2:1704.320,base2:1777.945,div:1877.041,rule_y:1885.041,dcy:1887.041,lines:[2006.512,2076.387,2146.262]} };
const T0='translate(312 684) scale(0.708536585)';
const near=(a,b,m)=>must(Math.abs(a-b)<0.0005,`${m}: built ${a}, spec ${b}`);
const DIV1=layer(src,'divider-1'); must(openTag(DIV1)==='<g inkscape:groupmode="layer" id="divider-1" transform="translate(0 -74.836)" inkscape:label="divider 1">','divider-1 open tag');
const head=src.slice(0,src.indexOf('<g inkscape:groupmode="layer" id="medallion"')); const GROUND=layer(src,'ground');
must(head.endsWith(GROUND+'\n'),'header layout'); const ROOTTAG=head.slice(0,head.indexOf('\n<title>'));
must(ROOTTAG==='<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1206" height="2622" viewBox="0 0 1206 2622">','root tag');
const SPECREF=`Science's layout spec ~/Downloads/TETRASEMAPHORE-SCIENCE-J4-LAYOUT-SPEC.md, revision 4 of 21 Oct 2026 (sha256-16 ${SPEC16})`;
const FONTREF=`DejaVu Sans Bold 2.34 (dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf, sha256-16 ${FONT16}) at 58 px, outlined as paths by vector-masters/work/lockscreen/textlayout.js (opentype.js 1.3.4, kerning on) with its stringToGlyphs shadowed by a per-code-point cmap mapping, so no ligature is set: as shipped, textlayout.js would set the fl ligature U+FB02 in 'reflect' and 'reflection' (advances 718.373 / 941.084 against the spec's 720.497 / 943.208); every other string is byte-identical either way; no live text, no raster`;
const safe=s=>{ must(!/[<>&"]/.test(s),'unsafe metadata text: '+s); return s; };
fs.mkdirSync(OUT+'/work',{recursive:true}); fs.mkdirSync(OUT+'/proofs',{recursive:true});
const report={generator:'vector-masters/work/lockscreen-tetrasemaphore/build-five.js',date:'2026-10-21',spec:{file:SPEC,sha16:SPEC16,revision:4},
  sources:{no_title_master:{file:SRC,sha16:SRC16},template:{file:TPL,sha16:TPL16},font:{file:T.FONT,sha16:FONT16}},regression_gates:G,
  glyph_mapping:'one glyph per code point (cmap); textlayout.js stringToGlyphs (opentype.js 1.3.4) would substitute the U+FB02 fl ligature in the lines marked textlayout_ligature',screens:{}};
function stackLayers(rows,dy,labels){ // rows: {operator,forall,cogito} inner svg; dy: 0 (card grid) or 202.877 (lock screen)
  const tr=id=>n(TY[id]+dy);
  const op=`<g inkscape:groupmode="layer" id="operator" transform="translate(0 ${tr('operator')})" inkscape:label="${safe(labels.operator)}">${rows.operator}</g>`;
  const fa=`<g inkscape:groupmode="layer" id="forall" transform="translate(0 ${tr('forall')})" inkscape:label="${safe(labels.forall)}">${rows.forall}</g>`;
  const dv=dy?DIV1.replace('transform="translate(0 -74.836)"',`transform="translate(0 ${tr('divider-1')})"`):DIV1;
  const cg=`<g inkscape:groupmode="layer" id="cogito" transform="translate(0 ${tr('cogito')})" inkscape:label="${safe(labels.cogito)}">${rows.cogito}</g>`;
  return `<g inkscape:groupmode="layer" id="stack" inkscape:label="${safe(labels.stack)}">${op}${fa}${dv}${cg}</g>`; }
function finish(name,file,title,desc,figure,stack,rep){
  const out=`${ROOTTAG}\n<title>${safe(title)}</title>\n<desc>${safe(desc)}</desc>\n${GROUND}\n${figure}\n\n${stack}\n</svg>`;
  const ids=idsOf(out); const dup=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))]; must(!dup.length,name+' duplicate ids '+dup);
  const idset=new Set(ids); const refs=refsOf(out); const bad=refs.filter(r=>!idset.has(r)); must(!bad.length,name+' unresolved references '+bad);
  must(!/<text\b|<image\b|<foreignObject\b|<script\b|<style\b/.test(out),name+': text/image/script/style');
  fs.writeFileSync(OUT+'/'+file,out); rep.file=file; rep.sha16=sha16(fs.readFileSync(OUT+'/'+file)); rep.bytes=Buffer.byteLength(out); rep.ids=ids.length; rep.references=refs.length;
  report.screens[name]=rep; console.log(name.padEnd(20),rep.sha16,file); }
const lineRep=(L,text,base_wt,ty,sx,sb)=>{ const cps=Array.from(text).map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0'));
  return {string:text,code_points:cps,advance:r3(L.adv),textlayout_advance:r3(L.textlayout_advance),textlayout_ligature:ligs(text),textlayout_identical:L.textlayout_identical,
    x:L.x,baseline:r3(base_wt+ty),baseline_in_layer:base_wt,layer_ty:ty,fill:CREAM,spec:{advance:sx[0],x:sx[1],baseline:sb},
    ink:{x1:r3(L.ink.x1),y1:r3(L.ink.y1+ty),x2:r3(L.ink.x2),y2:r3(L.ink.y2+ty)}}; };
const rowRep=(B,text,ty,boxy,base,stroke,role)=>({role,string:text,code_points:Array.from(text).map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')),
  advance:r3(B.adv),textlayout_advance:r3(B.textlayout_advance),textlayout_ligature:ligs(text),textlayout_identical:B.textlayout_identical,
  box:{x:B.bx,y:r3(boxy+ty),w:B.w,h:BOXH,rx:R,stroke_width:SW,stroke,rect_as_written:{x:B.bx+2,y:r3(boxy+2+ty),width:B.w-4,height:BOXH-4,rx:R-2,y_in_layer:boxy+2}},
  text_x:B.tx,baseline:r3(base+ty),baseline_in_layer:base,layer_ty:ty,path_fills:B.paths,glyph_split_code_points:B.split,
  ink:{x1:r3(B.ink.x1),y1:r3(B.ink.y1+ty),x2:r3(B.ink.x2),y2:r3(B.ink.y2+ty)}});
const divRep=dy=>({layer_ty:r3(TY['divider-1']+dy),rule:{x:503,y:r3(1757+TY['divider-1']+dy),w:200,h:4,fill:GOLD},diamond:{cx:603,cy:r3(DIVCY+TY['divider-1']+dy),half_diagonal:r3(14/Math.SQRT2),fill:GOLD},row_y:r3(1749+TY['divider-1']+dy),bytes_identical_to_master:dy===0});
// (a) the three state cards
for(const S of STATE){ const C=COINS[S.st]; const inner=coinInner(S.st); const X=SPECX.card;
  const opText=C.op+C.map; const op=boxRow(opText,Array.from(C.op).length,C.ring,C.glyph,BOXY1,BASE1);
  near(op.adv,S.op.adv,S.st+' operator advance'); near(op.w,S.op.w,S.st+' operator w'); near(op.bx,S.op.bx,S.st+' operator x'); near(op.tx,S.op.tx,S.st+' operator text x');
  near(BOXY1+TY.operator,X.row1,'row 1 y'); near(BASE1+TY.operator,X.base1,'row 1 baseline');
  const ru=boxRow(S.rule.text,0,GOLD,null,BOXY2,BASE2); near(ru.adv,S.rule.adv,S.st+' rule advance'); near(ru.w,S.rule.w,S.st+' rule w'); near(ru.bx,S.rule.bx,S.st+' rule x'); near(ru.tx,S.rule.tx,S.st+' rule text x');
  near(BOXY2+TY.forall,X.row2,'row 2 y'); near(BASE2+TY.forall,X.base2,'row 2 baseline'); near(1749+TY['divider-1'],X.div,'divider y'); near(1757+TY['divider-1'],X.rule_y,'rule y'); near(DIVCY+TY['divider-1'],X.dcy,'diamond y');
  const ML=S.motto.map(([t,a,x],i)=>{ const L=line(t,MOT1+i*PITCH); near(L.adv,a,S.st+' motto advance '+t); near(L.x,x,S.st+' motto x '+t); near(MOT1+i*PITCH+TY.cogito,X.lines[i],'motto baseline'); return L; });
  const med=`<g inkscape:groupmode="layer" id="medallion" inkscape:label="medallion (linked master ${C.hash}: the Tetrasemaphore ${S.st} coin, build 7, inlined verbatim, its ids unchanged; proposal)"><g id="medallion-slot820" transform="${T0}">${inner}</g></g>`;
  const mottoTxt=S.motto.map(m=>m[0]).join(' / ');
  const labels={stack:`type stack (no title; the build-7 METACOGNITIVE screen's rows and layer transforms, gaps 40·φ = 64.72, its divider 2 and M := box dropped): operator row · rule box · divider · motto`,
    operator:`operator row: ${opText} (${C.opname}); box ${op.w} × 108 at x ${op.bx}, y 1328.721 (text advance ${r3(op.adv)} + 88, to the nearest even px), stroke the coin's ring colour ${C.ring}; the operator ${C.op} in ${C.glyphname} ${C.glyph}, the rest cream ${CREAM}; text x ${op.tx}, baseline 1402.346`,
    forall:`rule box: ${S.rule.text}; box ${ru.w} × 108 at x ${ru.bx}, y 1501.443 (text advance ${r3(ru.adv)} + 88, to the nearest even px), stroke gold ${GOLD}, text cream ${CREAM}; text x ${ru.tx}, baseline 1575.068`,
    cogito:`motto (${ML.length} lines, unboxed, cream, centred on x 603): ${mottoTxt}; baselines ${X.lines.slice(0,ML.length).join(', ')}`};
  const stack=stackLayers({operator:op.svg,forall:ru.svg,cogito:ML.map(L=>L.svg).join('')},0,labels);
  const title=`Dose 01 · iPhone 17 Pro · Tetrasemaphore ${S.st} flashcard (build-7 coin) · layered vector master (1206 × 2622) · proposal`;
  const desc=`The Tetrasemaphore ${S.st} flashcard, one of the three state cards of J4, built as ${SPECREF}, §3. Rows, top to bottom: the coin, the operator row, one rule box, a divider, the motto; no bottom box. Built 2026-10-21 by vector-masters/work/lockscreen-tetrasemaphore/build-five.js as a layer swap on the no-title lock-screen master vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg (sha256-16 ${SRC16}: assemble.js laid out without the title by build-notitle-phi.js, 16 Sep), the build-meta7.js recipe of the accepted METACOGNITIVE screen (${TPL16}): the ground and divider 1 are byte-identical to that master; the rows keep its layer transforms (operator −124.279, rule −99.557, divider −74.836, motto −50.115), so row 1 is at y 1328.721, row 2 at 1501.443, the divider at 1674.164 and the motto baselines at 1803.635 / 1873.51 / 1943.385, the deck's row grid; divider 2 and the M := box are dropped. Coin: master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-${S.st}-notation-slot820.svg (sha256-16 ${C.hash}, build 7: its mark on its own field ${C.field}, rings ${C.ring}, English legend shown, Spanish legend layers inside, hidden), its root content inlined verbatim (title, desc and inkscape attributes stripped; no recolouring, no clip, no crop) at ${T0}, a 581 px box centred (602.5, 974.5), the registration of the owl medallion; one coin per document, so its ids are unchanged (no prefix). Operator row ${opText}: box ${op.w} × 108 at x ${op.bx}, stroke the coin's ring colour ${C.ring}, the operator ${C.op} in ${C.glyphname} ${C.glyph}, the rest cream ${CREAM}. Rule box ${S.rule.text}: ${ru.w} × 108 at x ${ru.bx}, stroke gold ${GOLD}, text cream. Boxes: width = text advance + 88 to the nearest even px, centred on x 603, text from box x + 43.625, stroke 4, radius 28. Motto, unboxed, cream, each line centred on x 603 to 1/8 px: ${mottoTxt} Divider: gold 200 × 4 rule and diamond. ${FONTREF}. Proposal, not final; Carey decides.`;
  finish(S.st,`dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-${S.st}-flashcard-MASTER.svg`,title,desc,med,stack,{kind:'state flashcard',spec_section:'§3',
    coins:[{state:S.st,master:`MASTER-medallion-${S.st}-notation-slot820.svg`,sha16:C.hash,transform:T0,translate:[312,684],scale:0.708536585,box_px:r3(820*0.708536585),cell:{x:312,y:684,w:r3(820*0.708536585),h:r3(820*0.708536585)},prefix:null,ids:idsOf(inner).length+1,references:refsOf(inner).length,ring:C.ring,mark:C.glyph,field:C.field}],
    layers:{ground:'byte-identical to '+SRC16,medallion:'coin',operator:r3(TY.operator),forall:r3(TY.forall),'divider-1':r3(TY['divider-1']),cogito:r3(TY.cogito)},
    rows:[rowRep(op,opText,TY.operator,BOXY1,BASE1,C.ring,'operator row'),rowRep(ru,S.rule.text,TY.forall,BOXY2,BASE2,GOLD,'rule box')],divider:divRep(0),
    lines:ML.map((L,i)=>lineRep(L,S.motto[i][0],MOT1+i*PITCH,TY.cogito,[S.motto[i][1],S.motto[i][2]],X.lines[i]))}); }
// (b) and (c) the all-four screens
for(const kind of ['card','lock']){ const Gd=GRID[kind], X=SPECX[kind], dy=Gd.dy, sc=+Gd.scale;
  const sym=boxRow(FOUR.sym.text,0,GOLD,null,BOXY1,BASE1), law=boxRow(FOUR.law.text,0,GOLD,null,BOXY2,BASE2);
  for(const [B,E] of [[sym,FOUR.sym],[law,FOUR.law]]){ near(B.adv,E.adv,kind+' advance '+E.text); near(B.w,E.w,kind+' w '+E.text); near(B.bx,E.bx,kind+' x '+E.text); near(B.tx,E.tx,kind+' text x '+E.text); }
  near(BOXY1+TY.operator+dy,X.row1,kind+' row 1 y'); near(BASE1+TY.operator+dy,X.base1,kind+' row 1 baseline'); near(BOXY2+TY.forall+dy,X.row2,kind+' row 2 y'); near(BASE2+TY.forall+dy,X.base2,kind+' row 2 baseline');
  near(1749+TY['divider-1']+dy,X.div,kind+' divider y'); near(1757+TY['divider-1']+dy,X.rule_y,kind+' rule y'); near(DIVCY+TY['divider-1']+dy,X.dcy,kind+' diamond y');
  const SL=FOUR.sentence.map(([t,a,x],i)=>{ const L=line(t,MOT1+i*PITCH); near(L.adv,a,kind+' sentence advance '+t); near(L.x,x,kind+' sentence x '+t); near(MOT1+i*PITCH+TY.cogito+dy,X.lines[i],kind+' sentence baseline'); return L; });
  // the grid: coin box 820·s, pitch box + 40·φ, side 2·box + 40·φ centred on 603, bottom one φ gap above row 1
  const box=820*sc, gap=40*(1+Math.sqrt(5))/2; near(+Gd.cells[0][1]+2*box+gap+gap,X.row1,kind+' grid bottom + φ gap = row 1');
  const coinsRep=[]; const cells=ORDER.map((st,i)=>{ const C=COINS[st]; const [tx,ty]=Gd.cells[i]; const tr=`translate(${tx} ${ty}) scale(${Gd.scale})`;
    const inner=coinInner(st); const pin=prefixIds(inner,C.prefix); const cid=C.prefix+'medallion-slot820';
    const own=idsOf(pin), refs=refsOf(pin); must(own.every(x=>x.startsWith(C.prefix)),st+': unprefixed id'); must(refs.every(r=>r.startsWith(C.prefix)&&own.includes(r)),st+': reference outside its coin');
    must(idsOf(inner).length===own.length&&refsOf(inner).length===refs.length,st+': prefixing changed the id/reference count');
    must(pin.replace(new RegExp(`(\\sid="|url\\(#|href="#)${C.prefix.replace('-','\\-')}`,'g'),'$1')===inner,st+': prefixing changed something other than ids and references');
    coinsRep.push({cell:CELLNAME[i],state:st,master:`MASTER-medallion-${st}-notation-slot820.svg`,sha16:C.hash,transform:tr,translate:[+tx,+ty],scale:sc,box_px:r3(box),cell_box:{x:+tx,y:+ty,w:r3(box),h:r3(box)},prefix:C.prefix,ids:own.length+1,references:refs.length,group_id:cid});
    return `<g inkscape:groupmode="layer" id="${cid}" transform="${tr}" inkscape:label="${safe(`${CELLNAME[i]}: the Tetrasemaphore ${st} coin (linked master ${C.hash}, build 7), inlined verbatim with every id and reference prefixed ${C.prefix}`)}">${pin}</g>`; });
  const left=+Gd.cells[0][0], top=+Gd.cells[0][1];
  const fig=`<g inkscape:groupmode="layer" id="figure" inkscape:label="${safe(`figure: the four Tetrasemaphore coins of build 7, 2 × 2 (NORMATIVE top-left, NON-NORMATIVE top-right, METACOGNITIVE bottom-left, CRITICAL bottom-right), scale ${Gd.scale}, coin ${r3(box)} px, pitch ${r3(box+gap)} px, grid ${r3(2*box+gap)} px from x ${left}, y ${top}`)}">${cells.join('')}</g>`;
  const sentTxt=FOUR.sentence.map(m=>m[0]).join(' / ');
  const labels={stack:kind==='card'?`type stack (no title; the deck's row grid, the build-7 METACOGNITIVE screen's rows and layer transforms, gaps 40·φ = 64.72): the four symbols · the law · divider · the sentence`
                                   :`type stack (no title; the card's rows moved 202.877 px down as whole layers, gaps 40·φ = 64.72): the four symbols · the law · divider · the sentence`,
    operator:`the four symbols: ${FOUR.sym.text}; box ${sym.w} × 108 at x ${sym.bx}, y ${X.row1}, stroke gold ${GOLD}, all text cream ${CREAM}; text x ${sym.tx}, baseline ${X.base1}`,
    forall:`the law: ${FOUR.law.text}; box ${law.w} × 108 at x ${law.bx}, y ${X.row2}, stroke gold ${GOLD}, text cream ${CREAM}; text x ${law.tx}, baseline ${X.base2}`,
    cogito:`the sentence (three lines on its own semicolons, unboxed, cream, centred on x 603): ${sentTxt}; baselines ${X.lines.join(', ')}`};
  const stack=stackLayers({operator:sym.svg,forall:law.svg,cogito:SL.map(L=>L.svg).join('')},dy,labels);
  const isCard=kind==='card', NAME=isCard?'ALL-FOUR-flashcard':'ALL-FOUR-lockscreen';
  const title=isCard?`Dose 01 · iPhone 17 Pro · Tetrasemaphore fifth flashcard, all four states (build-7 coins) · layered vector master (1206 × 2622) · proposal`
                    :`Dose 01 · iPhone 17 Pro lock screen · Tetrasemaphore fifth lock screen, all four states (build-7 coins) · layered vector master (1206 × 2622) · proposal, held`;
  const cellTxt=coinsRep.map(c=>`${c.cell} ${c.state} (${c.sha16}) at ${c.transform}, ids prefixed ${c.prefix}`).join('; ');
  const desc=(isCard?`The Tetrasemaphore fifth flashcard, all four states, built as ${SPECREF}, §4. `:`The Tetrasemaphore fifth lock screen, all four states, built as ${SPECREF}, §5. Held for Carey's phone check, 21 Oct. `)+
   `Rows, top to bottom: the four coins 2 × 2, the four symbols, the law, a divider, the sentence; no title, no label, no caption (the coins carry their own legends). Built 2026-10-21 by vector-masters/work/lockscreen-tetrasemaphore/build-five.js as a layer swap on the no-title lock-screen master vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg (sha256-16 ${SRC16}), the build-meta7.js recipe of the accepted METACOGNITIVE screen (${TPL16}): the ground is byte-identical to that master and divider 1 is its divider-1 layer `+(isCard?`byte for byte; the rows keep its layer transforms (−124.279, −99.557, −74.836, −50.115), the deck's row grid: row 1 y 1328.721, row 2 y 1501.443, divider 1674.164, sentence baselines 1803.635 / 1873.51 / 1943.385.`:`with only its transform changed; every row is the card's moved 202.877 px down as a whole layer (transforms 78.598, 103.32, 128.041, 152.762): row 1 y 1531.598, row 2 y 1704.32, divider 1877.041, sentence baselines 2006.512 / 2076.387 / 2146.262.`)+
   ` Figure: the four build-7 coin masters of master/states/proposals/notation/final-masters-2026-10-05/ (sha256-16 NORMATIVE e0b6366d5c032523, NON-NORMATIVE 4ef1de6ae126279e, METACOGNITIVE cccfcff10dc74930, CRITICAL 33413c4af9ec838c), each root content inlined verbatim (title, desc and inkscape attributes stripped; no recolouring, no clip, no crop) under one uniform scale ${Gd.scale} (coin ${r3(box)} px, gap 40·φ = 64.721 px, grid ${r3(2*box+gap)} px centred on x 603 from y 481.123): ${cellTxt}. Per spec §2 every id of a coin and every reference to it (the url references in any attribute, href, xlink:href, begin, end, aria-labelledby, aria-describedby) carries that coin's prefix, so each coin resolves inside itself. Both boxes gold ${GOLD}, all text cream ${CREAM}: ${FOUR.sym.text} (box ${sym.w} at x ${sym.bx}) and ${FOUR.law.text} (box ${law.w} at x ${law.bx}); width = text advance + 88 to the nearest even px, centred on x 603, text from box x + 43.625, stroke 4, radius 28. The sentence, unboxed, cream, each line centred on x 603 to 1/8 px: ${sentTxt} ${FONTREF}. Proposal, not final; Carey decides.`;
  finish(NAME,`dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-${NAME}-MASTER.svg`,title,desc,fig,stack,{kind:isCard?'fifth flashcard (all four)':'fifth lock screen (all four), held for Carey\'s phone check, 21 Oct',spec_section:isCard?'§4':'§5',
    grid:{scale:sc,box_px:r3(box),pitch:r3(box+gap),side:r3(2*box+gap),x0:left,y0:top,bottom:r3(top+2*box+gap)},coins:coinsRep,
    layers:{ground:'byte-identical to '+SRC16,figure:'four coin sub-layers',operator:r3(TY.operator+dy),forall:r3(TY.forall+dy),'divider-1':r3(TY['divider-1']+dy),cogito:r3(TY.cogito+dy)},
    rows:[rowRep(sym,FOUR.sym.text,TY.operator+dy,BOXY1,BASE1,GOLD,'the four symbols'),rowRep(law,FOUR.law.text,TY.forall+dy,BOXY2,BASE2,GOLD,'the law')],divider:divRep(dy),
    lines:SL.map((L,i)=>lineRep(L,FOUR.sentence[i][0],MOT1+i*PITCH,TY.cogito+dy,[FOUR.sentence[i][1],FOUR.sentence[i][2]],X.lines[i]))}); }
fs.writeFileSync(OUT+'/work/layout_report.json',JSON.stringify(report,null,1)+'\n');
fs.copyFileSync(CANON,OUT+'/work/build-five.js');
console.log('wrote',Object.keys(report.screens).length,'screens and work/layout_report.json');
