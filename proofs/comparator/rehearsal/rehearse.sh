#!/usr/bin/env bash
# A local rehearsal of the judge's statement comparison, without the judge.
#
# Compiles Challenge.lean (this folder's parent) and the published proofs/TetrasemaphoreAlgebra.lean with
# the Lean the proofs pin (4.33.0, from the lean-toolchain file here), then prints, for each of the
# seventeen theorems, its stored statement in the form `lake comparator` compares (Lean.Expr.eqv: binder
# names and binder annotations erased, nothing unfolded), together with every constant of the module the
# statements use, and diffs the two listings.  An empty diff means the judge's `compare_statements` step
# should pass; a non-empty diff names the statement (or definition) that differs.
#
# It is not the judge: no sandbox, no kernel replay of an export, no axiom check.  Run from anywhere.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
comp="$(cd "$here/.." && pwd)"            # proofs/comparator
proofs="$(cd "$comp/.." && pwd)"          # proofs
out="${REHEARSAL_OUT:-$here/.out}"
rm -rf "$out"; mkdir -p "$out"
cd "$here"
# every lean call below names its toolchain explicitly (elan's `+toolchain` form), so the rehearsal
# never falls back to elan's default toolchain, whatever folder it is run from
tc="+$(tr -d '[:space:]' < "$here/lean-toolchain")"
echo "lean: $(lean "$tc" --version)"
lean "$tc" -o "$out/DumpCore.olean" DumpCore.lean
( cd "$comp"   && lean "$tc" -o "$out/Challenge.olean" Challenge.lean | grep -v -E "declaration uses .sorry." || true )
( cd "$proofs" && lean "$tc" -o "$out/TetrasemaphoreAlgebra.olean" TetrasemaphoreAlgebra.lean | grep -v -E "does not depend on any axioms|depends on axioms" || true )
LEAN_PATH="$out" lean "$tc" DumpChallenge.lean > "$out/challenge.txt" || { cat "$out/challenge.txt"; exit 2; }
LEAN_PATH="$out" lean "$tc" DumpPublished.lean > "$out/published.txt" || { cat "$out/published.txt"; exit 2; }
# the module name is the only expected difference in the headers
sed -i.bak 's/module Challenge/module MODULE/; s/inside Challenge/inside MODULE/; s/of Challenge in/of MODULE in/' "$out/challenge.txt"
sed -i.bak 's/module TetrasemaphoreAlgebra/module MODULE/; s/inside TetrasemaphoreAlgebra/inside MODULE/; s/of TetrasemaphoreAlgebra in/of MODULE in/' "$out/published.txt"
echo "statements and closure constants listed: $(grep -c '^## ' "$out/published.txt") (published), $(grep -c '^## ' "$out/challenge.txt") (challenge)"
if diff -u "$out/published.txt" "$out/challenge.txt" > "$out/diff.txt"; then
  echo "REHEARSAL: no difference in the seventeen statements or their definitions (as Expr.eqv sees them)"
else
  echo "REHEARSAL: differences found; see $out/diff.txt"
  grep -E '^[-+]## |^[-+]canon:|^[-+]pp:|^[-+]  type:|^[-+]  value:|^[-+]MISSING' "$out/diff.txt" | cut -c1-200 || true
  exit 1
fi
