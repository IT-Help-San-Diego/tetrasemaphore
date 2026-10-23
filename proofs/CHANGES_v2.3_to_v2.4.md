# What changed between version 2.3 and version 2.4 of the Lean folder

Claude Science, 22 October 2026. The sixth pass over the gate, answering the second opinion on version 2.3
(`TETRASEMAPHORE-DOORBELL-CLAUDE-SCIENCE-LEAN-V2.3-SECOND-OPINION.md`, sha256 `aed75362b5e20cc4…`). Every
item in that packet is answered one to one in `ANSWERS_v2.3_SECOND_OPINION.md`; this file is the list of
what moved.

**The Lean file did not change.** `TetrasemaphoreAlgebra.lean` is byte-identical to the file v2.2 and v2.3
shipped — sha256 `f066faf6595d22e9…`, 1503 lines, 118 theorems, 118 `#print axioms` lines, zero imports. No
theorem was added, removed or restated. Everything below is the gate, the listing's prose and the
bookkeeping.

## 1. The gate

| section | v2.3 | v2.4 |
|---|---|---|
| `scan()` | knew a line comment, a block comment and a double-quoted string | knows character literals (opened only where the previous character cannot end an identifier, so `g'` is a name) and raw strings (`r"`, `r#"`, hash-counted terminator, state carried across lines) |
| the scanner's end state | not recorded | written out, and a scan that does not end in open code fails before section 2, naming the line that left it open |
| source patterns | seven: 1a–1f and the refused-command pattern | eight: a new pattern refuses character literals and raw strings, which the honest file does not contain |
| generated-shape names | reported only by the audit, and only when the parent was missing | refused in source before elaboration (1g4), and the audit fails on an `aux`-classified constant whose name appears in the gate's own source-declaration lists (3j) |
| numeric-literal instances | section 3k reported a constant whose type head, as written, is `OfNat` | 3k is kept, and section 3l added beside it: 3l reads the head of every non-theorem constant's type and every definition's body, after unfolding reducible wrappers, and compares it against the set this file's own declarations produce |
| the tool probe (0c) | gave `comm` and `join` known inputs, took `cmp` and `diff` on trust | gives `cmp` and `diff` a known pair as well |
| the self-test | seven patterns and two scanner probes | eight patterns and six scanner probes, four of them new: a character literal and a raw string each have to leave the following line visible, a primed name has to not read as a literal, and the probe's scan has to end in open code |
| the per-toolchain line | `private declarations: 0` was a literal, and `OfNat instances declared` was the only head count | all four numbers are counted from the audit's rows: auxiliaries, names belonging to no declaration, private declarations, and heads outside this file's own set, with the number of heads read |
| the one-toolchain OK line | the fallback branch read "under the 1 toolchains that ran" | that branch pluralised; the listed branch still reads "under all 1 listed toolchains" where one toolchain is installed |

### The head rule, in full

The rule has two clauses, and both are needed. A head that is itself a declaration of the module being
audited — one of its own types, constructors, recursors or definitions — is accepted as such, because a
constant of this file cannot be an instance of a class from outside it. Every other head is compared
against the sets the honest file produces: thirteen heads in types
(`«no-constant-head»`, `Bool`, `Decidable`, `Decidable.rec`, `Int`, `List`, `Nat`, `PProd`, `Prod`, `Repr`,
`SizeOf`, `Std.Format`, counting the own-constant token) and seven in bodies (`«no-constant-head»`,
`«own-constant»`, `List.append`, `List.cons`, `Prod`, `Repr.mk`, `SizeOf.mk`). The sets are identical under
4.32.2, 4.33.0, 4.33.1 and 4.34.1. On the honest file the gate reads 360 heads and none is outside the set.

## 2. The listing

`STATEMENTS.md` is regenerated, and its theorems section is byte-identical to v2.2's and v2.3's — all 164
rows, 24,850 characters in 25,436 bytes, character for character. What changed is the third section's
introduction, which gained three things a reader was otherwise asked to take from a comment in the gate:

* what the `_private.Subject.0.` prefix is — Lean's encoding of a private name, with `Subject` the fixed
  module name the gate compiles the file under — and that the 121 rows carrying it are Lean's own private
  equation lemmas for matchers, the file itself declaring nothing private;
* what "parent" means in the `aux` classification: a constant of this module that Lean does not call
  internal, which includes the derived constructors and recursors, so a parent can be a name with no row of
  its own;
* the documented limit, in the place a reader meets it: ten rows of this section change under the
  `andF`/`orF` arm swap, and a reader who regenerates this listing from a swapped file rather than
  comparing against the committed one gets a green run and a listing that carries the swap.

## 3. `check_output.txt`

Regenerated, and the diff against v2.3's is four hunks, no more:

| line | v2.3 | v2.4 |
|---|---|---|
| the self-test line | "the seven source patterns … blanks a string literal's inside and does not blank a declaration behind a doc comment" | "the eight source patterns … and keeps a character literal and a raw string from hiding the line after them" |
| the audit line, three times | "names Lean calls internal: 345, each one an auxiliary of a listed declaration ; private declarations: 0 ; OfNat instances declared: 0" | "names Lean calls internal: 345 auxiliaries of a listed declaration, 0 belonging to none ; private declarations: 0 ; declaration heads outside this file's own set: 0 of 360 read" |
| the README name count | 114 names checked | 116, the two new ones being `LT` and `Neg`, the class names the README's new paragraph cites |

The file is 236 lines where v2.3's was 232, and the verdict, the 118 axiom lines, the footprint section and
the listing comparison are unchanged.

## 4. The documents

| file | change |
|---|---|
| `README_LEAN.md` | the self-test count is eight and the four new probes are described; the `OfNat` paragraph carries the head rule and what it does not cover; "the second half of `STATEMENTS.md`" is the definitions section; the temporary-directory paragraph says where the directory comes from; two new sections — what a green light says and does not say, and what else is in this folder |
| `RED_TEAM_LEAN.md` | a new section, "v2.4 — a sixth pass", with the three blockers, the rule, the thirteen attack files of this pass, in a table of twelve rows, the projection-class asymmetry, what the rule costs and the cases that are green by design; the four `—` cells of the v2.3 table carry their hashes; the three in-window PATH runs are named; two leftovers of replaced wording corrected |
| `ANSWERS_v2.2_SECOND_OPINION.md` | five counts and citations corrected, and the two sentences about the side-effect column scoped to the runs they are true of |
| `CHANGES_v2.2_to_v2.3.md` | five counts corrected, including the file count of `attacks/` and the column count of the index |
| `SCIENCE_CHECK_v2.3.md` | the duplicated phrase deleted, the arm-swap row count made one text with the other three places, the theorems-section size stated in characters and bytes. Two further changes went in undeclared and were put back at version 2.4.1: the section "One edit by Science after its review (22 October 2026)" had been dropped, and the README row of its hash table had been rebuilt from a pre-edit draft (05644d85e3c90dd2 / 47,074 instead of the 97d2a7572c05f57e / 46,071 that version 2.3 shipped) |
| `ANSWERS_v2.3_SECOND_OPINION.md` | new: the three blockers, the ten should-fix items and the fourteen notes, each answered with what reproduced and what changed |
| `CHANGES_v2.3_to_v2.4.md` | new: this file |
| `SCIENCE_CHECK_v2.4.md` | new: the hashes, the runs and what a reader can check. Renamed `SCIENCE_CHECK_v2.4.1.md` at version 2.4.1 |
| `attacks/README.md` | new: what each attack file is, and which of them run code when compiled |

## 5. The bookkeeping

| file | v2.3 | v2.4 |
|---|---|---|
| `RUN_INDEX.tsv` | twelve columns; the corpus rows labelled `plain`; two runs both named `M1_regen` | fourteen columns, the two new ones being `gate_sha16`, which ties every row to the build it ran under, and `command`; the corpus rows labelled `write-statements, v2 README`, with the three mode values defined in `SCIENCE_CHECK_v2.4.1.md` and in `attack_matrix.json` under `provenance.v2_4_runs` rather than in the file's own header, which is its fourteen column names; the rows named `M1a_regen` and `M1b_regen`, with the counterparts run that were missing; the harness rows carrying their command line |
| `attack_matrix.json` | ten rows without `file` or `sha256_16` | every row carries both, or says why there is no file (the PATH and README harness rows run the honest file under a changed environment) |
| the release manifest | two `.DS_Store` files staged | excluded |

## 6. What did not change

* The Lean file, its 118 theorems, their statements and their proofs.
* The theorems section of `STATEMENTS.md`, character for character.
* The verdict on every one of the 236 files in the v2.2 replay corpus; of the 25 v2.3 attacks one honest
  variant, `F2_string_sorry`, changes from pass to fail on the head rule when the listing is regenerated
  first (`SCIENCE_CHECK_v2.4.1.md`, The replay). The exit code and
  failure lines of every attack version 2.3 already caught, apart from five whose failure lines gained the
  new checks' lines: `K1d_proofN_name`, `N1_hidden_instance`, `N1b_false_row_hidden_instance` and
  `N1c_visible_instance` gain the head rule's, and `N1e_aux_named_instance` is refused in source by 1g4
  before it is elaborated at all.
* The three toolchains the gate runs, and the window the listing is byte-identical under.
