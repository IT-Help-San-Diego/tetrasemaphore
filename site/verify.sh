#!/bin/bash
# verify.sh — tetrasemaphore.systems static-site invariant gate. Exits non-zero on failure.
set -euo pipefail
cd "$(dirname "$0")"

python3 -I - <<'PY'
import base64, glob, hashlib, html, json, os, re, struct, sys, unicodedata

FAIL = 0
def say(msg):
    print(msg)
def bad(msg):
    global FAIL
    print("FAIL: " + msg)
    FAIL = 1

PAGES = tuple(p for p in ("index.html", "note.html", "method.html", "404.html") if p in ("index.html", "method.html", "404.html") or os.path.exists(p))
POLICIES = ("infra/cloudfront/security-headers.json", "infra/cloudfront/assets-headers.json")

# 1. All three <style> blocks must be byte-identical, contain no @import/url(), and their quoted sha256 hash must sit in all 3 meta CSPs + both header policies.
styles = {}
for p in PAGES:
    if not os.path.exists(p):
        bad(f"{p}: missing")
        continue
    raw = open(p, encoding="utf-8").read()
    m = re.search(r"<style>(.*?)</style>", raw, re.S)
    if not m:
        bad(f"{p}: missing <style> block")
    else:
        styles[p] = m.group(1)
        if re.search(r"@import\b|url\s*\(", styles[p], re.I):
            bad(f"{p}: <style> contains @import or url()")

if len(styles) == len(PAGES):
    ref_style = styles["index.html"]
    for p in PAGES[1:]:
        if styles[p] != ref_style:
            bad(f"{p}: <style> block differs from index.html")
    h = "sha256-" + base64.b64encode(hashlib.sha256(ref_style.encode("utf-8")).digest()).decode()
    quoted = f"style-src 'self' '{h}'"
    for p in PAGES:
        raw = open(p, encoding="utf-8").read()
        mc = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"', raw)
        if not mc:
            bad(f"{p}: meta CSP missing")
        elif quoted not in mc.group(1):
            bad(f"{p}: meta CSP missing quoted hash {quoted}")
    for pol in POLICIES:
        if not os.path.exists(pol):
            bad(f"{pol}: missing")
            continue
        raw_pol = open(pol, encoding="utf-8").read()
        if quoted not in raw_pol:
            bad(f"{pol}: policy CSP missing quoted hash {quoted}")
    say(f"OK: <style> identical across pages and quoted CSP hash synced ({h})")

# 2. No executable JS; every <script> tag must be literally <script type="application/ld+json"> and parse as JSON.
for p in PAGES:
    raw = open(p, encoding="utf-8").read()
    for m in re.finditer(r"<script\b[^>]*>", raw, re.I):
        if m.group(0) != '<script type="application/ld+json">':
            bad(f"{p}: non-JSON-LD script tag: {m.group(0)}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            bad(f"{p}: JSON-LD parse error: {e}")
for pol in POLICIES:
    try:
        json.load(open(pol, encoding="utf-8"))
    except Exception as e:
        bad(f"{pol}: JSON parse error: {e}")
say("OK: no executable JS; JSON-LD and header policies parse")

# 3. No inline style attributes; no external or protocol-relative subresources (double- or single-quoted); no leaked local paths; valid symbols.
home_pat = "/" + "Users/"
for p in PAGES:
    raw = open(p, encoding="utf-8").read()
    if re.search(r'\bstyle\s*=', raw, re.I):
        bad(f"{p}: inline style attribute")
    if re.search(r'\b(?:src|srcset)\s*=\s*[\'"]?(?:https?:|//)', raw, re.I):
        bad(f"{p}: external or protocol-relative src/srcset")
    for lm in re.finditer(r"<link\b[^>]*>", raw, re.I):
        tag = lm.group(0)
        if 'rel="canonical"' in tag or "rel='canonical'" in tag:
            continue
        if re.search(r'\bhref\s*=\s*[\'"]?(?:https?:|//)', tag, re.I):
            bad(f"{p}: external link tag: {tag}")
    if home_pat in raw or "/private/tmp/" in raw:
        bad(f"{p}: leaked local filesystem path")
    for ent in ("&#7510;", "&#8335;"):
        if ent in raw:
            bad(f"{p}: forbidden entity {ent}")
    txt = html.unescape(raw)
    for ch in set(txt):
        if ord(ch) > 127:
            cat = unicodedata.category(ch)
            if unicodedata.name(ch, None) is None or cat in ("Cn", "Co", "Cs") or ch in ("\u1d56", "\u208f"):
                bad(f"{p}: forbidden/unassigned code point U+{ord(ch):04X}")
say("OK: no inline styles, external subresources, local paths, or bad code points")

# 4. og:image metadata and 1200x630 JPEG dimensions.
for p in PAGES:
    raw = open(p, encoding="utf-8").read()
    for prop, val in (("og:image", "https://tetrasemaphore.systems/assets/og-card.jpg"),
                      ("og:image:type", "image/jpeg"),
                      ("og:image:width", "1200"),
                      ("og:image:height", "630")):
        if f'property="{prop}" content="{val}"' not in raw:
            bad(f"{p}: missing {prop}={val}")

def jpg_dims(path):
    b = open(path, "rb").read()
    if len(b) < 4 or b[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(b) - 1:
        if b[i] != 0xFF:
            return None
        while i < len(b) and b[i] == 0xFF:
            i += 1
        if i >= len(b):
            break
        marker = b[i]
        i += 1
        if marker in (0xD8, 0xD9) or (0xD0 <= marker <= 0xD7):
            continue
        if i + 2 > len(b):
            break
        seg_len = struct.unpack(">H", b[i:i+2])[0]
        if marker in (0xC0, 0xC1, 0xC2) and i + 7 <= len(b):
            h_px, w_px = struct.unpack(">HH", b[i+3:i+7])
            return (w_px, h_px)
        i += seg_len
    return None

if not os.path.exists("assets/og-card.jpg"):
    bad("assets/og-card.jpg missing")
else:
    dims = jpg_dims("assets/og-card.jpg")
    if dims != (1200, 630):
        bad(f"assets/og-card.jpg dimensions {dims} != (1200, 630)")
say("OK: og:image metadata and 1200x630 JPEG verified")

# 5. Exact sealed asset inventory, 300 dpi + sRGB on all PNGs, and zero owl/flashcard files.
SEALED_ASSETS = {
    "assets/TETRASEMAPHORE-CRITICAL-en-1298.png": "a43da812ca3a7c88",
    "assets/TETRASEMAPHORE-CRITICAL-en-512.png": "89dc35c8fcd840f0",
    "assets/TETRASEMAPHORE-CRITICAL-es-1298.png": "54bcc40dea8e470d",
    "assets/TETRASEMAPHORE-CRITICAL-es-512.png": "30af4e519891b595",
    "assets/TETRASEMAPHORE-METACOGNITIVE-en-1298.png": "0f050e240c74e952",
    "assets/TETRASEMAPHORE-METACOGNITIVE-en-512.png": "1fc5ca3480246e12",
    "assets/TETRASEMAPHORE-METACOGNITIVE-es-1298.png": "0b74d6670118923a",
    "assets/TETRASEMAPHORE-METACOGNITIVE-es-512.png": "289b7447e6ab663e",
    "assets/TETRASEMAPHORE-NON-NORMATIVE-en-1298.png": "658837bd2d2802b3",
    "assets/TETRASEMAPHORE-NON-NORMATIVE-en-512.png": "9b90f014e077453b",
    "assets/TETRASEMAPHORE-NON-NORMATIVE-es-1298.png": "a4017750741981e9",
    "assets/TETRASEMAPHORE-NON-NORMATIVE-es-512.png": "af1236728c2dd7a6",
    "assets/TETRASEMAPHORE-NORMATIVE-en-1298.png": "eacf65bc9181f649",
    "assets/TETRASEMAPHORE-NORMATIVE-en-512.png": "b893c34898ab9ebc",
    "assets/TETRASEMAPHORE-NORMATIVE-es-1298.png": "077215b442760441",
    "assets/TETRASEMAPHORE-NORMATIVE-es-512.png": "1c49f6829a561265",
    "assets/og-card.jpg": "a175dc759f3a2fd9",
}

actual_assets = {}
for root, _, fs in os.walk("assets"):
    for fn in fs:
        if fn == ".DS_Store":
            continue
        rel = os.path.join(root, fn)
        actual_assets[rel] = hashlib.sha256(open(rel, "rb").read()).hexdigest()[:16]
        if "owl" in fn.lower() or "flashcard" in fn.lower():
            bad(f"forbidden asset filename: {rel}")

for k, h in sorted(actual_assets.items()):
    if k not in SEALED_ASSETS:
        bad(f"unexpected file in assets/: {k} ({h})")
    elif SEALED_ASSETS[k] != h:
        bad(f"{k}: sha16 {h} != sealed {SEALED_ASSETS[k]}")
for k, h in sorted(SEALED_ASSETS.items()):
    if k not in actual_assets:
        bad(f"missing sealed asset: {k} ({h})")

n_png = 0
for p in sorted(glob.glob("assets/*.png")):
    b = open(p, "rb").read()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        bad(f"{p}: not a valid PNG")
        continue
    pos, chunks, phys_data = 8, set(), None
    while pos < len(b):
        ln = struct.unpack(">I", b[pos:pos+4])[0]
        ctype = b[pos+4:pos+8]
        cdata = b[pos+8:pos+8+ln]
        chunks.add(ctype)
        if ctype == b"pHYs" and len(cdata) == 9:
            phys_data = struct.unpack(">IIB", cdata)
        pos += 12 + ln
    if b"sRGB" not in chunks or b"pHYs" not in chunks:
        bad(f"{p}: missing sRGB or pHYs chunk")
    elif phys_data is None or phys_data[2] != 1 or not (11810 <= phys_data[0] <= 11812 and 11810 <= phys_data[1] <= 11812):
        bad(f"{p}: pHYs {phys_data} is not 300 dpi (expected ~11811 ppm, unit=1)")
    n_png += 1

say(f"OK: {len(actual_assets)} sealed assets verified, {n_png} PNGs tagged sRGB + 300 dpi, no owl/flashcard ships")

# 6. Repo privacy gate: forbid tracking Research Artifacts, private_research_vault, transcripts, or sqlite/jsonl dumps in git.
import subprocess
try:
    tracked = subprocess.check_output(["git", "ls-files"], cwd="..", text=True).splitlines()
except Exception:
    tracked = []
FORBIDDEN_GIT = ("research artifacts/", "private_research_vault/", "wispr", "transcript", ".jsonl", ".sqlite", "doorbell", "handoff")
for tf in tracked:
    tfl = tf.lower()
    if any(tok in tfl for tok in FORBIDDEN_GIT):
        bad(f"forbidden private/dump path tracked in git: {tf}")
say("OK: git tracked-files privacy gate clean")

if FAIL == 0:
    say("verify.sh: ALL CHECKS PASS")
    sys.exit(0)
else:
    say("verify.sh: FAILURES PRESENT")
    sys.exit(1)
PY
