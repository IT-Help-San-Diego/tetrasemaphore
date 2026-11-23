# Final statement check — the seventeen, and why they reject

Run at 2026-11-23T18:47:40Z on lab-pc.

- challenge `Challenge.lean` sha256 `c5ed8f0cac379627175a311004af6cd26c3356b1227feab2e794aaca05f1491f` (17 theorems, 21 definition blocks by this runner's own count)
- solution `TetrasemaphoreAlgebra.lean` at tag v1.2.0 sha256 `f066faf6595d22e94d6d7507b07e28a1993fe5d56e13d9a6512b9dcf9a30cd2a`
- permitted axioms: `propext`, `Quot.sound`, `Classical.choice`; no others
- judge: `lake comparator` v4.36.0, sandboxed; external checkers on the accepted config

## Per-config results

| config | build v4.33.0 | build v4.36.0 |
|---|---|---|
| all17 | exit 1 — do not match: 'T1_all_distinct' | exit 1 — do not match: 'T1_all_distinct' |
| q14 | exit 0 — ACCEPTED | exit 0 — ACCEPTED |
| q14+T7 | exit 0 — ACCEPTED | exit 0 — ACCEPTED |
| q14+T1 | exit 1 — do not match: 'T1_all_distinct' | exit 1 — do not match: 'T1_all_distinct' |
| q14+T8 | exit 1 — do not match: 'T8_five_are' | exit 1 — do not match: 'T8_five_are' |

## Reading

The all-seventeen config is expected to reject, and does: the challenge states
`T1_all_distinct` in a different form from the published file. Science proved both
equivalences, so this is a form difference recorded as the finding, not a failure.
Fifteen theorems are accepted as the same statement by the judge, on both builds: the
fourteen whose text matches the published statements exactly, plus `T7_both_mirrors`, whose text
differs by a binder bracket that the judge reads as the same statement. All fifteen were also
accepted by all five external checkers on the 4.36.0 build.

## What this does NOT show

- It does not show the seventeen statements say what the note says in English.
  Claude Code wrote them and Claude Science wrote the proofs: both Claude models.
- It does not show the semaphores help anyone think.

## Independent kernels

On the **4.36.0 build**, `--paranoid` was run twice with `lake comparator` sandboxed:

| config | names | result |
|---|---|---|
| `q14` | the fourteen text-identical statements | exit 0 — `leanchecker-paranoid`, `lean4lean`, `nanoda`, `con-leche`, `con-ron` and Lean's default kernel all accept |
| `q14+T7` | the fifteen, adding `T7_both_mirrors` | exit 0 — the same six kernels accept (3 m 02 s) |

The fifteen name set is what Claude Code's `comparator-15.json` names. `T7_both_mirrors` was run
separately because its text differs from the published statement by a binder bracket; the judge
reads the two as the same statement, so no equivalence argument is needed for it.

The five external checkers were **not** run on the 4.33.0 build and could not be: they cannot
read a 4.33 core library. The 4.33.0 build got the plain judge only, and passed it.

## Corrections to this record

Two strings in the generated record were wrong and are corrected here. No judge output
changed; every verdict, exit code and message below came from `lake comparator`.

- The header said "19 definition blocks". The runner measured 21 and printed 21 to its
  log; the 19 had been transcribed from another lane's read instead of taken from the
  measurement. The count above is now the runner's own. Same file, same sha256: 21 by
  `^(abbrev|inductive|structure|def)`, 19 by Science's selection.
- The results table printed raw cells like "1 do not match". They now read
  "exit 1 — do not match: ...".

The generator has been fixed so a re-run cannot repeat either mistake.

## Addition, same day

The `--paranoid` run above was first made on the fourteen. Claude Code's reconciliation caught
that `T7_both_mirrors` therefore had only the plain judge's acceptance, and asked for the
fifteen-name run. It was made on lab-pc against the same 4.36.0 exports and the same
`Challenge.lean` (sha256 `c5ed8f0c…`): exit 0, all five external checkers and Lean's default
kernel accept. The count "fourteen" in earlier summaries becomes **fifteen**.
