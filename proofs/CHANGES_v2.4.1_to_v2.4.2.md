# What changed between version 2.4.1 and version 2.4.2 of the Lean folder

Claude Science, 22 October 2026. Texts and indexes only, from the second reviewer's read of version 2.4.1
against the re-run packet's ids (`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.4.1-READ.md`, sha256
`543dcd77881cdd36…`), ruled item by item by Science on 22 October 2026. That read closed nine of the ten
should-fix items of the re-run and confirmed the stop: it ran no gate and no attack. The eight items of its
section 3 are the corrections below.

**The gate, the proofs and the attack files did not change.** `check.sh` (`ab6f55d3216e1f19…`),
`TetrasemaphoreAlgebra.lean` (`f066faf6595d22e9…`), `STATEMENTS.md` (`12b11a5e6651b386…`),
`check_output.txt` (`df2f24dc4e5e3852…`), `lean-toolchain` (`302cd63c54178885…`) and every attack file and
generator under `attacks/` are byte-identical to the version 2.4 the reviewer re-ran, so that re-run's
verdicts hold for this folder. No attack was added, and no check behaves differently.

## The corrections, one row per item

Line numbers are the read's, against the version 2.4.1 files. Where one pointed a line off, the passage was
found by its words; those rows say where it was.

| item | file : line | was | is |
|---|---|---|---|
| 1 — fid24-5 (a) | `CHANGES_v2.3_to_v2.4.md` : 85 | "the corpus rows labelled `write-statements, v2 README`; a mode legend in the header" — the file's header is its fourteen column names | the three mode values "defined in `SCIENCE_CHECK_v2.4.1.md` and in `attack_matrix.json` under `provenance.v2_4_runs` rather than in the file's own header", which is where ask 5 asked the sentence to point |
| 2 — the matrix pointer | `attack_matrix.json` : the eight `A1`–`A5` and `B1`–`B3` rows | `no_file_because` ended "and RUN_INDEX.tsv carries the run", which is false: none of the eight names or hashes is in that file | ends "its verdict is recorded in RED_TEAM_LEAN.md under \"Attacks written against v2.2\", which gives the verdicts of that round without log hashes" |
| 2 — the eight files | `README_LEAN.md` : 737–738 | "A copy holding only the eight files named at the top of this document passes on its own" — no list of eight is named at the top | the eight are named in the sentence: `TetrasemaphoreAlgebra.lean`, `check.sh`, `STATEMENTS.md`, `check_output.txt`, `README_LEAN.md`, `RED_TEAM_LEAN.md`, `lean-toolchain` and `attack_matrix.json` |
| 3 — the split table | `RED_TEAM_LEAN.md` : 1493–1494 | the seconds sentence sat inside the v2.4 attack table, so the last two rows (`PRIVATE_DEF`, `LTSWAP`) fell out of it and ten rows rendered | the sentence moved below the table's last row, so all twelve render |
| 3 — the seconds in prose | `RED_TEAM_LEAN.md` : 1470 | the generated-shape attacks "are caught in the source, in one second" | "in a few seconds — 6, 2 and 2 under the plain runs the index records" |
| 3 — the re-measured seconds | `SCIENCE_CHECK_v2.4.1.md` : 113–114 | `ABBREV16` "fails in 99 s" and `ABBREVFALSE` "fails in 100 s" | 107 s and 110 s, the seconds of index rows 318 and 320 as re-measured at version 2.4.1 |
| 3 — the undeclared seconds | `RUN_INDEX.tsv` : 318, 320, 357 | version 2.4.1 replaced these rows' log hashes and declared that, and their `seconds` moved with the re-runs — 99 → 107, 100 → 110, 195 → 191 — without a line saying so | declared here: the three rows' seconds are those of the version 2.4.1 re-runs, measured on a machine running several copies of the gate at once |
| 4 — two raw rows | `RUN_INDEX.tsv` : 309, 317 | `DESYNC_EOF` and `PRIVATE_DEF` under the v2.3 gate still carried raw failure lines, 309 cut at exactly 400 characters | both re-run under the v2.3 gate (`d6e8a00ff33ed454`) and re-emitted in the v2.3 form with no cap: 309 is 302 characters, 317 is 55. Both re-runs reproduced the recorded log hash exactly — `3fb2e8bd60822454` and `62289c2c5139f54b` — so no hash moved |
| 4 — a command | `RUN_INDEX.tsv` : 302, `attack_matrix.json` harness entry | command `./check.sh README_LEAN_typo.md`, beside a log that says "no such README: README_LEAN.mdx" | `./check.sh TetrasemaphoreAlgebra.lean README_LEAN.mdx`, the run the recorded log comes from, as row 384 was corrected at version 2.4.1 |
| 5 — the PATH paragraph | `RED_TEAM_LEAN.md` : 1345–1346 (found at 1346) | "each put on PATH as the only `lean` and the gate's explicit-path list pointed at it", which contradicts the rows | the rows' own recipe: `ELAN_HOME` at a directory whose `toolchains/` is empty, so that none of the three listed releases is present and the gate falls back to the PATH entry |
| 5 — the four logs | `RED_TEAM_LEAN.md` : after 1346 | nothing said that the four logs do not ship or that their hashes did not reproduce | one sentence: the four logs do not ship, and the second reviewer's run of the same setup measured `9fe9ed7d5dde2c7b` where the 4.34.1 row records `d7742a8245c7fc79`; what did reproduce is the exit code, the byte-identical regenerated listing and the drift text |
| 6 — an undeclared edit | `ANSWERS_v2.3_SECOND_OPINION.md` : 224–226 | rewritten at version 2.4.1 with no row naming it, and attributing "for the runs of the final build" to `ANSWERS_v2.2_SECOND_OPINION.md` | declared in this table, and the phrase attributed to `SCIENCE_CHECK_v2.3.md`, where it stands; `ANSWERS_v2.2_SECOND_OPINION.md` is credited with what it does say, the index rows |
| 6 — a file's name | `CHANGES_v2.3_to_v2.4.md` : 78 | "`SCIENCE_CHECK_v2.4.1.md` \| new" at version 2.4, a name that file did not have then | "`SCIENCE_CHECK_v2.4.md` \| new … Renamed `SCIENCE_CHECK_v2.4.1.md` at version 2.4.1" |
| 7 — L4-NOTE-5 (h) | — | no disposition was recorded for it | no change to any file, ruled by Science on 22 October 2026: no shipped text claims the `attacks/ATTACKS.tsv` cells are generator output, and `attacks/build_attacks_v24.py` is a frozen attack-folder file |
| 8 — a purged claim | `ANSWERS_v2.3_SECOND_OPINION.md` : 49 | "The packet's evidence had been purged with `/private/tmp`" | "The packet's own copies were not to hand at the time — they are kept in the reviewer's preserved trees, which its re-run of version 2.4 names by path" |
| 8 — a broken sentence | `ANSWERS_v2.2_SECOND_OPINION.md` : 144 (found at 146) | the sentence ended "… and its splitter" with no full stop, after the garbled fragment was deleted at version 2.4.1 | the sentence ends "… and its splitter." |
| 8 — a note listed twice over | `CHANGES_v2.4_to_v2.4.1.md` : 99–100 | note 15 listed among the notes that stayed notes, while row 61 of the same table changes the README for it | note 15 named as the one of that group that did change a file, with the row that did it |
| 8 — an over-wide claim | `CHANGES_v2.3_to_v2.4.md` : 95–96 (found at 96) | "the exit code and failure lines of every attack version 2.3 already caught" did not change | scoped: five changed — `K1d_proofN_name`, `N1_hidden_instance`, `N1b_false_row_hidden_instance` and `N1c_visible_instance` gain the head rule's lines, and `N1e_aux_named_instance` is refused in source by 1g4 before elaboration |
| 8 — two files disagreeing | `README_LEAN.md` : 743 against `attacks/README.md` : 28 | "each such file writes one small text file in the directory it is compiled in and nothing else", where `attacks/README.md` says a15 writes nothing | the README now says five files run code: four write one small text file each, and the fifth prints one forged line of the gate's own output and writes nothing. `attacks/README.md` was the one that was right — a15's own line is `#eval IO.println`, checked in the file |
| — | `README_LEAN.md` : 48–51 | "This folder is version 2.4.1 …" | version 2.4.2, with what each pass changed and both change logs and both check summaries named |
| — | `README_LEAN.md` : the folder inventory | two check summaries named | three, the new one among them |
| — | `SCIENCE_CHECK_v2.4.1.md` : 44 | the hash table stood without saying which folder it is of | one sentence: it is the version 2.4.1 folder's, and `SCIENCE_CHECK_v2.4.2.md` carries this folder's |
| — | `SCIENCE_CHECK_v2.4.2.md` | — | new: what 2.4.2 changed, the byte-identity, the honest run and a hash table matching this folder |
| — | `CHANGES_v2.4.1_to_v2.4.2.md` | — | new: this file |

## What is not changed, and why

* **`check.sh`**, including its comment at 131–132 that reads as 3l replacing 3k (the read's item 8): the
  file is frozen for this release, so that the re-run's verdicts hold, and the prose correction stands in
  `CHANGES_v2.3_to_v2.4.md` instead.
* **"the DOI"** at `SCIENCE_CHECK_v2.4.1.md` 85 and `RED_TEAM_LEAN.md` 1552, as ruled: no DOI number
  appears anywhere in the folder, which is what fid24-18 asked for.
* **`attacks/ATTACKS.tsv` against the generators' strings** (item 7), for the reason in the table above.
* **`RUN_INDEX.tsv` row 295**, the version 2.2 harness run of the misspelled README, which carries the same
  command text that rows 302 and 384 carried. It was not among the items ruled on, and its log
  (`de3102e6c91e1990`, exit 0) is not one this pass re-ran, so which command produced it is not something
  this folder can show. It is recorded here for the next version.
* **The seconds of index rows 309 and 317**: the re-runs took 122 s and 170 s where the rows record 133 s
  and 194 s. The rows keep the recorded figures, since the logs are byte-identical and the difference is
  machine load rather than anything the run did.
