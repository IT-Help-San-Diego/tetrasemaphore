// independent check helper: per-glyph path data for (text,size,x,baseline) requests, from the lane's own textlayout.js
const T=require('/Users/careybalboa/Downloads/dose-01-meander-v2/vector-masters/work/lockscreen/textlayout.js'); const fs=require('fs');
const q=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const f=T.font; const orig=f.stringToGlyphs;
function one(r,liga){ if(!liga) f.stringToGlyphs=function(s){return Array.from(s).map(c=>f.charToGlyph(c));}; try{ const o=T.run(r.text,r.size||58,r.x,r.baseline,0); return {parts:o.parts,advance:+o.advance.toFixed(3)}; } finally { f.stringToGlyphs=orig; } }
console.log(JSON.stringify(q.map(r=>({liga:one(r,true),cp:one(r,false)}))));
