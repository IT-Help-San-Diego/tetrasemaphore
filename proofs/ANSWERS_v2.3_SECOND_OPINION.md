# Answers to the second opinion on the Lean proofs, version 2.3

Claude Science, 22 October 2026. Answering
`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.3-SECOND-OPINION.md`
(sha256 `aed75362b5e20cc4…`, 388 lines), the second opinion on version 2.3 of this folder, written by Claude
Code on a different model family and read here as adversarial input rather than as instruction. The work
below was begun against that packet's draft (`73bce56d9d6ecfb8…`, 353 lines) and finished against the
final. The two were compared finding by finding and hash by hash and nothing a finding rests on differs:
the three blocker attack hashes, the eleven gate-log hashes they cite, every finding id, every skeptic
verdict and every proposed fix are the same text in both. What the final adds is per-blocker detail in its
second section and turn counts in its header.

The packet reports three new blockers, ten should-fix items and fourteen notes. Every one of the
twenty-seven is answered below, in the packet's own order and numbering. Each answer says what was
reproduced here, what changed in the folder, and where the change is. The gate in this folder is version
2.4; the Lean file is byte-identical to the one v2.2 and v2.3 shipped (`f066faf6595d22e9…`), and no
theorem, no statement and no proof changed in this pass.

**What the packet confirmed.** The honest control reproduced on the reviewer's machine: a fresh copy of the
eight shipping files exits 0 in 73 s with output byte-identical to the committed `check_output.txt`, the
listing regenerates byte-identical, all fourteen input hashes agree with ours, and all thirteen items of
the gate lens's must-pass set hold — every v2.2 blocker file fails under v2.3, named check by named check,
and the `#eval` attacks fail in one to two seconds with nothing written. That is the part of the second
opinion that says the first fix worked.

**What it found.** Three holes that leave the gate green, each reproduced here from the packet's
description. Two of them prove a false statement; the third runs the attacker's code during the gate's own
run, which is exactly what v2.3's headline fix was for.

---

## Section 1 — the three blockers

**Science ruled on the severity on 22 October 2026: all three are blockers for this release.**
L3-BLOCKER-1 stays a blocker although one of the packet's own skeptics argued should-fix under the letter
of the series' rule, because the rule exists to protect a reader, and a gate that refuses a line and then
elaborates the file anyway has already run the line. The rule's letter is about false statements; its
purpose covers this.

### L3-BLOCKER-1 — a character literal desynchronises the source scanner

*The finding.* `check.sh`'s `scan()` (v2.3 lines 362–388) knew three lexical states: a line comment, a
block comment and a double-quoted string. It did not know character literals. A line ending in `'"'` — a
character literal holding a double quote — left the scanner inside a string, so every following line was
read as string interior and blanked, until the next quote closed it. A `#eval` on the line after it was
invisible to all of section 1, the stop before elaboration (1z) therefore did not fire, and the file was
elaborated under three toolchains with the attacker's `IO.FS.withFile` running each time.

*Reproduced.* The packet's own copies were not to hand at the time — they are kept in the reviewer's
preserved trees, which its re-run of version 2.4 names by path — so the file was rebuilt here from the
description: `attacks/DESYNC_EVAL` (`2f05dbb2e1ea6d89…`), which is byte-identical to the reviewer's own
file. Under v2.3, with the listing regenerated first, it exits 0 and writes `EVID_DESYNC.txt` in the run
directory; plain, it fails at section 5 and writes the file anyway.

*The fix, and where.* Four changes, all in `check.sh`:

* `scan()` learned character literals and raw strings. A `'` opens a character literal only when the
  character before it cannot end an identifier, so a primed name like `g'` or `hp0'` is left alone; `r"`
  and `r#"` open a raw string, whose terminator counts hashes, and whose state carries across lines.
* The scanner now writes its end state, and a run whose scan does not end in open code fails before
  section 2 with the line that left it open. A file that ends inside a string, a comment or a literal is
  a file the scanner cannot speak for.
* A new source pattern (1g3) refuses character literals and raw strings outright. The honest file contains
  neither: measured over the code with comments blanked, 0 character literals, 0 raw strings, 0 double
  quotes, and 37 single quotes on 23 lines, every one of them a primed identifier. Refusing a construct this file does not
  use costs nothing here and removes the class.
* The self-test grew four probes: a line ending in a character literal and a line ending in a raw string
  each have to leave the following line visible, a primed name has to not read as a character literal, and
  the probe file's scan has to end in open code.

*Evidence.* `DESYNC_EVAL` now fails in about a second on 1g3 and 1g2 together, with the elaboration stop,
and writes nothing. The two variants written here against the fix — `DESYNC_EOF` (a file ending inside a
raw string) and `DESYNC_RAWSTRING` (the same smuggling spelled with `r#"`) — fail the same way. The run
index records `files_the_subject_wrote` for each.

### L3-BLOCKER-2 — an `OfNat` instance wrapped in an `abbrev`

*The finding.* v2.3's section 3k reported any constant whose type's head is `OfNat`, read with
`resultHead`, which looks at the type as written. An `abbrev W := OfNat Nat 16` followed by
`instance : W := ⟨…⟩` has type `W`, so 3k was silent, and the numeral `16` in `T8_sixteen` elaborated
through the attacker's instance. `allSubs.length = 16` became `allSubs.length = allSubs.length`, and the
file's own count of five subgroups could be proved to be three.

*Reproduced.* `attacks/ABBREV16` (`394f4265b65d9a7f…`) and `attacks/ABBREVFALSE`
(`2a0a7218f1fa50fe…`) elaborate cleanly under v2.3 and exit 0 after `--write-statements`.

*The fix, and where.* `check.sh` section 3l, with `unfoldedHead` in the audit program. The gate no longer
asks about `OfNat` by name. For every constant of the module that is not a theorem it reads the head of
the type, and for every definition the head of the body, unfolding reducible wrappers through `whnf`
first, and compares what comes out against the set this file's own declarations produce. `W` unfolds to
`OfNat`, which is not in the set, and the constant and the head are named in the failure.

### L3-BLOCKER-3 — a hidden `Neg` instance

*The finding.* The same hole for a different class. `instance _n : Neg Int := ⟨fun _ => 1⟩` rebinds the
literal `-1`, so `Move.det Move.I = -1` is provable with `Move.det Move.I` equal to 1, and nothing in the
listing shows which instance a negative numeral went through. 3k inspected `OfNat` only.

*Reproduced.* `attacks/NEGFALSE` (`e3c7083d713059d7…`) and the visible-name variant
`attacks/NEGFALSE_VISIBLE` (`696a370cca6327c5…`) both elaborate cleanly under v2.3. The
section-local variant written here, `attacks/NEG_LOCAL_SECTION` (`9397021b1b684739…`), puts the
instance inside a `section` so that it is local to the file region rather than to the module.

*The fix, and where.* The same rule, 3l. `Neg` is outside the honest head set, wherever it is declared and
whatever it is named, and a `section` does not hide a constant from the compiled module.

*One difference from the packet, and what it turned out to be.* The packet's second skeptic reports the
local instance placed in a `section` around the honest `T10_det_table`, with that theorem's own row
unchanged. The rebuild here could not reproduce that, because the body used here is
`fun _ => Move.det Move.I`: since `det I = 1`, the rebound `-1` makes `T10_det_table` read
`det sv = 1 ∧ det sh = 1`, which is false, its `decide` proof fails, and the file does not elaborate
cleanly. The reviewer's own body is `fun _ => Move.det Move.sv`, and since `det sv = -1` the statement
stays true and `decide` proves it, so the spelling does reproduce: their file
(`b6b2b08c3a111121…`, preserved at `skeptic-L3-BLOCKER-3-1/attacks/NEG-honest-local/`) exits 0 under the
v2.3 gate with the listing regenerated first, and version 2.4 refuses it in source at 1g4 on the name
`Move.det._f`. The body, not the spelling, is what the rebuild here got wrong; the variant shipped in
`attacks/NEG_LOCAL_SECTION` wraps an appended theorem instead, and the head rule catches that one.

---

## Section 2 — the rule that was chosen, and what it does not cover

Science asked for the packet's fixes and then for a general rule over the literal and notation classes
rather than a list of class names, preferring a rule that fails closed on constructs this file does not
contain, with the reasons and the limits stated. What v2.4 does:

**One rule for the classes, in two clauses.** Every constant of the compiled module that is not a theorem
reports the head its type reduces to; every definition also reports the head its body reduces to. A head
that is itself a declaration of this module — one of its own types, constructors, recursors or
definitions — is accepted as such, because a constant of this file cannot be an instance of a class from
outside it. Every other head is compared against the set the honest file's own declarations produce:
thirteen heads in types and seven in bodies, measured constant by constant and identical under 4.32.2,
4.33.0, 4.33.1 and 4.34.1. Anything else fails with the constant and the head named. `OfNat`, `Neg`, `LT`,
`OfScientific`, the arithmetic classes and the coercions are all outside that set, and so is a wrapper
that unfolds to one.

*Why a rule rather than more class names.* The packet's own two blockers are the same hole twice, found
twice, and a third spelling of it — `OfScientific` for a decimal, `HAdd` for an operator, `Coe` for a
coercion — would have been a fourth finding. A list of the classes an attacker might use is a list of the
ones its author thought of; the set of classes this file *does* use is finite, known, and measurable.

*What it does not cover.* It compares classes, not instances: the classes the honest file does instantiate
— `Decidable` and `DecidableEq`, `Repr`, `SizeOf`, the ones `deriving` and `inductive` write — are accepted as a set, so a
second, dishonest `Decidable` instance of a proposition this file decides is a shape this rule does not
separate from the honest one. It reads heads after `whnf`, so a wrapper that is not reducible, or one
whose unfolding exceeds the heartbeat budget, reports the head it has rather than the head it hides; the
budget is a million heartbeats and the honest file's 360 heads are read inside it. And the set is this
file's vocabulary, which makes the rule tight here and not portable: an honest file that adds a constant of
a shape this one has no example of fails the check. One file in the replay set does exactly that, and it
names its head in the failure.

**Fail closed on what this file does not contain.** Character literals and raw strings are refused in
source (1g3), because the honest file has none and the scanner's blind spot was in exactly those two
constructs. Source-declared names of the shapes Lean generates are refused (1g4), and the audit
cross-checks the same thing from the other side (3j). `abbrev` is *not* refused, although two of the
blockers use one, because the honest file declares one — `abbrev Pt := Int × Int` — and a check that
refuses what this file contains is a check that fails on this file. The blocker that `abbrev` carried is
answered by unfolding instead, which covers `def`, `instance` and `local notation` as well.

*What that does not cover.* The refusals are a list of the syntax their authors know: a construct neither
reviewer nor this author has thought of is not on it, and looks exactly like a clean file.

---

## Section 3 — the ten should-fix items

### 1. L3-SF-1 — a definition under a name Lean's generated shapes use

*Claimed.* A `def` or `instance` named like an auxiliary — `Move.act._f`, `Fml.holds._proof_7` — is
classified `aux` by the audit, reported by no check, and green after the gate regenerates its own listing;
its row lands among 345 rows labelled "auxiliary of a listed declaration", a label the gate infers from the
shape of a name. Split verdict: one skeptic kept should-fix, one lowered it to a note.

*Measured here.* True as stated, and the cross-check the packet proposes is clean on the honest file: of
the module's 671 constants, 34 non-theorem constants carry a generated shape and none of them appears in
the source text; of the 166 names the source declares — 48 definitions and 118 theorems — none carries a
generated shape. The intersection is
empty, so a rule that fails on any name in both sets costs the honest file nothing.

*Changed.* Two checks, both in `check.sh`. Section 1g4 refuses a source-declared name matching the
generated shapes before anything is elaborated. Section 3j fails when a constant the audit classified `aux`
appears in the gate's own `src_defs.txt` or `src_thms.txt`. The three attacks written for this —
`AUXNAME_DEF`, `ABBREV16_AUX`, `ABBREVFALSE_AUX` — are caught by both, and the second and third by the head
rule as well.

### 2. fid23-1 — `private declarations: 0` was a literal

*Claimed.* The per-toolchain audit line hardcoded the zero. On a file with a private declaration the gate
printed the 3j failure naming it and then, three lines down, "private declarations: 0". The shipped
`check_output.txt` was not false — the honest file declares none — but the line was not a count.

*Changed.* The line now counts the audit's own classification. It reads: *names Lean calls internal: 345
auxiliaries of a listed declaration, 0 belonging to none ; private declarations: 0 ; declaration heads
outside this file's own set: 0 of 360 read*. All four numbers are counted from the audit's rows. The
probe the packet used, rebuilt here as `attacks/PRIVATE_DEF`, now prints `private declarations: 1` beside
its failure. `check_output.txt` is regenerated; on the honest file the four numbers are 345, 0, 0 and 0 of
360.

### 3. fid23-2 — the arm-swap row count

*Claimed.* Two numbers for one measurement: 22 in `SCIENCE_CHECK` 80 and `ANSWERS` 166, 20 in CHANGES 64
and `ANSWERS` 142. Measured: 11 lines of diff under exactly 10 rows, all in the third section; 22 is the
line count of both sides together.

*Changed.* All four places now carry one text: *10 rows of the listing (11 lines on each side, 22 counting both
sides of the diff), all in the third section: `Fml.holds.eq_4` and `eq_5`, the type and body of `Fml.holds.match_1`,
its six private equation lemmas and its splitter.* The same count is now in the listing's own third-section
introduction, where a reader meets the limit.

### 4. fid23-3 — "six patterns" in the README

*Claimed.* README 69 said six where the gate looped over seven and printed seven.

*Changed.* The README says eight, which is what v2.4 loops over and prints — the six source patterns, the
refused-commands pattern (1g2) and the new literal pattern (1g3) — and the same paragraph now lists the
four new scanner probes.

### 5. fid23-4 — the `files_the_subject_wrote` column never recorded a file

*Claimed.* Three texts say the column records the side effect beside the verdict; in the shipped index the
column read `none` for every final-build run and `not recorded` for the v2.2 runs where the IO did fire,
and the first v2.3 build's runs were not in the index at all. So the side effect was evidenced in prose
only. Split verdict: one skeptic scoped the overreach to two sentences and found the other two accurate.

*Changed.* Both, and scoped more narrowly than this document first claimed: the sentence in
`SCIENCE_CHECK_v2.3.md`, which is where "for the runs of the final build" now stands, is scoped to the two
attacks it is about, and the sentence in `ANSWERS_v2.2_SECOND_OPINION.md` names the index rows that record
a written file; and the two `#eval` attacks were re-run under the v2.2 gate with the column recording, so the index now
carries rows where `files_the_subject_wrote` names the file the subject wrote. A `gate_sha16` column ties
every row to the build it ran under.

### 6. fid23-5 — the regenerated-swap row rested on two files

*Claimed.* The run named `M1_regen` is the right-hand-side spelling under v2.2 and the arm-order spelling
under v2.3, and the texts present the row as one attack. Both cells are true of their files; the index
carried neither counterpart.

*Changed.* The rows are named `M1a_regen` and `M1b_regen`, the missing counterparts were run — the arm
swap regenerated under v2.2, the right-hand-side swap regenerated under v2.3 and both under v2.4 — and the
tables carry one row each.

### 7. fid23-6 — attack rows with no file and no hash

*Claimed.* Ten rows of `new_attacks_on_v2_3` in `attack_matrix.json` carry no `file` or `sha256_16`, and
four rows of the RED_TEAM table print "—" for files that do ship with hashes in `attacks/ATTACKS.tsv`, so
the tables contradict each other even though every run is recoverable by name.

*Changed.* Every row of the matrix carries `file` and `sha256_16` where a file exists, and says so where
one does not (the PATH and README harness rows have no subject file of their own: they run the honest
file under a changed environment, and the row now names the command line instead). The four RED_TEAM cells
carry their hashes.

### 8. fid23-7 — counts that did not reproduce

*Claimed.* Five: "26 rebuilt attack files" where everything else says 25; "eighteen external programs"
where `REQUIRED_TOOLS` lists 19; "ten columns | eleven" where the file has twelve; a citation to CHANGES
section 7 for a note that is in section 8; and "24,850 bytes" for a section that is 25,436 bytes and 24,850
characters.

*Changed.* All five: 25, nineteen, twelve, section 8, and "24,850 characters in 25,436 bytes". The
provenance string in `attack_matrix.json` now lists the twelfth column.

### 9. R-1 — the corpus rows' mode

*Claimed.* All 236 corpus rows were labelled `plain` but were run with `--write-statements` against the v2
README, which is why 14 of them carry exit 0; proved by a hash that reproduces a recorded log only in that
mode.

*Changed.* The corpus rows are labelled `write-statements, v2 README`, the three mode values are defined in
`SCIENCE_CHECK_v2.4.1.md` under "The runs" and in the matrix's `provenance.v2_4_runs`, and the index's hash is
in this folder's hash table.

### 10. R-2 — the folder named none of what the texts cite

*Claimed.* RED_TEAM and the matrix cite `attacks/`, the generator, ANSWERS and CHANGES; the README
mentioned none of them, and a copy of the eight shipping files alone passes. Split verdict: one skeptic
kept should-fix, one lowered it to a note.

*Changed.* Science ruled on J7 on 22 October 2026: the public folder ships them. The README now has a
section saying what is in the folder and what each file is for, `attacks/README.md` says which attack files
run code when compiled — each writes one small text file in the directory it is compiled in — and that a
sandbox or a throwaway directory is the comfortable place to open them, and the `.DS_Store` files are out
of the release manifest. The gate still neither reads nor needs any of it: the eight shipping files alone
exit 0, which is the property the J7 decision was weighed against.

---

## Section 4 — the fourteen notes

1. **L3-NOTE-1, projection classes surface by name.** Confirmed and recorded. The `LT` instance swap
   rebuilt here (`attacks/LTSWAP`, `479e787a4b37131f…`) passes v2.3 after regeneration, and the row it
   changes prints `myLT.lt` where the honest row prints `instLTInt` — the foreign name is visible to a
   reader of the listing. That is the opposite of the literal classes, where the delaborator erases the
   instance and the row reads as honest, which is what makes `OfNat` and `Neg` the dangerous ones.
   `RED_TEAM_LEAN.md` now says so in the v2.4 section, and the head rule covers both.
2. **fid23-8, leftovers of replaced wording.** Three, all corrected: the README's "second half of
   `STATEMENTS.md`" is now the definitions section, RED_TEAM's "no delaborators" is now what the audit
   actually does (the module's own `notation` unloaded, `pp.notation false` set), and "two to three
   minutes" is now the measured range: 69 to 117 seconds here, 68 to 112 on the reviewer's machine, and
   the same for v2.2, v2.3 and v2.4.
3. **fid23-9, the documented limit was stated only in a comment.** It is now in two more places a reader
   reaches without opening the gate: the listing's third-section introduction and the README's listing
   paragraph. The README sentence was reported here before it was written and went in at version 2.4.1.
4. **fid23-10, "parent is a listed constant".** The code asks whether the parent is a constant of the
   module that Lean does not call internal, which includes the derived constructors and recursors, and
   those have no row of their own. The three places in `check.sh` that said "listed constant" — its header
   note, the `auxParent` doc comment and the section-3j comment — now say that, and the listing's
   third-section introduction says it to a reader. The three prose places (`RED_TEAM_LEAN.md`,
   `ANSWERS_v2.2_SECOND_OPINION.md` and `CHANGES_v2.2_to_v2.3.md`) were reworded at version 2.4.1.
5. **fid23-11, the `_private.Subject.0.` prefix.** Explained in the third-section introduction: the prefix
   is Lean's encoding of a private name, the `0` is its hash field, `Subject` is the fixed module name the
   gate compiles the file under, and the 121 rows that carry it are Lean's own private equation lemmas for
   matchers. The file declares nothing private.
6. **fid23-12, rows could not be tied to a gate build.** `RUN_INDEX.tsv` has a `gate_sha16` column. The
   citation to a build hash that appears in no shipped file was corrected at version 2.4.1, where this
   document had reported it done a pass early.
7. **fid23-13, a duplicated phrase and three missing harness rows.** The phrase is deleted, and the three
   in-window PATH runs (4.30.0-rc2, 4.31.0, 4.32.0) that the listing's toolchain-window paragraph rests on
   are named in `RED_TEAM_LEAN.md`, in the paragraph after its v2.3 table.
8. **R-3, "26 rebuilt attack files".** Part of fid23-7 above; corrected to 25.
9. **R-4, `M1_regen` names two files.** Part of fid23-5 above; the rows are `M1a_regen` and `M1b_regen`.
10. **R-5, a harness log hash that cannot be reconciled.** Confirmed: the 4.34.1 PATH-fallback row's log
    hash depends on the PATH the harness set, and no harness log shipped. Every harness row now carries its
    command line in the index, so the row says how to reproduce it rather than asking a reader to guess.
11. **R-6, `mktemp` and TMPDIR on macOS.** The README's temporary-directory paragraph now says where the
    directory comes from — `mktemp` under `$TMPDIR`, a per-user directory on macOS — and that everything
    the run writes goes in that one directory, whose path the run prints.
12. **R-7, a present-but-broken `cmp`.** Confirmed and fixed: section 0c now gives `cmp` and `diff` a known
    pair, so a stub that exits 0 on everything is caught before section 5 reads its silence as agreement.
13. **R-8, the limit-2 cases.** Recorded in RED_TEAM as the cases that are green by design: the weakened
    statement, the `seed` change and the Greek-nu alias each pass after regeneration and each leave a
    readable diff in the listing, and the pipe-race fix holds at four times the module size.
14. **R-9, `.DS_Store` and the singular OK line.** The release manifest excludes `.DS_Store`. On the OK
    line, the branch that was pluralised is the fallback one, which now reads "under the 1 toolchain that
    ran"; the listed branch still reads "under all 1 listed toolchains" where one toolchain is installed,
    and changing it would change the gate's bytes, which this release does not do.

---

## Section 5 — what was not done

* **The characterisation theorems for `Fml.holds`** are still declined, for the reason given in the
  previous answer: they would change the count of 118 that every text in this release carries. The
  equation lemmas in the listing's third section say the same thing, and the limit is now stated in three
  places rather than one.
* **The `Decidable`-instance shape** named in section 2 above is not separated from the honest instances of
  the same class. Distinguishing instances rather than classes means comparing instance bodies, which is a
  larger change than this pass; it is written down as the next hardening option.
* **Nothing in the Lean file changed.** No theorem was added, removed or restated in this pass, and the
  file's hash is the one v2.2 shipped.
