# Lean v2.3: the check behind this folder (21 October 2026)

**Folder:** `TETRASEMAPHORE-SCIENCE-LEAN-proofs-v2.3/`, built by Claude Science's Lean v2.3 sub-agent in answer to Claude Code's v2.2
second opinion (`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.2-SECOND-OPINION.md`, da2d6a94731565f0). Hashes of this folder are at the
foot of this file. Not final; it goes into the repository when Carey says final.

## What was checked, from a fresh copy

1. **The honest file passes** under Lean 4.32.2, 4.33.0 and 4.33.1, each named by path, with no `sorry`, no added axiom, no declaration
   hidden from the listing under an internal name, no `OfNat` instance of its own, 671 constants audited, 642 re-added through the
   kernel with 0 rejected, and 118 printed axiom lines agreeing with the compiled module. That run is `check_output.txt`.
2. **Nothing was weakened, and nothing was added.** `TetrasemaphoreAlgebra.lean` is byte-identical to v2.2 (f066faf6595d22e9): the same
   1503 lines, 118 theorems, 118 `#print axioms` lines, zero imports. The theorems half of `STATEMENTS.md` is byte-identical to v2.2's
   as well — all 164 rows, 24,850 characters in 25,436 bytes — so every statement a reader has already read is character for character what it was. The
   definitions half differs in its three-line introduction only; its 135 rows are unchanged. What is new is a third section, the 345
   constants Lean generates underneath those definitions, and a header that says what a row does and does not carry.
3. **The blocker is answered twice over and the listing a third time.** A name Lean calls internal that belongs to no listed
   declaration — `_i`, `proof_1` — is reported by section 3j; an `OfNat` instance declared by the module is reported by section 3k,
   which is what catches the companion attack after a listing has been regenerated; and either one is a row in the third section of the
   listing. On the honest file: 345 names Lean calls internal, every one an auxiliary of a listed declaration, 0 private, 0 `OfNat`
   instances, identical under all three toolchains.
4. **The attacks, rebuilt and re-run.** The packet's evidence directory was purged before this lane started, so every attack was rebuilt
   from the packet's one-line description by `attacks/build_attacks.py` and run against v2.2 and v2.3 in directories of their own. Three
   came out byte-identical to the hashes the packet records for them (3f467c422bea4148, 16b0a1a016895688, 7c01faa6f2a1a45f). The table
   below is every run; `RUN_INDEX.tsv` carries the exit code, the seconds and the log hash for each.
5. **The corpus, replayed.** The 236 adversarial and tamper files of `attack_matrix.json` were re-run against v2.3, each with the v2
   README as its second argument and `--write-statements`, which is how the v2.2 matrix was recorded. All 236 were present on disk with
   the hashes the matrix states.

## The runs

Every attack below was run under both gates where the file applies, each run in a directory of its own, plus the honest controls. Every attack file is
in `attacks/`, with its sha256 prefix in `attacks/ATTACKS.tsv`; every run is in `RUN_INDEX.tsv` with its exit code, its duration and the
sha256 prefix of the gate's output.

| run | gate v2.2 | gate v2.3 | what v2.3 catches it with |
|---|---|---|---|
| the honest file, unmodified | **passes** | **passes** | passes |
| blocker 2.1: hidden `instance _i : OfNat Nat 16`, `T8_sixteen` by `rfl` | **passes** | fails | listing differs; OfNat instance declared; internal/private name |
| blocker 2.1 widened: the same under the name `proof_1` | **passes** | fails | listing differs; OfNat instance declared; internal/private name |
| blocker 2.1 companion: hidden `_k` proving a count of 3 where it is 5 | fails | fails | listing differs; OfNat instance declared; internal/private name |
| the same, with the listing regenerated (v2.2's green path) | **passes** | fails | OfNat instance declared; internal/private name |
| control: the same instance under the visible name `inst16vis` | fails | fails | listing differs; OfNat instance declared |
| written here: the same instance named `Move.act._f`, which the classification calls an auxiliary | **passes** | fails | listing differs; OfNat instance declared |
| 3.1: `open Nat in #eval …` writing a file during the gate | **passes** | fails | refused command on a line |
| written here: the same IO from an `#eval` that is only indented | **passes** | fails | refused command on a line |
| 3.4: `@[inline, extern "lean_nat_add"]` on an already-listed definition | **passes** | fails | unsafe/extern in source |
| 3.4 variant: the same attribute on its own line | fails | fails | unsafe/extern in source; command allowlist |
| 3.5: the `andF`/`orF` arms of `Fml.holds` swapped (the packet's file) | **passes** | fails | listing differs |
| the same, with the listing regenerated | **passes** | **passes** | passes |
| 3.5 variant: the right-hand sides swapped, arm order left alone | fails | fails | listing differs |
| 3.2: honest Lean with banned words inside a string literal | fails | **passes** | passes |
| the honest variant that has to pass: banned words in a doc comment, a namespaced extra theorem | **passes** | **passes** | passes |
| 3.3: a `#print axioms` line replaced by one naming a core lemma | fails | fails | #print axioms names a non-theorem; theorem with no #print axioms line |
| 3.3: the same tamper with the full PATH | fails | fails | #print axioms names a non-theorem; theorem with no #print axioms line |
| 3.3: the same tamper with `comm` removed from PATH | **passes** | fails | missing tool |
| 3.8: the honest file under a PATH fallback resolving to Lean 4.34.1 | fails | **passes** | passes |
| 3.12: the honest file with the README argument misspelled | **passes** | fails | no such README |
| section 5 row 2.2, untested until now: `@[simp]` on the line above `axiom` | fails | fails | axiom/opaque in source; command allowlist |
| section 5 row 2.4, not re-tested since v2.1: `#exit` | fails | fails | refused command on a line; command allowlist |
| section 5 row 3.1, untested until now: `set_option` split across a line break | fails | fails | set_option in source; command allowlist |
| v2.1 (a) rebuilt: `#guard_msgs(drop info)` swallowing a `#print axioms` line | fails | fails | refused command on a line; command allowlist |
| v2.1 (c, g) rebuilt: `decide +native` behind a macro alias | fails | fails | refused command on a line; command allowlist |
| v2.1 (f) rebuilt: `@«sorryAx»` | fails | fails | sorry in source |
| v2.1 (g) rebuilt: a `syntax` + `macro_rules` command standing in for `#print axioms` | fails | fails | refused command on a line; command allowlist; theorem with no #print axioms line |
| v2.1 (h) rebuilt: `@[ extern "…"] opaque` | fails | fails | unsafe/extern in source; axiom/opaque in source; command allowlist |
| v2.1 (c, e, g) rebuilt: macro-hidden `decide +native` plus a forged footprint | fails | fails | refused command on a line; command allowlist |
| v2.1 (f) rebuilt: `sorry` through a macro alias | fails | fails | sorry in source; refused command on a line; command allowlist |
| v2.1 (h) rebuilt: `namespace Lean` declaring `collectAxioms` | fails | fails | listing differs; core namespace |
| note 7: the one corpus file of 29 KB or more that had no matrix row | — | fails | refused command on a line; command allowlist; theorem with no #print axioms line |

**The corpus replay.** 236 of the 236 rows were re-run against v2.3's second build; 236 came out with the verdict
the matrix records for v2.2 and 0 changed.

**The FAIL lines.** 15 of the 236 rows report the same set of FAIL lines as the v2.2 matrix records and 221 report a different set, with no verdict changed. The reason is the second build's stop: a file the source checks refuse is no longer elaborated, so 214 rows gain `the file was not elaborated` and lose the findings of sections 2 to 7 (143 lose the axiom walk, 94 the axiom-or-opaque-in-module line, 87 the Prop-proved-by-a-non-theorem line, 61 the printed-versus-audited footprint), and 73 gain the line that refuses a command anywhere on a line of code. `attack_matrix.json` carries the full breakdown under `corpus_replay_v2_3`.

## Science's ruling on item 3.5

Ruled 22 October 2026, accepting the reasoning in `ANSWERS_v2.2_SECOND_OPINION.md`: a should-fix rather than a blocker, fixed for the
packet's spelling of the attack by the third section of the listing. With the listing regenerated the swap stays visible in 10 rows of the listing (11 lines on each side, 22 counting both sides of the diff), all in the third section: `Fml.holds.eq_4` and `eq_5`, the type and body of `Fml.holds.match_1`, its six private equation lemmas and its splitter — a documented limit for a reader of
`STATEMENTS.md` rather than a hole in the gate. The characterisation theorems that would break the
proof outright are declined for this release, to keep the count of 118 stable across every text that quotes it, and are logged as a
future hardening option.

## What the second build changed

Science's check of the first v2.3 build found that the gate refused both `#eval` attacks in section 1 and then elaborated the file
anyway, once per toolchain, so each attack still wrote its evidence file while the gate was running: the verdict was right and the code
ran. The second build stops before section 2 whenever a source check has failed and says that the file was not elaborated. Both attacks
now fail in about two seconds with nothing written, which the `files_the_subject_wrote` column of `RUN_INDEX.tsv` records for the runs of
the final build; the runs where the IO did fire are in the index too, with the file each wrote. The honest path is unchanged: byte-identical to `check_output.txt`.

## Limits of this check

- The packet's own evidence files were unreachable (`/private/tmp` is purged), so no run here compares against their logs. The
  comparison is with what the packet *says* each attack does, plus three files that came out hash-identical.
- The replay ran under two builds of v2.3's `check.sh` that differ in one line: the list of README words exempted from the name check.
  The v2 README used by the replay cites none of the added words, so that line cannot change a corpus verdict; a sample was re-run under
  the final build to confirm it.
- The S3/T6 item, stated the right way round this time: what the v2 and v2.1 packets asked for is a theorem that the table-only language
  does **not** separate σᵥ from C₂ — the `swapVC` analogue of `S3_fml_swapVH` — or a softened sentence. The sentence was softened in
  v2.2 and stands: the README says the file proves that pair of relabellings and not a general interchangeability, and
  `T6_three_interchangeable` is what it names. The theorem itself is still not proved.
- LICENSE, CITATION.cff, .zenodo.json and README.md are still absent, by the agreement recorded in the v2 and v2.1 answers: they go in
  at release, with the licence decided then.
- A constant hidden under a name that is both a shape Lean generates and the child of a listed declaration (`Move.act._f`) is classified
  as an auxiliary and is not reported by 3j. It is a row in the third section of the listing, and if it is an `OfNat` instance 3k names
  it. The gate's own header says so.
- Under a toolchain outside the window the listing was written in, rows for definitions Lean generates are not compared. Lean 4.34.1 is
  outside it.

## One edit by Science after its review (22 October 2026)

Science's review of the second build found two passages in `README_LEAN.md` printed twice, one copy straight after the other: the sentence
saying that the gate stops before section 2, and the paragraph "The limit under all of it". Science removed the second copy of each and
changed nothing else. The honest run's output is unchanged: exit 0 under the three listed toolchains, byte-identical to `check_output.txt`
(2dbf34d60d59b9c1). The README row in the table below is the edited file.

## The files

sha256, first 16 hex digits, from this folder. `SCIENCE_CHECK_v2.3.md` is this file and is not in its own table.

| file | sha256_16 | bytes |
|---|---|---|
| `TetrasemaphoreAlgebra.lean` | f066faf6595d22e9 | 61,638 |
| `check.sh` | d6e8a00ff33ed454 | 83,188 |
| `STATEMENTS.md` | f08fda83857f7d4c | 286,908 |
| `check_output.txt` | 2dbf34d60d59b9c1 | 14,249 |
| `README_LEAN.md` | 97d2a7572c05f57e | 46,071 |
| `RED_TEAM_LEAN.md` | e358290b76673d8c | 96,043 |
| `attack_matrix.json` | 1caade181946f246 | 373,220 |
| `lean-toolchain` | 302cd63c54178885 | 25 |
| `ANSWERS_v2.2_SECOND_OPINION.md` | 2c9ed88cc1dd1221 | 29,664 |
| `CHANGES_v2.2_to_v2.3.md` | 7be22e1ff807af45 | 19,447 |
| `RUN_INDEX.tsv` | a98928aaf9e1b9ee | 92,825 |
| `attacks/ATTACKS.tsv` | 9e9bd43b4e59fdd4 | 3,853 |
| `attacks/build_attacks.py` | 99fd88333c8885e0 | 10,097 |

v2.2's nine, for comparison: TetrasemaphoreAlgebra.lean f066faf6595d22e9 (unchanged here), check.sh 8eddb30c49d75e26,
STATEMENTS.md 3d5f7469422232a8, check_output.txt 5bbe6fb27678d396, README_LEAN.md 66deb27923146108, RED_TEAM_LEAN.md
04eb7a1f15aa50fb, attack_matrix.json 05fd1c8fcd282093, lean-toolchain 302cd63c54178885 (unchanged here), SCIENCE_CHECK_v2.2.md
64bebd7705b3477a.

`attacks/` holds the 25 rebuilt attack files, one directory each, with `ATTACKS.tsv` giving every file's sha256 prefix and what it
attempts, and `build_attacks.py`, which writes all 25 from the honest source — every file in `attacks/` was checked against what the
generator produces. `RUN_INDEX.tsv` holds every gate run behind the table above: group, gate, run, the subject file's hash, the
toolchains that ran, the exit code, the seconds and the hash of the gate's output.
