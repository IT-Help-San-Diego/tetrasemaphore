#!/usr/bin/env node
// finish6.js — finish5.js (the APPROVED meander finish, verbatim) + three OPTIONAL "shine" knobs that all default OFF.
// With no shine flags the SVG is byte-identical to finish5.js's output (verified: cmp against S/gen3/out/fa/v4d.svg).
// Built by the verifier/integrator from three independently developed knobs (S/shine/ridge-shine, S/shine/glints, S/shine/fresnel-edge).
//
//   --glints 1            KEPT (delivered). Catch-lights: a separate layer of thresholded fractalNoise (glintFreq 0.05/print px, glintOct 4,
//                         glintSeed 41, threshold glintThresh 0.85 on 0.9G+0.6B with gain glintGain 30) in glintColor #FDF3D3 at glintOp 0.68,
//                         masked to the ridge band (insets transInset+glintInner .. ridgeInset+glintOuter = 2.6..4.6 px) AND to the lit lobes
//                         (glintLobe 'wedge' = sectors glintSectors '30-90,240-300' softened by feGaussianBlur glintSoft 8 px; 'cos' = gradient
//                         along glintAx where cos(2(θ-ax)) > glintCos fading over glintFade; 'both' = wedge x cos), clipped to the footprint.
//                         Layer id finalA5-glints sits between the geometry layer and the finish bands. Scale with --glintOp (0.68 = delivered).
//   --ridgeShine X        DROPPED (kept selectable, default 0). Smooth light (#FFF3CF, ridgeShineColor) over the ridge band whose opacity follows
//                         max(cos(H(θ-axis)),0)^ridgeShineP, H = ridgeShineHarm 2 (axis default axA) or 4; layer finalA5-ridgeShineLayer on top
//                         of the bands. Does not move the highlight tail (p99/>90/blobs unchanged) and spends the 24-sector budget the glints need.
//   --edgeLight X         DROPPED (kept selectable, default 0). Fresnel edge: rim+transition darkening x (1 - edgeLight*max(cos2(θ-edgeAx),0)) via
//                         black gradient fills (edgeBands 'rt'); --edgeCatch X adds a pale hairline 0..edgeCatchWidth px at the outline (lit lobes).
//                         Measured against the original the lit edge is already lighter than the target; edgeCatch breaks the footprint gate.
//
// Below this line: finish5.js verbatim except the marked KNOB insertions and the absolute require path.
// finish5.js — final-A recipe with RELATIVE tonal bands: the body (with sector sweeps and grain) fills the whole footprint, and the rim /
// transition / centre are proportional darkenings of the local tone (black at partial opacity on band shapes), so dark sectors darken
// as one piece of metal instead of showing a fixed outline. Derived from finish4.js (the ported panel recipe).
// Every layer is the same outline at an inset (never a re-stroke), so the ink footprint is the geometry's by construction.
// Layers, bottom to top, inside the footprint: rim (#55421F, full outline) > transition (inset 0.9, #8A7550) >
// [body group, grain-filtered]: body (inset 2.2, #BEA571) > chased ridge (inset 2.2, #E4D8B6 @0.42) > core (inset 3.6, #BEA571)
// > struck centre (centreline ribbon, #A08858 @0.6) > sector sweeps A (2nd harmonic) and B (fundamental) through the body mask
// > per-channel cap at #F2E4B8 > feComposite in SourceAlpha. Pure vector, deterministic, ids prefixed finalA3-.
// finish7.js — finish6 + organic-band knobs (bandBlur, bandWarp, warpFreq/Oct/Seed, rimStroke, glintMaskBlur); all default OFF = byte-identical to finish6.
// usage: node finish7.js --frame slot820|print1220 [--phaseDeg X] [--rc 6.5 --rf 6] [--out file.svg] [--<recipe key> value] [--glints 1 ...]
'use strict';
const fs = require('fs');
const { outline, DEFAULTS } = require(__dirname + '/meander3.js');
const P = {
  rimInset: 0.9, rimOp: 0.60, transInset: 2.2, transOp: 0.20, ridgeInset: 4.6, ridgeOp: 0.0, centreOp: 0.13,   // relative bands: black at these opacities over the local tone (r4 calibration)
  body: '#B29F7B', bodyInset: 0.0,   // Lab(66.3, 1.42, 21.4): luminance from the sector fit, hue from the hue fit
  axA: 83.094, creamA: '#F0E3C9', opA: 0.814, amberA: '#6C5324', opAd: 0.477, lobeBright: 1, lobeDark: 1,   // sector-light fit wf_44fad277-b27 (2nd harmonic of the original's 24-sector L*)
  axB: 307.5, creamB: '#EBDFC8', opB: 0.0, amberB: '#6E5321', opBd: 0.452, R: 522,   // fundamental: only its amber lobe is needed (105–180° trough)
  grainFreq: 0.09, grainOct: 3, grainSeed: 17, grainLight: '#EEDFB4', grainLightGain: 0.7, grainLightBase: 0.05,
  grainDark: '#6E5532', grainDarkGain: 0.55, grainDarkBase: 0.12, slowFreq: 0.003, slowOct: 2, slowSeed: 5, slowAmp: 0.10, cap: '#F2E4B8',
  zoneFreq: 0.012, zoneOct: 2, zoneSeed: 23, zoneLo: 0.70, zoneHi: 0.82,   // unvarnished zones: mottle only where the slow zone field is high
  fleckThresh: 0.98, fleckGain: 25, fleckColor: '#F2E4B8', fleckOp: 0.22,  // sparse hard specular flecks (dings): top ~2 % of the noise field
  bodyBlur: 0.0,            // softens the ridge / centre bands into gradients across the stroke (print px); stays inside the footprint (body is inset 2.2)
  purple: '#8C4191', id: 'finalA5-',
  // ---- KNOB glints (finish6; default OFF) ----
  glints: 0, glintFreq: 0.05, glintOct: 4, glintSeed: 41, glintThresh: 0.85, glintGain: 30, glintColor: '#FDF3D3', glintOp: 0.68,
  glintAx: 83.094, glintCos: 0.3, glintFade: 0.25, glintInner: 0.4, glintOuter: 0, glintLobe: 'wedge', glintSectors: '30-90,240-300', glintSoft: 8,
  // ---- KNOB ridgeShine (finish6; default OFF) ----
  ridgeShine: 0, ridgeShineP: 1.5, ridgeShineColor: '#FFF3CF', ridgeShineAxis: null, ridgeShineHarm: 2,
  // ---- KNOB fresnel edge (finish6; default OFF) ----
  edgeLight: 0, edgeAx: null, edgeBands: 'rt', edgeCatch: 0, edgeCatchWidth: 0.6, edgeCatchColor: '#F2E4B8',
  // ---- KNOB organic bands (finish7; default OFF): the relative bands are warped by low-frequency noise and blurred, so no tone step
  //      follows the outline at a constant depth (Carey 2026-09-15: "little lines / right angles where it gets bright") ----
  bandBlur: 0, bandWarp: 0, warpFreq: 0.02, warpOct: 2, warpSeed: 7, rimStroke: 0, glintMaskBlur: 0, glintBlur: 0, bandMaskInset: 0, glintFull: 0,
  bandHex: '#000',   // colour of the relative-band overlays (Hermes GOLD-RENDERING-RECIPE: warm dark brown #332A11, never neutral)   // 1: glint mask = everything inside inset transInset+glintInner (no inner inset: an inset beyond the half-width folds the contour and renders differently across renderers)   // >0: the band group is masked by the outline inset this far (AA-safe: the ink footprint's edge alpha stays the geometry's) instead of clipped at the outline
};
function build(g, f) {
  g = Object.assign({}, DEFAULTS, g || {}); f = Object.assign({}, P, f || {});
  const size = g.frame === 'print1220' ? 1220 : 820, W = size, H = size, k = W / 1220, c = size / 2;
  const n = x => (Math.round(x * 1000) / 1000).toFixed(3).replace(/\.?0+$/, '');
  const S = v => v * k;
  const O = inset => outline(Object.assign({}, g, { inset, filletMode: inset > 0 ? 'tight' : 'offset' }));
  const two = (o, attrs) => `<path d="${o.pathB}" ${attrs}/><path d="${o.pathA}" ${attrs}/>`;
  const N = f.id;
  const rad = d => d * Math.PI / 180;
  const axisPts = deg => { const R = S(f.R); return { x1: n(c + R * Math.cos(rad(deg))), y1: n(c + R * Math.sin(rad(deg))), x2: n(c - R * Math.cos(rad(deg))), y2: n(c - R * Math.sin(rad(deg))) }; };
  const A = axisPts(f.axA), B = axisPts(f.axB);
  const ts = [-1, -0.95, -0.9, -0.85, -0.8, -0.75, -0.7071, -0.6, -0.45, -0.3, 0, 0.3, 0.45, 0.6, 0.7071, 0.75, 0.8, 0.85, 0.9, 0.95, 1];
  const pB = f.lobeBright == null ? 1 : f.lobeBright, pD = f.lobeDark == null ? 1 : f.lobeDark;
  // KNOB fresnel edge (default off)
  const edgeOn = f.edgeLight > 0, catchOn = f.edgeCatch > 0, litT = t => Math.max(2 * t * t - 1, 0);
  const E = axisPts(f.edgeAx == null ? f.axA : f.edgeAx);
  const edgeGrad = (id, color, opOf) => `<linearGradient id="${N}${id}" gradientUnits="userSpaceOnUse" x1="${E.x1}" y1="${E.y1}" x2="${E.x2}" y2="${E.y2}">${ts.map(t => `<stop offset="${((t + 1) / 2).toFixed(4)}" stop-color="${color}" stop-opacity="${opOf(t).toFixed(4)}"/>`).join('')}</linearGradient>`;
  const edgeDefs = (edgeOn ? edgeGrad('edgeRim', '#000', t => f.rimOp * (1 - (f.edgeBands.includes('r') ? f.edgeLight : 0) * litT(t))) + edgeGrad('edgeTrans', '#000', t => f.transOp * (1 - (f.edgeBands.includes('t') ? f.edgeLight : 0) * litT(t))) : '') + (catchOn ? edgeGrad('edgeCatch', f.edgeCatchColor, t => f.edgeCatch * litT(t)) : '');
  const rimFill = edgeOn ? `fill="url(#${N}edgeRim)"` : `fill-opacity="${f.rimOp}"`, transFill = edgeOn ? `fill="url(#${N}edgeTrans)"` : `fill-opacity="${f.transOp}"`;
  const edgeDesc = (edgeOn || catchOn) ? ` Fresnel edge (finish6): bands ${f.edgeBands} opacity x(1-${f.edgeLight}*max(cos2(theta-${f.edgeAx == null ? f.axA : f.edgeAx}),0))${catchOn ? `; catch-light 0-${f.edgeCatchWidth} px ${f.edgeCatchColor} @${f.edgeCatch}*max(cos2,0)` : ''}.` : '';
  const stopsA = ts.map(t => { const s = 2 * t * t - 1, off = ((t + 1) / 2).toFixed(4); return s >= 0 ? `<stop offset="${off}" stop-color="${f.creamA}" stop-opacity="${(f.opA * Math.pow(s, pB)).toFixed(3)}"/>` : `<stop offset="${off}" stop-color="${f.amberA}" stop-opacity="${(f.opAd * Math.pow(-s, pD)).toFixed(3)}"/>`; }).join('');
  const stopsB = `<stop offset="0" stop-color="${f.creamB}" stop-opacity="${f.opB}"/><stop offset="0.5" stop-color="${f.creamB}" stop-opacity="0"/><stop offset="0.5" stop-color="${f.amberB}" stop-opacity="0"/><stop offset="1" stop-color="${f.amberB}" stop-opacity="${f.opBd}"/>`;
  const h2 = hex => [1, 3, 5].map(i => (parseInt(hex.slice(i, i + 2), 16) / 255).toFixed(4));
  const gL = f.grainLightGain, gD = f.grainDarkGain, [lr, lg, lb] = h2(f.grainLight), [dr, dg, db] = h2(f.grainDark), [fr, fg, fb] = h2(f.fleckColor);
  const capRGB = [1, 3, 5].map(i => parseInt(f.cap.slice(i, i + 2), 16) / 255);
  const tbl = cc => Array.from({ length: 41 }, (_, i) => Math.min(i / 40, cc).toFixed(4)).join(' ');
  const filt = `<filter id="${N}grain" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}" color-interpolation-filters="sRGB">
<feGaussianBlur in="SourceGraphic" stdDeviation="${(f.bodyBlur * k).toFixed(3)}" result="sg"/>
<feTurbulence type="fractalNoise" baseFrequency="${(f.grainFreq / k).toFixed(5)}" numOctaves="${f.grainOct}" seed="${f.grainSeed}" stitchTiles="noStitch" result="n0"/>
<feColorMatrix in="n0" type="matrix" values="0 0 0 0 ${lr}  0 0 0 0 ${lg}  0 0 0 0 ${lb}  0 ${(0.9 * gL).toFixed(3)} ${(0.6 * gL).toFixed(3)} 0 ${(-0.75 * gL + f.grainLightBase).toFixed(3)}" result="light"/>
<feColorMatrix in="n0" type="matrix" values="0 0 0 0 ${dr}  0 0 0 0 ${dg}  0 0 0 0 ${db}  0 ${(-0.9 * gD).toFixed(3)} ${(-0.6 * gD).toFixed(3)} 0 ${(0.75 * gD + f.grainDarkBase).toFixed(3)}" result="dark"/>
<feTurbulence type="fractalNoise" baseFrequency="${(f.zoneFreq / k).toFixed(5)}" numOctaves="${f.zoneOct}" seed="${f.zoneSeed}" stitchTiles="noStitch" result="z0"/>
<feColorMatrix in="z0" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0.9 0.6 0 0" result="zA"/>
<feComponentTransfer in="zA" result="gate"><feFuncA type="table" tableValues="${Array.from({ length: 21 }, (_, i) => Math.min(1, Math.max(0, (i / 20 - f.zoneLo) / (f.zoneHi - f.zoneLo))).toFixed(3)).join(' ')}"/></feComponentTransfer>
<feComposite in="light" in2="gate" operator="in" result="lightZ"/><feComposite in="dark" in2="gate" operator="in" result="darkZ"/>
<feColorMatrix in="n0" type="matrix" values="0 0 0 0 ${fr}  0 0 0 0 ${fg}  0 0 0 0 ${fb}  0 ${(0.9 * f.fleckGain).toFixed(3)} ${(0.6 * f.fleckGain).toFixed(3)} 0 ${(-f.fleckThresh * f.fleckGain).toFixed(3)}" result="fleck0"/>
<feComponentTransfer in="fleck0" result="fleck"><feFuncA type="linear" slope="${f.fleckOp}"/></feComponentTransfer>
<feComposite in="darkZ" in2="sg" operator="atop" result="m1a"/><feComposite in="lightZ" in2="m1a" operator="atop" result="m1b"/><feComposite in="fleck" in2="m1b" operator="atop" result="m1"/>
<feTurbulence type="fractalNoise" baseFrequency="${(f.slowFreq / k).toFixed(6)}" numOctaves="${f.slowOct}" seed="${f.slowSeed}" stitchTiles="noStitch" result="s0"/>
<feColorMatrix in="s0" type="matrix" values="0 0.5 0.5 0 0  0 0.5 0.5 0 0  0 0.5 0.5 0 0  0 0 0 0 1" result="v"/>
<feComposite in="m1" in2="v" operator="arithmetic" k1="${f.slowAmp.toFixed(3)}" k2="${(1 - f.slowAmp / 2).toFixed(3)}" k3="0" k4="0" result="m2"/>
<feComponentTransfer in="m2" result="m3"><feFuncR type="table" tableValues="${tbl(capRGB[0])}"/><feFuncG type="table" tableValues="${tbl(capRGB[1])}"/><feFuncB type="table" tableValues="${tbl(capRGB[2])}"/></feComponentTransfer>
<feComposite in="m3" in2="sg" operator="atop"/></filter>`;
  const geom = O(0), o1 = O(f.rimInset), o2 = O(f.transInset), o3 = O(f.ridgeInset);
  // KNOB organic bands (finish7; default off): displacement by fractalNoise then Gaussian blur, applied to the band group BEFORE its clip
  const bandOn = f.bandBlur > 0 || f.bandWarp > 0;
  const bandDefs = bandOn ? `
<filter id="${N}bandF" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="${(f.warpFreq / k).toFixed(5)}" numOctaves="${f.warpOct}" seed="${f.warpSeed}" stitchTiles="noStitch" result="w0"/>
<feDisplacementMap in="SourceGraphic" in2="w0" scale="${(f.bandWarp * k).toFixed(3)}" xChannelSelector="R" yChannelSelector="G" result="w1"/>
<feGaussianBlur in="w1" stdDeviation="${(f.bandBlur * k).toFixed(3)}"/></filter>` : '';
  const bandOpen = bandOn ? `<g filter="url(#${N}bandF)">` : '', bandClose = bandOn ? '</g>' : '';
  const bandMaskDef = f.bandMaskInset > 0 ? `\n<mask id="${N}bandMask" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">${two(O(f.bandMaskInset), 'fill="#fff" fill-rule="evenodd"')}</mask>` : '';
  const bandDesc = bandOn ? ` Organic bands (finish7): band group displaced by fractalNoise (${f.warpFreq}/print px, ${f.warpOct} oct, seed ${f.warpSeed}) scale ${f.bandWarp} px and blurred σ ${f.bandBlur} px before the footprint clip${f.rimStroke > 0 ? `; rim as a ${f.rimStroke} px stroke of the outline (half outside, clipped)` : ''}.` : '';
  const bandTwo = (oa, ob, attrs) => `<path d="${oa.pathB} ${ob.pathB}" ${attrs}/><path d="${oa.pathA} ${ob.pathA}" ${attrs}/>`;   // evenodd: region between two insets
  const ring = (r0, r1) => `<circle cx="${n(c)}" cy="${n(c)}" r="${n(S((r0 + r1) / 2))}" fill="none" stroke="${f.purple}" stroke-width="${n(S(r1 - r0))}"/>`;
  // KNOB glints (default off)
  let glintDefs = '', glintLayer = '', glintDesc = '';
  if (f.glints) {
    const [qr, qg, qb] = h2(f.glintColor), GA = axisPts(f.glintAx);
    const lobe = ts.map(t => { const s2 = 2 * t * t - 1, off = ((t + 1) / 2).toFixed(4); const v = Math.min(1, Math.max(0, (s2 - (f.glintCos - f.glintFade)) / (2 * f.glintFade))); const hex = Math.round(v * 255).toString(16).padStart(2, '0'); return `<stop offset="${off}" stop-color="#${hex}${hex}${hex}"/>`; }).join('');
    const oi = O(f.transInset + f.glintInner), oo = O(f.ridgeInset + f.glintOuter);
    const RW = S(720), wedgePath = String(f.glintSectors).split(',').map(seg => { const [a0, a1] = seg.split('-').map(Number); const p0 = [c + RW * Math.cos(rad(a0)), c + RW * Math.sin(rad(a0))], p1 = [c + RW * Math.cos(rad(a1)), c + RW * Math.sin(rad(a1))]; return `M${n(c)},${n(c)} L${n(p0[0])},${n(p0[1])} A${n(RW)},${n(RW)} 0 ${a1 - a0 > 180 ? 1 : 0},1 ${n(p1[0])},${n(p1[1])} Z`; }).join(' ');
    const cosRect = `<rect x="0" y="0" width="${W}" height="${H}" fill="url(#${N}glintLobe)"/>`;
    const wedges = `<g filter="url(#${N}glintSoft)"><path d="${wedgePath}" fill="#fff"/></g>`;
    const softDef = f.glintLobe !== 'cos' ? `<filter id="${N}glintSoft" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}"><feGaussianBlur stdDeviation="${(f.glintSoft * k).toFixed(3)}"/></filter>` : '';
    glintDefs = `
<filter id="${N}glintF" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="${(f.glintFreq / k).toFixed(5)}" numOctaves="${f.glintOct}" seed="${f.glintSeed}" stitchTiles="noStitch" result="q0"/>
<feColorMatrix in="q0" type="matrix" values="0 0 0 0 ${qr}  0 0 0 0 ${qg}  0 0 0 0 ${qb}  0 ${(0.9 * f.glintGain).toFixed(3)} ${(0.6 * f.glintGain).toFixed(3)} 0 ${(-f.glintThresh * f.glintGain).toFixed(3)}" result="q1"/>
<feComponentTransfer in="q1"${f.glintBlur > 0 ? ' result="q2"' : ''}><feFuncA type="linear" slope="${f.glintOp}"/></feComponentTransfer>${f.glintBlur > 0 ? `<feGaussianBlur in="q2" stdDeviation="${(f.glintBlur * k).toFixed(3)}"/>` : ''}</filter>
${softDef}
<linearGradient id="${N}glintLobe" gradientUnits="userSpaceOnUse" x1="${GA.x1}" y1="${GA.y1}" x2="${GA.x2}" y2="${GA.y2}">${lobe}</linearGradient>
<mask id="${N}glintRidge" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">${f.glintMaskBlur > 0 ? `<g filter="url(#${N}glintMaskF)">` : ''}${f.glintFull ? two(oi, 'fill="#fff" fill-rule="evenodd"') : bandTwo(oi, oo, 'fill="#fff" fill-rule="evenodd"')}${f.glintMaskBlur > 0 ? '</g>' : ''}</mask>${f.glintMaskBlur > 0 ? `<filter id="${N}glintMaskF" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}"><feGaussianBlur stdDeviation="${(f.glintMaskBlur * k).toFixed(3)}"/></filter>` : ''}
<mask id="${N}glintLit" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">${f.glintLobe === 'cos' ? cosRect : wedges}</mask>${f.glintLobe === 'both' ? `
<mask id="${N}glintCos" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">${cosRect}</mask>` : ''}`;
    glintLayer = `<g id="${N}glints" inkscape:groupmode="layer" inkscape:label="2b catch-lights: thresholded noise on the ridge, lit lobes only" clip-path="url(#${N}clip)" mask="url(#${N}glintLit)">
<g mask="url(#${N}glintRidge)">${f.glintLobe === 'both' ? `<g mask="url(#${N}glintCos)">` : ''}<rect x="0" y="0" width="${W}" height="${H}" filter="url(#${N}glintF)"/>${f.glintLobe === 'both' ? '</g>' : ''}</g>
</g>
`;
    glintDesc = ` Glints (finish6): thresholded fractalNoise (${f.glintFreq}/print px, ${f.glintOct} oct, seed ${f.glintSeed}, top ≈${Math.round(100 * (1 - f.glintThresh) / 2)} %) in ${f.glintColor} @${f.glintOp} on the ridge band (${f.transInset + f.glintInner}–${f.ridgeInset + f.glintOuter} px), lit lobes only (${f.glintLobe}${f.glintLobe === 'cos' ? '' : ' ' + f.glintSectors + '° soft ' + f.glintSoft + ' px'}).`;
  }
  // KNOB ridgeShine (default off)
  const shineOn = +f.ridgeShine > 0;
  const RS = shineOn ? axisPts(f.ridgeShineAxis == null ? f.axA : f.ridgeShineAxis) : null;
  const shineStops = shineOn ? Array.from({ length: 81 }, (_, i) => { const t = -1 + i / 40; let s = 2 * t * t - 1; if (+f.ridgeShineHarm === 4) s = 2 * s * s - 1; const op = s > 0 ? f.ridgeShine * Math.pow(s, f.ridgeShineP) : 0; return `<stop offset="${(i / 80).toFixed(4)}" stop-color="${f.ridgeShineColor}" stop-opacity="${op.toFixed(4)}"/>`; }).join('') : '';
  const shineDefs = shineOn ? `\n<linearGradient id="${N}ridgeShine" gradientUnits="userSpaceOnUse" x1="${RS.x1}" y1="${RS.y1}" x2="${RS.x2}" y2="${RS.y2}">${shineStops}</linearGradient>` : '';
  const shineDesc = shineOn ? ` Ridge shine (finish6): ${f.ridgeShineColor} on the ridge band (${f.transInset}–${f.ridgeInset} px) at opacity ${f.ridgeShine}·max(cos(${+f.ridgeShineHarm === 4 ? 4 : 2}(θ−${f.ridgeShineAxis == null ? f.axA : f.ridgeShineAxis}°)),0)^${f.ridgeShineP}.` : '';
  const shineLayer = shineOn ? `<g id="${N}ridgeShineLayer" inkscape:groupmode="layer" inkscape:label="3b ridge shine (specular light on the ridge band)" clip-path="url(#${N}clip)">\n${bandTwo(o2, o3, `fill="url(#${N}ridgeShine)" fill-rule="evenodd"`)}\n</g>\n` : '';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
<title>Dose 01 medallion — meander v3.1 with finish final-A, relative bands (finish5), ${g.frame}</title>
<desc>Geometry: meander v3.1 channel outline (meander3.js: rc ${g.rc}, rf ${g.rf}, phase ${g.phaseDeg}). Finish: body ${f.body} over the whole footprint with the measured sector sweeps (A axis ${f.axA}°, B axis ${f.axB}°) and zone-gated foil grain (fractalNoise ${f.grainFreq}/print px seed ${f.grainSeed}; zones seed ${f.zoneSeed}; flecks top ≈2 % @${f.fleckOp}); then RELATIVE bands clipped to the footprint: rim (0–${f.rimInset} px) black @${f.rimOp}, transition (${f.rimInset}–${f.transInset} px) black @${f.transOp}, ridge (${f.transInset}–${f.ridgeInset} px) black @${f.ridgeOp}, centre (inside ${f.ridgeInset} px) black @${f.centreOp}; highlight cap ${f.cap}. Ink footprint = geometry. Pure vector, deterministic.${glintDesc}${shineDesc}${edgeDesc}${bandDesc}</desc>
<defs><linearGradient id="${N}sweepA" gradientUnits="userSpaceOnUse" x1="${A.x1}" y1="${A.y1}" x2="${A.x2}" y2="${A.y2}">${stopsA}</linearGradient>
<linearGradient id="${N}sweepB" gradientUnits="userSpaceOnUse" x1="${B.x1}" y1="${B.y1}" x2="${B.x2}" y2="${B.y2}">${stopsB}</linearGradient>${edgeDefs}
${filt}
<mask id="${N}mBody" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}">${two(O(0.6), 'fill="#fff" fill-rule="evenodd"')}</mask>
<clipPath id="${N}clip" clipPathUnits="userSpaceOnUse">${two(geom, 'clip-rule="evenodd"')}</clipPath>${glintDefs}${shineDefs}${bandDefs}${bandMaskDef}</defs>
<g id="${N}rings" inkscape:groupmode="layer" inkscape:label="1 purple rings">${ring(g.purpleIn[0], g.purpleIn[1])}${ring(g.purpleOut[0], g.purpleOut[1])}</g>
<g id="${N}geometry" inkscape:groupmode="layer" inkscape:label="2 meander geometry (ink footprint) with body tone, sweeps, grain" filter="url(#${N}grain)">
<g fill="${f.body}" fill-rule="evenodd">${two(geom, '')}</g>
<rect x="0" y="0" width="${W}" height="${H}" fill="url(#${N}sweepA)" mask="url(#${N}mBody)"/>
<rect x="0" y="0" width="${W}" height="${H}" fill="url(#${N}sweepB)" mask="url(#${N}mBody)"/>
</g>
${glintLayer}<g id="${N}finish" inkscape:groupmode="layer" inkscape:label="3 gold finish: relative rim / transition / centre bands" ${f.bandMaskInset > 0 ? `mask="url(#${N}bandMask)"` : `clip-path="url(#${N}clip)"`} fill="${f.bandHex}" fill-rule="evenodd">
${bandOpen}${f.rimStroke > 0 ? two(geom, `fill="none" stroke="${f.bandHex}" stroke-width="${n(S(2 * f.rimStroke))}" stroke-opacity="${f.rimOp}"`) : bandTwo(O(0.7), o1, rimFill)}
${bandTwo(o1, o2, transFill)}
${bandTwo(o2, o3, `fill-opacity="${f.ridgeOp}"`)}
${two(o3, `fill-opacity="${f.centreOp}"`)}${catchOn ? '\n' + bandTwo(geom, O(f.edgeCatchWidth), `fill="url(#${N}edgeCatch)"`) : ''}${bandClose}
</g>
${shineLayer}<g id="owl-slot" inkscape:groupmode="layer" inkscape:label="4 owl slot (licensed vector bird goes here)"/>
</svg>
`;
  return svg;
}
if (require.main === module) {
  const args = process.argv.slice(2); const g = {}, f = {}; let out = null;
  for (let i = 0; i < args.length; i++) { const a = args[i]; if (!a.startsWith('--')) continue; const key = a.slice(2), v = args[++i]; if (key === 'out') { out = v; continue; } const val = isNaN(v) ? v : parseFloat(v); if (key in P) f[key] = val; else g[key] = val; }
  const svg = build(g, f); if (out) { fs.writeFileSync(out, svg); console.log(JSON.stringify({ out, bytes: svg.length })); } else process.stdout.write(svg);
}
module.exports = { build, P };
