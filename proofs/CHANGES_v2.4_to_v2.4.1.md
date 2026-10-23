# What changed between version 2.4 and version 2.4.1 of the Lean folder

Claude Science, 22 October 2026. Documentation and run-index corrections only, from the second reviewer's
re-run of its existing attacks against version 2.4
(`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.4-RERUN.md`, sha256 `8f73859548ba5887…`), ruled by Science
on 22 October 2026. That re-run found **no blocker**; with it, the outside checking of the checker stopped.

**The gate and the proofs did not change.** `check.sh` (`ab6f55d3216e1f19…`),
`TetrasemaphoreAlgebra.lean` (`f066faf6595d22e9…`), `STATEMENTS.md` (`12b11a5e6651b386…`) and
`check_output.txt` (`df2f24dc4e5e3852…`) are byte-identical to the version 2.4 that was re-run, so the
re-run's verdicts carry over to this folder. No attack file was added, removed or changed, and no check
behaves differently.

## The corrections, one row per finding

Line numbers are the ones the re-run packet cites, against the version 2.4 files. Where a line number
pointed one line off, the passage was found by its words; those rows say so.

| id | file : line | was | is |
|---|---|---|---|
| L4-SF-1 | `RUN_INDEX.tsv` : 318, 320, 357, 359 | log hashes `afb6ba1cfa8934c0`, `7007a482ec443887`, `1a3127a5e336517e`, `3d032503d43ea5b4`, which do not reproduce from the shipped files | the four rows re-run against the shipped README and their hashes replaced with the measured ones: `933e3bd5c11e1e7f`, `82727dbbd8e57cfe`, `74f7992822e1d06e`, `71c21e625d46e2f1` |
| fid24-1 | `ANSWERS_v2.3_SECOND_OPINION.md` : 99 | `NEG_LOCAL_SECTION` as `723666a3910f0677` | `9397021b1b684739`, the file that ships |
| fid24-1 | `RED_TEAM_LEAN.md` : 1488 | the same stale hash in the attack table | `9397021b1b684739` |
| fid24-1 | `RED_TEAM_LEAN.md` : 1481 | `DESYNC_RAWSTRING` as `e049a849175573c1` | `66a2e64cff7acaad`, the file that ships |
| fid24-2 | `RED_TEAM_LEAN.md` : 1475–1476 | "three of the rebuilds are byte-identical to the reviewer's own files" | "one of the rebuilds, `DESYNC_EVAL`, is byte-identical to the reviewer's file, and the other twelve differ" |
| fid24-3 | `SCIENCE_CHECK_v2.3.md` : 122 | the README row `05644d85e3c90dd2` / 47,074, which is a pre-edit draft and no file on disk | `97d2a7572c05f57e` / 46,071, the README version 2.3 shipped |
| fid24-3 | `SCIENCE_CHECK_v2.3.md` : before "The files" | the section "One edit by Science after its review (22 October 2026)" was missing | restored verbatim from the copy version 2.3 shipped |
| fid24-3 | `CHANGES_v2.3_to_v2.4.md` : 75 | three changes to that file declared | the same three, plus the two above named as undeclared and put back here |
| fid24-4 | `ANSWERS_v2.3_SECOND_OPINION.md` : 199–200, `ANSWERS_v2.2_SECOND_OPINION.md` : 144 and 168, `SCIENCE_CHECK_v2.3.md` : 80, `CHANGES_v2.2_to_v2.3.md` : 64 | "10 rows of the listing (11 lines of diff, counting both sides)" | "10 rows of the listing (11 lines on each side, 22 counting both sides of the diff)" |
| fid24-4 | `ANSWERS_v2.2_SECOND_OPINION.md` : 144 | the leftover fragment ", among them rows, among them" | deleted |
| fid24-5 (a) | `CHANGES_v2.3_to_v2.4.md` : 85 | "thirteen columns, the new one being `gate_sha16`" | "fourteen columns, the two new ones being `gate_sha16` … and `command`" |
| fid24-5 (b) | `RED_TEAM_LEAN.md` : 1445–1446 | "six body heads" | "seven body heads", which is what `check.sh` lists and the audit reads |
| fid24-5 (c) | `CHANGES_v2.3_to_v2.4.md` : 72 | "the twelve attacks of this pass" | "the thirteen attack files of this pass, in a table of twelve rows" |
| fid24-5 (d) | `ANSWERS_v2.3_SECOND_OPINION.md` : 170–171, `RED_TEAM_LEAN.md` : 1466–1467 | 29 generated-shape constants, 165 source-declared names | 34 and 166 (48 definitions and 118 theorems); the intersection is still empty |
| fid24-5 (e) | `ANSWERS_v2.3_SECOND_OPINION.md` : 63, `RED_TEAM_LEAN.md` : 1414 | "23 single quotes" | "37 single quotes on 23 lines", every one a primed identifier |
| fid24-6 | `CHANGES_v2.3_to_v2.4.md` : 93 | "every one of the 236 files in the v2.2 replay corpus but one" | no corpus verdict changed; `F2_string_sorry`, one of the 25 v2.3 attacks, changes with the listing regenerated first |
| fid24-6 | `attack_matrix.json` : `corpus_replay_v2_4.note` | "body head", naming no file | "the type head String", naming `F2_string_sorry` and the mode it flips in |
| fid24-7 (a) | `SCIENCE_CHECK_v2.3.md` : 89–91 (found at 90–91) | "every run in `RUN_INDEX.tsv` carries a `files_the_subject_wrote` column so that the side effect is recorded beside the verdict" | scoped to the runs of the final build, with the rows that do record a written file named |
| fid24-7 (a) | `ANSWERS_v2.2_SECOND_OPINION.md` : 85–88 | the v2.2 runs "carry `not recorded`" | the rows that record a written file named: 375 and 376 under the v2.2 gate, 310 and 311 under the v2.3 gate |
| fid24-7 (b) | `ANSWERS_v2.2_SECOND_OPINION.md` : 207 | "gate build ee9822311c44ebcd", in no shipped file | `d6e8a00ff33ed454`, the build `RUN_INDEX.tsv` names |
| fid24-7 (b) | `ANSWERS_v2.3_SECOND_OPINION.md` : 304–305 (found at 305) | "The citation … is gone" | says that it was corrected at version 2.4.1, where this document had reported it a pass early |
| fid24-7 (c) | `README_LEAN.md` : the listing paragraph | the regenerate limit was claimed to be there and was not | a sentence on the limit, where a reader of that paragraph meets it |
| fid24-7 (c) | `ANSWERS_v2.3_SECOND_OPINION.md` : 293–295 | the claim as made | the claim with the date the README sentence went in |
| fid24-7 (d) | `ANSWERS_v2.3_SECOND_OPINION.md` : 296–298 | "The three places that said 'listed constant' now say that" | names the three places in `check.sh`, and says the three prose places were reworded at version 2.4.1 |
| fid24-7 (d) | `RED_TEAM_LEAN.md` : 1309, `ANSWERS_v2.2_SECOND_OPINION.md` : 37, `CHANGES_v2.2_to_v2.3.md` : 33 | "a listed constant of this module" | "a constant of this module that Lean does not call internal", with the derived constructors and recursors named |
| fid24-8 | `ANSWERS_v2.3_SECOND_OPINION.md` : 105–112 (found at 104–112) | the reviewer's section-local spelling "does not reproduce here", their file "purged … cannot be narrowed further" | the difference is the instance body: theirs is `fun _ => Move.det Move.sv`, which keeps `T10_det_table` true, so the spelling does reproduce; their file is named with its preserved path, and version 2.4 refuses it at 1g4 |
| fid24-8 | `attacks/ATTACKS.tsv` : 27 | "the packet's file differs from its one-line description in a way this rebuild cannot recover" | the body that differs, the reviewer's preserved path, and the 1g4 refusal |
| fid24-8 | `RED_TEAM_LEAN.md` : 1475–1476, `SCIENCE_CHECK_v2.4.1.md` : 87–88 (found at 88) | "their evidence directory had been purged" | "their own copies were not to hand at the time", with the preserved trees named |
| fid24-9, L4-NOTE-4 | `RUN_INDEX.tsv` : the `fail_lines` column | the v2.4 rows raw — log order, `[4.x.y]` prefixes, full banners, a trailing `FAILED.`, cut at 400 characters | every v2.4 row in the same form as the v2.3 rows — prefixes stripped, banners as `Lean <version>`, no summary line, sorted, no cap. The 236 corpus pairs now compare row by row: 236 of 236 identical |
| L4-NOTE-3, R-2 | `RUN_INDEX.tsv` : the four PATH rows | a `PATH=…` command that does not say how the listed toolchains were absent | each says that `ELAN_HOME` pointed at a directory with an empty `toolchains/` and that PATH carried only that release's bin |
| L4-NOTE-5 (g), R-2 | `RUN_INDEX.tsv` : 384 | command `./check.sh README_LEAN_typo.md` | `./check.sh TetrasemaphoreAlgebra.lean README_LEAN.mdx`, which is the run the recorded log comes from |
| R-2 | `RUN_INDEX.tsv` : the `path4341` row | mode "listing regenerated first" against a command without `--write-statements` | the command carries `--write-statements`, which is the run that was made |
| L4-NOTE-6 | `CHANGES_v2.3_to_v2.4.md` : 21 | reads as 3k replaced by 3l | "3k is kept, and section 3l added beside it" |
| L4-NOTE-10, fid24-13 | `attacks/README.md` : 28 | "The other thirty-four … compile without side effects" | `a15_full_chain` prints one forged footprint line and writes nothing; the remaining thirty-three have no side effect |
| L4-NOTE-12, fid24-15 | `README_LEAN.md` : 681 | `mktemp` "puts it under `$TMPDIR`" | Apple's `mktemp` ignores `$TMPDIR` and chooses a per-user directory; the GNU one honours it |
| L4-NOTE-14, fid24-17 | `README_LEAN.md` : 697–699 | "Four separate passes … and the fifth one did too" | "… and the fifth and sixth did too", with the reviewer's stop sentence after it |
| L4-NOTE-14, fid24-17 | `ANSWERS_v2.3_SECOND_OPINION.md` : 307–308 (found at 308) | the three PATH runs "are in the RED_TEAM table" | named in the paragraph after it, which is where they are |
| L4-NOTE-14, fid24-17 | `ANSWERS_v2.3_SECOND_OPINION.md` : 51 | "Under v2.3 it exits 0" | "Under v2.3, with the listing regenerated first, it exits 0 …; plain, it fails at section 5 and writes the file anyway" |
| L4-NOTE-16, R-8 | `attack_matrix.json` : `new_attacks_on_v2_2` A1–A5 and B1–B3 | a hash with no file and no reason | each says the file was built in an earlier pass and not kept, and where the run is |
| L4-NOTE-16, R-8 | `README_LEAN.md` : "What else is in this folder" | one generator named, the two check summaries unmentioned, no standalone `lean` command | both generators and both summaries named, and the standalone `lean TetrasemaphoreAlgebra.lean` run stated |
| fid24-18 | `README_LEAN.md` : 703 | "the DOI for this release", with no DOI anywhere in the folder | "the Zenodo record of this release, linked from the repository's `CITATION.cff`", so the folder does not wait on the deposit |
| R-3 | `RED_TEAM_LEAN.md` : 1482 | `DESYNC_EOF` as "a file that ends inside a raw string" | "a file that ends inside a plain string, opened after a character literal", which is what the generator writes |
| R-5 | `CHANGES_v2.3_to_v2.4.md` : 25, `ANSWERS_v2.3_SECOND_OPINION.md` : 322–323 (found at 323) | the one-toolchain OK line "pluralised" | the fallback branch is the one that was pluralised; the listed branch still reads "under all 1 listed toolchains", and changing it would change the gate's bytes |
| fid24-12 | `RED_TEAM_LEAN.md` : 1481–1489 | per-attack seconds that disagree with the index | "fails before elaboration" where that is the point, with a sentence saying the seconds are in `RUN_INDEX.tsv` |
| — | `README_LEAN.md` : after the `./check.sh` block | — | one sentence saying this folder is version 2.4.1 and the gate and proofs are byte-identical to the version 2.4 that was re-run |
| — | `SCIENCE_CHECK_v2.4.md` | — | renamed `SCIENCE_CHECK_v2.4.1.md`, with a section on what 2.4.1 changed and a hash table matching this folder |

## The four re-measured run hashes

The four rows the re-run could not reproduce were run again here, against the files as this folder ships
them — the same attack files, the same gate, the shipped README — one run per row:

| row | attack | mode | log sha256 (first 16), as recorded in 2.4 | as measured here |
|---|---|---|---|---|
| 318 | `ABBREV16` | plain | `afb6ba1cfa8934c0` | `933e3bd5c11e1e7f` |
| 320 | `ABBREVFALSE` | plain | `7007a482ec443887` | `82727dbbd8e57cfe` |
| 357 | `ABBREV16_regen` | listing regenerated first | `1a3127a5e336517e` | `74f7992822e1d06e` |
| 359 | `ABBREVFALSE_regen` | listing regenerated first | `3d032503d43ea5b4` | `71c21e625d46e2f1` |

Each measured hash equals the one the reviewer measured independently. The exit code, the failure lines,
the `3l` lines naming `SixteenInst` / `mySixteen` and `ThreeInst` / `myThree`, and the section-5 difference
were the same before and after; the one line that differed was the count of README names, which the
recorded logs gave as 117 and the shipped README gives as 116.

Fifteen more rows were re-run to recover their failure lines in full, the ones the 400-character cap had
cut. Every one of the fifteen reproduced its recorded log hash exactly, so only the four above moved.

## What is not changed, and why

* **The gate's bytes.** Two of the re-run's items would have changed `check.sh`: the singular branch of the
  OK line (R-5) and the comment at its header about a source-declared auxiliary name (note 8). Both are
  left alone, so that the re-run's verdicts hold for the file as it ships; both are written down here and
  in the texts instead.
* **`check.sh` 847's comment count** (fid24-5 (d)), for the same reason. The two prose places that carried
  that count are corrected.
* **The optional extra attack file** (fid24-8): no file was added after the stop.
* **The two `.DS_Store` files** (fid24-16): excluded from the release manifest, as before.
* **The notes that record no false statement**: 1 (the documented cost, measured on the reviewer's own
  honest variants), 2, 4 beyond the cap fix, 7 (the shape lists 1g4 and the audit use), 8 (the claim is
  true; the shipped runs stop earlier) and 11 stay notes, as ruled. Note 15 is the one of that group that
  did change a file: it is fid24-18, the README's Zenodo-record wording, in the table above.
