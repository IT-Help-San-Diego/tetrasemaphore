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
    ref_other = styles["note.html"]
    for p in ("method.html", "404.html"):
        if styles[p] != ref_other:
            bad(f"{p}: <style> block differs from note.html")
    hashes = []
    for p in PAGES:
        hp = "sha256-" + base64.b64encode(hashlib.sha256(styles[p].encode("utf-8")).digest()).decode()
        if hp not in hashes:
            hashes.append(hp)
        raw = open(p, encoding="utf-8").read()
        mc = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"', raw)
        if not mc:
            bad(f"{p}: meta CSP missing")
        elif f"'{hp}'" not in mc.group(1):
            bad(f"{p}: meta CSP missing quoted hash '{hp}'")
    for pol in POLICIES:
        if not os.path.exists(pol):
            bad(f"{pol}: missing")
            continue
        raw_pol = open(pol, encoding="utf-8").read()
        for hp in hashes:
            if f"'{hp}'" not in raw_pol:
                bad(f"{pol}: policy CSP missing quoted hash '{hp}'")
    say(f"OK: per-page <style> CSP hashes synced across meta + CloudFront policies ({', '.join(hashes)})")

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
    for prop, val in (("og:image", "https://tetrasemaphore.systems/assets/og-card.png"),
                      ("og:image:alt", "The four semaphores of the Tetrasemaphore, NORMATIVE, NON-NORMATIVE, METACOGNITIVE and CRITICAL, above the line V₄ = {I, σᵥ, σₕ, C₂}."),
                      ("og:image:type", "image/png"),
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
    "assets/og-card.png": "0cf08ac9028fc22d",
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

# 5b. The films. The site serves the release's own ten films from semaphores/films at the repository root and keeps no
# copy of them; site/Makefile uploads them from there to assets/films/ in the bucket. This section seals those ten
# files and the Makefile that uploads them. It catches accidents and drift in a reviewed checkout. Outside it: the
# deploying shell's command line and environment (another -f makefile, MAKEFILES, -i, the path of the checkout), and
# anyone able to write to the checkout, who could change this script itself.
SEALED_FILMS = {
    "CRITICAL-semaphore-three-moves.mp4": "5ec0d38ab26f27f468fe7ae84803e37b2ba1405a069de52777b7288469501d6a",
    "CRITICAL-semaphore-three-moves.webm": "76f52d0773424721fbaacc7cf10031289d4393aa72504ca471ce222bea002df7",
    "METACOGNITIVE-semaphore-three-moves.mp4": "145b27519fc8e0e493b786e82b797850cc216f2c82668d3bb40374b23174c71c",
    "METACOGNITIVE-semaphore-three-moves.webm": "cd3242484589a9f9a50a8497c1d498912d5299332eaf6c4c8ce806fad6cc46bd",
    "NON-NORMATIVE-semaphore-three-moves.mp4": "2ac167ff861474393cc9ff7ed26fc4ac08762ca08135e0c648328da10e03068e",
    "NON-NORMATIVE-semaphore-three-moves.webm": "b1942e8d2e817f62238d4ad4ef7b1485ececfb4382499fa21a69964d516c30dc",
    "NORMATIVE-semaphore-three-moves.mp4": "33718b22afe8ef1429a352afc42de12caf59388865dde1c5122737d0802b01e8",
    "NORMATIVE-semaphore-three-moves.webm": "2c87ea10582734ead58cacc3bbfbf54b9863bf7fa8882e61e42c388f62746c1f",
    "TETRASEMAPHORE-four-own-moves-loop.mp4": "35c210d93378ba0d7d7686d9c02718062648a34e388f5165e61ac04cdeb759bc",
    "TETRASEMAPHORE-four-own-moves-loop.webm": "ed041ff799eddffa891108cd9b39abf466fb9d9a80f11fe244c5b0731505d039",
}
FILMS_DIR = os.path.join("..", "semaphores", "films")
FILM_EXT = (".webm", ".mp4")
VIDEO_EXT = FILM_EXT + (".mov", ".m4v", ".mkv", ".ogv", ".avi", ".mpg", ".mpeg", ".m2ts", ".wmv", ".flv", ".3gp", ".vob",
                        ".divx", ".f4v", ".asf")
film_fails = []
def bad_film(msg):
    film_fails.append(msg); bad(msg)
def finder_file(folder, n):
    path = os.path.join(folder, n)
    return n == ".DS_Store" and os.path.isfile(path) and not os.path.islink(path)

# (a) The folder. Apart from a Finder .DS_Store file it holds exactly the ten sealed films, as regular files, under exactly
# those names (matched against the folder's own listing, so a case-only rename fails even on a case-insensitive disk;
# a symlink or a folder in a film's place fails), each with its sealed sha256 (the digests RELEASE-MANIFEST.md
# publishes for release 1.3.0). Neither semaphores/ nor semaphores/films/ may be a symlink.
for folder in (os.path.join("..", "semaphores"), FILMS_DIR):
    if os.path.islink(folder):
        bad_film(f"{folder} is a symlink: the films must sit in the repository's own folder")
if not os.path.isdir(FILMS_DIR):
    bad_film(f"{FILMS_DIR} is missing")
    present = []
else:
    present = sorted(n for n in os.listdir(FILMS_DIR) if not finder_file(FILMS_DIR, n))
for fn in present:
    if fn not in SEALED_FILMS:
        bad_film(f"unexpected entry in {FILMS_DIR}: {fn} (the folder may hold only the ten sealed films)")
for fn, h in sorted(SEALED_FILMS.items()):
    path = os.path.join(FILMS_DIR, fn)
    if fn not in present:
        bad_film(f"release film missing: {path}"); continue
    if os.path.islink(path) or not os.path.isfile(path):
        bad_film(f"{path} is not a regular file (a symlink or a folder in a film's place is not admitted)"); continue
    try:
        hf = hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError as e:
        bad_film(f"{path} cannot be read: {e}"); continue
    if hf != h:
        bad_film(f"{path}: sha256 {hf} != sealed {h}")

# (b) One copy. Under site/: no file with one of VIDEO_EXT, no symlinked folder, no folder that cannot be read, and
# nothing in a leftover assets/films folder but a Finder .DS_Store file.
def walk_error(e):
    bad_film(f"cannot read {getattr(e, 'filename', '?')} under site/: {e.__class__.__name__}")
for root, dirs, fs in os.walk(".", onerror=walk_error):
    for d in dirs:
        if os.path.islink(os.path.join(root, d)):
            bad_film(f"symlinked folder under site/: {os.path.join(root, d)} (nothing under site/ may be a symlinked folder)")
    for fn in fs:
        if fn.lower().endswith(VIDEO_EXT):
            bad_film(f"video file under site/: {os.path.join(root, fn)} (the site keeps no copy of the films)")
leftover = os.path.join("assets", "films")
if os.path.isdir(leftover) and not os.path.islink(leftover):
    try:
        extra = sorted(n for n in os.listdir(leftover) if not finder_file(leftover, n))
    except OSError:
        extra = ["(unreadable)"]
    if extra:
        bad_film(f"assets/films holds {', '.join(extra[:3])}{' and more' if len(extra) > 3 else ''}: remove the folder (the site keeps no copy of the films; they are served from ../semaphores/films)")
elif os.path.lexists(leftover):
    bad_film("assets/films is not a folder: remove it (the site keeps no copy of the films)")

# (c) The Makefile is sealed by its sha256, so its recipes, its folder line and its two lists are the reviewed text. A
# change to the Makefile must update SEALED_MAKEFILE here, as a style change updates the CSP hash.
SEALED_MAKEFILE = "d03e354d8a3de47e2ff02500a3322305f851b8e7952a3788710cb5aaebbbf6cb"
mk_bytes = open("Makefile", "rb").read()
mk_sha = hashlib.sha256(mk_bytes).hexdigest()
if mk_sha != SEALED_MAKEFILE:
    if hashlib.sha256(mk_bytes.replace(b"\r\n", b"\n")).hexdigest() == SEALED_MAKEFILE:
        bad_film("Makefile has CRLF line endings and is otherwise the sealed text: check it out with LF line endings (do not update the seal)")
    else:
        bad_film(f"Makefile differs from the sealed text: sha256 {mk_sha} != sealed {SEALED_MAKEFILE} (review the change, then update SEALED_MAKEFILE in verify.sh)")

# (d) Readable checks on the Makefile, for the day its seal is updated. They compare text (CRLF read as LF) and do not
# interpret make. The Makefile holds, verbatim and after a line that is not continued, the block that sets the folder
# and the two lists (EXPECTED_BLOCK: the sealed folder, then the five WebM and the five MP4 names in sorted order, one
# to a line). The names FILMS_DIR, FILMS_WEBM and FILMS_MP4 occur nowhere else in the file, comments included, except
# as $(NAME) or ${NAME}. No line begins with include, -include or sinclude, and 'eval' appears nowhere in the file. The
# file ends with the three lines that declare the Makefile never remade, after a line that is not continued. No
# GNUmakefile, makefile, Makefile.* sibling, RCS or SCCS sits beside the Makefile, in any letter case (make would read
# or rebuild from those). What the recipes do with the folder and the lists is not checked here: the seal alone guards
# the recipes.
mk = mk_bytes.decode("utf-8", "replace").replace("\r\n", "\n")
def listed(ext):
    return " \\\n".join("\t" + n for n in sorted(SEALED_FILMS) if n.endswith(ext)) + "\n"
EXPECTED_BLOCK = ("override FILMS_DIR := ../semaphores/films\n"
                  + "override FILMS_WEBM := \\\n" + listed(".webm")
                  + "override FILMS_MP4 := \\\n" + listed(".mp4"))
at = mk.find("\n" + EXPECTED_BLOCK)
if at < 0 or mk[max(at - 1, 0):at] == "\\":
    bad_film("Makefile must hold verbatim, after a line that is not continued, the block that sets FILMS_DIR to ../semaphores/films and lists the five WebM and the five MP4 films in sorted order, one to a line, as the sealed Makefile does")
for name in ("FILMS_DIR", "FILMS_WEBM", "FILMS_MP4"):
    count = mk.replace("$(" + name + ")", "").replace("${" + name + "}", "").count(name)
    if count != 1:
        bad_film(f"Makefile must name {name} once only, where it is set ($({name}) and ${{{name}}} references aside, comments included); found {count}")
if re.search(r"^[ \t]*(?:-|s)?include\b", mk, re.M):
    bad_film("Makefile must not include another makefile (no line may begin with include, -include or sinclude)")
if "eval" in mk:
    bad_film("Makefile must not contain 'eval' anywhere, comments included")
NEVER_REMADE = "\nMAKEFLAGS += -r\n.SUFFIXES:\nMakefile: ;\n"
if not mk.endswith(NEVER_REMADE) or mk[:-len(NEVER_REMADE)].endswith("\\"):
    bad_film("Makefile must end with the three lines 'MAKEFLAGS += -r', '.SUFFIXES:' and 'Makefile: ;', after a line that is not continued: they declare the Makefile never remade")
for other in sorted(n for n in os.listdir(".") if n != "Makefile" and n.lower() in ("gnumakefile", "makefile")):
    bad_film(f"{other} sits beside Makefile: GNU make would read it first, so the sealed Makefile would not be the one run")
for other in sorted(n for n in os.listdir(".") if n != "Makefile" and (n.lower().startswith("makefile.") or n.lower() in ("makefile,v", "rcs", "sccs", "s.makefile"))):
    bad_film(f"{other} sits beside Makefile: a sibling of that name could rebuild or replace it (make rebuilds a makefile from Makefile.sh and the like); remove it")

# (e) The pages. Python's html.parser reads each page. For every src or href attribute it reports on a start tag, the
# value is taken as a browser takes a URL: tab, newline and carriage return are removed, then control characters and
# spaces at both ends, then everything from the first ? or #. If what is left ends in .webm or .mp4 (in any letter
# case) or begins with /assets/films/, it must be exactly /assets/films/ followed by a sealed film's name. Prose and
# other attributes are not read. A page the parser cannot read fails.
from html.parser import HTMLParser
class FilmRefs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("src", "href") and v:
                self.refs.append((tag, k, v))
C0_AND_SPACE = "".join(map(chr, range(33)))
named = set()
for p in PAGES:
    film_refs = FilmRefs()
    try:
        film_refs.feed(open(p, encoding="utf-8").read())
        film_refs.close()
    except Exception as e:
        bad_film(f"{p}: the HTML parser could not read this page ({e.__class__.__name__}), so its film references are unchecked: repair the markup")
        continue
    for tag, k, v in film_refs.refs:
        path = re.split(r"[?#]", re.sub(r"[\t\n\r]", "", v).strip(C0_AND_SPACE), maxsplit=1)[0]
        if not (path.lower().endswith(FILM_EXT) or path.startswith("/assets/films/")):
            continue
        name = path[len("/assets/films/"):] if path.startswith("/assets/films/") else None
        if name in SEALED_FILMS:
            named.add(name)
        else:
            bad_film(f"{p}: <{tag} {k}={v!r}> is a film reference that is not exactly /assets/films/<a sealed film>")
if not film_fails:
    say(f"OK: {len(SEALED_FILMS)} films sealed by sha256 in ../semaphores/films (nothing else there but, at most, a Finder .DS_Store file); no file with one of the gate's video extensions under site/; the Makefile is the sealed text and sets exactly those ten; {len(named)} of them named by the pages")

# 6. Repo privacy gate: forbid tracking Research Artifacts, private_research_vault, transcripts, or sqlite/jsonl dumps in git.
# For the films: no file with one of VIDEO_EXT may be tracked outside semaphores/films/ (the repository holds the films
# once). Git's raw, NUL-separated paths are read. If git does not answer, these checks are skipped and the gate says so.
import subprocess
git_ok = True
try:
    tracked = [t for t in subprocess.check_output(["git", "ls-files", "-z"], cwd="..", stderr=subprocess.DEVNULL).decode("utf-8", "backslashreplace").split("\0") if t]
except Exception:
    tracked = []
    git_ok = False
FORBIDDEN_GIT = ("research artifacts/", "private_research_vault/", "wispr", "transcript", ".jsonl", ".sqlite", "doorbell")
PUBLIC_HANDOFF_TABLES = {
    "tools/handoff_art_colours.json",
    "tools/handoff_drafting_candidates.json",
}
git_fails = 0
for tf in tracked:
    if tf in PUBLIC_HANDOFF_TABLES:
        continue
    tfl = tf.lower()
    if any(tok in tfl for tok in FORBIDDEN_GIT):
        bad(f"forbidden private/dump path tracked in git: {tf}"); git_fails += 1
    if tfl.endswith(VIDEO_EXT) and not tf.startswith("semaphores/films/"):
        bad(f"video file tracked outside semaphores/films/: {tf} (the repository holds the films once)"); git_fails += 1
if not git_ok:
    say("SKIPPED: git ls-files did not answer here (not a repository, no git, or git refused): the tracked-files checks did not run")
elif git_fails == 0:
    say("OK: git tracked-files privacy gate clean; no file with one of the gate's video extensions tracked outside semaphores/films/")

if FAIL == 0:
    say("verify.sh: ALL CHECKS PASS")
    sys.exit(0)
else:
    say("verify.sh: FAILURES PRESENT")
    sys.exit(1)
PY
