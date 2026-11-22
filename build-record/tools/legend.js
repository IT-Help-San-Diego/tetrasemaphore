// legend.js <in-master.svg> <out-master.svg> [--cap 4.4] [--a0 45 --a1 135] [--plaque #16120C] [--track 1.10] [--rim 0.6 --trans 0.8 --ridge 1.4 --centreOp 0.10 --blur 0.15] [--shadow 4 --shadowOp 0.6 --lip 1 --lipOp 0.2 --lightDeg 240]
const fs=require('fs'); const M='/private/tmp/claude-501/-Users-careybalboa-Downloads/f53c0528-5366-4b21-a083-f42921c4609f/scratchpad/meander/node_modules';
const opentype=require(M+'/opentype.js'); const FONT='/Users/careybalboa/Downloads/dose-01-FOR-CLAUDE-CODE/05-DejaVuSans-Bold.ttf';
const [,,inp,out,...rest]=process.argv; const P={cap:4.4,a0:45,a1:135,plaque:'#16120C',track:1.10,rim:0.6,rimHex:'#332A11',rimOp:1.0,trans:0.8,transOp:0.3,ridge:1.4,ridgeHex:'#FFF9E3',ridgeOp:0.6,centreOp:0.10,blur:0.15,shadow:4,shadowOp:0.6,lip:1,lipOp:0.2,lightDeg:240,word:'METACOGNITIVE',fill:'#DEC875',corner:1.4,ao:5,aoOp:0.30,textShadow:1.2,textShadowOp:0.6,textShadowBlur:1.0};
for(let i=0;i<rest.length;i+=2){const k=rest[i].slice(2), v=rest[i+1]; P[k]=isNaN(v)?v:parseFloat(v);}
const K=820/1220, c=410, MMPX=0.0847;                      // slot px per print px; mm per print px
const railIn=464.75, railOut=568.6, tRail=14.0;            // sealed geometry (print px)
const rIn=(railIn+tRail/2)*K, rOut=(railOut-tRail/2)*K, rMid=(rIn+rOut)/2, OVER=1.0;   // plaque edges = rail inner faces; OVER = overlap tucked under the rails
const n=x=>(Math.round(x*1000)/1000).toString(); const rad=d=>d*Math.PI/180; const XY=(d,r)=>[c+r*Math.cos(rad(d)), c+r*Math.sin(rad(d))];
const arcPath=(r0,r1,a0,a1)=>{const [x0,y0]=XY(a0,r0),[x1,y1]=XY(a1,r0),[x2,y2]=XY(a1,r1),[x3,y3]=XY(a0,r1); return `M${n(x0)} ${n(y0)} A${n(r0)} ${n(r0)} 0 0 1 ${n(x1)} ${n(y1)} L${n(x2)} ${n(y2)} A${n(r1)} ${n(r1)} 0 0 0 ${n(x3)} ${n(y3)} Z`;};
const rho=P.corner/MMPX*K;   // fillet radius, slot px
function filletSector(r0,r1,a0,a1,rho){
  // corners in traversal order: inner arc a0->a1 (increasing angle), radial out at a1, outer arc a1->a0, radial in at a0
  const C=[[a0,r0],[a1,r0],[a1,r1],[a0,r1]];
  const trim=(v,o)=>{ if(Math.abs(v[0]-o[0])<1e-9) return [v[0], v[1]+Math.sign(o[1]-v[1])*rho]; const d=rho/v[1]*180/Math.PI; return [v[0]+Math.sign(o[0]-v[0])*d, v[1]]; };
  const cross=(a,b,c)=>(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);
  const seg=(f,t)=>{ if(Math.abs(f[0]-t[0])<1e-9){const [x,y]=XY(t[0],t[1]); return `L${n(x)} ${n(y)}`;} const [x,y]=XY(t[0],t[1]); return `A${n(t[1])} ${n(t[1])} 0 0 ${t[0]>f[0]?1:0} ${n(x)} ${n(y)}`; };
  let d=''; let prevOut=null, first=null;
  for(let j=0;j<4;j++){ const v=C[j], pv=C[(j+3)%4], nx=C[(j+1)%4]; const pin=trim(v,pv), pout=trim(v,nx);
    const A=XY(pin[0],pin[1]), Bv=XY(v[0],v[1]), Cc=XY(pout[0],pout[1]); const sw=cross(A,Bv,Cc)>0?1:0;
    if(j===0){ d+=`M${n(Cc[0])} ${n(Cc[1])}`; first=pout; } else { d+=` ${seg(prevOut,pin)} A${n(rho)} ${n(rho)} 0 0 ${sw} ${n(Cc[0])} ${n(Cc[1])}`; }
    prevOut=pout; }
  const v0=C[0], pin0=trim(v0,C[3]); const A=XY(pin0[0],pin0[1]), Bv=XY(v0[0],v0[1]), Cc=XY(first[0],first[1]); const sw=cross(A,Bv,Cc)>0?1:0;
  d+=` ${seg(prevOut,pin0)} A${n(rho)} ${n(rho)} 0 0 ${sw} ${n(Cc[0])} ${n(Cc[1])} Z`; return d; }
const plaqueExact=filletSector(rIn,rOut,P.a0,P.a1,rho), plaque=plaqueExact;
const dIn=rho/rIn*180/Math.PI, dOut=rho/rOut*180/Math.PI;
const seams=arcPath(rIn-OVER,rIn+OVER,P.a0+dIn,P.a1-dIn)+' '+arcPath(rOut-OVER,rOut+OVER,P.a0+dOut,P.a1-dOut);   // hidden under the rails: kills the anti-alias seam at the rail faces
// light direction for the recess: shadow on the walls nearest the light, lip on the far walls
const L=[Math.cos(rad(P.lightDeg)),Math.sin(rad(P.lightDeg))]; const g0=XY(P.lightDeg, rMid), g1=XY(P.lightDeg+180, rMid);
const buf=fs.readFileSync(FONT); const font=opentype.parse(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength));
const capPx=P.cap/MMPX*K, fs_=capPx/0.730; const advs=[...P.word].map(ch=>font.getAdvanceWidth(ch,fs_)); const total=advs.reduce((a,b)=>a+b*P.track,0);
let th=rad(90)+total/2/rMid; const glyphs=[];
[...P.word].forEach((ch,i)=>{const a=advs[i]*P.track; const tc=th-a/2/rMid; const [x,y]=[c+rMid*Math.cos(tc), c+rMid*Math.sin(tc)]; const d=font.getPath(ch,-advs[i]/2,capPx/2,fs_).toPathData(3); glyphs.push({ch,d,tr:`translate(${n(x)} ${n(y)}) rotate(${n(tc*180/Math.PI-90)})`}); th-=a/rMid;});
const spanDeg=total/rMid*180/Math.PI;
const paths=glyphs.map(g=>`<path transform="${g.tr}" d="${g.d}"/>`).join('');
const clipPaths=glyphs.map(g=>`<path transform="${g.tr}" d="${g.d}"/>`).join('');
const NS='xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"';
const bar=`<g id="legend-plaque" inkscape:groupmode="layer" inkscape:label="5a legend plaque: inlaid channel, keys 21-2 (${P.a0}-${P.a1} deg), rails continue">
<defs><clipPath id="legend-plaque-clip" clipPathUnits="userSpaceOnUse"><path d="${plaque}"/></clipPath>
<linearGradient id="legend-shadow-grad" gradientUnits="userSpaceOnUse" x1="${n(g0[0])}" y1="${n(g0[1])}" x2="${n(g1[0])}" y2="${n(g1[1])}"><stop offset="0" stop-color="#000" stop-opacity="${P.shadowOp}"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="legend-lip-grad" gradientUnits="userSpaceOnUse" x1="${n(g1[0])}" y1="${n(g1[1])}" x2="${n(g0[0])}" y2="${n(g0[1])}"><stop offset="0" stop-color="${P.ridgeHex}" stop-opacity="${P.lipOp}"/><stop offset="1" stop-color="${P.ridgeHex}" stop-opacity="0"/></linearGradient>
<filter id="legend-shadow-blur" filterUnits="userSpaceOnUse" x="0" y="0" width="820" height="820"><feGaussianBlur stdDeviation="${n(P.shadow/2)}"/></filter>
<filter id="legend-lip-blur" filterUnits="userSpaceOnUse" x="0" y="0" width="820" height="820"><feGaussianBlur stdDeviation="${n(P.lip*0.6)}"/></filter>
<filter id="legend-ao-blur" filterUnits="userSpaceOnUse" x="0" y="0" width="820" height="820"><feGaussianBlur stdDeviation="${n(P.ao/2)}"/></filter>
<filter id="legend-textshadow-blur" filterUnits="userSpaceOnUse" x="0" y="0" width="820" height="820"><feGaussianBlur stdDeviation="${n(P.textShadowBlur)}"/></filter></defs>
<path id="legend-plaque-seams" d="${seams}" fill="${P.plaque}"/>
<path id="legend-plaque-fill" d="${plaque}" fill="${P.plaque}"/>
<g clip-path="url(#legend-plaque-clip)"><path d="${plaqueExact}" fill="none" stroke="#000" stroke-opacity="${P.aoOp}" stroke-width="${n(2*P.ao)}" filter="url(#legend-ao-blur)"/><path d="${plaqueExact}" fill="none" stroke="url(#legend-shadow-grad)" stroke-width="${n(2*P.shadow)}" filter="url(#legend-shadow-blur)"/><path d="${plaqueExact}" fill="none" stroke="url(#legend-lip-grad)" stroke-width="${n(2*P.lip)}" filter="url(#legend-lip-blur)"/></g>
</g>
`;
const text=`<g id="legend-text" inkscape:groupmode="layer" inkscape:label="5b legend ${P.word}: champagne ${P.fill}, cap ${P.cap} mm at the channel mid-radius, ring bevel recipe">
<defs><clipPath id="legend-text-clip" clipPathUnits="userSpaceOnUse">${clipPaths}</clipPath><filter id="legend-text-blur" filterUnits="userSpaceOnUse" x="0" y="0" width="820" height="820"><feGaussianBlur stdDeviation="${n(P.blur)}"/></filter></defs>
<g id="legend-cast-shadow" clip-path="url(#legend-plaque-clip)"><g transform="translate(${n(P.textShadow*Math.cos(rad(P.lightDeg+180)))} ${n(P.textShadow*Math.sin(rad(P.lightDeg+180)))})" fill="#000" fill-opacity="${P.textShadowOp}" filter="url(#legend-textshadow-blur)">${paths}</g></g>
<g id="legend-glyphs" fill="${P.fill}">${paths}</g>
<g id="legend-bevel" clip-path="url(#legend-text-clip)"><g filter="url(#legend-text-blur)" fill="none" stroke-linejoin="round" stroke-linecap="round">
<g fill="#000" fill-opacity="${P.centreOp}" stroke="none">${paths}</g>
<g stroke="${P.ridgeHex}" stroke-opacity="${P.ridgeOp}" stroke-width="${n(2*P.ridge)}">${paths}</g>
<g stroke="${P.rimHex}" stroke-opacity="${P.transOp}" stroke-width="${n(2*P.trans)}">${paths}</g>
<g stroke="${P.rimHex}" stroke-opacity="${P.rimOp}" stroke-width="${n(2*P.rim)}">${paths}</g>
</g></g>
</g>
`;
let svg=fs.readFileSync(inp,'utf8'); if(!svg.includes(NS)) svg=svg.replace('<svg ','<svg '+NS+' ');
const gm=svg.match(/<g id="[^"]*geometry"[^>]*>/) || svg.match(/<g id="[^"]*"[^>]*inkscape:label="2 meander[^"]*"[^>]*>/); if(!gm) throw new Error('no geometry group'); const gi=gm.index; svg=svg.slice(0,gi)+bar+svg.slice(gi);
const starts=['<defs><mask id="pupils"','<g id="owl-pupils-open"','<g id="owl-placement"','<g id="owl" '].map(s=>svg.indexOf(s)).filter(k=>k>=0); const oi=Math.min(...starts); svg=svg.slice(0,oi)+text+svg.slice(oi);
fs.writeFileSync(out,svg);
console.log(JSON.stringify({corner_mm:P.corner,ao_px:P.ao,textShadow_px:P.textShadow,cap_mm:P.cap,cap_slot_px:+n(capPx),fontSize_slot:+n(fs_),rIn:+n(rIn),rOut:+n(rOut),rMid:+n(rMid),channel_mm:+n((rOut-rIn)/K*MMPX),word_span_deg:+n(spanDeg),margin_each_deg:+n((P.a1-P.a0-spanDeg)/2),margin_each_mm:+n((P.a1-P.a0-spanDeg)/2*Math.PI/180*rMid/K*MMPX),clearance_to_rails_mm:+n(((rOut-rIn)-capPx)/2/K*MMPX),stem_mm:+n(P.cap*0.25)}));
