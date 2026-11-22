#!/usr/bin/env node
// meander3.js — Dose 01 medallion meander v3: the two interleaved lines drawn as FILLED CHANNEL OUTLINES (not stroked wire).
//   line B (outer) = outer gold rail + 24 U-hooks reaching inward  : drop at col 0, run clockwise along row A, stub up at col 2
//   line A (inner) = inner gold rail + 24 U-hooks reaching outward : rise at col 3, run counter-clockwise along row B, stub down at col 1
// Each line is ONE filled <path> (evenodd): a circle plus one closed contour that snakes around the 24 hooks, so the ribbon is a single
// connected shape with the original's body: tight convex corners (rc), concave fillets (rf) where members meet the rails and inside the U's,
// and rounded-square stub tips. Parameters in PRINT PX of the 1220 frame (centre 610); frame slot820 scales by 820/1220.
// The same builder with an `inset` emits the identical outline shrunk inward (for a rim / body / highlight finish that never leaves the footprint).
// Pure construction, deterministic, no source pixels.
'use strict';
const fs = require('fs');

const DEFAULTS = {
  N: 24, cols: 4,
  railIn: 464.75, railOut: 568.6,     // rail centre radii
  tRail: 14.0, t: 13.5,               // rail thickness, run thickness (radial)
  w: 17.0,                            // radial member width (px at the member's mid radius; constant angle along the member)
  rowA: 491.0, rowB: 542.75,          // run centre radii: A = outer line's run, B = inner line's run
  tipA: 523.6, tipB: 510.1,           // stub tip radii: outer line's stub reaches out to tipA; inner line's stub reaches in to tipB
  rc: 5.0, rf: 5.0,                   // convex corner radius, concave fillet radius (print px)
  rTip: null,                         // stub-tip corner radius; null = full semicircle (w/2)
  phaseDeg: 0.0,                      // 0 = key boundary channel at bottom vertical (+90°, y down)
  purpleIn: [434.06, 452.7], purpleOut: [584.9, 609.6],
  gold: '#D4A853', purple: '#8C4191', fieldFill: 'none',
  frame: 'slot820', inset: 0.0,       // inset > 0 shrinks the ribbon by that many px on every side (finish layers)
  filletMode: 'offset',
  idPrefix: '',
  legendKeys: [],                     // keys (0..N-1, key k spans 90+15k .. 90+15(k+1) deg) whose hooks are omitted for a legend channel
  seamFix: 0,                         // 1 = wrap-safe corner trimming at the contour's closing seam (2026-10-01). 0 reproduces the sealed rings byte for byte:
                                      // there the trim direction at the first and last vertex is taken from the raw angle difference, which has the wrong sign
                                      // across the 360-degree wrap, so those two corners per line (four per ring, at the legend window's ends) are filleted
                                      // backwards and bite into the gold. Carey spotted it on the printed coin, 2026-09-30.
};

function outline(p) {
  // returns { pathB, pathA } path data strings in the chosen frame
  const scale = p.frame === 'print1220' ? 1 : 820 / 1220;
  const size = p.frame === 'print1220' ? 1220 : 820;
  const c = size / 2;
  const n = x => (Math.round(x * 1000) / 1000).toFixed(3).replace(/\.?0+$/, '');
  const S = v => v * scale;
  const XY = (th, r) => { const a = th * Math.PI / 180; return [c + S(r) * Math.cos(a), c + S(r) * Math.sin(a)]; };
  const P = (th, r) => { const [x, y] = XY(th, r); return `${n(x)} ${n(y)}`; };
  const i = p.inset;
  const t = p.t - 2 * i, tRail = p.tRail - 2 * i, w = p.w - 2 * i;
  const rc = Math.max(0.3, p.rc - i), rf = p.filletMode === 'tight' ? Math.max(1.0, p.rf - i) : p.rf + i;   // 'offset' = true offset curve; 'tight' = keep fillets small so inset ribbons run into the rails as a T
  const rTip = Math.max(0.3, Math.min((p.rTip == null ? p.w / 2 : p.rTip) - i, w / 2 - 0.02));
  const pitch = 15 / p.cols;
  const col = (k, j) => 90 + p.phaseDeg + k * 15 + (j + 0.5) * pitch;
  const halfDeg = (wpx, rmid) => (wpx / rmid) * 180 / Math.PI / 2;

  // vertex lists: [theta, r, cornerRadius]; consecutive vertices differ in exactly one coordinate (radial line or tangential arc)
  const rri = p.railOut - tRail / 2;          // outer rail inner edge
  const rA0 = p.rowA - t / 2, rA1 = p.rowA + t / 2, tipA = p.tipA - i;
  const rro = p.railIn + tRail / 2;           // inner rail outer edge
  const rB0 = p.rowB - t / 2, rB1 = p.rowB + t / 2, tipB = p.tipB + i;
  const vB = [], vA = [];
  const skip = new Set(Array.isArray(p.legendKeys) ? p.legendKeys : (typeof p.legendKeys === 'string' && p.legendKeys.length ? p.legendKeys.split(',').map(Number) : []));
  for (let k = 0; k < p.N; k++) {
    if (skip.has(k)) continue;   // legend keys: no hooks, the rail runs straight through (exergue channel)
    const d = col(k, 0), u = col(k, 1), s = col(k, 2), v = col(k, 3);
    const hd = halfDeg(w, (rri + rA0) / 2), hs = halfDeg(w, (rA1 + tipA) / 2);
    const hu = halfDeg(w, (tipB + rB0) / 2), hv = halfDeg(w, (rro + rB1) / 2);
    vB.push([d - hd, rri, rf], [d - hd, rA0, rc], [s + hs, rA0, rc], [s + hs, tipA, rTip], [s - hs, tipA, rTip], [s - hs, rA1, rf], [d + hd, rA1, rf], [d + hd, rri, rf]);
    vA.push([v - hv, rro, rf], [v - hv, rB0, rf], [u + hu, rB0, rf], [u + hu, tipB, rTip], [u - hu, tipB, rTip], [u - hu, rB1, rc], [v + hv, rB1, rc], [v + hv, rro, rf]);
  }
  // emit a closed contour with rounded corners: trim each edge by the corner radius, join with a quadratic whose control is the sharp corner
  function contour(V) {
    const m = V.length; let d = '';
    const edgeIsRadial = (a, b) => Math.abs(a[0] - b[0]) < 1e-9;
    const trimPoint = (vtx, other, rho) => {        // point on the edge vtx->other at distance rho from vtx
      if (edgeIsRadial(vtx, other)) return [vtx[0], vtx[1] + Math.sign(other[1] - vtx[1]) * rho];
      const dth = (rho / vtx[1]) * 180 / Math.PI; const dir = p.seamFix ? Math.sign(norm(other[0] - vtx[0])) : Math.sign(other[0] - vtx[0]); return [vtx[0] + dir * dth, vtx[1]];
    };
    const norm = a => ((a + 180) % 360 + 360) % 360 - 180;     // wrap an angle difference into (-180, 180]
    const segTo = (from, to) => {
      if (edgeIsRadial(from, to)) return Math.abs(to[1] - from[1]) < 1e-6 ? '' : `L${P(to[0], to[1])}`;
      const dth = norm(to[0] - from[0]); if (Math.abs(dth) < 1e-6) return '';
      return `A${n(S(to[1]))} ${n(S(to[1]))} 0 ${Math.abs(dth) > 180 ? 1 : 0} ${dth > 0 ? 1 : 0} ${P(to[0], to[1])}`;
    };
    const cornerArc = (pin, vtx, pout, rho) => {     // circular arc of radius rho from pin to pout, turning at vtx
      const a = XY(pin[0], pin[1]), b = XY(vtx[0], vtx[1]), c2 = XY(pout[0], pout[1]);
      const cross = (b[0] - a[0]) * (c2[1] - b[1]) - (b[1] - a[1]) * (c2[0] - b[0]);   // y-down: positive = clockwise turn on screen
      return `A${n(S(rho))} ${n(S(rho))} 0 0 ${cross > 0 ? 1 : 0} ${P(pout[0], pout[1])}`;
    };
    let prevOut = null, first = null;
    for (let j = 0; j < m; j++) {
      const vtx = V[j], prev = V[(j - 1 + m) % m], next = V[(j + 1) % m], rho = vtx[2];
      const pin = trimPoint(vtx, prev, rho), pout = trimPoint(vtx, next, rho);
      if (j === 0) { d += `M${P(pout[0], pout[1])}`; first = pout; }
      else { d += ` ${segTo(prevOut, pin)} ${cornerArc(pin, vtx, pout, rho)}`; }
      prevOut = pout;
    }
    const v0 = V[0], pin0 = trimPoint(v0, V[m - 1], v0[2]);
    d += ` ${segTo(prevOut, pin0)} ${cornerArc(pin0, v0, first, v0[2])} Z`;
    return d.replace(/\s+/g, ' ');
  }
  const circle = r => `M${P(0, r)} A${n(S(r))} ${n(S(r))} 0 0 1 ${P(180, r)} A${n(S(r))} ${n(S(r))} 0 0 1 ${P(360, r)} Z`;
  const pathB = circle(p.railOut + tRail / 2) + ' ' + contour(vB);      // outer boundary circle + inner snaking contour
  const pathA = contour(vA) + ' ' + circle(p.railIn - tRail / 2);       // outer snaking contour + inner boundary circle
  return { pathB, pathA, size, c, n, S };
}

function build(p) {
  p = Object.assign({}, DEFAULTS, p || {});
  const { pathB, pathA, size, c, n, S } = outline(p);
  const ring = (r0, r1) => `<circle cx="${n(c)}" cy="${n(c)}" r="${n(S((r0 + r1) / 2))}" fill="none" stroke="${p.purple}" stroke-width="${n(S(r1 - r0))}"/>`;
  const field = p.fieldFill === 'none' ? '' : `<circle id="${p.idPrefix}field" cx="${n(c)}" cy="${n(c)}" r="${n(S(p.purpleIn[0]))}" fill="${p.fieldFill}"/>`;
  const desc = `Dose 01 medallion meander v3: two interleaved continuous lines as filled channel outlines (outer rail + ${p.N} inward U-hooks; inner rail + ${p.N} outward U-hooks). Print px: rails ${p.railIn}/${p.railOut} t ${p.tRail}, rows ${p.rowA}/${p.rowB} t ${p.t}, member w ${p.w}, tips ${p.tipA}/${p.tipB}, corners rc ${p.rc} rf ${p.rf} tip ${p.rTip == null ? 'semicircle' : p.rTip}, ${p.cols} members per key on a ${15 / p.cols}° pitch, phase ${p.phaseDeg}°, inset ${p.inset}. Frame ${p.frame}. Classical construction; no source pixels.`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
<title>Dose 01 medallion — meander v3 (two interleaved lines, channel outline), ${p.frame}</title>
<desc>${desc}</desc>
<g id="${p.idPrefix}rings">${field}${ring(p.purpleIn[0], p.purpleIn[1])}${ring(p.purpleOut[0], p.purpleOut[1])}</g>
<g id="${p.idPrefix}geometry">
<path id="${p.idPrefix}line-outer" d="${pathB}" fill="${p.gold}" fill-rule="evenodd"/>
<path id="${p.idPrefix}line-inner" d="${pathA}" fill="${p.gold}" fill-rule="evenodd"/>
</g>
<g id="${p.idPrefix}finish"/>
<g id="${p.idPrefix}owl-slot"/>
</svg>
`;
  return { svg, params: p, paths: { pathB, pathA } };
}

if (require.main === module) {
  const args = process.argv.slice(2); const p = {}; let out = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--params') Object.assign(p, JSON.parse(fs.readFileSync(args[++i], 'utf8')));
    else if (a === '--out') out = args[++i];
    else if (a.startsWith('--')) { const k = a.slice(2); const v = args[++i]; p[k] = (v === 'null') ? null : (isNaN(v) ? (v[0] === '{' || v[0] === '[' ? JSON.parse(v) : v) : parseFloat(v)); }
  }
  const { svg, params } = build(p);
  if (out) { fs.writeFileSync(out, svg); fs.writeFileSync(out.replace(/\.svg$/, '') + '.params.json', JSON.stringify(params, null, 1)); console.log(JSON.stringify({ out, bytes: svg.length, frame: params.frame, t: params.t, w: params.w, rc: params.rc, rf: params.rf, inset: params.inset })); }
  else process.stdout.write(svg);
}
module.exports = { build, outline, DEFAULTS };
