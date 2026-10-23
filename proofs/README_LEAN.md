# The Tetrasemaphore algebra, machine-checked

`TetrasemaphoreAlgebra.lean` is a proof file. A computer reads it and checks every
step; nothing in it is taken on anybody's word, including mine.

What it is about is small and worth stating plainly. There are four ways to move the
plane that the coins use, and only those four are used here:

| name | move | what it does to the point `(x, y)` |
|---|---|---|
| NORMATIVE | `I` — the identity | `(x, y)` — leaves everything where it is |
| NON-NORMATIVE | `sv` — mirror in the vertical axis | `(-x, y)` — left and right swap |
| METACOGNITIVE | `sh` — mirror in the horizontal axis | `(x, -y)` — top and bottom swap |
| CRITICAL | `C2` — the half-turn | `(-x, -y)` — the page is turned upside down |

Everything below follows from those four lines.

Two adversarial passes have gone through this file looking for exactly the failure that
makes machine-checked proofs worthless: statements that type-check, sound impressive, and
restate their own definitions. Those reviews are in `RED_TEAM_LEAN.md`, they are candid,
and reading them alongside this document is the honest way to read either. Six claims
this README used to make turned out to be stronger than anything in the file; they are
now theorems — `S1_one_of_five`, `S3_fml_swapVH` with `S3_no_formula_separates_mirrors`,
the three `allSubs` theorems `S0_MoveSet_ext`, `S0_allSubs_nodup` and
`S0_allSubs_exactly_once`, `S2_realizes_stab` with `S2_quadrant_mark_exact`,
`T6_three_interchangeable`, and `S4_eight_are_all` — and the review says where each was
and what was done. The most recent of
them — that the file covers *all eight* symmetries of the square — is the subject of S4
below.

A third pass rewrote the checking script. An independent reviewer observed that a gate
which reads a file with `grep`, and reads the axiom footprint out of the text Lean
prints, is asking the file under test to describe itself. Five ways of giving a false
answer to that question are recorded in the review; the script now reads the footprint
out of the compiled module instead.

A fourth pass answered a second, longer review from the same reviewer, who built an
adversarial corpus against the third-pass gate and ran all of it. Every file in that
corpus was replayed here; what the replay found, and the nine changes it prompted, are in
`RED_TEAM_LEAN.md`. The one new companion file is `STATEMENTS.md`, described below.

## Checking it yourself

```
./check.sh
```

This folder is version 2.4.2. `check.sh`, `TetrasemaphoreAlgebra.lean`, `STATEMENTS.md`,
`check_output.txt`, `lean-toolchain` and every attack file are byte-identical to the version
2.4 that the second reviewer re-ran on 22 October 2026, so its verdicts hold for this folder.
What changed since then is prose and the run index: version 2.4.1 answered the re-run's
findings, and version 2.4.2 answers the eight items its read of 2.4.1 raised: seven are corrected (a false
pointer, a table that split in two, stale numbers and wording) and one needed no change. The two passes are
listed in `CHANGES_v2.4_to_v2.4.1.md` and `CHANGES_v2.4.1_to_v2.4.2.md`, and checked in
`SCIENCE_CHECK_v2.4.1.md` and `SCIENCE_CHECK_v2.4.2.md`.

That is the whole thing — the script is committed executable, so there is no `chmod` step.
It reads the file, runs it under each of the three Lean toolchains it lists (4.32.2,
4.33.0, 4.33.1) that is installed, compiles it and audits the compiled module under each,
and prints what it finds. It ends in `OK` or in `FAILED`, and its exit code says the same
thing, so it can sit in a build. Expect one to three minutes depending on the machine:
nine Lean runs, three of them full audits of the compiled module. Measured 69 to 117
seconds on a sixteen-core machine, including runs with several other copies of the gate
going at once. Run it from inside this folder; given no arguments it reads the three files
beside it by name. The `lean-toolchain` file names the primary version,
`leanprover/lean4:v4.33.0`, for `elan`'s benefit — a reader who types `lean` in this
directory gets that version from elan's proxy. The gate itself does not call `elan` and does
not read that file: it names all three toolchains by path under `$HOME/.elan/toolchains/`
(or `$ELAN_HOME`), so it runs the versions it says it runs. There is no `lakefile`, and
none is needed: one file, zero imports, and the gate calls `lean` directly.

The script pins `LC_ALL=C` before it does anything. Two things depended on the
locale and neither should: `sort` and `comm` collate differently under a UTF-8 locale,
which moved two dozen lines of the gate's own output without changing the verdict; and a
pattern carrying a multi-byte character behaves differently under C, where each byte is
a character. The recorded `check_output.txt` is a run under `LC_ALL=C`.

It also tests its own source checks before it runs them. Each of the eight patterns is
given a line it has to match — including four spellings of `sorry`, one of them written
`@«sorryAx»` — and the set is given an honest line none of them may match. Since 2.3 the
scanner is probed in both directions as well: a banned word inside a string literal has to
be blanked, and a declaration behind a doc comment on the same line has to survive. Since
2.4 four more probes run: a line ending in a character literal, and a line ending in a raw
string, each has to leave the *following* line visible; a primed name like `g'` has to not
read as a character literal; and the scanner has to finish the probe file in open code
rather than inside a string, a comment or a literal. A check
that cannot fire looks exactly like a clean file in the output, so if the self-test
disagrees the gate stops there rather than reporting a pass. That test exists because version 2.1's
`sorry` check was inert in a C locale for exactly that reason, and nothing in its output
said so.

Two things about *how* it is run, because a reviewer found that both mattered. It is a
bash script and it checks that it is one: run as `sh check.sh`, bash enters POSIX mode,
where some of the script's constructs are syntax errors — the earlier version lost two of
its checks that way and still printed `OK`. This version stops with an explanation
instead. And it no longer assumes that the three toolchains it names are present: it runs
each one that is installed, falls back to whatever `lean` is on `PATH` when none is, says
in its output exactly which ones ran, and claims all three only when all three ran. A
machine with no Lean at all gets a failure rather than a quiet pass. It also checks, before
anything else, that every program it runs is on `PATH`, and gives `comm` and `join` a pair
of files whose answer is known. Three of its checks are a `comm` whose empty output means
agreement; with `comm` absent from `PATH`, version 2.2 printed those three as clean and
exited zero on a file that a full `PATH` catches.

The recorded `check_output.txt` is this machine's run, offered for comparison. Six of its
lines carry a target triple and commit hashes — `arm64-apple-darwin24.6.0` and the release
commits of each toolchain, printed once in section 2 and once in the summary. Those are
properties of the machine and the build, not of the proof: the same release on another
platform prints a different triple, and on another build of the same release the commit
does not. Compare the counts, the per-theorem footprints and the verdict; the version
banners will differ. Version 2.2 printed three further lines carrying the full path of each
toolchain, and so the username of whoever ran it; 2.3 prints those relative to the elan
root, so a run on another machine with the same three releases differs in no line at all,
and on another platform in six.

The script is deliberately suspicious, for a reason the earlier `dns-tool-proofs` gate
learned the hard way: Lean accepts the word `sorry` in place of a proof, and reports it
only as a *warning*. A file full of `sorry` compiles, exits zero, and proves nothing. So
the gate fails on `sorry` or `sorryAx` written in the file, on Lean's own warning about
it, and on a theorem that turns out to rest on it. It also fails on `native_decide`
(which hands the checking to the compiled program instead of Lean's kernel), on any
`axiom` declaration (which would let a claim in with no proof behind it), on `unsafe`,
`partial` and friends, and on any `import` — this file rests on core Lean and nothing
else, so there is no library to inspect or to trust.

Two checks were added in the second pass, both because the review found the gate could
be walked past:

- **`set_option debug.skipKernelTC true`** switches off kernel typechecking and leaves
  the build green, with no `sorry`, no added axiom and no import. It was the quietest
  way to fake a file that otherwise looks impeccable. The gate now refuses `set_option`
  altogether: this file needs none, and a list of harmless options is a surface worth
  not having.
- **Every theorem is followed by its own `#print axioms` line**, and the gate fails if
  one is missing, or if the number of axiom lines in the build output differs from the
  number of theorems declared. The earlier version printed 55 of 64, which left the
  footprint a selection rather than a complete account.

### What the third pass changed

The second-pass gate still asked the file to describe itself, in two places: it decided
what the file contained by running `grep` over the source, and it read the axiom
footprint out of the text Lean printed. A file can write both of those. It can print its
own footprint with `#eval IO.println`, swallow the real one with `#guard_msgs(drop info)`,
reach the compiler through `decide +native` rather than the banned word `native_decide`,
hide that spelling behind a `macro_rules` alias, or put an attribute in front of `axiom`
so that the line no longer begins with the word. Each of those walked past the second
gate, and `RED_TEAM_LEAN.md` records the runs.

Three things changed, and they are worth describing because they are the difference
between a gate and a formality.

- **A list of the commands a proof file is allowed to begin a line with.** Declarations,
  comments, `namespace`, `open`, and `#print axioms`. Everything else is refused —
  `#eval`, `#exit`, `#guard_msgs`, `syntax`, `macro`, `macro_rules`, `notation`,
  `set_option`, `axiom`, `opaque` — and so is any line the list does not recognise, which
  is the direction a gate should fail in. Reading the first word of a line turned out not
  to be enough, and version 2.3 says so: `open Nat in #eval …` satisfied that list and ran
  disk IO while the gate was running, and so did an `#eval` that was merely indented,
  because Lean accepts a top-level command at any column. Those commands are refused
  anywhere on a line of code now, at any column and after any number of `in`s, with
  `#print axioms <name>` the one `#`-command this file uses. The source checks read the
  file with its comments blanked out — and, since 2.3, the inside of its string literals
  as well — rather than skipping lines that happen to start with a comment marker: prose
  inside a doc comment does not trip them, a doc comment in front of a declaration does
  not hide it, and an honest `String` that carries one of the refused words as prose,
  which version 2.2 refused, does not fail the run. When any of these checks refuses a line
  the gate stops there, before section 2: it does not elaborate a file it has just refused,
  because elaborating a Lean file runs code the file contains.
- **The axiom footprint is read from the compiled module.** The file is built to an
  `.olean`; the script then writes its own small Lean program, imports that module, walks
  every constant defined in it — all 671 of them, not only the 118 theorems — and
  collects the axioms each one actually depends on. The file cannot write into that
  output: it is produced by a program the gate wrote, from the compiled artifact. The
  footprint the file prints about itself is then compared against it, so a forged line is
  a disagreement rather than a lie.
- **The theorems in the compiled module are checked against the ones the source
  declares**, allowing only the lemma shapes Lean generates for `inductive`, `structure`
  and `deriving`; and every Lean name this README cites in backticks is looked up in the
  compiled environment. A theorem that was not elaborated — because `#exit` cut the file
  short — is not a theorem, and a README that cites a theorem the file does not have is a
  README that has drifted.

### What the fourth pass changed

The third-pass gate read every constant of the compiled module for its axiom *report*,
but made its decisions about theorems only. The reviewer found the gap and named it: an
`abbrev ZA : False := by admit` is not a theorem, so an audit that enumerates theorems
walks past it with an admitted contradiction in the environment. Five changes follow from
that review, and four more from the rest of it.

- **The audit reads every constant, of every kind** — theorem, definition, abbreviation,
  instance, opaque, constructor — and computes each one's axioms by walking the compiled
  environment. Axiom names are compared by exact match against `propext`,
  `Classical.choice` and `Quot.sound`, so a declaration called `propext2` is not mistaken
  for one of them. A constant whose type is a proposition but which is not a theorem is
  refused outright: that is a proposition proved by a definition, which is the shape the
  gap had.
- **The imports are read from the compiled module's own header**, where the source text
  cannot reach them, and each one has to be `Init`.
- **Every declaration is re-added to a fresh `Init`-only environment through the kernel.**
  The entry point used is `Kernel.Environment.addDecl`, which is the kernel's own and has
  no parameter for switching the check off, so a build made under
  `debug.skipKernelTC true` is re-checked here from nothing. The audit also loads the
  module with its environment extensions unloaded, so no `initialize` block and no
  `@[init]` function runs inside it.
- **The audit is run by the same toolchain that compiled the module.** A 4.34 program
  reading a 4.33 `.olean` fails closed on an incompatible header, which is a failure and
  not a result; the script passes each toolchain its own sysroot so the question does not
  arise.
- **Private declarations are refused**, apart from the pattern-matching auxiliaries Lean
  generates for its own definitions. A private theorem needs no `#print axioms` line of
  its own, is invisible to the source-level count, and would not appear in the listing
  below; a file published as a proof has nothing it needs to hide from its own listing.
- **The source checks are run twice**, once over the file and once over a copy with the
  line breaks collapsed, because Lean reads a newline as whitespace and `set_option` on
  one line with its argument on the next is one command.

**`STATEMENTS.md`, the companion file.** The gate checks how the proofs were made. It
cannot check what they say, and the reviewer showed one way that matters: a `notation`
can be declared that renames a constant, after which `#check` displays a theorem about
`Z_fakeDet` as a theorem about `Move.det`. So the gate now writes `STATEMENTS.md` — every
theorem of the compiled module, its axioms, and its elaborated statement — regenerates it
on every run, and fails if the regenerated listing differs from the committed one. The
statements there print as plain constant applications, `Eq a b` rather than `a = b`,
because the audit loads the module with its environment extensions unloaded and sets
`pp.notation false`: no `notation`, no user delaborator and no unexpander runs while a
statement is printed, so nothing a `notation` declares can change which constant a row
names. Lean's own builtin delaborators do run — binders, `fun` and field notation
(`f.holds r`) are theirs — and with the class table unloaded an instance projection prints
under its own name, `List.instMembership.mem L q` rather than `Membership.mem`. It is where
a reader audits what is claimed, which is the part no script does.

**What that listing shows, and what it does not.** Stated exactly, because the second
reviewer got through the sentence that used to stand here. It shows every theorem's
elaborated statement with the axioms it rests on; every definition's kind, type and body;
and, since 2.3, every constant Lean generates underneath those definitions, which is where
the equation lemmas say which arm of a definition by cases belongs to which constructor —
`Fml.holds.eq_4` says outright that the `Fml.andF` arm is the conjunction, and the printed body
of `Fml.holds` does not. What it does not show is the instance a numeral elaborated
through: `16` prints as `16` whichever `OfNat` instance bound it. A reviewer used that —
an instance hidden under a name Lean's own `Name.isInternalDetail` calls internal, `_i` or
the innocent-looking `proof_1` — to rebind the `16` in `T8_sixteen`, which became
`allSubs.length = allSubs.length` with this file byte-identical. The gate reports such a
name now, and any `OfNat` instance the module declares, each by name; the listing is the
other half of that answer. The same reviewer then rebound the `16` through an `abbrev`
wrapper instead of an instance, which is not an `OfNat` declaration and was not reported.
Since 2.4 the gate stops naming classes one at a time: it reads the head of every
declaration's type and of every definition's body, unfolds reducible wrappers, and fails
on any head outside the set this file's own honest declarations produce — thirteen heads
in types, seven in bodies, the same set under all three toolchains, with a head that is
one of this file's own declarations accepted as such. An `OfNat`, a `Neg` or
a `LT` appearing anywhere in the module is outside that set whatever it is spelled
through. The listing also carries no attributes, and
under a toolchain outside the window it was written in (4.30.0-rc2 to 4.33.1) the rows for
definitions Lean generates are not compared at all, because 4.34 stops generating two of
them.

The same file carries the definitions, bodies included, and for a reason worth stating: a
statement is only as stable as the definitions it names. Changing `seed` from five points
to three leaves every statement about it character for character the same and changes what
all of them mean. A reviewer built that tamper; it is the definitions section of
`STATEMENTS.md` that sees it, not the theorems. One limit of this file is worth a reader's
attention here: the gate compares the committed listing against the one it regenerates, and
a reader who regenerates the listing first — the maintainer's path — gets a green run on a
file whose swap the new listing carries. Ten rows of the third section change under the
`Fml.holds` arm swap, and the third section says so where those rows are. Two weakened statements that kept their names — `T1_mul_comm`
restated as `Move.mul g h = Move.mul g h`, and the `↔` in `S1_one_of_five` weakened to
`→` — were green under the previous gate and fail this one on the line that changed.

The compiled-module audit began life as `VerifyAxioms.lean`, a 139-line prototype written
by the reviewer who found these gaps and shipped with their report. The program the gate
writes is a rewrite rather than a copy — it reads every constant rather than every
theorem, goes through the kernel's own `addDecl`, and emits the statements listing — but
the design, and several of the Lean 4.33 API facts it rests on, came from that prototype.

**The limit under all of it.** Elaborating any Lean file can run code that file contains: `#eval` and the commands beside it run while
Lean reads the file, before a single proof is checked. The source checks and the command allowlist are what stands between a reader and
that code, and they are a list of what their author knew to look for. Since the second build of 2.3 the gate stops before it elaborates
anything when any of those checks has failed, and says that the file was not elaborated — the first build refused a smuggled
`open Nat in #eval (… IO.FS.withFile …)` in its section 1 and then elaborated the file anyway, three times, once per toolchain, which
got the verdict right and ran the code. A reader checking a file from anywhere other than the published folder does that in a sandbox.

**What the gate does not catch, and cannot.** It checks *how* a proof was made: whether
the kernel really ran, whether an assumption was added, whether the footprint is honest.
It does not check that a theorem says what its name says, or that the English in this
document describes the same thing the Lean does. A file of true, kernel-checked,
axiom-free theorems that restate their own definitions would pass every check here, and
that is exactly the failure this whole exercise is about. The only instrument for it is
someone reading the statements. That is what the rest of this document is for, and what
`RED_TEAM_LEAN.md` does adversarially — including by counting how many of the theorems
below are restatements.

## What is proved

One hundred and eighteen results, every one followed in the file by `#print axioms`. One
line each, in words. The three added in the fourth pass are second proofs of statements
that were already there, so the count is 115 net of those three. Counted another way, by
the statements themselves rather than by what they were added for, the 118 rows of
`STATEMENTS.md` carry 114 distinct statement strings — `T4_fix_I` prints exactly as
`Move.act_I` does, and each of the three second proofs prints exactly as its original — and
113 if two that differ only in an implicit binder are read as one.
`RED_TEAM_LEAN.md` counts which of the theorems are restatements of one another.

**T1 — the four moves form a group.** Composing three in a row gives the same answer
however you bracket it. Doing nothing, then a move, is that move. Every one of the four
undoes itself: do it twice and the plane is back as it was. Order does not matter — `sv`
then `sh` is the same as `sh` then `sv`. And the list `[I, sv, sh, C2]` catches every
move in this alphabet, with the four entries all different, so "four" is exact rather
than loose. (`T1_mul_assoc`, `T1_one_mul`, `T1_mul_one`, `T1_self_inverse`,
`T1_mul_comm`, `T1_mem_all`, `T1_all_length`, `T1_all_distinct`.)

The table is tied to the moving by `Move.act_mul`: looking up two moves in the table and
applying the result does the same thing to a point as applying the two moves in turn.
Without that, the rest would be arithmetic about four symbols rather than about the
plane.

**T2 — the four are genuinely different.** Given two different names, there is a point
they send to different places. The proof exhibits one point that works for every pair at
once: `(1, 1)`, which lies on neither axis and so gets moved by all four to four different
corners. (`T2_probe_injective`, `T2_faithful`.)

**T3 — the determinant is a homomorphism, and it sees exactly one distinction.** Each
move has a 2×2 matrix of whole numbers, and `T3_act_matrix` proves the matrix really does
describe the move. The determinant of that matrix is `+1` for NORMATIVE and CRITICAL and
`-1` for the two mirrors, and the determinant of a composition is the product of the
determinants. So the moves with determinant `+1` are exactly NORMATIVE and CRITICAL —
the two that keep the sense of the plane; the two mirrors reverse it. (`T3_det_mul`,
`T3_act_matrix`, `T3_det_eq_ad_sub_bc`, `T3_det_kernel`, `T3_det_mirrors`.)

**T4 — what each move holds still.** This is the part the gold is for. NORMATIVE holds
the whole plane. NON-NORMATIVE holds exactly the vertical axis, and nothing off it.
METACOGNITIVE holds exactly the horizontal axis. CRITICAL holds exactly one point, the
centre. Whole plane, a line, another line, a point: four different kinds of stillness.
(`T4_fix_I`, `T4_fix_sv`, `T4_fix_sh`, `T4_fix_C2`, `T4_mirrors_differ`.)

**T5 — the two mirrors are twins; the half-turn is alone.** Turn the page a quarter turn
and the horizontal mirror becomes the vertical one — `T5_R90_conj_sh` proves exactly
that. Do the same to the half-turn and you get the half-turn back. The file then writes
down eight symmetries of the square (four rotations, four mirrors — the four moves sit
inside as `id`, `mirV`, `mirH` and `rot180`), checks that those eight are eight different
things, and proves the half-turn commutes with every one of them. A consequence worth
reading twice: no symmetry of the square turns the half-turn into a mirror, while a
quarter turn does turn one mirror into the other. (`T5_eight_distinct`,
`T5_C2_commutes`, `T5_C2_conj_fixed`, `T5_C2_never_sv`, `T5_C2_never_sh`.) That these
eight are *all* the symmetries of the square is a further claim, and it is S4 below —
this README used to assert it here, on the strength of a hand-written list of eight.

**T6 — what the algebra cannot see.** Relabel the moves by swapping the two mirrors:
the composition table comes out identical and so does the determinant. Relabel by
swapping `sv` with `C2` instead: the table still comes out identical, but the determinant
does not. So there is a table-preserving relabelling that carries `sv` to `C2`, and
another that carries `sv` to `sh`; what the file proves about the three non-identity
moves is that pair of relabellings, not a general interchangeability. The determinant
adds one distinction the table does not make — half-turn versus mirror — and for the two
mirrors S3 below proves that nothing in that language adds any — the theorem behind that
paragraph is `S3_fml_swapVH`.
(`T6_swapVH_hom`, `T6_swapVH_det`, `T6_swapVC_hom`, `T6_swapVC_breaks_det`,
`T6_three_interchangeable`.) How far that goes is S3 below, and it is further than this
paragraph used to be able to claim.

**T7 — the symmetries of a figure are closed.** If a figure looks the same after one
move and the same after another, it looks the same after the two composed. Every figure
survives doing nothing. The pleasant corollary: a figure that survives both mirrors
survives the half-turn too, whether or not anyone intended it to — and the same for any
two of the three non-identity moves, which always hand you the third. (`T7_invariant_I`,
`T7_invariant_mul`, `T7_both_mirrors`, `T7_mirror_and_turn`, `T7_turn_and_mirror`.)

**T8 — there are exactly five possibilities, and no sixth.** Four moves make sixteen
subsets. Of those sixteen, five are subgroups: `{I}` alone, the three two-element ones
`{I, sv}`, `{I, sh}`, `{I, C2}`, and all four together. Lean checks all sixteen by
enumeration. (`T8_isSubgroup_iff`, `T8_sixteen`, `T8_enum_complete`, `T8_five_count`,
`T8_five_list`, `T8_five_are`, `T8_no_three_element`.) That the symmetries of *any*
figure land in one of those five is a further step, and it is S1 below — this README
used to assert it here as though T7 and T8 together had already said it.

**T9 — the construction rule.** Take any letter or shape at all, add its image under one
of the moves, and the result survives that move. That is the recipe each coin's mark
follows, and it works whatever the letter is, which is why it is a rule rather than a
piece of luck. (`T9_build`, `T9_build_any`.) What it does not give is the other half of
the design claim — that the mark survives *nothing else* — and for a symmetric letter
that half is false. S2 below supplies it.

**T10 — the assignment of states to subgroups.** `stab` is a definition: it writes down
that NORMATIVE is given all four moves and each of the other three states is given
exactly `{I, g}` for its own move `g`. The T10 theorems check that table against itself —
that the four sets are subgroups, are four different ones, and that the trivial subgroup
`{I}` is the one of the five no state uses, so a figure with no symmetry at all has no
state in this scheme. (`T10_stab_subgroup`, `T10_stab_distinct`, `T10_stab_is_pair`,
`T10_stab_I`, `T10_subI_unused`, `T10_det_table`.) Whether any actual figure has these
symmetries is S2.

### The four sections added in the second pass


**S0 — four flags really are a set of moves.** Subsets of the four moves are stored as
four true/false flags. Before counting subgroups it is worth proving that four flags are
the same thing as a set: two of them with the same members are equal, and the sixteen
entries of the enumeration are sixteen *different* sets, each occurring exactly once.
Without this, "five of the sixteen" would be a remark about a hand-written list.
This section also proves that invariance means what it looks like — a figure survives a
move exactly when the figure moved *is* the figure — and that a subgroup here contains an
inverse for each of its members. (`S0_MoveSet_ext`, `S0_allSubs_nodup`,
`S0_allSubs_exactly_once`, `S0_invariant_iff_eq`, `S0_subgroup_has_inverses`.)

**S1 — the symmetries of any figure at all are one of the five.** Take any figure
whatsoever: drawn or not, finite or not, a shape nobody could compute with. The set of
moves it survives is literally one of the five subgroups of T8. This is the sentence the
design rests on — there is no sixth possibility to design for — and it is now a theorem
rather than two theorems read side by side. Arbitrary figures are not something a
computer can test, so the symmetry set is assembled with classical logic, and that shows
up honestly in the axiom lines as `Classical.choice`. (`S1_one_of_five`, with
`S1_symSet_mem`, `S1_symSet_closed`, `S1_symSet_isSubgroup` underneath it.)

**S2 — a mark that survives its own move and fails the other two.** This is the design
claim, proved for model marks. A figure here is a finite list of points with whole-number
coordinates. The lemma that makes the section possible turns invariance — a statement
about every point of an infinite plane — into a finite check on the list, and the reason
it works is that each move undoes itself, so a move carrying the list into itself carries
it back out again. (`S2_invariant_ofList`.)

With that in hand: an L-shaped seed of five points, drawn in the first quadrant so it
touches neither axis, has no symmetry of its own. Add its image under `sv` and the result
survives `I` and `sv` and fails `sh` and `C2`. The same for `sh` and for `C2`. Add all
three images and the result survives all four. So the four sets of moves that `stab`
writes down are the sets of moves four actual figures survive. (`S2_seed_asymmetric`,
`S2_mark_sv_exact`, `S2_mark_sh_exact`, `S2_mark_C2_exact`, `S2_markAll_invariant`,
`S2_realizes_stab`.)

A reader is right to wonder whether the seed was picked to make that come out, so the
general version is proved too: *any* non-empty seed drawn entirely inside the open first
quadrant gives, for each move other than the identity, a mark that
survives exactly that move and the identity. The reasoning is the one a geometer would
give at a whiteboard: the seed together with its mirror image in the vertical axis sits
entirely in the upper half plane, and both the horizontal mirror and the half-turn send
the upper half plane to the lower one, so neither can carry the mark to itself. The
L-shaped seed is then one instance of a general construction, and the three concrete
results above are proved a second time as that instance, so the two routes meet.
(`S2_quadrant_mark_exact`, `S2_mark_sv_exact_via_general`, `S2_mark_sh_exact_via_general`,
`S2_mark_C2_exact_via_general`.)

The hypothesis is doing work, and it is worth saying what falls outside it. A seed that
meets an axis, or straddles one, is not covered: `[(1, 1), (-1, 1)]` lies on neither axis
yet is already symmetric under `sv`, and its `sh`-mark survives all four moves. "Drawn
entirely inside the open first quadrant" is the condition; "off both axes" is weaker and
is not enough.

**S3 — "the algebra cannot see the difference", made into a theorem.** T6 shows one
relabelling that preserves the table and the determinant and exchanges the two mirrors.
The conclusion usually drawn from it is about *every statement* in that language, which
is a different kind of claim and does not follow from one example. So S3 writes the
language down — terms built from variables, the identity and composition; statements
built from equations between terms, equations between their determinants, "not", "and",
"or", and "for every move" — and proves by induction that whatever such a statement says
of NON-NORMATIVE, it says of METACOGNITIVE. The induction is `S3_fml_swapVH`, which is
the general theorem; the headline `S3_no_formula_separates_mirrors` is its one-variable
corollary. The language has no name of its own for any
particular move except the identity, which is the point: a language with a word for `sv`
tells `sv` from `sh` by fiat, and that is a fact about naming rather than about the
group. S3 also checks the language is not empty-handed — it does separate the half-turn
from a mirror, which is T3 said from inside. (`S3_no_formula_separates_mirrors`,
`S3_fml_swapVH`, `S3_language_separates_turn_from_mirror`.)

So the difference between the two mirror coins is not in the algebra at all. It is T4's
geometry: which line each one holds still. A design that claims to render the group
structure can honestly show the determinant pairing and which axis is fixed, and the
difference it cannot show between the two mirrors is one that is not there.

### The section added in the third pass

**S4 — the eight really are all of them.** §6 writes down eight maps, calls them the
symmetries of the square, and checks that they are eight different maps. That is a list
with a distinctness check, and a list is not an argument: nothing in §6 ruled out a ninth
symmetry the author had forgotten. This README nevertheless said "all eight symmetries of
the square", which was a stronger claim than the file contained.

S4 closes it. Each of the eight acts by a 2×2 matrix of whole numbers (`S4_act_matrix`);
that action is linear, which is to say additive and homogeneous (`S4_matAct_add`,
`S4_matAct_smul`); and it carries the four corners `(±1, ±1)` of the square onto
themselves — into them, and every corner coming back from one (`S4_corner_maps`,
`S4_corner_onto`). The eight are closed under composition, by a table proved to *be*
composition of the maps rather than to resemble it, with the identity and with inverses
(`S4_comp_act`, `S4_comp_assoc`, `S4_id_comp`, `S4_comp_id`, `S4_comp_inv`,
`S4_inv_comp`).

Then the converse, which is the part that turns a list into a classification: every
integer 2×2 matrix that carries the corner set onto itself is the action of exactly one of
the eight (`S4_entries`, `S4_classification`), and the two halves together are a single
biconditional (`S4_eight_are_all`). There is no ninth to find.

The argument is the one a geometer gives at a whiteboard. A linear map is fixed by where
it sends `(1, 1)` and `(1, -1)`; both images have to be corners, which leaves sixteen
candidate matrices; and every corner has to be the image of something, which kills the
eight candidates that collapse the square onto a diagonal. The eight that survive are the
eight. Lean does the sixteen cases; the reasoning is not hidden in them.

## Reading the axiom lines

After each theorem the file prints one of two things.

`does not depend on any axioms` — 61 of the 118 — means the proof is pure computation that
Lean's kernel ran to completion. There is no assumption underneath it at all.

`depends on axioms: …` — the other 57 — means the proof used one or more of the three
standard axioms that come with Lean itself. The breakdown:

| axioms | theorems |
|---|---|
| none | 61 |
| `propext` | 22 |
| `propext`, `Quot.sound` | 21 |
| `propext`, `Classical.choice`, `Quot.sound` | 14 |

They arrive through the `simp` and `omega` tactics, and in fourteen cases through the
classical symmetry set of S1, the three T4 fixed-point theorems, and the `omega` calls in
S4. They are the standard foundation that nearly all Lean and Mathlib work rests on. What
matters for reading this file is the negative: no axiom specific to the Tetrasemaphore
appears anywhere, and `sorryAx` — the marker Lean leaves when a proof was skipped —
appears nowhere. Since version 2.1 the gate checks this against the compiled module
rather than against the lines the file prints, and it checks every constant the module
defines, not only the theorems.

## What is *not* proved

**1. Nothing here says the printed or rendered artwork has these symmetries.** S2 proves
that a particular finite set of integer points survives exactly one move. A rendered mark
is strokes with width, font outlines, antialiasing, gold and a die. Whether an actual mark
comes back to itself under its own move — and, just as important, whether it *fails* the
moves it is supposed to fail — is measured on the files, by rendering and comparing. A
proof and a measurement are different kinds of evidence, and conflating them is how a
design claim quietly becomes untrue. What S2 adds is that the target is coherent: there
exists a figure with exactly the symmetry the design asks for, and a general recipe for
building one from any letter drawn entirely inside the open first quadrant.

**2. Nothing here says the state names are the right meanings.** That NORMATIVE goes with
the identity, CRITICAL with the half-turn, and so on, is a convention chosen by the
designer. The algebra constrains the choice a little — T4 and S3 together say the two
mirrors can be told apart only by which axis each holds still, so the difference the
mathematics supplies between the two mirror coins is their orientation. The coins' colours
are a convention laid on top of that, like the names — but the algebra does not pick the
names. It cannot. Names are what people agree to.

**3. Nothing here has anything to do with seL4.** seL4's proof is about an operating
system kernel: that its isolation behaves as specified, that one process cannot reach
another's memory. It is a magnificent piece of work and it is about a different subject.
Running Lean on top of a verified kernel would say something about the machine the
checker ran on; it would add nothing whatever to the mathematics checked here. The
theorems above are true independently of what computer reads them, which is rather the
point of a proof. If someone offers seL4 as evidence for a mathematical claim, the two
have been mixed up.

**4. "Only four moves" is a choice of alphabet, not a discovery.** The file declares four
and proves things about them, and S4 proves that the square has exactly eight symmetries,
of which those four are a part. What is *not* proved — what could not be — is that four is
the right number to build a sign system on. The plane has many more symmetries than eight,
and the square is itself a choice. The four are the four the coins use.

**5. S3's result is about S3's language.** Composition, the identity, equality,
determinant-equality, and "for every move". A language that can also name a particular
move, or quantify over points of the plane, is a different language and the theorem says
nothing about it.

**6. S2's general construction carries a hypothesis.** The seed is non-empty and lies in
the open first quadrant. A seed that meets an axis, or straddles one, is outside the
theorem — and for some such seeds the conclusion is false, since a letter already
symmetric in the horizontal axis yields a mark that survives all four moves. The
hypothesis is the content of the theorem rather than a technicality in it.

## Scope

Coordinates here are whole numbers. The *statements* do not depend on that: they use
arithmetic that holds for coordinates in any torsion-free abelian group, for example that
`-(-x) = x` and that `-x = x` only when `x = 0`. So the same statements are true in the
real plane, where a design lives. The *proofs* are another matter, and an earlier version
of this file claimed otherwise in its header: several of them close with `omega`, a
decision procedure for whole numbers, or with `decide` on integer arithmetic, and neither
survives the move to ℝ. A real-plane version would need different tactics and Mathlib,
which defines the real numbers. That version has not been written; until it is, the
real-plane claim rests on the reasoning above rather than on Lean.

A Mathlib version could go further: state the group over `ℝ`, and connect it to Mathlib's
own `IsKleinFour`, which would get the general theory of the Klein four-group for free and
would let the subgroup count follow from general results instead of from checking sixteen
cases. That has not been done, on purpose. Importing Mathlib means depending on a large
body of code, and this file was written to rest on core Lean alone so that the check is
self-contained and quick. The present proofs are complete as they stand; a Mathlib version
would be more connected, not more certain.

## How a skeptic can check this

Five steps, in increasing order of how much they tell you.

**1. Install the toolchain and run the gate.** Install `elan` (https://github.com/leanprover/elan), then

```
elan toolchain install leanprover/lean4:v4.33.0
elan toolchain install leanprover/lean4:v4.32.2
elan toolchain install leanprover/lean4:v4.33.1
./check.sh
```

It takes one to three minutes depending on the machine: three elaborations, three
compilations to `.olean`, and three runs of the audit program, which re-adds every
declaration through the kernel. A clean run ends in `OK` and exits zero. Three toolchains
are run because a result that depends on one compiler version is a result about that
compiler; the output names the ones that ran, and the `OK` line says "all three" only when
all three were installed. These three are also the window the statements listing belongs
to. The 118 theorems elaborate with no errors on every release from 4.30.0-rc2 to 4.34.1,
but the set of definitions Lean *generates* is not the same across all of them: 4.34 stopped
generating Move.toCtorIdx and Sq.toCtorIdx (written without backticks here because 4.34 is the
release that removes them), which the listing carries. Under a toolchain
the gate does not list, a listing difference confined to rows for definitions Lean generates
is reported as toolchain drift rather than as tampering, and the gate says which rows it
then left uncompared. Version 2.2 failed the honest file under 4.34.1 with the tampering
message, which is the wrong thing to tell a reader.

**2. Read the axiom lines in the output.** The gate prints the footprint it read out of
the compiled module — 164 lines, which is the 118 theorems plus the 46 lemmas Lean
generates for the `inductive` and `structure` declarations and audits alongside them. It
then reports, separately, whether the 118 lines the file prints about itself agree with
what the audit found. Anything other than `propext`, `Classical.choice` and `Quot.sound`
would be an assumption smuggled in, and `sorryAx` would mean a proof was skipped. The gate
fails on either, and fails as well if the file's account and the audit disagree.

**3. Try to break it.** The obvious experiments — replace a proof with `sorry`, add an
`axiom` and use it, change a `decide` to `native_decide`, add an `import`, add
`set_option debug.skipKernelTC true`, delete a `#print axioms` line — are all rejected,
most of them by two or more independent checks. So are the subtler ones that the previous gate
nonetheless caught: `decide +native` in place of `native_decide`, a `sorry` wrapped in
`#guard_msgs(drop warning)`, `@[simp] axiom` so that the line does not begin with the
word. The interesting experiments are the six that the previous gate did *not* catch:
swallow a `#print axioms` line with `#guard_msgs(drop info)` and print a clean one with
`#eval IO.println`; define a command of your own with `syntax` and `macro_rules`; write
`@[ extern "…"]` with a space after the bracket; move `set_option debug.skipKernelTC true
in` off the start of a line; hide `decide +native` behind a macro alias *and* forge its
footprint; declare into `namespace Lean` to poison the checking script's own machinery.
Seventeen such files were built and run in the third pass. In the fourth, an independent
reviewer's corpus of 236 adversarial and tamper files was replayed against the gate as
well, and five attacks and three tampers from that review were written against the version
that came out of it. In the fifth pass a second reviewer, on a different model, found one
way through 2.2 and twelve narrower defects; the corpus was replayed again, and the attacks
of that pass — a hidden instance rebinding a numeral, the same under the name `proof_1`, an
`extern` attribute in second position, a swap of two match arms, an `#eval` smuggled past
the allowlist, a missing `comm`, a misspelled README path and a toolchain outside the
listing's window — were rebuilt and re-run.
`RED_TEAM_LEAN.md` lists each one, what the earlier gates did with it and what this one
does. `check_output.txt` holds a clean run for comparison, and `STATEMENTS.md` the
statements listing the gate regenerates and checks.

**4. Read the statements, not the names.** This is the step that matters, and no script
substitutes for it. A Lean file can type-check and mean nothing: a theorem can restate its
own definition, or a definition can be arranged so that the impressive-sounding theorem
about it closes immediately. `RED_TEAM_LEAN.md` is exactly that reading, done
adversarially and in public: it classifies all 118 theorems into those that restate
definitions (33 of them), those that check every case of a finite question (28), and those
that say something general (57); it names the eight that restate another theorem rather
than a definition; and it names the places where this README used to claim more than the
file proved. `STATEMENTS.md` is the other half of this step: the elaborated statement of
every theorem, printed with no notation in the way, regenerated and checked on every gate
run.

**5. Disagree with the modelling.** The theorems are about four maps of ℤ². Whether those
four maps are the right account of what four coins do is not a question Lean can answer,
and the "What is not proved" section above is where to start arguing.

## Two notes on names

`Inv` and `Sub` are both taken in core Lean — `Inv` is the class behind the `⁻¹` notation
and `Sub` the class behind subtraction — so the invariance predicate is called `Invariant`
and the four-flag subset type is called `MoveSet`. The statements are the ones described
above; only the identifiers moved.

Uniqueness in S4 is written out — "there is one, and anything with the same property
equals it" — rather than with the `∃!` notation, which a file with no imports does not
have.

`T6_three_interchangeable` changed its statement in the second pass. It used to say
`swapVH sv = sh ∧ swapVC sv = C2`, which unfolds two definitions and does not by itself
say that the relabellings preserve anything. It now says there is a self-inverse map
preserving the composition table that carries `sv` to `sh`, and another that carries `sv`
to `C2` — which is what the name was claiming all along. The witnesses are the same two
functions.

## Before this goes public

`check.sh` looks for the three Lean toolchains under `$HOME/.elan/toolchains/`, where
`elan` installs them. On another machine, install the same versions with the commands in
"How a skeptic can check this", or edit the list at the top of the script. The
`lean-toolchain` file pins the primary one for `elan`'s benefit; the script names all
three explicitly by path, so that it runs the versions it says it runs rather than
whichever one a shim resolves to.

The script needs a writable directory to compile and audit in. It asks `mktemp` first,
which on macOS puts it under a per-user directory of its own choosing — Apple's `mktemp`
ignores `$TMPDIR`, where the GNU one honours it — and falls back to a directory beside the
file; where neither can be made, it stops and
says so rather than reporting success on checks it did not run. Everything it writes goes
in that one directory, and the run prints its path.

## What a green light says, and what it does not

A pass from `check.sh` says one thing: on this machine, under these three toolchains, the
file in this folder compiled, the kernel accepted every proof, no axiom beyond Lean's three
standard ones appeared in any of the 118 footprints — `propext`, `Quot.sound` and
`Classical.choice`, which come in through `simp`, `omega` and the classical step in the
S1 counting argument, and none of which is specific to this file — and none of the tricks
the gate's authors knew to look for were found in it.

What it is not is a proof that the file is honest. The gate is a list of the attacks two
reviewers and its authors thought of, plus a refusal of the constructs this particular file
does not contain. A trick nobody here has thought of looks exactly like a clean file. Four
separate passes each added checks for something the pass before had missed, and the fifth
and sixth did too, so the honest reading of the next pass is that it would find something
as well.

The second reviewer's checking stopped after it re-ran its existing attacks against version
2.4 on 22 October 2026; it looked for no new ones after that.

A green light on a copy from somewhere else says less again. Anyone can edit a Lean file
and anyone can edit a shell script, and a copy of both that agree with each other proves
only that. The file this document is about is the one whose sha256 is recorded in
the Zenodo record of this release, linked from the repository's `CITATION.cff`: check that
hash before trusting a green light, and read `STATEMENTS.md`, where every statement is
printed from the compiled module rather than copied from the source. Those two steps — the
hash against the Zenodo record, and the statements read by a human — are what the gate
cannot do for you.

## What else is in this folder

Beside the file, the gate and the listing, this folder ships the record of how the checks
were arrived at: `RED_TEAM_LEAN.md`, which is the adversarial reading; the two answer
documents to the outside reviews, `ANSWERS_v2.2_SECOND_OPINION.md` and
`ANSWERS_v2.3_SECOND_OPINION.md`, with the change logs beside them; `attack_matrix.json`
and `RUN_INDEX.tsv`, which are the attacks and every run of them in machine-readable form;
the check summaries, `SCIENCE_CHECK_v2.3.md`, `SCIENCE_CHECK_v2.4.1.md` and `SCIENCE_CHECK_v2.4.2.md`,
which say what was checked in each pass and carry the hash table for this folder; and
`attacks/`, the attack files themselves, one directory each, with the two scripts that
generate them from the honest file — `build_attacks.py` for the twenty-five of the fifth
pass and `build_attacks_v24.py` for the thirteen of the sixth.

Nothing in that list is read by the gate. A copy holding only these eight files passes on
its own — `TetrasemaphoreAlgebra.lean`, `check.sh`, `STATEMENTS.md`, `check_output.txt`,
`README_LEAN.md`, `RED_TEAM_LEAN.md`, `lean-toolchain` and `attack_matrix.json` — and `lean TetrasemaphoreAlgebra.lean`, in a
directory holding the file and `lean-toolchain`, elaborates it in about ten seconds and
prints the 118 axiom lines without the gate at all.

A word about `attacks/`: five of those files run code when they are compiled, by design —
that is the thing they were built to demonstrate. Four of them write one small text file in
the directory they are compiled in and nothing else; the fifth, the one attacks/README.md calls a15, prints one
forged line of the gate's own output and writes nothing. They are source, not programs to
be run, and `attacks/README.md` says which ones they are. A sandbox, a container or a
throwaway directory is the comfortable place to open them.
