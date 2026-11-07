#!/usr/bin/env python3
"""Evidence that the quotation-punctuation check works.

Runs the check over the three faults found in earlier review rounds, their
three corrected forms, the one full stop the source genuinely has, and three
invented cases - ten in all. A check that reports zero faults is only
informative if it fires on a real one, so this is run alongside the sheets.
"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location('mk', 'make_anatomy_plate.py')
mk = importlib.util.module_from_spec(spec); sys.modules['mk'] = mk; spec.loader.exec_module(mk)
S = mk.Sources(mk.Master('METACOGNITIVE'))

CASES = [
    ("station 5 before the fix (the note continues with a colon)",
     "\u201cEach semaphore's mark is built to survive its own move.\u201d", True),
    ("station 5 as it now reads",
     "\u201cEach semaphore's mark is built to survive its own move \u2026\u201d", False),
    ("METACOGNITIVE gold before the fix (the note continues with a comma)",
     "\u201cGold shows what the semaphore's move leaves in place: \u2026 a horizontal line "
     "for \u03c3\u2095.\u201d", True),
    ("METACOGNITIVE gold as it now reads",
     "\u201cGold shows what the semaphore's move leaves in place: \u2026 a horizontal line "
     "for \u03c3\u2095 \u2026\u201d", False),
    ("NORMATIVE absence note before the fix (the note continues with a comma)",
     "\u201c\u2026 the whole figure for I.\u201d", True),
    ("NORMATIVE absence note as it now reads",
     "\u201c\u2026 the whole figure for I \u2026\u201d", False),
    ("CRITICAL gold: the full stop the note does have at that point",
     "\u201cGold shows what the semaphore's move leaves in place: \u2026 a single point "
     "for C\u2082.\u201d", False),
    ("a semicolon the note does not have",
     "\u201cColour comes second. Shape carries every state;\u201d", True),
    ("a comma in place of the note's full stop",
     "\u201cCheck the mark, not the ring,\u201d", True),
    ("a span that is not in the note at all",
     "\u201cShape carries nothing at all.\u201d", True),
]

if __name__ == '__main__':
    ok = True
    for label, span, expect_fire in CASES:
        _, faults = S.quotation_punctuation(span)
        fired = bool(faults)
        good = fired == expect_fire
        ok &= good
        detail = (f"claimed {faults[0]['claimed']!r}, note has {faults[0]['source_has']!r}"
                  if fired else "no fault")
        print(f"  {'PASS' if good else 'MISS'}  fires={fired!s:5s} expected={expect_fire!s:5s}  "
              f"{label}\n        {detail}")
    print(f"\n{len(CASES)} cases, all as intended: {ok}")
    sys.exit(0 if ok else 1)
