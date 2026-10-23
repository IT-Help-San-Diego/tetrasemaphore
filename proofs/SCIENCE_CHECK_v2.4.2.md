# Version 2.4.2 of the Lean folder — the last text pass before the release

Claude Science, 22 October 2026.

Version 2.4.2 is texts and indexes. It answers the second reviewer's read of version 2.4.1 against the
re-run packet's ids (`543dcd77881cdd36…`), which closed nine of the ten should-fix items of the re-run,
confirmed that the stop stands, and listed eight statements in the shipped texts that were false or that
disagreed with each other. Science ruled on those eight on 22 October 2026, and
`CHANGES_v2.4.1_to_v2.4.2.md` carries them one row each, with the file, the line, the old text and the new.

## What this version changed

A false pointer in `attack_matrix.json` (eight rows said the run was in `RUN_INDEX.tsv`, where it is not —
it is in `RED_TEAM_LEAN.md`); a sentence that had been put inside a Markdown table, so that two of the
twelve attack rows stopped rendering; four numbers that had gone stale (two seconds in the check of 2.4.1,
one "in one second" in the adversarial reading, and the three rows whose seconds moved with the version
2.4.1 re-runs, now declared); two run-index rows still carrying raw failure lines, one of them cut at 400
characters, re-emitted from fresh runs of the same two attacks under the same gate; a command column that
named a run that was not the one made; a paragraph about the toolchain-fallback runs brought into agreement
with the rows it describes, with one sentence on what does not reproduce there; an edit made at version
2.4.1 without a line declaring it, now declared and correctly attributed; and five smaller statements that
were false or that contradicted another file.

Two items were ruled no change: the generator strings behind `attacks/ATTACKS.tsv`, and "the DOI" where no
DOI number appears in the folder at all.

## The gate and the proofs did not change

`check.sh` (`ab6f55d3216e1f19…`), `TetrasemaphoreAlgebra.lean` (`f066faf6595d22e9…`), `STATEMENTS.md`
(`12b11a5e6651b386…`), `check_output.txt` (`df2f24dc4e5e3852…`), `lean-toolchain` (`302cd63c54178885…`) and
every attack file and generator under `attacks/` are byte-identical to the version 2.4 that the second
reviewer re-ran on 22 October 2026. Its verdicts therefore hold for this folder unchanged: no blocker, every
attack failing where it should, the honest set reproducing. No attack file was added in this pass or the one
before it.

## The honest run

A fresh copy of the eight shipping files in a directory holding nothing else: **exit 0**, under the three
listed toolchains in one run (4.33.0, 4.32.2 and 4.33.1, each compiling the file and auditing the compiled
module), output byte-identical to the committed `check_output.txt`, stderr 0 bytes, and the README name
check reading 116 names, all resolving. The same run from the extracted release archive gives the same
result.

## The hashes

The files as this folder ships them. `SCIENCE_CHECK_v2.4.1.md` carries the table for the folder version
2.4.1 shipped, which is what that document is the check of.

| file | bytes | sha256 (first 16) |
|---|---:|---|
| `TetrasemaphoreAlgebra.lean` | 61,638 | `f066faf6595d22e9` |
| `check.sh` | 102,794 | `ab6f55d3216e1f19` |
| `STATEMENTS.md` | 287,840 | `12b11a5e6651b386` |
| `check_output.txt` | 14,484 | `df2f24dc4e5e3852` |
| `README_LEAN.md` | 52,081 | `eb930febe5fec749` |
| `RED_TEAM_LEAN.md` | 110,747 | `89bde723a74f58db` |
| `lean-toolchain` | 25 | `302cd63c54178885` |
| `attack_matrix.json` | 417,388 | `0d24cf58b1438ee4` |
| `ANSWERS_v2.2_SECOND_OPINION.md` | 30,607 | `b7897400e7b9bbe4` |
| `ANSWERS_v2.3_SECOND_OPINION.md` | 25,086 | `8e0180103468f93d` |
| `CHANGES_v2.2_to_v2.3.md` | 19,783 | `b7d8c2031cd20aac` |
| `CHANGES_v2.3_to_v2.4.md` | 9,872 | `9d523a8e2bfa9291` |
| `CHANGES_v2.4_to_v2.4.1.md` | 13,224 | `62695593df4c3a14` |
| `CHANGES_v2.4.1_to_v2.4.2.md` | 9,570 | `5c438f85113eb693` |
| `SCIENCE_CHECK_v2.3.md` | 13,786 | `bfc7327d83519c30` |
| `SCIENCE_CHECK_v2.4.1.md` | 13,426 | `6b17554ff591947f` |
| `RUN_INDEX.tsv` | 220,637 | `6fb36722a6513bf2` |
| `attacks/README.md` | 3,569 | `3f9f453bb37a7928` |
| `attacks/ATTACKS.tsv` | 6,433 | `a165a7928217ce63` |
| `attacks/build_attacks.py` | 10,097 | `99fd88333c8885e0` |
| `attacks/build_attacks_v24.py` | 6,850 | `82d45ebb0b0e9ce9` |
| `SCIENCE_CHECK_v2.4.2.md` | — | this file, so its own hash is on the ledger rather than in it |
| `attacks/<38 directories>` | — | one `.lean` each, byte-identical to version 2.4, with its hash in `attacks/ATTACKS.tsv` |

## What a reader can check

The three steps are the ones version 2.4 states and this version does not change: compare the sha256 of
`TetrasemaphoreAlgebra.lean` against the Zenodo record of this release, linked from the repository's
`CITATION.cff`; run `./check.sh`; read `STATEMENTS.md`. The gate cannot do the third of those, and a green
light on a copy from anywhere else says only that a Lean file and a shell script in the same folder agree
with each other.

Anything found after this pass goes into the next version. This one is the last text pass before the files
are archived.

## One edit by Science after its review

Science changed one sentence of `README_LEAN.md` after reviewing this folder. The summary said that version 2.4.2 "corrects a further eight
items"; one of the eight needed no change, as ruled, so the sentence now says that seven are corrected and one needed no change. The edit adds
and removes no cited name (the README name check still reads 116), and the honest run on a fresh copy of the eight shipping files, made after
the edit, gives output byte-identical to `check_output.txt`. The hash table above carries the README as edited.
