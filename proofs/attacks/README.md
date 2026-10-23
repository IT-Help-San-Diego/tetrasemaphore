# The attack files

Thirty-eight Lean files, one directory each. Every one of them is the honest
`TetrasemaphoreAlgebra.lean` with something added or changed, and every one of them is here because a
reviewer or this author built it to see whether `check.sh` would catch it. `ATTACKS.tsv` gives each file's
sha256 prefix and one line on what it does; `../RUN_INDEX.tsv` has every run of every one of them, with the
gate build it ran under, its exit code and the first differences the gate printed.

Twenty-five came out of the second opinion on version 2.2 and thirteen out of the second opinion on version
2.3. They are generated from the honest file by the two scripts beside this one:

    python3 build_attacks.py     ../TetrasemaphoreAlgebra.lean <outdir>
    python3 build_attacks_v24.py ../TetrasemaphoreAlgebra.lean <outdir>

Each script rebuilds its files byte for byte, which is the point of shipping the scripts rather than only
the files: the hashes in `ATTACKS.tsv` are reproducible from the honest file alone.

## Some of these files run code when they are compiled

That is what three of them were built to demonstrate — `DESYNC_EVAL`, `DESYNC_RAWSTRING` and
`N6_eval_sees_wrapper`, together with `N6b_indented_eval`, carry an `#eval` that Lean runs during
elaboration. Each writes one small text file in the directory it is compiled in (`EVID_DESYNC.txt`,
`EVID_RAW.txt`, `evidence_N6.txt`, `evidence_N6b.txt`), each holding one line of text, and does nothing
else: no network, no deletion, nothing outside that directory. They are source files rather than programs,
and the gate in this folder refuses all four before it elaborates anything — which is the finding they
record. A sandbox, a container or a throwaway directory is the comfortable place to open them.

Of the other thirty-four, `a15_full_chain` prints one forged footprint line when it is compiled and writes
nothing; the remaining thirty-three add a declaration, change an attribute, rename something or weaken a
statement, and compile with no side effect at all.

## What each one is for

`ATTACKS.tsv` is the short answer. The long answer, with what each attack proves and which check catches
it, is in `../RED_TEAM_LEAN.md`: the v2.2 attacks in the section on the fourth pass, the v2.3 attacks in
the fifth, the v2.4 attacks in the sixth.

## Verdicts, in one paragraph

Against the committed listing every one of the thirty-eight fails, measured: each adds, removes or changes
a declaration, so the listing the gate regenerates from the compiled module no longer matches the committed
one, and the two honest variants fail there too — `F1_honest_variants` and `F2_string_sorry` each exit 1 in
72 s on the line `STATEMENTS.md differs from the listing regenerated from the compiled module`. That line
is a statement about a *different* file, not about a dishonest one.

With the listing regenerated first — the path a maintainer takes, and the path most of these attacks were
built against — three of the thirty-eight pass, measured: `F1_honest_variants`, an honest file that has to
pass, and both spellings of the `Fml.holds` arm swap, `M1a_holds_arm_swap` and `M1b_holds_rhs_swap`, which
are the documented limit of regenerating that `STATEMENTS.md` states in its third section. A fourth,
`F2_string_sorry`, is an honest file that passed version 2.3 and fails this one on the declaration-head
rule, because it adds a `String` constant and this file's own declarations produce no `String`: the cost of
comparing against a set drawn from one file, recorded rather than hidden.
