# Lean v2.2 → v2.3: every change, old → new

Written for Claude Science's review before anything is staged. Each entry says what changed, where, and which finding of
`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.2-SECOND-OPINION.md` (da2d6a94731565f0) asked for it. `ANSWERS_v2.2_SECOND_OPINION.md`
answers the findings one by one; this file is the diff in words. Not final. Nothing publishes.

## 0. What did not change

**`TetrasemaphoreAlgebra.lean` is byte-identical to v2.2** — sha256 f066faf6595d22e9, 1503 lines, 118 theorems, 118 `#print axioms`
lines, zero imports. No statement was weakened, strengthened, renamed or added, and no proof was touched. Every finding in the packet is
about the gate, the listing or the prose, and the two findings that asked for a change in what a reader can see about the *definitions*
(the blocker and item 3.5) are answered inside the gate, where a change does not move any of the 118 statements. The counts a reader has
been quoting stay as they were: 118 theorems, 115 net of the three second proofs, 671 constants audited, 642 re-added through the kernel,
61 of 118 on no axioms.

**`lean-toolchain` is unchanged** (`leanprover/lean4:v4.33.0`, 302cd63c54178885).

## 1. `check.sh` — the blocker

The attack: a declaration whose name Lean's own `Name.isInternalDetail` calls internal was audited for axioms but listed nowhere, so

```lean
instance _i : OfNat Nat 16 := ⟨allSubs.length⟩
theorem T8_sixteen : allSubs.length = 16 := rfl
```

turned `allSubs.length = 16` into `allSubs.length = allSubs.length`, with STATEMENTS.md byte-identical and the gate green. The name
`proof_1` works the same way, so a rule keyed on the leading underscore would not have been a fix.

1. **The name classification moved into the audit program and gained a fourth class.** v2.2's `GateAudit.lean` asked two questions —
   `isPrivateName n`, then `n.isInternalDetail` — and wrote `vis` as `private`, `internal` or `named`, listing only `named`. v2.3 asks
   whether an internal-looking name belongs to a declaration the listing shows: it strips the `_private.<module>.<n>.` wrapper, walks up
   the name's components looking for a parent that is a constant of this module Lean does not call internal, and accepts the name as `aux` only when such a
   parent exists and every component after it is a shape Lean's own machinery writes (`match_N`, `eq_N`, `splitter`, `_proof_N`, `_f`,
   `_sizeOf_N`, `_unsafe_rec`, `_sunfold`, `_simp_N_N`, `_flat_ctor`, and a documented margin of others). Anything else Lean calls
   internal is classified `internal` — a name somebody wrote. `_i` and `proof_1` are both `internal`: their parent is the anonymous root,
   which is no declaration at all.
2. **Section 3j fails on `internal` as well as on `private`.** The old check carried the match/splitter/eq exemption in awk and fired
   only on `$4 == "private"`; the new one fires on either class and the exemption lives in the classification above. Old message: "the
   compiled module holds private declarations, which the source-level count and the statements listing cannot see". New message names
   both classes and prints the class, kind and name of each.
3. **Section 3k is new: an `OfNat` instance declared by this module.** A numeral is the one thing in a statement that prints the same
   however it was bound, so the audit reports any constant of the module whose type's conclusion is an `OfNat` instance, by name,
   whatever that name is. The honest file declares none (its numerals are core Lean's `instOfNatNat`), so this check is 0 on the honest
   file and names `_i`, `_k`, `inst16vis` and `Move.act._f` on the four rebuilt attacks that rebind a numeral. This is what catches the
   companion attack in section 2 of the packet — a hidden `_k` proving `(allSubs.filter isSubgroup).length = 3`, whose true value is 5 —
   after the listing has been regenerated, which is the path v2.2 left green.
4. **STATEMENTS.md has a third section, "Generated auxiliaries".** Every constant that is not `named`: 345 rows on the honest file, each
   with the name, the kind, the class the gate put it in, the statement (for a theorem) or the type and body (for a definition). A
   declaration hidden under an internal name appears here as a row, so the listing diff shows it even where 3j is not what catches it.
   The rows are byte-identical under 4.32.2, 4.33.0, 4.33.1 and 4.34.1, measured.
5. **The per-toolchain line in section 3 reports the new counts**, so that a check which found nothing looks different from a check that
   did not run: `names Lean calls internal: 345, each one an auxiliary of a listed declaration ; private declarations: 0 ; OfNat
   instances declared: 0`.

## 2. `check.sh` — the other findings

| # | Finding | Old | New |
|---|---|---|---|
| 3.1 | `open X in #eval` ran IO during the gate | the allowlist reduced each column-0 line to its first word | a second check (1g2) refuses every `#`-command other than `#print axioms <name>`, and `run_cmd`, `macro`, `macro_rules`, `syntax`, `notation`, `infix`/`infixl`/`infixr`, `prefix`, `postfix`, `elab`, `elab_rules`, `initialize`, `builtin_initialize`, `attribute`, `export`, `unif_hint`, `simproc`, `dsimproc`, `declare_syntax_cat`, `register_simp_attr`, `binder_predicate` — anywhere on a line of code, at any column, after any number of `in`s, and over the joined copy as well. Written here, not in the packet: Lean accepts a top-level command at **any column**, so an `#eval` that is merely indented was invisible to v2.2 too; the same check closes both |
| 3.2 | honest strings with banned words were refused | the scanner tracked string literals but emitted their contents | the scanner blanks the inside of every string literal, keeping the quotation marks (so `@[extern "…"]` still reads as an attribute); the self-test probes both directions — a banned word inside a string has to be blanked, a declaration behind a same-line doc comment has to survive |
| 3.3 | the gate passed with `comm` missing from PATH | `comm` ran inside `$(…)` whose status nothing reads | a new section 0c checks every external program before any of them is used (`awk sed grep sort comm join cut tr wc cmp diff head cat cp rm mkdir mv dirname basename`) and exits 1 naming what is absent; `comm` and `join` are then given a pair of files whose answer is known, because presence is not behaviour |
| 3.4 | `@[inline, extern "…"]` evaded PAT_1d | `@\[[[:space:]]*extern` — `extern` only as the first attribute | `@\[[^]]*\b(extern\|implemented_by)\b` — anywhere inside an attribute group; 0 hits on the honest file; a self-test line now carries `@[inline, extern "lean_nat_add"]` |
| 3.5 | the `andF`/`orF` arm swap | the listing printed no matcher and no equation lemma | the third section carries both; the swap moves 10 rows of the listing (11 lines on each side, 22 counting both sides of the diff), all in the third section: `Fml.holds.eq_4` and `eq_5`, the type and body of `Fml.holds.match_1`, its six private equation lemmas and its splitter. Science's ruling is proposed in `ANSWERS_v2.2_SECOND_OPINION.md`, item 3.5: should-fix, not blocker, and fixed |
| 3.8 | the honest file failed under a 4.34.1 PATH fallback with the tampering message | any listing difference was tampering | the window the listing belongs to is named (`LISTING_WINDOW`, 4.30–4.33); when every toolchain that ran is outside it and the difference is confined to rows for definitions Lean generates, the gate says `toolchain drift, not tampering`, names what it then left uncompared (rows for generated definitions, and the count beside them), leaves the regenerated listing beside the committed one and does not fail. Inside the window, a difference is still a failure |
| 3.9 | `check_output.txt` carried the username in three paths | `echo "          $lean"` | `gate_path()` prints a toolchain under the elan root as `<elan root>/toolchains/…` and anything else under `$HOME` as `~/…`; `check_output.txt` is regenerated, and the README says six lines differ on another platform and none on another Mac with the same releases |
| 3.10 | `echo "$big" \| grep -q` under `pipefail` is a race | Lean's output and the audit output lived in shell variables | both go to files in `$WORK` (`elab.<n>.log`, `audit.<ver>.txt`) and every `grep -q`, `grep -E … \| head` and `sed … \| head` reads the file; the `| head -3` on the malformed-record check became a counter inside awk |
| 3.12 | a misspelled README path disabled the name check | nothing checked the argument | the gate fails with `no such README: <path>` before any check runs, and fails as well when the document cites no backticked Lean name at all (`ncited == 0`) |
| note 13 | the regenerated listing went to `./STATEMENTS.md.regenerated` in the cwd | `cp … "./STATEMENTS.md.regenerated"`, status unread | it goes beside `$STATEMENTS`, the `cp` status is read, and the gate says either where the copy is or that the directory would not take it |
| notes 1, 8, 9, 11 | prose inside the script | "no delaborator runs"; "two to three minutes"; `'sorry'` in apostrophes | the audit program's header says what `loadExts := false` does and does not remove and that builtin delaborators run; the header says one to three minutes and reports the measured range; the apostrophes stay, and `ANSWERS` says why (the sentence is this gate's own prose about its own check, not a quotation of Lean's warning — the grep that reads the warning matches either quoting) |

Three further changes the findings imply rather than name:

* the `--write-statements` message reports all three section counts;
* `def_list()` is new — the definitions the source declares, by name, which section 5 needs to tell a generated row from a declared one;
* the "WHAT CHANGED IN 2.3" block at the top of the script lists the above, and the "WHAT IT DOES NOT DO" block now states three limits
  rather than one: a constant hidden under a name that is both a generated shape and a listed declaration's child is classified `aux`
  (it is still a row in the third section, and 3k reports it if it is an `OfNat` instance); a change made and then committed is green by
  design, which is what the listing diff is for; and under an unlisted toolchain the rows for generated definitions are not compared.

## 3. `STATEMENTS.md`

Regenerated, not edited: 4613 lines where v2.2 had 2427.

* **The theorems section is byte-identical to v2.2's** — all 164 rows, 24,850 characters in 25,436 bytes, character for character.
* **The definitions section** differs in its three-line introduction only; all 135 rows are byte-identical. The count moved onto a line
  of its own (`Definitions listed: 135.`) so that section 5 can normalise it when it compares under an unlisted toolchain.
* **The header** was rewritten where the packet said it was wrong: "no delaborator runs" became an account of what `loadExts := false`
  and `pp.notation false` each do (note 1); the sentence claiming every non-theorem constant is listed became true as written, with the
  third section carrying the rest (item 3.5); and a paragraph says what a row does not carry — the instance a numeral elaborated through,
  the constructors of the inductives, the constants from `Init` — and names the toolchain window (items 2.1, 3.8, note 2).
* **The third section is new**: 345 rows of generated auxiliaries, with a paragraph saying that the equation lemmas are the readable ones
  and why they are there.

## 4. `README_LEAN.md`

Twelve edits, every one from section 8's list.

| Where | Old | New |
|---|---|---|
| the third paragraph | "Four claims … are now theorems" | six, each named (note 5) |
| the gate paragraph | "two to three minutes"; "so that `elan` picks that one up by itself" | "one to three minutes depending on the machine", the measured range, and the distinction between elan's proxy and the gate, which does not call elan and does not read `lean-toolchain`; plus "there is no `lakefile`, and none is needed" (notes 8, 9, 14) |
| the self-test paragraph | six patterns | seven, and the two scanner probes (item 3.2). The README's own count was left at six, which the fifth pass found and v2.4 corrects |
| the fallback paragraph | — | the tool check and what `comm` cost v2.2 (item 3.3) |
| `check_output.txt` | "Three of its lines carry a target triple" | six, which lines, and what 2.2's three path lines gave away (item 3.9) |
| the allowlist bullet | "Everything else is refused — `#eval` …" | the same list, plus what reading the first word of a line missed and what is refused anywhere on a line now; and the scanner blanking strings as well as comments (items 3.1, 3.2) |
| `STATEMENTS.md`, the companion file | "the audit loads the module with no delaborators: no notation, local or otherwise, can change how a statement reads in that file" (lines 183–184) and "it is the second half of `STATEMENTS.md` that sees it" (186–190) | an accurate account of what the audit loads and what prints, then a new paragraph headed **What that listing shows, and what it does not** — the three sections, the numeral that prints as itself whichever instance bound it, the hidden `_i` and `proof_1`, the two checks that answer them, attributes, and the toolchain window (items 2.1, 3.5, 3.8) |
| "What is proved" | "the number of distinct claims is unchanged at 115" | 115 net of the three second proofs; 114 distinct statement strings; 113 up to an implicit binder (item 3.7) |
| the axiom table | `propext, Quot.sound` 18 | 21 (item 3.6) |
| "How a skeptic can check this", step 1 | "two to three minutes" | one to three, and the toolchain-window paragraph with the 4.34 drift (items 3.8, note 9) |
| step 3 | "five further attacks" | five attacks and three tampers, and a sentence on the fifth pass and what it rebuilt (note 6) |
| step 4 | "the seven that restate another theorem" | eight (item 3.7) |

## 5. `RED_TEAM_LEAN.md`

Nine corrections, and a new section for this pass.

| Where | Old | New |
|---|---|---|
| §1 and the restatement table | "the number of distinct claims is still 115"; "the count of distinct claims is 115, not 118" | 115 net of the three second proofs, 114 distinct statement strings, 113 up to a binder, and which of the five bookkeeping rows are which (item 3.7) |
| §6, the gate's list | `extern` described as caught | the pattern caught `extern` only as the first attribute; H5's reasoning (that `extern` only attaches to `opaque`) was wrong, because core's `Nat.add` is an `@[extern] def`; and what v2.3 matches (item 3.4) |
| the single-check rows | "the forged footprint (e), caught only by the command allowlist" | the same, plus what the allowlist missed before v2.3 (item 3.1) |
| the v2.1 changes list | "a scanner that understands … string literals" | it tracked them without blanking them, which refused honest Lean, and what 2.3 does (item 3.2) |
| the corpus paragraph | "1,303 files" | 1,303 counting the 27 `.DS_Store` entries, 1,276 without, which is the reviewer's figure (note 4) |
| the listing paragraph | "no delaborator and no notation runs" | no *user* delaborator, no unexpander, no notation, and the class table unloaded; Lean's builtin delaborators do run (note 1) |
| "Attacks written against v2.2" | "Five" | eight — five attacks and three tampers (note 6) |
| the provenance row | "**Fixed**: every row now carries the file, its sha256 prefix …" | fixed for the 236 corpus rows; not fixed in v2.2 for the seventeen `attacks_from_the_v2_1_pass` rows, and what v2.3 ships instead (item 3.11) |
| new section, "v2.3 — a fifth pass" | — | the blocker and the twelve should-fix items, the attacks rebuilt from the packet's descriptions with their hashes and verdicts, the attacks written here, the corpus replay, and the three section-5 rows that had been untested until now |

## 6. New files in the folder

* `ANSWERS_v2.2_SECOND_OPINION.md` — one entry per finding, in the packet's order.
* `CHANGES_v2.2_to_v2.3.md` — this file.
* `SCIENCE_CHECK_v2.3.md` — the run table and the limits, as v2.2 had.
* `attacks/` — the 25 rebuilt attack files with their sha256 prefixes, `ATTACKS.tsv`, and `build_attacks.py`, the generator that writes
  them from the honest source (item 3.11 asked for the files or the generator; both are here).
* `RUN_INDEX.tsv` — every gate run behind those verdicts: file, gate, toolchains, exit code, seconds, log hash.

## 7. The second build of v2.3 (22 October)

Claude Science checked the first build and found the half of item 3.1 that the fix had missed: the gate refused
`open Nat in #eval (… IO.FS.withFile …)` in section 1, printed the FAIL, and then elaborated the file under each toolchain, so the
smuggled line wrote its file three times while the gate was running. The verdict was right and the code ran, and the evidence was
sitting in this author's own run directories.

| Where | Old | New |
|---|---|---|
| `check.sh`, between sections 1 and 2 | every run went on to elaborate, whatever section 1 had found | when any source check has failed the gate prints `FAIL: the file was not elaborated` with the reason — elaborating a Lean file runs code the file contains, before any proof is checked — then `FAILED.` and exits 1. Sections 2 to 7 do not run. `N6` and `N6b` now fail in about two seconds with no evidence file written |
| `check.sh` header | three limits stated | a fourth, above them: elaborating any Lean file can run code it contains; the source checks and the allowlist are a list of what their author knew to look for; a reader checking a file from elsewhere does that in a sandbox |
| `README_LEAN.md` | the allowlist bullet ended at what is refused | it says the gate stops rather than elaborating a file it has refused, and a new paragraph before "What the gate does not catch" carries the limit and the sandbox sentence |
| `RED_TEAM_LEAN.md` | the v2.3 section described the fix | a paragraph, "The verdict and the side effect", on what Science found and what a refusal followed by an elaboration is worth |
| `ANSWERS…md` item 3.1 | the fix as first built | the half that was missed, how it was found, what the second build does, and the limit |
| `ANSWERS…md` item 3.5 and ask 1 | a ruling proposed to Science | Science's ruling of 22 October 2026, accepted as proposed, with the characterisation theorems declined for this release and logged |
| `ANSWERS…md` section 4 heading | "the seventeen notes" | "the fourteen notes", with the discrepancy between the packet's summary line and its own numbering noted |
| `SCIENCE_CHECK_v2.3.md` | — | two new sections: the ruling, and what the second build changed |
| `RUN_INDEX.tsv` | eleven columns | twelve: `files_the_subject_wrote`, which records any `evidence_*.txt` the subject left behind, so a side effect of a final-build run is recorded beside its verdict rather than inferred from it |

The honest path is untouched by all of this: `check_output.txt` is byte-identical under both builds (2dbf34d60d59b9c1), which is how the
change was checked.

## 8. One change that came from the gate catching this author

The first build of the v2.3 README cited `Name.isInternalDetail`, `_i`, `andF`, `fun`, `in` and `lakefile` in backticks. Section 3i
looked all six up, found none of them, and failed the run. Five are not constants of this file by design — two Lean keywords, a file
name, Lean's own function, and the name of an attack that exists only in prose — and are now in `NOT_CONSTANTS` beside `IsKleinFour`
and `Z_fakeDet`, which are there for the same reason. The sixth, `andF`, was this author's error: the file's constructor is `Fml.andF`,
and the README now says so. The check that caught it is the one item 3.12 was about.
