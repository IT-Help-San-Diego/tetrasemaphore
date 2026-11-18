#!/usr/bin/env python3
"""tools/make_release_manifest.py: write or check the file table of RELEASE-MANIFEST.md.

The manifest says of itself that its list covers every file of the release except itself, CHANGELOG.md and
CITATION.cff. This script makes that sentence true and keeps it true. It leaves every word outside the table as it
is and rewrites only the rows: one for each file of the release, with its size in bytes and its SHA-256, sorted by
path. The files of the release are the files git tracks; in a copy without git (the unpacked zip) they are the files
under the tree.

  python3 tools/make_release_manifest.py            rewrite the rows from the tree
  python3 tools/make_release_manifest.py --check    change nothing; exit 1 if a file has no row, a row has no file,
                                                    or a row's size or hash is not the file's

Why it exists: release 1.1.0 had added 34 files when its manifest was first tagged, with the 283 rows of 1.0.0. A check
that tests only the rows a manifest has passes a manifest that leaves every new file out; this one starts from the
files.

A symbolic link stops the run: git stores a link and not the bytes it points at, so a row made from those bytes
would not describe what the release holds. The tree has none.

Standard-library Python only.
"""
import argparse, hashlib, os, re, subprocess, sys

MANIFEST = 'RELEASE-MANIFEST.md'
EXEMPT = (MANIFEST, 'CHANGELOG.md', 'CITATION.cff')     # the three the manifest says it does not list
ROW = re.compile(r'^\| `([^`]+)` \| ([\d,]+) \| ([0-9a-f]{64}) \|$')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def release_files(tree):
    """The files of the release, as paths with forward slashes."""
    if os.path.exists(os.path.join(tree, '.git')):
        p = subprocess.run(['git', '-C', tree, 'ls-files', '-s', '-z'], capture_output=True)
        if p.returncode != 0:
            sys.exit('STOP: git ls-files failed in %s:\n%s' % (tree, p.stderr.decode('utf-8', 'replace')))
        files, links = [], []
        for rec in p.stdout.split(b'\0'):
            if not rec:
                continue
            meta, name = rec.split(b'\t', 1)
            name = name.decode('utf-8')
            if meta.split()[0] not in (b'100644', b'100755'):     # 120000 is a symbolic link, 160000 a submodule
                links.append(name)
            files.append(name)
    else:
        files, links = [], []
        for dp, dns, fns in os.walk(tree):
            for x in dns + fns:
                if os.path.islink(os.path.join(dp, x)):
                    links.append(os.path.relpath(os.path.join(dp, x), tree).replace(os.sep, '/'))
            for fn in fns:
                files.append(os.path.relpath(os.path.join(dp, fn), tree).replace(os.sep, '/'))
    links += [f for f in files if f not in links and os.path.islink(os.path.join(tree, f))]
    if links:
        sys.exit('STOP: not a plain file (a symbolic link or a submodule), so it cannot have a row: %s' % ', '.join(sorted(links)))
    missing = [f for f in files if not os.path.isfile(os.path.join(tree, f))]
    if missing:
        sys.exit('STOP: tracked but not in the tree: %s' % ', '.join(missing))
    return sorted(f for f in files if f not in EXEMPT)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tree', default=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')),
                    help='the release tree (default: the parent of this file\'s folder)')
    ap.add_argument('--check', action='store_true', help='compare the rows with the tree and change nothing')
    A = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):       # a path this console cannot show is printed with escapes, not with an error
        stream.reconfigure(errors='backslashreplace')

    path = os.path.join(A.tree, MANIFEST)
    if not os.path.isfile(path):
        sys.exit('STOP: no %s in %s' % (MANIFEST, A.tree))
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    at = [i for i, l in enumerate(lines) if ROW.match(l)]
    if not at:
        sys.exit('STOP: %s has no rows of the form | `path` | bytes | sha256 |' % MANIFEST)
    first, last = at[0], at[-1]
    if at != list(range(first, last + 1)):
        sys.exit('STOP: the rows of %s are not one unbroken table' % MANIFEST)
    rows = {}
    for i in at:
        m = ROW.match(lines[i])
        if m.group(1) in rows:
            sys.exit('STOP: two rows for %s' % m.group(1))
        rows[m.group(1)] = (int(m.group(2).replace(',', '')), m.group(3))

    files = release_files(A.tree)
    actual = {f: (os.path.getsize(os.path.join(A.tree, f)), sha256(os.path.join(A.tree, f))) for f in files}

    if A.check:
        no_row = [f for f in files if f not in rows]
        no_file = sorted(r for r in rows if r not in actual)
        differ = [f for f in files if f in rows and rows[f] != actual[f]]
        order = list(rows) != sorted(rows)
        for label, items in (('no row for', no_row), ('a row but no file for', no_file), ('size or hash differs for', differ)):
            for x in items:
                print('FAULT  %s %s' % (label, x))
        if order:
            print('FAULT  the rows are not sorted by path')
        bad = len(no_row) + len(no_file) + len(differ) + (1 if order else 0)
        print('%s: %d files of the release besides the three it exempts, %d rows; %d without a row, %d rows without a file, %d that differ' % (
            MANIFEST, len(files), len(rows), len(no_row), len(no_file), len(differ)))
        print('MANIFEST CHECK %s' % ('PASS' if not bad else 'FAIL'))
        sys.exit(0 if not bad else 1)

    new_rows = ['| `%s` | %s | %s |' % (f, format(actual[f][0], ','), actual[f][1]) for f in files]
    out = lines[:first] + new_rows + lines[last + 1:]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    added = [f for f in files if f not in rows]
    changed = [f for f in files if f in rows and rows[f] != actual[f]]
    dropped = sorted(r for r in rows if r not in actual)
    print('%s: %d rows written (%d new, %d changed, %d dropped, %d as they were)' % (
        MANIFEST, len(new_rows), len(added), len(changed), len(dropped), len(new_rows) - len(added) - len(changed)))


if __name__ == '__main__':
    main()
