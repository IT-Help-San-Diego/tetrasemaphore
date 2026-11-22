#!/usr/bin/env python3
"""tools/check_semaphores.py: prove that semaphores/ holds the build record's own files.

semaphores/vector-masters/ and semaphores/pictures/ hold the release's four masters and its finished pictures: the files to
use and to cite. The sealed build record keeps the same files as the evidence of how they were built, in
build-record/master/states/proposals/notation/final-masters-2026-10-05/ (the masters) and its png/ folder (the pictures),
and that folder's MANIFEST.json gives each one's SHA-256 as it was built. This script stops with exit code 1 unless every
file in the two folders is byte for byte the build record's file of the same name, carries the hash MANIFEST.json gives,
and the two folders hold exactly the 4 masters and the 40 pictures and nothing else.

  python3 tools/check_semaphores.py [--tree <release tree>]

Standard-library Python only.
"""
import argparse, hashlib, json, os, sys

SEALED_PREFIX = 'master/states/proposals/notation/final-masters-2026-10-05'      # the folder, as MANIFEST.json names it
RECORD = 'build-record/' + SEALED_PREFIX
STATES = ('NORMATIVE', 'NON-NORMATIVE', 'METACOGNITIVE', 'CRITICAL')
MASTERS = ['MASTER-medallion-%s-notation-slot820.svg' % s for s in STATES]
PICTURES = ['TETRASEMAPHORE-%s-%s-%d.png' % (s, lang, px) for s in STATES for lang in ('en', 'es') for px in (512, 1024, 1214, 1298, 2460)]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tree', default=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
    tree = ap.parse_args().tree
    with open(os.path.join(tree, RECORD, 'MANIFEST.json'), encoding='utf-8') as f:
        sealed = {e['path']: e['sha256'] for e in json.load(f)['files']}      # paths as built: relative to build-record/
    bad = 0
    for folder, names, record_sub in (('semaphores/vector-masters', MASTERS, ''), ('semaphores/pictures', PICTURES, 'png')):
        have = sorted(n for n in os.listdir(os.path.join(tree, folder)) if n != '.DS_Store')
        for n in sorted(set(have) - set(names)):
            print('EXTRA     %s/%s is not one of the %d files this folder holds' % (folder, n, len(names))); bad += 1
        for n in names:
            copy, original = os.path.join(tree, folder, n), os.path.join(tree, RECORD, record_sub, n)
            if not os.path.isfile(copy):
                print('MISSING   %s/%s' % (folder, n)); bad += 1; continue
            if not os.path.isfile(original):
                print('NO RECORD %s/%s has no file of that name in the build record' % (folder, n)); bad += 1; continue
            c, o = sha256(copy), sha256(original)
            if c != o:
                print('DIFFERENT %s/%s %s, build record %s' % (folder, n, c[:16], o[:16])); bad += 1
            elif sealed.get('/'.join(x for x in (SEALED_PREFIX, record_sub, n) if x)) != c:
                print('UNSEALED  %s/%s %s is not the hash MANIFEST.json gives for %s' % (folder, n, c[:16], n)); bad += 1
    if bad:
        sys.exit('CHECK FAILED: %d fault(s); semaphores/ is not the build record\'s files' % bad)
    print('CHECK PASS: the %d masters and %d pictures in semaphores/ are byte for byte the build record\'s files, '
          'with the hashes its MANIFEST.json gives' % (len(MASTERS), len(PICTURES)))

if __name__ == '__main__':
    main()
