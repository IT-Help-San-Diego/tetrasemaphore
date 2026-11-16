#!/usr/bin/env python3
"""
check_datasheet_html.py: read the four datasheet HTML pages back against their audit records.

It shares no code with tools/make_datasheet_html.py: it parses each page as a browser would see it and
checks, for each one,

  1. provenance. Every piece of text in the page is either inside an element whose data-audit attribute
     names a field of audit_<STATE>.json, in which case the element's whole text must equal that field
     as the record writes it (numbers character for character), or it is exactly one of the labels
     declared in tools/datasheet_html_labels.json. Anything else is a fault. Words in attributes are
     held to the same rule: alt text, aria labels, the title and the description lines;
  2. completeness. Every string and number in the record is shown, except the fields listed in
     NOT_SHOWN below, so nothing drops out of a page without this file saying so;
  3. colour. Every swatch's fill is a colour stated in the field the swatch names;
  4. links. Every address is one the labels file declares or one built from the record;
  5. the site's hardening. One <style> block, byte for byte site/index.html's, its hash in the page's
     policy line, that line byte for byte index.html's; no script element, no style attribute, no
     event attribute, no external subresource; images only from site/assets and present there;
  6. structure. One h1, heading levels in order, unique ids, one linkable article per station, alt on
     every image, a scope on every table header;
  7. language. No em dash in a label, no personal name anywhere on a page, and no label declared
     that none of the four pages shows (the labels file lists as optional the few that belong to
     fields a record may leave out).

With --self-test it first damages a copy of each page in eight ways (a changed digit, an added word, a
dropped station and so on) and requires every damaged copy to fail, so a clean result means something.

Usage:
  python3 -I tools/check_datasheet_html.py                       site/ against docs/datasheet-audit
  python3 -I tools/check_datasheet_html.py --self-test
  python3 -I tools/check_datasheet_html.py --audit-dir DIR --pages-dir DIR [--site DIR]
"""
import argparse, base64, hashlib, json, os, re, sys
from html.parser import HTMLParser

STATES = ['NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL']
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
LABELS_FILE = os.path.join(TOOLS, 'datasheet_html_labels.json')
AUDIT_REPO_DIR, SHEET_REPO_DIR = 'docs/datasheet-audit/', 'site/assets/'

# Record fields a page does not show. Everything else in the record must appear.
NOT_SHOWN = [
    r'/drafting(/.*)?',                      # the plate's leader lines, badges and axis: a reflowed page has none
    r'/audit(/.*)?',                         # the plate build's own check counts, geometry among them
    r'/callouts/\d+/key', r'/callouts/\d+/layer_groups/\d+', r'/callouts/\d+/anchor_slot_units/\d+',   # where the plate draws
    r'/chart/own_move/\d+', r'/chart/rows/\d+/key',                                                     # keys; each row's is_own is shown
]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
FORBIDDEN_TAGS = {'script', 'iframe', 'object', 'embed', 'form', 'base', 'frame', 'frameset', 'applet'}
NAMES = ('carey', 'balboa')
EM_DASH = '\u2014'


def page_name(state):
    return f'datasheet-{state.lower()}.html'


def norm(s):
    return ' '.join(s.replace('\u00a0', ' ').split())


class Num(str):
    """A JSON number, kept as the characters the record writes."""


def leaves(node, at=''):
    """Every (pointer, value) in the record whose value is a string, a number or a boolean."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, f'{at}/{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, f'{at}/{i}')
    elif node is not None:
        yield at, node


class Reader(HTMLParser):
    """Walks a page and files what it finds: audited elements, loose text, tags and their attributes."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.faults = [], []
        self.audited, self.loose, self.tags = [], [], []
        self.capture = None            # [depth, kind, key, parts, attrs]
        self.title, self.styles = [], []
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        a = {}
        for k, v in attrs:
            if k in a:
                self.faults.append(f'<{tag}> repeats the attribute {k}')
            a[k] = v or ''
        self.tags.append((tag, a, [t for t, _ in self.stack]))
        if tag == 'body':
            self.in_body = True
        if tag == 'style':
            self.styles.append([])
        kinds = [k for k in ('data-audit', 'data-audit-file', 'data-audit-state') if k in a]
        if kinds and tag != 'svg':
            if self.capture is not None or len(kinds) > 1:
                self.faults.append(f'<{tag} {kinds[0]}="{a[kinds[0]]}"> sits inside another audited element')
            elif tag in VOID:
                self.faults.append(f'<{tag}> is audited and can hold no text')
            else:
                self.capture = [len(self.stack), kinds[0], a[kinds[0]], [], a]
        if tag not in VOID:
            self.stack.append((tag, a))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.faults.append(f'</{tag}> closes nothing open here (open: {[t for t, _ in self.stack][-3:]})')
            return
        self.stack.pop()
        if self.capture is not None and len(self.stack) == self.capture[0]:
            _, kind, key, parts, a = self.capture
            self.audited.append((kind, key, ''.join(parts), tag, a))
            self.capture = None

    def handle_data(self, data):
        open_tags = [t for t, _ in self.stack]
        if 'style' in open_tags:
            self.styles[-1].append(data)
        elif 'title' in open_tags:
            self.title.append(data)
        elif self.capture is not None:
            self.capture[3].append(data)
        elif data.strip():
            if not self.in_body:
                self.faults.append(f'text outside the body: {norm(data)[:60]!r}')
            self.loose.append((norm(data), open_tags[-1] if open_tags else ''))

    def handle_comment(self, data):
        self.faults.append(f'a comment: {norm(data)[:60]!r}')

    def close(self):
        super().close()
        if self.stack:
            self.faults.append(f'left open at the end: {[t for t, _ in self.stack]}')


def index_chrome(site_dir):
    raw = open(os.path.join(site_dir, 'index.html'), encoding='utf-8').read()
    styles = re.findall(r'<style>(.*?)</style>', raw, re.S)
    csp = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)">', raw)
    origin = re.search(r'<link rel="canonical" href="(https://[^"/]+/)">', raw)
    metas = {}
    for m in re.finditer(r'<meta (?:property|name)="([^"]+)" content="([^"]*)">', raw):
        metas[m.group(1)] = m.group(2)
    icon = re.search(r'<link rel="icon" href="([^"]*)" type="([^"]*)">', raw)
    return dict(style=styles[0] if len(styles) == 1 else None, csp=csp.group(1) if csp else None,
                origin=origin.group(1) if origin else None, metas=metas,
                icon=(icon.group(1), icon.group(2)) if icon else None)


def check_page(state, raw, record_path, labels, site_dir, all_states):
    """Returns (faults, counts) for one page given as text."""
    F = []
    rec_bytes = open(record_path, 'rb').read()
    rec = json.loads(rec_bytes.decode('utf-8'), parse_float=Num, parse_int=Num)
    known = dict(leaves(rec))
    rec_name, rec_sha = os.path.basename(record_path), hashlib.sha256(rec_bytes).hexdigest()
    chrome = index_chrome(site_dir)
    label_text = {norm(v) for v in labels['text'].values()}
    r = Reader()
    r.feed(raw)
    r.close()
    F += r.faults

    def expect(pointer):
        if pointer not in known:
            return None
        v = known[pointer]
        if isinstance(v, bool):
            return labels['booleans'].get(pointer.rsplit('/', 1)[-1], {}).get('true' if v else 'false')
        return str(v)

    # 1. provenance: audited elements
    shown = {}
    for kind, key, text, tag, a in r.audited:
        t = norm(text)
        if kind == 'data-audit':
            want = expect(key)
            if want is None:
                F.append(f'<{tag} data-audit="{key}"> names a field the record does not hold')
            elif t != norm(want):
                F.append(f'{key}: the page shows {t[:70]!r} and the record holds {norm(want)[:70]!r}')
            shown[key] = shown.get(key, 0) + 1
        elif kind == 'data-audit-file':
            want = {'name': rec_name, 'sha256': rec_sha}.get(key)
            if want is None or t != want:
                F.append(f'the audit file {key}: the page shows {t[:70]!r} and the file is {str(want)[:70]!r}')
        elif kind == 'data-audit-state':
            if key not in all_states or t != all_states[key]:
                F.append(f'the link to {key!r} is worded {t!r}, and that record names its state {all_states.get(key)!r}')
            if a.get('href') != '/' + page_name(key):
                F.append(f"the link to {key!r} goes to {a.get('href')!r}")
            if (a.get('aria-current') == 'page') != (key == state):
                F.append(f'aria-current on the link to {key!r} is wrong for the page of {state}')
    # 1b. provenance: every other piece of text is a declared label
    for t, parent in r.loose:
        if t not in label_text:
            F.append(f'text that is neither a record field nor a declared label, in <{parent}>: {t[:70]!r}')
    title = norm(''.join(r.title))
    want_title = labels['templates']['title'].format(state=rec.get('state'))
    if title != want_title:
        F.append(f'<title> is {title!r}, not {want_title!r}')

    # 2. completeness
    hidden = [re.compile(p) for p in NOT_SHOWN]
    standfirst = [k for k in shown if k in ('/standfirst/text', '/standfirst/unelided')]
    if len(standfirst) != 1:
        F.append(f'the standfirst is shown {len(standfirst)} times, not once')
    elif standfirst[0] == '/standfirst/text' and '\u2026' in str(known.get('/standfirst/text', '')) \
            and '/standfirst/unelided' not in known:
        F.append('the standfirst shown is elided and the record holds no unelided sentence')
    for pointer in known:
        if any(h.fullmatch(pointer) for h in hidden) or pointer in ('/standfirst/text', '/standfirst/unelided'):
            continue
        if pointer not in shown:
            F.append(f'{pointer} is in the record and not on the page')
    if rec.get('state') != state:
        F.append(f"the record is of {rec.get('state')!r}, not of {state}")

    # 3. colour
    swatches = 0
    for i, (tag, a, parents) in enumerate(r.tags):
        if tag == 'svg':
            ptr = a.get('data-audit-fill')
            rect = next((b for t, b, p in r.tags[i + 1:i + 3] if t == 'rect'), None)
            fill = (rect or {}).get('fill', '')
            swatches += 1
            if ptr is None or ptr not in known or rect is None:
                F.append(f'a swatch names no record field (data-audit-fill={ptr!r})')
            elif not re.fullmatch(r'#[0-9A-Fa-f]{6}', fill) or fill.upper() not in str(known[ptr]).upper():
                F.append(f'a swatch is filled {fill!r}, which {ptr} does not state')
            if a.get('aria-hidden') != 'true':
                F.append('a swatch is not hidden from screen readers; the colour is stated in the text beside it')
        if tag == 'rect' and 'svg' not in parents:
            F.append('a rect outside a swatch')

    # 4. links, and the words in attributes
    L = labels['links']
    png = str(known.get('/sources/site_png/file', ''))
    small = png[:-len('-1298.png')] + '-512.png' if png.endswith('-1298.png') else None
    allowed = {'#main', L['home'], L['note'], L['method'], L['repository'], L['licence_cc'], L['licence_apache'],
               '/assets/' + png, L['blob_main'] + AUDIT_REPO_DIR + rec_name,
               L['blob_main'] + SHEET_REPO_DIR + str(known.get('/sheet/file', ''))}
    allowed |= {'/' + page_name(s) for s in STATES}
    if '/release/doi' in known:
        allowed.add(L['doi_resolver'] + str(known['/release/doi']))
    aria = {v for v in labels['aria'].values()}
    ids, headings, stations = [], [], 0
    sf_shown = norm(str(known.get(standfirst[0], ''))) if len(standfirst) == 1 else None
    url = (chrome['origin'] or '') + page_name(state)
    want_meta = {'description': sf_shown, 'og:description': sf_shown, 'twitter:description': sf_shown,
                 'og:title': want_title, 'twitter:title': want_title, 'og:url': url, 'og:type': 'article',
                 'viewport': 'width=device-width, initial-scale=1'}
    for k in ('og:site_name', 'og:image', 'og:image:alt', 'og:image:type', 'og:image:width', 'og:image:height',
              'twitter:card', 'twitter:image', 'twitter:image:alt'):
        want_meta[k] = chrome['metas'].get(k)
    seen_meta = set()
    for tag, a, parents in r.tags:
        if tag in FORBIDDEN_TAGS:
            F.append(f'a <{tag}> element')
        for k in a:
            if k == 'style' or k.startswith('on'):
                F.append(f'<{tag}> carries the attribute {k}')
            if k in ('src', 'srcset') and tag != 'img':
                F.append(f'<{tag}> carries {k}')
        if 'id' in a:
            ids.append(a['id'])
        if tag == 'a':
            if a.get('href') not in allowed:
                F.append(f"a link goes to {a.get('href')!r}, an address neither declared nor built from the record")
        if tag == 'img':
            if a.get('src') != '/assets/' + str(small) or not os.path.exists(os.path.join(site_dir, 'assets', str(small))):
                F.append(f"the image is {a.get('src')!r}, not the site's /assets/{small}")
            if 'srcset' in a:
                F.append('the image carries srcset')
            if a.get('alt') != labels['templates']['alt'].format(state=rec.get('state')):
                F.append(f"the image's alt text is {a.get('alt')!r}")
        if 'aria-label' in a and a['aria-label'] not in aria:
            F.append(f"aria-label {a['aria-label']!r} is not a declared label")
        if tag == 'th' and a.get('scope') not in ('col', 'row'):
            F.append('a table header without a scope')
        if re.fullmatch(r'h[1-6]', tag):
            headings.append(int(tag[1]))
        if tag == 'article' and re.fullmatch(r'station-\d+', a.get('id', '')):
            stations += 1
            if a.get('aria-labelledby') != a['id'] + '-title':
                F.append(f"{a['id']} is not labelled by its own title")
        if tag == 'link':
            rel = a.get('rel')
            if rel == 'canonical':
                if a.get('href') != url:
                    F.append(f"the canonical link is {a.get('href')!r}, not {url!r}")
            elif rel == 'icon':
                if chrome['icon'] is None or (a.get('href'), a.get('type')) != chrome['icon']:
                    F.append("the icon link is not index.html's")
            else:
                F.append(f'a <link rel="{rel}">')
        if tag == 'meta':
            name = a.get('property') or a.get('name')
            if a.get('http-equiv') == 'Content-Security-Policy':
                seen_meta.add('csp')
                if a.get('content') != chrome['csp']:
                    F.append("the policy line is not index.html's, byte for byte")
            elif 'charset' in a:
                if a['charset'].lower() != 'utf-8':
                    F.append(f"charset {a['charset']!r}")
            elif name in want_meta:
                seen_meta.add(name)
                if want_meta[name] is None or norm(a.get('content', '')) != norm(want_meta[name]):
                    F.append(f"meta {name} is {a.get('content', '')[:60]!r}, not {str(want_meta[name])[:60]!r}")
            else:
                F.append(f'a meta line this check does not know: {a}')
    for name in list(want_meta) + ['csp']:
        if name not in seen_meta:
            F.append(f'no meta line for {name}')

    # 5. the site's hardening
    if len(r.styles) != 1:
        F.append(f'{len(r.styles)} <style> blocks, not one')
    page_styles = re.findall(r'<style>(.*?)</style>', raw, re.S)
    if chrome['style'] is None or page_styles != [chrome['style']]:
        F.append("the <style> block is not index.html's, byte for byte")
    elif chrome['csp'] is None or ("'sha256-" + base64.b64encode(hashlib.sha256(
            page_styles[0].encode('utf-8')).digest()).decode() + "'") not in chrome['csp']:
        F.append("the style block's hash is not in the policy line")
    if re.search(r'(?:src|srcset|href)\s*=\s*["\']?//', raw, re.I) or re.search(r'\bsrc\s*=\s*["\']?https?:', raw, re.I):
        F.append('an external or protocol-relative subresource')
    if ('/' + 'Users/') in raw or '/private/tmp/' in raw:
        F.append('a local filesystem path')

    # 6. structure
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        F.append(f'the id {i!r} is used more than once')
    if headings.count(1) != 1 or (headings and headings[0] != 1):
        F.append(f'{headings.count(1)} h1 elements, or the first heading is not the h1')
    for a_, b_ in zip(headings, headings[1:]):
        if b_ > a_ + 1:
            F.append(f'a heading jumps from h{a_} to h{b_}')
    if str(stations) != str(rec.get('stations')) or stations != len(rec.get('callouts', [])):
        F.append(f"{stations} station articles for a record of {rec.get('stations')} stations")
    callout_ns = [str(c.get('n')) for c in rec.get('callouts', [])]
    for n in callout_ns:
        if f'station-{n}' not in ids:
            F.append(f'no element with the id station-{n}')

    # 7. language
    low = raw.lower()
    body = low[low.find('<body'):]
    for nm in NAMES:
        if nm in re.sub(r'<style>.*?</style>', '', low, flags=re.S):
            F.append(f'the name {nm!r} appears on the page')
    used = {t for t, _ in r.loose} | {norm(text) for kind, key, text, tag, a in r.audited if isinstance(known.get(key), bool)}
    used_aria = {a['aria-label'] for tag, a, parents in r.tags if 'aria-label' in a}
    return F, dict(audited=len(r.audited), fields=len(shown), labels=len(r.loose), swatches=swatches,
                   stations=stations, record_leaves=len(known), used=used, used_aria=used_aria)


def damaged(raw):
    """Eight copies of a page, each wrong in one way the check must catch."""
    out = []
    m = re.search(r'(<td data-audit="/chart/rows/0/iou">)(\d)', raw)
    out.append(('a changed digit in a measured value', raw[:m.start(2)] + str((int(m.group(2)) + 1) % 10) + raw[m.end(2):]))
    out.append(('a word that is neither record nor label', raw.replace('</h1>', '</h1>\n<p>Certified accurate.</p>', 1)))
    m = re.search(r'  <article class="panel" id="station-2".*?</article>\n', raw, re.S)
    out.append(('a station left out', raw[:m.start()] + raw[m.end():]))
    m = re.search(r'fill="#([0-9A-Fa-f]{6})"', raw)
    out.append(('a swatch in a colour the record does not state', raw[:m.start(1)] + 'FF00FF' + raw[m.end(1):]))
    out.append(('a style attribute', raw.replace('<h1>', '<h1 style="color:red">', 1)))
    out.append(('a script', raw.replace('</body>', '<script>1</script></body>', 1)))
    out.append(('a changed rule in the style block', raw.replace('<style>', '<style>\nbody{color:red}', 1)))
    m = re.search(r'<code data-audit="/callouts/0/values/0/sha16">(.*?)</code>', raw, re.S)
    out.append(('a source hash that is not the record\'s', raw[:m.start(1)] + '0000000000000000' + raw[m.end(1):]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--audit-dir', default=os.path.join(ROOT, 'docs', 'datasheet-audit'))
    ap.add_argument('--pages-dir', default=None, help='where datasheet-<state>.html are read (default: the site folder)')
    ap.add_argument('--site', default=os.path.join(ROOT, 'site'), help='the site folder: index.html and assets/')
    ap.add_argument('--self-test', action='store_true', help='first prove the check fires on eight kinds of damage')
    a = ap.parse_args()
    pages_dir = a.pages_dir or a.site
    labels = json.load(open(LABELS_FILE, encoding='utf-8'))
    bad, used, used_aria = 0, set(), set()
    for group in ('text', 'aria', 'templates'):
        for k, v in labels[group].items():
            if EM_DASH in v:
                print(f'FAULT  labels file: {group}.{k} holds an em dash'); bad += 1
    records = {s: os.path.join(a.audit_dir, f'audit_{s}.json') for s in STATES}
    all_states = {}
    for s, p in records.items():
        if not os.path.exists(p):
            raise SystemExit(f'check_datasheet_html: no audit record at {p}')
        all_states[s] = json.load(open(p, encoding='utf-8')).get('state')
    for s in STATES:
        path = os.path.join(pages_dir, page_name(s))
        if not os.path.exists(path):
            print(f'FAULT  {page_name(s)}: not there'); bad += 1
            continue
        raw = open(path, encoding='utf-8').read()
        faults, n = check_page(s, raw, records[s], labels, a.site, all_states)
        if a.self_test:
            # a kind of damage counts as caught only when it raises a fault the undamaged page does not have
            missed = [what for what, text in damaged(raw)
                      if not set(check_page(s, text, records[s], labels, a.site, all_states)[0]) - set(faults)]
            for what in missed:
                print(f'FAULT  {page_name(s)}: the check did not catch {what}'); bad += 1
            print(f'self-test  {page_name(s)}: {8 - len(missed)} of 8 kinds of damage caught')
        for f in faults:
            print(f'FAULT  {page_name(s)}: {f}')
        bad += len(faults)
        used |= n['used']
        used_aria |= n['used_aria']
        print(f'{"FAIL" if faults else "ok  "}  {page_name(s)}: {n["audited"]} audited elements showing {n["fields"]} record '
              f'fields ({n["record_leaves"]} in the record), {n["labels"]} label texts, {n["swatches"]} swatches, '
              f'{n["stations"]} stations, {len(faults)} faults')
    # the labels file lists the words the pages show, and no others
    declared = dict(labels['text'])
    declared.update({f'booleans.{k}.{tf}': v for k, pair in labels['booleans'].items() for tf, v in pair.items()})
    optional = set(labels.get('optional', []))
    for k in sorted(optional - set(labels['text'])):
        print(f'FAULT  labels file: optional names {k!r}, which is not a text label'); bad += 1
    for k, v in declared.items():
        if norm(v) not in used and k not in optional:
            print(f'FAULT  labels file: {k} ({v!r}) is declared and shown on none of the four pages'); bad += 1
    for k, v in labels['aria'].items():
        if v not in used_aria:
            print(f'FAULT  labels file: aria.{k} ({v!r}) is declared and used on none of the four pages'); bad += 1
    print('CHECK PASS: every text on the four pages is a record field or a declared label' if not bad
          else f'CHECK FAIL: {bad} faults')
    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
