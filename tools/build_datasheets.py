#!/usr/bin/env python3
"""
build_datasheets.py: build the four semaphore datasheets from a checkout (Tetrasemaphore 1.1, step 1).

What it does, in order:
  1. checks the interpreter it runs in (Pillow and FreeType versions, cairo and cairosvg versions) and
     that Pillow's Raqm text layout engine is OFF: with Raqm on, text widths and line breaks change and
     the sheets do not reproduce (tools/datasheets-environment/README.md). It stops if Raqm is on,
     unless --allow-raqm is given;
  2. stages the inputs make_anatomy_plate.py reads into <out>/src: the four masters, the published note
     (README.md), notation-measurements.json, the Lean proof file and the four site PNGs, taken from
     the release the sheets cite (git show <cited tag>:<path>, default v1.0.0, the tag named in
     make_anatomy_plate.py's RELEASE constants), so the sheets quote the note they say they quote.
     When the tag exists, every input must exist at it or the build stops. When the checkout has no git
     history or no such tag, the inputs come from the working tree, with a printed warning. It also
     copies tools/drafting_measurements.json beside them;
  3. runs make_anatomy_plate.py once per state and make_audit_report.py once, with SOURCE_DATE_EPOCH set
     (so the build is reproducible byte for byte), FREETYPE_PROPERTIES removed from the child
     environment (that variable changes text metrics: interpreter-version=35 shortens a 15 px line
     from 876.0 to 845.0 px), and the citation passed as DATASHEET_RELEASE_TAG, DATASHEET_RELEASE_COMMIT
     and DATASHEET_RELEASE_DOI (--cited-tag, --release-commit, --release-doi; the staged note and proof
     file are named after the tag, as DATASHEET_NOTE_FILE and DATASHEET_LEAN_FILE): the sheets' footer
     prints the tag, then the commit and the DOI when they are known and nothing in their place when
     they are not, since a release's sheets are built before its commit exists. For a tag other than
     v1.0.0 the build stops unless --release-doi is given (the reserved DOI, or '' to print none), so
     no sheet inherits 1.0.0's DOI by default. With --verify the citation comes from the committed audit
     JSON (tag, commit if any, DOI), like the clock, so sheets that name no commit verify after their tag exists;
  4. runs test_quotation_punctuation.py against the staged note, so the build's "0 punctuation
     faults" is backed by the ten cases that prove the checker fires, and stops if any case misses;
  5. writes SHA256SUMS over everything it produced (<out>/sheets) and BUILD-RECORD.json: the
     interpreter check, every input with its source and hash, the citation, the clocks, the
     punctuation test's result, the products;
  6. with --verify, compares the build with the copies committed in the checkout
     (site/assets/datasheet_*.png, docs/datasheet-audit/audit_*.json, docs/AUDIT_REPORT.md),
     taking each state's clock from the committed audit JSON, and exits 1 on any difference.

Usage:
  python3 -I tools/build_datasheets.py                 build into build/datasheets (clock: $SOURCE_DATE_EPOCH,
                                                       else the HEAD commit time, else now)
  python3 -I tools/build_datasheets.py --verify        prove the checkout regenerates its committed sheets
  python3 -I tools/build_datasheets.py --out DIR --epoch SECONDS --cited-tag v1.0.0
  python3 -I tools/build_datasheets.py --cited-tag v1.1.0 --release-commit '' --release-doi <the DOI reserved for 1.1>
                                                       a release whose commit does not exist yet: inputs from the
                                                       working tree (with a warning), footer without a commit
"""
import argparse, datetime, hashlib, json, os, shutil, subprocess, sys

STATES = ['NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL']
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)

# what make_anatomy_plate.py reads (its ./src contract): repository path -> staged path
MASTERS_REL = 'artwork/master/states/proposals/notation/final-masters-2026-10-05'
def inputs_for(tag):
    """The repository paths the build reads, and the names make_anatomy_plate.py expects them under src/."""
    return [(f'{MASTERS_REL}/MASTER-medallion-{s}-notation-slot820.svg',
             os.path.join('src', 'masters', f'MASTER-medallion-{s}-notation-slot820.svg')) for s in STATES] + [
            ('README.md', os.path.join('src', f'README-{tag}.md')),
            (f'{MASTERS_REL}/notation-measurements.json', os.path.join('src', 'notation-measurements.json')),
            ('proofs/TetrasemaphoreAlgebra.lean', os.path.join('src', f'TetrasemaphoreAlgebra-{tag}.lean'))] + [
            (f'site/assets/TETRASEMAPHORE-{s}-en-1298.png', os.path.join('src', 'site', f'TETRASEMAPHORE-{s}-en-1298.png'))
            for s in STATES]
TOOL_INPUTS = [(os.path.join(TOOLS, 'drafting_measurements.json'), 'drafting_measurements.json')]

# where the checkout commits the build's products (--verify compares against these)
COMMITTED = {f'datasheet_{s}.png': os.path.join(ROOT, 'site', 'assets', f'datasheet_{s}.png') for s in STATES}
COMMITTED.update({f'datasheet_{s}_1200.png': os.path.join(ROOT, 'site', 'assets', f'datasheet_{s}_1200.png') for s in STATES})
COMMITTED.update({f'audit_{s}.json': os.path.join(ROOT, 'docs', 'datasheet-audit', f'audit_{s}.json') for s in STATES})
COMMITTED['AUDIT_REPORT.md'] = os.path.join(ROOT, 'docs', 'AUDIT_REPORT.md')

PREFLIGHT = r'''
import json, sys
from PIL import features, __version__ as pillow
import cairocffi, cairosvg
print(json.dumps(dict(python=sys.version.split()[0], pillow=pillow, freetype=features.version("freetype2"),
                      raqm=bool(features.check("raqm")), cairo=cairocffi.cairo_version_string(), cairosvg=cairosvg.__version__)))
'''


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


CITATION = {}
DATASHEET_VARS = ('DATASHEET_RELEASE_TAG', 'DATASHEET_RELEASE_COMMIT', 'DATASHEET_RELEASE_DOI', 'DATASHEET_NOTE_FILE', 'DATASHEET_LEAN_FILE')


def child_env(epoch):
    """The environment the scripts run in: the clock pinned, FREETYPE_PROPERTIES removed, every DATASHEET_*
    variable set by this driver and none inherited, so the sheets and the punctuation test read the same note."""
    env = {k: v for k, v in os.environ.items() if k != 'FREETYPE_PROPERTIES' and k not in DATASHEET_VARS}
    env['SOURCE_DATE_EPOCH'] = str(epoch)
    env.update(CITATION)
    return env


def tag_commit(tag):
    """The commit a tag points at in this checkout, or None."""
    try:
        r = subprocess.run(['git', '-C', ROOT, 'rev-parse', f'{tag}^{{commit}}'], capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except Exception:
        return None


def git_show(ref, relpath):
    """The file at <ref> from the checkout's history, or None when git or the path at that ref is unavailable."""
    try:
        r = subprocess.run(['git', '-C', ROOT, 'show', f'{ref}:{relpath}'], capture_output=True, check=True)
        return r.stdout
    except Exception:
        return None


def head_commit_time():
    try:
        out = subprocess.run(['git', '-C', ROOT, 'log', '-1', '--format=%ct'], capture_output=True, text=True, check=True)
        return int(out.stdout.strip())
    except Exception:
        return None


def committed_epoch(state):
    """The clock the committed audit JSON was written with (its generated field), as an epoch."""
    p = COMMITTED[f'audit_{state}.json']
    if not os.path.exists(p):
        return None
    g = json.load(open(p, encoding='utf-8'))['generated']
    return int(datetime.datetime.fromisoformat(g).timestamp())


def run(cmd, cwd, epoch):
    r = subprocess.run(cmd, cwd=cwd, env=child_env(epoch), capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stdout.write(r.stderr)
        raise SystemExit(f'FAILED ({r.returncode}): {" ".join(cmd)}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=os.path.join(ROOT, 'build', 'datasheets'))
    ap.add_argument('--epoch', type=int, default=None, help='SOURCE_DATE_EPOCH for every output')
    ap.add_argument('--verify', action='store_true', help='compare with the committed copies; clocks from their audit JSONs')
    ap.add_argument('--cited-tag', default='v1.0.0', help='the release the sheets cite; inputs are staged from it (default v1.0.0)')
    ap.add_argument('--allow-raqm', action='store_true', help='build even if Pillow reports its Raqm layout engine on')
    ap.add_argument('--release-commit', default=None, help="the commit the sheets cite; default: what --cited-tag resolves to here, else none; pass '' for none")
    ap.add_argument('--release-doi', default=None, help="the DOI the sheets cite, reserved before the build; '' prints none; required for any tag but v1.0.0")
    a = ap.parse_args()
    if a.verify:
        # the citation and the tag of a verify run are the committed sheets' own, read from their audit JSON
        p = COMMITTED['audit_NORMATIVE.json']
        if not os.path.exists(p):
            raise SystemExit(f'--verify: no committed audit JSON at {os.path.relpath(p, ROOT)}')
        rel = json.load(open(p, encoding='utf-8')).get('release', {})
        others = {s: json.load(open(COMMITTED[f'audit_{s}.json'], encoding='utf-8')).get('release', {})
                  for s in STATES if os.path.exists(COMMITTED[f'audit_{s}.json'])}
        if any(o != rel for o in others.values()):
            raise SystemExit('--verify: the committed audit JSONs do not agree on the release they cite: '
                             + '; '.join(f'{s} {o}' for s, o in others.items()) + '; nothing built')
        if rel.get('tag') and rel['tag'] != a.cited_tag:
            print(f"--verify: the committed sheets cite {rel['tag']}; staging the inputs from it, not from --cited-tag {a.cited_tag}")
        tag, commit, doi = rel.get('tag', a.cited_tag), rel.get('commit', ''), rel.get('doi', '')
    else:
        tag = a.cited_tag
        commit = a.release_commit if a.release_commit is not None else (tag_commit(tag) or '')
        if a.release_doi is None:
            if tag != 'v1.0.0':
                raise SystemExit(f'a DOI decision is needed for {tag}: pass --release-doi <reserved DOI>, or --release-doi \'\' to print none; '
                                 f'nothing built, so no sheet inherits the 1.0.0 DOI')
            doi = '10.5281/zenodo.23575816'
        else:
            doi = a.release_doi
    a.cited_tag = tag
    INPUTS = inputs_for(tag)
    CITATION.update(DATASHEET_RELEASE_TAG=tag, DATASHEET_RELEASE_COMMIT=commit, DATASHEET_RELEASE_DOI=doi,
                    DATASHEET_NOTE_FILE=f'README-{tag}.md', DATASHEET_LEAN_FILE=f'TetrasemaphoreAlgebra-{tag}.lean')

    out = os.path.abspath(a.out)
    sheets = os.path.join(out, 'sheets')
    os.makedirs(sheets, exist_ok=True)

    # 1. the interpreter
    r = subprocess.run([sys.executable, '-I', '-c', PREFLIGHT], env=child_env(0), capture_output=True, text=True)
    if r.returncode != 0:
        sys.stdout.write(r.stderr)
        raise SystemExit('the interpreter cannot import Pillow, cairocffi or cairosvg; install tools/datasheets-environment first')
    interp = json.loads(r.stdout.strip().splitlines()[-1])
    interp['freetype_properties_dropped'] = os.environ.get('FREETYPE_PROPERTIES')
    interp['executable'] = sys.executable
    interp['DYLD_FALLBACK_LIBRARY_PATH'] = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH')
    print('interpreter: ' + ', '.join(f'{k} {v}' for k, v in interp.items()))
    run_identity = dict(argv=sys.argv[1:], scripts={n: sha256(os.path.join(TOOLS, n)) for n in
                        ('build_datasheets.py', 'make_anatomy_plate.py', 'make_audit_report.py', 'test_quotation_punctuation.py')})
    if interp['raqm'] and not a.allow_raqm:
        with open(os.path.join(out, 'BUILD-RECORD.json'), 'w') as f:
            json.dump(dict(root=ROOT, interpreter=interp, run=run_identity, refused='Raqm layout engine on; nothing built'), f, indent=1)
        raise SystemExit('Pillow reports its Raqm layout engine ON (a libfribidi is loadable); with the template\'s explicit basic '
                         'engine the sheets still reproduce, but this driver refuses by default so the condition is never silent. '
                         'Make fribidi unloadable (for example point DYLD_FALLBACK_LIBRARY_PATH at a folder holding only libcairo) '
                         'or pass --allow-raqm to build anyway.')

    # 2. stage the inputs, from the cited release when the checkout's history has it
    from_tag = git_show(a.cited_tag, 'README.md') is not None
    inputs_from = f'git show {a.cited_tag}' if from_tag else 'working tree'
    if not from_tag:
        print(f'WARNING: {a.cited_tag} is not available from git here; staging the inputs from the working tree, '
              f'which may not be the note the sheets cite')
    staged = []
    for relpath, rel in INPUTS:
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if from_tag:
            data = git_show(a.cited_tag, relpath)
            if data is None:
                raise SystemExit(f'{relpath} does not exist at {a.cited_tag}; nothing built')
            with open(dst, 'wb') as f:
                f.write(data)
        else:
            shutil.copyfile(os.path.join(ROOT, relpath), dst)
        staged.append(dict(staged=rel, source=inputs_from, repository_path=relpath, sha256=sha256(dst)))
    for src, rel in TOOL_INPUTS:
        shutil.copyfile(src, os.path.join(out, rel))
        staged.append(dict(staged=rel, source='working tree (tools/)', repository_path=os.path.relpath(src, ROOT), sha256=sha256(os.path.join(out, rel))))
    print(f'inputs staged from {inputs_from}: ' + ', '.join(f"{os.path.basename(i['staged'])} {i['sha256'][:16]}" for i in staged))

    # 3. the clock
    epoch = a.epoch
    if epoch is None:
        e = os.environ.get('SOURCE_DATE_EPOCH')
        epoch = int(e) if e else (head_commit_time() or int(datetime.datetime.now(datetime.timezone.utc).timestamp()))
    epochs = {s: epoch for s in STATES}
    if a.verify:
        for s in STATES:
            ce = committed_epoch(s)
            if ce is None:
                raise SystemExit(f'--verify: no committed audit JSON for {s} at {COMMITTED[f"audit_{s}.json"]}')
            epochs[s] = ce
    report_epoch = epochs['NORMATIVE']   # the report prints a date only

    # 4. build
    for s in STATES:
        run([sys.executable, '-I', os.path.join(TOOLS, 'make_anatomy_plate.py'), '--state', s, '--outdir', sheets], out, epochs[s])
    run([sys.executable, '-I', os.path.join(TOOLS, 'make_audit_report.py')], sheets, report_epoch)

    # 4b. the punctuation test: it imports make_anatomy_plate.py from its working directory and
    #     reads the staged note, so the template is copied beside src/ for it
    shutil.copyfile(os.path.join(TOOLS, 'make_anatomy_plate.py'), os.path.join(out, 'make_anatomy_plate.py'))
    r = subprocess.run([sys.executable, '-I', os.path.join(TOOLS, 'test_quotation_punctuation.py')], cwd=out,
                       env=child_env(report_epoch), capture_output=True, text=True)
    punct = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-300:]
    print('punctuation test:', punct)
    if r.returncode != 0 or 'all as intended: True' not in punct:
        raise SystemExit('the quotation-punctuation test did not pass; the sheets\' "0 punctuation faults" is not backed')

    # 5. record
    products = sorted(f for f in os.listdir(sheets) if f != 'SHA256SUMS')
    with open(os.path.join(sheets, 'SHA256SUMS'), 'w') as f:
        for name in products:
            f.write(f'{sha256(os.path.join(sheets, name))}  {name}\n')
    record = dict(root=ROOT, interpreter=interp, run=run_identity, inputs_from=inputs_from, citation=CITATION, epochs=epochs,
                  inputs=staged, punctuation_test=punct, products={n: sha256(os.path.join(sheets, n)) for n in products})
    with open(os.path.join(out, 'BUILD-RECORD.json'), 'w') as f:
        json.dump(record, f, indent=1)
    print(f'built {len(products)} files in {sheets}')

    # 6. verify
    if a.verify:
        bad = 0
        for name, committed in sorted(COMMITTED.items()):
            built = os.path.join(sheets, name)
            if not os.path.exists(built):
                print(f'MISSING   {name} (not built)'); bad += 1; continue
            if not os.path.exists(committed):
                print(f'MISSING   {name} (not committed at {os.path.relpath(committed, ROOT)})'); bad += 1; continue
            same = sha256(built) == sha256(committed)
            print(f'{"EQUAL  " if same else "DIFFERS"}   {name}  {sha256(built)[:16]} vs committed {sha256(committed)[:16]}')
            bad += 0 if same else 1
        verdict = 'VERIFY PASS: the checkout regenerates its committed datasheets byte for byte' if bad == 0 \
            else f'VERIFY FAIL: {bad} of {len(COMMITTED)} products differ or are missing'
        record['verify'] = verdict
        with open(os.path.join(out, 'BUILD-RECORD.json'), 'w') as f:
            json.dump(record, f, indent=1)
        print(verdict)
        raise SystemExit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
