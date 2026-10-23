#!/usr/bin/env python3
"""tools/generate_pdfs.py: typeset the two release PDFs of The Tetrasemaphore 1.0.0 from the approved sources.

Spec: Claude Science's PDF spec for release 1.0.0 (22 October 2026, 18:59Z, with its update of 19:00Z; the project's decision log, item 118).
Pipeline: source markdown -> pandoc (-f gfm -t typst) -> the Typst template below -> typst compile (PDF/A-2a).
Standard-library Python only. Every input is checked by sha256 before use and the run stops on the first mismatch.
Nothing is read from outside the release tree, the font folder and the build folder; nothing is written into the release tree.

The two PDFs:
  pdf/TETRASEMAPHORE-PUBLIC-NOTE.pdf      from README.md                                  (cover title: The Tetrasemaphore)
  pdf/TETRASEMAPHORE-METHODS-NOTE-01.pdf  from methods/tetrasemaphore-methods-note-01-rev1.md (cover title: the source's first line)

Usage (from anywhere):
  python3 tools/generate_pdfs.py --tree <release tree> --font-dir <folder with the seven DejaVu 2.37 files>
      --timestamp <unix epoch> (--doi 10.5281/zenodo.<n> | --doi-pending) [--suffix -PREVIEW]
      --build <build folder> --out <folder> [--out <another folder>]
The same inputs and timestamp give byte-identical PDFs.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys

PANDOC_VERSION = '3.9.0.2'
TYPST_VERSION = '0.14.2'

# Inputs by sha256 (release paths; the full hashes are the rows of the release manifest and the font files' own hashes).
SOURCES = {
    'README.md': ('c98c3ee4a94a3daee326e7a2c41bf9af700f775132555241536c0076a6420927', 23648),  # the public note, version 2 (Carey's approval, item 148; NOTE-V2-TEXT-PASS 1ab9ba1cf43bba71)
    'methods/tetrasemaphore-methods-note-01-rev1.md': ('46f436d9ef3a35ceceec395a4f86009e8bfa094fcf786fbb1e9da468b518cb05', 15308),
}
PNG_DIR = 'artwork/master/states/proposals/notation/final-masters-2026-10-05/png'
SEMAPHORES = [  # state word, bright colour (site --c-*-bright), transform line (site index.html figcaption), png sha256, bytes, alt text (site index.html, after the text pass of item 149)
    ('NORMATIVE', '#e5c97b', 'I : (x, y) \u2192 (x, y)', 'eacf65bc9181f649ff29d76011bc0cc759f3c9aacb01b0ab4875c764b2526438', 755820, 'The NORMATIVE semaphore'),
    ('NON-NORMATIVE', '#5ec4b6', '\u03c3\u1d65 : (x, y) \u2192 (\u2212x, y)', '658837bd2d2802b35b8a85f91fdd50d839471acf092f57e9f587589f42bc8db0', 720684, 'The NON-NORMATIVE semaphore'),
    ('METACOGNITIVE', '#c79ce8', '\u03c3\u2095 : (x, y) \u2192 (x, \u2212y)', '0f050e240c74e952fb475211b5a31657b832e374d9587656e7f76df085cc0de0', 721125, 'The METACOGNITIVE semaphore'),
    ('CRITICAL', '#e3746a', 'C\u2082 : (x, y) \u2192 (\u2212x, \u2212y)', 'a43da812ca3a7c885a4e688c978e6e4011c0996968b2411b6ca8a959a0ae2461', 757191, 'The CRITICAL semaphore'),
]
FONTS = {  # DejaVu 2.37, the files LibreOffice ships
    'DejaVuSerif.ttf': ('42d1edeb7952f31b1f96d767ed7030b08a39e0c372b0071641518864e2bffb51', 380132),
    'DejaVuSerif-Italic.ttf': ('2e39b1d50f90b933b00c7bb54a96afd3f86419b3d717c7cf202e36f2d4973e47', 345996),
    'DejaVuSerif-Bold.ttf': ('c47b5527bcdc8dcf9ea8c77054454c5a884beaca2f44851a2a823ee639cbf07f', 356088),
    'DejaVuSerif-BoldItalic.ttf': ('8d3dd3d31350309042ed226af82b34539bd773518e6107cb352712853ba80308', 347460),
    'DejaVuSans.ttf': ('7da195a74c55bef988d0d48f9508bd5d849425c1770dba5d7bfc6ce9ed848954', 757076),
    'DejaVuSans-Bold.ttf': ('e6476c1b80502924294eed40894c5b18e06c181444ca953e5334262df9c27724', 705684),
    'DejaVuSansMono.ttf': ('b4a6c3e4faab8773f4ff761d56451646409f29abedd68f05d38c2df667d3c582', 340712),
}

# The fixed strings of the spec's section 5, each with its source.
EYEBROW = 'Tetrasemaphore \u00b7 V\u2084 = {I, \u03c3\u1d65, \u03c3\u2095, C\u2082}'   # site/note.html, the eyebrow
AUTHOR = 'Carey James Balboa'                                                 # NOTICE; the creator
VERSION_LINE = 'Version 1.0.0'                                                # the release
HEADER_VERSION = '1.0.0'                                                      # the release
LICENCE = 'CC BY 4.0'                                                         # NOTICE; LICENSE
SITE = 'tetrasemaphore.systems'                                               # the site
SITE_URL = 'https://tetrasemaphore.systems/'
REPO = 'github.com/IT-Help-San-Diego/tetrasemaphore'                          # the repository
REPO_URL = 'https://github.com/IT-Help-San-Diego/tetrasemaphore'
PUBLIC_NOTE_MENU = 'Public note'                                              # the site's top menu
DOI_PENDING = 'DOI pending'                                                   # the spec's update of 19:00Z, for the preview only

DOCS = [
    {   # the public note
        'name': 'TETRASEMAPHORE-PUBLIC-NOTE',
        'source': 'README.md',
        'title': 'The Tetrasemaphore',                       # site/note.html h1; the Zenodo title
        'header_left': 'The Tetrasemaphore \u00b7 ' + PUBLIC_NOTE_MENU,
        'title_from_first_line': False,
    },
    {   # the methods note
        'name': 'TETRASEMAPHORE-METHODS-NOTE-01',
        'source': 'methods/tetrasemaphore-methods-note-01-rev1.md',
        'title': None,                                        # the source's first line, without its '# '
        'header_left': None,                                  # the source's title
        'title_from_first_line': True,
    },
]

# The Typst template. @@TOKENS@@ are replaced by this script; the body is pandoc's typst for the source.
TEMPLATE = r'''// The Tetrasemaphore 1.0.0: generated by tools/generate_pdfs.py from @@SOURCE_PATH@@ (sha256 @@SOURCE_SHA16@@). Do not edit.
#let ground = rgb("#0d1117")
#let fg = rgb("#e8e4dc")
#let gold = rgb("#d4a853")
#let muted = rgb("#9e998e")
#let ink = rgb("#1a1a1a")
#let h2col = rgb("#907238")
#let hdrcol = rgb("#5f5a50")
#let rulecol = rgb("#c9c2b4")
#let sans = "DejaVu Sans"
#let serif = "DejaVu Serif"
#let mono = "DejaVu Sans Mono"

#let title = "@@TITLE@@"
#let header-left = "@@HEADER_LEFT@@"
#let doi-text = "@@DOI_TEXT@@"
#let doi-url = "@@DOI_URL@@"
#let cite-tail = "@@CITE_TAIL@@"
#let doi-link(body) = if doi-url == "" { body } else { link(doi-url, body) }

#set document(title: title, author: "@@AUTHOR@@")
#set text(font: serif, size: 10pt, lang: "en", fill: ink, fallback: false, hyphenate: false)
#set par(justify: false, leading: 0.74em, spacing: 1.0em)  // 15 pt baseline to baseline at 10 pt (the line box runs cap height to baseline)
#set page(paper: "us-letter", margin: (left: 72pt, right: 72pt, top: 80pt, bottom: 72pt))
#set table(stroke: (x, y) => (bottom: 0.5pt + rulecol), inset: (x: 5pt, y: 4pt))
#set table.hline(stroke: 0.5pt + rulecol)
#set table.header(repeat: false)
#show table.cell: set align(left + top)
#show table.cell.where(y: 0): strong
#show table: set text(size: 9pt)
#show table: set par(leading: 0.42em)
#show figure.where(kind: table): set block(breakable: true)
#show raw: set text(font: mono, size: 1.15em)  // Typst sets inline raw at 0.8 em of its surroundings; 0.8 x 1.15 = 0.92 em
#show quote.where(block: true): it => block(above: 1.2em, below: 1.2em, inset: (left: 1em), stroke: (left: 2pt + gold), it.body)
#show heading.where(level: 2): it => block(above: 1.8em, below: 0.9em)[#box(height: 0.75em, align(horizon, rotate(45deg, reflow: true, square(size: 5pt, stroke: 0.75pt + gold))))#h(0.55em)#text(font: sans, weight: "bold", size: 10.5pt, tracking: 0.06em, fill: h2col, upper(it.body))]
#show heading.where(level: 3): it => block(above: 1.5em, below: 0.6em, text(font: sans, weight: "bold", size: 10pt, fill: ink, it.body))
#show regex("\\b(?:NON-NORMATIVE|NON-NORMATIVO|NORMATIVE|NORMATIVO|METACOGNITIVE|METACOGNITIVO|INFORMATIVO|CRITICAL|CRÍTICO)\\b"): it => box(it)
#let horizontalrule = block(sticky: true, above: 1.4em, below: 1.4em, context { if here().position().y > 81pt { line(length: 100%, stroke: 0.5pt + rulecol) } })  // not drawn at a page top

// Page 1: the cover, dark like the site.
#let state(word, colour) = align(center, box(text(font: sans, weight: "bold", size: 8.5pt, tracking: 0.08em, fill: rgb(colour), word)))
#let transform(line) = align(center, text(font: mono, size: 7.5pt, fill: fg, line))
#page(fill: ground, header: none, footer: none)[
  #set text(fill: fg)
  #show link: it => underline(text(fill: gold, it))
  #show heading.where(level: 1): it => block(above: 0pt, below: 0pt, text(font: sans, weight: "bold", size: 28pt, fill: fg, it.body))
  #text(font: sans, weight: "bold", size: 9pt, tracking: 0.14em, fill: gold)[@@EYEBROW@@]
  #v(16pt)
  #heading(level: 1, title)
  #v(30pt)
  #grid(columns: (36mm, 36mm, 36mm, 36mm), column-gutter: 7mm, row-gutter: 6pt,
@@SEMAPHORE_ROW@@
  )
  #v(1fr)
  #set par(leading: 0.5em, spacing: 0.5em)
  #text(font: sans, weight: "bold", size: 11pt, fill: fg)[@@AUTHOR@@]

  #text(font: sans, size: 9pt, fill: fg)[@@VERSION_LINE@@]

  #text(font: sans, size: 9pt, fill: fg)[#doi-link(doi-text)]

  #text(font: sans, size: 9pt, fill: fg)[@@LICENCE@@]

  #text(font: sans, size: 9pt, fill: fg)[#link("@@SITE_URL@@")[@@SITE@@] · #link("@@REPO_URL@@")[@@REPO@@]]
  #v(12pt)
  #text(font: sans, size: 8pt, fill: muted)[Cite as: Balboa, C. J. (2026). The Tetrasemaphore (Version 1.0.0). Zenodo. #doi-link(cite-tail)]
]

// Pages 2 onward: white, for reading and printing.
#set page(fill: white,
  header: context {
    set text(font: sans, size: 8pt, fill: hdrcol)
    grid(columns: (1fr, auto), align: (left, right), header-left, "@@HEADER_VERSION@@")
    v(-3pt)
    line(length: 100%, stroke: 0.5pt + gold)
  },
  footer: context {
    set text(font: sans, size: 8pt, fill: hdrcol)
    grid(columns: (1fr, 1fr, 1fr), align: (left, center, right), doi-text, counter(page).display("1 / 1", both: true), "@@LICENCE@@")
  })

#show link: it => underline(text(fill: h2col, it))  // pages 2 onward; the cover above has its own rule (gold)

@@BODY@@

// The colophon.
#v(2.4em)
#line(length: 100%, stroke: 0.5pt + rulecol)
#v(0.6em)
#text(font: sans, size: 8pt, fill: hdrcol)[This PDF was typeset from #raw("@@SOURCE_PATH@@") (sha256 #raw("@@SOURCE_SHA16@@")) by #raw("tools/generate_pdfs.py"), with pandoc @@PANDOC_VERSION@@ and Typst @@TYPST_VERSION@@, as PDF/A-2a. Fonts: DejaVu Serif, DejaVu Sans and DejaVu Sans Mono 2.37 (Bitstream Vera licence; DejaVu\'s changes are in the public domain). The semaphore pictures are the four 1298-pixel renders in #raw("@@PNG_DIR@@/"). The text and the art are licensed under CC BY 4.0, and the code under Apache 2.0 (see NOTICE).]
'''


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check(path, expected, size, label):
    if not os.path.isfile(path):
        sys.exit('STOP: %s missing: %s' % (label, path))
    actual, actual_size = sha256(path), os.path.getsize(path)
    if actual != expected or actual_size != size:
        sys.exit('STOP: %s differs from the record: %s\n  expected %s %d\n  found    %s %d' % (label, path, expected, size, actual, actual_size))
    return actual


def tool_version(exe, name, expected, allow_other):
    try:
        out = subprocess.run([exe, '--version'], capture_output=True, encoding='utf-8', check=True).stdout.strip().splitlines()[0]
    except (OSError, subprocess.CalledProcessError, IndexError) as e:
        sys.exit('STOP: %s cannot be run as %r: %s' % (name, exe, e))
    ver = out.split()[1] if out.lower().startswith(name) else out
    if ver != expected and not allow_other:
        sys.exit('STOP: %s is %s; the spec names %s (pass --allow-other-versions to go on)' % (name, ver, expected))
    return ver


def typst_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tree', default=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')), help='the release tree (default: the parent of this file\'s folder)')
    ap.add_argument('--font-dir', required=True, help='folder holding the seven DejaVu 2.37 files')
    ap.add_argument('--timestamp', required=True, type=int, help='unix epoch used as the PDFs\' creation date (recorded; a rebuild with it is byte-identical)')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--doi', help='the reserved DOI, as 10.5281/zenodo.<n>')
    g.add_argument('--doi-pending', action='store_true', help='preview: the string "DOI pending" wherever the DOI goes, with no link')
    ap.add_argument('--suffix', default='', help='appended to the PDF names, e.g. -PREVIEW')
    ap.add_argument('--build', required=True, help='build folder: the .typ files, the copied pictures and the report')
    ap.add_argument('--out', action='append', required=True, help='output folder for the PDFs (repeatable; every copy is the same bytes)')
    ap.add_argument('--pandoc', default='pandoc'); ap.add_argument('--typst', default='typst')
    ap.add_argument('--allow-other-versions', action='store_true')
    A = ap.parse_args()

    if A.doi and not re.fullmatch(r'10\.5281/zenodo\.[0-9]+', A.doi):
        sys.exit('STOP: the DOI must be 10.5281/zenodo.<n> with n digits only; got %r' % A.doi)
    if A.doi_pending and not A.suffix.strip():
        sys.exit('STOP: a render with "DOI pending" is a preview: pass --suffix -PREVIEW')

    report = {'tree': os.path.abspath(A.tree), 'font_dir': os.path.abspath(A.font_dir), 'timestamp': A.timestamp,
              'doi': A.doi or DOI_PENDING, 'suffix': A.suffix, 'inputs': [], 'tools': {}, 'outputs': []}

    # 1. Tools.
    report['tools']['pandoc'] = tool_version(A.pandoc, 'pandoc', PANDOC_VERSION, A.allow_other_versions)
    report['tools']['typst'] = tool_version(A.typst, 'typst', TYPST_VERSION, A.allow_other_versions)

    # 2. Inputs by hash.
    for rel, (h, n) in SOURCES.items():
        report['inputs'].append({'path': rel, 'sha256': check(os.path.join(A.tree, rel), h, n, 'source'), 'bytes': n})
    for word, colour, line, h, n, alt in SEMAPHORES:
        rel = '%s/TETRASEMAPHORE-%s-en-1298.png' % (PNG_DIR, word)
        report['inputs'].append({'path': rel, 'sha256': check(os.path.join(A.tree, rel), h, n, 'picture'), 'bytes': n})
    for fn, (h, n) in FONTS.items():
        report['inputs'].append({'path': 'font:' + fn, 'sha256': check(os.path.join(A.font_dir, fn), h, n, 'font'), 'bytes': n})
    extra = sorted(e for e in os.listdir(A.font_dir) if e not in FONTS and not e.startswith('.'))  # any other entry, file or folder: typst would search it
    if extra:
        sys.exit('STOP: the font folder holds entries beyond the seven: %s' % ', '.join(extra))

    os.makedirs(A.build, exist_ok=True)
    for out in A.out:
        os.makedirs(out, exist_ok=True)

    doi_text = ('DOI ' + A.doi) if A.doi else DOI_PENDING
    doi_url = ('https://doi.org/' + A.doi) if A.doi else ''
    cite_tail = doi_url if A.doi else DOI_PENDING

    for doc in DOCS:
        src_rel = doc['source']; src = os.path.join(A.tree, src_rel)
        src_sha = SOURCES[src_rel][0]
        with open(src, 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != src_sha:  # the bytes read are the bytes checked
            sys.exit('STOP: %s changed between the check and the read' % src_rel)
        text = raw.decode('utf-8')
        if doc['title_from_first_line']:
            first, _, rest = text.partition('\n')
            if not first.startswith('# '):
                sys.exit('STOP: %s does not start with a level-1 heading' % src_rel)
            title = first[2:].strip(); body_md = rest.lstrip('\n')
        else:
            title = doc['title']; body_md = text
        header_left = doc['header_left'] or title

        bdir = os.path.join(A.build, doc['name']); os.makedirs(bdir, exist_ok=True)
        for word, colour, line, h, n, alt in SEMAPHORES:   # the pictures, copied into the build folder (typst reads inside its root only)
            dst = os.path.join(bdir, 'semaphore-%s.png' % word)
            shutil.copyfile(os.path.join(A.tree, PNG_DIR, 'TETRASEMAPHORE-%s-en-1298.png' % word), dst)
            if sha256(dst) != h:
                sys.exit('STOP: the copy of the %s picture differs' % word)

        # 3. pandoc: the body.
        md_path = os.path.join(bdir, 'body.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(body_md)
        p = subprocess.run([A.pandoc, '-f', 'gfm', '-t', 'typst', '--wrap=none', md_path], capture_output=True, encoding='utf-8')  # utf-8 whatever the locale
        if p.returncode != 0:
            sys.exit('STOP: pandoc failed on %s:\n%s' % (src_rel, p.stderr))
        body = p.stdout

        # 4. The .typ: the template, then the body.
        images = ''.join('    image("semaphore-%s.png", width: 36mm, alt: "%s"),\n' % (w, typst_string(alt)) for w, c, l, h, n, alt in SEMAPHORES)
        words = ''.join('    state("%s", "%s"),\n' % (w, c) for w, c, l, h, n, alt in SEMAPHORES)
        lines = ''.join('    transform("%s"),\n' % typst_string(l) for w, c, l, h, n, alt in SEMAPHORES)
        rep = {
            '@@SOURCE_PATH@@': src_rel, '@@SOURCE_SHA16@@': src_sha[:16], '@@TITLE@@': typst_string(title),
            '@@HEADER_LEFT@@': typst_string(header_left), '@@HEADER_VERSION@@': HEADER_VERSION,
            '@@DOI_TEXT@@': doi_text, '@@DOI_URL@@': doi_url, '@@CITE_TAIL@@': cite_tail,
            '@@AUTHOR@@': AUTHOR, '@@EYEBROW@@': EYEBROW, '@@VERSION_LINE@@': VERSION_LINE, '@@LICENCE@@': LICENCE,
            '@@SITE@@': SITE, '@@SITE_URL@@': SITE_URL, '@@REPO@@': REPO, '@@REPO_URL@@': REPO_URL,
            '@@SEMAPHORE_ROW@@': (images + words + lines).rstrip('\n'),
            '@@PANDOC_VERSION@@': report['tools']['pandoc'], '@@TYPST_VERSION@@': report['tools']['typst'], '@@PNG_DIR@@': PNG_DIR,
            '@@BODY@@': body.rstrip('\n'),
        }
        typ = TEMPLATE
        for k, v in rep.items():
            typ = typ.replace(k, v)
        if '@@' in typ:
            sys.exit('STOP: a template token was not filled')
        typ_name = doc['name'] + '.typ'
        with open(os.path.join(bdir, typ_name), 'w', encoding='utf-8') as f:
            f.write(typ)

        # 5. typst compile, PDF/A-2a, the seven fonts only, the recorded timestamp.
        pdf_name = doc['name'] + A.suffix + '.pdf'
        cmd = [A.typst, 'compile', '--root', bdir, '--ignore-system-fonts', '--ignore-embedded-fonts', '--font-path', os.path.abspath(A.font_dir),
               '--pdf-standard', 'a-2a', '--creation-timestamp', str(A.timestamp), typ_name, pdf_name]
        t = subprocess.run(cmd, cwd=bdir, capture_output=True, encoding='utf-8', errors='replace')
        if t.returncode != 0:
            sys.exit('STOP: typst failed on %s:\n%s' % (typ_name, t.stderr))
        built = os.path.join(bdir, pdf_name)
        out_sha = sha256(built)
        report['outputs'].append({'pdf': pdf_name, 'sha256': out_sha, 'bytes': os.path.getsize(built), 'typ_sha256': sha256(os.path.join(bdir, typ_name)),
                                  'source': src_rel, 'title': title, 'built': built, 'copies': [], 'typst_stderr': t.stderr.strip(),
                                  'command': ' '.join(cmd)})
        print('%s  %d bytes  sha256 %s  <- %s' % (pdf_name, os.path.getsize(built), out_sha[:16], src_rel))

    # 6. Both built: now the copies into every --out folder (nothing is copied if either PDF failed).
    for o in report['outputs']:
        for out in A.out:
            dst = os.path.join(out, o['pdf'])
            shutil.copyfile(o['built'], dst)
            if sha256(dst) != o['sha256']:
                sys.exit('STOP: the copy at %s differs' % dst)
            o['copies'].append(dst)

    with open(os.path.join(A.build, 'generate-report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print('report: %s' % os.path.join(A.build, 'generate-report.json'))


if __name__ == '__main__':
    main()
