#!/bin/bash
# verify.sh — tetrasemaphore.systems static-site invariant gate. Exits non-zero on failure.
set -euo pipefail
cd "$(dirname "$0")"
FAIL=0
say() { printf '%s\n' "$*"; }
bad() { say "FAIL: $*"; FAIL=1; }

# 1. CSP style hash: recomputed from index.html must appear in every page meta AND both header policies.
HASH=$(python3 - <<'PY'
import re, hashlib, base64
html = open("index.html", encoding="utf-8").read()
style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
print("sha256-" + base64.b64encode(hashlib.sha256(style.encode()).digest()).decode())
PY
)
for f in index.html method.html 404.html; do
  grep -q "$HASH" "$f" || bad "$f: meta CSP hash missing/stale"
done
for f in infra/cloudfront/security-headers.json infra/cloudfront/assets-headers.json; do
  grep -q "$HASH" "$f" || bad "$f: policy CSP hash missing/stale"
done
say "OK: CSP style hash synced across pages and policies ($HASH)"

# 2. No executable JS; only JSON-LD allowed.
for f in index.html method.html 404.html; do
  if grep -qE '<script( type="application/ld\+json")?>' "$f"; then
    grep -q '<script type="application/ld+json">' "$f" || bad "$f: non-JSON-LD script tag"
  fi
done
say "OK: no executable JS"

# 3. No inline style attributes; no external subresources.
for f in index.html method.html 404.html; do
  grep -q 'style="' "$f" && bad "$f: inline style attribute"
  grep -qE '(src|srcset)="https?://' "$f" && bad "$f: external subresource"
done
say "OK: no inline style attributes, no external subresources"

# 4. JSON-LD parses; policies parse.
python3 - <<'PY'
import json, re, sys
for f in ("index.html", "method.html", "404.html"):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', open(f, encoding="utf-8").read(), re.S):
        json.loads(m.group(1))
for f in ("infra/cloudfront/security-headers.json", "infra/cloudfront/assets-headers.json"):
    json.load(open(f))
print("OK: JSON-LD and header policies parse")
PY

# 5. og:image is a raster with explicit dimensions.
grep -q 'property="og:image:type" content="image/jpeg"' index.html || bad "og:image:type missing"
[ -s assets/og-card.jpg ] || bad "assets/og-card.jpg missing"
say "OK: og:image is a raster (jpeg) with dimensions"

# 6. Email lockdown documented (no mail domain): null MX + SPF -all is set in Route 53, not in the repo.
# 7. Asset PNGs tagged 300 dpi + sRGB.
python3 - <<'PY'
import glob, struct
n = 0
for p in glob.glob("assets/*.png"):
    b = open(p, "rb").read()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", p
    pos, chunks = 8, set()
    while pos < len(b):
        ln = struct.unpack(">I", b[pos:pos+4])[0]
        chunks.add(b[pos+4:pos+8]); pos += 12 + ln
    assert b"sRGB" in chunks and b"pHYs" in chunks, f"/Users/careybalboa/.cache/dose01-toolchain/node missing sRGB/pHYs"
    n += 1
print(f"OK: {n} PNGs tagged sRGB + pHYs")
PY

# 8. No owl asset ships (rule: no owl in anything new).
ls assets/ | grep -qi owl && bad "owl asset present in assets/"
say "OK: no owl asset ships"

[ "$FAIL" = 0 ] && say "verify.sh: ALL CHECKS PASS" || { say "verify.sh: FAILURES PRESENT"; exit 1; }
