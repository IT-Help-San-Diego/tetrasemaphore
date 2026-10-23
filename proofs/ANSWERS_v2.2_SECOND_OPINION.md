# Answers to the Lean v2.2 second opinion

One entry per finding of `~/Downloads/TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.2-SECOND-OPINION.md` (sha256 da2d6a94731565f0,
508 lines), in the packet's order: its id, what it found, the verdict here — **fixed**, **narrowed**, **declined** or **no action
needed** — and the evidence. Written for Claude Science's review; nothing is staged and nothing publishes until Carey says final.

**How the evidence was obtained.** The packet's own evidence lives in `/private/tmp/claude-501/…/scratchpad/wf-lean22/`, which is purged;
none of it was reachable from here. Every attack below was therefore **rebuilt from the packet's one-line description of it**, by
`attacks/build_attacks.py` applied to the honest v2.2 source (f066faf6595d22e9), and re-run. Three of the rebuilt files came out
byte-identical to the hashes the packet records for them — `M1a_holds_arm_swap` 3f467c422bea4148 (the packet's
`fidelity/attacks/M1-holds-andF-orF-swap`), `N3b_extern_sameline` 16b0a1a016895688 (its `skeptic-L3-SF-4-1/attacks/N3b_extern_existing_def`)
and `Comm_tamper_dangling_print` 7c01faa6f2a1a45f (its `skeptic-L3-SF-2-0` tamper) — which is as close to their files as this lane can
get. Where a rebuilt file behaved differently from what the packet reports, the entry says so.

Every verdict below rests on a run recorded in `RUN_INDEX.tsv`: gate, subject file and its sha256 prefix, toolchains, exit code,
seconds, and the sha256 prefix of the gate's own output. v2.2 and v2.3 were run on the same files, in directories of their own, so each
entry has a before and an after.

---

## Section 2 — the blocker

### 2.1 L3-BLOCKER-1 — a hidden, internal-named instance rebinds a numeral in a public statement

**What it found.** `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` in front of `theorem T8_sixteen : allSubs.length = 16 := rfl` makes
the theorem read `allSubs.length = allSubs.length`; the gate stays green and the committed `STATEMENTS.md` is byte-identical, because
`GateAudit` wrote statements and definitions only for names `Name.isInternalDetail` does not call internal. Skeptic 1 widened it: the
name `proof_1` does the same, and it carries no underscore. Companion: a hidden `_k` proving
`(allSubs.filter isSubgroup).length = 3` — whose true value is 5 — fails on the listing count as submitted and is green once the listing
is regenerated, leaving a row that reads as a proved falsehood.

**Verdict: fixed, by two independent checks and a third section of the listing.** Reproduced first: under v2.2, `N1_hidden_instance`
and `K1d_proofN_name` both exit 0 with the same log hash (7af0693036e4d5ea), as the packet's two skeptics also found, and
`N1b_regen` exits 0 — all three green, on this machine, from files rebuilt here.

The fix is not keyed on the name's spelling. `GateAudit.lean` now classifies every constant of the module into `named`, `private`, `aux`
or `internal`: `aux` means the name's parent is a constant of this module that Lean does not call internal — the derived constructors and recursors
included, so a parent may have no row of its own — and every component after that parent is a shape Lean's
own machinery writes (measured on this file under 4.32.2, 4.33.0, 4.33.1 and 4.34.1: `eq_N`, `_proof_N`, `_proof_N_N`, `match_N`,
`splitter`, `_sizeOf_inst`, `_sizeOf_N`, `_unsafe_rec`, `_sunfold`, `_simp_N_N`, `_f`, `_flat_ctor`). `_i` and `proof_1` have no parent
at all — the anonymous root is not a declaration — so both are `internal`, and **section 3j now fails on `internal` as well as on
`private`**. On the honest file the classification is 345 `aux`, 326 `named`, 0 `internal`, 0 `private`, identical under all three
listed toolchains.

A second check answers the companion, which the listing cannot: **3k reports any constant of this module whose type is an `OfNat`
instance**, because a numeral prints as itself whichever instance bound it. The honest file declares none. `_i`, `_k`, `inst16vis` and
`Move.act._f` are each named by it, so the `_k` variant fails after the listing has been regenerated, which is the path v2.2 left green.

Third, **the listing gained a section**: the 345 generated auxiliaries, each with its class, so a hidden declaration is a visible row
even where the two checks above are not what catches it.

Also run, written here rather than in the packet: `N1e_aux_named_instance`, the same instance under the name `Move.act._f`, which the
classification accepts as `aux`. 3j does not report it; 3k does, and it is a row in the third section. That residual is stated in
`check.sh`'s own header and in the README rather than left to be found.

**Evidence.** Runs `v22/N1_hidden_instance`, `v22/K1d_proofN_name`, `v22/N1b_false_row_hidden_instance`, `v22/N1b_regen`,
`v22/N1c_visible_instance`, `v22/N1e_aux_named_instance` and their `v23/` counterparts in `RUN_INDEX.tsv`; attack files and hashes in
`attacks/ATTACKS.tsv`.

---

## Section 3 — the twelve should-fix items

### 3.1 L3-SF-1 — `open X in <command>` bypasses the allowlist; a smuggled `#eval` runs IO during the gate

**What it found.** The allowlist reduced each column-0 line to its first word; `open` is allowed and nothing re-examined what followed
`in`, so `open Nat in #eval (… IO.FS.withFile … .append …)` ran disk IO while the gate was running. Skeptics widened it to
`variable … in`, `section … in`, `theorem … := … in` and `def … in`.

**Verdict: fixed, and widened again.** Under v2.2 the rebuilt `N6_eval_sees_wrapper` exits 0 with a log byte-identical to the honest
`check_output.txt` (5bbe6fb27678d396) and leaves `evidence_N6.txt` in the run directory. v2.3 adds check 1g2: every `#`-command other
than `#print axioms <name>`, and `run_cmd`, `macro`, `macro_rules`, `syntax`, `notation`, `infix`/`infixl`/`infixr`, `prefix`, `postfix`,
`elab`, `elab_rules`, `initialize`, `builtin_initialize`, `attribute`, `export`, `unif_hint`, `simproc`, `dsimproc`,
`declare_syntax_cat`, `register_simp_attr` and `binder_predicate`, refused **anywhere on a line of code**, at any column, after any
number of `in`s, and over the line-break-collapsed copy as well. 0 hits on the honest file.

One thing this lane found that the packet did not: **Lean accepts a top-level command at any column**, so an `#eval` that is merely
indented was invisible to v2.2's allowlist too — the scanner marks a line as beginning a command only when it starts in column 1.
`N6b_indented_eval` exits 0 under v2.2 and writes its evidence file. The same check closes both, because it does not look at columns.

**The half of this finding the first v2.3 build missed.** Science's check of that build found the gate refusing both `#eval` attacks in
section 1 and then elaborating the file anyway, under each toolchain in turn, so each attack still wrote its evidence file three times —
in the first build's own run directories, where this author had read the verdict and not looked for the file. The finding was about the
smuggled command running, and a refusal followed by an elaboration does not stop it. The second build stops before section 2 whenever a
source check has failed, printing one line that says the file was not elaborated and why; both attacks now fail in about two seconds
with nothing written. Every run of the final build in `RUN_INDEX.tsv` carries a `files_the_subject_wrote` column recording what the subject left
behind, which is `none` for every run of version 2.4's own gate. The runs where the IO did fire are in the index with the file
they wrote: the two `#eval` attacks under the v2.2 gate (rows 375 and 376, `evidence_N6.txt` and `evidence_N6b.txt`) and the two scanner
attacks under the v2.3 gate (rows 310 and 311, `EVID_DESYNC.txt` and `EVID_RAW.txt`). The rows that predate the column carry `not
recorded`. The honest path is unchanged: its output is byte-identical to `check_output.txt`
(2dbf34d60d59b9c1) under the second build.

The limit this leaves, plainly: elaborating any Lean file can run code the file contains, and the source checks and the allowlist are
what stands between a reader and that code — a list of what their author knew to look for. A reader checking a file from anywhere other
than the published folder does that in a sandbox. That sentence is in the README, in `RED_TEAM_LEAN.md` and in the script's own header.
The texts the finding called false are corrected: `check.sh`'s section-1 banner, README's allowlist bullet and RED_TEAM's
single-check row.

### 3.2 L3-SF-3 — string literals are not blanked, so honest strings with banned words are refused

**Verdict: fixed.** `scan()` blanks the inside of every string literal and keeps the quotation marks, so `@[extern "…"]` still reads as
an attribute. The self-test gained two scanner probes — a banned word inside a string has to be blanked, a declaration behind a same-line
doc comment has to survive — because a check that cannot fire looks like a clean file. `F2_string_sorry` fails under v2.2 with the three
FAILs the finding names and passes the source checks under v2.3. `check.sh` lines 12–13, which the finding called an overstatement, are
now true as written. The honest file is unaffected either way: its 17 lines carrying a double quote are all inside doc comments.

### 3.3 L3-SF-2 — the gate fails open when `comm` is missing from PATH

**Verdict: fixed, fail-closed on every external tool.** Reproduced: the skeptic's tamper — one theorem's `#print axioms` line replaced
by `#print axioms Nat.add_comm`, rebuilt here byte-identical to their file (7c01faa6f2a1a45f) — fails under v2.2 with the full PATH
(`v22/withcomm`: unprinted theorem, dangling print, footprint disagreement) and **passes under v2.2 with `comm` removed from PATH**
(`v22/nocomm`, exit 0). v2.3 checks all nineteen external programs it uses before using any of them and exits 1 naming what is absent,
and then gives `comm` and `join` a pair of files whose answer it knows, because presence is not behaviour. `v23/nocomm` fails with
`these programs this gate uses are not on PATH: comm`.

### 3.4 L3-SF-4 — `@[inline, extern "…"]` evades the extern check

**Verdict: fixed.** `PAT_1d` matched `@[` followed by `extern`, so only a first-position `extern` was caught. The rebuilt
`N3b_extern_sameline` (byte-identical to the skeptic's file, 16b0a1a016895688) exits 0 under v2.2 with the listing unchanged. v2.3
matches `@\[[^]]*\b(extern|implemented_by)\b` — 0 hits on the honest file, a hit on every probed spelling — and the self-test carries
`@[inline, extern "lean_nat_add"]`. H5's reasoning in RED_TEAM, that `extern` only ever attaches to the refused `opaque`, is corrected
there: core Lean's own `Nat.add` is an `@[extern] def`.

Noted for the record: the variant with the attribute on its **own line** (`N3b_extern_existing_def`) fails under v2.2, but for an
unrelated reason — a line consisting only of an attribute group reduces to the empty string and the allowlist reports it as
unrecognised.

### 3.5 fid22-1 — the `andF`/`orF` arm swap, and the severity question put to Science

**What it found.** Swapping the two match arms of `Fml.holds` changes what the connectives mean with the gate green and the committed
listing byte-identical, because the definitions half prints `Fml.brecOn … Fml.holds._f` and the arm-to-constructor mapping lives in
auxiliaries that were listed nowhere. Its finder and both skeptics kept it at should-fix and asked Science to rule, because it meets the
letter of the blocker rule and not its substance.

**Verdict: fixed, and narrowed; a ruling is proposed below.**

*Narrowed first, because the mechanism is not quite what the packet says.* There are two ways to write that swap. Swapping the **arms**
(the `orF` pattern first, each right-hand side left where it stood) gives the packet's own file, 3f467c422bea4148 — rebuilt here
byte-identical — and under v2.2 it is green: theorems half and definitions half both byte-identical to the honest build, measured from
the compiled `.olean`. That part reproduces exactly. Swapping the **right-hand sides** while leaving the arm order alone
(`M1b_holds_rhs_swap`, e81fb7991e16cf83) is a different compiled module, and **v2.2 catches it**, on `STATEMENTS.md` line 139 — the row
for `Fml.holds.eq_def`, a generated theorem the listing already carried, whose statement spells the handlers out in order. So the
listing was blind to one spelling of this attack and not to the other; the finding's headline holds for the file it was built from, and
its general claim — that nothing in the listing pins the arm mapping — does not.

*The fix.* The third section of `STATEMENTS.md` carries every generated auxiliary. The arm swap moves 10 rows of the listing (11 lines on each side, 22 counting both sides of the diff), all in the third section: `Fml.holds.eq_4` and `eq_5`, the type and body of `Fml.holds.match_1`, its six private equation lemmas and its splitter.

```
Fml.holds.eq_4   ∀ (x : Nat → Move) (f g : Fml), Eq ((f.andF g).holds x) (And (f.holds x) (g.holds x))
```

which becomes `Eq ((f.orF g).holds x) (And …)` in the tampered build. That is the arm mapping in one line, for a reader, and it is also
what makes the swap fail the gate. The same rows cover `Move.mul`, `Sq.comp`, `Move.act` and `Sq.act`, whose tables the finding named as
carrying the same blindness. The rows are byte-identical under all three listed toolchains and under 4.34.1, so this costs no stability.
`STATEMENTS.md`'s own sentence about listing every non-theorem constant, which the finding called false as written, is now true, and
README 187–193 is rewritten.

*The ruling proposed to Science: should-fix, not blocker, and fixed anyway.* Three reasons. First, the two attacks differ in kind. The
blocker makes a *claim* false: `T8_sixteen` stops saying what it says, and the `_k` companion proves a count of 3 where the answer is 5.
The arm swap relabels two constructors of a toy object language, after which all 118 theorems remain true of the relabelled semantics,
no axiom or `sorry` enters, and the file still proves that the language has a conjunction and a disjunction — only which name denotes
which has moved. Second, the damage it does is to the *prose*, not to the proofs: the README's sentence calling `Fml.andF` "and" becomes
wrong, which is the class of defect this project answers by having a reader read `STATEMENTS.md` beside the README, not by having the
gate refuse. Third, the gate's own rule is about how a proof was made, and nothing about how these proofs were made changed.

Against that, the finder's point stands as the letter of the rule — a changed meaning, green, with the committed listing unchanged — and
it is why the fix was worth making regardless of where the severity lands.

**Ruled by Science, 22 October 2026: accepted as proposed.** A should-fix, fixed for the packet's spelling by the third section of the
listing. With the listing regenerated the swap stays visible in 10 rows of the listing (11 lines on each side, 22 counting both sides of the diff), all in the third section: `Fml.holds.eq_4` and `eq_5`, the type and body of `Fml.holds.match_1`, its six private equation lemmas and its splitter — a documented limit for a reader of
`STATEMENTS.md` rather than a hole in the gate. The characterisation theorems are declined for this release, to keep the count of 118
stable across every text that quotes it, and are logged as a future hardening option.

The option Science declined, logged for a later pass: characterisation theorems in the source
(`(Fml.andF f g).holds r = (f.holds r ∧ g.holds r) := rfl`, one per constructor) would break the proof outright instead of showing the
swap in a listing row. They would add six theorems and take the headline count from 118 to 124, which ripples into every document and
coin text that quotes it. Six lines and a re-run, whenever that count is being changed for another reason.

### 3.6 fid22-2 = R2 — the README axiom table says 18 where it is 21

**Verdict: fixed.** README's table row `propext, Quot.sound` now reads 21, and the column sums to 118. Recomputed from
`STATEMENTS.md`'s 118 non-generated rows in this run: 61 none, 22 `propext`, 21 `propext,Quot.sound`, 14 all three.

### 3.7 fid22-3 — "seven" restatements against RED_TEAM's eight, and "distinct claims 115"

**Verdict: fixed.** README now says eight, matching RED_TEAM's eight-row table. Both documents now distinguish the two counts: 115 is
118 net of the three second proofs; the listing carries 114 distinct statement strings (`T4_fix_I` prints exactly as `Move.act_I`, and
each second proof prints exactly as its original), and 113 if `S1_no_three_element_symmetry` and `T7_both_mirrors`, which differ only in
an implicit binder, are read as one.

### 3.8 R1 — the honest file fails with the tampering message under a 4.34.1 PATH fallback

**What it found.** Under 4.34.1 the audit finds 669 constants instead of 671, because 4.34 no longer generates `Move.toCtorIdx` and
`Sq.toCtorIdx`; the definitions half regenerates with 133 rows instead of 135 and the gate prints `FAIL: STATEMENTS.md differs … Either
a statement changed without the listing being updated, or the listing was edited by hand` — both explanations false in this case.

**Verdict: fixed, by labelling the drift and saying what is then left uncompared.** Measured here under 4.34.1: the theorems half is
byte-identical (164 rows), the third section is byte-identical (345 rows), and the definitions half differs by exactly the two rows
named, `Move.toCtorIdx` and `Sq.toCtorIdx`, neither of which the source declares. v2.3 names the window the listing belongs to, and when
every toolchain that ran is outside it and the difference survives dropping rows for definitions the source does not declare, the gate
says `toolchain drift, not tampering`, prints which rows it did not compare, leaves the regenerated listing beside the committed one,
and exits 0. Inside the window, a difference is still a failure, with the old message. `v22/path4341` fails with the tampering message;
`v23/path4341` prints the drift paragraph and exits 0. The window is stated in `STATEMENTS.md`'s header, in the README's step 1 and in
`check.sh`.

Getting there took one more correction, of this author's own prose. The first v2.3 README explained the drift by naming the two
constants in backticks; 4.34.1 is the release that removes them, so section 3i looked them up, did not find them, and failed the run
that was meant to demonstrate the fix. They are named without backticks now, and the run that `RUN_INDEX.tsv` records is the one made
after that — gate build d6e8a00ff33ed454, the build `RUN_INDEX.tsv` names, exit 0.

The residual, stated rather than left: under an unlisted toolchain a change confined to rows for definitions Lean generates is not
compared. Adding `deriving Inhabited` would be such a change; it would be visible in the source, in the theorems half nothing moves, and
a reader who wants those rows compared runs one of the three listed versions, which is what the README asks for anyway.

### 3.9 R4 — `check_output.txt` ships the username in three paths, and "three lines differ" is nine

**Verdict: fixed.** The toolchain path prints as `<elan root>/toolchains/…`, or `~/…` for a `lean` outside the elan root, so the
recorded output carries no username. `check_output.txt` is regenerated. The README now says six lines carry a target triple and commit —
three in section 2, three in the summary — so a run on another Mac with the same three releases differs in no line at all and a run on
another platform in six.

### 3.10 R3 — `echo "$big" | grep -q` under `pipefail` is a race, in both directions

**Verdict: fixed.** Lean's elaboration output and the audit output are written to files in `$WORK` and every `grep -q`,
`grep -E … | head` and `sed … | head` reads a file. The `| head -3` on the malformed-record check became a counter inside awk. Nothing
pipes a shell variable into a program that exits early any more, so neither the spurious failure the reviewer saw twice under load nor
the fail-open direction (a `sorry` file with ~150 KB of elaboration output labelled `[ok]`) has a path. The 236-file replay in this pass
ran five and then eleven gates at once on a 16-CPU machine with no occurrence of either.

### 3.11 R6 — the eight rebuilt v2.1-era attacks have no file, hash or row

**Verdict: fixed.** All eight are rebuilt from `SCIENCE_CHECK_v2.2.md`'s table — `a2_guard_msgs_printaxioms`,
`a5_macro_decide_native`, `a9_quoted_sorryAx`, `a10_macro_command`, `a13_extern_space`, `a15_full_chain`, `a16_macro_sorry`,
`a17_poison_audit` — and ship in `attacks/`, each with its sha256 prefix in `ATTACKS.tsv`, together with `build_attacks.py`, the
generator that writes them from the honest source. All eight were run under v2.2 and under v2.3, so the matrix rows carry an rc for both
where they carried `None`. RED_TEAM's claim that every row carries provenance is corrected to say which rows do.

### 3.12 R7 — a missing or misspelled README path silently disables the name check

**Verdict: fixed.** The gate fails with `no such README: <path>` before any check runs, and fails as well when the document cites no
backticked Lean name at all. `v22/readme-typo` passes with `README names checked: 0 ; all resolve: yes`; `v23/readme-typo` fails.
This check then caught its own author: the first v2.3 README cited `Name.isInternalDetail`, `_i`, `andF`, `fun`, `in` and `lakefile` in
backticks, five of which are not constants of this file by design and one of which, `andF`, was an error — the constructor is
`Fml.andF`. `CHANGES_v2.2_to_v2.3.md` §8 records it.

---

## Section 4 — the fourteen notes

(The packet's summary line counts seventeen notes and its section 4 numbers fourteen, each covering one or more finding ids; Science
noted the discrepancy. The fourteen below are one-to-one with the numbered notes.)

1. **fid22-4, "no delaborator runs" is the wrong explanation.** *Fixed.* The audit program's header, `STATEMENTS.md`'s header, the
   README and RED_TEAM now say what is accurate: environment extensions are not loaded and `pp.notation false` is set, so no user
   delaborator, no unexpander and no notation runs and the class table is absent, which is why an instance projection prints under its
   own name; Lean's builtin delaborators do run, which is where binders, `fun` and field notation come from. The two settings are named
   in the listing's header.
2. **fid22-5, what a row cannot show.** *Narrowed, and partly fixed.* The matcher auxiliaries the printed bodies delegate to are now
   rows of their own (the third section). The other two classes the note names are stated in the header rather than listed: the
   constructors of each inductive, which appear in the type of its `casesOn`, and the 55 constants from `Init`. A second listing under
   `pp.explicit true` is declined for now — it would double a 287 KB file to show instance arguments that check 3k reports directly
   where they matter.
3. **fid22-6, SCIENCE_CHECK:51 states the S3/T6 item backwards.** *Fixed.* `SCIENCE_CHECK_v2.3.md` carries it the right way round: what
   the earlier packets asked for is a theorem that the table-only language does **not** separate `sv` from `C2`, and what was done
   instead was to soften the README sentence to what `T6_three_interchangeable` and `S3_fml_swapVH` actually prove.
4. **fid22-7, RED_TEAM's account of the lane is accurate; "1,303 files" counts 27 `.DS_Store` entries.** *Fixed* (1,303 counting them,
   1,276 without, which is the reviewer's figure). The corpus arithmetic reproduced here as well: 236 rows, 236 distinct hashes, all 236
   present on disk at the stated paths with the stated hashes.
5. **fid22-8, "four claims are now theorems" undercounts.** *Fixed:* six, each named in the README.
6. **R9, "five further attacks" against eight rows.** *Fixed:* "five attacks and three tampers from the second review", in both
   documents.
7. **R5, the corpus counts (refuted in its headline).** *No action needed on the counts*, which reproduce; *fixed* on what stood of it:
   `v2-fidelity/probes/probe.lean` (e56d585763a438b1, 54,383 B) was the one distinct file of 29 KB or more absent from the matrix. It
   now has a row, run under v2.3.
8. **R11, toolchain handling.** *Fixed:* the README now separates elan's proxy from the gate, which does not call elan and does not read
   `lean-toolchain`.
9. **Timing.** *Fixed:* "one to three minutes depending on the machine", with the measured range, in both the script and the README.
10. **The three second proofs are independent routes.** *No action needed.* Confirmed by the fidelity lens from the compiled module; the
    README and the file describe them correctly.
11. **Cosmetic.** *Partly declined.* The listing part is fixed (note 2 above). The apostrophes in `check.sh`'s source-check message stay:
    that sentence is this gate's own prose about its own check, not a quotation of Lean's warning, and the grep that reads the warning
    (`declaration uses .sorry`) matches either quoting, which the finding also says.
12. **Other fail-closed and false-positive results.** *No action needed.* Re-measured here: `v23/honest_control` passes, `F1` — a doc
    comment made of every banned word, plus a namespaced extra theorem with its own `#print axioms` line — passes with the listing
    regenerated.
13. **R10, `STATEMENTS.md.regenerated` and the cwd.** *Fixed.* The regenerated copy is written beside `$STATEMENTS`, the `cp` status is
    read, and the gate says either where the copy is or that the directory would not take it. The README says to run the gate from
    inside the folder.
14. **R8, release files.** *Declined for now, by the agreement the note itself cites:* LICENSE, CITATION.cff, .zenodo.json and README.md
    go in when Carey says final, with the licence decided at release. The one part that was cheap is done: the README says there is no
    `lakefile` and none is needed.

---

## Section 5 — the rows that were still reading "not tested"

Three rows of the packet's table said a shape had not been tested in this run. All three are tested here, against v2.2 and v2.3, and
all three fail both.

| row | rebuilt as | v2.2 | v2.3 |
|---|---|---|---|
| 2.2, the attribute and newline spellings of `axiom` | `S5_22_attr_newline_axiom` — `@[simp]` on the line above `axiom ZA_evil : Move.sv = Move.sh` | fails | fails |
| 2.4, `#exit` | `S5_24_exit` — `#exit` before `T8_five_count` | fails | fails |
| 3.1, a keyword split across a newline | `S5_31_keyword_split_newline` — `set_option` on one line, `debug.skipKernelTC true in` on the next | fails | fails |

---

## Section 6 — fidelity

Items 1 to 6 are findings of fact about the listing, the three second proofs, the 115 carried statements, the README and RED_TEAM
claims, and the laugh test on the 118. *No action needed* on the facts; the four places they name as needing rewording —
`STATEMENTS.md` 15 and 1344–1346, README 183–193 — are rewritten (items 2.1, 3.5, note 1). The two wrong numbers are items 3.6 and 3.7
and the undercount is note 5. The theorems half of the listing is byte-identical to v2.2's, so every statement those items checked is
character for character what it was.

---

## Section 7 — reproducibility and packaging

1. **The fresh-copy run.** *No action needed*, and re-measured: v2.3 on a fresh copy passes under all three listed toolchains, output
   recorded as `check_output.txt`.
2. **The refusals.** *No action needed* on the ones that hold; the two fail-open paths are items 3.3 and 3.12 and the
   fail-closed-by-mistake path is item 3.8, all fixed.
3. **Toolchains.** *Fixed* in the prose: the window is named, and the drift under 4.34 is labelled rather than reported as tampering.
4. **The matrix's consistency.** *Fixed* for the two gaps: the eight rebuilt attacks have rows with files and hashes (3.11), and
   `probe.lean` has a row (note 7).
5. **What the release still needs.** The blocker and the twelve should-fix items are answered above. LICENSE, CITATION.cff,
   .zenodo.json, README.md remain for release (note 14). `check_output.txt` is regenerated. The toolchain-window sentence is in. The
   matrix carries rows for N1, K1d, N1b, N1c, N1e, N6, N6b, N3b, M1a, M1b, the `comm` and README-path harness cases, the string probe
   and the 4.34.1 fallback.
6. **This packet's evidence.** *Not actionable here:* `/private/tmp` was purged before this lane started, so nothing under
   `scratchpad/wf-lean22/` was readable. Everything was rebuilt from the descriptions, as the opening note says. The v2 evidence copy
   under `~/Downloads/TETRASEMAPHORE-CC-LEAN-V2-SECOND-OPINION/` was read and not written: all 236 corpus files are present with the
   hashes the matrix records.
7. **Spend.** Not this lane's to report.

---

## Section 8 — the asks

1. **Rule on 2.1's fix and on 3.5's severity.** 2.1: both, not either — section 3j fails on any user-written internal name, and the
   listing carries every constant that is not `named`, so a hidden instance forces a listing diff as the visible-name control already
   did. 3.5: should-fix rather than blocker, with the fix made regardless — ruled by Science on 22 October 2026, accepting the
   reasoning above and declining the characterisation theorems for this release. A second pass of the three lenses on v2.3 before the
   repository is welcome; the attacks of this pass and their hashes are in `attacks/`, which should make a re-run cheaper.
2. **The `check.sh` list.** All eleven are done: the allowlist after any `in` (3.1), strings blanked plus two self-test probes (3.2),
   every external tool checked and `comm`/`join` probed (3.3), the extern pattern (3.4), the auxiliaries printed (3.5), the
   toolchain-window text and the drift label (3.8), the path relative to the elan root with `check_output.txt` regenerated (3.9), the
   four `echo | grep -q` sites and the two `| head` sites (3.10), a failure on a missing README argument (3.12), and the regenerated
   copy beside `$STATEMENTS` (note 13).
3. **The prose list.** Every line named in the ask is edited; `CHANGES_v2.2_to_v2.3.md` §§4–5 is the table of them.
4. **Packaging.** The eight rebuilt attack files with their hashes and matrix rows (3.11), `probe.lean` as a row (note 7), the release
   files when Carey says final (note 14).
5. **The rows still reading "not tested".** Section 5 above.
