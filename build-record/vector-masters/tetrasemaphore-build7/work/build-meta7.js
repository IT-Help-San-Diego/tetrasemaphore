// The METACOGNITIVE Tetrasemaphore lock screen from the BUILD-7 coin (2026-10-14; Science's wake-up packet J2: "the METACOGNITIVE lock screen regenerated
// from the build-7 coin (build-four.js, METACOGNITIVE only)"). Same recipe as build-four.js (the build-6 set, accepted by Carey for METACOGNITIVE on
// 11 Oct): the coin in the owl medallion's place, the σₕ operator row in the σₕ row's place, the box stroke in the coin's ring colour, the glyph in
// the mark colour, everything else byte-identical to the 16 Sep no-title master. The three withdrawn screens are not rebuilt.
// Usage: META7_SHA16=<sha16 of the build-7 METACOGNITIVE master> node build-meta7.js
const fs=require('fs'), crypto=require('crypto'); const T=require('../lockscreen/textlayout.js'); const n=T.n;
const ROOT='/Users/careybalboa/Downloads/dose-01-meander-v2', OUT=ROOT+'/vector-masters/tetrasemaphore-build7';
const SRC=ROOT+'/vector-masters/dose-01-iphone-17-pro-lockscreen-1206x2622-MASTER.svg', NOT=ROOT+'/master/states/proposals/notation/final-masters-2026-10-05/';
const sha16=b=>crypto.createHash('sha256').update(b).digest('hex').slice(0,16);
if(sha16(fs.readFileSync(SRC))!=='1cf8f0f9f4aa30ea') throw new Error('lock-screen master moved');
const EXP=process.env.META7_SHA16; if(!EXP||!/^[0-9a-f]{16}$/.test(EXP)) throw new Error('set META7_SHA16 to the build-7 METACOGNITIVE master hash');
const STATES=[{st:'METACOGNITIVE',hash:EXP,op:'σₕ',map:' : (x, y) → (x, −y)',ring:'#B498E6',glyph:'#B498E6',field:'#17121D',opname:'σₕ, the top-bottom mirror',glyphname:'the mark colour'}];
const SIZE=58, BASE=1526.625, AXIS=603, PAD=43.625, SW=4, R=28, BOXY=1453, BOXH=108, CREAM='#E8E0D2';
function row(op,map,ring,glyph){ const full=op+map; const adv=T.advance(full,SIZE,0); const w=Math.round((adv+88)/2)*2; const bx=AXIS-w/2; const tx=bx+PAD;
  const r=T.run(full,SIZE,tx,BASE,0); const c1=Array.from(op).length;
  const svg=`<rect x="${n(bx+SW/2)}" y="${n(BOXY+SW/2)}" width="${n(w-SW)}" height="${n(BOXH-SW)}" rx="${n(R-SW/2)}" fill="none" stroke="${ring}" stroke-width="${SW}"/>`+
    `<path fill="${glyph}" d="${r.parts.slice(0,c1).join('')}"/><path fill="${CREAM}" d="${r.parts.slice(c1).join('')}"/>`;
  return {svg,w,bx,tx,adv:+adv.toFixed(3)}; }
const src=fs.readFileSync(SRC,'utf8');
const a=src.indexOf('<g inkscape:groupmode="layer" id="medallion"'), b=src.indexOf('<g inkscape:groupmode="layer" id="stack"');
const T0='translate(312 684) scale(0.708536585)'; if(!src.slice(a,b).includes(`<g id="medallion-slot820" transform="${T0}">`)) throw new Error('medallion transform');
const OPEN='<g inkscape:groupmode="layer" id="sigma-h" transform="translate(0 -124.279)" inkscape:label="σₕ box">';
const o=src.indexOf(OPEN); if(o<0) throw new Error('σₕ layer not found'); const oc=src.indexOf('</g>',o); const oldRow=src.slice(o+OPEN.length,oc); if(oldRow.includes('<g')) throw new Error('σₕ layer has nested groups');
const reg=row('σₕ',' : (x, y) → (x, −y)','#8C4191','#B498E6'); if(reg.svg!==oldRow) throw new Error('generator does not reproduce the σₕ row'); console.log('regression: σₕ row reproduced byte for byte (w '+reg.w+', x '+reg.bx+', text x '+reg.tx+')');
const oldTitle='<title>Dose 01 · iPhone 17 Pro lock screen · layered vector master (1206 × 2622) · no title</title>';
const oldMed='Medallion: inlined MASTER-medallion-METACOGNITIVE-slot820.svg (sha256-16 d4054fa6e02e66e4) at translate(312 684) scale(0.708536585) → centre (602.5, 974.5), outer diameter 580.3 px.';
if(!src.includes(oldTitle)||!src.includes(oldMed)) throw new Error('title/desc anchors');
fs.mkdirSync(OUT,{recursive:true}); const report={};
for(const S of STATES){
  const cf=NOT+`MASTER-medallion-${S.st}-notation-slot820.svg`; const cb=fs.readFileSync(cf); const h=sha16(cb); if(h!==S.hash) throw new Error(`${S.st} coin is ${h}, expected ${S.hash}`);
  const coin=cb.toString('utf8');
  if(!coin.includes(`inkscape:label="1 ${S.st} rings ${S.ring} `)) throw new Error(`${S.st}: ring colour ${S.ring} not the coin's`);
  if(!new RegExp(`<g id="glyph-body"[^>]*fill="${S.glyph}">`).test(coin)) throw new Error(`${S.st}: glyph colour ${S.glyph} not the coin's`);
  if(!coin.includes(`0 field: ${S.st} tint ${S.field}`)) throw new Error(`${S.st}: field ${S.field} not the coin's`);
  if(!coin.includes('more than 170 deg')) throw new Error(`${S.st}: the coin does not carry the build-7 guard label`);
  const mm=coin.match(/<svg[^>]*>([\s\S]*)<\/svg>\s*$/); const inner=mm[1].replace(/\s+inkscape:[a-z-]+="[^"]*"/g,'').replace(/<title>[\s\S]*?<\/title>/,'').replace(/<desc>[\s\S]*?<\/desc>/,'');
  const med=`<g inkscape:groupmode="layer" id="medallion" inkscape:label="medallion (linked master ${S.hash}: the Tetrasemaphore ${S.st} coin, build 7, proposal)"><g id="medallion-slot820" transform="${T0}">${inner}</g></g>\n\n`;
  const rw=row(S.op,S.map,S.ring,S.glyph);
  const lab=`${S.op} box: the coin's operator (${S.opname}) and its mapping, as the Owl Semaphore table (owl-semaphore README §2.2); box stroke in the coin's ring colour ${S.ring}, the operator glyph in ${S.glyphname} ${S.glyph}, the rest cream; box ${rw.w} × 108 centred on x 603 (text advance + 88, to the nearest even px, as the σₕ row), text from x ${rw.tx}`;
  let out=src.slice(0,a)+med+src.slice(b);
  const STALE='Title layer kept here (client removed the big title from the SHIRT 2026-09-16; on the lock screen it stays as approved).'; if(out.split(STALE).length!==2) throw new Error('stale title sentence not unique'); out=out.replace(STALE,'Title removed 2026-09-16 as on the shirt (build-notitle-phi.js: the six rows below the medallion moved down as whole layers, gaps 40 → 40·φ; the with-title master is in with-title-record/).');
  const oo=out.indexOf(OPEN), ooc=out.indexOf('</g>',oo); out=out.slice(0,oo)+`<g inkscape:groupmode="layer" id="operator" transform="translate(0 -124.279)" inkscape:label="${lab}">`+rw.svg+out.slice(ooc);
  out=out.replace(oldTitle,`<title>Dose 01 · iPhone 17 Pro lock screen · Tetrasemaphore ${S.st} coin (build 7) · layered vector master (1206 × 2622) · no title</title>`)
    .replace(oldMed,`Medallion: inlined master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-${S.st}-notation-slot820.svg (sha256-16 ${S.hash}: the Tetrasemaphore ${S.st} coin of build 7, its mark on its own field ${S.field}, rings ${S.ring}, the gold with flecks off and lit edges with the bow-tie guard, its English legend shown and its Spanish legend layers inside, hidden) at translate(312 684) scale(0.708536585) → centre (602.5, 974.5), a 581 px box (the ring's outer edge 580.6 px), the registration of the owl medallion it replaces (d4054fa6e02e66e4).`)
    .replace('Generated by vector-masters/work/lockscreen/assemble.js.</desc>',`Generated by vector-masters/work/lockscreen/assemble.js. Tetrasemaphore METACOGNITIVE screen, build 7, 2026-10-14 (vector-masters/work/lockscreen-tetrasemaphore/build-meta7.js, the build-four.js recipe of 2026-10-10 on the build-7 coin, from the no-title master 1cf8f0f9f4aa30ea, which is assemble.js's master laid out without the title by build-notitle-phi.js): the medallion layer, the operator row, the sentence about the title (was the σₕ row: now ${S.op}${S.map}, box ${rw.w} px wide, stroke ${S.ring}, glyph ${S.glyph}), the title and this description changed; the ground and every other row are byte-identical to that master. The ∀n line, the motto and the M := line stay as on the build-6 METACOGNITIVE screen, which Carey accepted by eye on 11 October (card 16). Proposal, not final.</desc>`);
  const ids=[...out.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]); const dup=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))]; if(dup.length) throw new Error(S.st+' duplicate ids '+dup);
  if(/<text\b|<image\b/.test(out)) throw new Error('text/image');
  const f=`${OUT}/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-${S.st}-MASTER.svg`; fs.writeFileSync(f,out);
  report[S.st]={file:f.split('/').pop(),sha16:sha16(fs.readFileSync(f)),coin_sha16:S.hash,row:{text:S.op+S.map,w:rw.w,box_x:rw.bx,text_x:rw.tx,advance:rw.adv,stroke:S.ring,glyph:S.glyph},ids:ids.length,hidden:(out.match(/style="display:none"/g)||[]).length};
}
console.log(JSON.stringify(report,null,1));
