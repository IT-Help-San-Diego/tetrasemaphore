# Red team: `TetrasemaphoreAlgebra.lean`

An adversarial reading of the proof file and its README, written to one
standard: *would a skeptical mathematician, or someone who reviews Lean for a
living, take this seriously — or is it the kind of Lean file that type-checks
English sentences and proves nothing?*

The file read was `TetrasemaphoreAlgebra.lean`, sha256 `849872e2…`, 630 lines,
64 theorems, zero imports, together with `README_LEAN.md`, sha256 `37166d5d…`,
and `check.sh`, sha256 `95d65c06…`. Everything recommended below has been
carried out; after that pass the file stood at 99 theorems, sha256 `4a434e30…`.
Each criticism is stated as it was found, with the repair recorded underneath it,
so that a reader can see what the file looked like before and judge both.

A **third pass** followed, recorded in the "v2.1" section near the end. Its
subject was the gate rather than the file: an independent reviewer observed that
`check.sh` decided what the file contained by running `grep` over it, and read the
axiom footprint out of the text Lean printed — both of which the file under test
can write. Seventeen attacks were built and run; six defeated the v2 gate, none
defeats the rewritten one. One further overclaim in the README was found and
closed by sixteen new theorems (O9, the symmetries of the square), which is why
the counts below say 115 and not 99.

A **fourth pass** followed, recorded in the "v2.2" section near the end. Its
subject was the gate again: the same reviewer built an adversarial corpus
against v2.1 and shipped it, and a second reviewer read v2.1 itself. All 236
distinct files of that corpus were replayed here, nine changes to the gate
followed, and two findings against v2.1 that no corpus file had reached were
closed as well — a `sorry` check that was inert in a C locale, and a statements
listing blind to a changed definition. Three theorems were added, so the counts
below say 118 and not 115; the three are second proofs of statements that were
already in the file, so the count is 115 net of those three. By the statements
themselves the file carries 114 distinct statement strings, and 113 if two that
differ only in an implicit binder are read as one; §4 names which.

The files as they now stand: `TetrasemaphoreAlgebra.lean`, 1503 lines,
118 theorems, zero imports; `check.sh`; `README_LEAN.md`; `STATEMENTS.md`, the
statements-and-definitions listing the gate regenerates and checks;
`lean-toolchain`. Green under Lean 4.32.2, 4.33.0 and 4.33.1. Hashes are not
quoted here: they change with every edit to this paragraph, and the gate's own
output is the thing to compare.

---

## Summary verdict

The original file was not the failure mode it was being tested for. It is not a
sequence of true-by-construction sentences dressed as theorems. It has a real
hinge — `Move.act_mul`, which proves that the composition table is the
composition of actual maps of the plane — and without that hinge the rest would
have been arithmetic on four symbols. Someone thought about where the content
had to be.

But its three strongest-sounding claims were not theorems in it.

1. "The set of moves any figure survives is one of the five" was an informal
   combination of two theorems, and the gap between them was real: nothing
   connected invariance, which is a proposition about an arbitrary predicate on
   the plane, to the four-flag subset type the five subgroups live in.
2. "Nothing in the table and the determinant separates the two mirrors" is a
   claim about *every statement* in a formal language. The file exhibited one
   relabelling. That is evidence for the claim, not the claim.
3. The design claim — each mark survives exactly its own move — had no proof at
   all, not even for an idealized mark. `stab`, the thing that looked like the
   assignment theorem, is a definition, and all six T10 theorems check it
   against itself.

Of the 64 theorems, 24 restate the file's own definitions. That is not a
scandal; formalizations need restatements. It is a problem only because the
README counted all 64 as "results" without saying which kind each was.

All three gaps are now closed by theorems rather than by softened prose, and the
numbers below are the new ones. A skeptic's remaining objections — the artwork
is not the model mark, the plane is not ℤ², the names are a convention — are
objections the README already made against itself, and makes more precisely now.

---

## 1. Classification of every theorem

A methodological point first, because it is where this kind of review usually
goes wrong: **"proved by `rfl`" is not the same as "definitional."**
`T1_mul_assoc` closes with `rfl` in each of 64 cases and has real content — a
different table would fail it. What makes a theorem definitional is that its
*statement* is obtained by unfolding the file's own definitions case by case,
asserting nothing the author did not already write down. `T1_one_mul` is
definitional in that sense: the table literally contains the four lines
`I, h => h`.

Classes used:

- **(a) definitional** — restates the file's own definitions; true by unfolding.
- **(b) exhaustive finite check** — a real property, settled by checking all 4
  moves, 16 pairs, 64 triples or 16 subsets.
- **(c) general** — quantified over all points of the plane, all figures, all
  predicates, all seeds, or all formulas, with content.

| | class (a) | class (b) | class (c) | total |
|---|---|---|---|---|
| original file | 24 | 18 | 22 | 64 |
| added in the second pass | 4 | 8 | 23 | 35 |
| added in the third pass (S4) | 5 | 2 | 9 | 16 |
| added in the fourth pass | 0 | 0 | 3 | 3 |
| **file as it now stands** | **33** | **28** | **57** | **118** |

**The fourth pass recounted this table**, because a reviewer checked it against the
definitions above and two rows did not follow from them. `S1_flag_true` is core Lean's
`decide_eq_true_eq` wrapped around this file's `flag`, and `S0_subgroup_has_inverses` is
`T1_self_inverse` repackaged — its `MoveSet` binder is never used, so it is not a fact
about subgroups at all. Both were counted (c); by the definition of (a) above, "restates
the file's own definitions; true by unfolding", both belong there. They have been moved,
and the second-pass row changed with them.

**And a count the three classes do not make.** Class (a) is about restating
*definitions*; it has no place for a theorem that restates another *theorem*. Eight of
the 118 are in that position, and naming them is more useful than finding a column for
them:

| theorem | class | what it restates |
|---|---|---|
| `T4_fix_I` | a | the same statement as `Move.act_I`, proved the same way |
| `S1_flag_true` | a | core's `decide_eq_true_eq`, for this file's `flag` |
| `S0_subgroup_has_inverses` | a | `T1_self_inverse`, packaged as an existence claim |
| `S1_no_three_element_symmetry` | c | `T7_both_mirrors` applied; identical up to an implicit binder. The name promises a statement about three-element symmetry sets that it does not make |
| `S4_unique_of_act` | c | `S4_act_injective` with the existence hypothesis repackaged |
| `S2_mark_sv_exact_via_general` | c | `S2_mark_sv_exact`, proved a second way |
| `S2_mark_sh_exact_via_general` | c | `S2_mark_sh_exact`, proved a second way |
| `S2_mark_C2_exact_via_general` | c | `S2_mark_C2_exact`, proved a second way |

The first five are bookkeeping: 115 is 118 net of the three second proofs, and
of the five, two — `T4_fix_I` against `Move.act_I`, and
`S1_no_three_element_symmetry` against `T7_both_mirrors` up to an implicit
binder — print as statements that already appear under another name, which takes
the distinct statement strings in `STATEMENTS.md` to 114 and, reading those two
binders as one, to 113. The other three (`S1_flag_true`,
`S0_subgroup_has_inverses`, `S4_unique_of_act`) are repackagings with statements
of their own. The last
three are deliberate: a statement proved two independent ways is worth having twice, and
those three exist because this report had claimed two independent proofs before the
second one was written. `S1_no_three_element_symmetry` is kept because the S1 section is
where a reader looks for the shape of the five-subgroup answer, and its docstring now says
it is `T7_both_mirrors` restated.

Reading the table net of restatements: of the 33 in (a), three restate something; of the
57 in (c), five do, leaving 52 class-(c) theorems with content of their own. A reviewer
who moves all eight into (a) gets 38/28/52, which is the same information arranged
differently — the names above are the part that matters, not which column they sit in.

### Why exhaustive checking over four moves is a complete proof, and where it is small

A group of order four is a finite object. "For every move `g`" is four cases;
"for every pair" is sixteen; "for every subset of the four" is sixteen. When
Lean's kernel evaluates `decide` on such a statement it is not sampling or
testing — it computes the truth value of each case and checks that the result is
`true`, and the proof term it produces is checked by the kernel like any other.
There is no gap between "checked all sixteen" and "proved for all sixteen",
because sixteen is all of them. This is the same completeness a truth table has.

Where it is small is worth saying just as plainly. A human can verify
`T1_mul_assoc` by hand in a few minutes, and `T8_five_are` in an afternoon.
Machine-checking them buys certainty against clerical error, not against
conceptual error, and nobody should present a 4-element group as a feat. What
the finite checks are *for* in this file is that they feed the general theorems:
the five subgroups of T8 become interesting only when S1 proves every figure's
symmetry set is one of them.

### The 33 class (a) theorems, named

These restate definitions. They are true, they are useful as the convenient form
of a table, and none of them is evidence of anything beyond the definition it
unfolds. A reviewer found this list had been left at the 26 of the second pass
while the table above moved to 31 and then 33, so it is written out in full here
and the later additions are marked:

`Move.act_I`, `Move.act_sv`, `Move.act_sh`, `Move.act_C2`, `T1_one_mul`,
`T1_mul_one`, `T1_self_inverse`, `T1_mem_all`, `T1_all_length`,
`T1_all_distinct`, `T3_det_kernel`, `T3_det_mirrors`, `T4_fix_I`,
`Sq.ofMove_act`, `T5_rot90_eq_R90`, `T5_rot270_eq_R90inv`,
`T6_swapVH_involution`, `T8_sixteen`, `T10_stab_subgroup`, `T10_stab_distinct`,
`T10_stab_is_pair`, `T10_stab_I`, `T10_subI_unused`, `T10_det_table`,
`S3_swapVC_involution`, `S2_mem_mark` — the twenty-six of the second pass; then
the five added with S4 in the third, `S4_act_matrix`, `S4_id_comp`,
`S4_comp_id`, `S4_comp_inv`, `S4_inv_comp`; and the two the fourth pass moved
here from (c), `S1_flag_true` and `S0_subgroup_has_inverses`.

Three deserve a specific note.

- `T1_self_inverse` is definitional *given the table* — the table's four
  diagonal entries are exactly what it says. It becomes a fact about the plane
  only through `Move.act_mul`. It is also load-bearing: the decision lemma
  `S2_invariant_ofList` and the T9 construction both rest on it.
- `T1_mem_all` and `T1_all_distinct` together give "there are exactly four
  moves". But the "only four" is stipulated by the `inductive Move` declaration,
  not discovered. The plane has many more symmetries; T5 exhibits eight of them.
  "There is no fifth" is true of this alphabet by construction.
- The six `T10_*` theorems are the clearest case in the file of a definition
  being checked against itself. See §3.

The full table, with each theorem's class and its axiom footprint, is the
appendix; it has 118 rows now.

---

## 2. Where the README outran the file

Six substantive overclaims and two small ones. In each case the sentence was
either stronger than any single theorem, or stronger than the file as a whole.

### O1. "the set of moves that any figure whatsoever survives is always one of those five"

*(README, T8 paragraph; the same sentence appears as the §9 section comment in
the .lean.)*

This was an informal combination of T7 (symmetries are closed) and T8 (five
subgroups among sixteen subsets), and the two do not meet. `Invariant g S` is a
proposition about an arbitrary `S : Pt → Prop`; the five subgroups are values of
`MoveSet`, a structure of four booleans. Nothing in the file built the symmetry
set of a figure as a `MoveSet`, so "is always one of those five" was a sentence
a reader assembled, not a theorem anyone had proved. It is also the sentence
most load-bearing for the design, since it is what licenses "there is no sixth
possibility to design for".

**Repaired** by `S1_one_of_five`: for every `S : Pt → Prop` there exists
`s ∈ fiveSubgroups` with `∀ g, s.mem g = true ↔ Invariant g S`. Arbitrary
predicates are not decidable, so the symmetry set is built with excluded middle;
the resulting `Classical.choice` is visible in the `#print axioms` line and is
one of Lean's own three standard axioms, not a new one.

### O2. "*Nothing* in the table and the determinant together separates NON-NORMATIVE from METACOGNITIVE"

*(README, T6 paragraph; the .lean §7 comment says "no statement in the language
of multiplication-and-determinant can distinguish `sv` from `sh`".)*

This is a quantification over every statement in a formal language. What the
file proved is that one particular relabelling, `swapVH`, preserves the
composition table and the determinant. The step from there to "no statement"
is the standard automorphism-invariance argument, and it is a correct argument —
but it is an argument about a formal language, carried out on paper, and the
README presented it as something Lean had checked. It was the sharpest claim in
the document and the one with the widest gap between assertion and proof.

**Repaired** by writing the language down. §15 defines terms (variables, the
identity, composition) and formulas (equations between terms, equations between
their determinants, negation, conjunction, disjunction, and quantification over
moves), and proves by induction that satisfaction is invariant under the
relabelling (`S3_fml_swapVH`), hence `S3_no_formula_separates_mirrors`: for
every formula `f`, `f` holds of `sv` exactly when it holds of `sh`.
`S3_language_separates_turn_from_mirror` checks the language is not vacuous — it
does separate the half-turn from a mirror, which is T3 said inside the language.

The honest limit, now stated in the file and the README: the language has one
sort, the operation and the identity, equality, determinant-equality, and
quantifiers over moves. It deliberately has no constant naming `sv`. A language
with such a constant separates the mirrors trivially, and that is a fact about
naming rather than about the group.

### O3. "the same statements and the same proofs read over ℚ or ℝ unchanged"

*(File header.)*

False for the proofs, and the README's own Scope section said the opposite three
pages later ("several close with `omega`… so a real-plane version would need
different tactics"). `omega` is a decision procedure for linear integer
arithmetic and `decide` on `Int` equality is integer-specific; neither survives
the move to ℝ. The *statements* do transfer — they use only that coordinates
form a torsion-free abelian group — but that is a different claim.

**Repaired**: the header now distinguishes statements from proofs and says the
real-plane version has not been written.

### O4. "nothing is hidden by that: a headline theorem's line already accounts for every lemma underneath it"

*(README, axiom section, explaining why 9 of 64 theorems had no `#print axioms`
line.)*

The reasoning is sound *provided* each unprinted lemma lies underneath a printed
one. Three of the nine did not: `R90_left_inv`, `R90_right_inv` and
`Sq.ofMove_act` are used by no other proof in the file. (`T6_swapVH_involution`
was a fourth until this pass began using it.) Their axiom footprint was
therefore genuinely unreported, and the README's justification did not cover
them. This is a small thing that a reviewer finds in about ninety seconds, and
finding it costs the document more credibility than it costs the mathematics.

**Repaired** by printing axioms for all 99 theorems and — more usefully — by
making `check.sh` fail if any theorem lacks its own line, so the claim is
enforced rather than asserted. The three unused lemmas are kept: they are what
justifies calling `R90inv` an inverse and saying the four moves "sit inside" the
eight symmetries of the square, which are claims the prose makes.

### O5. "Four moves make sixteen subsets… Lean checks all sixteen by enumeration"

`T8_sixteen` proves `allSubs.length = 16` by `rfl` on a hand-written list. That
is the length of a list, not a count of subsets. Two things were missing: that
the sixteen entries are sixteen *different* subsets, and that `MoveSet` — four
booleans — faithfully represents subsets of `Move` at all. Without the latter,
"five of the sixteen are subgroups" is a statement about a structure of flags
that a reader is trusting to mean what it looks like.

**Repaired** by `S0_MoveSet_ext` (two subsets with the same members are equal),
`S0_allSubs_nodup`, and `S0_allSubs_exactly_once` (every subset occurs exactly
once in the enumeration).

### O6. T10 is described as a result; it is a definition

*(README: "NORMATIVE is given all four moves; each of the other three states is
given exactly `{I, g}`… Each of those four sets is one of the five subgroups.")*

`stab` is a `def`. All six T10 theorems check the table against itself: that the
four sets written down are subgroups, are four different ones, have the shape
`{I, g}`, and omit the trivial subgroup. Not one of them says any figure has
these symmetries. The design claim the coins actually make — each mark survives
exactly its own move — appeared nowhere in the file, and could not have followed
from T9, which gives only that seed-plus-image survives its own move and is
silent on whether it survives more. For a symmetric seed it does survive more,
so the "exactly" was not merely unproved but unprovable from what was there.

**Repaired** in §14, and this is the largest addition. A figure is a finite list
of integer points; `S2_invariant_ofList` proves that invariance of such a figure
— a statement about every point of the infinite plane — is equivalent to a
finite check on the list, the equivalence resting on each move undoing itself.
Then `S2_mark_sv_exact`, `S2_mark_sh_exact`, `S2_mark_C2_exact` prove that the
concrete mark built from an L-shaped five-point seed survives exactly `{I, g}`,
`S2_markAll_invariant` that the four-fold mark survives all four, and
`S2_realizes_stab` that the moves each mark survives are exactly the moves
`stab` assigns. `stab` stops being a table someone wrote down.

Because a reviewer would reasonably ask whether the seed was chosen to make the
answer come out, `S2_quadrant_mark_exact` proves the general version: for *any*
non-empty finite seed drawn entirely inside the open first quadrant, and any
`g ≠ I`, the mark `seed ∪ g(seed)` survives exactly `I` and `g`.  The weaker
reading, "any letter off both axes", is not what the theorem says and is false:
`[(1, 1), (-1, 1)]` misses both axes and its `sh`-mark survives all four moves.
The argument is the geometric one: `seed ∪ sv(seed)` lies in the upper half
plane and both `sh` and `C2` reverse it. The hand-picked seed is then an
instance (`S2_seed_in_quadrant`).  In the fourth pass that instance was written
out, so the three concrete results now carry two proofs apiece — one by
enumeration, one as a one-term instance of the general theorem
(`S2_mark_sv_exact_via_general`, `S2_mark_sh_exact_via_general`,
`S2_mark_C2_exact_via_general`).  Until then "proved two independent ways"
described both ingredients being present rather than the instance being taken,
which a reviewer was right to call a claim the file did not contain.

### O7. `T6_three_interchangeable` promised more than it stated

Its name says the three non-identity moves are interchangeable. Its statement
was `swapVH sv = sh ∧ swapVC sv = C2` — two unfoldings of two definitions, which
on their own say nothing about the relabellings preserving anything.

**Repaired** by strengthening the statement, not renaming the theorem: it now
asserts the existence, for each target, of a self-inverse map that preserves the
composition table and carries `sv` there. The witnesses are the same two
functions; the hypotheses that make the name true are now in the statement.

### O8. "all three installed Lean toolchains"

Six toolchains are installed on the machine this was checked on. The script runs
the three it lists. Corrected to say so.

### Credit where it is due

Four claims that a reviewer would check first and that held up:

- The counts in the README — 64 theorems, 55 printed axiom lines, 37 with no
  axioms and 18 with standard ones — were all exactly right.
- The "What is *not* proved" section is better than most published formalization
  READMEs: it concedes the artwork is measured rather than proved, that the
  names are a convention, and that seL4 has nothing to do with it. The seL4
  paragraph in particular refuses a borrowed credibility that would have been
  easy to take.
- `Move.act_mul` is placed exactly where the content has to be, and the file
  says so in its docstring ("this is the hinge").
- `T8_isSubgroup_iff` does the thing that is easy to skip: it proves the boolean
  test equals quantification over the *type* of moves, not over the entries of a
  list. A file that cut that corner would look identical and mean less.

---

## 3. Do definitions bake in their conclusions?

This is the question that decides whether a formalization is worth anything, so
here is the audit definition by definition. The pattern to look for: define `X`
to have property `P`, then prove `X` has property `P`.

**Closed properly** — the definition is independently checked against something
it could have disagreed with:

- `Move.mul` is a hand-written table; `Move.act_mul` checks it against actual
  composition of maps on an arbitrary point. This is the one that matters.
- `Move.a/b/c/d` are hand-written matrix entries; `T3_act_matrix` checks them
  against `act` for every point.
- `Move.det` is a hand-written table; `T3_det_eq_ad_sub_bc` checks it against
  `ad − bc` computed from those entries. So the chain `act → matrix → det` is
  closed at both joints, and `det` is not a second convention bolted on.
- `isSubgroup` is a boolean test over a list; `T8_isSubgroup_iff` checks it
  against identity-plus-closure quantified over the type.
- `subI … subAll` are five named values; `T8_five_are` proves they are exactly
  the subgroups rather than five that happen to be.

**Was not closed, now is**:

- `MoveSet` was a structure of four flags with no theorem saying flags are
  subsets (O5). Closed by `S0_MoveSet_ext`.
- `stab` was the central baked-in definition (O6). Closed by
  `S2_realizes_stab`.
- `Invariant` was a definition nobody connected to its intended reading. Closed
  by `S0_invariant_iff_eq`: `Invariant g S` holds exactly when the figure moved
  equals the figure, `(fun p => S (act g p)) = S`.
- `isSubgroup`'s docstring claimed inverses "come free". True, but a remark.
  Now `S0_subgroup_has_inverses`.

**Stipulated, and should be read that way**: `inductive Move` fixes four moves.
No theorem could establish "there is no fifth", because it is a choice of
alphabet. The docstring's flat "there is no fifth" is defensible as scoping; a
reader coming to it cold could take it for a claim about the plane, which T5
shows would be false.

**New definitions in this pass**: `seed`, `mark`, `markAll`, `markOf` are
choices, and the theorems about them do not bake anything in — `S2_seed_asymmetric`
proves the seed has no symmetry rather than assuming it, and
`S2_quadrant_mark_exact` removes the dependence on the choice altogether.
`flag` and `symSet` are classical constructions whose defining property is the
thing proved about them (`S1_flag_true`, `S1_symSet_mem`), which is the normal
shape for a definition-plus-characterization and is not hiding anything — the
content is in `S1_symSet_isSubgroup` and `S1_one_of_five`.

---

## 4. Names and docstrings

- `T6_three_interchangeable` — name outran statement. Fixed (O7).
- `T8_sixteen` — the name reads as "there are sixteen subsets"; the statement is
  the length of a list. Now backed by `S0_allSubs_nodup` and
  `S0_allSubs_exactly_once`.
- `T10_stab_subgroup` — reads as a discovery about states. It is a check on a
  table. Docstring now says so, and §11's comment points at §14 for the version
  that is about figures.
- `T1_all_length` — accurate, and accurately unexciting.
- "These are the whole alphabet: there is no fifth" (`inductive Move`) — fine as
  scoping, risky read out of context. Flagged here rather than rewritten, since
  the sentence is true of the alphabet it describes.
- The §9 comment asserting the five-possibilities conclusion now says plainly
  that it is a conclusion from T7 and T8 together, and names the theorem (§13)
  that proves it.
- Everything else surveyed: the docstrings describe what the statements say.
  The file does not have a habit of overselling in prose what it understates in
  Lean; O1 and O2 were in the README and the two section comments, not scattered
  through the theorem docstrings.

---

## 5. Is anything an "English sentence" that merely type-checks?

No. Nothing in the file is of the form `theorem design_is_sound : True :=
trivial`, nor the subtler version where a predicate is defined so that the
headline theorem closes by `rfl` and the definition quietly contains the
conclusion. The nearest approaches were `stab` (O6) and `MoveSet` (O5), and both
are now tied to something external.

The class (a) theorems are the ones that would look like filler to a reviewer
counting results. They are not false and not useless — `T3_det_kernel` in iff
form is genuinely more convenient than the table — but anyone citing "99
theorems" should know that 26 of them restate definitions, which is why this
report leads with the classification rather than the count.

---

## 6. The gate

`check.sh` is part of what gets published, so it was attacked too. The original
caught `sorry` three ways (source text, Lean's warning, `sorryAx` in the axiom
output), `native_decide`, `axiom` declarations, `unsafe`/`implemented_by`/
`extern`, imports, and any axiom outside the standard three. That is a good
list, and the comment explaining *why* — that `sorry` is a warning, so a green
build proves nothing by itself — is the right first paragraph for such a script.
One correction to what this section said about `extern` through v2.2: the pattern
matched `@[` followed by `extern`, so it caught only an `extern` written as the
first attribute, and `@[inline, extern "lean_nat_add"]` on a definition the
listing already carries was green, with the listing byte-identical and the log
identical to the honest run. The reasoning in H5 below — that `extern` only ever
attaches to an `opaque`, which is refused anyway — was wrong as well: core Lean's
own `Nat.add` is an `@[extern] def`. Version 2.3 matches `extern` or
`implemented_by` anywhere inside an attribute group, which is 0 hits on the honest
file and matches every spelling that has been probed.

Holes found:

1. **`set_option debug.skipKernelTC true`** was not checked for. It switches off
   kernel typechecking and leaves the build green, with no `sorry`, no axiom and
   no import. It is the quietest way to fake a file that otherwise looks
   impeccable, and it was the one serious hole.
2. **`sorryAx` written directly in source** passed the text check, since
   `\bsorry\b` does not match `sorryAx`.
3. **`partial`** was not in the unsafe list; a `partial def` is compiled through
   an unsafe implementation and is opaque to the kernel.
4. **No check that every theorem prints its axioms**, which is what made O4
   possible: the axiom footprint in the log was a selection, and nothing
   enforced which selection.
5. **The gate reported OK when its own machinery failed.** Found while editing:
   on a system where `mktemp` fails, the theorem-extraction step errored, every
   downstream comparison compared empty files, and the script printed its
   success line regardless. A gate that passes when its checks cannot run is the
   exact failure it exists to prevent. It now uses no temporary files and fails
   if it finds zero theorems.

All five are fixed. What the gate still cannot do, and now says so in its own
header: it checks the known ways a Lean file can look proved without being
proved. It cannot tell you the theorems say what their names say. Only reading
the statements does that, which is what this report is.

### Tamper tests

Six deliberate breaks of the final file, each run through the gate:

| break | exit | caught by |
|---|---|---|
| `T1_mul_comm` proved by `sorry` | 1 | source text; Lean's warning, which it writes as ``declaration uses `sorry` `` with backticks, under all three toolchains; `sorryAx` in the axiom output; non-standard axiom check |
| `axiom tetra_cheat` added and used | 1 | `axiom` declaration check; non-standard axiom check |
| one `decide` replaced by `native_decide` | 1 | source text; non-standard axiom check — on 4.32.2, 4.33.0 and 4.33.1 the axiom that appears is the per-theorem auxiliary `<theorem>._native.native_decide.ax_1_1`, and `<theorem>._native.decide.ax_1_1` for the `decide +native` spelling.  `Lean.ofReduceBool` still exists in core, is deprecated, and does not appear in the output of these versions; an earlier draft of this table named it |
| `import Lean` prepended | 1 | import check |
| `set_option debug.skipKernelTC true` | 1 | kernel-affecting option check |
| one `#print axioms` line deleted | 1 | per-theorem coverage check; axiom-line count vs theorem count |

Four of the six are caught by two or more independent checks, which is the
property you want: no single `grep` is load-bearing.

---

## 7. What is still not proved

The README's own list stands, and this pass adds to it rather than subtracting.

1. **The artwork.** Everything in §14 is about finite lists of integer points.
   A rendered glyph is strokes with width, antialiasing and a font's outlines,
   and whether it comes back to itself under its own move — and fails the other
   two — is measured on the files. A model mark is a model.
2. **The names.** NORMATIVE with the identity, CRITICAL with the half-turn: a
   convention. The algebra constrains it a little (T4 and S3 together say the
   two mirrors differ only in which axis they hold still) and chooses nothing.
3. **The real plane.** Statements transfer; proofs do not. No Mathlib version
   has been written.
4. **seL4.** Unrelated, as the README already said.
5. **The S3 language result is about that language.** One sort, composition, the
   identity, equality, determinant-equality, quantifiers over moves. Add a
   constant naming `sv` and the mirrors separate at once, which is a fact about
   naming.
6. **S1 is classical.** `Classical.choice` appears in its axiom lines. It is one
   of Lean's three standard axioms, not a new assumption, but it is there
   because the symmetry set of an arbitrary predicate is not computable.
7. **`S2_quadrant_mark_exact` has a hypothesis.** The seed must be non-empty and
   lie in the open first quadrant. Seeds meeting an axis, or straddling one, are
   not covered, and for some of them the conclusion is false — a seed symmetric
   in the horizontal axis gives a mark that survives all four moves. The
   hypothesis is the content, not a technicality.

---

## 8. What changed in the file

- §0 header: statements-versus-proofs over ℝ corrected; the axiom-printing claim
  strengthened to all theorems; a note added on which sections are new.
- `#print axioms` added for the nine theorems that lacked one.
- `T6_three_interchangeable`: statement strengthened to match its name, with the
  change recorded in its docstring.
- §9 and §11 section comments: now say which claims are conclusions drawn across
  theorems, and name the theorems that prove them.
- `T10_stab_subgroup`: docstring says it is a check on a table.
- §12 (S0, 6 theorems): `MoveSet` extensionality, `allSubs` distinctness and
  exact-occurrence, subgroup inverses, invariance as set equality.
- §13 (S1, 7 theorems): the symmetry set of an arbitrary figure, its closure,
  and `S1_one_of_five`.
- §14 (S2, 16 theorems): the decision lemma, the concrete marks and their exact
  symmetry sets, `S2_realizes_stab`, and the general quadrant construction.
- §15 (S3, 6 theorems): the term and formula algebra, the invariance induction,
  and `S3_no_formula_separates_mirrors`.
- `check.sh`: five holes closed (§6), and the per-theorem axiom coverage check
  added.

---

---

## v2.1 — a third pass, against the gate

The second pass hardened the file. This one was asked to break the *gate*, on the
observation that a checking script which reads the file with `grep`, and reads the
axiom footprint out of the text Lean prints, is asking the file under test to
describe itself. That is not a check; it is an interview.

Seventeen files were built, each a copy of the proof file with one thing changed,
and each was run through both gates. The table below gives, for every one, what
version 2 did with it and what version 2.1 does. Six of the seventeen passed the
v2 gate. None passes v2.1, and the honest file passes both.

A word on reading the table. "Caught by" lists every independent check that fired,
not the first one. That matters more than the verdict: a tamper caught by one
`grep` is a tamper that a slightly different spelling defeats, which is precisely
how four of the six holes below were found. Where a row names a single check, the
gate is resting on one thing and it is worth saying so. **Three rows do**, and all
three are attacks that defeated the v2 gate:

- the forged footprint (e), caught only by the command allowlist — and the
  allowlist as v2.2 wrote it read only the first word of a line, so
  `open Nat in #eval …` satisfied it; v2.3 refuses those commands anywhere on a
  line, which is what that row now rests on;
- the self-defined command (g), caught only by the command allowlist;
- `set_option` moved off the start of a line (h), caught only by the `set_option`
  source check.

What the three have in common is that the gate is refusing a *capability* rather
than detecting a *consequence*, because in these particular files there is no
consequence to detect. The line the forgery writes happens to be true; the
self-defined command only renames `#print axioms`; the misplaced option leaves a
theorem that is true anyway. Nothing improper reaches the compiled module in any
of them, so the audit — the part of the gate that cannot be written by the file —
has nothing to find, and correctly says so.

That is the honest result rather than a weakness in those three runs, but it does
locate the thin part of the gate, and it should be read as a caveat rather than a
reassurance. All three rest on reading the source text, which is the one layer an
attacker controls; each would fall to a spelling the scanner does not anticipate,
which is exactly how the six v2 holes were found. They hold here because the
allowlist refuses what it does not recognise rather than only what it knows to
ban — a property worth preserving in any later edit. What makes the file safe is
that these capabilities, once *used* for anything, show up in the audit: when the
same forging machinery writes a false line, four checks fire, and that is the
full-chain row.

| attack | v2 | v2.1 | caught in v2.1 by |
|---|---|---|---|
| *the honest file, unmodified* | **passes** | **passes** | — |
| (a) `#guard_msgs(drop warning) in` wrapping a theorem proved by `sorry` | fails | fails | source: `sorry`/`sorryAx`; command allowlist; `sorryAx` in the log; compiled-module audit |
| (a) `#guard_msgs(drop info) in` wrapping a theorem's own `#print axioms` line | fails | fails | command allowlist; footprint count; printed vs audited footprint |
| (b) `set_option warn.sorry false` with a `sorry` proof | fails | fails | source: `sorry`/`sorryAx`; source: `set_option`; command allowlist; `sorryAx` in the log; compiled-module audit |
| (c) `decide +native`, the spelling `native_decide` does not cover | fails | fails | source: `+native`; compiled-module audit |
| (c, g) `decide +native` hidden behind a `macro_rules` tactic alias | fails | fails | source: `+native`; command allowlist; compiled-module audit |
| (d) `#exit` before the last theorems, a false theorem after it | fails | fails | command allowlist; Lean's `#exit` warning; module vs source theorems; README names resolve; footprint count; printed vs audited footprint |
| (d, e) the same, with `#eval` lines forging the footprints `#exit` removed | fails | fails | command allowlist; Lean's `#exit` warning; module vs source theorems; README names resolve; footprint count; printed vs audited footprint |
| (e) real `#print axioms` output swallowed, footprint forged by `#eval` | **passes** | fails | command allowlist |
| (f) `sorryAx` under a spelling the word-boundary grep misses: `@«sorryAx»` | fails | fails | source: `sorry`/`sorryAx`; Lean's sorry warning; `sorryAx` in the log; compiled-module audit |
| (g) `syntax`/`macro_rules` defining a command of the file's own | **passes** | fails | command allowlist |
| (h) `@[simp] axiom` — an attribute in front of `axiom` | fails | fails | source: `axiom`/`opaque`; command allowlist; compiled-module audit |
| (h) `/-- doc -/ axiom` on one line | fails | fails | source: `axiom`/`opaque`; command allowlist; compiled-module audit |
| (h) `@[ extern "…"] opaque` with a space after the bracket | **passes** | fails | source: `axiom`/`opaque`; source: `unsafe`/`extern`; command allowlist |
| (h) `set_option debug.skipKernelTC true in` moved off the line start | **passes** | fails | source: `set_option` |
| (c, e, g) full chain: macro-hidden `decide +native` plus a forged footprint | **passes** | fails | source: `+native`; command allowlist; compiled-module audit; printed vs audited footprint |
| (f) `sorry` reached only through a `macro_rules` alias, never in a proof position | fails | fails | source: `sorry`/`sorryAx`; command allowlist; Lean's sorry warning; `sorryAx` in the log; compiled-module audit |
| (h) `namespace Lean` declaring a constant the gate's own audit wrapper calls | **passes** | fails | audit failed closed; printed vs audited footprint |

### The six weaknesses, and the six files that got through

Two lists, and they are not the same list — which is worth being exact about.

**The six attack files that passed the v2 gate** are the rows marked *passes*
above: the forged footprint (e); a `syntax`/`macro_rules` pair defining a command
of the file's own (g); `@[ extern "…"] opaque` with a space after the bracket (h);
`set_option debug.skipKernelTC true in` moved off the start of a line (h); the
full chain — macro-hidden `decide +native` with its footprint forged (c, e, g);
and `namespace Lean` declaring a constant the gate's own audit wrapper calls (h).

**The six weaknesses below** are what those runs exposed, and the two lists differ
because some weaknesses are only dangerous in combination. v2 did catch plain
`decide +native` (H2), and the attribute in front of `axiom` (H4) — but in each
case *only* through the axiom footprint, and H1 is the demonstration that the
footprint is something the file can write. Pair either one with H1 and the catch
disappears: the full-chain row is exactly that pairing, and it passed. A defence
that holds only until it is combined with another hole is a weakness, which is
why both are listed here rather than filed as successes.


**H1. The footprint can be written by the file.** `#eval IO.println "'X' does not
depend on any axioms"` puts a line into the build output that is
indistinguishable from the real thing, and `#guard_msgs(drop info)` on the line
before a `#print axioms` swallows the real one. Written on two lines — the
`#guard_msgs(drop info) in` first, the `#print axioms X` in column 1 after it —
the per-theorem coverage check still saw the `#print axioms` line, the count
still matched, and the footprint in the log was whatever the file said. This is
the serious one: every other v2 defence against an added axiom or a skipped proof
ends at that footprint.

*The fix is not a better `grep`.* The gate now compiles the file to an `.olean`,
writes its own Lean program, imports the compiled module, walks every constant
defined in it and collects the axioms each one depends on. 671 constants, not the
118 theorems — the auto-generated lemmas and the definitions are audited too. The
file cannot write into that output. The footprint it prints about itself is then
compared against the audited one, so a forged line is a disagreement.

**H2. `decide +native` is `native_decide` under another name.** The v2 gate banned
the word. Lean 4.33 accepts `decide +native`, which hands the check to the
compiled program exactly as `native_decide` does, and the word never appears.
The resulting constant depends on a generated axiom named after the declaration
(`T8_sixteen._native.decide.ax_1_1`), which v2 did catch in the footprint — but
only through the footprint, which H1 shows is forgeable. Combined, the two gave a
file where a theorem was decided by the compiler and the published axiom lines
said it depended on nothing. The gate now matches `+native` in any spelling, and
the compiled-module audit catches the generated axiom independently.

**H3. `macro_rules` can rename anything.** `syntax "fastcheck" : tactic` plus one
`macro_rules` line, and a proof reads `by fastcheck` with no banned word in it.
The same trick renames commands. A gate that bans tokens cannot survive a file
that defines its own tokens, so the gate no longer tries: it has a list of the
commands a proof file may begin a line with, and `syntax`, `macro`, `macro_rules`
and `notation` are not on it.

**H4. An attribute in front of `axiom`.** The v2 check for an added axiom was
anchored to the start of a line. `@[simp] axiom cheat : …` is not at the start of
a line, and neither is `/-- a shortcut -/ axiom cheat : …`. Both were caught by
v2's footprint check — and only by it. The source checks now read the file with
its comments blanked out by a scanner that understands Lean's nesting block
comments, so a doc comment no longer hides what follows it; the same change fixed
a false positive in the other direction, where the prose "the axiom footprint"
inside a doc comment tripped the axiom check.

**H5. `@[ extern "…"]` with a space.** v2 matched the literal `@[extern`. One
space defeated it. Matched now with the space allowed — though the real answer is
that `opaque`, the declaration `extern` attaches to, is itself refused, and the
command allowlist refuses the line regardless of how it is spaced.

**H6. `set_option` off the start of a line.** v2 looked for `set_option` in column
1 and merely *noted* options it did not recognise as kernel-affecting.
`theorem T8_sixteen : … := by set_option debug.skipKernelTC true in decide` is
neither in column 1 nor on the list. The gate now refuses `set_option` anywhere.
The file needs none, and an allowlist of harmless options is a surface worth not
having — `warn.sorry false`, which silences Lean's own warning about a skipped
proof, would have had to be on it.

### Attacks that v2 already caught, and one that cannot be built

`#guard_msgs(drop warning)` around a `sorry` proof, `set_option warn.sorry false`,
`@«sorryAx»`, and a `macro_rules` alias expanding to `sorry` were all caught by
v2 — in each case because the word `sorry` or `sorryAx` still appears somewhere in
the file, even if only inside a syntax quotation. They are caught by v2.1 too, by
more checks.

The brief for this pass asked for a `sorry` that never spells the word: an `elab`
or `macro` tactic calling `Lean.Meta.mkSorry`, or assembling `sorryAx` from name
fragments. **It cannot be written in a file with no imports.** `elab`, `run_cmd`
and the `Lean.Meta` namespace all live in the `Lean` package, and a zero-import
file has only `Init`; `elab` fails with "Unknown constant
`Lean.Elab.Tactic.Tactic`" and `run_cmd` with "to use this command, include
`import Lean.Elab.Command`". Adding the import is caught by the import check. So
the attack is real against a file that imports Lean and not against this one —
and the compiled-module audit would catch its result anyway, since a term built by
`mkSorry` depends on `sorryAx` no matter how the text spelled it. That is the
point of auditing the artifact rather than the source.

### An attack on the new machinery

The audit wrapper calls `Lean.collectAxioms`. A file with no imports can still
declare into the `Lean` namespace, so the obvious counter-attack is to define a
`Lean.collectAxioms` of one's own and see what the wrapper calls. Tried: Lean
refuses to import two modules that declare the same constant, the wrapper fails
to compile, and the gate reports that its audit did not run and exits 1. Failing
closed is the behaviour that was designed for — v2's own review (§6, hole 5) found
the opposite, a gate that printed its success line when its machinery had broken —
and this is the first attack to exercise it. The gate also refuses, separately, any
constant in the compiled module whose name begins with a core namespace.

### What the gate still cannot do

Unchanged, and worth restating because the hardening might suggest otherwise. The
gate checks *how* a proof was made. It does not check that a theorem says what its
name says. A file of true, kernel-checked, axiom-free theorems that restate their
own definitions would pass every check in version 2.1, and that failure mode is the
one this whole document exists to measure — which is why §1 leads with the
classification and not the count. The gate also cannot tell that the README
describes the same thing the Lean does; the one check in that direction is weak
and worth describing precisely: every Lean name the README cites in backticks must
exist in the compiled module. That catches a renamed or deleted theorem still
being advertised. It does not catch a paragraph that describes a theorem
incorrectly.

### O9. "all eight symmetries of the square"

One more place where the README outran the file, found in this pass and listed
here with O1–O8 above.

README v2 said the file "builds all eight symmetries of the square". What §6
contained was `inductive Sq` with eight constructors, a `Sq.act` written out by
hand, and `T5_eight_distinct` proving the eight act differently. Eight maps, and
a proof that they are eight — but nothing saying there is no ninth. The claim a
reader takes from "all eight symmetries of the square" is a classification, and a
hand-written list is the opposite of one: it is exactly as complete as its author
remembered to be.

This is a mild overclaim compared with O1–O3 — the eight *are* all of them, as a
matter of classical fact, and the file was not wrong about the mathematics. It is
listed because the file did not contain the argument, and because "the author
wrote down eight and the group has eight" is the kind of agreement that holds
until it does not.

**Closed by §16 (S4), sixteen theorems.** Each of the eight is shown to act by an
integer 2×2 matrix (`S4_act_matrix`), linearly (`S4_matAct_add`,
`S4_matAct_smul`), carrying the four corners `(±1, ±1)` onto themselves —
*onto*, with every corner the image of one, not merely *into*
(`S4_corner_maps`, `S4_corner_onto`). The eight are closed under composition, with
a 64-entry table proved to be composition of the maps rather than to resemble one
(`S4_comp_act`), and with associativity, identity and inverses (`S4_comp_assoc`,
`S4_id_comp`, `S4_comp_id`, `S4_comp_inv`, `S4_inv_comp`). And then the converse:
any integer 2×2 matrix carrying the corner set onto itself has one of eight
quadruples of entries (`S4_entries`) and is the action of exactly one of the eight
(`S4_classification`), the two directions stated together as a biconditional
(`S4_eight_are_all`).

`S4_entries` is where the content is, and the shape of its proof is worth stating
so that a reader can check it is not circular. Both halves of "onto itself" are
used, and for different purposes. From the images of `(1,1)` and `(1,-1)` having
to be corners, `omega` derives that each of `(a,b)` and `(c,d)` is one of four
pairs — sixteen candidate matrices. Eight of those sixteen are singular: they
send the square to a diagonal, which satisfies *into* and fails *onto*. The
surjectivity hypothesis supplies a preimage for `(1,1)` and for `(1,-1)`, and in
each of those eight cases the two demands contradict each other. Nothing about
`Sq` enters the argument until the surviving eight quadruples are matched against
`Sq.mat`, which is what keeps it a classification rather than a check that a list
agrees with itself.

The eight theorems of the new section that restate the file's own definitions are
counted as such in §1, as the others were: five of the sixteen are class (a).

### What changed, v2 to v2.1

In `check.sh`:

- a list of the commands a proof file may begin a line with; everything else
  refused, including anything the list does not recognise;
- the source checks read the file with its comments blanked by a scanner that
  understands nesting block comments, line comments and string literals, in place
  of excusing lines that start with a comment marker or mention a word in
  backticks.  Through v2.2 that scanner tracked string literals without blanking
  them, so an honest `def note : String := "… sorry …"` tripped three patterns and
  the gate refused it; v2.3 blanks their insides, keeping the quotation marks, and
  the self-test probes both directions;
- the axiom footprint read from the compiled `.olean` by a gate-written wrapper
  that walks every constant in the module, under each of the three toolchains;
- the file's own printed footprint compared against the audited one;
- the theorems in the compiled module required to be the ones the source
  declares, allowing only the lemma shapes Lean generates for `inductive`,
  `structure` and `deriving`;
- every Lean name the README cites in backticks required to exist;
- `set_option` refused outright rather than noted; `+native` matched in any
  spelling; `axiom` and `opaque` matched anywhere a declaration can begin;
  `@[ extern` matched with spacing; Lean's "using 'exit' to interrupt" warning
  made a failure;
- the working directory it needs is created with a fallback where `mktemp` is
  unavailable, and the gate stops rather than reporting success if it cannot be
  made.

In `TetrasemaphoreAlgebra.lean`:

- §16 (S4), sixteen theorems: the classification of the square's symmetries (O9);
- the header note on what the file contains, and on the gate no longer taking the
  printed footprint on trust.

In `README_LEAN.md`: the square sentence replaced by what S4 proves; a section on
what the gate does and does not catch; counts and the axiom table updated to 115
theorems; the runtime stated honestly at about a minute. (The fourth pass moved
that number, because the audit now re-adds every declaration through the kernel.
Measured since: 69 to 117 seconds here for v2.2, v2.3 and v2.4 alike, on a
16-core machine with other runs of the same gate going at once, and 68 to 112
seconds by the reviewer on theirs.)

Added: `lean-toolchain`, naming `leanprover/lean4:v4.33.0`. `check.sh` is
committed executable.

---

---

## v2.2 — a fourth pass, against an independent reviewer's corpus

The third pass closed the holes it could find by writing its own attacks. A
reviewer in another lane then read v2 end to end, built 39 adversarial files, 24
reproduction tampers and 14 fidelity tampers, ran 33 independent skeptics each
trying to refute one finding on its own files, and shipped the whole evidence
tree — 1,303 files counting the 27 `.DS_Store` entries, 1,276 without, which is
the figure their packet gives — with the report. That corpus was replayed here against the
v2.1 gate, and then against the gate this pass produced.

**How the replay was run.** 329 candidate `.lean` files were collected (every
adversarial file, every tamper, and every full-size attack file under the 33
`verify-*` folders, including `AttA2`), deduplicated by content hash to 236
distinct files; 50 of the 329 were byte-identical copies of the honest v2 file.
Every one of the 236 was run through the gate under all three toolchains. The
corpus was built against v2, so each file was given the v2 `README_LEAN.md` as
the gate's second argument, and a control was run first: **the honest v2 file
with the v2 README passes the v2.1 gate** (99 theorems, 480 constants audited,
87 README names all resolving), so a failure in the replay is the tamper and not
the pairing. Against the v2.2 gate each file was run with `--write-statements`,
which writes the statements listing instead of comparing it — otherwise every
attack file would have failed on a missing `STATEMENTS.md` and told us nothing
about the rest.

Both replays ran with `LANG` empty and `LC_COLLATE`/`LC_CTYPE` set to `C` — which
is, as it turned out, the condition under which v2.1's own `sorry` check does not
fire. So no v2.1 row in `attack_matrix.json` carries that FAIL line and every
v2.2 row that should carries it; the difference between the two columns' fail
sets is that line, and nothing else. No verdict rests on it: every file that
passes v2.1 also passes the v2.2 gate, which pins the locale and runs the check
as plain ASCII, apart from the two honest private theorems v2.2 refuses on a
different ground.

**Counts.**

| | v2 | v2.1 | v2.2 |
|---|---|---|---|
| corpus files passing | 48 of the 104 with a recorded verdict | 13 of 236 | 14 of 236 |
| corpus files failing | 56 | 223 | 222 |

v2.2 passes one more than v2.1, and the three that moved are a repair: `fp02`
(nested namespaces), `fp03` (a `section … end` inside a namespace) and `fp04`
(`#print  axioms` with two spaces) are honest Lean that both earlier gates
rejected. Two that v2.1 passed are now refused, both honest private theorems —
below.

The v2 column is the reviewer's own recorded verdict where their logs carry one
(104 files); for the other 132 the packet records aggregate results only, and
nothing is claimed for them here.

### The attacks the reviewer asked to see in this table

Every file in the reviewer's ask-4 list, with what it does, what each gate did
with it, and which checks fire now. All three columns are measured runs.

| attack | v2 | v2.1 | v2.2 | caught in v2.2 by |
|---|---|---|---|---|
| a01a–a01f — six accepted spellings of `axiom` that do not start a line (`@[simp] axiom`, `/-- doc -/ axiom`, `set_option … in axiom`, `axiom`⏎`name`, `/- -/ axiom`, `@[simp] private axiom`), each hidden behind `propext` in the footprint | **passes** | fails | fails | source: `axiom`; command allowlist; the axiom walk over every constant |
| a02b — `admit` under `#guard_msgs (drop warning)`, the real `#print axioms` output swallowed and a clean line forged by `#eval` | **passes** | fails | fails | command allowlist; sorryAx in the log; the axiom walk; the printed footprint against the audited one |
| a02d — the same with `set_option warn.sorry false` and the word `sorry` hidden in a backticked comment | **passes** | fails | fails | source: `sorry` (comments are blanked, not exempted); source: `set_option`; command allowlist; the axiom walk |
| a03 — `#exit` after a forged footprint, with a never-elaborated false theorem after it | **passes** | fails | fails | command allowlist; Lean's `#exit` warning; module theorems against source theorems; printed footprint against audited |
| a04b — `/- -/ theorem … := sorry` on one line, under drop-warning | not recorded | fails | fails | source: `sorry`; command allowlist; the axiom walk |
| a05b, a05c — `sorry` in a private theorem, and in a counted theorem, with the word hidden by a trailing backticked comment | **passes** | fails | fails | source: `sorry`; command allowlist; the axiom walk; private declarations refused |
| a06 — `/- -/ unsafe def` plus `@[implemented_by]` plus a fake `DecidableEq` instance plus `decide +native`: a false theorem with the kernel apparently on | **passes** | fails | fails | source: `+native`; source: `unsafe`/`implemented_by`; the axiom walk; the kernel re-add |
| a08 — `namespace`/`end` read from inside a block comment so a top-level false theorem shares an honest theorem's print line | **passes** | fails | fails | the comment scanner; module theorems against source theorems; the axiom walk |
| a09b — six theorems of `Move.sv = Move.sh` in forms the v2 counter did not count (`private`, `nonrec`, `/-- doc -/ theorem`, `theorem`⏎`name`, `set_option … in theorem`) | **passes** | fails | fails | command allowlist; module theorems against source theorems; private declarations refused; the axiom walk |
| a12c — `import Lean` hidden behind a comment prefix, then `run_cmd … addDecl (.axiomDecl …)` adding an axiom with no keyword | not recorded | fails | fails | source: `import`; command allowlist; the module header's imports; the axiom walk |
| a14c — `/- -/ axiom Foo.propext : False` and a counted, printed `theorem Z14c_counted : (1 : Nat) = 2 := Foo.propext.elim` | not recorded | fails | fails | source: `axiom`; command allowlist; exact-name axiom comparison, which does not confuse `Foo.propext` with `propext` |
| AttA2 — `#guard_msgs (drop warning) in def ZA_sv_eq_sh : … := by admit` and `abbrev ZA3_false : False := by admit`: the def/abbrev gap the reviewer found in their own prototype | not recorded | fails | fails | command allowlist; the axiom walk returns sorryAx; and in v2.2 also the Prop-typed-non-theorem check, which is the structural answer |
| T09a–c — `axiom` with an attribute, in a `set_option … in`, and behind a doc comment, each giving `1 = 2` and hidden behind `propext` | **passes** | fails | fails | source: `axiom`; command allowlist; the axiom walk |
| T10 — `decide +native` with `propext` in the same footprint line | **passes** | fails | fails | source: `+native`; the axiom walk |
| T11b — the `#guard_msgs` drop-and-forge chain | **passes** | fails | fails | command allowlist; the axiom walk; printed footprint against audited |
| T12 — `private theorem tamper_priv : (1:Nat) = 2 := tamper_ax6`, with no print line | **passes** | fails | fails | source: `axiom`; command allowlist; the axiom walk; private declarations refused |
| T18 — a theorem with no `#print axioms` line and a `#print axioms` line naming a non-theorem; the finding was that `sh check.sh` turned both checks into stderr syntax errors and printed OK | fails | fails | fails | under bash, both 1h failures; under `sh`, v2.1 reports them too and v2.2 refuses to run at all |

### The eleven files that pass, and why that is right

A gate that fails everything is not a gate. Each file that comes back green was
read; none holds a false, forged or unsound claim.

| file | what it adds | why passing is correct |
|---|---|---|
| `fp01-theorem-in-block-comment`, `T14_block_comment_ghost`, `verify-v2-repro-10/t14/T14`, and the siblings `S1`, `S2`, `S3` | a `theorem`, a `sorry`, or a `partial def` inside `/- … -/` or after `--` | honest Lean. v2 **failed** four of these, which is the gate-11 finding: its regexes read comments as code. The comment scanner introduced in v2.1 is what makes them pass, and passing is the correct answer |
| `fp02-nested-namespace`, `fp03-section-inside-namespace`, `fp04-print-axioms-two-spaces` | `namespace` inside `namespace`; `section … end` inside a namespace; `#print  axioms` written with two spaces | honest Lean that **v2 and v2.1 both rejected**. The namespace prefix was held in one variable, so an inner `namespace` overwrote the outer name and a `section` cleared it; and the matcher for the print lines wanted exactly one space. v2.2 keeps the prefix on a stack and allows any run of whitespace. This is the gate-11 finding properly closed: a check that fails honest Lean is one that gets loosened later, and loosening it under pressure is how a real hole gets in |
| `verify-v2-fidelity-1/probes/probe` | the reviewer's probe: `[(1, 1), (-1, 1)]` misses both axes, is not in the open first quadrant, and its `sh`-mark survives all four moves | every theorem in it is true. It is the evidence for the wording fix in §7 of their report, now made in this file |
| `verify-v2-fidelity-5/probes/skeptic` | the skeptic's probes P3, P3b and others about S3's language | true theorems. This file also found a false positive in the first draft of the v2.2 Prop-typed check: Lean generates `P3d_exists_definable.match_1_1`, a Prop-typed *definition*, for a theorem that pattern-matches on a proposition. The check now exempts Lean's own `match_N` auxiliaries when the declaration they belong to is a constant of the module, which is the same exemption the private-declaration check uses |
| `verify-v2-gate-5/run-a06/ctrl-honest-ne` | `theorem Z06_honest : Move.sv ≠ Move.sh := by decide` | a control written to pass, and true |
| `a10-name-vs-statement` | `Z10_sv_fixes_whole_plane : True := trivial`, and `Z10_mirrors_equal (h : Move.sv = Move.sh) : Move.det Move.sv = 1` | both statements are true; only the names mislead. No gate that reads how a proof was made can refuse this, and refusing it would mean refusing honest theorems with badly chosen names. `STATEMENTS.md` is the answer: the statement is printed beside the name, so the two can be compared |
| `a11a-shadow-det-namespace` | `namespace Z11; def Move.det := fun _ => 1; theorem T3_det_mirrors_positive (g) : Move.det g = 1` | true about `Z11.Move.det`. Same class as `a10`, and the same answer: in `STATEMENTS.md` this statement prints as a statement about `Z11.Move.det`, because the audit loads the module without running this file's own `notation` declarations and prints with `pp.notation false`, so none of them is in the way |

**Two files that v2.1 passed and v2.2 refuses**, both honest in content:
`verify-v2-repro-3/work/T12b-priv-only` (`private theorem tamper_priv_clean :
(1:Nat) = 1 := rfl`) and `verify-v2-gate-9/mine/h2-private-honest-no-print`
(`private theorem Zh2_true : (1 : Nat) + 1 = 2 := rfl`). Both are true. Both are
refused because a private theorem is invisible to the source-level count, needs
no `#print axioms` line, and would not appear in `STATEMENTS.md`. That is the
reviewer's gate-9 finding with the dishonest content removed, and it is the
shape rather than the content that v2.2 declines.

### What changed in the gate, v2.1 to v2.2

1. **It refuses to run under `sh`, or under bash in POSIX mode.** The reviewer's
   repro-4 finding was that `sh check.sh` turned v2's two coverage checks into
   stderr syntax errors and printed OK. v2.1 had already removed the process
   substitution those checks used, so `sh check.sh` happens to work there —
   measured: v2.1 under `sh` passes the honest file and fails T18 correctly. It
   works by luck rather than by design, so v2.2 stops. Testing `BASH_VERSION`
   alone is not enough, because POSIX-mode bash sets it; the test is `[ -o
   posix ]`, as their skeptic established.
2. **Toolchains are discovered, not assumed.** Each listed toolchain that is
   installed is run; if none is, the `lean` on `PATH` is used; the output names
   the versions that ran and the `OK` line claims all three only when all three
   ran. A machine with no Lean gets `FAIL: no Lean found` rather than three
   confusing "toolchain not executable" lines on a file that is fine.
3. **The audit reads every constant, of every kind.** This is ask 1 and the
   section-6 gap. The reviewer's prototype enumerated `thmInfo` only, so it
   passed `abbrev ZA3_false : False := by admit`. Their own test of v2.1
   (`AttA2`) in fact fails, because v2.1 already ran `collectAxioms` over every
   constant and caught `sorryAx` — but that was the axiom walk doing the work,
   and a Prop-typed definition with a clean footprint would still have passed.
   v2.2 adds the structural check: a constant whose type is a proposition and
   which is not a theorem is refused outright.
4. **Axiom names are compared by exact match**, against `propext`,
   `Classical.choice` and `Quot.sound`. `Foo.propext` and `propext2` are not
   `propext`.
5. **The imports are read from the compiled module's header**, where the source
   text cannot reach them, and each one has to be `Init`.
6. **Every declaration is re-added to a fresh `Init`-only environment through
   the kernel**, using `Kernel.Environment.addDecl` — the kernel's own entry
   point, which, unlike `Environment.addDeclCore`, has no `doCheck` parameter to
   pass `false` to. A build made under `debug.skipKernelTC true` is re-checked
   from nothing. The audit runs with `loadExts := false`, so no module
   initializer and no `@[init]` function runs inside it, and it is run by the
   same toolchain that compiled the module, each toolchain being given its own
   `--print-prefix` sysroot. The reviewer's gate-15 skeptic showed why that last
   one matters: a 4.34.1 verifier reading a 4.33.0 `.olean` fails closed on an
   incompatible header, which is a failure and not a result.
7. **Private declarations are refused**, apart from the pattern-matching
   auxiliaries Lean generates for its own definitions, and only when the
   definition they belong to is a constant of the module.
8. **The source checks run twice**, once over the file and once over a copy with
   the line breaks collapsed, because Lean reads a newline as whitespace. `admit`
   and `unsafeCast` were added to the words they look for.
9. **`STATEMENTS.md`.** The gate writes every theorem's elaborated statement
   beside its axioms, regenerates the file on every run, and fails if the
   regenerated listing differs from the committed one. The statements print as
   plain constant applications, `Eq a b` rather than `a = b`, because the audit
   loads the module with its environment extensions unloaded and sets
   `pp.notation false`: no *user* delaborator, no unexpander and no notation runs,
   and the class table is not loaded either, so an instance projection prints under
   its own name.  (Lean's builtin delaborators do run — binders, `fun` and field
   notation are theirs — which is the accurate form of the "no delaborator runs"
   sentence this report and the README both used to carry.)  So the
   `local notation "Move.det" => Z11b_fakeDet` trick —
   gate-12, which their skeptic raised in severity after finding that a
   non-local `notation` fools `#print` as well as `#check` — cannot change how a
   statement reads there.

The compiled-module audit began as `VerifyAxioms.lean`, the 139-line prototype
shipped with the reviewer's report. The program the gate writes is a rewrite
rather than a copy, but the design and several of the Lean 4.33 API facts it
rests on came from that prototype, and it is credited in `README_LEAN.md`.

### Attacks written against v2.2

Eight — five attacks and three tampers — each aimed at something v2.2 introduced
rather than at something it inherited. The second column is the full gate; the third is the audit program
run on its own against the compiled `.olean`, with the text checks bypassed,
which is the question "does the audit catch this, or only the greps?"

| attack | the v2.2 gate | the audit alone |
|---|---|---|
| A1 `def ZA_sv_eq_sh : Move.sv = Move.sh := by admit` — a Prop-typed definition, no `#guard_msgs` | fails: `sorry`/`admit` in source; Lean's own warning and `sorryAx` under all three toolchains; the axiom walk; the Prop-typed-non-theorem check | fails twice: the constant is reported as a Prop-typed non-theorem, and its axiom walk returns `sorryAx` |
| A2 `abbrev ZA3_false : False := by admit` | fails, the same five ways | fails twice, the same two ways |
| A3 `set_option debug.skipKernelTC true in theorem ZD_sv_eq_sh : Move.sv = Move.sh := unsafeCast ()` | fails: source `set_option`; source `unsafe`/`unsafeCast`; the axiom walk returns `lcProof`; the kernel rejects the re-add | fails twice, with the kernel saying `invalid declaration, it uses unsafe declaration 'unsafeCast'` |
| A4 the same with `set_option debug.skipKernelTC true` on line 1, governing the whole file, proving `False` | fails, the same four ways | fails twice, the same two ways |
| A5 `unsafe def ZF._unsafe_rec : Move.sv = Move.sh := unsafeCast ()`, used by a public theorem — a squat on the one name shape v2.2 exempts | fails: source `unsafe`; and the file does not compile at all under any of the three toolchains | not reached. Lean refuses the theorem: `(kernel) invalid declaration, it uses unsafe declaration 'ZF._unsafe_rec'`. A safe theorem cannot use an unsafe constant, so the squat is not expressible |
| B1 `seed` redefined from five points to three, every statement left character for character the same | fails on the listing | the definitions half of `STATEMENTS.md` differs on the body of `seed`; nothing else in the gate notices, which is the whole argument for carrying the definitions |
| B2 `T1_mul_comm` weakened to `Move.mul g h = Move.mul g h`, name kept | fails on the listing | one line differs: `Eq (g.mul h) (h.mul g)` against `Eq (g.mul h) (g.mul h)` |
| B3 the `↔` in `S1_one_of_five` weakened to `→`, proof adjusted | fails on the listing | one line differs, `Iff (…) (…)` against `… → …` |

B1, B2 and B3 come from the second review, described below; all three were green
under v2.1, and B2 and B3 are what it called the declared limit of a gate that
reads how a proof was made.

Two further checks on the gate's own machinery: `STATEMENTS.md` edited by hand
(one statement altered) fails, with the regenerated listing left beside it for
comparison; `STATEMENTS.md` deleted fails, because there is nothing to compare
against. `attack_matrix.json` holds all 236 corpus rows with their failure
reasons, these five, and the harness tests.

### The second review, and what it found that the corpus did not

While this pass was running, the same lane posted a second packet, on v2.1
itself rather than on the corpus. It reproduced the mathematics and the gate —
the honest run byte-identical in nine logs, every count recomputed, the 99 v2
statements byte-identical inside v2.1, the sixteen S4 theorems saying what the
README says — and raised five should-fix items. Two of them were things no
adversarial file in the corpus had reached, and both were real.

1. **The `sorry` source check was inert in a C locale.** v2.1 answered
   `@«sorryAx»` by putting the French quotation marks into the pattern itself:
   `«?(sorry|sorryAx)»?`. Under `LC_ALL=C` each of those marks is two bytes and
   the `?` binds to the second, so the pattern asked for a byte that was not
   there and matched **none** of `  sorry`, `:= by sorry`, `@«sorryAx»`,
   `foo sorryAx` — 0 of 4, against 4 of 4 under UTF-8. Reproduced here before
   fixing it. No file went green on it, because Lean's own warning and the
   compiled-module audit still fired, but the gate was printing "OK: no sorry"
   on a file with `sorry` in it, and eight rows of this report credited a layer
   that was not running. **Fixed** by stripping the quotation marks from the
   code before the token checks, which leaves every pattern plain ASCII, and by
   pinning `LC_ALL=C`. And because a check that cannot fire looks exactly like a
   clean file, the gate now **tests its own patterns** before it runs them: each
   of the six is given a line it has to match, the set is given an honest line
   none may match, and a disagreement stops the run.
2. **The output was byte-reproducible only under C collation.** `sort` and
   `comm` were unpinned; a UTF-8 locale moved 24 lines of section 5 without
   changing the verdict. **Fixed** by the same `LC_ALL=C`, and said in the
   README.
3. **"Any letter off both axes" was still false in six places.** Carried over
   from the first packet, which arrived three minutes after v2.1 landed.
   **Fixed** in all six, with the counterexample — `[(1, 1), (-1, 1)]` misses
   both axes, is not in the open first quadrant, and its `sh`-mark survives all
   four moves — now written into the theorem's own docstring and into the
   README.
4. **`attack_matrix.json` shipped without provenance.** **Fixed for the 236
   corpus rows**: each carries the file, its sha256 prefix, what the file
   attempts, the verdicts and the gate's own FAIL lines with the version banners
   normalised to a version number; and this section cites the file. Not fixed in
   v2.2 for the seventeen `attacks_from_the_v2_1_pass` rows, which carried no file
   and no hash, so a reader could not check that the file the table describes is
   the file that was run; the second reviewer said so, and v2.3 ships the eight of
   them that `SCIENCE_CHECK` had rebuilt, as files with their hashes, together
   with the generator that writes them.
5. **A statements listing alone is blind to a changed definition.** This is the
   one that changed the design. Their tamper redefines `seed` from five points
   to three: every statement about it stays character for character the same
   while what all of them mean changes. **Fixed** by carrying the definitions in
   the same file, bodies included — 135 of them beside the 164 theorems. Their
   two weakened-statement tampers, which were green under v2.1 and which that
   review called the declared limit of a proof-side gate, both fail now: B2 and
   B3 above.

Their notes also gave the gate `${ELAN_HOME:-${HOME:-}/.elan}` in place of a
bare `$HOME` (v2.1 aborted with `HOME: unbound variable` when `HOME` was unset),
the corrected line count in this report's header, the five S4 names missing from
the class-(a) list, `S4_unique_of_act` as a fifth restatement, `S3_fml_swapVH`
named in the README's T6 paragraph, and elan's URL.

### Every row of the reviewer's status table, tested

The second review's section 5 marked ten rows "claimed … not tested this run".
The replay covers all of them. Each row below is measured: the files are from
the corpus, run under all three toolchains.

| what the row asks about | files | v2.1 | v2.2 |
|---|---|---|---|
| 2.2 six `axiom` spellings | 6 | `a01a-attr-axiom`, `a01b-doc-axiom`, `a01c-setoption-in-axiom`, `a01d-split-axiom`, `a01e-commentprefix-axiom`, `a01f-attr-private-axiom` | fails | fails |
| 2.3 `admit` | 3 | `a02b-admit-guardmsgs-drop-forge`, `a02a-admit-warnsorry-drop-forge`, `a02d-admit-warnsorry-backtick-drop-forge` | fails | fails |
| 2.5 `implemented_by` / `unsafeCast` | 1 | `a06-native-implemented_by-false` | fails | fails |
| 2.6 same-line `/- -/` and backtick exemptions | 7 | `a04b-commentprefix-sorry-guardmsgs`, `a05b-backtick-private-sorry`, `a05c-backtick-counted-sorry-drop-forge`, `a07-skipKernelTC-forms`, `a12a-commentprefix-import`, `a13b-commentprefix-partial`, `a17c-native_decide-backtick` | fails | fails |
| 3.1 keywords split across a newline | 3 | `a01d-split-axiom`, `a12b-split-import`, `a09b-uncounted-theorem-forms` | fails | fails |
| 3.2 skipKernelTC spellings | 2 | `a07-skipKernelTC-forms`, `T05_skipKernelTC` | fails | fails |
| 3.3 uncounted theorem forms, `private` | 4 | `a09b-uncounted-theorem-forms`, `T12_private_theorem_doccomment_axiom`, `T12b-priv-only`, `h2-private-honest-no-print` | fails / passes | fails |
| 3.4 `import`, `run_cmd addDecl` | 3 | `a12a-commentprefix-import`, `a12b-split-import`, `a12c-import-addDecl-axiom` | fails | fails |
| 4.1 honest false positives of the old counter | 5 | `fp01-theorem-in-block-comment`, `fp02-nested-namespace`, `fp03-section-inside-namespace`, `fp04-print-axioms-two-spaces`, `T14_block_comment_ghost` | fails / passes | passes |
| 6 Prop-typed `def`/`abbrev` with `admit` | 1 | `AttA2` | fails | fails |

Two rows are not uniform, in opposite directions. The private-theorem case:
`T12b-priv-only` and `h2-private-honest-no-print` passed v2.1 and are refused by
v2.2, and both are honest — it is the shape v2.2 declines, not the content. And
the honest false positives, which only v2.2 gets right throughout: `fp01` and
`T14` pass from v2.1 onward, `fp02`, `fp03` and `fp04` only from v2.2, so that
row reads "fails / passes" under v2.1 and "passes" under v2.2.

### What v2.2 still does not do

- **It does not read English.** `a10` and `a11a` pass, correctly: their theorems
  are true and only their names mislead. `STATEMENTS.md` makes that visible to a
  reader; nothing makes it visible to a script.
- **A statement can still be opaque.** `theorem X : Foo` where `def Foo := False`
  prints as `Foo` in the listing. The listing shows the statement, not the
  definitions it names, and a reader following it has to follow those too.
- **The honest-file false positives are gone, but the risk is not.** gate-11 was
  about checks that fail honest Lean; the first draft of this pass's Prop-typed
  check did exactly that on the reviewer's own probe file, and it was caught
  because the corpus was replayed rather than sampled. A check added without
  that replay is a check that has not been tested.
- **It is text plus an audit, not a proof of the gate.** The audit is the part
  the file cannot write into. The source checks in front of it are convenience
  and speed, and a hole in them is a hole only if the audit also misses it.
- **The listing is a listing, not a reader.** It catches a changed statement and
  a changed definition because it is regenerated and diffed. It does not know
  whether the statement is the one anybody wanted. That is still a person's job,
  and `STATEMENTS.md` is written to be read once and then diffed.

---

## Appendix: all 118 theorems

Class (a) definitional, (b) exhaustive finite check, (c) general. "axioms" is
the `#print axioms` line from the build log; `none` means the proof is pure
computation the kernel ran to completion.

| theorem | class | note | axioms |
|---|---|---|---|
| `Move.act_I` | a |  | none |
| `Move.act_sv` | a |  | none |
| `Move.act_sh` | a |  | none |
| `Move.act_C2` | a |  | none |
| `Move.act_mul` | c | the hinge: the 16 table entries are composition of the actual maps, for every point | propext |
| `T1_mul_assoc` | b |  | none |
| `T1_one_mul` | a | the four table lines `I,h => h` restated | none |
| `T1_mul_one` | a | the four table lines `g,I => g` restated | none |
| `T1_self_inverse` | a | the four diagonal table lines restated; becomes geometry only via `act_mul` | none |
| `T1_mul_comm` | b |  | none |
| `T1_mem_all` | a | "only four moves" is stipulated by `inductive Move`, not proved here | propext |
| `T1_all_length` | a | length of a hand-written four-element list | none |
| `T1_all_distinct` | a | constructors of an inductive type are distinct automatically | none |
| `T2_probe_injective` | b |  | none |
| `T2_faithful` | c |  | none |
| `T3_det_mul` | b |  | none |
| `T3_act_matrix` | c | ties the matrix entries to `act`, for every point | propext, Quot.sound |
| `T3_det_eq_ad_sub_bc` | b |  | none |
| `T3_det_kernel` | a | reads the four-line `det` table back in iff form | none |
| `T3_det_mirrors` | a | reads the four-line `det` table back in iff form | none |
| `T4_fix_I` | a | the defining equation of `act I`; restatement: same statement as `Move.act_I` | none |
| `T4_fix_sv` | c |  | propext, Classical.choice, Quot.sound |
| `T4_fix_sh` | c |  | propext, Classical.choice, Quot.sound |
| `T4_fix_C2` | c |  | propext, Classical.choice, Quot.sound |
| `T4_mirrors_differ` | b |  | none |
| `R90_left_inv` | c | backs the word "inverse" in the prose; used by no later proof | propext |
| `R90_right_inv` | c | backs the word "inverse" in the prose; used by no later proof | propext |
| `T5_R90_conj_sh` | c |  | propext |
| `T5_R90_conj_C2` | c |  | propext |
| `Sq.act_inv` | c |  | propext |
| `Sq.ofMove_act` | a | two definitions written to agree, checked to agree | none |
| `T5_rot90_eq_R90` | a | two definitions written to agree | none |
| `T5_rot270_eq_R90inv` | a | two definitions written to agree | none |
| `T5_eight_distinct` | b |  | none |
| `T5_C2_commutes` | c |  | none |
| `T5_C2_conj_fixed` | c |  | propext |
| `T5_C2_never_sv` | c |  | propext |
| `T5_C2_never_sh` | c |  | propext |
| `T6_swapVH_hom` | b |  | none |
| `T6_swapVH_involution` | a | the definition is an involution by inspection | none |
| `T6_swapVH_det` | b |  | none |
| `T6_swapVC_hom` | b |  | none |
| `T6_swapVC_breaks_det` | b |  | none |
| `T6_three_interchangeable` | b |  | none |
| `T7_invariant_I` | c |  | none |
| `T7_invariant_mul` | c | closure, for every figure and every pair of moves | propext |
| `T7_both_mirrors` | c |  | propext |
| `T7_mirror_and_turn` | c |  | propext |
| `T7_turn_and_mirror` | c |  | propext |
| `T8_isSubgroup_iff` | b | ties the Bool test to quantification over the type, not over a list | none |
| `T8_sixteen` | a | length of a hand-written sixteen-element list | none |
| `T8_enum_complete` | b |  | propext |
| `T8_five_count` | b |  | none |
| `T8_five_list` | b |  | none |
| `T8_five_are` | b |  | none |
| `T8_no_three_element` | b |  | none |
| `T9_build` | c | seed-plus-image survives its own move, for every figure | propext |
| `T9_build_any` | c |  | propext |
| `T10_stab_subgroup` | a | `stab` is a definition; this checks the table against itself | none |
| `T10_stab_distinct` | a | as above | none |
| `T10_stab_is_pair` | a | as above | none |
| `T10_stab_I` | a | as above | none |
| `T10_subI_unused` | a | as above | none |
| `T10_det_table` | a | reads the `det` table back at four arguments | none |
| `S0_MoveSet_ext` | c |  | none |
| `S0_MoveSet_ext_iff` | c |  | none |
| `S0_allSubs_nodup` | b |  | none |
| `S0_allSubs_exactly_once` | b |  | none |
| `S0_subgroup_has_inverses` | a | restatement: `T1_self_inverse` packaged; the `MoveSet` binder is not used, so this is not a subgroup fact | none |
| `S0_invariant_iff_eq` | c |  | propext, Quot.sound |
| `S1_five_iff_subgroup` | b |  | propext |
| `S1_flag_true` | a | restatement: core's `decide_eq_true_eq` for this file's `flag` | propext, Classical.choice, Quot.sound |
| `S1_symSet_mem` | c |  | propext, Classical.choice, Quot.sound |
| `S1_symSet_closed` | c |  | propext, Classical.choice, Quot.sound |
| `S1_symSet_isSubgroup` | c |  | propext, Classical.choice, Quot.sound |
| `S1_one_of_five` | c | new: the T7+T8 conclusion, for every figure whatsoever | propext, Classical.choice, Quot.sound |
| `S1_no_three_element_symmetry` | c | restatement: `T7_both_mirrors` applied | propext |
| `S2_invariant_ofList` | c | new: invariance over the infinite plane reduced to a finite check | propext, Quot.sound |
| `S2_seed_off_axes` | b |  | none |
| `S2_seed_asymmetric` | c |  | propext, Quot.sound |
| `S2_mark_sv_exact` | c |  | propext, Quot.sound |
| `S2_mark_sh_exact` | c |  | propext, Quot.sound |
| `S2_mark_C2_exact` | c |  | propext, Quot.sound |
| `S2_markAll_invariant` | c |  | propext, Quot.sound |
| `S2_seed_subset` | b |  | propext, Quot.sound |
| `S2_not_invariant_of_region` | c | new: a figure inside a region its move reverses cannot survive it | none |
| `S2_mem_mark` | a | repackages core's `List.mem_append` and `List.mem_map` | propext, Quot.sound |
| `S2_mark_eq_build` | c |  | propext, Quot.sound |
| `S2_mark_invariant_self` | c |  | propext, Quot.sound |
| `S2_quadrant_mark_exact` | c | new: ANY non-empty seed drawn entirely inside the open first quadrant, not just the one drawn | propext, Quot.sound |
| `S2_seed_in_quadrant` | b |  | none |
| `S2_mark_sv_exact_via_general` | c | new: `S2_mark_sv_exact` again, as a one-term instance of `S2_quadrant_mark_exact` | propext, Quot.sound |
| `S2_mark_sh_exact_via_general` | c | new: `S2_mark_sh_exact`, the same way | propext, Quot.sound |
| `S2_mark_C2_exact_via_general` | c | new: `S2_mark_C2_exact`, the same way | propext, Quot.sound |
| `S2_realizes_stab` | c | new: four concrete figures have exactly the assigned symmetry sets | propext, Quot.sound |
| `S2_stab_is_symSet` | c |  | propext, Classical.choice, Quot.sound |
| `S3_swapVC_involution` | a | as above | none |
| `S3_tm_swapVH` | c |  | propext |
| `S3_fml_swapVH` | c | new: induction over the whole language, not one relabelling | propext, Quot.sound |
| `S3_no_formula_separates_mirrors` | c | new: T6's claim about every statement, proved | propext, Quot.sound |
| `S3_language_separates_turn_from_mirror` | b |  | none |
| `S3_language_separates_I_from_sv` | b |  | none |
| `S4_act_matrix` | a | `Sq.mat` and `Sq.act` written to agree, checked to agree, for every point | propext, Quot.sound |
| `S4_matAct_add` | c | additivity of an arbitrary integer matrix action | propext, Quot.sound |
| `S4_matAct_smul` | c | homogeneity of the same | propext |
| `S4_corner_maps` | b | 8 symmetries × 4 corners | propext, Classical.choice, Quot.sound |
| `S4_corner_onto` | c | every corner is an image, by the inverse; not a case check | propext, Classical.choice, Quot.sound |
| `S4_comp_act` | c | new: the hinge for the eight — the 64 table entries are composition of the actual maps, for every point | propext |
| `S4_comp_assoc` | b | 512 triples | none |
| `S4_id_comp` | a | the eight table lines `id, t => t` restated | none |
| `S4_comp_id` | a | the eight table lines `s, id => s` restated | none |
| `S4_comp_inv` | a | eight table entries restated against `Sq.inv` | none |
| `S4_inv_comp` | a | the same eight, the other way round | none |
| `S4_act_injective` | c | `T5_eight_distinct` in the form the classification needs | none |
| `S4_entries` | c | **the content**: an arbitrary integer matrix, sixteen candidates from the corner condition, eight killed by surjectivity | propext, Classical.choice, Quot.sound |
| `S4_unique_of_act` | c | uniqueness, written out — `∃!` is unavailable with no imports; restatement: `S4_act_injective` with the existence hypothesis repackaged | none |
| `S4_classification` | c | new: every corner-preserving integer matrix is one of the eight | propext, Classical.choice, Quot.sound |
| `S4_eight_are_all` | c | new: the same as a biconditional — this is what "all eight" means | propext, Classical.choice, Quot.sound |

## v2.3 — a fifth pass, against a second reviewer on another model

Claude Code ran the three lenses again over v2.2, on a different model family from the one that wrote the proofs, with thirty-two
skeptics rebuilding each finding from their own copies. They returned one blocker, twelve should-fix items and seventeen notes
(`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.2-SECOND-OPINION.md`, da2d6a94731565f0). The answers are in
`ANSWERS_v2.2_SECOND_OPINION.md` one by one and the diff is in `CHANGES_v2.2_to_v2.3.md`; this section is the adversarial half.

**The blocker, in one line.** A declaration whose name Lean's own `Name.isInternalDetail` calls internal was audited for axioms and
listed nowhere, so an `OfNat` instance named `_i` — or `proof_1`, which that function also calls internal and which has no leading
underscore — rebound the numeral in a public statement while the committed `STATEMENTS.md` stayed byte-identical. It is the first attack
in four passes to change what a theorem says with the gate green and the listing unmoved, and it did so without touching a proof.

What makes it worth more than its fix is where it sits. Every earlier hole was a *capability* the gate refused by spelling —
`native_decide`, `axiom`, `set_option`, `extern` — and every fix was another spelling. This one used the gate's own definition of what
counts as a declaration worth listing. Lean's `isInternalDetail` exists to keep a user's `#print` output tidy; v2.2 read it as "nobody
wrote this", which is a different claim. The fix stops asking what the name looks like and asks what it belongs to: a name is an
auxiliary when its parent is a constant of this module that Lean does not call internal — the derived constructors and recursors included — and every component after that parent is a shape Lean's own machinery
writes. On the honest file that accepts 345 names and rejects none, under all three toolchains and under 4.34.1.

The second half of the fix assumes the first will be got round eventually. A numeral is the one thing in a statement that prints the
same however it was bound, so the gate now reports any `OfNat` instance this module declares, by name, whatever that name is; and the
listing carries a third section with every constant the first two do not, so a hidden declaration is a visible row even when it is
classified as an auxiliary. The attack written here against that fix — the same instance under the name `Move.act._f`, which the
classification accepts — is caught by the numeral check and appears in the third section, and `check.sh`'s own header says so rather
than leaving it to be found.

**The attacks, rebuilt.** The reviewer's evidence directory was purged before this lane could read it, so every attack below was rebuilt
from the packet's one-line description of it by `attacks/build_attacks.py`, run against v2.2 and against v2.3 in directories of their
own. Three came out byte-identical to the hashes the packet records: 3f467c422bea4148, 16b0a1a016895688 and 7c01faa6f2a1a45f.

| attack | file sha256_16 | v2.2 | v2.3 |
|---|---|---|---|
| a hidden `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` and `T8_sixteen` proved by `rfl`: the numeral is rebound and the theorem reads `allSubs.length = allSubs.length` | 865a0adbc58f4106 | **passes** | fails |
| the same under the name `proof_1`, which `Name.isInternalDetail` also calls internal and which has no underscore | 3a445f6045d55e9a | **passes** | fails |
| a hidden `_k` proving `(allSubs.filter isSubgroup).length = 3`, where the answer is 5 | d55a180f17526376 | fails | fails |
| the same with the listing regenerated, which is the path v2.2 left green | d55a180f17526376 | **passes** | fails |
| the control: the same instance under the visible name `inst16vis` | 972f4f7eb24e6488 | fails | fails |
| written here: the same instance named `Move.act._f`, a name the classification accepts as an auxiliary | cb6455d67334203a | **passes** | fails |
| `open Nat in #eval (… IO.FS.withFile … .append …)`, which wrote a file during the gate's own run | c4f501246159fe57 | **passes** | fails |
| written here: the same IO from an `#eval` indented by two spaces, which Lean accepts as a top-level command | ea9b849369758a26 | **passes** | fails |
| `@[inline, extern "lean_nat_add"]` on `imageOf`, a definition the listing already carried | 16b0a1a016895688 | **passes** | fails |
| the `andF` and `orF` arms of `Fml.holds` swapped, arm order changed, right-hand sides in place | 3f467c422bea4148 | **passes** | fails |
| the same with the listing regenerated | 3f467c422bea4148 | **passes** | **passes** |
| the other spelling: the right-hand sides swapped, arm order left alone | e81fb7991e16cf83 | fails | fails |
| honest Lean with `sorry`, `axiom` and `set_option` inside a string literal | d7a7dae718f8c45d | fails | **passes** |
| the honest variant that has to pass: a doc comment of every banned word, a namespaced extra theorem | b99e16987e4d24ee | **passes** | **passes** |
| a theorem's `#print axioms` line replaced by `#print axioms Nat.add_comm` | 7c01faa6f2a1a45f | fails | fails |
| `@[simp]` on the line above an `axiom` declaration (section 5 row 2.2, untested until now) | 9684c2bbc806842c | fails | fails |
| `#exit` before the T8 block (row 2.4, not re-tested since v2.1) | f56319b02ebdc211 | fails | fails |
| `set_option` split from its argument across a line break (row 3.1, untested until now) | bb5e162fda4f1a01 | fails | fails |

**The three in-window toolchains, on PATH.** The listing's toolchain-window paragraph rests on runs the
table above does not carry, so they are here: the honest file under 4.30.0-rc2, 4.31.0 and 4.32.0, each
put on PATH as the only `lean`, with `ELAN_HOME` pointed at a directory whose `toolchains/` is empty, so
that none of the three listed releases is present and the gate falls back to the PATH entry. All three
regenerate the committed listing byte-identically, which is what the paragraph claims; the runs are in
`RUN_INDEX.tsv` under the names `path-4.30.0-rc2`, `path-4.31.0` and `path-4.32.0`, with that recipe
beside each. Those four logs — the three here and the 4.34.1 one — do not ship, and their recorded hashes
did not reproduce when the second reviewer ran the same setup: for 4.34.1 it measured
`9fe9ed7d5dde2c7b` where the row records `d7742a8245c7fc79`. What did reproduce there is what the
paragraph rests on: the exit code, the byte-identical regenerated listing, and the 4.34.1 drift text.

**One correction to the reviewer, on item 3.5.** The arm swap has two spellings. Swapping the arms — the reviewer's own file,
3f467c422bea4148 — leaves both halves of v2.2's listing byte-identical, which is what they reported and what reproduces here. Swapping
the right-hand sides instead leaves the arm order alone, and **v2.2 catches that one**, on the row for `Fml.holds.eq_def`, a generated
theorem the listing already carried, whose statement spells the handlers out in order. So the listing was blind to one spelling and not
to the other, and the finding's general claim — that nothing in the listing pins which arm belongs to which constructor — held for the
file it was built from rather than for the class. Science ruled on the severity on 22 October 2026: a should-fix, fixed for the packet's spelling by the third section, with the
characterisation theorems declined for this release to keep the count of 118 stable across every text and logged as a future hardening
option. v2.3 catches both spellings, on the equation lemmas in the third section, which say the mapping in one readable line: `Fml.holds.eq_4` is `Eq ((f.andF g).holds x) (And (f.holds x) (g.holds x))` on the honest file and
`Eq ((f.orF g).holds x) (And …)` on the tampered one.

**The verdict and the side effect.** Science's check of the first v2.3 build found the half of item 3.1 that the fix had missed. The
gate refused `open Nat in #eval (… IO.FS.withFile … )` in section 1, printed the FAIL, and then went on to section 2 and elaborated the
file under each toolchain, so the smuggled line wrote its file three times while the gate was running. A refusal that is followed by an
elaboration is a verdict, not a defence. The second build stops before section 2 whenever a source check has failed and says that the
file was not elaborated; the two `#eval` attacks now fail in about two seconds with nothing written, which the run index records per run
in its `files_the_subject_wrote` column. The limit this leaves is worth stating where a reader will meet it: elaborating any Lean file
can run code that file contains, the source checks and the allowlist are a list of what their author knew to look for, and a reader
checking a file from anywhere other than the published folder does that in a sandbox.

**The two fail-open paths, and what they cost.** With `comm` absent from PATH, three of v2.2's checks came back empty and read as
agreement: the tamper above passes v2.2 with exit 0 and a log a reader could not tell from an honest one. With the README argument
misspelled, the name check reported `0 ; all resolve: yes`. Neither is a clever attack; both are a reviewer noticing that a check which
cannot run looks exactly like a check that found nothing, which is the same observation that put the self-test into v2.2. v2.3 checks
every external program it uses before it uses any of them, gives `comm` and `join` a pair of files whose answer it knows, and fails on a
README argument that does not resolve.

**The honest file failing.** Under a PATH fallback resolving to Lean 4.34.1, v2.2 failed the honest file with the tampering message,
because 4.34 stops generating `Move.toCtorIdx` and `Sq.toCtorIdx`. A gate that calls an honest file a tamper is a gate that gets
loosened later, so v2.3 names the window the listing belongs to and labels a difference confined to rows for definitions Lean generates
as drift, printing what it then leaves uncompared. The author's first attempt at the README paragraph explaining this cited those two
constants in backticks, and section 3i — the check item 3.12 was about — failed the run under 4.34.1 because they do not exist there.

**The corpus, replayed.** All 236 files of `attack_matrix.json`, each with the v2 README as its second argument and
`--write-statements`, as the v2.2 matrix was recorded: 236 verdicts, 236 agreeing with the matrix, none changed. Forty of them were run
under both of this pass's builds of the gate and agree on the exit code and the FAIL lines in every case. The one file of 29 KB or more
that the matrix had no row for, `v2-fidelity/probes/probe.lean` (e56d585763a438b1), now has one: it fails.

## v2.4 — a sixth pass, against the second reviewer's reading of v2.3

The same reviewer read version 2.3 and returned three new holes, ten should-fix items and fourteen notes.
The honest control reproduced on their machine — exit 0 in 73 s, output byte-identical to the committed
`check_output.txt`, the listing regenerating byte-identical, all fourteen input hashes equal — and all
thirteen items of the must-pass set held, including the two `#eval` attacks that version 2.3 was written
to stop. Then three files went green anyway. Two of them prove a false statement; the third runs the
attacker's code during the gate's own run, which is the thing version 2.3 existed to prevent.

Science ruled all three blockers for the release on 22 October 2026, including the first, which one of the
reviewer's own skeptics had argued down to should-fix on the letter of the rule. A refusal followed by an
elaboration is a verdict printed after the fact.

### The scanner desynchronised on a character literal

`scan()` knew a line comment, a block comment and a double-quoted string, and that is all it knew. A line
ending in `'"'` — a character literal holding a quote — left it inside a string, so the next line was read
as string interior and blanked, and a `#eval` sitting there was invisible to every pattern in section 1.
The stop before elaboration never fired, the file was compiled under three toolchains, and the smuggled
`IO.FS.withFile` ran each time. The gate's own output said nothing was wrong.

The fix is in four parts, and the third is the one worth arguing about. `scan()` learned character literals
— opened only where the preceding character cannot end an identifier, so `g'` and `hp0'` are not literals —
and raw strings, with hash counting and a state that crosses lines. The scanner now writes its end state,
and a scan that ends anywhere but in open code is a failure before section 2, because a scanner that lost
its place cannot speak for the file. A new pattern refuses character literals and raw strings outright:
measured over the honest code with comments blanked there are none of either, no double quotes at all, and
37 single quotes on 23 lines, every one of them a primed identifier. Refusing a construct this file does not
use costs this file nothing and removes the class of hole rather than the instance. And the self-test grew
four probes, two of them in the direction that matters: a line ending in a character literal, and one
ending in a raw string, each have to leave the *following* line visible.

What the refusal does not cover is the obvious thing: it is a list of the syntax its authors know. Lean has
more lexical forms than three reviewers have thought of, and the next one is invisible in exactly the way
this one was.

### A numeral rebound behind an `abbrev`, and a `Neg` nobody looked for

Version 2.3 answered the hidden-instance attack by reporting every constant whose type's head is `OfNat`.
The reviewer wrapped the instance: `abbrev W := OfNat Nat 16` and then `instance : W := ⟨…⟩`, whose type's
head, as written, is `W`. The check was silent, the numeral `16` in `T8_sixteen` elaborated through the
attacker's instance, and a file that says five subgroups was made to prove three. The third hole is the
same one with a different class — a `Neg Int` instance rebinding `-1`, so that `Move.det Move.I = -1` is
provable with the determinant equal to 1 — and `Neg` was a class nobody had named.

Naming `Neg` too would have been the fourth finding of the same shape. What v2.4 does instead is stop
naming classes:

> Every constant of the compiled module that is not a theorem reports the head its type reduces to, and
> every definition also the head its body reduces to, each read after unfolding reducible wrappers. A head
> that is itself a declaration of this module is accepted as such. Every other head is compared against the
> set the honest file's own declarations produce, and anything outside it fails with the constant and the
> head named.

The two clauses are not decoration. Without the first, an honest definition built from this file's own
constructors fails: the skeptic's own probe file, which defines a `Fml` by `andF`, was refused by the
first draft of this rule because no honest definition in this file has a body whose head is `Fml.andF`.
A constant of this module cannot be an instance of a class from outside it, so a head that *is* one of this
module's declarations needs no allowlist. Everything else is compared against thirteen type heads and seven
body heads, measured constant by constant and identical under 4.32.2, 4.33.0, 4.33.1 and 4.34.1.

The rule catches all five instance attacks written against it, each naming the constant and the head: the
body of `SixteenInst` reduces to `OfNat`; `ThreeInst` the same; `negIntVisible` and `negIntLocal` to `Neg`,
the second from inside a `section`, which does not hide a constant from the compiled module; `myLT` to
`LT`. Where the attack adds a wrapper and an instance the gate reads 3 heads outside the set of 364 it
read; where it adds an instance alone, 2 of 362. On the honest file: 0 of 360.

What it does not cover is said in the gate's own comment and worth repeating here. It compares classes, not
instances: a second `Decidable` instance for a proposition this file already decides is inside the set, so
this rule does not separate an honest `Decidable` from a dishonest one. It reads heads after `whnf`, so an
irreducible wrapper reports the head it has. And the set is this file's vocabulary, which makes the rule
tight here and makes it refuse honest files that are not this one — see the cost, below.

### Names shaped like Lean's own

A `def` or `instance` named `Move.act._f` is classified as an auxiliary by the audit, which reads name
shape, and version 2.3 reported it nowhere. The reviewer's point was camouflage rather than bypass: the row
lands among 345 rows labelled "auxiliary of a listed declaration" and a reader scanning the third section
has no reason to stop on it. Measured here, the cross-check they proposed is free: of the module's 671
constants, 34 non-theorem constants carry a generated shape and none of them is named in the source; of the
166 names the source declares — 48 definitions and 118 theorems — none carries a generated shape. The intersection on the honest file is
empty. So v2.4 refuses a source-declared name of a generated shape before anything is elaborated, and the
audit fails on a constant it classified `aux` whose name appears in the gate's own list of source
declarations. The three attacks of this shape are caught in the source, in a few seconds — 6, 2 and 2 under
the plain runs the index records — without compiling anything.

### The attacks of this pass

Every file was rebuilt here from the reviewer's description, their own copies not being to hand at the
time; one of the rebuilds, `DESYNC_EVAL`, is byte-identical to the reviewer's file, and the other twelve
differ. The reviewer's files are kept in their preserved trees, and their re-run of version 2.4 names the
paths.

| attack | file (sha16) | v2.3 | v2.4 | caught by |
|---|---|---|---|---|
| `#eval` hidden behind a character literal, the reviewer's own file | `2f05dbb2e1ea6d89` | **passes, and runs the code** | fails before elaboration, nothing written | the literal pattern, then the allowlist, then the stop |
| the same smuggling spelled with a raw string | `66a2e64cff7acaad` | **passes** | fails before elaboration, nothing written | the same three |
| a file that ends inside a plain string, opened after a character literal | `84b28ac9093273a0` | **passes** | fails | the scanner's end state |
| `OfNat Nat 16` behind an `abbrev`, `T8_sixteen` rebound | `394f4265b65d9a7f` | **passes** | fails | the head rule: `SixteenInst` reduces to `OfNat` |
| the same, proving the five subgroups are three | `2a0a7218f1fa50fe` | **passes** | fails | the head rule: `ThreeInst` reduces to `OfNat` |
| either of those two under an auxiliary-shaped name | `679346bd4f734bee`, `a5d9ad3ad702a794` | **passes** | fails before elaboration | the generated-shape pattern, in source |
| a hidden `Neg Int`, proving `det I = -1` | `e3c7083d713059d7` | **passes** | fails before elaboration | the generated-shape pattern (the reviewer's instance is named `Move.det._f`) |
| the same under a visible name | `696a370cca6327c5` | **passes** | fails | the head rule: `negIntVisible` reduces to `Neg` |
| the same inside a `section` | `9397021b1b684739` | **passes** | fails | the head rule: `negIntLocal` reduces to `Neg` |
| a `def` named like an auxiliary | `421628fb75a2408f` | **passes** | fails before elaboration | the generated-shape pattern |
| a `private def`, which the source-level count cannot see | `f4f8e15bd0f18a22` | fails | fails | the private-name check, now with a real count beside it |
| an `LT Int` instance at priority 10000 | `479e787a4b37131f` | **passes** after regeneration | fails | the head rule: `myLT` reduces to `LT` |

The seconds each run took are in `RUN_INDEX.tsv`, which is where they are measured; a run refused in source
takes a few seconds and one that reaches the compiled-module checks takes about as long as the honest run.

### Projection classes surface by name; literal classes do not

The `LT` row is the reviewer's note, and it is the most useful thing in the packet for understanding why
the literal classes are the dangerous ones. With the foreign `LT` instance in place, the quadrant theorem's
row in the listing prints `myLT.lt 0 q.fst` where the honest row prints `instLTInt`. The foreign name is
*visible*: a reader comparing the listing against the honest one sees a name that is not Lean's and not
this file's. A numeral is the opposite. `16` prints as `16` whichever `OfNat` instance bound it, and `-1`
prints as `-1`; the delaborator erases the instance, so the row reads exactly as it should and the listing
has no signal at all. That asymmetry is why `OfNat` and `Neg` were worth blockers and the `LT` swap was
worth a note — and the head rule now covers both, since it reads the compiled constant rather than the
printed row.

### What the rule costs

An allowlist built from one file refuses other files. One honest file in the replay set fails version 2.4
and passed version 2.3, and it names the head that did it: a file that adds `def noteText : String := …`
fails because the type head `String` is outside this file's vocabulary. Before the own-constant clause was
added a second one failed — the skeptic's `Fml`-building probe — which is why that clause is in the rule.
Neither is a false claim about the published file; both are different files. But it is the honest statement
of the trade: this gate checks
*this* file, and a reader who adds an honest declaration of a new shape will see a failure that names their
own constant. The alternative, an allowlist of classes an attacker might use, fails in the other
direction, which is the direction that matters.

### The cases that are green by design

Three listing-committed tampers pass after the gate regenerates its own listing, and each leaves a readable
diff in `STATEMENTS.md` rather than a silent pass: the weakened statement of a theorem that kept its name,
the `seed` change from five points to three, and the Greek-nu alias. The arm swap is the fourth, with its
10 rows. The pipe-race fix behind that regeneration holds at four times this module's size — a 10,503-line
honest module regenerates with no broken-pipe lines. These are limits of regenerating, not of checking: a
reader who compares against the committed listing rather than rewriting it sees every one of them.

### Two more things the reviewer broke

A present-but-broken `cmp` — a stub that exits 0 on everything — made section 5 read as agreement and a
listing-tampered file pass with the honest log. Section 0c probed `comm` and `join` with known inputs but
took `cmp` and `diff` on trust; it now gives both a known pair. A stub `awk` was already caught, by the
self-test. This is an adversarial PATH rather than a stranger's clone, and it is recorded for the same
reason the `comm` finding was: a check that cannot run looks exactly like a check that found nothing.

And the per-toolchain line printed `private declarations: 0` as a literal, so a file with a private
declaration got the failure naming it and, three lines later, a zero. The line now counts the audit's own
classification: auxiliaries, names belonging to no declaration, private declarations, and heads outside the
file's own set, with the number of heads read beside it.

### What v2.4 still does not do

Everything the previous section says, and three more. It does not separate instances of the classes this
file does instantiate, so a second `Decidable` instance is a shape the head rule passes. It does not
characterise `Fml.holds`: the equation lemmas in the third section of the listing say which arm is which,
and the characterisation theorems that would make it a proof are still declined for this release, because
they would change the count of 118 that every text here carries. And it does not make a green light on a
copy from anywhere else mean anything: the file this folder is about is the one whose hash is recorded with
the DOI, and the listing is there to be read.
