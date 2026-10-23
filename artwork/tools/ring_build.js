// ring_build.js --out <file.svg> [--frame slot820|print1220] [--legendKeys 21,22,23,0,1,2 | none] [--seamFix 0|1] [--knobs <file>]
// One finished meander ring from the sealed recipe (meander3.js geometry rc 8 rf 7 + finish7.js with finish/finish7-knobs.txt, glints 1),
// the same call tools/ring-legend.js makes. --legendKeys none = the UNCUT ring (all 24 keys). Added 2026-10-05; edits no sealed tool.
// --knobs <file> (2026-10-09, build 5): read the finish knobs from this file instead of finish/finish7-knobs.txt; without it the output is
// unchanged byte for byte. finish/finish7-knobs-noflecks.txt = the same knobs plus --fleckOp 0 (Carey with Science, 9 Oct: the bright flecks off).
// --litEdge <opacity> (2026-10-10, build 6; Carey chose gold version 3; 2026-10-14 build 7: litedge.js carries Science's bow-tie guard): adds the lit-edge layer from tools/litedge.js (spec: Science's rulings
// doorbell update 3) directly after the finish layer and a sentence to <desc>; the finish7 output itself is untouched. Without it: unchanged.
const fs=require('fs'), path=require('path'); const {build}=require(path.join(__dirname,'finish7.js')); const {DEFAULTS}=require(path.join(__dirname,'meander3.js'));
const A={frame:'slot820',legendKeys:'none',seamFix:'0',litEdge:'0'}; const av=process.argv.slice(2); for(let i=0;i<av.length;i+=2) A[av[i].slice(2)]=av[i+1];
if(!A.out) throw new Error('--out required');
const knobs='--rc 8 --rf 7 --glints 1 '+fs.readFileSync(A.knobs||path.join(__dirname,'..','finish','finish7-knobs.txt'),'utf8').trim();
const a=knobs.split(/\s+/); const g={}, f={};
for(let i=0;i<a.length;i+=2){const k=a[i].slice(2), v=a[i+1]; const val=isNaN(v)?v:parseFloat(v); if(k in DEFAULTS) g[k]=val; else f[k]=val;}
const p=Object.assign({},g,{frame:A.frame}); if(A.legendKeys!=='none') p.legendKeys=A.legendKeys.split(',').map(Number); if(+A.seamFix) p.seamFix=1;
let svg=build(p,f); let lit=null;
if(+A.litEdge>0){ const {litEdgeLayer}=require(path.join(__dirname,'litedge.js')); lit=litEdgeLayer(p,{opacity:+A.litEdge, axisDeg:f.axA==null?83.094:f.axA, idPrefix:f.id||'finalA5-'});
  const i=svg.indexOf('<g id="owl-slot"'); if(i<0) throw new Error('no owl-slot'); svg=svg.slice(0,i)+lit.layer+svg.slice(i);
  const j=svg.indexOf('</desc>'); svg=svg.slice(0,j)+lit.desc+svg.slice(j); }
fs.writeFileSync(A.out, svg); console.log(JSON.stringify({out:A.out,frame:A.frame,legendKeys:p.legendKeys||'none (uncut)',seamFix:p.seamFix||0,knobs:A.knobs||'finish/finish7-knobs.txt',litEdge:+A.litEdge||0,strips:lit?lit.pieces:0,levels:lit?lit.levels:0,samples:lit?lit.samples:0}));
