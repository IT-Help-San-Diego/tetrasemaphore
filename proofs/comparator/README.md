# The statement check: Lean's judge on the seventeen headline theorems

`../check.sh` checks how the proofs were made. It says of itself that it cannot tell whether a
theorem says what its name says. This folder sets up the standard answer to that, the one the 2026
Riemann Hypothesis proof was put through: `lake comparator`, Lean's own judge. A second file,
`Challenge.lean`, states seventeen theorems with no proofs. The judge confirms that the published
file, `../TetrasemaphoreAlgebra.lean`, proves exactly those statements, with Lean's three standard
axioms and no others, and that Lean's kernel and the independent checkers accept the proofs.

The judge's own caveat, from `lake help comparator`: it "has no way to figure out whether the
statements in the challenge file properly correspond to the meaning intended by their author. It
can only establish that the statements as written down are correct". The statements as written
down are this folder's contribution; whether they say what the note says is a question for a
reader, and the one question a mathematician will be asked.

Nothing in this folder changes the published proofs. `Challenge.lean` copies the definitions from
the published file at tag `v1.2.0` unchanged and adds statements with `sorry`; the published file
is judged in place (the Lake library `TetrasemaphoreAlgebra` has `srcDir = ".."`), not from a copy.

## The verdict

Hermes ran the judge on 23 November 2026, sandboxed, on a Linux machine (lab-pc), against this folder's `Challenge.lean`
(SHA-256 `c5ed8f0c…`) and the published proof file at `v1.2.0` (SHA-256 `f066faf6…`). Its record is
`RESULT-lab-pc-2026-11-23.md`, kept here as Hermes wrote it. Every verdict is the one this README predicted before the run.

| statements | proof file built with Lean 4.33.0 | built with Lean 4.36.0 |
|---|---|---|
| all seventeen | rejected at `T1_all_distinct` | rejected at `T1_all_distinct` |
| the fifteen | accepted | accepted, and accepted by all five outside checkers |
| the fourteen and `T1_all_distinct` | rejected at `T1_all_distinct` | rejected at `T1_all_distinct` |
| the fourteen and `T8_five_are` | rejected at `T8_five_are` | rejected at `T8_five_are` |

So fifteen of the seventeen statements are, to the judge, the published statements, and the proofs of those fifteen
pass Lean's kernel and five independent checkers. The other two differ from the published statements in form and not
in meaning; each equivalence is proved (see "The two form differences" below), and the judge rejects them by name
because it compares statements and does not prove equivalences. The five outside checkers ran on the 4.36.0 build
only: they cannot read a 4.33 library. Nothing false was found in the proofs.

This is the project's own lanes checking one another: Claude Code wrote the statements, Claude Science wrote the
proofs, and both are Claude models. It is not an outside review.

## How `Challenge.lean` was written, and by whom

Claude Science wrote the proofs, so Claude Science did not write the statements. Claude Code did,
on 23 November 2026, by this protocol:

1. The definitions the statements need were cut from the published file by line range and checked
   line for line against it (every non-comment line of the definitions block occurs verbatim in
   `../TetrasemaphoreAlgebra.lean` at `v1.2.0`). The judge compares, by name, every constant a
   statement uses, so these have to be the same constants.
2. Three drafters, each a fresh Claude subagent given only two files, the definitions and an
   English dossier (the note's sentences, the guide's "What is proved" paragraphs, the site's
   "How the four fit together" list, the seven datasheet captions, and Claude Science's handoff
   table pairing each claim with its theorem name), each wrote all seventeen statements from the
   English and type-checked them under Lean 4.33.0. They were told not to open the proof file or
   anything else in the repository, and were asked afterwards to confess anything beyond the two
   files that influenced them. That is an instruction, not a wall: a drafter that disobeyed could
   not be detected from here.
3. Five comparison agents, one per group of related theorems, then compared the drafts with the
   published statements. Where a draft differed in form they proved or refuted the equivalence in
   Lean. They also judged whether each published statement says what the English says.
4. Ten skeptics, two per group, tried to break those judgements. One critic read everything,
   checked the names, the datasheet seven, the definitions' closure and the handoff's own prior
   finding, chose the statement for each theorem, and compiled the result.
5. Claude Code assembled `Challenge.lean` from the critic's choices and rehearsed the judge's
   comparison locally (below). No statement was reconciled toward the published form: where the
   from-English statement and the published one differ, the difference stands in the file, and
   the judge is expected to report it.

Claude Code and Claude Science are both Claude models. This protocol catches slips and
mismatches between the English and the Lean; it is not an outside review.

## What the check found

**The drafts.** The three drafters, working from the English alone, wrote the same statement for
every one of the seventeen (one hypothesis name and one pair of parentheses apart), and all three
confessed to nothing beyond the two files and general Lean knowledge. The critic's caveat is right:
the definitions' docstrings and the datasheet captions hand a drafter the exact objects (`mark g`,
`markAll`, `ofList`, `Invariant`, `fiveSubgroups`) and all but transcribe the four gold theorems, so
unanimity is weak evidence of independence. The two places where the English leaves a real choice
are exactly the two where the drafts differ from the published form.

**Fifteen of the seventeen** are, as the judge sees them, the published statements. Two differ in
form and not in meaning. For every theorem the published statement says what the guide says; where
the note, the site or the handoff row says something else, that is recorded below.

### The seventeen, one by one

| theorem | from-English statement, against the published one | the judge should | what the English check turned up |
|---|---|---|---|
| `Move.act_mul` | identical | accept | The site's list cites this name for "Any two of the three moves make the third", which it does not say; no theorem says it for the moves (the handoff's own finding, confirmed; see below). |
| `T1_self_inverse` | identical | accept | A table equation, `mul g g = I`, as the site's line says ("the diagonal is all I"). The guide ("do it twice and the plane is back as it was") and the note ("any move made twice brings you back") promise the plane-level fact `act g (act g p) = p`, which is no named theorem: it is an inline `have` in three proofs. |
| `T1_mul_comm` | identical | accept | Same table-to-plane gap, bridged by `Move.act_mul`. |
| `T1_mem_all` | identical | accept | none |
| `T1_all_distinct` | **different form**, proved equivalent | **reject** by name | The English says the four entries of the list are all different: `Move.all.Nodup`. The published statement is six inequalities between the constructors and never mentions the list; both are faithful to different sentences (the guide's names the list, the handoff row does not). |
| `T2_faithful` | identical | accept | none. The guide's "one point that works for every pair at once" is `T2_probe_injective`, not among the seventeen. |
| `T4_fix_I` | identical | accept | none |
| `T4_fix_sv` | identical | accept | "Leaves exactly the vertical line in place" is true pointwise, which is what the statement says; read setwise, `sv` also carries every horizontal line onto itself. |
| `T4_fix_sh` | identical | accept | Same remark. |
| `T4_fix_C2` | identical | accept | The statement names the centre, which is more than the handoff's "exactly one point". |
| `T7_both_mirrors` | identical (the drafts write `S` explicitly, the published file implicitly; the judge ignores that) | accept | "Survives both flips" could mean the two flips done in turn, which would make the claim trivial; the guide's "whether or not anyone intended it to" settles it as each flip separately, which is the statement. |
| `T8_five_are` | **different form**, proved equivalent | **reject** by name | Four things. (a) The handoff row and the site say "closed"; under the file's own `MoveSet.closed` the empty set is closed, six of the sixteen are, and the literal claim is false; the theorem is about subgroups (identity and closure), as the guide says. "Non-empty and closed" is an equally good repair and coincides with `isSubgroup`. (b) The English yields "one of the five listed" as membership in `fiveSubgroups`; the published form is a five-way disjunction. (c) Neither states the count five; that is `T8_five_count`. (d) The from-English statement is the published `S1_five_iff_subgroup` with its two sides swapped. |
| `S1_one_of_five` | identical | accept | A figure is a predicate on the integer lattice; the guide's "any figure whatsoever" and the note's "flat picture" are wider. The guide's "Scope" section discloses this. |
| `S2_mark_sv_exact` | identical | accept | The theorem is about the ten-point model mark `mark Move.sv`. The sheet's caption and the note say "the mark", which to a reader is the drawn one; the sheet's own station F measures the drawn mark at less than full overlap, and the caption's pointer "Note, test 1" is the print-and-flip test. Only the guide says "model marks". Also, the note's "the σᵥ mark only the left-right flip" literally excludes `I`, which every figure survives; the handoff's "(and doing nothing)" repairs it. |
| `S2_mark_sh_exact` | identical | accept | Same. |
| `S2_mark_C2_exact` | identical | accept | Same. |
| `S2_markAll_invariant` | identical | accept | Same, for the twenty-point `markAll`. |

### The two form differences, and why they stand

`T1_all_distinct`: all three drafters wrote `Move.all.Nodup`. The equivalence with the published six
inequalities was proved by form (a lemma about any four entries, instantiated), not by `decide`,
which would only show both sides true. `T8_five_are`: all three wrote `isSubgroup s = true ↔ s ∈
fiveSubgroups`; the equivalence with the five-way disjunction was proved by unfolding the list and
nothing else. Both are left as written. The judge compares stored terms and unfolds nothing, so it
reports each as `Challenge and solution theorem statement do not match`; that report is the record
of the difference, which is the point of writing the statements from the English. The published
statements are not wrong, and nothing here asks for them to change; a next version may state
`T1_all_distinct` about the list and `T8_five_are` through the list, or leave them as they are.

### Findings for the next version, ranked

1. **"Exactly five sets of moves are closed" is false as written**, on the site ("How the four fit
   together") and in the handoff row: the empty set is closed, so six are. The theorem proves the
   true sentence, which the guide already has: five are subgroups (contain `I` and are closed).
   *Corrected in release 1.3.0:* the site now says "exactly five contain I and are closed".
2. **The site cites `Move.act_mul` for "Any two of the three moves make the third"**, which it does
   not state. For the moves the fact is three entries of the table (`mul sv sh = C2` and the two like
   it, each `rfl`) plus `Move.act_mul`; for figures it is the T7 trio. A direct theorem,
   `act sv (act sh p) = act C2 p` and the two like it, is one line each and uses no axiom (the critic
   compiled both forms).
   *In release 1.3.0* the site cites `Move.mul, Move.act_mul`, the table and the theorem that ties it to the plane; the
   direct theorem waits for the next version of the proof file.
3. **Two statements differ from the published ones in form** (`T1_all_distinct`, `T8_five_are`),
   as above. The judge will name them; that is expected.
4. **The plane-level "each move undoes itself" and "order does not matter" are unnamed.** The guide
   and the note promise them; the file proves table equations and uses the plane-level fact only as
   an inline `have` in three proofs. Candidates for named theorems.
5. **The axiom footprint is a Lean 4.33.0 footprint.** Under 4.36.0 the four `S2` mark theorems
   gain `Classical.choice` (seventeen: 6 / 3 / 0 / 8; all 118: 61 / 22 / 10 / 25 against the
   published 61 / 22 / 21 / 14). Hermes found it; this Mac reproduces it. No verdict moves. The
   guide's axiom table should say which Lean it was read under.
6. **Model marks, not drawn marks.** The `S2` captions and the note say "the mark"; the theorems are
   about five-point seeds and their images. The guide discloses it; the sheets and the note do not,
   and the sheets point at the physical test. A clause on the sheets or in the note would close it.
7. **"Exactly five" is a count the statement does not carry**; `T8_five_count` does. A reader who
   wants the count in `T8_five_are` would add that the five are distinct (`fiveSubgroups.Nodup`,
   which `decide` proves).
8. **The datasheets cite release 1.1.0**, and this check targets 1.2.0; the proof file is
   byte-identical at both tags, so nothing changes, but the handoff should say so.
9. **The site's "no figure survives exactly three" cites `S1_no_three_element_symmetry`**, which is
   `T7_both_mirrors` applied, and rules out only the `{I, sv, sh}` pattern directly; the full claim
   rests on `S1_one_of_five`.
10. **`deriving Repr` on `Move` is load-bearing for the judge.** Lean reuses the matcher it generates
    for `Repr` (`instReprMove.repr.match_1`) in `MoveSet.mem`, so that constant is in the closure the
    judge compares. The definitions must be copied with their `deriving` clauses, as they are here.

The closure itself is identical: 35 constants of the module, the same names, the same canonical type
and value in the challenge and in the published file (the critic checked it with the rehearsal's
dumper; the rehearsal below checks it again).

### The judge, rehearsed on this Mac without its sandbox

Lean 4.36.0 (`lake comparator --inadvisably-no-sandbox`, macOS 27.2.1, arm64), on 23 November
2026. Without the sandbox the verdicts are not trustworthy as verdicts; they are exact as a
prediction of what the judge prints, and both files are this project's own.

| run | configuration | result |
|---|---|---|
| 1 | `comparator.json`, all seventeen | exit 1, `Challenge and solution theorem statement do not match: 'T1_all_distinct'`. The judge stops at the first mismatch, in the order of `theorem_names`, and judges nothing after it |
| 2 | `comparator-15.json`, the fifteen | exit 0, `Lean default kernel accepts the solution`, `Your solution is okay!` |
| 3 | `comparator-T1_all_distinct.json` | exit 1, mismatch named `T1_all_distinct` |
| 4 | `comparator-T8_five_are.json` | exit 1, mismatch named `T8_five_are` |
| 5 | `comparator-15.json --paranoid` | exit 0, accepted by Lean's kernel, Lean paranoid (`leanchecker-paranoid`), lean4lean, nanoda, con-leche and con-ron |

`rehearsal/rehearse.sh`, under Lean 4.33.0, reports exactly the two statement differences and no
difference in the 35 closure constants.


## Files

| file | what it is |
|---|---|
| `Challenge.lean` | the seventeen statements, each `:= sorry`, after the definitions copied unchanged from `../TetrasemaphoreAlgebra.lean` at `v1.2.0`; no imports, as the published file |
| `comparator.json` | the judge's configuration: challenge module `Challenge`, solution module `TetrasemaphoreAlgebra`, the seventeen names, and the permitted axioms `propext`, `Quot.sound`, `Classical.choice` |
| `comparator-15.json` | the same, for the fifteen statements the judge should accept |
| `comparator-T1_all_distinct.json`, `comparator-T8_five_are.json` | the same, one theorem each, so the judge names each form difference on its own |
| `export-targets.txt` | the names to export when the judge is given exports instead of building (route B below): the seventeen, the three axioms, `Quot` and the primitives Lake itself exports |
| `lakefile.toml` | the Lake workspace: library `Challenge` from this folder, library `TetrasemaphoreAlgebra` from the parent folder, in place |
| `lake-manifest.json` | written by Lake; no dependencies. The judge requires one |
| `lean-toolchain` | the judge's toolchain, Lean 4.36.0 (`lake comparator` exists from 4.35). The proofs themselves pin 4.33.0 in `../lean-toolchain`; see the two routes |
| `rehearsal/` | a local rehearsal of the judge's statement comparison, without the judge: `rehearse.sh` |
| `RESULT-lab-pc-2026-11-23.md` | Hermes's record of the judge's run on lab-pc: versions, configurations, verdicts, the outside checkers, and its own corrections |

## Running the judge (Part 2, Hermes, on lab-pc)

Hermes's readiness note of 23 November 2026 (`lean-statement-check-part2-readiness-20261123.md`)
measured lab-pc: Ubuntu 24.04.5, kernel 7.0.0-43-generic, bubblewrap 0.9.0 (with a user-namespace
grant scoped to `/usr/bin/bwrap`, since Ubuntu 24.04 restricts unprivileged user namespaces), Lean
4.33.0 and 4.36.0, and `lake comparator` proven on three controls (a true theorem accepted, a
changed statement rejected by name, a self-declared axiom rejected by name) with all five bundled
checkers running. Hermes's harness, `~/lean-statement-check/run.sh` there, pins the published file
to its v1.2.0 sha256, refuses to override the seventeen names, refuses definition holes, and runs
two judgements:

- **Run A**, both files built with Lean 4.33.0, the proofs' own pin, and judged plain (Lean's
  kernel) by the 4.36 comparator from exports. This is the route the handoff describes and the one
  the Riemann Hypothesis check used. `--paranoid` is not meaningful here: Hermes and the Riemann
  Hypothesis checkers both found that lean4lean from Lean 4.36 rejects every 4.33-built export
  (`unknown constant 'Decidable.intro'`, because 4.36 redefined `Decidable`) and that nanoda panics
  on `Lean.trustCompiler`, machinery removed in 4.35. Neither has anything to do with these proofs.
- **Run B**, both files built with Lean 4.36.0, judged plain and `--paranoid`, so all five external
  checkers (leanchecker-paranoid, lean4lean, nanoda, con-leche, con-ron) are meaningful. The
  published file compiles unchanged under 4.36.0 (118 axiom lines, no errors, no warnings; checked
  on lab-pc and on this Mac).

Hermes's harness copies the published file under the module name `Solution`; the configuration in
this folder names it `TetrasemaphoreAlgebra` and judges it in place. The statements file is the same
either way: nothing in `Challenge.lean` depends on the solution's module name.

To run the judge from this folder instead of from the harness, the requirements are those of
`lake help comparator`: Linux, `bwrap` on `PATH`, not root, no `.lake` folder (a clean state), Lean
4.36.0 through elan (this folder's `lean-toolchain`). Exit codes: 0 accepted, 1 rejected
(statement mismatch, forbidden axiom, kernel rejection or a failed build), 2 could not start.

```bash
cd proofs/comparator
rm -rf .lake
lake comparator                  # Run B, plain: Lean's kernel
rm -rf .lake
lake comparator --paranoid       # Run B, paranoid: the five bundled checkers too
```

Add `--json` to either for a machine-readable report of every step. The configuration names no
`external_kernels`: Lake looks those up on `PATH`, where elan's proxies do not put the toolchain's
checker binaries, so `--paranoid`, which finds the bundled checkers itself, is the second run.

Run A from this folder, by exports:

```bash
cd proofs/comparator
rm -rf .lake
lake +leanprover/lean4:v4.33.0 build
# lean4export at its tag v4.33.0, built with Lean 4.33.0: https://github.com/leanprover/lean4export
LEAN_PATH="$PWD/.lake/build/lib/lean" <path-to-lean4export> Challenge -- $(cat export-targets.txt) > challenge.export
LEAN_PATH="$PWD/.lake/build/lib/lean" <path-to-lean4export> TetrasemaphoreAlgebra -- $(cat export-targets.txt) > solution.export
# from an empty directory
lake +leanprover/lean4:v4.36.0 comparator --config /path/to/proofs/comparator/comparator.json \
  --challenge-from-export /path/to/challenge.export --solution-from-export /path/to/solution.export
```

Every name in `export-targets.txt` exists in Lean 4.33.0 and 4.34.1 (checked). Lake 4.33.0 builds
this folder although its `lean-toolchain` names 4.36.0 (checked); the `+toolchain` form is elan's.

**The axiom footprint is version-pinned.** Hermes found, and this Mac reproduces, that the same
source reports different footprints under the two toolchains. Under 4.33.0 the seventeen are six
with no axiom, three with `propext`, four with `propext, Quot.sound` and four with all three, as
`STATEMENTS.md` records. Under 4.36.0 the four `S2` mark theorems gain `Classical.choice`, so the
count is six, three, none and eight; across all 118 theorems the published 61 / 22 / 21 / 14
becomes 61 / 22 / 10 / 25. The permitted list covers both, so no verdict moves; but the published
axiom line is a 4.33.0 line, and a reader re-deriving it under a newer Lean will see a difference
that is not a defect. That is a sentence for the next version of `README_LEAN.md`.

**What to post.** `lean --version` and `lake --version` for each toolchain used, `bwrap --version`,
`uname -r`, the exact commands, and the judge's complete output or JSON for every run, pass or
fail. If a checker cannot run for a reason unrelated to the proofs, name it and say why; do not
count it as a pass.

**Expected result.** The judge stops at the first theorem whose statement differs, so the five
configurations above give five runs, each with a predicted verdict (the table in "What the check
found"): all seventeen, rejected at `T1_all_distinct`; the fifteen, accepted, plain and
`--paranoid`; and each of `T1_all_distinct` and `T8_five_are` alone, rejected by name. The two
exports of Run A serve every configuration, since `export-targets.txt` carries all seventeen. A
rejection the table does not predict is a new finding; so is an acceptance where it predicts a
rejection.

## The local rehearsal

`rehearsal/rehearse.sh` compiles `Challenge.lean` and the published file with the proofs' own Lean
(4.33.0, pinned in `rehearsal/lean-toolchain` and passed to every `lean` call explicitly), then
prints each of the seventeen statements, and every constant of the module the statements use, in
the form the judge compares, and diffs the two listings. The judge's comparison is `Lean.Expr.eqv`
on the stored statement (alpha-equivalence: binder names and binder annotations ignored, nothing
unfolded), and, for every definition the statements reach, equality of the whole constant, value
included. The rehearsal erases exactly what `Expr.eqv` ignores and compares the rest. An empty diff
means the `compare_statements` step should pass; a non-empty one names what differs. It is not the
judge: no sandbox, no export, no kernel replay, no axiom check.

```bash
proofs/comparator/rehearsal/rehearse.sh
```

## What this check will not show

- That the statements mean what the note means. The judge compares terms. The question "do these
  seventeen statements say what the note says?" is for a reader, and it is the one question to put
  to a mathematician the day one is available.
- Anything about the artwork, or about people. Lean covers the algebra of four moves on the integer
  plane and five-point model marks; whether a printed mark survives its move is measured on the
  files, and whether the semaphores help anyone think is a test with people (the note, "How to
  test it").
- An outside review. Both lanes here are Claude models.
