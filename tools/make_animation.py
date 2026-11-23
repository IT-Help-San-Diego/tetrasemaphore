#!/usr/bin/env python3
"""tools/make_animation.py: the four semaphores under the three moves, as short videos, and one loop of all four.

Two kinds of film.

  <STATE>-semaphore-three-moves     one semaphore under each of the three moves in turn, with the published overlap
  TETRASEMAPHORE-four-own-moves-loop  all four at once and always in motion: three make their own move on every beat,
                                      and NORMATIVE, whose mark survives every move, makes the three in turn

What is drawn. Each picture is the release's own finished picture (semaphores/pictures/TETRASEMAPHORE-<STATE>-en-2460.png,
rendered from the master by the release's build). Nothing is redrawn. Each move is applied to that picture as a linear map
about its centre:

  identity            I       : (x, y) -> (x, y)      nothing moves
  left-to-right flip  sigma_v : (x, y) -> (-x, y)     shown as (x, y) -> (x cos t, y),            t from 0 to 180 degrees
  top-to-bottom flip  sigma_h : (x, y) -> (x, -y)     shown as (x, y) -> (x, y cos t),            t from 0 to 180 degrees
  half-turn           C2      : (x, y) -> (-x, -y)    shown as a rotation in the plane by t,      t from 0 to 180 degrees

A flip cannot be reached by sliding or turning a picture within its plane, so the frames in between show the picture being
turned over through the third dimension, seen straight on and as if drawn on glass: that is the map (x, y cos t). The first
and last frame of each move are exact: the last is the first with its rows, its columns, or both reversed, pixel for pixel.
Making the same move again (t from 180 to 360 degrees) brings the picture back, because each move undoes itself.

The outline is the edge of everything drawn inside the ring (the mark, its gold and its bars), rendered from the master's own
layers glyph-body, glyph-fix and symmetry-marks, whichever of them that master has. It stays where the mark started.

The overlap figures, and so the words "yes" and "no", are read from the release's measurement record
(notation-measurements.json). A move counts as the mark's own when its overlap is above 0.99, the line the datasheet
specification draws. Each semaphore's colour is read from its master's ring.

The films of the release are in semaphores/films/, and RELEASE-MANIFEST.md gives each one's SHA-256. A run of this script
makes the same frames from the same pictures. It does not make the same bytes: a video encoder's output differs from one
ffmpeg build to the next, so the published files are identified by their hashes and not by a rebuild.

Usage, from the top folder:
  python3 tools/make_animation.py --tree . --out <folder> [--only <STATE>|loop]    make the films
  python3 tools/make_animation.py --tree . --check-frames                          test that every landing is exact

--check-frames makes each of the three moves on each of the four pictures and stops with exit code 1 unless the picture
after the move is the picture with its rows, its columns, or both reversed, pixel for pixel, and the picture after the
same move made twice is the picture it started from.

Needs Pillow, numpy and cairosvg, and imageio-ffmpeg for the encoder (not for --check-frames).
"""
import argparse, io, json, math, os, subprocess, sys
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg

W = H = 1080                      # the frame
FPS = 30
GROUND = (13, 17, 23)             # the website's ground, #0d1117
CREAM = (242, 228, 184)           # the datasheets' body text, #F2E4B8
GOLD = (222, 200, 117)            # the datasheets' value colour, #DEC875
ICE = (195, 230, 255)             # the datasheets' drafting colour, #C3E6FF
REL = 'build-record/master/states/proposals/notation/final-masters-2026-10-05'
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')
OWN = {'NORMATIVE': 'identity', 'NON-NORMATIVE': 'sigma_v', 'METACOGNITIVE': 'sigma_h', 'CRITICAL': 'c2'}
WORDS = {'identity': 'Nothing moves', 'sigma_v': 'Left-to-right flip', 'sigma_h': 'Top-to-bottom flip', 'c2': 'Half-turn'}
SYMBOL = {'identity': 'I', 'sigma_v': '\u03c3\u1d65', 'sigma_h': '\u03c3\u2095', 'c2': 'C\u2082'}
FORMULA = {'identity': 'I : (x, y) \u2192 (x, y)', 'sigma_v': '\u03c3\u1d65 : (x, y) \u2192 (\u2212x, y)',
           'sigma_h': '\u03c3\u2095 : (x, y) \u2192 (x, \u2212y)', 'c2': 'C\u2082 : (x, y) \u2192 (\u2212x, \u2212y)'}
SURVIVES = 0.99                   # docs/DATASHEET_SPEC.md: a semaphore's own move is the one whose overlap exceeds 0.99

def ease(u):                      # timing only: where in the move a frame is, not what the move is
    return 0.5 - 0.5 * math.cos(math.pi * u)

def moved(img, key, t):
    """The picture after the move's map at angle t (radians), same size, same centre. Exact at every multiple of pi."""
    n = img.size[0]
    if key == 'identity':
        return img.copy()
    if abs(math.sin(t)) < 1e-12:
        if round(math.cos(t)) == 1:
            return img.copy()
        return img.transpose({'sigma_h': Image.FLIP_TOP_BOTTOM, 'sigma_v': Image.FLIP_LEFT_RIGHT, 'c2': Image.ROTATE_180}[key])
    if key == 'c2':
        return img.rotate(-math.degrees(t), resample=Image.BICUBIC)
    s = math.cos(t)
    m = max(2, 2 * round(n * abs(s) / 2))                      # even, so the picture stays centred to the pixel
    out = Image.new(img.mode, (n, n), 0)
    if key == 'sigma_h':
        part = img.resize((n, m), Image.LANCZOS)
        if s < 0: part = part.transpose(Image.FLIP_TOP_BOTTOM)
        out.paste(part, (0, (n - m) // 2))
    else:
        part = img.resize((m, n), Image.LANCZOS)
        if s < 0: part = part.transpose(Image.FLIP_LEFT_RIGHT)
        out.paste(part, ((n - m) // 2, 0))
    return out

def mark_mask(master, px):
    """Everything drawn inside the ring, as one mask, from the master's own layers."""
    t = ET.parse(master); r = t.getroot(); pm = {c: p for p in r.iter() for c in p}
    kept = [e for e in r.iter() if e.get('id') in ('glyph-body', 'glyph-fix', 'symmetry-marks')]; anc = set()
    for e in kept:
        x = e
        while x in pm:
            x = pm[x]; anc.add(x)
    def prune(node):
        for ch in list(node):
            if ch in kept: continue
            if ch in anc: prune(ch)
            else: node.remove(ch)
    prune(r)
    png = cairosvg.svg2png(bytestring=ET.tostring(r, encoding='unicode').encode(), output_width=px, output_height=px)
    return Image.open(io.BytesIO(png)).convert('RGBA').getchannel('A')

def ring_colour(master):
    rings = [e for e in ET.parse(master).getroot().iter() if e.get('id') == 'finalA5-rings'][0]
    hexes = sorted({e.get('stroke') for e in rings.iter() if e.get('stroke')})
    if len(hexes) != 1: sys.exit('STOP: %s: the ring layer has %d stroke colours, expected one' % (master, len(hexes)))
    h = hexes[0].lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def axis_marks(d2, key, cx, cy, sem):
    """The line a flip turns about, or the arrow of a turn in the plane. Drawn at twice size on d2."""
    if key == 'identity': return
    r0, r1 = (sem // 2 + 10) * 2, (sem // 2 + 10 + max(14, sem // 26)) * 2; cx, cy = cx * 2, cy * 2; w = 6 if sem > 500 else 5
    if key == 'sigma_h':
        for sx in (-1, 1): d2.line([(cx + sx * r0, cy), (cx + sx * r1, cy)], fill=ICE + (255,), width=w)
    elif key == 'sigma_v':
        for sy in (-1, 1): d2.line([(cx, cy + sy * r0), (cx, cy + sy * r1)], fill=ICE + (255,), width=w)
    else:
        ra = (sem // 2 + (36 if sem > 500 else 22)) * 2; k = 1.0 if sem > 500 else 0.7
        d2.arc([cx - ra, cy - ra, cx + ra, cy + ra], start=-62, end=-28, fill=ICE + (255,), width=w)
        a = math.radians(-28); px, py = cx + ra * math.cos(a), cy + ra * math.sin(a); tx, ty = -math.sin(a), math.cos(a); nx, ny = math.cos(a), math.sin(a)
        d2.polygon([(px + 26 * k * tx, py + 26 * k * ty), (px - 6 * k * tx + 16 * k * nx, py - 6 * k * ty + 16 * k * ny),
                    (px - 6 * k * tx - 16 * k * nx, py - 6 * k * ty - 16 * k * ny)], fill=ICE + (255,))

class Semaphore:
    """One semaphore at a given size in the frame: its picture, its outline, its colour, its published overlaps."""
    def __init__(self, tree, state, sem, ss, inner_px, outer_px):
        self.state, self.sem = state, sem
        picture = os.path.join(tree, 'semaphores/pictures/TETRASEMAPHORE-%s-en-2460.png' % state)
        master = os.path.join(tree, 'semaphores/vector-masters/MASTER-medallion-%s-notation-slot820.svg' % state)
        record = json.load(open(os.path.join(tree, REL, 'notation-measurements.json'), encoding='utf-8'))['states']
        entry = [x for x in record if x.get('name') == state]
        if len(entry) != 1: sys.exit('STOP: the measurement record has %d entries named %s' % (len(entry), state))
        self.overlap = entry[0]['measure']['print']['iou']
        self.colour = ring_colour(master)
        src = Image.open(picture).convert('RGBA')
        self.big = src.resize((sem * ss, sem * ss), Image.LANCZOS)           # worked size
        self.rest = self.big.resize((sem, sem), Image.LANCZOS)               # the picture at rest, at frame size
        m = mark_mask(master, sem * ss).point(lambda v: 255 if v > 127 else 0)
        outer = m.filter(ImageFilter.MaxFilter(2 * round(outer_px * ss) + 1)); inner = m.filter(ImageFilter.MaxFilter(2 * round(inner_px * ss) + 1))
        band = Image.fromarray(np.where(np.asarray(inner) > 0, 0, np.asarray(outer)).astype(np.uint8)).resize((sem, sem), Image.LANCZOS)
        self.outline = Image.new('RGBA', (sem, sem), ICE + (0,)); self.outline.putalpha(band.point(lambda v: int(v * 0.92)))

    def turned(self, img, fx, fy):
        """The picture as earlier moves left it: columns reversed (fx), rows reversed (fy), or both. Exact."""
        if fx: img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if fy: img = img.transpose(Image.FLIP_TOP_BOTTOM)
        return img

    def at(self, key, t, fx=False, fy=False):
        if key == 'identity' or abs(math.sin(t)) < 1e-12:
            return moved(self.turned(self.rest, fx, fy), key, t)               # exact frames, at frame size
        return moved(self.turned(self.big, fx, fy), key, t).resize((self.sem, self.sem), Image.LANCZOS)

def centred(d, cx, y, text, font, fill):
    w = d.textlength(text, font=font); d.text((cx - w / 2, y), text, font=font, fill=fill)

class Fonts:
    def __init__(self, tree): self.tree = tree
    def __call__(self, n, bold=False):
        return ImageFont.truetype(os.path.join(self.tree, 'tools/fonts', 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'), n)

class ThreeMoves:
    """One semaphore under sigma_h, sigma_v and C2 in turn; each move is then made again to bring the picture back."""
    SEM, CX, CY = 620, W // 2, 505
    PLAN = [('sigma_h', 36, 108, 54, 21), ('sigma_v', 15, 66, 39, 21), ('c2', 15, 66, 39, 21)]     # move: rest, move, hold, back
    END = 48
    def __init__(self, tree, state):
        self.s = Semaphore(tree, state, self.SEM, 2, 2.0, 4.5); self.font = Fonts(tree); self.state = state
        self.name = '%s-semaphore-three-moves' % state
        self.timeline = []
        for i, (key, rest, move, hold, back) in enumerate(self.PLAN):
            self.timeline += [(i, 'rest', 0.0)] * rest + [(i, 'move', (k + 1) / move) for k in range(move)]
            self.timeline += [(i, 'hold', 1.0)] * hold + [(i, 'back', (k + 1) / back) for k in range(back)]
        self.timeline += [(None, 'end', 0.0)] * self.END
        self._over = {}

    def angle(self, n):
        i, phase, u = self.timeline[n]
        if phase in ('rest', 'end'): return i, phase, 0.0
        if phase == 'hold': return i, phase, math.pi
        if phase == 'move': return i, phase, math.pi * (1.0 if u == 1.0 else ease(u))
        return i, phase, math.pi * (2.0 if u == 1.0 else 1.0 + ease(u))

    def overlay(self, i, phase):
        k = (i, phase == 'hold', phase == 'end')
        if k in self._over: return self._over[k]
        s, f = self.s, self.font
        big = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
        if i is not None: axis_marks(ImageDraw.Draw(big), self.PLAN[i][0], self.CX, self.CY, self.SEM)
        over = big.resize((W, H), Image.LANCZOS)
        over.alpha_composite(s.outline, (self.CX - self.SEM // 2, self.CY - self.SEM // 2))
        d = ImageDraw.Draw(over); col = s.colour + (255,)
        centred(d, W / 2, 38, self.state, f(54, True), col)
        centred(d, W / 2, 112, 'Does the mark survive the move?', f(34), CREAM + (255,))
        if i is not None:
            key = self.PLAN[i][0]
            centred(d, W / 2, 858, WORDS[key] + '      ' + FORMULA[key], f(38), CREAM + (255,))
            if phase == 'hold':
                says = 'Yes: it lands on itself.' if s.overlap[key] > SURVIVES else 'No: it lands somewhere else.'
                tail = 'Overlap %.4f' % s.overlap[key]; fb, fr = f(38, True), f(38); gap = 26
                w1, w2 = d.textlength(says, font=fb), d.textlength(tail, font=fr); x = (W - (w1 + gap + w2)) / 2
                d.text((x, 922), says, font=fb, fill=col); d.text((x + w1 + gap, 922), tail, font=fr, fill=GOLD + (255,))
        else:
            own = [key for key in ('sigma_v', 'sigma_h', 'c2') if s.overlap[key] > SURVIVES]
            if len(own) == 3: lines = ['Every move leaves the mark', 'where it was.']
            elif len(own) == 1: lines = ['Only its own move, %s, leaves the mark' % SYMBOL[own[0]], 'where it was.']
            else: sys.exit('STOP: %s survives %d of the three moves; no closing line is written for that' % (self.state, len(own)))
            centred(d, W / 2, 858, lines[0], f(38, True), col); centred(d, W / 2, 912, lines[1], f(38, True), col)
        centred(d, W / 2, 984, 'Outline: where the mark started', f(30), ICE + (255,))
        centred(d, W / 2, 1026, 'Overlap is measured on the master. 1.0000 would be a perfect match.', f(26), GOLD + (255,))
        self._over[k] = over
        return over

    def picture(self, n):
        i, phase, t = self.angle(n)
        return self.s.at(self.PLAN[i][0] if i is not None else 'sigma_h', t)

    def frame(self, n):
        i, phase, t = self.angle(n)
        im = Image.new('RGBA', (W, H), GROUND + (255,))
        im.alpha_composite(self.picture(n), (self.CX - self.SEM // 2, self.CY - self.SEM // 2))
        im.alpha_composite(self.overlay(i, phase))
        return im.convert('RGB')

class FourOwnMoves:
    """All four at once, always in motion, in six beats that end where they began: a loop.

    NON-NORMATIVE, METACOGNITIVE and CRITICAL are shown under their own move on every beat. NORMATIVE's own move is the
    identity, in which nothing moves, so there is no motion of its own to show; its mark survives every move, so the
    three are applied to it in turn: sigma_v, sigma_h, C2. Its name line keeps I; the line below names the move on screen. Any two of the three make the third, so
    three beats bring NORMATIVE's picture home, two beats bring each of the others home, and six bring all four home."""
    SEM = 340
    PLACE = {'NORMATIVE': (290, 300), 'NON-NORMATIVE': (790, 300), 'METACOGNITIVE': (290, 752), 'CRITICAL': (790, 752)}
    BEATS, SETTLE, MOVE = 6, 6, 48
    SEQ = {'NORMATIVE': ['sigma_v', 'sigma_h', 'c2'] * 2, 'NON-NORMATIVE': ['sigma_v'] * 6, 'METACOGNITIVE': ['sigma_h'] * 6, 'CRITICAL': ['c2'] * 6}
    def __init__(self, tree):
        self.font = Fonts(tree); self.name = 'TETRASEMAPHORE-four-own-moves-loop'
        self.sems = {st: Semaphore(tree, st, self.SEM, 3, 1.5, 3.5) for st in STATES}
        for st in STATES:                                        # a move is shown as a mark's own only if the record says it survives it
            for key in set(self.SEQ[st]):
                if not self.sems[st].overlap[key] > SURVIVES:
                    sys.exit('STOP: %s under %s has overlap %s in the record, not above %s' % (st, key, self.sems[st].overlap[key], SURVIVES))
        self.timeline = []
        for b in range(self.BEATS):
            self.timeline += [(b, 0.0)] * self.SETTLE + [(b, (k + 1) / self.MOVE) for k in range(self.MOVE)]
        self._over = {}

    def before(self, st, b):
        """Which way round the picture is when beat b starts: (columns reversed, rows reversed)."""
        fx = fy = False
        for key in self.SEQ[st][:b]:
            if key in ('sigma_v', 'c2'): fx = not fx
            if key in ('sigma_h', 'c2'): fy = not fy
        return fx, fy

    def angle(self, n):
        b, u = self.timeline[n]
        return b, math.pi * (0.0 if u == 0.0 else 1.0 if u == 1.0 else ease(u))

    def overlay(self, b):
        k = b % 3
        if k in self._over: return self._over[k]
        f = self.font
        big = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d2 = ImageDraw.Draw(big)
        for st in STATES: axis_marks(d2, self.SEQ[st][b], self.PLACE[st][0], self.PLACE[st][1], self.SEM)
        over = big.resize((W, H), Image.LANCZOS); d = ImageDraw.Draw(over)
        centred(d, W / 2, 18, 'The Tetrasemaphore', f(42, True), CREAM + (255,))
        one, two, ft = 'Each mark survives its own move.', 'Outline: where each mark started.', f(25)
        w1, w2, gap = d.textlength(one, font=ft), d.textlength(two, font=ft), 18; x = (W - (w1 + gap + w2)) / 2
        d.text((x, 74), one, font=ft, fill=CREAM + (255,)); d.text((x + w1 + gap, 74), two, font=ft, fill=ICE + (255,))
        for st in STATES:
            cx, cy = self.PLACE[st]; s = self.sems[st]
            over.alpha_composite(s.outline, (cx - self.SEM // 2, cy - self.SEM // 2))
            y = cy + self.SEM // 2 + (32 if cy < H / 2 else 8)
            centred(d, cx, y, st + '  ·  ' + SYMBOL[OWN[st]], f(28, True), s.colour + (255,))            # its own element, always
            centred(d, cx, y + 36, 'Move shown:  ' + FORMULA[self.SEQ[st][b]], f(23), CREAM + (255,))  # the move on screen now
        nc = self.sems['NORMATIVE'].colour + (255,)
        centred(d, W / 2, 1004, "NORMATIVE's own move is I, in which nothing moves.", f(22), nc)
        centred(d, W / 2, 1038, 'Its mark survives every move, so all three are shown on it in turn.', f(22), nc)
        self._over[k] = over
        return over

    def picture(self, st, n):
        b, t = self.angle(n); fx, fy = self.before(st, b)
        return self.sems[st].at(self.SEQ[st][b], t, fx, fy)

    def frame(self, n):
        im = Image.new('RGBA', (W, H), GROUND + (255,))
        for st in STATES:
            cx, cy = self.PLACE[st]
            im.alpha_composite(self.picture(st, n), (cx - self.SEM // 2, cy - self.SEM // 2))
        im.alpha_composite(self.overlay(self.timeline[n][0]))
        return im.convert('RGB')

def encode(film, out):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe(); N = len(film.timeline)
    head = [ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
            '-vf', 'scale=out_color_matrix=bt709:out_range=tv']
    tags = ['-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']
    mp4, webm = os.path.join(out, film.name + '.mp4'), os.path.join(out, film.name + '.webm')
    procs = [subprocess.Popen(head + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-tune', 'animation'] + tags + ['-movflags', '+faststart', mp4], stdin=subprocess.PIPE),
             subprocess.Popen(head + ['-c:v', 'libvpx-vp9', '-crf', '30', '-b:v', '0', '-row-mt', '1'] + tags + [webm], stdin=subprocess.PIPE)]
    for n in range(N):
        raw = film.frame(n).tobytes()
        for p in procs: p.stdin.write(raw)
    for p in procs:
        p.stdin.close()
        if p.wait() != 0: sys.exit('an encoder failed')
    for f in (mp4, webm):
        print('%s: %d frames, %.2f s, %d bytes' % (os.path.basename(f), N, N / FPS, os.path.getsize(f)))

def check_frames(tree):
    """Every landing is exact: one move reverses the picture's rows, columns or both; the same move again restores it."""
    bad = 0
    for st in STATES:
        src = Image.open(os.path.join(tree, 'semaphores/pictures/TETRASEMAPHORE-%s-en-2460.png' % st)).convert('RGBA'); a = np.asarray(src)
        for key, want in (('sigma_h', a[::-1]), ('sigma_v', a[:, ::-1]), ('c2', a[::-1, ::-1])):
            once = moved(src, key, math.pi)
            ok = (np.array_equal(np.asarray(once), want) and np.array_equal(np.asarray(moved(once, key, math.pi)), a)
                  and np.array_equal(np.asarray(moved(src, key, 2 * math.pi)), a))
            print('%-9s %-13s %-7s %s' % ('exact' if ok else 'NOT EXACT', st, key, 'once reverses, twice restores' if ok else ''))
            bad += not ok
        if not np.array_equal(np.asarray(moved(src, 'identity', math.pi)), a):
            print('NOT EXACT %-13s identity' % st); bad += 1
    print('FRAME CHECK %s: 4 pictures, 3 moves each' % ('PASS' if not bad else 'FAIL'))
    return 1 if bad else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tree', required=True); ap.add_argument('--out', default='')
    ap.add_argument('--only', default='', help='a state name, or "loop"; default: all five films')
    ap.add_argument('--check-frames', action='store_true', help='test the landings and make no film')
    a = ap.parse_args()
    if a.check_frames: sys.exit(check_frames(a.tree))
    if not a.out: ap.error('--out is needed to make films')
    os.makedirs(a.out, exist_ok=True)
    for st in STATES:
        if a.only in ('', st): encode(ThreeMoves(a.tree, st), a.out)
    if a.only in ('', 'loop'): encode(FourOwnMoves(a.tree), a.out)

if __name__ == '__main__':
    main()
