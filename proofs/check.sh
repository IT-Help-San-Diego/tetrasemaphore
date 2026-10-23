#!/usr/bin/env bash
# Gate for TetrasemaphoreAlgebra.lean — version 2.4
#
# WHY THIS EXISTS: `sorry` makes any proposition compile, including a false one,
# and Lean reports it as a warning — which is to say, with exit code 0.  A green
# build is therefore not by itself evidence that anything was proved.
#
# WHAT CHANGED IN 2.1.  Version 2 read the axiom footprint out of the text Lean
# printed while elaborating the file, and decided what the file contained by
# running `grep` over the source.  Both of those are things the file itself can
# write.  So 2.1 stopped asking the file what it is: a top-level command
# allowlist, a scanner that blanks comments and string literals before any
# regex runs, and an axiom footprint read from the compiled module by a wrapper
# this script writes.
#
# WHAT CHANGED IN 2.2.  An independent reviewer replayed a corpus of adversarial
# files against 2.1 and listed what 2.1 still left open.  This version closes
# that list:
#
#   * it refuses to run under `sh`, or under bash in POSIX mode.  Version 2's
#     gate lost two of its checks that way and still exited 0; testing
#     `BASH_VERSION` alone does not catch it, because POSIX-mode bash sets it.
#   * it runs every toolchain on its list that is installed, falls back to
#     whatever `lean` is on PATH when none of them is, prints which ones ran,
#     and says "all three" only when all three ran.  A machine with no Lean
#     fails rather than passing quietly.
#   * the audit of the compiled module now reads EVERY constant — definitions,
#     abbreviations, instances, opaques, constructors — and not only the
#     theorems.  Version 2.1 would have passed `abbrev ZA : False := by admit`,
#     because an abbreviation is not a theorem.  Axiom names are compared
#     exactly against propext, Classical.choice and Quot.sound.
#   * the imports are read from the compiled module header, where the source
#     text cannot reach them: every one has to be `Init`.
#   * every declaration is re-added to a fresh Init-only environment through
#     `Kernel.Environment.addDecl`, the kernel's own entry point, which has no
#     parameter for switching the check off.  A build made under
#     `debug.skipKernelTC` is therefore re-checked here from scratch.
#   * the audit runs with module initializers off and environment extensions
#     not loaded, so no `initialize` block, `@[init]` function or user
#     delaborator runs inside it.
#   * the gate writes STATEMENTS.md — every theorem's elaborated statement
#     beside its axioms — and fails if the listing it regenerates differs from
#     the committed one.  The gate checks how the proofs were made; that file
#     is where a reader checks what they say.
#
# WHAT CHANGED IN 2.3.  A second independent reviewer attacked 2.2 and found one
# way through it and a list of narrower ones.  The way through: a declaration
# whose name Lean's `Name.isInternalDetail` calls internal — `_i`, and also the
# innocent-looking `proof_1` — was audited but listed nowhere, so
# `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` rebound the numeral in
# `allSubs.length = 16` and the gate stayed green with the committed listing
# byte-identical.  This version:
#
#   * classifies every constant of the compiled module into named, private, aux
#     or internal.  `aux` is a name Lean generates for a declaration the listing
#     shows: its parent is a constant of the module that Lean does not call
#     internal — which includes the constructors and recursors Lean derives,
#     so a parent can be a name with no row of its own — and every component
#     after that parent is a shape Lean's own machinery writes.  Anything else
#     Lean calls internal is a name an author wrote, and section 3j reports it,
#     whatever the name is — a rule keyed on the leading underscore would miss
#     `proof_1`.
#   * reports any `OfNat` instance the module declares.  A numeral prints as
#     itself however it was bound, so it is the one thing a reader cannot check
#     by reading the listing.
#   * carries those generated auxiliaries in a third section of STATEMENTS.md,
#     with the matchers and equation lemmas that say which arm of a definition
#     belongs to which constructor.  Swapping the `andF` and `orF` arms of
#     `Fml.holds` moved nothing in 2.2's listing; it moves `Fml.holds.eq_4` and
#     `Fml.holds.eq_5` here.
#   * refuses `#eval`, `run_cmd`, `macro`, `syntax`, `notation`, `initialize`,
#     `attribute`, `export` and every other `#`-command anywhere on a line of
#     code, not only at the start of one.  2.2 reduced each line to its first
#     word, so `open Nat in #eval …` ran arbitrary IO during the gate, and so
#     did an indented `#eval`, which Lean accepts as a top-level command.
#   * blanks the inside of string literals as well as comments, so an honest
#     `def note : String := "… sorry …"` is no longer refused.
#   * checks every external program it uses before it uses any of them, and
#     gives `comm` and `join` a pair of files with a known answer.  Without
#     `comm` on PATH, three of 2.2's checks came back empty and read as clean.
#   * matches `extern` anywhere in an attribute group, not only as the first
#     attribute: `@[inline, extern "lean_nat_add"]` went past 2.2.
#   * fails when the README it was given does not exist.  With a misspelled
#     path, 2.2 checked zero names and printed `all resolve: yes`.
#   * writes the elaboration and audit output to files instead of piping a
#     shell variable into `grep -q`, where the pipeline could die of SIGPIPE
#     and, under `pipefail`, read as a failed check.
#   * prints the toolchain path relative to the elan root, so the recorded
#     output carries no username.
#   * says `toolchain drift` rather than `tampering` when the only difference
#     in the listing is in rows for definitions Lean generates and the toolchain
#     is one this gate does not list.  Lean 4.34 stops generating two of them,
#     and 2.2 failed the honest file with the tampering message.
#   * stops before section 2 when any source check has failed, and says that the
#     file was not elaborated.  Elaborating a Lean file runs code the file
#     contains, so a gate that refuses a line and then elaborates the file has
#     got the verdict right and run the code; the first build of 2.3 did exactly
#     that with a smuggled `#eval`.
#
# It still fails on: `sorry` or `sorryAx` in a proof position; Lean's own
# "declaration uses `sorry`" warning; `native_decide` and the `+native`
# spellings; any `axiom` or `opaque` declaration; `unsafe` / `implemented_by` /
# `partial`; `extern` or `implemented_by` anywhere in an attribute group; any
# `import`; any `set_option`; any command outside the allowlist at the start of
# a line; any of the commands listed above anywhere on a line; and any theorem
# without its own `#print axioms` line.  The source checks also run over a copy
# of the file with its line breaks collapsed, so splitting a keyword from its
# argument across two lines does not hide it.
#
# WHAT IT DOES NOT DO.  It checks how a proof was made.  It cannot tell you that
# a theorem says what its name says, or that the English around it describes the
# same thing.  Only reading the statements does that; STATEMENTS.md,
# README_LEAN.md and RED_TEAM_LEAN.md are that reading.
#
# WHAT CHANGED IN 2.4.  A second reviewer attacked 2.3 and found three ways to
# reach a green verdict, after the gate's own regenerate-and-commit step, on a
# file whose public statements do not mean what they read.  All three are the
# same shape: something the gate reads is not what Lean reads.
#
#   * a character literal holding a quotation mark desynced the source scanner,
#     which then blanked every line to the next quotation mark — a smuggled
#     `#eval` among them — so the file was elaborated and its IO ran during the
#     gate.  The scanner reads character literals and raw strings now; a file it
#     reaches the end of while still inside a string, a raw string or a block
#     comment is refused before anything is elaborated; and both constructs are
#     refused outright (1g3), because this file uses neither.
#   * an `OfNat` instance behind a one-line `abbrev` answered section 3k's head
#     test with the abbrev's name, so a numeral was rebound and a count of five
#     was proved to be three.  The audit now reports the head a type reduces to,
#     not the head it is written with.
#   * a `Neg` instance rebound the literal `-1`, which 3k never looked at, so
#     `det I = -1` was proved where the determinant is 1.  Section 3l replaces
#     that one-class check with a general one: every non-theorem declaration
#     reports what its type and body reduce to, and anything outside the set the
#     honest file produces fails, by constant and by class.
#   * a name of the shape Lean gives its own auxiliaries can be written by an
#     author, which dressed two of those instances as generated rows.  Such a
#     name is refused in the source (1g4) and cross-checked against the compiled
#     module (3j).
#   * `cmp` and `diff` are given a known pair of files beside `comm` and `join`,
#     because a `cmp` that answers "same" to everything makes a tampered listing
#     read as matching.
#
# The limit under all of this, stated plainly: elaborating any Lean file can run
# code that file contains, and the source checks and the command allowlist are
# what stands between a reader and that code.  They are a list of what this
# author knows to look for.  A reader checking a file from anywhere other than
# the published folder does that in a sandbox.
#
# Four further limits of this version, stated rather than discovered:
#   * section 3l compares classes, not instances: the classes this file does
#     instantiate — `Decidable` and `DecidableEq`, `Repr`, `SizeOf`, the ones
#     `deriving` and `inductive` write — are a set it accepts, so a second
#     instance of one of those is not reported by it.  The kernel re-add and the axiom walk are
#     what stand behind it there.
#   * a constant hidden under a name that is both a shape Lean generates and a
#     listed declaration's child — `Move.act._f`, say — is classified aux and
#     not reported by 3j.  It does appear as a row in the third section of
#     STATEMENTS.md, and if it is an `OfNat` instance 3k reports it by name.
#   * the gate compares a listing it regenerates against a committed one.  A
#     change made and then committed is green here by design; it is the diff in
#     that file, and a reader reading it, that catches a weakened statement.
#     The one thing the listing cannot show about a statement is the instance a
#     numeral elaborated through, which is why 3k exists.
#   * under a toolchain this gate does not list, rows for definitions Lean
#     generates are not compared (see section 5).
#
# The compiled-module audit began as `VerifyAxioms.lean`, a prototype written by
# the reviewer whose corpus prompted this version; it is credited in
# README_LEAN.md.
#
# Usage:  ./check.sh [file.lean] [README.md] [STATEMENTS.md]
#         ./check.sh --write-statements    (regenerate the committed listing)
#
# Expect one to three minutes, depending on the machine: three elaborations,
# three compilations and three full audits of the compiled module.  Measured
# 69-117 s on a 16-CPU machine with other runs of this gate going at once.

# --- 0. the interpreter ---------------------------------------------------
# Under `sh check.sh` on macOS this script is bash in POSIX mode, where process
# substitution is a syntax error.  Version 2 lost two checks to exactly that and
# printed OK anyway.  `BASH_VERSION` is set in POSIX mode too, so it is not
# enough on its own.
if [ -z "${BASH_VERSION:-}" ]; then
  echo "FAIL: this gate is a bash script and is being run by another shell."
  echo "      Run it as:  bash check.sh   or   ./check.sh"
  exit 1
fi
if [ -o posix ]; then
  echo "FAIL: this gate is running under bash in POSIX mode (this is what"
  echo "      'sh check.sh' does).  Some of its checks are syntax errors there,"
  echo "      and a gate that cannot run its checks has not passed them."
  echo "      Run it as:  bash check.sh   or   ./check.sh"
  exit 1
fi

# --- 0b. the locale ---------------------------------------------------------
# Two things depend on it.  `sort`, `comm` and `join` collate differently under
# a UTF-8 locale, which moved 24 lines of this script's own output without
# changing the verdict; and a pattern carrying a multi-byte character behaves
# differently under C, where each byte is a character.  Both are pinned here
# rather than left to whoever runs the script.  The recorded check_output.txt
# is a run under this setting.
export LC_ALL=C
export LANG=C

set -uo pipefail

# --- 0c. the tools this gate runs ------------------------------------------
# Every external program used below, checked before any of them is used.  A
# reviewer removed `comm` from PATH and watched three checks come back empty and
# read as clean: `comm` runs inside a command substitution whose status nothing
# reads, so a missing one is silence, and silence here looks like agreement.
# `mktemp` is not on this list: there is a fallback for it a few lines down.
REQUIRED_TOOLS=(awk sed grep sort comm join cut tr wc cmp diff head cat cp rm mkdir mv dirname basename)
missing_tools=""
for t in "${REQUIRED_TOOLS[@]}"; do
  command -v "$t" >/dev/null 2>&1 || missing_tools="$missing_tools $t"
done
if [ -n "$missing_tools" ]; then
  echo "FAIL: these programs this gate uses are not on PATH:$missing_tools"
  echo "      Several of its checks read as clean when the program that was to"
  echo "      run them is absent, so it stops here instead."
  exit 1
fi

WRITE_STATEMENTS=0
if [ "${1:-}" = "--write-statements" ]; then WRITE_STATEMENTS=1; shift; fi

FILE="${1:-TetrasemaphoreAlgebra.lean}"
README="${2:-README_LEAN.md}"
STATEMENTS="${3:-STATEMENTS.md}"

# The toolchains this gate is written against.  Each one that is installed is
# used; if none is, whatever `lean` is on PATH is used instead and the output
# says so.  A machine with no Lean at all fails.
ELAN_ROOT="${ELAN_HOME:-${HOME:-}/.elan}"
TOOLCHAIN_PATHS=(
  "$ELAN_ROOT/toolchains/leanprover--lean4---v4.33.0/bin/lean"
  "$ELAN_ROOT/toolchains/leanprover--lean4---v4.32.2/bin/lean"
  "$ELAN_ROOT/toolchains/leanprover--lean4---v4.33.1/bin/lean"
)

# What the types and bodies of this file's own definitions reduce to.
#
# A numeral, a negative numeral, a decimal, an operator and a coercion all print
# in a statement without the instance they went through, so a statement cannot
# show a reader which instance bound them.  Section 3k reported one class,
# `OfNat`; a reviewer then rebound a numeral through an `OfNat` instance hidden
# behind a reducible `abbrev`, and rebound `-1` through a `Neg` instance, which
# that check never looked at.  Rather than name those classes one at a time, the
# audit reports the head constant that every non-theorem declaration's type and
# every definition's body reduces to, and the gate fails on any head outside the
# two sets below.
#
# The rule has two clauses.  A head that is a declaration of the module being
# audited — one of its own types, constructors, recursors or definitions — is
# reported as `«own-constant»`, because a constant of this file cannot be an
# instance of a class from outside it; `Fml`, `Move`, `MoveSet.mk` and
# `Fml.rec` are heads of that kind.  Every other head is compared against the
# sets below, which are what the honest file produces, measured constant by
# constant under 4.32.2, 4.33.0, 4.33.1 and 4.34.1, where they are identical.
# A file that instantiates a class this one does not — `OfNat`, `Neg`,
# `OfScientific`, `LT`, `HAdd`, `Coe`, anything — fails with the constant and
# the head named.  What it does not cover is said plainly in the limits at the
# top of this file: the classes the honest file does instantiate (`Decidable`
# and `DecidableEq`, `Repr`, `SizeOf`) are not distinguished from each
# other here, and an honest file that adds a constant of a shape this one has
# no example of — a `String`, say — fails this check and says which head did
# it, which is the cost of comparing against a set this small.
HONEST_TYPE_HEADS="«no-constant-head» «own-constant» Bool Decidable Decidable.rec Int List Nat PProd Prod Repr SizeOf Std.Format"
HONEST_BODY_HEADS="«no-constant-head» «own-constant» List.append List.cons Prod Repr.mk SizeOf.mk"

# The releases the committed listing was generated under.  The 118 theorems
# elaborate with no errors on every release from 4.30.0-rc2 to 4.34.1, but the
# set of definitions Lean *generates* is not the same across all of them: 4.34
# stopped generating `Move.toCtorIdx` and `Sq.toCtorIdx`, which the listing
# carries, so a run under 4.34 or later regenerates a listing that differs in
# those two rows.  Section 5 calls that drift rather than tampering, and says
# what it then leaves uncompared.
LISTING_WINDOW='^4\.3[0-3]\.'

# The three axioms Lean itself ships.  Compared by exact name, not by substring:
# a declaration called `propext2` is not `propext`.  Nothing else is allowed
# anywhere in the compiled module — not in a theorem, not in a definition, not
# in an auto-generated lemma.
STANDARD_AXIOMS="propext Classical.choice Quot.sound"

# Lemma shapes Lean generates for `inductive`, `structure` and `deriving`.  A
# theorem in the compiled module may carry one of these suffixes without being
# declared in the source; anything else must be in the source.
GENERATED_SHAPES='\.(inj|injEq|sizeOf_spec|eq_def|ofNat_ctorIdx)$|\.brecOn\.eq$'

# Backticked words in the README that are not Lean constants, and so cannot be
# looked up: Lean keywords, commands and tactic names (nothing in the
# environment is called `theorem` or `simp`); words naming a program or a shell
# command; `g`, which this README uses as a stand-in for an arbitrary move; and
# `IsKleinFour`, a Mathlib name the file deliberately does not import and
# mentions only to say what it has not done.
NOT_CONSTANTS='^(sorry|sorryAx|native_decide|omega|simp|decide|rfl|axiom|opaque|import|partial'
NOT_CONSTANTS="$NOT_CONSTANTS"'|unsafe|set_option|implemented_by|extern|theorem|lemma|def|abbrev|example'
NOT_CONSTANTS="$NOT_CONSTANTS"'|inductive|structure|instance|deriving|namespace|open|variable|section|end'
NOT_CONSTANTS="$NOT_CONSTANTS"'|syntax|macro|macro_rules|notation|infix|prefix|postfix|elab|run_cmd|attribute'
NOT_CONSTANTS="$NOT_CONSTANTS"'|initialize|export|admit|elan|chmod|grep|mktemp|bash|sh|lake|posix'
NOT_CONSTANTS="$NOT_CONSTANTS"'|sort|comm|join|sed|awk|diff|tr|cmp|printf'
NOT_CONSTANTS="$NOT_CONSTANTS"'|addDecl|loadExts|OK|FAILED|PATH|lean|olean'
# Names the README mentions precisely because they are NOT in this file: a
# Mathlib name it does not import, Lean's own module and API, and the invented
# constants used to describe an attack.
NOT_CONSTANTS="$NOT_CONSTANTS"'|g|IsKleinFour|Init|Lean|Kernel.Environment.addDecl'
# Two more Lean keywords the 2.3 README quotes (`fun` in the statement-printing
# paragraph, `in` in the command paragraph), one more file name, Lean's own
# name-classification function, and the invented names of the attacks this
# version answers: there is no `_i` in this file, which is the whole point of
# the paragraph that mentions it.
NOT_CONSTANTS="$NOT_CONSTANTS"'|fun|in|lakefile|Name.isInternalDetail|lean_nat_add'
NOT_CONSTANTS="$NOT_CONSTANTS"'|_i|_k|proof_1|inst16vis|Z_fakeDet2'
NOT_CONSTANTS="$NOT_CONSTANTS"'|Z_fakeDet|propext2|VerifyAxioms|GateAudit)$'

fail=0
drift_noted=0

# The recorded output of this gate is offered for comparison, so it carries no
# path that names whoever ran it: a toolchain under the elan root prints
# relative to that root, anything else under the home directory prints as `~/`.
gate_path() {
  local p="$1"
  case "$p" in
    "$ELAN_ROOT"/*) printf '%s\n' "<elan root>/${p#"$ELAN_ROOT"/}" ;;
    "${HOME:-/nonexistent-home}"/*) printf '%s\n' "~/${p#"${HOME:-/nonexistent-home}"/}" ;;
    *) printf '%s\n' "$p" ;;
  esac
}

if [ ! -f "$FILE" ]; then
  echo "FAIL: no such file: $FILE"
  exit 1
fi
# A misspelled README path left the name check with nothing to check and the
# gate printed `README names checked: 0 ; all resolve: yes`.  A check over no
# names is not a check that passed.
if [ ! -f "$README" ]; then
  echo "FAIL: no such README: $README"
  echo "      Section 3i checks that every Lean name this document cites in"
  echo "      backticks exists; with no document there is nothing to check."
  exit 1
fi

# --- the toolchains that will actually be used ----------------------------
LEANS=()
for p in "${TOOLCHAIN_PATHS[@]}"; do
  [ -x "$p" ] && LEANS+=("$p")
done
TOOLCHAIN_SOURCE="listed"
if [ "${#LEANS[@]}" -eq 0 ]; then
  if command -v lean >/dev/null 2>&1; then
    LEANS+=("$(command -v lean)")
    TOOLCHAIN_SOURCE="PATH"
  fi
fi
if [ "${#LEANS[@]}" -eq 0 ]; then
  echo "FAIL: no Lean found.  None of the toolchains this gate lists is installed"
  echo "      and there is no 'lean' on PATH, so nothing could be checked."
  echo "      lean-toolchain in this directory names the version to install."
  exit 1
fi

# A working directory to compile and audit in.  `mktemp` is tried first; where
# it is unavailable — a locked-down TMPDIR, a build sandbox — the fallback sits
# beside the file being checked.  If neither can be made the gate stops: a gate
# that cannot run its checks has not passed them.
WORK=$(mktemp -d 2>/dev/null) || WORK=""
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then
  WORK="$(cd "$(dirname "$FILE")" && pwd)/.check-work.$$"
  rm -rf "$WORK"
  mkdir -p "$WORK" 2>/dev/null
fi
if [ ! -d "$WORK" ] || [ ! -w "$WORK" ]; then
  echo "FAIL: could not create a writable working directory.  This gate needs one"
  echo "      to compile the file and audit it; it does not pass when it cannot run."
  exit 1
fi
trap 'rm -rf "$WORK"' EXIT

# Presence is not behaviour.  `comm` and `join` are the two programs whose
# silence reads as agreement, so each is given a pair of files whose answer is
# known before any check depends on it.
printf 'a\nb\n' > "$WORK/probe1"; printf 'b\nc\n' > "$WORK/probe2"
printf 'k\tv\n'  > "$WORK/probe3"; printf 'k\tw\n' > "$WORK/probe4"
printf 'same\n' > "$WORK/probe5"; printf 'same\n' > "$WORK/probe6"; printf 'other\n' > "$WORK/probe7"
if ! cmp -s "$WORK/probe5" "$WORK/probe6" || cmp -s "$WORK/probe5" "$WORK/probe7" \
   || [ -n "$(diff "$WORK/probe5" "$WORK/probe6")" ] || [ -z "$(diff "$WORK/probe5" "$WORK/probe7")" ]; then
  echo "FAIL: 'cmp' or 'diff' on this PATH does not answer a known pair of files"
  echo "      as this gate reads it.  Section 5 compares the committed listing"
  echo "      with the regenerated one through 'cmp', and a 'cmp' that reports"
  echo "      agreement whatever it is given makes a tampered listing read as"
  echo "      matching, so the gate stops."
  exit 1
fi
if [ "$(comm -23 "$WORK/probe1" "$WORK/probe2")" != "a" ] \
   || [ "$(comm -13 "$WORK/probe1" "$WORK/probe2")" != "c" ] \
   || [ "$(comm -12 "$WORK/probe1" "$WORK/probe2")" != "b" ] \
   || [ "$(join -t "$(printf '\t')" "$WORK/probe3" "$WORK/probe4")" != "$(printf 'k\tv\tw')" ]; then
  echo "FAIL: 'comm' or 'join' on this PATH does not answer a known pair of"
  echo "      files as this gate reads it.  Three of the checks below are a"
  echo "      'comm' whose empty output means agreement, so the gate stops."
  exit 1
fi

# A fixed module name, so the audit does not depend on what the file is called.
cp "$FILE" "$WORK/Subject.lean" || { echo "FAIL: could not copy $FILE."; exit 1; }

echo "=== 1. source checks on $FILE ==="

# The source checks below read *code*, not text.  Version 2 ran its greps over
# the raw file and excused any line that began with a comment marker or
# mentioned a banned word in backticks.  That was wrong in both directions:
# prose inside a doc comment ("the axiom footprint") tripped the axiom check,
# and a doc comment placed in front of a declaration on the same line hid it
# ("/-- a shortcut -/ axiom cheat : …").  So the file is first passed through a
# scanner that understands Lean's nesting block comments, line comments and
# string literals, and blanks every comment, and the inside of every string,
# while keeping line numbers.  Every check after this point reads the blanked
# copy, which is why none of them needs an exception for comments or for
# backticks.
#
# The string interiors are blanked because the patterns were refusing honest
# Lean: `def note : String := "… sorry …"` tripped three of them.  It is safe
# to blank them because nothing in a string can become code here — every command
# that could turn string text into a declaration is refused, the file imports
# nothing, and the compiled module is audited constant by constant afterwards.
# The quotation marks themselves are kept, so that an attribute written
# `@[extern "lean_nat_add"]` still reads as one.
#
# For each line the scanner emits: line number, whether that line begins a
# top-level command (it starts in column 1, outside any comment or string), and
# the line with its comments blanked out.
scan() {
  awk -v endfile="${2:-}" '
    function idchar(ch) { return (ch ~ /[A-Za-z0-9_'"'"'!?]/) }
    BEGIN { depth = 0; instr = 0; inraw = 0; rawh = 0 }
    {
      startDepth = depth; startStr = (instr || inraw)
      line = $0; n = length(line); i = 1; out = ""
      while (i <= n) {
        c = substr(line, i, 1); c2 = substr(line, i, 2)
        prev = (i > 1) ? substr(line, i - 1, 1) : ""
        if (inraw) {
          # A raw string ends at a quotation mark followed by as many `#` as
          # opened it.  Backslash is not an escape here, which is why version
          # 2.3, which treated it as one, could be desynced by `r#"a " b"#`.
          if (c == "\"") {
            h = 0
            while (substr(line, i + 1 + h, 1) == "#" && h < rawh) h++
            if (h == rawh) {
              out = out c
              for (k = 1; k <= rawh; k++) out = out "#"
              i += 1 + rawh; inraw = 0; continue
            }
          }
          out = out " "; i += 1; continue
        }
        if (instr) {
          if (c == "\\") { out = out "  "; i += 2; continue }
          if (c == "\"") { instr = 0; out = out c; i += 1; continue }
          out = out " "; i += 1; continue
        }
        if (depth > 0) {
          if (c2 == "/-") { depth += 1; out = out "  "; i += 2; continue }
          if (c2 == "-/") { depth -= 1; out = out "  "; i += 2; continue }
          out = out " "; i += 1; continue
        }
        if (c2 == "--") { while (i <= n) { out = out " "; i += 1 }; break }
        if (c2 == "/-") { depth += 1; out = out "  "; i += 2; continue }
        # A character literal.  `'"'"'` is a quotation mark that opens nothing, and
        # version 2.3 read it as opening a string, which blanked every line to
        # the next quotation mark and hid whatever was in between — a smuggled
        # `#eval` among them.  A quote that follows an identifier character is a
        # primed name (`g'"'"'`), not a literal, which is why `prev` is consulted.
        if (c == "'"'"'" && !idchar(prev)) {
          j = i + 1
          if (substr(line, j, 1) == "\\") j += 2; else j += 1
          if (substr(line, j, 1) == "'"'"'") {
            out = out "'"'"'"
            for (k = i + 1; k < j; k++) out = out " "
            out = out "'"'"'"
            i = j + 1; continue
          }
        }
        # A raw string opener: `r"`, `r#"`, `r##"` …
        if (c == "r" && !idchar(prev)) {
          j = i + 1; h = 0
          while (substr(line, j, 1) == "#") { h++; j++ }
          if (substr(line, j, 1) == "\"") {
            out = out "r"
            for (k = 1; k <= h; k++) out = out "#"
            out = out "\""
            inraw = 1; rawh = h; i = j + 1; continue
          }
        }
        if (c == "\"") { instr = 1 }
        out = out c; i += 1
      }
      starts = (startDepth == 0 && startStr == 0 && line ~ /^[^ \t]/) ? 1 : 0
      print NR "\t" starts "\t" out
    }
    END {
      # What state the scanner ended the file in.  A file that ends inside a
      # string or a raw string is one the scanner cannot have read correctly.
      if (endfile != "") print (inraw ? "raw-string" : (instr ? "string" : (depth > 0 ? "block-comment" : "clean"))) > endfile
    }' "$1"
}
scan "$FILE" "$WORK/scan.end" > "$WORK/scan.tsv"
if [ "$(wc -l < "$WORK/scan.tsv" | tr -d ' ')" -ne "$(wc -l < "$FILE" | tr -d ' ')" ]; then
  echo "FAIL: the comment scanner did not return one record per line of the file."
  echo "      This gate's own machinery is broken, which is not the same thing as"
  echo "      the file being clean."
  exit 1
fi
# A file that ends inside a string, a raw string or a block comment is a file
# the scanner has not read: every check below reads its output, so the gate
# stops here rather than elaborating on a reading it does not trust.  This is
# before section 2 by construction, so nothing of the file has run.
scan_end=$(cat "$WORK/scan.end" 2>/dev/null || echo "missing")
if [ "$scan_end" != "clean" ]; then
  echo "FAIL: the source scanner reached the end of the file still inside a"
  echo "      $scan_end.  Every check in this section reads what the scanner"
  echo "      blanked, so a file it cannot read to the end is one this gate does"
  echo "      not elaborate: elaborating a Lean file runs code the file contains."
  echo
  echo "FAILED."
  exit 1
fi
cut -f3- "$WORK/scan.tsv" > "$WORK/code.lean"
CODE="$WORK/code.lean"

# Lean lets any identifier be written inside French quotation marks:
# `@«sorryAx»` and `sorryAx` are the same constant.  Version 2.1 answered that
# by putting the quotation marks into the pattern itself, which made the check
# depend on the locale — under C each of those marks is two bytes and the `?`
# binds to the second, so the pattern asked for a byte that was not there and
# matched no spelling of `sorry` at all.  They are stripped from the code here
# instead, so every pattern below is plain ASCII and reads the same under any
# locale.
# An apostrophe as a shell variable, so that the self-test probes below can be
# written without fighting the quoting.
SQ="'"
GUILL_OPEN=$(printf '\302\253'); GUILL_CLOSE=$(printf '\302\273')
sed "s/$GUILL_OPEN//g; s/$GUILL_CLOSE//g" "$WORK/code.lean" > "$WORK/code.ascii.lean"
mv "$WORK/code.ascii.lean" "$WORK/code.lean"

# The same code with its line breaks turned into spaces.  Lean reads a newline
# as whitespace, so `set_option` on one line and `debug.skipKernelTC true` on
# the next is one command; the checks below are run over this copy as well so
# that a line break does not hide a keyword from its argument.  Line numbers are
# lost here, which is why it is the second pass and not the first.
tr '\n' ' ' < "$CODE" > "$WORK/joined.lean"
JOINED="$WORK/joined.lean"

# Each source check runs twice: once over the code with its lines intact, where
# it can report a line number, and once over the joined copy.
src_check() {
  local re="$1" msg="$2"
  if grep -nE "$re" "$CODE" ; then
    echo "FAIL: $msg"
    fail=1
  elif grep -qE "$re" "$JOINED" ; then
    echo "FAIL: $msg  (found only after joining lines: the keyword and its"
    echo "      argument are split across a line break, which Lean reads as"
    echo "      whitespace.)"
    fail=1
  fi
}

# The patterns, named so that the self-test below can run the same ones the
# checks run.
#   1a `sorry` / `sorryAx` / `admit` in a proof position.  `admit` is `sorry`
#      wearing another name.
#   1b native_decide hands the check to the compiler instead of the kernel; in
#      Lean 4.33 `decide +native` is the same tactic under another spelling.
#   1c an `axiom` declaration asserts a claim without proving it, an `opaque`
#      one hides a body from the kernel; an attribute or a doc comment in front
#      of the word does not make it something else.
#   1d unsafe / implemented_by / extern / partial detach a definition from the
#      kernel's view of it.  `extern` is matched anywhere inside an attribute
#      group, not only as the first attribute: version 2.2 asked for
#      `@[ extern` and `@[inline, extern "lean_nat_add"]` walked past it, on
#      an already-listed definition, with the listing and the log unchanged.
#   1e zero imports: the file rests on core Lean only.  (The compiled module's
#      own header is checked in section 3, where the source text cannot reach
#      it.)
#   1f no `set_option` at all.  `warn.sorry false` silences Lean's warning about
#      a skipped proof and `debug.skipKernelTC true` switches the kernel off,
#      and neither has to be enumerated if none is permitted.
PAT_1a='(^|[^-[:alnum:]_.])(sorry|sorryAx|admit)\b'
PAT_1b='\bnative_decide\b|\+[[:space:]]*native\b'
PAT_1c='(^|[^[:alnum:]_.])(axiom|opaque)[[:space:]]+[A-Za-z_]'
PAT_1d='\b(unsafe|unsafeCast|implemented_by|partial)\b|@\[[^]]*\b(extern|implemented_by)\b'
PAT_1e='(^|[^[:alnum:]_.])import([[:space:]]|$)'
PAT_1f='\bset_option\b'
#   1g2 the commands a proof file has no use for, anywhere on a line of code
#      rather than only at its start.  `open Nat in #eval …` satisfied the
#      allowlist below, which reads the first word of a line, and ran arbitrary
#      IO while the gate was running; so did `variable … in`, `section … in`,
#      and an `#eval` that was merely indented, which Lean accepts as a
#      top-level command.  The `#print axioms <name>` lines are blanked before
#      this pattern runs, being the one `#`-command this file uses.
PAT_1g2='(^|[^[:alnum:]_.])(#[A-Za-z_][A-Za-z_]*|run_cmd|macro|macro_rules|syntax|notation|infix|infixl|infixr|prefix|postfix|elab|elab_rules|initialize|builtin_initialize|attribute|export|unif_hint|simproc|dsimproc|declare_syntax_cat|register_simp_attr|binder_predicate)([^[:alnum:]_]|$)'
#   1g3 the two lexical constructs this file does not use and a scanner can read
#      wrongly: a character literal and a raw string.  A reviewer hid a `#eval`
#      behind a character literal holding a quotation mark; in version 2.3's
#      scanner that quotation mark opened a string, which blanked every line to
#      the next one and hid the `#eval`, so the file was elaborated and its IO
#      ran during the gate.  The scanner above reads both constructs now; this
#      check refuses them as well, because a file that needs neither is cheaper
#      to refuse than to lex.  Counted on the honest file with its comments
#      blanked: 0 character literals, 0 raw strings.  The leading guard is what
#      keeps a primed name (`g'`, `hp0'`) out of it: a character literal opens
#      where an identifier does not continue.
PAT_1g3='(^|[^A-Za-z0-9_!?])('"'"'[^'"'"']{0,6}'"'"'|r#*")'

# A check that does not fire is indistinguishable, in the output, from a file
# that is clean.  So before any of them runs, each pattern is given a line it
# has to match and the whole set is given a line none of them may match.  If
# the self-test disagrees, the gate stops: it has not performed its checks.
selftest() {
  local probe="$WORK/selftest.raw" blanked="$WORK/selftest.lean" bad=""
  {
    printf '%s\n' '  sorry'
    printf '%s\n' 'theorem z : False := by sorryAx'
    printf '%s\n' "exact @${GUILL_OPEN}sorryAx${GUILL_CLOSE} _ false"
    printf '%s\n' 'theorem z2 : False := by admit'
    printf '%s\n' 'theorem z3 : True := by native_decide'
    printf '%s\n' 'theorem z4 : True := by decide +native'
    printf '%s\n' '@[simp] axiom cheat : False'
    printf '%s\n' '/-- d -/ opaque hidden : Nat'
    printf '%s\n' 'unsafe def u : Nat := 0'
    printf '%s\n' '@[inline] partial def pd : Nat := 0'
    printf '%s\n' '@[implemented_by u] def v : Nat := 0'
    printf '%s\n' '@[inline, extern "lean_nat_add"] def w : Nat := 0'
    printf '%s\n' 'import Lean'
    printf '%s\n' 'set_option debug.skipKernelTC true'
    printf '%s\n' 'open Nat in #eval (1 + 1)'
    printf '%s\n' "def dq : Char := ${SQ}\"${SQ}"
  } > "$probe"
  sed "s/$GUILL_OPEN//g; s/$GUILL_CLOSE//g" "$probe" > "$blanked"
  local n
  for n in 1a 1b 1c 1d 1e 1f 1g2 1g3; do
    local pat; eval "pat=\$PAT_$n"
    grep -qE "$pat" "$blanked" || bad="$bad $n"
  done
  # Four spellings of `sorry` the earlier gate's pattern missed under this
  # locale; each is checked on its own, not just somewhere in the file.
  local line
  while IFS= read -r line; do
    printf '%s\n' "$line" | grep -qE "$PAT_1a" || bad="$bad 1a/$line"
  done <<< "$(head -4 "$blanked")"
  printf '%s\n' 'theorem T4_fix_I (p : Pt) : Move.act Move.I p = p := by cases p; rfl' > "$WORK/selftest.neg"
  for n in 1a 1b 1c 1d 1e 1f 1g2 1g3; do
    local pat; eval "pat=\$PAT_$n"
    grep -qE "$pat" "$WORK/selftest.neg" && bad="$bad neg/$n"
  done
  # The scanner itself, in both directions: a banned word inside a string
  # literal is blanked, and a declaration behind a doc comment on the same line
  # is not.  The first direction is the one that was refusing honest Lean; the
  # second is the one version 2 lost.
  {
    printf '%s\n' 'def note : String := "sorry axiom set_option native_decide"'
    printf '%s\n' '/-- a shortcut -/ axiom cheat : False'
  } > "$WORK/selftest.str"
  scan "$WORK/selftest.str" | cut -f3- > "$WORK/selftest.str.blanked"
  sed -n '1p' "$WORK/selftest.str.blanked" > "$WORK/selftest.str.1"
  sed -n '2p' "$WORK/selftest.str.blanked" > "$WORK/selftest.str.2"
  for n in 1a 1b 1c 1f; do
    local pat; eval "pat=\$PAT_$n"
    grep -qE "$pat" "$WORK/selftest.str.1" && bad="$bad string/$n"
  done
  grep -qE "$PAT_1c" "$WORK/selftest.str.2" || bad="$bad doc-comment/1c"
  # The scanner against the two constructs that desynced version 2.3, and
  # against the honest shape they resemble.  Each probe is a line whose banned
  # word has to survive the scanner, because what desyncs a scanner is what
  # hides the next line from every check that reads its output.
  {
    printf '%s\n' "def dq : Char := ${SQ}\"${SQ}"
    printf '%s\n' '#eval IO.println 1'
    printf '%s\n' 'def rs : String := r#"a " b"#'
    printf '%s\n' 'axiom cheat2 : False'
    printf '%s\n' "theorem t (g${SQ} : Nat) : g${SQ} = g${SQ} := rfl"
  } > "$WORK/selftest.lex"
  scan "$WORK/selftest.lex" "$WORK/selftest.lex.end" | cut -f3- > "$WORK/selftest.lex.blanked"
  sed -n '2p' "$WORK/selftest.lex.blanked" > "$WORK/selftest.lex.2"
  sed -n '4p' "$WORK/selftest.lex.blanked" > "$WORK/selftest.lex.4"
  sed -n '5p' "$WORK/selftest.lex.blanked" > "$WORK/selftest.lex.5"
  grep -qE "$PAT_1g2" "$WORK/selftest.lex.2" || bad="$bad char-literal-desync/1g2"
  grep -qE "$PAT_1c"  "$WORK/selftest.lex.4" || bad="$bad raw-string-desync/1c"
  grep -qE "$PAT_1g3" "$WORK/selftest.lex.5" && bad="$bad primed-name/1g3"
  [ "$(cat "$WORK/selftest.lex.end" 2>/dev/null)" = "clean" ] || bad="$bad lex-probe-end"
  if [ -n "$bad" ]; then
    echo "FAIL: this gate's own source checks did not behave as written:$bad"
    echo "      A check that cannot fire is not the same thing as a clean file,"
    echo "      so the gate stops here.  (Locale in use: LC_ALL=$LC_ALL.)"
    exit 1
  fi
  echo "  self-test: the eight source patterns fire on a probe and leave an honest line"
  echo "  alone; the scanner blanks a string literal's inside, does not blank a"
  echo "  declaration behind a doc comment, and keeps a character literal and a raw"
  echo "  string from hiding the line after them."
}
selftest

src_check "$PAT_1a" "'sorry', 'sorryAx' or 'admit' used in a proof position (above)."
src_check "$PAT_1b" "the compiler is being asked to stand in for the kernel (above)."
src_check "$PAT_1c" "an 'axiom' or 'opaque' declaration is present (above)."
src_check "$PAT_1d" "'unsafe' / 'unsafeCast' / 'implemented_by' / 'partial' / 'extern' present (above)."
src_check "$PAT_1e" "file imports something; this gate expects zero imports."
src_check "$PAT_1f" "'set_option' is present (above); this file is expected to need none."
src_check "$PAT_1g3" "a character literal or a raw string is present (above).  This file uses
      neither — the count is 0 of each with its comments blanked — and both are
      constructs a scanner can read wrongly, which is how a smuggled '#eval' was
      hidden from version 2.3 and run during the gate."

# 1g. Top-level command allowlist.
#
# Each line that begins a command is reduced to its first word — after any
# attribute group and any declaration modifier — and that word has to be one a
# proof file needs.  Commands that change what Lean does or prints are not on
# the list: `#eval`, `#exit`, `#guard_msgs`, `#check`, `syntax`, `macro`,
# `macro_rules`, `notation`, `infix`, `prefix`, `postfix`, `elab`, `run_cmd`,
# `attribute`, `export`, `initialize`.  Neither is anything unrecognised, which
# is the direction a gate should fail in.
badcmds=$(awk -F'\t' '$2 == 1 {
    l = $3
    sub(/^[ \t]+/, "", l)
    sub(/[ \t]+$/, "", l)
    if (l == "") next
    gsub(/^(@\[[^]]*\][ \t]*)+/, "", l)
    while (sub(/^(private|protected|noncomputable|scoped|local)[ \t]+/, "", l) > 0) ;
    if (l ~ /^#print[ \t]+axioms[ \t]+[A-Za-z_][A-Za-z0-9_.]*$/) next
    head = l; sub(/[ \t(:{<|\[].*$/, "", head)
    ok = " theorem lemma def abbrev inductive structure instance namespace section end open variable deriving "
    if (index(ok, " " head " ") == 0) print "    line " $1 ": " l
  }' "$WORK/scan.tsv")
if [ -n "$badcmds" ]; then
  echo "FAIL: commands outside the allowlist, or an unrecognised line, at the"
  echo "      start of a line:"
  echo "$badcmds"
  fail=1
fi

# 1g2. The same commands, anywhere on a line.
#
# Reducing a line to its first word is not enough.  `open Nat in #eval …`
# satisfies the allowlist above and runs arbitrary IO while the gate is running
# — a reviewer wrote a file that appended to a log in the gate's own working
# directory, three times in the directory it was invoked from and three times in
# the directory the audit program is written to.  `variable … in`, `section … in`
# and `def … in` do the same, and so does an `#eval` that is simply indented,
# because Lean accepts a top-level command at any column.  So the commands this
# file has no use for are refused anywhere on a line of code, after any number
# of `in`s, at any column.  The one `#`-command the file does use, `#print
# axioms <name>`, is blanked first.
sed -E 's/^[[:space:]]*#print[[:space:]]+axioms[[:space:]]+[A-Za-z_][A-Za-z0-9_.]*[[:space:]]*$//' \
  "$CODE" > "$WORK/code.nopa.lean"
tr '\n' ' ' < "$WORK/code.nopa.lean" > "$WORK/joined.nopa.lean"
if grep -nE "$PAT_1g2" "$WORK/code.nopa.lean" ; then
  echo "FAIL: a command this gate refuses appears on a line of code (above)."
  echo "      Refused anywhere on a line, not only at its start: every"
  echo "      '#'-command other than '#print axioms <name>', run_cmd, macro,"
  echo "      macro_rules, syntax, notation, infix / prefix / postfix, elab,"
  echo "      initialize, attribute and export."
  fail=1
elif grep -qE "$PAT_1g2" "$WORK/joined.nopa.lean" ; then
  echo "FAIL: a command this gate refuses appears on a line of code  (found only"
  echo "      after joining lines: the command and its argument are split across"
  echo "      a line break, which Lean reads as whitespace.)"
  fail=1
fi

# 1h. Every theorem is followed somewhere by its own `#print axioms` line, so
#     the file's self-reported footprint is the whole file and not a flattering
#     selection.  (Section 4 no longer trusts that report, but a file that will
#     not state its own footprint is not one to publish either.)
#     The namespace prefix is kept on a stack rather than in one variable.  A
#     reviewer's honest-Lean probes showed why: with a single variable,
#     `namespace A` inside `namespace B` overwrote the outer name instead of
#     stacking, and a `section … end` inside a namespace cleared the prefix, so
#     the gate failed files that Lean itself is perfectly happy with.  A check
#     that fails honest Lean is a check that gets loosened later.
thm_list() {
  awk '
    BEGIN { depth = 0 }
    function prefix(   i, ns) {
      ns = ""
      for (i = 1; i <= depth; i++) if (stack[i] != "") ns = ns stack[i] "."
      return ns
    }
    /^namespace[ \t]+/     { stack[++depth] = $2; next }
    /^section([ \t]|$)/    { stack[++depth] = "";  next }
    /^end([ \t]|$)/        { if (depth > 0) depth--; next }
    /^[ \t]*(@\[[^]]*\][ \t]*)?(theorem|lemma)[ \t]+/ {
      line = $0
      sub(/^[ \t]*/, "", line)
      sub(/^@\[[^]]*\][ \t]*/, "", line)
      sub(/^(theorem|lemma)[ \t]+/, "", line)
      name = line
      sub(/[ \t(:{].*$/, "", name)
      if (name != "") print prefix() name
    }' "$CODE" | sort -u
}
print_list() {
  grep -E '^#print[[:space:]]+axioms[[:space:]]' "$CODE" | awk '{print $3}' | sort -u
}
# The definitions the source declares, by name.  Used in section 5: a listing
# row for a definition whose name the source does not declare is one Lean
# generated, and those are the rows that move between toolchain releases.
def_list() {
  awk '
    BEGIN { depth = 0 }
    function prefix(   i, ns) {
      ns = ""
      for (i = 1; i <= depth; i++) if (stack[i] != "") ns = ns stack[i] "."
      return ns
    }
    /^namespace[ \t]+/     { stack[++depth] = $2; next }
    /^section([ \t]|$)/    { stack[++depth] = "";  next }
    /^end([ \t]|$)/        { if (depth > 0) depth--; next }
    /^[ \t]*(@\[[^]]*\][ \t]*)?(private[ \t]+|protected[ \t]+|noncomputable[ \t]+)*(def|abbrev|instance|inductive|structure)[ \t]+/ {
      line = $0
      sub(/^[ \t]*/, "", line)
      sub(/^@\[[^]]*\][ \t]*/, "", line)
      while (sub(/^(private|protected|noncomputable)[ \t]+/, "", line) > 0) ;
      sub(/^(def|abbrev|instance|inductive|structure)[ \t]+/, "", line)
      name = line
      sub(/[ \t(:{\[].*$/, "", name)
      if (name != "") print prefix() name
    }' "$CODE" | sort -u
}
thm_list > "$WORK/src_thms.txt"
print_list > "$WORK/src_prints.txt"
def_list > "$WORK/src_defs.txt"

# 1g4. No declared name of the shape Lean uses for its own auxiliaries.
#      The audit accepts a name as an auxiliary when its parent is a constant of
#      this module and every component after it is a shape Lean generates — and
#      an author can write such a name directly, which is how an `OfNat` and a
#      `Neg` instance reached the third section of the listing dressed as
#      generated rows.  The honest file declares 165 names and none of them has
#      that shape, so a declared name that does is refused here, by the source,
#      before anything is elaborated.
forged=$(awk '
  /^[ \t]*(@\[[^]]*\][ \t]*)?(private[ \t]+|protected[ \t]+|noncomputable[ \t]+|local[ \t]+|scoped[ \t]+)*(def|abbrev|instance|theorem|lemma|inductive|structure|opaque)[ \t]+/ {
    line = $0
    sub(/^[ \t]*/, "", line); sub(/^@\[[^]]*\][ \t]*/, "", line)
    while (sub(/^(private|protected|noncomputable|local|scoped)[ \t]+/, "", line) > 0) ;
    sub(/^(def|abbrev|instance|theorem|lemma|inductive|structure|opaque)[ \t]+/, "", line)
    name = line; sub(/[ \t(:{<|\[].*$/, "", name)
    if (name ~ /\.(match_[0-9]+|eq_[0-9]+|eq_def|splitter|_proof_[0-9]+|_f|_g|_sunfold|_unsafe_rec|_sizeOf_[0-9]+|_sizeOf_inst|_flat_ctor|_simp_[0-9]+|_cstage[0-9]+)$/)
      print "    line " NR ": " name
  }' "$CODE")
if [ -n "$forged" ]; then
  echo "FAIL: these declarations carry names of the shape Lean uses for the"
  echo "      auxiliaries it generates underneath a declaration, which the audit"
  echo "      reads as generated and the listing files among 345 such rows:"
  echo "$forged"
  fail=1
fi
nthm=$(wc -l < "$WORK/src_thms.txt" | tr -d ' ')
npr=$(wc -l < "$WORK/src_prints.txt" | tr -d ' ')
if ! [ "$nthm" -gt 0 ] 2>/dev/null; then
  echo "FAIL: found no theorem declarations at all; this gate's own extraction"
  echo "      is broken, which is not the same thing as the file being clean."
  fail=1
  nthm=-1
fi
unprinted=$(comm -23 "$WORK/src_thms.txt" "$WORK/src_prints.txt")
dangling=$(comm -13 "$WORK/src_thms.txt" "$WORK/src_prints.txt")
if [ -n "$unprinted" ]; then
  echo "FAIL: these theorems have no '#print axioms' line of their own:"
  echo "$unprinted" | sed 's/^/    /'
  fail=1
fi
if [ -n "$dangling" ]; then
  echo "FAIL: these '#print axioms' lines name something that is not a theorem"
  echo "      declared in this file:"
  echo "$dangling" | sed 's/^/    /'
  fail=1
fi
echo "  theorems declared: $nthm ; '#print axioms' lines: $npr"

[ "$fail" -eq 0 ] && echo "OK: no sorry, no compiler-trusted decision, no axiom or opaque
    declaration, no unsafe, no extern, no import, no set_option, no command
    outside the allowlist at the start of a line and none of the refused
    commands anywhere on one, and every theorem prints its own axioms.  The
    same checks were run over a copy with the line breaks collapsed."

# --- 1z. nothing is elaborated until the checks above are satisfied -------
# Elaborating a Lean file runs code the file contains: `#eval` and the other
# commands the checks above look for run while Lean reads the file, before any
# proof is checked.  A reviewer's `open Nat in #eval (… IO.FS.withFile … )` wrote
# a file in the gate's own working directory while the gate was running; the
# first build of 2.3 refused that line in section 1 and then ran sections 2 and 3
# anyway, which got the verdict right and ran the code.  So the gate stops here
# when any check above failed, and says that the file was not elaborated.
if [ "$fail" -ne 0 ]; then
  echo
  echo "FAIL: the file was not elaborated.  The source checks above refused it, and"
  echo "      elaborating a Lean file runs code the file contains: \`#eval\` and the"
  echo "      other commands those checks look for run while Lean reads the file,"
  echo "      before any proof is checked.  Sections 2 to 7 were not run."
  echo
  echo "FAILED."
  exit 1
fi

echo
echo "=== 2. elaboration under every toolchain that is installed ==="
if [ "$TOOLCHAIN_SOURCE" = "PATH" ]; then
  echo "  (none of the ${#TOOLCHAIN_PATHS[@]} listed toolchains is installed; using the 'lean' on PATH)"
elif [ "${#LEANS[@]}" -lt "${#TOOLCHAIN_PATHS[@]}" ]; then
  echo "  (${#LEANS[@]} of the ${#TOOLCHAIN_PATHS[@]} listed toolchains are installed; the missing ones were not run)"
fi

# Lean's own output goes to a file rather than into a shell variable that is
# then piped into `grep -q`.  Under `pipefail`, `echo "$big" | grep -q` is a
# race: grep exits on its first match, echo takes SIGPIPE, and the pipeline
# reports a failure that reads as a check that could not run.  A reviewer saw
# both directions of it — a spurious failure on an honest audit, and a `sorry`
# file with a large elaboration output labelled `[ok]`.
primary_out=""
ran_versions=()
li=0
for lean in "${LEANS[@]}"; do
  li=$((li + 1))
  elog="$WORK/elab.$li.log"
  ver=$("$lean" --version 2>&1 | head -1)
  "$lean" "$FILE" > "$elog" 2>&1
  code=$?
  out=$(cat "$elog")
  if [ -z "$primary_out" ]; then primary_out="$out"; fi

  status="ok"
  if [ "$code" -ne 0 ]; then
    echo "FAIL: $ver exited $code"
    grep -E 'error' "$elog" | head -20
    status="errors"
    fail=1
  fi
  if grep -qi "declaration uses .sorry" "$elog"; then
    echo "FAIL: $ver reports a declaration using \`sorry\`."
    status="sorry"
    fail=1
  fi
  if grep -q 'sorryAx' "$elog"; then
    echo "FAIL: $ver reports a theorem depending on sorryAx."
    status="sorryAx"
    fail=1
  fi
  if grep -qi "using 'exit' to interrupt" "$elog"; then
    echo "FAIL: $ver reports the file cut itself short with '#exit'."
    status="exit"
    fail=1
  fi
  ran_versions+=("$ver")
  echo "  [$status] $ver"
  echo "          $(gate_path "$lean")"
done

echo
echo "=== 3. audit of the compiled module ==="
echo "  (read from the .olean by a wrapper this script writes, with module"
echo "   initializers off; not from anything the file printed about itself)"

# The names the README cites in backticks.  Each is tried bare and qualified by
# each namespace the file opens, so that prose may write `mirV` for `Sq.mirV`.
namespaces=$(grep -E '^namespace[[:space:]]' "$CODE" | awk '{print $2}' | sort -u)
grep -oE '`[^`]+`' "$README" 2>/dev/null | tr -d '`' \
  | grep -E '^[A-Za-z_][A-Za-z0-9_.]*$' \
  | grep -vE '\.(lean|sh|md|txt|py|json|cff|olean|tsv)$' \
  | grep -vE "$NOT_CONSTANTS" | sort -u > "$WORK/cited_names.txt"
: > "$WORK/cited.txt"
while IFS= read -r nm; do
  [ -z "$nm" ] && continue
  cands="$nm"
  for ns in $namespaces; do cands="$cands $ns.$nm"; done
  echo "$cands" >> "$WORK/cited.txt"
done < "$WORK/cited_names.txt"
ncited=$(wc -l < "$WORK/cited.txt" | tr -d ' ')

cat > "$WORK/GateAudit.lean" <<'LEANEOF'
/-
  GateAudit.lean — written by check.sh.  Not part of the proof file, not
  imported by it, and not readable by it.  It reads the COMPILED module and
  never the source text:
    * every import in the module header has to be `Init`
    * every constant of every kind — theorem, def, abbrev, instance, opaque,
      inductive, constructor — has its axiom set computed here, by this
      program, rather than taken from anything the module printed
    * a constant whose type is a Prop but which is not a theorem is reported:
      that is a proposition proved by a definition, which is how an admitted
      `False` slipped past an audit that enumerated theorems only
    * every declaration is re-added to a fresh Init-only environment through
      `Kernel.Environment.addDecl`, the kernel's own entry point, which has no
      parameter for switching the check off
    * every constant is classified by name into `named`, `private`, `aux` or
      `internal`, and the last of those is reported.  Version 2.2 asked
      `Name.isInternalDetail` and listed nothing it called internal, which let
      `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` — and the name `proof_1`,
      which that function also calls internal — rebind the numeral in a public
      statement while the committed listing stayed byte-identical.  `aux` here
      means a name Lean generates *for a declaration the listing shows*: the
      parent is a constant of this module that is listed, and every component
      after it is a shape Lean's own machinery writes.  Anything else Lean calls
      internal is a name somebody wrote, and it is reported and listed.
    * any constant of this module whose type is an `OfNat` instance is reported:
      that is what rebinding a numeral takes, and a numeral is the one thing in
      a statement that prints the same however it was bound
    * each theorem's elaborated statement, each definition's body and each
      generated auxiliary are written out for STATEMENTS.md

  The module is loaded with `loadExts := false`.  No module initializer, no
  `@[init]` function, no user delaborator and no user unexpander runs inside
  this program, and the class table is not loaded, so instance projections
  print under their own names (`List.instMembership.mem L q`) rather than
  through the class.  Lean's builtin delaborators do run — binders, `fun` and
  field notation are theirs — and `pp.notation false` is set, so statements
  print as plain constant applications (`Eq a b`, not `a = b`) and nothing a
  `notation` declares can change which constant a row names.

  Usage: lean --run GateAudit.lean <sysroot> <olean-dir> <Module> <cited.txt>
           <statements.tsv> <definitions.tsv> <auxiliaries.tsv>
-/
import Lean
open Lean

def valueConsts : ConstantInfo → Array Name
  | .thmInfo v    => v.value.getUsedConstants
  | .defnInfo v   => v.value.getUsedConstants
  | .opaqueInfo v => v.value.getUsedConstants
  | _ => #[]

/-- Axioms reachable from a constant, by walking the compiled environment. -/
partial def axiomsOf (env : Environment) (root : Name) : Array Name := Id.run do
  let mut seen : NameSet := {}
  let mut out : Array Name := #[]
  let mut stack : Array Name := #[root]
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | some (.axiomInfo _) => out := out.push n
    | some ci => stack := stack ++ ci.type.getUsedConstants ++ valueConsts ci
    | none => pure ()
  return out.qsort Name.lt

def kindOf : ConstantInfo → String
  | .axiomInfo _  => "axiom"
  | .thmInfo _    => "theorem"
  | .defnInfo _   => "def"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _   => "quot"
  | .inductInfo _ => "inductive"
  | .ctorInfo _   => "ctor"
  | .recInfo _    => "rec"

/-- Digit runs collapsed to `N`, so that `eq_4` and `eq_17` are one shape. -/
def normDigits (s : String) : String :=
  (s.toList.foldl (fun (acc : String × Bool) c =>
      if c.isDigit then (if acc.2 then acc else (acc.1.push 'N', true))
      else (acc.1.push c, false)) ("", false)).1

/-- The name shapes Lean's own machinery generates underneath a declaration.
    The first twelve are every shape this module actually produces, measured
    under 4.32.2, 4.33.0, 4.33.1 and 4.34.1; the rest are other shapes Lean's
    sources generate, listed so that a toolchain change does not fail an honest
    file.  A name Lean calls internal whose shape is not here is treated as one
    somebody wrote: it is reported by name, which is the direction to fail in. -/
def generatedShapes : List String :=
  ["eq_N", "_proof_N", "_proof_N_N", "match_N", "splitter", "_sizeOf_inst",
   "_sizeOf_N", "_unsafe_rec", "_sunfold", "_simp_N_N", "_f", "_flat_ctor",
   "eq_def", "eq_N_N", "match_N_N", "_simp_N", "_g", "_cstageN", "_closed_N",
   "_lambda_N", "_elambda_N", "_spec_N", "_redArg", "_unary", "_sparam_N",
   "_eq_N", "_cstage_N", "_unsafe_def"]

/-- `some parent` when the name is a non-internal constant of this module
    followed by components that are all shapes Lean generates.  `listed` is the
    set of non-internal constants, which is wider than the set of rows the
    listing prints: the derived constructors and recursors are in it.  Walks up from the full name,
    so `Fml.holds.match_1.splitter` resolves to `Fml.holds` through a parent
    (`…match_1`) that is itself an auxiliary. -/
partial def auxParent (listed : Name → Bool) (u : Name) (trailing : List String) : Option Name :=
  if listed u && !trailing.isEmpty
      && trailing.all (fun c => generatedShapes.contains (normDigits c)) then
    some u
  else
    match u with
    | .str p s => auxParent listed p (s :: trailing)
    | .num p i => auxParent listed p (s!"{i}" :: trailing)
    | .anonymous => none

/-- The head constant of a declaration's conclusion, under its binders, as the
    expression stands. -/
partial def resultHead (e : Expr) : Option Name :=
  match e with
  | .forallE _ _ b _ => resultHead b
  | .mdata _ b       => resultHead b
  | _                => e.getAppFn.constName?

/-- The head constant of a conclusion after weak-head normalisation — that is,
    after unfolding whatever definitions stand between the expression and its
    head.  Version 2.3 asked `resultHead` alone, and an `OfNat` instance behind a
    one-line `abbrev` answered with the abbrev's name: `instance myThree :
    ThreeInst`, where `abbrev ThreeInst := OfNat Nat 3`, was an `OfNat` instance
    that section 3k did not see, and it rebound a numeral.  Instance synthesis
    unfolds the abbrev; so does this. -/
def unfoldedHead (env : Environment) (e : Expr) : IO (Option Name) := do
  let ctx : Core.Context := { fileName := "<gate-audit>", fileMap := default,
                              options := {}, maxHeartbeats := 1000000 }
  try
    let act : MetaM (Option Name) := do
      let (_, _, concl) ← Lean.Meta.forallMetaTelescope e
      let w ← Lean.Meta.whnf concl
      pure w.getAppFn.constName?
    let (r, _) ← act.run'.toIO ctx { env := env }
    pure r
  catch _ => pure none

structure St where
  kenv  : Kernel.Environment
  done  : NameSet := {}
  errs  : Array String := #[]
  added : Nat := 0

def markBlockDone (src : Environment) (all : List Name) (d : NameSet) : NameSet :=
  all.foldl (fun d i =>
    let d := (d.insert i).insert (mkRecName i)
    match src.find? i with
    | some (.inductInfo iv) => iv.ctors.foldl (fun d c => d.insert c) d
    | _ => d) d

/-- `debug.skipKernelTC` is named explicitly and set to false, so that the value
    of the option in any surrounding environment cannot reach this check. -/
def kernelOpts : Options := (({} : Options).setBool `debug.skipKernelTC false)

def kernelAdd (decl : Declaration) (what : String) : StateT St IO Unit := do
  let s ← get
  match s.kenv.addDecl kernelOpts decl with
  | .ok kenv' => set { s with kenv := kenv', added := s.added + 1 }
  | .error e =>
    let msg ← (e.toMessageData {}).toString
    set { s with errs := s.errs.push s!"kernel rejects {what}: {msg}" }

partial def readd (src : Environment) (idx : ModuleIdx) (n : Name) : StateT St IO Unit := do
  if src.getModuleIdxFor? n != some idx then return
  if (← get).done.contains n then return
  let some ci := src.find? n | return
  let block? : Option (List Name) := match ci with
    | .inductInfo v => some v.all
    | .ctorInfo v   => match src.find? v.induct with | some (.inductInfo w) => some w.all | _ => none
    | .recInfo v    => some v.all
    | _ => none
  match block? with
  | some all =>
    modify fun s => { s with done := markBlockDone src all s.done }
    let mut types : List InductiveType := []
    let mut deps : Array Name := #[]
    for i in all do
      let some (.inductInfo iv) := src.find? i | throw <| IO.userError s!"not an inductive: {i}"
      let mut ctors : List Constructor := []
      for c in iv.ctors do
        let some cci := src.find? c | throw <| IO.userError s!"missing ctor {c}"
        ctors := ctors ++ [{ name := c, type := cci.type }]
        deps := deps ++ cci.type.getUsedConstants
      deps := deps ++ iv.type.getUsedConstants
      types := types ++ [{ name := i, type := iv.type, ctors := ctors }]
    for d in deps do readd src idx d
    let some (.inductInfo iv0) := src.find? all.head! | return
    kernelAdd (.inductDecl iv0.levelParams iv0.numParams types iv0.isUnsafe) s!"inductive block {all}"
  | none =>
    modify fun s => { s with done := s.done.insert n }
    let deps := ci.type.getUsedConstants ++ valueConsts ci
    for d in deps do readd src idx d
    match ci with
    | .thmInfo v    => kernelAdd (.thmDecl v) s!"theorem {n}"
    | .defnInfo v   =>
        -- Compiler helpers Lean generates for recursive definitions are unsafe
        -- and the kernel does not take them.  They are not added; they are
        -- reported on their CONST line, and a theorem that reached one would
        -- fail its own re-add below on an unknown constant, which is the
        -- failure we want.
        if v.safety == .safe then kernelAdd (.defnDecl v) s!"def {n}" else pure ()
    | .opaqueInfo v => kernelAdd (.opaqueDecl v) s!"opaque {n}"
    | .axiomInfo v  => kernelAdd (.axiomDecl v) s!"axiom {n}"
    | _ => pure ()

def ppStatement (env : Environment) (e : Expr) : IO String := do
  let opts := (({} : Options).setBool `pp.notation false).setBool `pp.unicode.fun true
  let ctx : Core.Context := { fileName := "<gate-audit>", fileMap := default,
                              options := opts, maxHeartbeats := 0 }
  try
    let (fmt, _) ← (Lean.Meta.ppExpr e).run'.toIO ctx { env := env }
    let s := (toString fmt).replace "\n" " "
    return " ".intercalate (s.splitOn " " |>.filter (· != ""))
  catch _ => return "<statement could not be rendered>"

def isPropType (env : Environment) (e : Expr) : IO Bool := do
  try
    let (b, _) ← (Lean.Meta.isProp e).run'.toIO
      { fileName := "<gate-audit>", fileMap := default, options := {}, maxHeartbeats := 0 }
      { env := env }
    pure b
  catch _ => pure false

def main (args : List String) : IO UInt32 := do
  let [sysroot, dir, modStr, citedFile, stmtFile, defsFile, auxFile] := args
    | do IO.eprintln "usage: GateAudit <sysroot> <dir> <Module> <cited.txt> <statements.tsv> <definitions.tsv> <auxiliaries.tsv>"; return 2
  let mod := modStr.toName
  initSearchPath sysroot [dir]
  -- trustLevel 0, no plugins, leakEnv false, loadExts false.
  let env ← importModules #[{ module := mod }] {} 0 #[] false false
  IO.println "AUDIT-BEGIN"
  let some idx := env.getModuleIdx? mod
    | do IO.println "AUDIT-ERROR module-not-found"; IO.println "AUDIT-END"; return 2
  let md := env.header.moduleData[idx.toNat]!
  for i in md.imports do IO.println s!"IMPORT {i.module}"
  -- Every constant of this module under the name a reader would see: a private
  -- declaration's `_private.<module>.<n>.` wrapper removed.  A name is `listed`
  -- when it is one of these and Lean does not call it internal, which is
  -- exactly the set the two halves of STATEMENTS.md print.
  let userNames : NameSet :=
    md.constNames.foldl (fun s n => s.insert ((privateToUserName? n).getD n)) {}
  -- Every constant this module declares, under both spellings of a private
  -- name: the set the head rule's first clause asks about.
  let modNames : NameSet :=
    md.constNames.foldl (fun s n => (s.insert n).insert ((privateToUserName? n).getD n)) {}
  let listed : Name → Bool := fun p => userNames.contains p && !p.isInternalDetail
  let mut stmts : Array String := #[]
  let mut defs : Array String := #[]
  let mut auxs : Array String := #[]
  for n in md.constNames do
    let some ci := env.find? n | continue
    let axs := axiomsOf env n
    -- Four classes, where 2.2 had three.  `private` is a declaration the
    -- source-level count cannot see.  `aux` is an auxiliary of a listed
    -- declaration, by parent and by shape.  `internal` is a name Lean calls
    -- internal that belongs to no listed declaration: nobody but an author
    -- writes one of those, and section 3j reports it.
    let u := (privateToUserName? n).getD n
    let priv := isPrivateName n
    let inter := u.isInternalDetail
    let vis := if !priv && !inter then "named"
               else if (auxParent listed u []).isSome then "aux"
               else if priv then "private" else "internal"
    let propTyped ← isPropType env ci.type
    IO.println s!"CONST\t{n}\t{kindOf ci}\t{vis}\t{if ci.isUnsafe then "unsafe" else "safe"}\t{if propTyped then "prop" else "data"}\t{String.intercalate "," (axs.toList.map toString)}"
    -- A numeral prints as itself whatever instance bound it, so an `OfNat`
    -- instance declared by this module is reported on its own line.  The honest
    -- file declares none; `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` is
    -- one, and it is what turns `allSubs.length = 16` into `x = x`.
    if resultHead ci.type == some ``OfNat then
      IO.println s!"OFNAT\t{n}\t{← ppStatement env ci.type}"
    -- The general form of that check.  Every constant of this module that is
    -- not a theorem reports the head its type reduces to, and every definition
    -- the head its body reduces to.  A statement prints the same whichever
    -- instance a literal or a notation went through, so what the gate can
    -- compare is the set of classes this module instantiates at all: `OfNat`
    -- for a numeral, `Neg` for a negative one, `OfScientific` for a decimal,
    -- `LT` and the arithmetic classes for the operators, `Coe` for a coercion.
    -- The honest file instantiates none of them.
    if !ci.isTheorem then
      -- Two clauses, not one list.  A head that is itself a declaration of
      -- this module — one of its own types, constructors, recursors or
      -- definitions — cannot be an instance of a class from outside it, so it
      -- is reported as `«own-constant»` and accepted as such; a reader sees
      -- which constants those are in `STATEMENTS.md`.  Every other head is
      -- compared against the set the honest file's own declarations produce.
      let ownHead : Name → Name := fun h =>
        if modNames.contains h then `«own-constant» else h
      let h := ownHead ((← unfoldedHead env ci.type).getD `«no-constant-head»)
      IO.println s!"TYPEHEAD\t{n}\t{kindOf ci}\t{h}"
      match ci with
      | .defnInfo v =>
          let bh := ownHead ((← unfoldedHead env v.value).getD `«no-constant-head»)
          IO.println s!"BODYHEAD\t{n}\t{bh}"
      | _ => pure ()
    if ci.isTheorem && vis == "named" then
      -- `none` rather than an empty field: a shell reading tab-separated
      -- records folds adjacent tabs together, and an empty column there would
      -- slide the statement into the axiom slot.
      let axStr := if axs.isEmpty then "none" else String.intercalate "," (axs.toList.map toString)
      stmts := stmts.push s!"{n}\t{axStr}\t{← ppStatement env ci.type}"
    -- A statement is only as stable as the definitions it names: changing
    -- `seed` from five points to three leaves every statement about it
    -- character for character the same and changes what all of them mean.  So
    -- the listing carries the definitions too, bodies included.
    if !ci.isTheorem && vis == "named" && kindOf ci != "ctor" && kindOf ci != "rec" then
      let body ← match ci with
        | .defnInfo v   => ppStatement env v.value
        | .opaqueInfo v => ppStatement env v.value
        | _ => pure "(no body: this constant is declared, not defined)"
      defs := defs.push s!"{n}\t{kindOf ci}\t{← ppStatement env ci.type}\t{body}"
    -- The third section of the listing.  A printed body delegates to matchers
    -- and equation lemmas that carry which arm belongs to which constructor —
    -- swap the `andF` and `orF` arms of `Fml.holds` and nothing in the first
    -- two sections moves.  These rows move.  They are also where a constant
    -- somebody hid under an internal name appears.
    if vis != "named" && kindOf ci != "ctor" && kindOf ci != "rec" then
      let body ← match ci with
        | .defnInfo v   => ppStatement env v.value
        | .opaqueInfo v => ppStatement env v.value
        | _ => pure ""
      auxs := auxs.push s!"{n}\t{kindOf ci}\t{vis}\t{← ppStatement env ci.type}\t{body}"
  IO.FS.writeFile stmtFile (String.intercalate "\n" (stmts.qsort (· < ·)).toList ++ "\n")
  IO.FS.writeFile defsFile (String.intercalate "\n" (defs.qsort (· < ·)).toList ++ "\n")
  IO.FS.writeFile auxFile (String.intercalate "\n" (auxs.qsort (· < ·)).toList ++ "\n")
  let env0 ← importModules #[{ module := `Init }] {} 0 #[] false false
  let ((), st) ← (md.constNames.forM fun n => readd env idx n).run { kenv := env0.toKernelEnv }
  IO.println s!"KERNEL added={st.added} rejected={st.errs.size}"
  for e in st.errs do IO.println s!"KERNELFAIL {e}"
  let cited ← try IO.FS.lines citedFile catch _ => pure #[]
  for line in cited do
    let cands := line.splitOn " " |>.filter (· != "")
    match cands with
    | [] => pure ()
    | first :: _ =>
      let found := cands.any fun c => (env.find? c.toName).isSome
      IO.println s!"CITED {first} {if found then "yes" else "no"}"
  IO.println "AUDIT-END"
  return 0
LEANEOF

audited_any=0
primary_audit=""
primary_stmts=""
primary_defs=""
primary_aux=""
stmt_mismatch=""
ran_short=()
for lean in "${LEANS[@]}"; do
  ver=$("$lean" --version 2>&1 | head -1 | sed -E 's/^Lean \(version ([^,]*).*/\1/')
  sysroot=$("$lean" --print-prefix 2>/dev/null)
  if [ -z "$sysroot" ] || [ ! -d "$sysroot" ]; then
    echo "FAIL: [$ver] could not determine this toolchain's own sysroot, so the"
    echo "      audit could not be run by the same toolchain that compiled."
    fail=1
    continue
  fi
  rm -rf "$WORK/out"; mkdir -p "$WORK/out"
  if ! (cd "$WORK" && "$lean" -o out/Subject.olean Subject.lean > build.log 2>&1); then
    echo "FAIL: [$ver] the file did not compile to an .olean:"
    sed 's/^/      /' "$WORK/build.log" | head -10
    fail=1
    continue
  fi
  auditlog="$WORK/audit.$ver.txt"
  (cd "$WORK" && "$lean" --run GateAudit.lean "$sysroot" out Subject cited.txt \
     "stmts.$ver.tsv" "defs.$ver.tsv" "aux.$ver.tsv") > "$auditlog" 2>&1
  audit=$(cat "$auditlog")
  if ! grep -q '^AUDIT-BEGIN$' "$auditlog" || ! grep -q '^AUDIT-END$' "$auditlog"; then
    echo "FAIL: [$ver] the audit wrapper did not run to completion.  A gate that"
    echo "      cannot perform its check has not performed it:"
    head -10 "$auditlog" | sed 's/^/      /'
    fail=1
    continue
  fi
  ran_short+=("$ver")
  nconst=$(echo "$audit" | grep -c '^CONST')
  if [ "$nconst" -lt 1 ]; then
    echo "FAIL: [$ver] the audit found no constants in the compiled module."
    fail=1
    continue
  fi
  audited_any=1
  if [ -z "$primary_audit" ]; then
    primary_audit="$audit"
    primary_stmts="$WORK/stmts.$ver.tsv"
    primary_defs="$WORK/defs.$ver.tsv"
    primary_aux="$WORK/aux.$ver.tsv"
  elif ! cmp -s "$primary_stmts" "$WORK/stmts.$ver.tsv" \
       || ! cmp -s "$primary_defs" "$WORK/defs.$ver.tsv" \
       || ! cmp -s "$primary_aux" "$WORK/aux.$ver.tsv"; then
    stmt_mismatch="$stmt_mismatch $ver"
  fi

  # Every CONST line has to be readable: seven tab-separated fields.  A name
  # carrying a tab would shift the columns, and a shifted column is a check
  # that did not happen.
  malformed=$(echo "$audit" | awk -F'\t' '/^CONST/ && NF != 7 && seen < 3 {print NR; seen++}')
  if [ -n "$malformed" ]; then
    echo "FAIL: [$ver] the audit produced CONST records this gate cannot parse."
    fail=1
  fi

  # 3a. The module header's imports.  The source text cannot reach this.
  imports=$(echo "$audit" | awk '$1 == "IMPORT" {print $2}' | sort -u)
  nonInit=$(echo "$imports" | grep -v '^Init$' | grep -v '^$')
  if [ -z "$imports" ] || [ -n "$nonInit" ]; then
    echo "FAIL: [$ver] the compiled module imports something other than Init:"
    echo "${nonInit:-  (no imports recorded at all)}" | sed 's/^/      /'
    fail=1
  fi

  # 3b. Every constant, of every kind, within the three standard axioms, by
  #     exact name.
  offenders=$(echo "$audit" | awk -F'\t' '/^CONST/ {
      n = $2; m = split($7, a, ",")
      for (i = 1; i <= m; i++) if (a[i] != "") print n "\t" a[i]
    }' | awk -F'\t' -v ok="$STANDARD_AXIOMS" '
      BEGIN { n = split(ok, A, " "); for (i = 1; i <= n; i++) S[A[i]] = 1 }
      !($2 in S)' | sort -u)
  if [ -n "$offenders" ]; then
    echo "FAIL: [$ver] constants depending on an axiom outside the standard three:"
    echo "$offenders" | sed 's/^/      /' | head -20
    fail=1
  fi

  # 3c. No axiom and no opaque declared by the module itself.
  declared=$(echo "$audit" | awk -F'\t' '/^CONST/ && ($3 == "axiom" || $3 == "opaque") {print $3 " " $2}' | sort -u)
  if [ -n "$declared" ]; then
    echo "FAIL: [$ver] the compiled module declares an axiom or an opaque constant:"
    echo "$declared" | sed 's/^/      /' | head -10
    fail=1
  fi

  # 3d. Unsafe constants.  The compiler helpers Lean generates for recursive
  #     definitions are named `<def>._unsafe_rec` and carry no proof; anything
  #     else that is unsafe is a definition the kernel never saw.
  unsafes=$(echo "$audit" | awk -F'\t' '/^CONST/ && $5 == "unsafe" {print $2}' \
            | grep -vE '\._unsafe_rec$' | sort -u)
  if [ -n "$unsafes" ]; then
    echo "FAIL: [$ver] the compiled module declares unsafe constants:"
    echo "$unsafes" | sed 's/^/      /' | head -10
    fail=1
  fi

  # 3e. A constant whose type is a Prop but which is not a theorem is a
  #     proposition proved by a definition.  This is the shape that walked past
  #     an audit which enumerated theorems only.
  #     Lean generates pattern-match auxiliaries of its own — `<name>.match_N`,
  #     `.match_N_M`, `.splitter`, `.eq_N` — and when the scrutinee is a
  #     proposition those are Prop-typed definitions nobody wrote.  They are
  #     allowed, and only when the declaration they belong to is itself a
  #     constant of this module.  A true proposition proved by a definition with
  #     one of those names proves nothing false; a false one still has to get
  #     past the axiom walk and the kernel re-add below.
  propdefs=$(echo "$audit" | awk -F'\t' '
    /^CONST/ {
      names[$2] = 1
      if ($3 != "theorem" && $6 == "prop") { k++; kind[k] = $3; nm[k] = $2 }
    }
    END {
      for (i = 1; i <= k; i++) {
        base = nm[i]; sub(/^_private\.[^.]+\.[0-9]+\./, "", base)
        if (base ~ /\.match_[0-9]+(_[0-9]+)*(\.splitter)?$/)      sub(/\.match_[0-9]+(_[0-9]+)*(\.splitter)?$/, "", base)
        else if (base ~ /\.match_[0-9]+(_[0-9]+)*\.eq_[0-9]+$/)   sub(/\.match_[0-9]+(_[0-9]+)*\.eq_[0-9]+$/, "", base)
        else { print kind[i] " " nm[i]; continue }
        if (!(base in names)) print kind[i] " " nm[i]
      }
    }' | sort -u)
  if [ -n "$propdefs" ]; then
    echo "FAIL: [$ver] the compiled module proves a proposition with something"
    echo "      that is not a theorem (a def, an abbrev or an instance):"
    echo "$propdefs" | sed 's/^/      /' | head -20
    fail=1
  fi

  # 3f. Every declaration re-added to a fresh Init-only environment through the
  #     kernel.
  kline=$(echo "$audit" | grep '^KERNEL ')
  kadded=$(echo "$kline" | sed -E 's/.*added=([0-9]+).*/\1/')
  krej=$(echo "$kline" | sed -E 's/.*rejected=([0-9]+).*/\1/')
  if [ -z "$kline" ] || ! [ "${kadded:-0}" -gt 0 ] 2>/dev/null; then
    echo "FAIL: [$ver] the kernel re-check did not run, or re-added nothing."
    fail=1
  elif [ "${krej:-1}" -ne 0 ]; then
    echo "FAIL: [$ver] the kernel rejected declarations when they were re-added"
    echo "      to a fresh Init-only environment:"
    echo "$audit" | grep '^KERNELFAIL' | sed 's/^/      /' | head -10
    fail=1
  fi

  # 3j. Nothing the listing cannot see.  Two classes of name:
  #
  #     * `private`: a declaration the source-level count cannot see, which
  #       needs no `#print axioms` line of its own.  A file published as a proof
  #       has nothing that has to be hidden from its own listing.
  #     * `internal`: a name Lean's `Name.isInternalDetail` calls internal which
  #       belongs to no listed declaration of this module.  Lean writes those
  #       underneath a declaration it generated them for; a bare `_i` or
  #       `proof_1` at the top of a module is one somebody wrote.  Version 2.2
  #       audited them and listed none of them, and
  #       `instance _i : OfNat Nat 16 := ⟨allSubs.length⟩` turned
  #       `allSubs.length = 16` into `allSubs.length = allSubs.length` with the
  #       committed listing byte-identical.  The classification is the audit
  #       program's; it accepts a name only when its parent is a non-internal
  #       constant of this module — the derived constructors and recursors
  #       included, so the parent may have no row of its own — and every
  #       component after that parent is a shape Lean's own machinery writes, so it is not keyed on the leading underscore —
  #       `proof_1` has none.
  # An author can write a name of the shape Lean generates, and the audit will
  # then class it as an auxiliary of whatever listed declaration its prefix
  # names.  Section 1g4 refuses such a name in the source; this is the same
  # question asked of the compiled module, for a name the source-level
  # extraction might have missed.
  echo "$audit" | awk -F'\t' '/^CONST/ && $4 == "aux" {print $2}' \
    | sed -E 's/^_private\.[^.]+\.[0-9]+\.//' | sort -u > "$WORK/aux_names.txt"
  forged_mod=$(comm -12 "$WORK/aux_names.txt" "$WORK/src_defs.txt"; comm -12 "$WORK/aux_names.txt" "$WORK/src_thms.txt")
  if [ -n "$forged_mod" ]; then
    echo "FAIL: [$ver] these constants carry a name of the shape Lean uses for its"
    echo "      own auxiliaries and are declared in the source, so the audit reads"
    echo "      them as generated and the listing files them among the auxiliaries:"
    echo "$forged_mod" | sort -u | sed 's/^/      /' | head -10
    fail=1
  fi

  hidden=$(echo "$audit" | awk -F'\t' '/^CONST/ && ($4 == "private" || $4 == "internal") {print $4 "  " $3 "  " $2}' | sort -u)
  if [ -n "$hidden" ]; then
    echo "FAIL: [$ver] the compiled module holds declarations that neither the"
    echo "      source-level count nor the first two sections of the statements"
    echo "      listing can see — a private declaration, or a name Lean calls"
    echo "      internal that is not an auxiliary of a listed declaration:"
    echo "$hidden" | sed 's/^/      /' | head -10
    fail=1
  fi

  # 3k. An `OfNat` instance declared by this module.
  #     Every other constant a statement elaborates through prints under its own
  #     name in the listing, because the audit loads the module without its
  #     class table.  A numeral does not: `16` prints as `16` whichever instance
  #     bound it.  So an `OfNat` instance declared here is reported by name,
  #     whether its own name is hidden or in plain sight.  The honest file
  #     declares none; its numerals are core Lean's `instOfNatNat`.
  ofnats=$(grep '^OFNAT' "$auditlog" | cut -f2,3)
  nofnat=$(grep -c '^OFNAT' "$auditlog" || true)
  if [ -n "$ofnats" ]; then
    echo "FAIL: [$ver] the compiled module declares an instance of OfNat:"
    echo "$ofnats" | sed 's/^/      /' | head -10
    echo "      A numeral in a statement prints as itself whatever instance"
    echo "      bound it, so a row of the listing reading 'Eq … 16' does not say"
    echo "      which 16 that is.  This file's numerals come from core Lean."
    fail=1
  fi

  # 3l. The same question in general: what every declaration that is not a
  #     theorem reduces to.  An `OfNat` instance behind a reducible `abbrev` has
  #     the abbrev as its head and `OfNat` as the head it reduces to; a `Neg`
  #     instance rebinds `-1` and was never within 3k's reach at all.  Both are
  #     named here, with the constant and the class, and so is every other class
  #     this file does not instantiate.
  strange=$(awk -F'\t' -v tok="$HONEST_TYPE_HEADS" -v bok="$HONEST_BODY_HEADS" '
    BEGIN { n = split(tok, A, " "); for (i = 1; i <= n; i++) T[A[i]] = 1
            m = split(bok, B, " "); for (i = 1; i <= m; i++) D[B[i]] = 1 }
    $1 == "TYPEHEAD" && !($4 in T) { print "    the type of " $2 " (" $3 ") reduces to " $4 }
    $1 == "BODYHEAD" && !($3 in D) { print "    the body of " $2 " reduces to " $3 }' \
    "$auditlog" | sort -u)
  nheads=$(grep -cE '^(TYPEHEAD|BODYHEAD)' "$auditlog" || true)
  if [ -n "$strange" ]; then
    echo "FAIL: [$ver] the compiled module declares constants whose type or body"
    echo "      reduces to something this file's own definitions never reduce to,"
    echo "      which is how an instance of a class a literal or a notation goes"
    echo "      through gets in — a numeral, a negative numeral, a decimal, an"
    echo "      operator or a coercion prints in a statement without naming the"
    echo "      instance it went through:"
    echo "$strange" | sed 's/^/  /' | head -12
    fail=1
  fi

  # 3g. No declaration into a namespace the audit wrapper itself relies on.
  reserved=$(echo "$audit" | awk -F'\t' '/^CONST/ {print $2}' \
    | grep -E '^(Lean|Init|Std|System|IO|Classical|Quot)\.' | sort -u)
  if [ -n "$reserved" ]; then
    echo "FAIL: [$ver] the file declares into a core namespace:"
    echo "$reserved" | sed 's/^/      /' | head -10
    fail=1
  fi

  # 3h. The theorems in the compiled module are exactly the ones the source
  #     declares, plus the lemma shapes Lean generates for itself.
  echo "$audit" | awk -F'\t' '/^CONST/ && $3 == "theorem" && $4 == "named" {print $2}' | sort -u > "$WORK/mod_thms.txt"
  extra=$(comm -13 "$WORK/src_thms.txt" "$WORK/mod_thms.txt" | grep -vE "$GENERATED_SHAPES")
  missing=$(comm -23 "$WORK/src_thms.txt" "$WORK/mod_thms.txt")
  if [ -n "$extra" ]; then
    echo "FAIL: [$ver] the compiled module holds theorems the source does not declare:"
    echo "$extra" | sed 's/^/      /' | head -20
    fail=1
  fi
  if [ -n "$missing" ]; then
    echo "FAIL: [$ver] the source declares theorems the compiled module does not hold"
    echo "      (a theorem that was never elaborated is not a theorem):"
    echo "$missing" | sed 's/^/      /' | head -20
    fail=1
  fi
  nmodthm=$(wc -l < "$WORK/mod_thms.txt" | tr -d ' ')
  naux_ver=$(echo "$audit" | awk -F'\t' '/^CONST/ && $4 == "aux"' | wc -l | tr -d ' ')
  npriv_ver=$(echo "$audit" | awk -F'\t' '/^CONST/ && $4 == "private"' | wc -l | tr -d ' ')
  nint_ver=$(echo "$audit" | awk -F'\t' '/^CONST/ && $4 == "internal"' | wc -l | tr -d ' ')
  echo "  [$ver] constants audited: $nconst ; theorems: $nmodthm (source declares $nthm) ;"
  echo "         kernel re-added ${kadded:-0} declarations into a fresh Init environment, ${krej:-?} rejected"
  echo "         names Lean calls internal: $naux_ver auxiliaries of a listed declaration,"
  echo "         $nint_ver belonging to none ; private declarations: $npriv_ver ; declaration"
  echo "         heads outside this file's own set: $(echo "$strange" | grep -c . || true) of $nheads read"
done

if [ "$audited_any" -eq 0 ]; then
  echo "FAIL: the compiled-module audit did not run under any toolchain."
  fail=1
fi
if [ -n "$stmt_mismatch" ]; then
  echo "FAIL: the statement listing came out differently under:$stmt_mismatch"
  fail=1
fi

in_window=1
for v in ${ran_short[@]+"${ran_short[@]}"}; do
  printf '%s\n' "$v" | grep -qE "$LISTING_WINDOW" || in_window=0
done

# 3i. Every Lean name the README cites in backticks exists.
if [ -n "$primary_audit" ]; then
  unknown=$(echo "$primary_audit" | awk '$1 == "CITED" && $3 == "no" {print $2}' | sort -u)
  ncheck=$(echo "$primary_audit" | grep -c '^CITED ')
  if [ "$ncheck" -ne "$ncited" ]; then
    echo "FAIL: the README name check covered $ncheck of $ncited names."
    fail=1
  fi
  # A check over zero names reports the same `all resolve: yes` as a check that
  # found every name.  With the README argument misspelled, that is what version
  # 2.2 printed, and the gate passed.
  if [ "$ncited" -eq 0 ]; then
    echo "FAIL: the README named on the command line cites no Lean names in"
    echo "      backticks at all, so section 3i checked nothing.  A check over"
    echo "      no names is not a check that passed."
    fail=1
  fi
  if [ -n "$unknown" ]; then
    echo "FAIL: the README cites Lean names in backticks that do not exist:"
    echo "$unknown" | sed 's/^/      /' | head -20
    fail=1
  fi
  echo "  README names checked: $ncheck ; all resolve: $([ -z "$unknown" ] && echo yes || echo no)"
fi

echo
echo "=== 4. the file's own footprint, checked against the audit ==="

# What the file says about itself, normalised.
echo "$primary_out" | grep -E "^'" \
  | sed -E "s/^'([^']*)' does not depend on any axioms.*/\1\t/; \
            s/^'([^']*)' depends on axioms: \[(.*)\].*/\1\t\2/" \
  | sed 's/, /,/g' | sort -u > "$WORK/claimed.txt"
# What the compiled module actually contains, for those same theorems.
echo "$primary_audit" | awk -F'\t' '/^CONST/ && $3 == "theorem" && $4 == "named" {print $2 "\t" $7}' | sort -u > "$WORK/actual_all.txt"
join -t $'\t' "$WORK/src_thms.txt" "$WORK/actual_all.txt" 2>/dev/null | sort -u > "$WORK/actual.txt"

nclaimed=$(wc -l < "$WORK/claimed.txt" | tr -d ' ')
if [ "$nclaimed" -ne "$nthm" ]; then
  echo "FAIL: the file printed $nclaimed axiom lines for $nthm declared theorems."
  fail=1
fi
disagree=$(comm -3 "$WORK/claimed.txt" "$WORK/actual.txt")
if [ -n "$disagree" ]; then
  echo "FAIL: the footprint the file prints disagrees with the compiled module."
  echo "      Lines the file claims, then what the module holds:"
  echo "$disagree" | sed 's/^/      /' | head -20
  fail=1
else
  echo "  the file's $nclaimed printed axiom lines agree with the compiled module."
fi

echo
echo "=== 5. the statements listing ==="

# STATEMENTS.md is the companion to this gate.  The gate reads how each theorem
# was proved; that file is where a reader reads what each theorem says.  It is
# regenerated here from the compiled module and compared with the committed
# copy, so the two cannot drift apart.
#
# Three sections since 2.3.  The theorems and the definitions are what 2.2
# wrote.  The third is the constants Lean generates underneath those
# definitions — matchers, their splitters, equation lemmas, proof terms — and it
# exists because the printed body of a definition made by pattern matching
# delegates to them: swapping the `andF` and `orF` arms of `Fml.holds` moved
# nothing in 2.2's listing, and moves `Fml.holds.eq_4` and `Fml.holds.eq_5`
# here.  It is also where a declaration hidden under an internal name would
# appear, which is the second half of the answer to that attack; section 3j is
# the first.
if [ -n "$primary_stmts" ] && [ -s "$primary_stmts" ] && [ -n "$primary_defs" ] && [ -s "$primary_defs" ] \
   && [ -n "$primary_aux" ] && [ -s "$primary_aux" ]; then
  nstmt=$(wc -l < "$primary_stmts" | tr -d ' ')
  ndef=$(wc -l < "$primary_defs" | tr -d ' ')
  naux=$(wc -l < "$primary_aux" | tr -d ' ')
  {
    echo "# STATEMENTS.md — what each theorem says"
    echo
    echo "Written by \`check.sh\`, regenerated on every run and compared with the"
    echo "committed copy; the gate fails if the two differ.  The gate checks how"
    echo "the proofs were made.  This file is where a reader checks what they"
    echo "claim, which is the part no script can check."
    echo
    echo "Each row of the first section is a theorem of the compiled module: its"
    echo "name, the axioms it depends on (computed by walking the compiled"
    echo "environment, not read from anything the file printed), and its"
    echo "elaborated statement."
    echo
    echo "Statements are printed as plain constant applications — \`Eq a b\` rather"
    echo "than \`a = b\`, \`And p q\` rather than \`p ∧ q\`.  That is not a style"
    echo "choice.  The audit loads the module with its environment extensions"
    echo "unloaded and sets \`pp.notation false\`, so no \`notation\`, no user"
    echo "delaborator and no unexpander runs while these are printed: a"
    echo "\`notation\` that renames a constant — the trick that makes a theorem"
    echo "about \`Z_fakeDet\` read as one about \`Move.det\` — cannot change how a"
    echo "statement reads here.  Lean's own builtin delaborators do run, which is"
    echo "why binders, \`fun\` and field notation (\`f.holds r\`) appear; and with"
    echo "the class table unloaded an instance projection prints under its own"
    echo "name (\`List.instMembership.mem L q\`) rather than as \`Membership.mem\`."
    echo "A reader who regenerates a row with \`#check @name\` under"
    echo "\`pp.notation false\` gets the same statement in their own session's"
    echo "spelling of those two things."
    echo
    echo "What a row does not carry.  The instance a numeral elaborated through"
    echo "is not visible in it: \`16\` prints as \`16\` whichever \`OfNat\` instance"
    echo "bound it, which is why the gate reports separately that this module"
    echo "declares none.  The constructors of an inductive are not rows of their"
    echo "own; each inductive's row says \"(no body: declared, not defined)\" and"
    echo "its constructors appear in the type of its \`casesOn\`.  Neither are the"
    echo "constants from \`Init\` that the statements rest on."
    echo
    echo "Theorems listed: $nstmt.  Rows marked (generated) are the lemma shapes"
    echo "Lean derives for \`inductive\`, \`structure\` and \`deriving\`; the rest are"
    echo "declared in the source.  The definitions those statements are written"
    echo "in terms of follow, with their bodies, in the second section: a"
    echo "statement is only as stable as the definitions it names, and changing"
    echo "\`seed\` from five points to three would leave every statement about it"
    echo "character for character the same while changing what all of them mean."
    echo "The third section carries the auxiliaries Lean generates underneath"
    echo "those definitions."
    echo
    echo "Toolchain window.  This listing is byte-identical under Lean 4.32.2,"
    echo "4.33.0 and 4.33.1, the three the gate runs, and under 4.30.0-rc2,"
    echo "4.31.0 and 4.32.0.  Lean 4.34 stops generating two of the definitions"
    echo "in the second section (\`Move.toCtorIdx\` and \`Sq.toCtorIdx\`), so a run"
    echo "under 4.34 or later regenerates a listing that differs in those rows"
    echo "and in the count beside them.  The theorems and the auxiliaries are"
    echo "unchanged there, and so are the proofs."
    echo
    echo "## Theorems"
    echo
    while IFS=$'\t' read -r nm axs stmt; do
      [ -z "$nm" ] && continue
      if grep -qxF "$nm" "$WORK/src_thms.txt"; then mark=""; else mark=" (generated)"; fi
      echo "## \`$nm\`$mark"
      echo
      echo "axioms: $axs"
      echo
      echo '```'
      echo "$stmt"
      echo '```'
      echo
    done < "$primary_stmts"
    echo "## Definitions"
    echo
    echo "Every constant of the compiled module that is not a theorem and that"
    echo "Lean does not call internal, other than the constructors and recursors"
    echo "it derives: its kind, its type and its body."
    echo
    echo "Definitions listed: $ndef."
    echo
    while IFS=$'\t' read -r nm knd typ body; do
      [ -z "$nm" ] && continue
      echo "### \`$nm\`  ($knd)"
      echo
      echo '```'
      echo "$typ"
      echo ":="
      echo "$body"
      echo '```'
      echo
    done < "$primary_defs"
    echo "## Generated auxiliaries"
    echo
    echo "Every remaining constant of the compiled module: the names Lean"
    echo "generates underneath the declarations above — the matchers a definition"
    echo "by cases compiles to, their splitters, the equation lemmas, the proof"
    echo "terms a tactic left behind, the \`sizeOf\` helpers.  Each row carries the"
    echo "name, the kind, the class the gate put the name in (\`aux\` for an"
    echo "auxiliary of a declaration of this module that Lean does not call"
    echo "internal; \`internal\` or \`private\` for a name that belongs to no such"
    echo "declaration, which the gate also reports as a failure), and the"
    echo "statement or the body.  The parent of an \`aux\` name is sometimes a"
    echo "constructor or a recursor Lean derived, which has no row of its own,"
    echo "so the set a parent is looked for in is wider than the rows above."
    echo
    echo "Names under \`_private.Subject.0.\` are Lean's encoding of a private"
    echo "declaration: the prefix marks it private, the \`0\` is Lean's hash field"
    echo "and \`Subject\` is the module name, which is the fixed name the gate"
    echo "compiles the file under.  121 of the rows below are Lean's own private"
    echo "equation lemmas for matchers, generated and named that way by Lean"
    echo "itself; the file declares nothing private."
    echo
    echo "The equation lemmas are the readable ones, and the reason this section"
    echo "exists.  The printed body of a definition written by pattern matching"
    echo "is a \`brecOn\` applied to a matcher, so which arm belongs to which"
    echo "constructor is not legible in the second section; \`Fml.holds.eq_4\` says"
    echo "it outright.  A reviewer swapped the \`andF\` and \`orF\` arms of"
    echo "\`Fml.holds\` and nothing in the first two sections changed.  Ten rows"
    echo "of this section change under that swap.  Where a reader regenerates"
    echo "this listing from a swapped file rather than comparing against the"
    echo "committed one, the run is green and the listing it writes carries the"
    echo "swap: that is a limit of regenerating, and the reason the committed"
    echo "copy is the one the gate compares against."
    echo
    echo "Auxiliaries listed: $naux."
    echo
    while IFS=$'\t' read -r nm knd cls typ body; do
      [ -z "$nm" ] && continue
      echo "### \`$nm\`  ($knd, $cls)"
      echo
      echo '```'
      echo "$typ"
      if [ -n "$body" ]; then
        echo ":="
        echo "$body"
      fi
      echo '```'
      echo
    done < "$primary_aux"
  } > "$WORK/STATEMENTS.md"

  # The regenerated copy goes beside the listing it was compared with, not into
  # whatever directory the gate was invoked from, and the gate says whether that
  # write worked rather than assuming it.
  REGEN="$(dirname "$STATEMENTS")/$(basename "$STATEMENTS").regenerated"
  leave_regenerated() {
    if cp "$WORK/STATEMENTS.md" "$REGEN" 2>/dev/null; then
      echo "      The listing this run produced has been left at $REGEN"
    else
      echo "      The listing this run produced could not be written beside"
      echo "      $STATEMENTS — that directory is not writable — so it is gone"
      echo "      with this run's working directory."
    fi
  }

  if [ "$WRITE_STATEMENTS" -eq 1 ]; then
    cp "$WORK/STATEMENTS.md" "$STATEMENTS"
    echo "  wrote $STATEMENTS ($nstmt theorems, $ndef definitions, $naux"
    echo "  generated auxiliaries).  Re-run without --write-statements to check it."
  elif [ ! -f "$STATEMENTS" ]; then
    echo "FAIL: there is no $STATEMENTS to compare against."
    leave_regenerated
    fail=1
  elif cmp -s "$WORK/STATEMENTS.md" "$STATEMENTS"; then
    echo "  $STATEMENTS matches the listing regenerated from the compiled module"
    echo "  ($nstmt theorems, $ndef definitions, $naux generated auxiliaries)."
  else
    # A difference confined to rows for definitions Lean generates, under a
    # toolchain this gate does not list, is drift and not tampering.  Both sides
    # are then compared with those rows dropped and the count beside them
    # normalised; what that leaves uncompared is printed, because a narrower
    # comparison that does not say so is worse than a failure.
    filter_listing() {
      awk -v srcdefs="$WORK/src_defs.txt" '
        BEGIN { while ((getline l < srcdefs) > 0) declared[l] = 1; sect = "head"; skip = 0 }
        /^## Theorems$/              { sect = "thm"; skip = 0 }
        /^## Definitions$/           { sect = "def"; skip = 0 }
        /^## Generated auxiliaries$/ { sect = "aux"; skip = 0 }
        sect == "def" && /^### `/ {
          n = $0; sub(/^### `/, "", n); sub(/`.*$/, "", n)
          skip = (n in declared) ? 0 : 1
        }
        {
          if (skip) next
          line = $0
          if (line ~ /^Definitions listed: [0-9]+\.$/) line = "Definitions listed: N."
          print line
        }' "$1"
    }
    drift=0
    if [ "$in_window" -eq 0 ]; then
      filter_listing "$STATEMENTS"           > "$WORK/committed.filtered"
      filter_listing "$WORK/STATEMENTS.md"   > "$WORK/regen.filtered"
      cmp -s "$WORK/committed.filtered" "$WORK/regen.filtered" && drift=1
    fi
    if [ "$drift" -eq 1 ]; then
      drift_noted=1
      echo "  $STATEMENTS differs from the listing regenerated here, and the"
      echo "  difference is confined to rows for definitions Lean generates,"
      echo "  under a toolchain this gate does not list (${ran_short[*]})."
      echo "  That is toolchain drift, not tampering: Lean 4.34 stopped"
      echo "  generating Move.toCtorIdx and Sq.toCtorIdx, and an honest file"
      echo "  cannot do anything about it.  Compared and matching: the $nstmt"
      echo "  theorem rows, the definitions this file declares, and the $naux"
      echo "  generated auxiliaries.  Not compared: rows for definitions Lean"
      echo "  generates, and the count beside them.  A run under 4.32.2, 4.33.0"
      echo "  or 4.33.1 compares those too; the regenerated listing is below."
      leave_regenerated
    else
      echo "FAIL: $STATEMENTS differs from the listing regenerated from the compiled"
      echo "      module.  Either a statement changed without the listing being"
      echo "      updated, or the listing was edited by hand."
      leave_regenerated
      echo "      First differences:"
      diff "$STATEMENTS" "$WORK/STATEMENTS.md" | head -20 | sed 's/^/      /'
      fail=1
    fi
  fi
else
  echo "FAIL: no statement listing was produced, so there was nothing to compare."
  fail=1
fi

echo "=== 6. axiom footprint (from the compiled module) ==="
echo "$primary_audit" | awk -F'\t' '/^CONST/ && $3 == "theorem" && $4 == "named" {
    if ($7 == "") printf "  %-45s no axioms\n", $2; else printf "  %-45s %s\n", $2, $7 }' \
  | sort || { echo "FAIL: no audited footprint to print."; fail=1; }

echo
echo "=== 7. summary ==="
clean=$(awk -F'\t' '$2 == ""' "$WORK/actual.txt" | wc -l | tr -d ' ')
withax=$(awk -F'\t' '$2 != ""' "$WORK/actual.txt" | wc -l | tr -d ' ')
echo "  theorems depending on no axioms at all : $clean"
echo "  theorems depending on standard axioms  : $withax"
echo "  theorems audited in the compiled module: $((clean + withax))  (source declares: $nthm)"
echo "  (the standard three are propext, Classical.choice and Quot.sound, which"
echo "   come in through simp, omega and the classical symmetry set in S1; none"
echo "   of them is specific to this file)"

if [ "$((clean + withax))" -ne "$nthm" ]; then
  echo "FAIL: $((clean + withax)) theorems audited but $nthm declared."
  fail=1
fi

echo
echo "  toolchains run (${#LEANS[@]} of ${#TOOLCHAIN_PATHS[@]} listed, source: $TOOLCHAIN_SOURCE):"
for v in "${ran_versions[@]}"; do echo "    $v"; done
echo "  (the version, commit and platform strings above are this machine's.  On"
echo "   another platform the target triple differs; on another build of the same"
echo "   release the commit does not.  Compare the counts and the verdict, not"
echo "   those lines.)"

echo
if [ "$fail" -eq 0 ]; then
  if [ "$TOOLCHAIN_SOURCE" = "listed" ] && [ "${#LEANS[@]}" -eq "${#TOOLCHAIN_PATHS[@]}" ]; then
    echo "OK: $FILE checks green under all ${#TOOLCHAIN_PATHS[@]} listed toolchains, with no sorry,"
  else
    if [ "${#LEANS[@]}" -eq 1 ]; then
      echo "OK: $FILE checks green under the 1 toolchain that ran (listed above;"
    else
      echo "OK: $FILE checks green under the ${#LEANS[@]} toolchains that ran (listed above;"
    fi
    echo "    not all ${#TOOLCHAIN_PATHS[@]} of the versions this gate names), with no sorry,"
  fi
  echo "    no added axiom, no command outside the allowlist and none of the"
  echo "    refused commands anywhere on a line, no declaration hidden from the"
  echo "    listing under an internal name, no OfNat instance of its own, every"
  echo "    declaration re-checked by the kernel in a fresh Init-only"
  echo "    environment, and a footprint read from the compiled module rather"
  echo "    than from the file's own output."
  if [ "$drift_noted" -eq 1 ]; then
    echo "    The statements listing was compared with the rows for definitions"
    echo "    Lean generates left out, because the toolchain that ran is outside"
    echo "    the window the listing was written in; section 5 says which rows."
  fi
else
  echo "FAILED."
fi
exit "$fail"
