# Version 2.4.1 of the Lean folder — what was checked, and what a reader can check

Claude Science, 22 October 2026.

This is the sixth pass over `check.sh`, answering the second opinion on version 2.3
(`aed75362b5e20cc4…`, 388 lines) written by Claude Code on a different model family. The packet is
answered item by item in `ANSWERS_v2.3_SECOND_OPINION.md`; what moved is listed in
`CHANGES_v2.3_to_v2.4.md`; the adversarial reading is in `RED_TEAM_LEAN.md`.

## Version 2.4.1, and what it changed

The second reviewer re-ran its existing attacks against version 2.4 on 22 October 2026 and found no
blocker; with that its checking of the checker stopped. It did find ten should-fix items and twenty notes,
all of them in the prose and the run index, and version 2.4.1 is those corrections: the files are listed
one by one in `CHANGES_v2.4_to_v2.4.1.md`.

`check.sh` (`ab6f55d3216e1f19…`), `TetrasemaphoreAlgebra.lean` (`f066faf6595d22e9…`), `STATEMENTS.md`
(`12b11a5e6651b386…`) and `check_output.txt` (`df2f24dc4e5e3852…`) are byte-identical to the version 2.4
the reviewer re-ran, so every verdict of that re-run carries over to this folder unchanged. What moved is
text, the run index, and four log hashes in it that are now measured from the files as they ship.

**The short version.** The reviewer found three ways to leave the gate green: a character literal that
desynchronised the gate's source scanner, so a smuggled `#eval` was invisible and the attacker's code ran
during the gate's own run; an `OfNat` instance wrapped in an `abbrev`, which rebound the numeral `16` and
proved a count of five to be three; and a `Neg` instance nobody had thought to look for, which rebound
`-1`. Science ruled all three blockers on 22 October 2026. All three are fixed, and the fix for the second
and third is one rule rather than three class names. The Lean file did not change: it is byte-identical to
the one version 2.2 shipped, 118 theorems, and no statement or proof moved in this pass.

1. **The file is the same file.** `TetrasemaphoreAlgebra.lean` is `f066faf6595d22e9…` in v2.2, v2.3 and
   v2.4 — 1503 lines, 118 theorems, 118 `#print axioms` lines, zero imports.
2. **The theorems section of `STATEMENTS.md` is byte-identical** to v2.2's and v2.3's as well — all 164
   rows, 24,850 characters in 25,436 bytes — so every statement a reader has already read is character for
   character what it was. What changed in the listing is the third section's introduction, which now says
   what the `_private.Subject.0.` prefix is, what "parent" means in the `aux` classification, and the
   documented limit of regenerating.
3. **The honest file passes under all three listed toolchains**, and a fresh copy of the shipping files in
   an empty directory reproduces `check_output.txt` byte for byte.
4. **Every attack fails, each on a named check**, and none of the four files that write something when
   they are compiled writes anything under this gate.
5. **The replay agrees with the pass before it**: 236 of 236 corpus files reach the same verdict under
   v2.4 as under v2.3, and all 236 failure-line sets are identical.

## The hashes

These are the files as version 2.4.1 shipped them, which is what this document is the check of. Version
2.4.2 corrected further text and two rows of the run index; `SCIENCE_CHECK_v2.4.2.md` carries the table
for the folder as it now stands, and `CHANGES_v2.4.1_to_v2.4.2.md` lists what moved.

| file | bytes | sha256 (first 16) |
|---|---:|---|
| `TetrasemaphoreAlgebra.lean` | 61,638 | `f066faf6595d22e9` |
| `check.sh` | 102,794 | `ab6f55d3216e1f19` |
| `STATEMENTS.md` | 287,840 | `12b11a5e6651b386` |
| `check_output.txt` | 14,484 | `df2f24dc4e5e3852` |
| `README_LEAN.md` | 51,414 | `76cc123f8e2a322d` |
| `RED_TEAM_LEAN.md` | 110,191 | `29f6b8a0b087ed1b` |
| `lean-toolchain` | 25 | `302cd63c54178885` |
| `attack_matrix.json` | 416,469 | `881c83a9498f09d9` |
| `ANSWERS_v2.2_SECOND_OPINION.md` | 30,606 | `96411538a6e211b6` |
| `ANSWERS_v2.3_SECOND_OPINION.md` | 24,974 | `3024818754c63f30` |
| `CHANGES_v2.2_to_v2.3.md` | 19,783 | `b7d8c2031cd20aac` |
| `CHANGES_v2.3_to_v2.4.md` | 9,373 | `94dd97a4d0c0e186` |
| `CHANGES_v2.4_to_v2.4.1.md` | 13,097 | `c0c6b337e4ffd735` |
| `SCIENCE_CHECK_v2.3.md` | 13,786 | `bfc7327d83519c30` |
| `RUN_INDEX.tsv` | 220,865 | `6fca7cd9b92e0bfc` |
| `attacks/README.md` | 3,569 | `3f9f453bb37a7928` |
| `attacks/ATTACKS.tsv` | 6,433 | `a165a7928217ce63` |
| `attacks/build_attacks.py` | 10,097 | `99fd88333c8885e0` |
| `attacks/build_attacks_v24.py` | 6,850 | `82d45ebb0b0e9ce9` |
| `SCIENCE_CHECK_v2.4.1.md` | — | this file, so its own hash is on the ledger rather than in it |
| `attacks/<38 directories>` | — | one `.lean` each, with its hash in `attacks/ATTACKS.tsv` |

## Two edits by Science after its review (22 October 2026)

Science's review of this folder found two things and changed nothing else:

1. **`README_LEAN.md` printed two passages twice**, one copy straight after the other: the sentence saying that the gate stops before section 2, and
   the paragraph "The limit under all of it". The same two passages had been removed from version 2.3 for the same reason; this README was built from
   the copy before that edit. Science removed the second copy of each.
2. **`check.sh` said "version 2.3" in its first comment line.** It now says "version 2.4". Nothing else in the file changed, as `diff` against build
   `c5a8d8d6a952af4c` shows. The runs in `RUN_INDEX.tsv` name that build, because it is the one they ran under.

After both edits Science ran the gate on a fresh copy of the eight shipping files: exit 0 under the three listed toolchains, output byte-identical to
`check_output.txt` (`df2f24dc4e5e3852`). The table above lists the edited files.

## What a reader can check in five minutes

Compare the sha256 of `TetrasemaphoreAlgebra.lean` against the DOI record for this release; run
`./check.sh`; read `STATEMENTS.md`. The first says the file is the published one, the second says the
proofs are proofs, the third says what they are about. The gate cannot do the third for you, and a green
light on a copy from anywhere else says only that a Lean file and a shell script in the same folder agree
with each other.

## The runs

Every run of this pass is in `RUN_INDEX.tsv`, one row each, with the build of `check.sh` it ran under in
the `gate_sha16` column. The modes are three: `plain` is the gate run as a reader would run it;
`listing regenerated first` is `--write-statements` and then the gate, which is the path a maintainer
takes; `write-statements, v2 README` is how the corpus replay was recorded in the v2.2 pass and is kept
here so that the three replays compare. The gate builds are `8eddb30c49d75e26` for v2.2,
`d6e8a00ff33ed454` for v2.3 and `c5a8d8d6a952af4c` for v2.4 (the build every v2.4 run in `RUN_INDEX.tsv` ran under; the shipped
`check.sh`, `ab6f55d3216e1f19`, differs from it only in its version label: see the two edits below).

### The attacks of this pass

Thirteen files, each rebuilt here from the reviewer's description because their own copies were not to
hand at the time; they are kept in the reviewer's preserved trees, which their re-run of version 2.4 names
by path. `DESYNC_EVAL` rebuilt byte-identical to the reviewer's own file, and the other twelve differ. Under version 2.4 every one
of them fails, and the two that wrote a file under version 2.3 write nothing:

| attack | sha256 (first 16) | v2.3, listing regenerated | v2.4 | v2.4 wrote | caught by |
|---|---|---|---|---|---|
| `DESYNC_EVAL` | `2f05dbb2e1ea6d89` | **passes**, wrote `EVID_DESYNC.txt` | fails in 2 s | none | the character-literal pattern, the allowlist, and the stop before elaboration |
| `DESYNC_RAWSTRING` | `66a2e64cff7acaad` | **passes**, wrote `EVID_RAW.txt` | fails in 1 s | none | the same three |
| `DESYNC_EOF` | `84b28ac9093273a0` | fails | fails in 0 s | none | the scanner's end state |
| `ABBREV16` | `394f4265b65d9a7f` | **passes** | fails in 107 s | none | the head rule — the body of `SixteenInst` reduces to `OfNat` |
| `ABBREVFALSE` | `2a0a7218f1fa50fe` | **passes** | fails in 110 s | none | the head rule — the body of `ThreeInst` reduces to `OfNat` |
| `ABBREV16_AUX` | `679346bd4f734bee` | **passes** | fails in 6 s | none | the generated-shape pattern, in source |
| `ABBREVFALSE_AUX` | `a5d9ad3ad702a794` | **passes** | fails in 2 s | none | the generated-shape pattern, in source |
| `NEGFALSE` | `e3c7083d713059d7` | **passes** | fails in 3 s | none | the generated-shape pattern — the instance is named `Move.det._f` |
| `NEGFALSE_VISIBLE` | `696a370cca6327c5` | **passes** | fails in 95 s | none | the head rule — the type of `negIntVisible` reduces to `Neg` |
| `NEG_LOCAL_SECTION` | `9397021b1b684739` | **passes** | fails in 98 s | none | the head rule — the type of `negIntLocal` reduces to `Neg` |
| `AUXNAME_DEF` | `421628fb75a2408f` | **passes** | fails in 2 s | none | the generated-shape pattern, in source |
| `PRIVATE_DEF` | `f4f8e15bd0f18a22` | fails | fails in 101 s | none | the private-name check, with the count now beside it |
| `LTSWAP` | `479e787a4b37131f` | **passes** | fails in 90 s | none | the head rule — the type of `myLT` reduces to `LT` |

### The honest controls

| control | result |
|---|---|
| the honest file, the three listed toolchains (4.33.0, 4.32.2, 4.33.1) | exit 0; the recorded `check_output.txt`, `df2f24dc4e5e3852`, 236 lines |
| a fresh copy of the shipping files in an empty directory | exit 0 in 103 s; output byte-identical to `check_output.txt` |
| Lean 4.30.0-rc2 on PATH, none of the three listed present | exit 0 in 34 s; the listing it regenerates is byte-identical to the committed one |
| Lean 4.31.0 on PATH, none of the three listed present | exit 0 in 36 s; the listing it regenerates is byte-identical to the committed one |
| Lean 4.32.0 on PATH, none of the three listed present | exit 0 in 34 s; the listing it regenerates is byte-identical to the committed one |
| Lean 4.34.1 the same way | exit 0 in 37 s, with the paragraph saying 4.34 stops generating two of the definitions the listing carries; the listing it writes differs in those rows |
| a tamper only the `comm`-based checks catch, with `comm` absent from PATH | exit 1 in 1 s |
| the same tamper with `comm` present, as the control | exit 1 in 4 s |
| the README argument misspelled, on the honest file | exit 1 in 0 s |

### The replay

274 files under the v2.4 gate: the 236 of the v2.2 reviewer's corpus, the 25 attacks of the v2.3 pass and
the 13 of this one. 257 fail, 17 pass, and no file wrote anything. Of the 236 comparable with the previous
replay, **236 of 236 agree on the verdict and 236 of 236 have identical failure-line sets** — the rule
added in this pass changes no verdict on that corpus. The 17 that pass are the files that are supposed to:
honest probes, honest variants, files whose names mislead but whose statements are true, and the
documented limit of regenerating the listing.

One honest file does change verdict, and it is one of the 25 rather than one of the 236: a file that adds
`def noteText : String := …` passes version 2.3 and fails version 2.4, because `String` is outside the set
of declaration heads this file's own declarations produce. That is the cost of comparing against a set
drawn from one file, and it is recorded rather than hidden — the failure names the constant and the head.

## The rule that was added, and what it does not cover

Every constant of the compiled module that is not a theorem reports the head its type reduces to, and
every definition also the head its body reduces to, each read after reducible wrappers are unfolded. A head
that is itself a declaration of this module is accepted as such, because a constant of this file cannot be
an instance of a class from outside it. Every other head is compared against the set the honest file's own
declarations produce — thirteen heads in types, seven in bodies, identical under 4.32.2, 4.33.0, 4.33.1 and
4.34.1 — and anything outside it fails with the constant and the head named.

It compares classes rather than instances, so a second `Decidable` instance for a proposition this file
already decides is inside the set. It reads heads after `whnf`, so an irreducible wrapper reports the head
it has. And the set is this file's vocabulary, so an honest file that adds a constant of a shape this one
has no example of fails the check — which is the trade, stated plainly, for a rule that needs no list of
the classes an attacker might reach for.

Beside it, two refusals: character literals and raw strings in source, which this file does not contain
and which were the scanner's blind spot; and source-declared names of the shapes Lean generates, which
this file does not use either. Both are lists of the syntax their authors know, which is the standing limit
of the whole exercise.

## What is still open

The characterisation theorems for `Fml.holds` are declined for this release, because they would change the
count of 118 that every text here carries; the listing's equation lemmas say the same thing, and the limit
is now stated in three places. Instances of the classes this file does instantiate are not separated from
each other. And nothing here says the English in `README_LEAN.md` describes the same thing the Lean does —
that is what reading `STATEMENTS.md` is for.
