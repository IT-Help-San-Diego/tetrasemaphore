#!/usr/bin/env python3
"""png_tag.py — give PNG files a 300 dpi pHYs chunk and an sRGB chunk (build 7, 14 Oct 2026; Science's BUILD-7-AND-CARDS item 2 and the wake-up
packet J2: "a 300 dpi pHYs chunk and an sRGB chunk on every export, pixels otherwise as rendered").
Pure chunk surgery: IHDR stays first; any existing sRGB / gAMA / cHRM / pHYs / iCCP chunk is removed; then sRGB (rendering intent 0, perceptual),
gAMA 45455 and cHRM (the sRGB primaries, which the PNG spec says SHOULD accompany sRGB for decoders that ignore it) and pHYs (11811 px/m = 300 dpi
on both axes, unit 1 = metre) are inserted right after IHDR. IDAT and every other chunk are untouched, so the pixels are byte for byte as rendered.
Idempotent. Usage: png_tag.py [--dpi 300] [--check] <png or dir> ...   (--check only reports; exit 1 if any file lacks the tags)
"""
import sys, os, struct, zlib, glob
args = [a for a in sys.argv[1:] if not a.startswith('--')]; dpi = 300; check = '--check' in sys.argv
if '--dpi' in sys.argv: dpi = float(sys.argv[sys.argv.index('--dpi') + 1])
PPM = int(round(dpi / 0.0254))
def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
def chunks(b):
    assert b[:8] == b'\x89PNG\r\n\x1a\n', 'not a PNG'; i = 8; out = []
    while i < len(b):
        n = struct.unpack('>I', b[i:i + 4])[0]; t = b[i + 4:i + 8]; d = b[i + 8:i + 8 + n]; out.append((t, d)); i += 12 + n
    return out
def tags(b):
    c = {t: d for t, d in chunks(b)}
    ph = c.get(b'pHYs'); x, y, u = struct.unpack('>IIB', ph) if ph else (0, 0, 0)
    return dict(sRGB=b'sRGB' in c, gAMA=b'gAMA' in c, cHRM=b'cHRM' in c, pHYs=ph is not None, ppm=(x, y, u), dpi=round(x * 0.0254, 2) if u == 1 else None)
def tag(p):
    b = open(p, 'rb').read(); cs = chunks(b); assert cs[0][0] == b'IHDR' and cs[-1][0] == b'IEND'
    keep = [(t, d) for t, d in cs if t not in (b'sRGB', b'gAMA', b'cHRM', b'pHYs', b'iCCP')]
    new = [chunk(b'sRGB', b'\x00'), chunk(b'gAMA', struct.pack('>I', 45455)),
           chunk(b'cHRM', struct.pack('>8I', 31270, 32900, 64000, 33000, 30000, 60000, 15000, 6000)), chunk(b'pHYs', struct.pack('>IIB', PPM, PPM, 1))]
    out = b[:8] + chunk(*keep[0]) + b''.join(new) + b''.join(chunk(t, d) for t, d in keep[1:])
    idat_before = b''.join(d for t, d in cs if t == b'IDAT'); idat_after = b''.join(d for t, d in chunks(out) if t == b'IDAT'); assert idat_before == idat_after
    open(p, 'wb').write(out); return tags(out)
files = []
for a in args:
    files += sorted(glob.glob(os.path.join(a, '**', '*.png'), recursive=True)) if os.path.isdir(a) else [a]
bad = 0
for p in files:
    t = tags(open(p, 'rb').read()) if check else tag(p)
    good = t['sRGB'] and t['pHYs'] and t['dpi'] == dpi; bad += (not good)
    print(('ok  ' if good else 'MISSING ') + f"{p}: sRGB {t['sRGB']} gAMA {t['gAMA']} cHRM {t['cHRM']} pHYs {t['pHYs']} dpi {t['dpi']}")
print(f'{len(files)} files, {bad} without the tags'); sys.exit(1 if (check and bad) else 0)
