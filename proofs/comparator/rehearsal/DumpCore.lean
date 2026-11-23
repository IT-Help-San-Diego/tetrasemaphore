import Lean
/-!
  Dump the seventeen statements, and every constant they use from this module, in the shape the
  judge compares: `Lean.Expr.eqv` (alpha-equivalence; binder names and binder annotations ignored),
  on the stored type of each theorem and on type and value of each definition in the closure.
  Run twice, once importing `Challenge` and once `TetrasemaphoreAlgebra`, and diff the output.
-/
open Lean Meta

namespace Dump

/-- Erase what `Expr.eqv` ignores: binder names, binder annotations, metadata. -/
partial def canon : Expr → Expr
  | .forallE _ t b _ => .forallE .anonymous (canon t) (canon b) .default
  | .lam _ t b _     => .lam .anonymous (canon t) (canon b) .default
  | .letE _ t v b nd => .letE .anonymous (canon t) (canon v) (canon b) nd
  | .app f a         => .app (canon f) (canon a)
  | .mdata _ e       => canon e
  | .proj n i e      => .proj n i (canon e)
  | e                => e

def theoremNames : List Name :=
  [`Move.act_mul, `T1_self_inverse, `T1_mul_comm, `T1_mem_all, `T1_all_distinct,
   `T2_faithful, `T4_fix_I, `T4_fix_sv, `T4_fix_sh, `T4_fix_C2, `T7_both_mirrors,
   `T8_five_are, `S1_one_of_five, `S2_mark_sv_exact, `S2_mark_sh_exact, `S2_mark_C2_exact,
   `S2_markAll_invariant]

def hintsStr : ReducibilityHints → String
  | .opaque => "opaque" | .abbrev => "abbrev" | .regular h => s!"regular {h}"

def safetyStr : DefinitionSafety → String
  | .unsafe => "unsafe" | .safe => "safe" | .partial => "partial"

def kind : ConstantInfo → String
  | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "recursor"

/-- The constants a constant's type and value use, as the judge walks them. -/
def used (ci : ConstantInfo) : Array Name := Id.run do
  let mut s := ci.type.getUsedConstants
  if let some v := ci.value? (allowOpaque := true) then s := s ++ v.getUsedConstants
  match ci with
  | .inductInfo i => s := s ++ i.ctors.toArray ++ i.all.toArray
  | .ctorInfo c => s := s.push c.induct
  | .recInfo r => for rule in r.rules do s := s.push rule.ctor ++ rule.rhs.getUsedConstants
  | _ => pure ()
  return s

def dump (modName : Name) : MetaM Unit := do
  let env ← getEnv
  let inModule (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some idx => env.header.moduleNames[idx.toNat]! == modName
    | none => false
  IO.println s!"# statements of module {modName}"
  for n in theoremNames do
    match env.find? n with
    | none => IO.println s!"## {n}\nMISSING"
    | some ci =>
      IO.println s!"## {n}  ({kind ci}; levelParams {ci.levelParams})"
      IO.println s!"pp:    {← ppExpr ci.type}"
      IO.println s!"canon: {repr (canon ci.type)}"
  -- the closure inside this module, as the judge's worklist would see it
  IO.println s!"# closure inside {modName} (type and value, canonical)"
  let mut work : Array Name := #[]
  for n in theoremNames do
    if let some ci := env.find? n then work := work ++ ci.type.getUsedConstants
  let mut seen : Std.HashSet Name := {}
  let mut rows : Array (Name × String) := #[]
  while !work.isEmpty do
    let n := work.back!
    work := work.pop
    if seen.contains n then continue
    seen := seen.insert n
    if !inModule n then continue
    let some ci := env.find? n | continue
    let val := match ci.value? (allowOpaque := true) with
      | some v => s!"\n  value: {repr (canon v)}"
      | none => ""
    let extra := match ci with
      | .defnInfo d => s!" hints={hintsStr d.hints} safety={safetyStr d.safety}"
      | .inductInfo i => s!" numParams={i.numParams} numIndices={i.numIndices} ctors={i.ctors} all={i.all} isRec={i.isRec} isUnsafe={i.isUnsafe} isReflexive={i.isReflexive}"
      | .ctorInfo c => s!" induct={c.induct} cidx={c.cidx} numParams={c.numParams} numFields={c.numFields}"
      | .recInfo r => s!" numParams={r.numParams} numIndices={r.numIndices} numMotives={r.numMotives} numMinors={r.numMinors} k={r.k} rules={r.rules.map fun (rl : RecursorRule) => (rl.ctor, rl.nfields)}"
      | _ => ""
    rows := rows.push (n, s!"## {n}  ({kind ci}{extra})\n  type: {repr (canon ci.type)}{val}")
    work := work ++ used ci
  for (_, row) in rows.qsort (fun a b => a.1.toString < b.1.toString) do
    IO.println row
  IO.println s!"# {rows.size} constants of {modName} in the closure"

end Dump
