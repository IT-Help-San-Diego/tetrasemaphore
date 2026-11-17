#!/usr/bin/env python3
"""
make_datasheet_html.py: one HTML page per semaphore datasheet, generated from audit_<STATE>.json.

Why: the datasheet plates are 2400 x 1500 px pictures whose smallest type is 14 px, about 2.2 px on a
375 px phone. The audit record the plate build writes already holds the plate's quotations, values,
sources and measurements as data. This script lays that record out as a page that reflows on a phone,
whose text can be selected, searched and read by a screen reader, and in which every station has its
own address, taken from the record's own name for it (the callout's "key"):
datasheet-metacognitive.html#fix, datasheet-critical.html#mark.

The rule it carries:
  every word and number a reader sees is read from the audit record at build time, or is one of the
  labels declared in tools/datasheet_html_labels.json. Nothing else is typed here. Each element that
  shows a record value names the field it shows in a data-audit attribute (a JSON Pointer into the
  record), so tools/check_datasheet_html.py can read the page back against the record. Numbers are
  printed as the record writes them, with no re-rounding. A field the page needs and the record lacks
  stops the build before anything is written.

What it does not render: the record's "drafting" block (it describes the plate's leader lines, badges
and axis, which a reflowed page does not have), its "audit" block and its plate geometry. They stay in
the record, which the page links.

The page's look is the site's own: the single <style> block, the Content-Security-Policy meta line and
the social-card lines are copied from site/index.html at build time, byte for byte, so the pages add no
new style hash to the site's policy and follow index.html whenever it changes. Zero script, no external
subresource, no style attribute. Colour swatches are inline SVG with a fill attribute read from the record.

Output is a function of its inputs only (the audit records, site/index.html, the labels file, this
script): no clock, no environment. A rebuild is byte-identical.

Usage:
  python3 -I tools/make_datasheet_html.py            write site/datasheet-<state>.html from docs/datasheet-audit
  python3 -I tools/make_datasheet_html.py --verify   regenerate and compare with the written pages; exit 1 on a difference
  python3 -I tools/make_datasheet_html.py --audit-dir DIR --out-dir DIR [--site DIR] [--state NAME ...]
"""
import argparse, base64, hashlib, html, json, os, re, sys

STATES = ['NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL']
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
LABELS_FILE = os.path.join(TOOLS, 'datasheet_html_labels.json')

# index.html's own class names for the four states (they select the state colour in its style block)
STATE_CLASS = {'NORMATIVE': 'norm', 'NON-NORMATIVE': 'nonnorm', 'METACOGNITIVE': 'meta', 'CRITICAL': 'crit'}
# where a state's name may wrap in the page title when a phone is too narrow for it at title size.
# The characters are the record's; only a line-break opportunity is added.
STATE_BREAKS = {'METACOGNITIVE': ('META', 'COGNITIVE'), 'NON-NORMATIVE': ('NON-', 'NORMATIVE')}
# the standfirst the page shows: the whole sentence ('unelided') or what the plate draws ('text')
STANDFIRST_SHOWS = 'unelided'
ELLIPSIS = '\u2026'
# where the repository keeps the files the page links
AUDIT_REPO_DIR = 'docs/datasheet-audit/'
SHEET_REPO_DIR = 'site/assets/'
HERO_PX = 256          # the semaphore at the top: 256 CSS px, so it fits a 320 px phone with the site's gutters
# the ids the page uses for its own parts; a station's id is its callout's key, and may not be one of these
PAGE_IDS = {'main', 'semaphore', 'stations', 'absent', 'absent-title', 'chart', 'chart-title', 'scale',
            'palette', 'palette-title', 'sources', 'record', 'datasheets'}


def page_name(state):
    return f'datasheet-{state.lower()}.html'


def stop(msg):
    raise SystemExit(f'make_datasheet_html: {msg}; nothing written')


class Num(str):
    """A JSON number, kept as the characters the record writes."""


class Record:
    """One audit record, read once. at() stops the build when a field is missing."""

    def __init__(self, path):
        if not os.path.exists(path):
            stop(f'no audit record at {path}')
        raw = open(path, 'rb').read()
        self.path, self.name = path, os.path.basename(path)
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self.data = json.loads(raw.decode('utf-8'), parse_float=Num, parse_int=Num)

    def _walk(self, pointer):
        cur = self.data
        for part in pointer.strip('/').split('/'):
            if isinstance(cur, list):
                cur = cur[int(part)]
            elif isinstance(cur, dict):
                cur = cur[part]
            else:
                raise KeyError(part)
        return cur

    def has(self, pointer):
        try:
            self._walk(pointer)
            return True
        except (KeyError, IndexError, ValueError):
            return False

    def at(self, pointer):
        try:
            return self._walk(pointer)
        except (KeyError, IndexError, ValueError):
            stop(f'{self.name} has no field {pointer}')


# --------------------------------------------------------------- text kit ---
def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


AFTER, BEFORE = '/_-.,;:=)]', '([@#'


def soft(s, code=False):
    """HTML for a record string, with <wbr> line-break opportunities in long unbroken tokens so a
    file name, a hash or a field path wraps on a phone instead of widening the page. No character
    is added or removed: the element's text is still the record's string. Prose breaks only after
    punctuation; file names, hashes and paths (code=True) also break every eight characters."""
    out = []
    for tok in re.split(r'(\s+)', s):
        if not tok:
            continue
        if tok.isspace() or len(tok) <= 12:
            out.append(esc(tok))
            continue
        run, n = 0, len(tok)
        for i, ch in enumerate(tok):
            if 0 < i and ch in BEFORE and run:
                out.append('<wbr>')
                run = 0
            out.append(esc(ch))
            run += 1
            if i < n - 1 and (ch in AFTER or (code and run >= 8)):
                out.append('<wbr>')
                run = 0
    return ''.join(out)


class Page:
    def __init__(self, state, rec, labels, chrome, site_dir):
        self.state, self.rec, self.labels, self.chrome, self.site = state, rec, labels, chrome, site_dir
        if rec.at('/state') != state:
            stop(f"{rec.name} is the record of {rec.at('/state')!r}, not of {state}")

    # ---- labels: every word that is not the record's
    def T(self, key):
        try:
            return esc(self.labels['text'][key])
        except KeyError:
            stop(f'the labels file declares no text label {key!r}')

    def A(self, key):
        try:
            return attr(self.labels['aria'][key])
        except KeyError:
            stop(f'the labels file declares no aria label {key!r}')

    def link(self, key):
        try:
            return self.labels['links'][key]
        except KeyError:
            stop(f'the labels file declares no link {key!r}')

    def template(self, key, **kw):
        try:
            return self.labels['templates'][key].format(**kw)
        except KeyError:
            stop(f'the labels file declares no template {key!r}')

    # ---- the record's own words and numbers
    def value(self, pointer):
        v = self.rec.at(pointer)
        if isinstance(v, bool):
            key = pointer.rsplit('/', 1)[-1]
            try:
                return self.labels['booleans'][key]['true' if v else 'false']
            except KeyError:
                stop(f'the labels file declares no wording for the boolean {key!r}')
        if not isinstance(v, str):          # Num is a str; lists, objects and null are not shown as one value
            stop(f'{self.rec.name}: {pointer} is not a string, a number or a boolean')
        if not v.strip():
            stop(f'{self.rec.name}: {pointer} is empty')
        return v

    def D(self, pointer, tag='span', code=False, extra=''):
        """An element that shows one record field and says which."""
        return f'<{tag} data-audit="{attr(pointer)}"{extra}>{soft(self.value(pointer), code)}</{tag}>'

    def C(self, pointer):
        return self.D(pointer, 'code', code=True)

    def swatch(self, colour, pointer):
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', colour):
            stop(f'{self.rec.name}: {pointer} holds {colour!r}, not a #RRGGBB colour')
        return (f'<svg data-audit-fill="{attr(pointer)}" width="18" height="18" viewBox="0 0 18 18" '
                f'aria-hidden="true" focusable="false"><rect x="1" y="1" width="16" height="16" '
                f'fill="{colour}" stroke="currentColor"/></svg>')

    def swatches(self, pointer):
        """One swatch per colour a value line states, so a stated colour is visible (spec 3.4)."""
        seen, out = set(), []
        for h in re.findall(r'#[0-9A-Fa-f]{6}(?![0-9A-Fa-f])', self.value(pointer)):
            if h.upper() not in seen:
                seen.add(h.upper())
                out.append(' ' + self.swatch(h, pointer))
        return ''.join(out)

    def source(self, base):
        """Where a line comes from: file, sha16 and field, and how the sheet presents it when the record says."""
        rows = [('file', self.C(base + '/source')), ('sha16', self.C(base + '/sha16')),
                ('field', self.C(base + '/field'))]
        if self.rec.has(base + '/kind'):
            rows.append(('kind', self.D(base + '/kind')))
        items = ''.join(f'<dt>{self.T(k)}</dt><dd>{v}</dd>' for k, v in rows)
        return f'<details><summary>{self.T("source")}</summary><dl>{items}</dl></details>'

    # ---- the parts of the page
    def head(self):
        c, origin = self.chrome, self.chrome['origin']
        title = self.template('title', state=self.rec.at('/state'))
        desc = self.value(self.standfirst_pointer())
        url = origin + page_name(self.state)
        return '\n'.join([
            '<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            c['csp'],
            f'<title>{esc(title)}</title>',
            f'<meta name="description" content="{attr(desc)}">',
            '<meta property="og:type" content="article">',
            c['og:site_name'],
            f'<meta property="og:title" content="{attr(title)}">',
            f'<meta property="og:description" content="{attr(desc)}">',
            f'<meta property="og:url" content="{attr(url)}">',
            c['og:image'], c['og:image:alt'], c['og:image:type'], c['og:image:width'], c['og:image:height'],
            c['twitter:card'],
            f'<meta name="twitter:title" content="{attr(title)}">',
            f'<meta name="twitter:description" content="{attr(desc)}">',
            c['twitter:image'], c['twitter:image:alt'],
            f'<link rel="canonical" href="{attr(url)}">',
            c['icon'],
            f"<style>{c['style']}</style>",
            '</head>'])

    def title(self):
        """The page's h1, first thing in main and outside any section, as method.html and 404.html
        have theirs: at the browser's own h1 size the longest unbroken word, NORMATIVE, measures
        about 240 px, inside the 266 px a 320 px phone leaves."""
        name = self.value('/state')
        parts = STATE_BREAKS.get(name)
        inner = '<wbr>'.join(esc(p) for p in parts) if parts and ''.join(parts) == name else esc(name)
        return f'<h1><span data-audit="/state">{inner}</span> {self.T("datasheet")}</h1>'

    def standfirst_pointer(self):
        if STANDFIRST_SHOWS == 'unelided':
            if self.rec.has('/standfirst/unelided'):
                return '/standfirst/unelided'
            # a record written before the plate elided anything: its text is the whole sentence
            if ELLIPSIS in self.rec.at('/standfirst/text'):
                stop(f'{self.rec.name}: the standfirst is elided and the record holds no unelided sentence')
        return '/standfirst/text'

    def header(self):
        formula = self.D('/notation', extra=' class="formula"')
        return '\n'.join([
            f'<a class="skip" href="#main">{self.T("skip")}</a>',
            '<header class="site">',
            f'  <p class="eyebrow">{self.T("eyebrow")} {formula}</p>',
            f'  <nav class="top" aria-label="{self.A("nav_site")}">',
            f'    <a href="{attr(self.link("home"))}">{self.T("nav_home")}</a>',
            f'    <a href="{attr(self.link("note"))}">{self.T("nav_note")}</a>',
            f'    <a href="{attr(self.link("method"))}">{self.T("nav_method")}</a>',
            f'    <a href="{attr(self.link("repository"))}">{self.T("nav_repository")}</a>',
            '  </nav>', '</header>'])

    def semaphore(self):
        png = self.value('/sources/site_png/file')
        if not png.endswith('-1298.png'):
            stop(f'{self.rec.name}: /sources/site_png/file is {png!r}, not a -1298.png site asset')
        small = png[:-len('-1298.png')] + '-512.png'
        for f in (png, small):
            if not os.path.exists(os.path.join(self.site, 'assets', f)):
                stop(f'site/assets/{f} is not there')
        have = hashlib.sha256(open(os.path.join(self.site, 'assets', png), 'rb').read()).hexdigest()[:16]
        if have != self.rec.at('/sources/site_png/sha16'):
            stop(f"site/assets/{png} is {have}, and {self.rec.name} cites {self.rec.at('/sources/site_png/sha16')}")
        alt = self.template('alt', state=self.rec.at('/state'))
        sf = self.standfirst_pointer()
        return '\n'.join([
            '<section id="semaphore">',
            f'  <p><a href="/assets/{attr(png)}"><img src="/assets/{attr(small)}" width="{HERO_PX}" '
            f'height="{HERO_PX}" alt="{attr(alt)}"></a></p>',
            f'  <blockquote><p data-audit="{sf}">{soft(self.value(sf))}</p></blockquote>',
            '  ' + self.source('/standfirst'),
            '</section>'])

    def station(self, i):
        b = f'/callouts/{i}'
        n = self.value(b + '/n')
        if not n.isdigit():
            stop(f'{self.rec.name}: {b}/n is {n!r}, not a station number')
        # the station's address is the record's own name for it, so a link to one station means the
        # same part on every sheet (#fix, #mark) whatever its number there
        key = self.value(b + '/key')
        if not re.fullmatch(r'[a-z][a-z0-9-]*', key) or key in PAGE_IDS or key + '-title' in PAGE_IDS or key in self.keys:
            stop(f'{self.rec.name}: {b}/key is {key!r}, which cannot serve as this station\'s id '
                 f'(not a plain lower-case name, used twice, or one of the page\'s own ids)')
        self.keys.append(key)
        values = self.rec.at(b + '/values')
        if not isinstance(values, list) or not values:
            stop(f'{self.rec.name}: {b}/values holds no value line')
        out = [f'  <article class="panel" id="{key}" aria-labelledby="{key}-title">',
               f'    <h3 id="{key}-title">{self.D(b + "/n")} {self.D(b + "/title")}</h3>', '    <ul>']
        for j in range(len(values)):
            v = f'{b}/values/{j}'
            out.append(f'      <li>{self.D(v + "/text")}{self.swatches(v + "/text")}{self.source(v)}</li>')
        out.append('    </ul>')
        for slot in ('meaning', 'check'):
            s = f'{b}/{slot}'
            out.append(f'    <p><strong>{self.T(slot)}</strong> {self.D(s + "/text")}</p>')
            out.append('    ' + self.source(s))
        out.append('  </article>')
        return '\n'.join(out)

    def stations(self):
        callouts = self.rec.at('/callouts')
        count = self.value('/stations')
        if not isinstance(callouts, list) or str(len(callouts)) != count:
            stop(f'{self.rec.name}: /stations says {count} and /callouts holds '
                 f'{len(callouts) if isinstance(callouts, list) else "no list"}')
        self.keys = []
        out = ['<section id="stations">',
               f'  <h2>{self.D("/stations")} {self.T("stations")}</h2>',
               f'  <div class="sema {STATE_CLASS[self.state]} strip">']
        out += [self.station(i) for i in range(len(callouts))]
        if self.rec.at('/absent') is not None:
            out += ['  <article class="panel wide" id="absent" aria-labelledby="absent-title">',
                    f'    <h3 id="absent-title">{self.D("/absent/title")}</h3>',
                    f'    <p>{self.D("/absent/text")}</p>', '    ' + self.source('/absent'),
                    f'    <p>{self.D("/absent/note/text")}</p>', '    ' + self.source('/absent/note'),
                    '  </article>']
        out += ['  </div>', '</section>']
        return '\n'.join(out)

    def chart(self):
        rows = self.rec.at('/chart/rows')
        if not isinstance(rows, list) or not rows:
            stop(f'{self.rec.name}: /chart/rows holds no row')
        title = self.D('/chart/title', 'h2', extra=' id="chart-title"')
        out = ['<section id="chart">', '  ' + title,
               '  <table class="cay" aria-labelledby="chart-title">',
               f'    <thead><tr><th scope="col">{self.T("move")}</th><th scope="col">{self.T("overlap")}</th></tr></thead>',
               '    <tbody>']
        for i in range(len(rows)):
            r = f'/chart/rows/{i}'
            out.append(f'    <tr><th scope="row">{self.D(r + "/move")}<br>{self.D(r + "/is_own")}</th>'
                       f'{self.D(r + "/iou", "td")}</tr>')
        out += ['    </tbody>', '  </table>',
                f'  <dl><dt>{self.T("measured_at_px")}</dt>{self.D("/chart/measured_at_px", "dd")}'
                f'<dt>{self.T("mm_per_px")}</dt>{self.D("/chart/mm_per_px", "dd")}</dl>',
                '  ' + self.source('/chart'), '</section>']
        return '\n'.join(out)

    def scale(self):
        src = (f'<details><summary>{self.T("source")}</summary><dl><dt>{self.T("file")}</dt>'
               f'<dd>{self.C("/scale/source")}</dd><dt>{self.T("sha16")}</dt><dd>{self.C("/scale/sha16")}</dd></dl></details>')
        return '\n'.join([
            '<section id="scale">', f'  <h2>{self.T("scale")}</h2>',
            f'  <dl><dt>{self.T("u_per_mm")}</dt>{self.D("/scale/u_per_mm", "dd")}'
            f'<dt>{self.T("print_diameter_mm")}</dt>{self.D("/scale/print_diameter_mm", "dd")}'
            f'<dt>{self.T("derived_from")}</dt>{self.D("/scale/derived_from", "dd")}</dl>',
            '  ' + src, '</section>'])

    def palette(self):
        roles = self.rec.at('/sheet/palette')
        if not isinstance(roles, dict) or not roles:
            stop(f'{self.rec.name}: /sheet/palette holds no colour')
        out = ['<section id="palette">', f'  <h2 id="palette-title">{self.T("palette")}</h2>',
               f'  <p><strong>{self.T("ground")}</strong> {self.swatch(self.value("/sheet/ground"), "/sheet/ground")} '
               f'{self.C("/sheet/ground")}</p>',
               '  <table class="cay" aria-labelledby="palette-title">',
               f'    <thead><tr><th scope="col">{self.T("colour")}</th><th scope="col">{self.T("contrast")}</th></tr></thead>',
               '    <tbody>']
        for role in roles:
            p = f'/sheet/palette/{role}'
            out.append(f'    <tr><th scope="row">{self.T("role_" + role)}<br>{self.swatch(self.value(p), p)} {self.D(p)}</th>'
                       f'<td>{self.D("/sheet/contrast_on_ground/" + role)}{self.T("to_one")}</td></tr>')
        below = self.rec.at('/sheet/contrast_below_floor')
        if not isinstance(below, list):
            stop(f'{self.rec.name}: /sheet/contrast_below_floor is not a list')
        if below:
            listed = ''.join(f'<dd>{self.D(f"/sheet/contrast_below_floor/{i}/role")} '
                             f'{self.C(f"/sheet/contrast_below_floor/{i}/colour")} '
                             f'{self.D(f"/sheet/contrast_below_floor/{i}/ratio")}{self.T("to_one")}</dd>'
                             for i in range(len(below)))
        else:
            listed = f'<dd>{self.T("none")}</dd>'
        out += ['    </tbody>', '  </table>',
                f'  <dl><dt>{self.T("contrast_floor")}</dt><dd>{self.D("/sheet/contrast_floor")}{self.T("to_one")}</dd>'
                f'<dt>{self.T("below_floor")}</dt>{listed}</dl>', '</section>']
        return '\n'.join(out)

    def sources(self):
        out = ['<section id="sources">', f'  <h2>{self.T("sources")}</h2>', '  <dl>']
        for key in ('master', 'note', 'measurements', 'lean', 'site_png'):
            b = f'/sources/{key}'
            hashes = [h for h in ('sha256', 'sha16') if self.rec.has(f'{b}/{h}')]
            if not hashes:
                stop(f'{self.rec.name}: {b} carries no hash')
            out.append(f'    <dt>{self.T("src_" + key)}</dt><dd>{self.C(b + "/file")}</dd>'
                       + ''.join(f'<dd>{self.T(h)} {self.C(f"{b}/{h}")}</dd>' for h in hashes))
        out += ['  </dl>', '</section>']
        return '\n'.join(out)

    def record(self):
        blob = self.link('blob_main')
        out = ['<section id="record">', f'  <h2>{self.T("record")}</h2>', '  <dl>',
               f'    <dt>{self.T("record_kind")}</dt>{self.D("/kind", "dd")}',
               f'    <dt>{self.T("record_generated")}</dt>{self.D("/generated", "dd")}',
               f'    <dt>{self.T("release_tag")}</dt>{self.D("/release/tag", "dd")}']
        if self.rec.has('/release/commit'):
            out.append(f'    <dt>{self.T("release_commit")}</dt><dd>{self.C("/release/commit")}</dd>')
        if self.rec.has('/release/doi'):
            doi = self.value('/release/doi')
            out.append(f'    <dt>{self.T("release_doi")}</dt><dd><a href="{attr(self.link("doi_resolver") + doi)}" '
                       f'data-audit="/release/doi">{soft(doi)}</a></dd>')
        sheet = self.value('/sheet/file')
        out += [f'    <dt>{self.T("this_page")}</dt><dd><a href="{attr(blob + AUDIT_REPO_DIR + self.rec.name)}">'
                f'<code data-audit-file="name">{soft(self.rec.name, True)}</code></a></dd>'
                f'<dd>{self.T("sha256")} <code data-audit-file="sha256">{soft(self.rec.sha256, True)}</code></dd>',
                f'    <dt>{self.T("sheet_px")}</dt><dd>{self.D("/sheet/px/0")} {self.T("times")} {self.D("/sheet/px/1")}</dd>'
                f'<dd><a href="{attr(blob + SHEET_REPO_DIR + sheet)}">{self.C("/sheet/file")}</a></dd>',
                '  </dl>', '</section>']
        return '\n'.join(out)

    def datasheets(self):
        out = ['<section id="datasheets">', f'  <h2>{self.T("datasheets")}</h2>',
               f'  <nav aria-label="{self.A("nav_datasheets")}"><ul>']
        for s in STATES:
            here = ' aria-current="page"' if s == self.state else ''
            out.append(f'    <li><a href="/{page_name(s)}" data-audit-state="{attr(s)}"{here}>{esc(s)}</a></li>')
        out += ['  </ul></nav>', '</section>']
        return '\n'.join(out)

    def footer(self):
        nb = lambda s: s.replace(' ', '&nbsp;')
        return '\n'.join([
            '<footer class="site">',
            f'  <p>{self.T("licence_lead")} <a href="{attr(self.link("licence_cc"))}">{nb(self.T("licence_cc"))}</a>'
            f'{self.T("licence_mid")} <a href="{attr(self.link("licence_apache"))}">{nb(self.T("licence_apache"))}</a>'
            f'{self.T("licence_end")}</p>',
            f'  <nav aria-label="{self.A("nav_footer")}"><a href="{attr(self.link("home"))}">{self.T("nav_home")}</a> '
            f'<a href="{attr(self.link("note"))}">{self.T("nav_note")}</a> '
            f'<a href="{attr(self.link("method"))}">{self.T("nav_method")}</a> '
            f'<a href="{attr(self.link("repository"))}">{self.T("nav_repository")}</a></nav>',
            '</footer>'])

    def html(self):
        return '\n'.join([
            self.head(), '<body>', self.header(), '', '<main id="main">', '', self.title(), '',
            self.semaphore(), '', self.stations(), '', self.chart(), '', self.scale(), '',
            self.palette(), '', self.sources(), '', self.record(), '', self.datasheets(), '',
            '</main>', '', self.footer(), '</body>', '</html>', ''])


# ------------------------------------------------------- the site's chrome ---
def site_chrome(site_dir):
    """The single <style> block, the policy line and the social-card lines of site/index.html,
    copied byte for byte: the datasheet pages are styled by the site, not by this script."""
    index = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index):
        stop(f'no site page at {index}')
    raw = open(index, encoding='utf-8').read()
    styles = re.findall(r'<style>(.*?)</style>', raw, re.S)
    if len(styles) != 1:
        stop(f'site/index.html holds {len(styles)} <style> blocks, and the pages copy exactly one')
    digest = 'sha256-' + base64.b64encode(hashlib.sha256(styles[0].encode('utf-8')).digest()).decode()

    def line(pattern, what):
        m = re.search(pattern, raw)
        if not m:
            stop(f'site/index.html has no {what} line to copy')
        return m.group(0)

    chrome = {'style': styles[0], 'style_hash': digest,
              'csp': line(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">', 'Content-Security-Policy meta'),
              'icon': line(r'<link rel="icon" href="[^"]*" type="[^"]*">', 'icon link')}
    if f"'{digest}'" not in chrome['csp']:
        stop("site/index.html's policy line does not pin its own style block")
    for prop in ('og:site_name', 'og:image', 'og:image:alt', 'og:image:type', 'og:image:width', 'og:image:height'):
        chrome[prop] = line(rf'<meta property="{re.escape(prop)}" content="[^"]*">', prop)
    for name in ('twitter:card', 'twitter:image', 'twitter:image:alt'):
        chrome[name] = line(rf'<meta name="{re.escape(name)}" content="[^"]*">', name)
    m = re.search(r'<link rel="canonical" href="(https://[^"/]+/)">', raw)
    if not m:
        stop('site/index.html has no canonical link naming the site origin')
    chrome['origin'] = m.group(1)
    return chrome


def build(audit_dir, site_dir, states):
    labels = json.load(open(LABELS_FILE, encoding='utf-8'))
    chrome = site_chrome(site_dir)
    pages = {}
    for s in states:
        rec = Record(os.path.join(audit_dir, f'audit_{s}.json'))
        pages[page_name(s)] = Page(s, rec, labels, chrome, site_dir).html()
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--audit-dir', default=os.path.join(ROOT, 'docs', 'datasheet-audit'), help='where audit_<STATE>.json are read')
    ap.add_argument('--site', default=os.path.join(ROOT, 'site'), help='the site folder: index.html for the style and policy, assets/ for the semaphore')
    ap.add_argument('--out-dir', default=None, help='where the pages are written (default: the site folder)')
    ap.add_argument('--state', action='append', choices=STATES, help='one state; repeat for more (default: all four)')
    ap.add_argument('--verify', action='store_true', help='write nothing; compare a fresh build with the pages in --out-dir and exit 1 on any difference')
    a = ap.parse_args()
    out_dir = a.out_dir or a.site
    pages = build(a.audit_dir, a.site, a.state or STATES)      # every page is built before any is written
    if a.verify:
        bad = 0
        for name, text in sorted(pages.items()):
            path = os.path.join(out_dir, name)
            same = os.path.exists(path) and open(path, 'rb').read() == text.encode('utf-8')
            print(f'{"EQUAL  " if same else "DIFFERS"}   {name}  {hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]}')
            bad += 0 if same else 1
        print('VERIFY PASS: the pages regenerate byte for byte' if not bad else f'VERIFY FAIL: {bad} of {len(pages)} pages differ or are missing')
        raise SystemExit(1 if bad else 0)
    os.makedirs(out_dir, exist_ok=True)
    for name, text in sorted(pages.items()):
        with open(os.path.join(out_dir, name), 'wb') as f:
            f.write(text.encode('utf-8'))
        print(f'wrote {name}  {hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]}  {len(text.encode("utf-8"))} bytes')


if __name__ == '__main__':
    main()
