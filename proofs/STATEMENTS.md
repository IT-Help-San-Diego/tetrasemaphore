# STATEMENTS.md — what each theorem says

Written by `check.sh`, regenerated on every run and compared with the
committed copy; the gate fails if the two differ.  The gate checks how
the proofs were made.  This file is where a reader checks what they
claim, which is the part no script can check.

Each row of the first section is a theorem of the compiled module: its
name, the axioms it depends on (computed by walking the compiled
environment, not read from anything the file printed), and its
elaborated statement.

Statements are printed as plain constant applications — `Eq a b` rather
than `a = b`, `And p q` rather than `p ∧ q`.  That is not a style
choice.  The audit loads the module with its environment extensions
unloaded and sets `pp.notation false`, so no `notation`, no user
delaborator and no unexpander runs while these are printed: a
`notation` that renames a constant — the trick that makes a theorem
about `Z_fakeDet` read as one about `Move.det` — cannot change how a
statement reads here.  Lean's own builtin delaborators do run, which is
why binders, `fun` and field notation (`f.holds r`) appear; and with
the class table unloaded an instance projection prints under its own
name (`List.instMembership.mem L q`) rather than as `Membership.mem`.
A reader who regenerates a row with `#check @name` under
`pp.notation false` gets the same statement in their own session's
spelling of those two things.

What a row does not carry.  The instance a numeral elaborated through
is not visible in it: `16` prints as `16` whichever `OfNat` instance
bound it, which is why the gate reports separately that this module
declares none.  The constructors of an inductive are not rows of their
own; each inductive's row says "(no body: declared, not defined)" and
its constructors appear in the type of its `casesOn`.  Neither are the
constants from `Init` that the statements rest on.

Theorems listed: 164.  Rows marked (generated) are the lemma shapes
Lean derives for `inductive`, `structure` and `deriving`; the rest are
declared in the source.  The definitions those statements are written
in terms of follow, with their bodies, in the second section: a
statement is only as stable as the definitions it names, and changing
`seed` from five points to three would leave every statement about it
character for character the same while changing what all of them mean.
The third section carries the auxiliaries Lean generates underneath
those definitions.

Toolchain window.  This listing is byte-identical under Lean 4.32.2,
4.33.0 and 4.33.1, the three the gate runs, and under 4.30.0-rc2,
4.31.0 and 4.32.0.  Lean 4.34 stops generating two of the definitions
in the second section (`Move.toCtorIdx` and `Sq.toCtorIdx`), so a run
under 4.34 or later regenerates a listing that differs in those rows
and in the count beside them.  The theorems and the auxiliaries are
unchanged there, and so are the proofs.

## Theorems

## `Fml.allF.inj` (generated)

axioms: none

```
∀ {n : Nat} {f : Fml} {n_1 : Nat} {f_1 : Fml}, Eq (Fml.allF n f) (Fml.allF n_1 f_1) → And (Eq n n_1) (Eq f f_1)
```

## `Fml.allF.injEq` (generated)

axioms: propext

```
∀ (n : Nat) (f : Fml) (n_1 : Nat) (f_1 : Fml), Eq (Eq (Fml.allF n f) (Fml.allF n_1 f_1)) (And (Eq n n_1) (Eq f f_1))
```

## `Fml.allF.sizeOf_spec` (generated)

axioms: none

```
∀ (n : Nat) (f : Fml), Eq (Fml._sizeOf_inst.sizeOf (Fml.allF n f)) (instHAdd.hAdd (instHAdd.hAdd 1 (instSizeOfNat.sizeOf n)) (Fml._sizeOf_inst.sizeOf f))
```

## `Fml.andF.inj` (generated)

axioms: none

```
∀ {f g f_1 g_1 : Fml}, Eq (f.andF g) (f_1.andF g_1) → And (Eq f f_1) (Eq g g_1)
```

## `Fml.andF.injEq` (generated)

axioms: propext

```
∀ (f g f_1 g_1 : Fml), Eq (Eq (f.andF g) (f_1.andF g_1)) (And (Eq f f_1) (Eq g g_1))
```

## `Fml.andF.sizeOf_spec` (generated)

axioms: none

```
∀ (f g : Fml), Eq (Fml._sizeOf_inst.sizeOf (f.andF g)) (instHAdd.hAdd (instHAdd.hAdd 1 (Fml._sizeOf_inst.sizeOf f)) (Fml._sizeOf_inst.sizeOf g))
```

## `Fml.brecOn.eq` (generated)

axioms: none

```
∀ {motive : Fml → Sort u} (t : Fml) (F_1 : (t : Fml) → Fml.below t → motive t), Eq (Fml.brecOn t F_1) (F_1 t (Fml.brecOn.go t F_1).2)
```

## `Fml.detT.inj` (generated)

axioms: none

```
∀ {s t s_1 t_1 : Tm}, Eq (Fml.detT s t) (Fml.detT s_1 t_1) → And (Eq s s_1) (Eq t t_1)
```

## `Fml.detT.injEq` (generated)

axioms: propext

```
∀ (s t s_1 t_1 : Tm), Eq (Eq (Fml.detT s t) (Fml.detT s_1 t_1)) (And (Eq s s_1) (Eq t t_1))
```

## `Fml.detT.sizeOf_spec` (generated)

axioms: none

```
∀ (s t : Tm), Eq (Fml._sizeOf_inst.sizeOf (Fml.detT s t)) (instHAdd.hAdd (instHAdd.hAdd 1 (Tm._sizeOf_inst.sizeOf s)) (Tm._sizeOf_inst.sizeOf t))
```

## `Fml.eqT.inj` (generated)

axioms: none

```
∀ {s t s_1 t_1 : Tm}, Eq (Fml.eqT s t) (Fml.eqT s_1 t_1) → And (Eq s s_1) (Eq t t_1)
```

## `Fml.eqT.injEq` (generated)

axioms: propext

```
∀ (s t s_1 t_1 : Tm), Eq (Eq (Fml.eqT s t) (Fml.eqT s_1 t_1)) (And (Eq s s_1) (Eq t t_1))
```

## `Fml.eqT.sizeOf_spec` (generated)

axioms: none

```
∀ (s t : Tm), Eq (Fml._sizeOf_inst.sizeOf (Fml.eqT s t)) (instHAdd.hAdd (instHAdd.hAdd 1 (Tm._sizeOf_inst.sizeOf s)) (Tm._sizeOf_inst.sizeOf t))
```

## `Fml.holds.eq_def` (generated)

axioms: none

```
∀ (x : Fml) (x_1 : Nat → Move), Eq (x.holds x_1) (Fml.holds.match_1 (fun x x_2 ↦ Prop) x x_1 (fun s t r ↦ Eq (s.eval r) (t.eval r)) (fun s t r ↦ Eq (s.eval r).det (t.eval r).det) (fun f r ↦ Not (f.holds r)) (fun f g r ↦ And (f.holds r) (g.holds r)) (fun f g r ↦ Or (f.holds r) (g.holds r)) fun n f r ↦ ∀ (m : Move), f.holds fun k ↦ ite (Eq k n) m (r k))
```

## `Fml.neg.inj` (generated)

axioms: none

```
∀ {f f_1 : Fml}, Eq f.neg f_1.neg → Eq f f_1
```

## `Fml.neg.injEq` (generated)

axioms: propext

```
∀ (f f_1 : Fml), Eq (Eq f.neg f_1.neg) (Eq f f_1)
```

## `Fml.neg.sizeOf_spec` (generated)

axioms: none

```
∀ (f : Fml), Eq (Fml._sizeOf_inst.sizeOf f.neg) (instHAdd.hAdd 1 (Fml._sizeOf_inst.sizeOf f))
```

## `Fml.orF.inj` (generated)

axioms: none

```
∀ {f g f_1 g_1 : Fml}, Eq (f.orF g) (f_1.orF g_1) → And (Eq f f_1) (Eq g g_1)
```

## `Fml.orF.injEq` (generated)

axioms: propext

```
∀ (f g f_1 g_1 : Fml), Eq (Eq (f.orF g) (f_1.orF g_1)) (And (Eq f f_1) (Eq g g_1))
```

## `Fml.orF.sizeOf_spec` (generated)

axioms: none

```
∀ (f g : Fml), Eq (Fml._sizeOf_inst.sizeOf (f.orF g)) (instHAdd.hAdd (instHAdd.hAdd 1 (Fml._sizeOf_inst.sizeOf f)) (Fml._sizeOf_inst.sizeOf g))
```

## `Move.C2.sizeOf_spec` (generated)

axioms: none

```
Eq (Move._sizeOf_inst.sizeOf Move.C2) 1
```

## `Move.I.sizeOf_spec` (generated)

axioms: none

```
Eq (Move._sizeOf_inst.sizeOf Move.I) 1
```

## `Move.act_C2`

axioms: none

```
∀ (x y : Int), Eq (Move.C2.act { fst := x, snd := y }) { fst := Int.instNegInt.neg x, snd := Int.instNegInt.neg y }
```

## `Move.act_I`

axioms: none

```
∀ (p : Pt), Eq (Move.I.act p) p
```

## `Move.act_mul`

axioms: propext

```
∀ (g h : Move) (p : Pt), Eq ((g.mul h).act p) (g.act (h.act p))
```

## `Move.act_sh`

axioms: none

```
∀ (x y : Int), Eq (Move.sh.act { fst := x, snd := y }) { fst := x, snd := Int.instNegInt.neg y }
```

## `Move.act_sv`

axioms: none

```
∀ (x y : Int), Eq (Move.sv.act { fst := x, snd := y }) { fst := Int.instNegInt.neg x, snd := y }
```

## `Move.ofNat_ctorIdx` (generated)

axioms: none

```
∀ (x : Move), Eq (Move.ofNat x.ctorIdx) x
```

## `Move.sh.sizeOf_spec` (generated)

axioms: none

```
Eq (Move._sizeOf_inst.sizeOf Move.sh) 1
```

## `Move.sv.sizeOf_spec` (generated)

axioms: none

```
Eq (Move._sizeOf_inst.sizeOf Move.sv) 1
```

## `MoveSet.mk.inj` (generated)

axioms: none

```
∀ {hasI hasSv hasSh hasC2 hasI_1 hasSv_1 hasSh_1 hasC2_1 : Bool}, Eq { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 } { hasI := hasI_1, hasSv := hasSv_1, hasSh := hasSh_1, hasC2 := hasC2_1 } → And (Eq hasI hasI_1) (And (Eq hasSv hasSv_1) (And (Eq hasSh hasSh_1) (Eq hasC2 hasC2_1)))
```

## `MoveSet.mk.injEq` (generated)

axioms: propext

```
∀ (hasI hasSv hasSh hasC2 hasI_1 hasSv_1 hasSh_1 hasC2_1 : Bool), Eq (Eq { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 } { hasI := hasI_1, hasSv := hasSv_1, hasSh := hasSh_1, hasC2 := hasC2_1 }) (And (Eq hasI hasI_1) (And (Eq hasSv hasSv_1) (And (Eq hasSh hasSh_1) (Eq hasC2 hasC2_1))))
```

## `MoveSet.mk.sizeOf_spec` (generated)

axioms: none

```
∀ (hasI hasSv hasSh hasC2 : Bool), Eq (MoveSet._sizeOf_inst.sizeOf { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 }) (instHAdd.hAdd (instHAdd.hAdd (instHAdd.hAdd (instHAdd.hAdd 1 (Bool._sizeOf_inst.sizeOf hasI)) (Bool._sizeOf_inst.sizeOf hasSv)) (Bool._sizeOf_inst.sizeOf hasSh)) (Bool._sizeOf_inst.sizeOf hasC2))
```

## `R90_left_inv`

axioms: propext

```
∀ (p : Pt), Eq (R90inv (R90 p)) p
```

## `R90_right_inv`

axioms: propext

```
∀ (p : Pt), Eq (R90 (R90inv p)) p
```

## `S0_MoveSet_ext`

axioms: none

```
∀ {s t : MoveSet}, (∀ (g : Move), Eq (s.mem g) (t.mem g)) → Eq s t
```

## `S0_MoveSet_ext_iff`

axioms: none

```
∀ (s t : MoveSet), Iff (∀ (g : Move), Eq (s.mem g) (t.mem g)) (Eq s t)
```

## `S0_allSubs_exactly_once`

axioms: none

```
∀ (s : MoveSet), Eq (List.filter (fun t ↦ instBEqOfDecidableEq.beq t s) allSubs).length 1
```

## `S0_allSubs_nodup`

axioms: none

```
List.Pairwise (fun x1 x2 ↦ Ne x1 x2) allSubs
```

## `S0_invariant_iff_eq`

axioms: propext,Quot.sound

```
∀ (g : Move) (S : Pt → Prop), Iff (Invariant g S) (Eq (fun p ↦ S (g.act p)) S)
```

## `S0_subgroup_has_inverses`

axioms: none

```
∀ (s : MoveSet) (g : Move), Eq (s.mem g) Bool.true → Exists fun h ↦ And (Eq (s.mem h) Bool.true) (Eq (g.mul h) Move.I)
```

## `S1_five_iff_subgroup`

axioms: propext

```
∀ (s : MoveSet), Iff (List.instMembership.mem fiveSubgroups s) (Eq (isSubgroup s) Bool.true)
```

## `S1_flag_true`

axioms: propext,Classical.choice,Quot.sound

```
∀ (P : Prop), Iff (Eq (flag P) Bool.true) P
```

## `S1_no_three_element_symmetry`

axioms: propext

```
∀ (S : Pt → Prop), Invariant Move.sv S → Invariant Move.sh S → Invariant Move.C2 S
```

## `S1_one_of_five`

axioms: propext,Classical.choice,Quot.sound

```
∀ (S : Pt → Prop), Exists fun s ↦ And (List.instMembership.mem fiveSubgroups s) (∀ (g : Move), Iff (Eq (s.mem g) Bool.true) (Invariant g S))
```

## `S1_symSet_closed`

axioms: propext,Classical.choice,Quot.sound

```
∀ (S : Pt → Prop), And (Eq ((symSet S).mem Move.I) Bool.true) (∀ (g k : Move), Eq ((symSet S).mem g) Bool.true → Eq ((symSet S).mem k) Bool.true → Eq ((symSet S).mem (g.mul k)) Bool.true)
```

## `S1_symSet_isSubgroup`

axioms: propext,Classical.choice,Quot.sound

```
∀ (S : Pt → Prop), Eq (isSubgroup (symSet S)) Bool.true
```

## `S1_symSet_mem`

axioms: propext,Classical.choice,Quot.sound

```
∀ (S : Pt → Prop) (g : Move), Iff (Eq ((symSet S).mem g) Bool.true) (Invariant g S)
```

## `S2_invariant_ofList`

axioms: propext,Quot.sound

```
∀ (g : Move) (L : List Pt), Iff (Invariant g (ofList L)) (Eq (L.all fun p ↦ Decidable.decide (List.instMembership.mem L (g.act p))) Bool.true)
```

## `S2_markAll_invariant`

axioms: propext,Quot.sound

```
∀ (k : Move), Invariant k (ofList markAll)
```

## `S2_mark_C2_exact`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.C2))) (Or (Eq k Move.I) (Eq k Move.C2))
```

## `S2_mark_C2_exact_via_general`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.C2))) (Or (Eq k Move.I) (Eq k Move.C2))
```

## `S2_mark_eq_build`

axioms: propext,Quot.sound

```
∀ (g : Move) (L : List Pt) (q : Pt), Iff (List.instMembership.mem (instHAppendOfAppend.hAppend L (List.map g.act L)) q) (Or (List.instMembership.mem L q) (List.instMembership.mem L (g.act q)))
```

## `S2_mark_invariant_self`

axioms: propext,Quot.sound

```
∀ (g : Move) (L : List Pt), Invariant g (ofList (instHAppendOfAppend.hAppend L (List.map g.act L)))
```

## `S2_mark_sh_exact`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.sh))) (Or (Eq k Move.I) (Eq k Move.sh))
```

## `S2_mark_sh_exact_via_general`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.sh))) (Or (Eq k Move.I) (Eq k Move.sh))
```

## `S2_mark_sv_exact`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.sv))) (Or (Eq k Move.I) (Eq k Move.sv))
```

## `S2_mark_sv_exact_via_general`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList (mark Move.sv))) (Or (Eq k Move.I) (Eq k Move.sv))
```

## `S2_mem_mark`

axioms: propext,Quot.sound

```
∀ (g : Move) (L : List Pt) (q : Pt), Iff (List.instMembership.mem (instHAppendOfAppend.hAppend L (List.map g.act L)) q) (Or (List.instMembership.mem L q) (Exists fun r ↦ And (List.instMembership.mem L r) (Eq (g.act r) q)))
```

## `S2_not_invariant_of_region`

axioms: none

```
∀ (k : Move) (L : List Pt) (region : Pt → Prop), (∀ (q : Pt), List.instMembership.mem L q → region q) → ∀ (p : Pt), List.instMembership.mem L p → (∀ (q : Pt), region q → Not (region (k.act q))) → Not (Invariant k (ofList L))
```

## `S2_quadrant_mark_exact`

axioms: propext,Quot.sound

```
∀ (L : List Pt) (p0 : Pt), List.instMembership.mem L p0 → (∀ (q : Pt), List.instMembership.mem L q → And (Int.instLTInt.lt 0 q.fst) (Int.instLTInt.lt 0 q.snd)) → ∀ (g : Move), Ne g Move.I → ∀ (k : Move), Iff (Invariant k (ofList (instHAppendOfAppend.hAppend L (List.map g.act L)))) (Or (Eq k Move.I) (Eq k g))
```

## `S2_realizes_stab`

axioms: propext,Quot.sound

```
∀ (g k : Move), Iff (Eq ((stab g).mem k) Bool.true) (Invariant k (ofList (markOf g)))
```

## `S2_seed_asymmetric`

axioms: propext,Quot.sound

```
∀ (k : Move), Iff (Invariant k (ofList seed)) (Eq k Move.I)
```

## `S2_seed_in_quadrant`

axioms: none

```
∀ (q : Pt), List.instMembership.mem seed q → And (Int.instLTInt.lt 0 q.fst) (Int.instLTInt.lt 0 q.snd)
```

## `S2_seed_off_axes`

axioms: none

```
Eq (seed.all fun p ↦ Decidable.decide (And (Ne p.fst 0) (Ne p.snd 0))) Bool.true
```

## `S2_seed_subset`

axioms: propext,Quot.sound

```
∀ (g : Move), Eq (seed.all fun p ↦ Decidable.decide (List.instMembership.mem (mark g) p)) Bool.true
```

## `S2_stab_is_symSet`

axioms: propext,Classical.choice,Quot.sound

```
∀ (g : Move), Eq (symSet (ofList (markOf g))) (stab g)
```

## `S3_fml_swapVH`

axioms: propext,Quot.sound

```
∀ (f : Fml) (r : Nat → Move), Iff (f.holds fun n ↦ swapVH (r n)) (f.holds r)
```

## `S3_language_separates_I_from_sv`

axioms: none

```
And ((Fml.eqT (Tm.var 0) Tm.one).holds fun x ↦ Move.I) (Not ((Fml.eqT (Tm.var 0) Tm.one).holds fun x ↦ Move.sv))
```

## `S3_language_separates_turn_from_mirror`

axioms: none

```
And (Not ((Fml.detT (Tm.var 0) Tm.one).holds fun x ↦ Move.sv)) ((Fml.detT (Tm.var 0) Tm.one).holds fun x ↦ Move.C2)
```

## `S3_no_formula_separates_mirrors`

axioms: propext,Quot.sound

```
∀ (f : Fml), Iff (f.holds fun x ↦ Move.sv) (f.holds fun x ↦ Move.sh)
```

## `S3_swapVC_involution`

axioms: none

```
∀ (g : Move), Eq (swapVC (swapVC g)) g
```

## `S3_tm_swapVH`

axioms: propext

```
∀ (t : Tm) (r : Nat → Move), Eq (t.eval fun n ↦ swapVH (r n)) (swapVH (t.eval r))
```

## `S4_act_injective`

axioms: none

```
∀ (s t : Sq), (∀ (p : Pt), Eq (s.act p) (t.act p)) → Eq s t
```

## `S4_act_matrix`

axioms: propext,Quot.sound

```
∀ (s : Sq) (p : Pt), Eq (s.act p) (matAct s.mat.fst s.mat.snd.fst s.mat.snd.snd.fst s.mat.snd.snd.snd p)
```

## `S4_classification`

axioms: propext,Classical.choice,Quot.sound

```
∀ (a b c d : Int), (∀ (p : Pt), corner p → corner (matAct a b c d p)) → (∀ (q : Pt), corner q → Exists fun p ↦ And (corner p) (Eq (matAct a b c d p) q)) → Exists fun s ↦ And (∀ (p : Pt), Eq (matAct a b c d p) (s.act p)) (∀ (u : Sq), (∀ (p : Pt), Eq (matAct a b c d p) (u.act p)) → Eq u s)
```

## `S4_comp_act`

axioms: propext

```
∀ (s t : Sq) (p : Pt), Eq ((s.comp t).act p) (s.act (t.act p))
```

## `S4_comp_assoc`

axioms: none

```
∀ (s t u : Sq), Eq ((s.comp t).comp u) (s.comp (t.comp u))
```

## `S4_comp_id`

axioms: none

```
∀ (s : Sq), Eq (s.comp Sq.id) s
```

## `S4_comp_inv`

axioms: none

```
∀ (s : Sq), Eq (s.comp s.inv) Sq.id
```

## `S4_corner_maps`

axioms: propext,Classical.choice,Quot.sound

```
∀ (s : Sq) (p : Pt), corner p → corner (s.act p)
```

## `S4_corner_onto`

axioms: propext,Classical.choice,Quot.sound

```
∀ (s : Sq) (q : Pt), corner q → Exists fun p ↦ And (corner p) (Eq (s.act p) q)
```

## `S4_eight_are_all`

axioms: propext,Classical.choice,Quot.sound

```
∀ (a b c d : Int), Iff (And (∀ (p : Pt), corner p → corner (matAct a b c d p)) (∀ (q : Pt), corner q → Exists fun p ↦ And (corner p) (Eq (matAct a b c d p) q))) (Exists fun s ↦ ∀ (p : Pt), Eq (matAct a b c d p) (s.act p))
```

## `S4_entries`

axioms: propext,Classical.choice,Quot.sound

```
∀ (a b c d : Int), (∀ (p : Pt), corner p → corner (matAct a b c d p)) → (∀ (q : Pt), corner q → Exists fun p ↦ And (corner p) (Eq (matAct a b c d p) q)) → Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))
```

## `S4_id_comp`

axioms: none

```
∀ (s : Sq), Eq (Sq.id.comp s) s
```

## `S4_inv_comp`

axioms: none

```
∀ (s : Sq), Eq (s.inv.comp s) Sq.id
```

## `S4_matAct_add`

axioms: propext,Quot.sound

```
∀ (a b c d : Int) (p q : Pt), Eq (matAct a b c d { fst := instHAdd.hAdd p.fst q.fst, snd := instHAdd.hAdd p.snd q.snd }) { fst := instHAdd.hAdd (matAct a b c d p).fst (matAct a b c d q).fst, snd := instHAdd.hAdd (matAct a b c d p).snd (matAct a b c d q).snd }
```

## `S4_matAct_smul`

axioms: propext

```
∀ (a b c d n : Int) (p : Pt), Eq (matAct a b c d { fst := instHMul.hMul n p.fst, snd := instHMul.hMul n p.snd }) { fst := instHMul.hMul n (matAct a b c d p).fst, snd := instHMul.hMul n (matAct a b c d p).snd }
```

## `S4_unique_of_act`

axioms: none

```
∀ (a b c d : Int) (s : Sq), (∀ (p : Pt), Eq (matAct a b c d p) (s.act p)) → Exists fun t ↦ And (∀ (p : Pt), Eq (matAct a b c d p) (t.act p)) (∀ (u : Sq), (∀ (p : Pt), Eq (matAct a b c d p) (u.act p)) → Eq u t)
```

## `Sq.act_inv`

axioms: propext

```
∀ (s : Sq) (p : Pt), Eq (s.act (s.inv.act p)) p
```

## `Sq.id.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.id) 1
```

## `Sq.mirA.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.mirA) 1
```

## `Sq.mirD.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.mirD) 1
```

## `Sq.mirH.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.mirH) 1
```

## `Sq.mirV.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.mirV) 1
```

## `Sq.ofMove_act`

axioms: none

```
∀ (g : Move) (p : Pt), Eq ((Sq.ofMove g).act p) (g.act p)
```

## `Sq.ofNat_ctorIdx` (generated)

axioms: none

```
∀ (x : Sq), Eq (Sq.ofNat x.ctorIdx) x
```

## `Sq.rot180.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.rot180) 1
```

## `Sq.rot270.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.rot270) 1
```

## `Sq.rot90.sizeOf_spec` (generated)

axioms: none

```
Eq (Sq._sizeOf_inst.sizeOf Sq.rot90) 1
```

## `T10_det_table`

axioms: none

```
And (Eq Move.I.det 1) (And (Eq Move.C2.det 1) (And (Eq Move.sv.det (-1)) (Eq Move.sh.det (-1))))
```

## `T10_stab_I`

axioms: none

```
∀ (k : Move), Eq ((stab Move.I).mem k) Bool.true
```

## `T10_stab_distinct`

axioms: none

```
And (Ne (stab Move.I) (stab Move.sv)) (And (Ne (stab Move.I) (stab Move.sh)) (And (Ne (stab Move.I) (stab Move.C2)) (And (Ne (stab Move.sv) (stab Move.sh)) (And (Ne (stab Move.sv) (stab Move.C2)) (Ne (stab Move.sh) (stab Move.C2))))))
```

## `T10_stab_is_pair`

axioms: none

```
∀ (g : Move), Ne g Move.I → ∀ (k : Move), Iff (Eq ((stab g).mem k) Bool.true) (Or (Eq k Move.I) (Eq k g))
```

## `T10_stab_subgroup`

axioms: none

```
∀ (g : Move), Eq (isSubgroup (stab g)) Bool.true
```

## `T10_subI_unused`

axioms: none

```
∀ (g : Move), Ne (stab g) subI
```

## `T1_all_distinct`

axioms: none

```
And (Ne Move.I Move.sv) (And (Ne Move.I Move.sh) (And (Ne Move.I Move.C2) (And (Ne Move.sv Move.sh) (And (Ne Move.sv Move.C2) (Ne Move.sh Move.C2)))))
```

## `T1_all_length`

axioms: none

```
Eq Move.all.length 4
```

## `T1_mem_all`

axioms: propext

```
∀ (g : Move), List.instMembership.mem Move.all g
```

## `T1_mul_assoc`

axioms: none

```
∀ (g h k : Move), Eq ((g.mul h).mul k) (g.mul (h.mul k))
```

## `T1_mul_comm`

axioms: none

```
∀ (g h : Move), Eq (g.mul h) (h.mul g)
```

## `T1_mul_one`

axioms: none

```
∀ (g : Move), Eq (g.mul Move.I) g
```

## `T1_one_mul`

axioms: none

```
∀ (g : Move), Eq (Move.I.mul g) g
```

## `T1_self_inverse`

axioms: none

```
∀ (g : Move), Eq (g.mul g) Move.I
```

## `T2_faithful`

axioms: none

```
∀ (g h : Move), Ne g h → Exists fun p ↦ Ne (g.act p) (h.act p)
```

## `T2_probe_injective`

axioms: none

```
∀ (g h : Move), Eq (g.act { fst := 1, snd := 1 }) (h.act { fst := 1, snd := 1 }) → Eq g h
```

## `T3_act_matrix`

axioms: propext,Quot.sound

```
∀ (g : Move) (x y : Int), Eq (g.act { fst := x, snd := y }) { fst := instHAdd.hAdd (instHMul.hMul g.a x) (instHMul.hMul g.b y), snd := instHAdd.hAdd (instHMul.hMul g.c x) (instHMul.hMul g.d y) }
```

## `T3_det_eq_ad_sub_bc`

axioms: none

```
∀ (g : Move), Eq g.det (instHSub.hSub (instHMul.hMul g.a g.d) (instHMul.hMul g.b g.c))
```

## `T3_det_kernel`

axioms: none

```
∀ (g : Move), Iff (Eq g.det 1) (Or (Eq g Move.I) (Eq g Move.C2))
```

## `T3_det_mirrors`

axioms: none

```
∀ (g : Move), Iff (Eq g.det (-1)) (Or (Eq g Move.sv) (Eq g Move.sh))
```

## `T3_det_mul`

axioms: none

```
∀ (g h : Move), Eq (g.mul h).det (instHMul.hMul g.det h.det)
```

## `T4_fix_C2`

axioms: propext,Classical.choice,Quot.sound

```
∀ (x y : Int), Iff (Eq (Move.C2.act { fst := x, snd := y }) { fst := x, snd := y }) (And (Eq x 0) (Eq y 0))
```

## `T4_fix_I`

axioms: none

```
∀ (p : Pt), Eq (Move.I.act p) p
```

## `T4_fix_sh`

axioms: propext,Classical.choice,Quot.sound

```
∀ (x y : Int), Iff (Eq (Move.sh.act { fst := x, snd := y }) { fst := x, snd := y }) (Eq y 0)
```

## `T4_fix_sv`

axioms: propext,Classical.choice,Quot.sound

```
∀ (x y : Int), Iff (Eq (Move.sv.act { fst := x, snd := y }) { fst := x, snd := y }) (Eq x 0)
```

## `T4_mirrors_differ`

axioms: none

```
And (Eq (Move.sv.act { fst := 0, snd := 1 }) { fst := 0, snd := 1 }) (Ne (Move.sh.act { fst := 0, snd := 1 }) { fst := 0, snd := 1 })
```

## `T5_C2_commutes`

axioms: none

```
∀ (s : Sq) (p : Pt), Eq (s.act (Move.C2.act p)) (Move.C2.act (s.act p))
```

## `T5_C2_conj_fixed`

axioms: propext

```
∀ (s : Sq) (p : Pt), Eq (s.act (Move.C2.act (s.inv.act p))) (Move.C2.act p)
```

## `T5_C2_never_sh`

axioms: propext

```
∀ (s : Sq), Not (∀ (p : Pt), Eq (s.act (Move.C2.act (s.inv.act p))) (Move.sh.act p))
```

## `T5_C2_never_sv`

axioms: propext

```
∀ (s : Sq), Not (∀ (p : Pt), Eq (s.act (Move.C2.act (s.inv.act p))) (Move.sv.act p))
```

## `T5_R90_conj_C2`

axioms: propext

```
∀ (p : Pt), Eq (R90 (Move.C2.act (R90inv p))) (Move.C2.act p)
```

## `T5_R90_conj_sh`

axioms: propext

```
∀ (p : Pt), Eq (R90 (Move.sh.act (R90inv p))) (Move.sv.act p)
```

## `T5_eight_distinct`

axioms: none

```
∀ (s t : Sq), Eq (s.act { fst := 1, snd := 2 }) (t.act { fst := 1, snd := 2 }) → Eq s t
```

## `T5_rot270_eq_R90inv`

axioms: none

```
∀ (p : Pt), Eq (Sq.rot270.act p) (R90inv p)
```

## `T5_rot90_eq_R90`

axioms: none

```
∀ (p : Pt), Eq (Sq.rot90.act p) (R90 p)
```

## `T6_swapVC_breaks_det`

axioms: none

```
Not (∀ (g : Move), Eq (swapVC g).det g.det)
```

## `T6_swapVC_hom`

axioms: none

```
∀ (g h : Move), Eq (swapVC (g.mul h)) ((swapVC g).mul (swapVC h))
```

## `T6_swapVH_det`

axioms: none

```
∀ (g : Move), Eq (swapVH g).det g.det
```

## `T6_swapVH_hom`

axioms: none

```
∀ (g h : Move), Eq (swapVH (g.mul h)) ((swapVH g).mul (swapVH h))
```

## `T6_swapVH_involution`

axioms: none

```
∀ (g : Move), Eq (swapVH (swapVH g)) g
```

## `T6_three_interchangeable`

axioms: none

```
And (Exists fun f ↦ And (∀ (g : Move), Eq (f (f g)) g) (And (∀ (g h : Move), Eq (f (g.mul h)) ((f g).mul (f h))) (Eq (f Move.sv) Move.sh))) (Exists fun f ↦ And (∀ (g : Move), Eq (f (f g)) g) (And (∀ (g h : Move), Eq (f (g.mul h)) ((f g).mul (f h))) (Eq (f Move.sv) Move.C2)))
```

## `T7_both_mirrors`

axioms: propext

```
∀ {S : Pt → Prop}, Invariant Move.sv S → Invariant Move.sh S → Invariant Move.C2 S
```

## `T7_invariant_I`

axioms: none

```
∀ (S : Pt → Prop), Invariant Move.I S
```

## `T7_invariant_mul`

axioms: propext

```
∀ {g k : Move} {S : Pt → Prop}, Invariant g S → Invariant k S → Invariant (g.mul k) S
```

## `T7_mirror_and_turn`

axioms: propext

```
∀ {S : Pt → Prop}, Invariant Move.sv S → Invariant Move.C2 S → Invariant Move.sh S
```

## `T7_turn_and_mirror`

axioms: propext

```
∀ {S : Pt → Prop}, Invariant Move.sh S → Invariant Move.C2 S → Invariant Move.sv S
```

## `T8_enum_complete`

axioms: propext

```
∀ (s : MoveSet), List.instMembership.mem allSubs s
```

## `T8_five_are`

axioms: none

```
∀ (s : MoveSet), Iff (Eq (isSubgroup s) Bool.true) (Or (Eq s subI) (Or (Eq s subSv) (Or (Eq s subSh) (Or (Eq s subC2) (Eq s subAll)))))
```

## `T8_five_count`

axioms: none

```
Eq (List.filter isSubgroup allSubs).length 5
```

## `T8_five_list`

axioms: none

```
Eq (List.filter isSubgroup allSubs) (List.cons subI (List.cons subC2 (List.cons subSh (List.cons subSv (List.cons subAll List.nil)))))
```

## `T8_isSubgroup_iff`

axioms: none

```
∀ (s : MoveSet), Iff (Eq (isSubgroup s) Bool.true) (And (Eq (s.mem Move.I) Bool.true) (∀ (g h : Move), Eq (s.mem g) Bool.true → Eq (s.mem h) Bool.true → Eq (s.mem (g.mul h)) Bool.true))
```

## `T8_no_three_element`

axioms: none

```
Eq (isSubgroup { hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.false }) Bool.false
```

## `T8_sixteen`

axioms: none

```
Eq allSubs.length 16
```

## `T9_build`

axioms: propext

```
∀ {g : Move}, Eq (g.mul g) Move.I → ∀ (S : Pt → Prop), Invariant g fun p ↦ Or (S p) (S (g.act p))
```

## `T9_build_any`

axioms: propext

```
∀ (g : Move) (S : Pt → Prop), Invariant g fun p ↦ Or (S p) (S (g.act p))
```

## `Tm.brecOn.eq` (generated)

axioms: none

```
∀ {motive : Tm → Sort u} (t : Tm) (F_1 : (t : Tm) → Tm.below t → motive t), Eq (Tm.brecOn t F_1) (F_1 t (Tm.brecOn.go t F_1).2)
```

## `Tm.eval.eq_def` (generated)

axioms: none

```
∀ (x : Tm) (x_1 : Nat → Move), Eq (x.eval x_1) (Tm.eval.match_1 (fun x x_2 ↦ Move) x x_1 (fun n r ↦ r n) (fun x ↦ Move.I) fun s t r ↦ (s.eval r).mul (t.eval r))
```

## `Tm.mulT.inj` (generated)

axioms: none

```
∀ {s t s_1 t_1 : Tm}, Eq (s.mulT t) (s_1.mulT t_1) → And (Eq s s_1) (Eq t t_1)
```

## `Tm.mulT.injEq` (generated)

axioms: propext

```
∀ (s t s_1 t_1 : Tm), Eq (Eq (s.mulT t) (s_1.mulT t_1)) (And (Eq s s_1) (Eq t t_1))
```

## `Tm.mulT.sizeOf_spec` (generated)

axioms: none

```
∀ (s t : Tm), Eq (Tm._sizeOf_inst.sizeOf (s.mulT t)) (instHAdd.hAdd (instHAdd.hAdd 1 (Tm._sizeOf_inst.sizeOf s)) (Tm._sizeOf_inst.sizeOf t))
```

## `Tm.one.sizeOf_spec` (generated)

axioms: none

```
Eq (Tm._sizeOf_inst.sizeOf Tm.one) 1
```

## `Tm.var.inj` (generated)

axioms: none

```
∀ {n n_1 : Nat}, Eq (Tm.var n) (Tm.var n_1) → Eq n n_1
```

## `Tm.var.injEq` (generated)

axioms: propext

```
∀ (n n_1 : Nat), Eq (Eq (Tm.var n) (Tm.var n_1)) (Eq n n_1)
```

## `Tm.var.sizeOf_spec` (generated)

axioms: none

```
∀ (n : Nat), Eq (Tm._sizeOf_inst.sizeOf (Tm.var n)) (instHAdd.hAdd 1 (instSizeOfNat.sizeOf n))
```

## Definitions

Every constant of the compiled module that is not a theorem and that
Lean does not call internal, other than the constructors and recursors
it derives: its kind, its type and its body.

Definitions listed: 135.

### `Fml`  (inductive)

```
Type
:=
(no body: this constant is declared, not defined)
```

### `Fml.allF.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 5 → ((n : Nat) → (f : Fml) → motive (Fml.allF n f)) → motive t
:=
fun {motive} t h allF ↦ Fml.ctorElim 5 t ⋯ { down := allF }
```

### `Fml.allF.noConfusion`  (def)

```
{P : Sort u} → {n : Nat} → {f : Fml} → {n' : Nat} → {f' : Fml} → Eq (Fml.allF n f) (Fml.allF n' f') → (Eq n n' → Eq f f' → P) → P
:=
fun {P} {n} {f} {n'} {f'} eq k ↦ id (@Fml.noConfusion P (Fml.allF n f) (Fml.allF n' f') eq k)
```

### `Fml.andF.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 3 → ((f g : Fml) → motive (f.andF g)) → motive t
:=
fun {motive} t h andF ↦ Fml.ctorElim 3 t ⋯ { down := andF }
```

### `Fml.andF.noConfusion`  (def)

```
{P : Sort u} → {f g f' g' : Fml} → Eq (f.andF g) (f'.andF g') → (Eq f f' → Eq g g' → P) → P
:=
fun {P} {f g f' g'} eq k ↦ id (@Fml.noConfusion P (f.andF g) (f'.andF g') eq k)
```

### `Fml.below`  (def)

```
{motive : Fml → Sort u} → Fml → Sort (max 1 u)
:=
fun {motive} t ↦ Fml.rec (fun s t ↦ PUnit) (fun s t ↦ PUnit) (fun f f_ih ↦ PProd (motive f) f_ih) (fun f g f_ih g_ih ↦ PProd (PProd (motive f) f_ih) (PProd (motive g) g_ih)) (fun f g f_ih g_ih ↦ PProd (PProd (motive f) f_ih) (PProd (motive g) g_ih)) (fun n f f_ih ↦ PProd (motive f) f_ih) t
```

### `Fml.brecOn`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → ((t : Fml) → Fml.below t → motive t) → motive t
:=
fun {motive} t F_1 ↦ (Fml.brecOn.go t F_1).1
```

### `Fml.brecOn.go`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → ((t : Fml) → Fml.below t → motive t) → PProd (motive t) (Fml.below t)
:=
fun {motive} t F_1 ↦ Fml.rec (fun s t ↦ { fst := F_1 (Fml.eqT s t) PUnit.unit, snd := PUnit.unit }) (fun s t ↦ { fst := F_1 (Fml.detT s t) PUnit.unit, snd := PUnit.unit }) (fun f f_ih ↦ { fst := F_1 f.neg f_ih, snd := f_ih }) (fun f g f_ih g_ih ↦ { fst := F_1 (f.andF g) { fst := f_ih, snd := g_ih }, snd := { fst := f_ih, snd := g_ih } }) (fun f g f_ih g_ih ↦ { fst := F_1 (f.orF g) { fst := f_ih, snd := g_ih }, snd := { fst := f_ih, snd := g_ih } }) (fun n f f_ih ↦ { fst := F_1 (Fml.allF n f) f_ih, snd := f_ih }) t
```

### `Fml.casesOn`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → ((s t : Tm) → motive (Fml.eqT s t)) → ((s t : Tm) → motive (Fml.detT s t)) → ((f : Fml) → motive f.neg) → ((f g : Fml) → motive (f.andF g)) → ((f g : Fml) → motive (f.orF g)) → ((n : Nat) → (f : Fml) → motive (Fml.allF n f)) → motive t
:=
fun {motive} t eqT detT neg andF orF allF ↦ Fml.rec (fun s t ↦ eqT s t) (fun s t ↦ detT s t) (fun f f_ih ↦ neg f) (fun f g f_ih g_ih ↦ andF f g) (fun f g f_ih g_ih ↦ orF f g) (fun n f f_ih ↦ allF n f) t
```

### `Fml.ctorElim`  (def)

```
{motive : Fml → Sort u} → (ctorIdx : Nat) → (t : Fml) → Eq ctorIdx t.ctorIdx → Fml.ctorElimType ctorIdx → motive t
:=
fun {motive} ctorIdx t h k ↦ Fml.casesOn (motive := fun t ↦ Eq ctorIdx t.ctorIdx → motive t) t (fun s t h ↦ (Eq.ndrec k h).down s t) (fun s t h ↦ (Eq.ndrec k h).down s t) (fun f h ↦ (Eq.ndrec k h).down f) (fun f g h ↦ (Eq.ndrec k h).down f g) (fun f g h ↦ (Eq.ndrec k h).down f g) (fun n f h ↦ (Eq.ndrec k h).down n f) h
```

### `Fml.ctorElimType`  (def)

```
{motive : Fml → Sort u} → Nat → Sort (max 1 u)
:=
fun {motive} ctorIdx ↦ cond (ctorIdx.ble 2) (cond (ctorIdx.ble 0) (PULift ((s t : Tm) → motive (Fml.eqT s t))) (cond (ctorIdx.ble 1) (PULift ((s t : Tm) → motive (Fml.detT s t))) (PULift ((f : Fml) → motive f.neg)))) (cond (ctorIdx.ble 3) (PULift ((f g : Fml) → motive (f.andF g))) (cond (ctorIdx.ble 4) (PULift ((f g : Fml) → motive (f.orF g))) (PULift ((n : Nat) → (f : Fml) → motive (Fml.allF n f)))))
```

### `Fml.ctorIdx`  (def)

```
Fml → Nat
:=
fun x ↦ Fml.casesOn x (fun s t ↦ 0) (fun s t ↦ 1) (fun f ↦ 2) (fun f g ↦ 3) (fun f g ↦ 4) fun n f ↦ 5
```

### `Fml.detT.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 1 → ((s t : Tm) → motive (Fml.detT s t)) → motive t
:=
fun {motive} t h detT ↦ Fml.ctorElim 1 t ⋯ { down := detT }
```

### `Fml.detT.noConfusion`  (def)

```
{P : Sort u} → {s t s' t' : Tm} → Eq (Fml.detT s t) (Fml.detT s' t') → (Eq s s' → Eq t t' → P) → P
:=
fun {P} {s t s' t'} eq k ↦ id (@Fml.noConfusion P (Fml.detT s t) (Fml.detT s' t') eq k)
```

### `Fml.eqT.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 0 → ((s t : Tm) → motive (Fml.eqT s t)) → motive t
:=
fun {motive} t h eqT ↦ Fml.ctorElim 0 t ⋯ { down := eqT }
```

### `Fml.eqT.noConfusion`  (def)

```
{P : Sort u} → {s t s' t' : Tm} → Eq (Fml.eqT s t) (Fml.eqT s' t') → (Eq s s' → Eq t t' → P) → P
:=
fun {P} {s t s' t'} eq k ↦ id (@Fml.noConfusion P (Fml.eqT s t) (Fml.eqT s' t') eq k)
```

### `Fml.holds`  (def)

```
Fml → (Nat → Move) → Prop
:=
fun x x_1 ↦ Fml.brecOn (motive := fun x ↦ (Nat → Move) → Prop) x Fml.holds._f x_1
```

### `Fml.neg.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 2 → ((f : Fml) → motive f.neg) → motive t
:=
fun {motive} t h neg ↦ Fml.ctorElim 2 t ⋯ { down := neg }
```

### `Fml.neg.noConfusion`  (def)

```
{P : Sort u} → {f f' : Fml} → Eq f.neg f'.neg → (Eq f f' → P) → P
:=
fun {P} {f f'} eq k ↦ id (@Fml.noConfusion P f.neg f'.neg eq k)
```

### `Fml.noConfusion`  (def)

```
{P : Sort u} → {t t' : Fml} → Eq t t' → Fml.noConfusionType P t t'
:=
fun {P} {t t'} eq ↦ Eq.ndrec (Fml.casesOn t (fun s t k ↦ k ⋯ ⋯) (fun s t k ↦ k ⋯ ⋯) (fun f k ↦ k ⋯) (fun f g k ↦ k ⋯ ⋯) (fun f g k ↦ k ⋯ ⋯) fun n f k ↦ k ⋯ ⋯) eq
```

### `Fml.noConfusionType`  (def)

```
Sort u → Fml → Fml → Sort u
:=
fun P t t' ↦ Fml.casesOn t (fun s t ↦ dite (Eq t'.ctorIdx 0) (fun h ↦ Fml.eqT.elim t' h fun s_1 t_1 ↦ (Eq s s_1 → Eq t t_1 → P) → P) fun h ↦ P) (fun s t ↦ dite (Eq t'.ctorIdx 1) (fun h ↦ Fml.detT.elim t' h fun s_1 t_1 ↦ (Eq s s_1 → Eq t t_1 → P) → P) fun h ↦ P) (fun f ↦ dite (Eq t'.ctorIdx 2) (fun h ↦ Fml.neg.elim t' h fun f_1 ↦ (Eq f f_1 → P) → P) fun h ↦ P) (fun f g ↦ dite (Eq t'.ctorIdx 3) (fun h ↦ Fml.andF.elim t' h fun f_1 g_1 ↦ (Eq f f_1 → Eq g g_1 → P) → P) fun h ↦ P) (fun f g ↦ dite (Eq t'.ctorIdx 4) (fun h ↦ Fml.orF.elim t' h fun f_1 g_1 ↦ (Eq f f_1 → Eq g g_1 → P) → P) fun h ↦ P) fun n f ↦ dite (Eq t'.ctorIdx 5) (fun h ↦ Fml.allF.elim t' h fun n_1 f_1 ↦ (Eq n n_1 → Eq f f_1 → P) → P) fun h ↦ P
```

### `Fml.orF.elim`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → Eq t.ctorIdx 4 → ((f g : Fml) → motive (f.orF g)) → motive t
:=
fun {motive} t h orF ↦ Fml.ctorElim 4 t ⋯ { down := orF }
```

### `Fml.orF.noConfusion`  (def)

```
{P : Sort u} → {f g f' g' : Fml} → Eq (f.orF g) (f'.orF g') → (Eq f f' → Eq g g' → P) → P
:=
fun {P} {f g f' g'} eq k ↦ id (@Fml.noConfusion P (f.orF g) (f'.orF g') eq k)
```

### `Fml.recOn`  (def)

```
{motive : Fml → Sort u} → (t : Fml) → ((s t : Tm) → motive (Fml.eqT s t)) → ((s t : Tm) → motive (Fml.detT s t)) → ((f : Fml) → motive f → motive f.neg) → ((f g : Fml) → motive f → motive g → motive (f.andF g)) → ((f g : Fml) → motive f → motive g → motive (f.orF g)) → ((n : Nat) → (f : Fml) → motive f → motive (Fml.allF n f)) → motive t
:=
fun {motive} t eqT detT neg andF orF allF ↦ Fml.rec eqT detT neg andF orF allF t
```

### `Invariant`  (def)

```
Move → (Pt → Prop) → Prop
:=
fun g S ↦ ∀ (p : Pt), Iff (S (g.act p)) (S p)
```

### `Move`  (inductive)

```
Type
:=
(no body: this constant is declared, not defined)
```

### `Move.C2.elim`  (def)

```
{motive : Move → Sort u} → (t : Move) → Eq t.ctorIdx 3 → motive Move.C2 → motive t
:=
fun {motive} t h C2 ↦ Move.ctorElim 3 t ⋯ { down := C2 }
```

### `Move.I.elim`  (def)

```
{motive : Move → Sort u} → (t : Move) → Eq t.ctorIdx 0 → motive Move.I → motive t
:=
fun {motive} t h I ↦ Move.ctorElim 0 t ⋯ { down := I }
```

### `Move.a`  (def)

```
Move → Int
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Int) x (fun _ ↦ 1) (fun _ ↦ -1) (fun _ ↦ 1) fun _ ↦ -1
```

### `Move.act`  (def)

```
Move → Pt → Pt
:=
fun x x_1 ↦ Move.act.match_1 (fun x x_2 ↦ Pt) x x_1 (fun x y ↦ { fst := x, snd := y }) (fun x y ↦ { fst := Int.instNegInt.neg x, snd := y }) (fun x y ↦ { fst := x, snd := Int.instNegInt.neg y }) fun x y ↦ { fst := Int.instNegInt.neg x, snd := Int.instNegInt.neg y }
```

### `Move.all`  (def)

```
List Move
:=
List.cons Move.I (List.cons Move.sv (List.cons Move.sh (List.cons Move.C2 List.nil)))
```

### `Move.b`  (def)

```
Move → Int
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Int) x (fun _ ↦ 0) (fun _ ↦ 0) (fun _ ↦ 0) fun _ ↦ 0
```

### `Move.c`  (def)

```
Move → Int
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Int) x (fun _ ↦ 0) (fun _ ↦ 0) (fun _ ↦ 0) fun _ ↦ 0
```

### `Move.casesOn`  (def)

```
{motive : Move → Sort u} → (t : Move) → motive Move.I → motive Move.sv → motive Move.sh → motive Move.C2 → motive t
:=
fun {motive} t I sv sh C2 ↦ Move.rec I sv sh C2 t
```

### `Move.ctorElim`  (def)

```
{motive : Move → Sort u} → (ctorIdx : Nat) → (t : Move) → Eq ctorIdx t.ctorIdx → Move.ctorElimType ctorIdx → motive t
:=
fun {motive} ctorIdx t h k ↦ Move.casesOn (motive := fun t ↦ Eq ctorIdx t.ctorIdx → motive t) t (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) h
```

### `Move.ctorElimType`  (def)

```
{motive : Move → Sort u} → Nat → Sort (max 1 u)
:=
fun {motive} ctorIdx ↦ cond (ctorIdx.ble 1) (cond (ctorIdx.ble 0) (PULift (motive Move.I)) (PULift (motive Move.sv))) (cond (ctorIdx.ble 2) (PULift (motive Move.sh)) (PULift (motive Move.C2)))
```

### `Move.ctorIdx`  (def)

```
Move → Nat
:=
fun x ↦ Move.casesOn x 0 1 2 3
```

### `Move.d`  (def)

```
Move → Int
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Int) x (fun _ ↦ 1) (fun _ ↦ 1) (fun _ ↦ -1) fun _ ↦ -1
```

### `Move.decidableForall`  (def)

```
(p : Move → Prop) → [DecidablePred p] → Decidable (∀ (g : Move), p g)
:=
fun p [DecidablePred p] ↦ dite (p Move.I) (fun hI ↦ dite (p Move.sv) (fun hv ↦ dite (p Move.sh) (fun hh ↦ dite (p Move.C2) (fun hc ↦ Decidable.isTrue ⋯) fun hc ↦ Decidable.isFalse ⋯) fun hh ↦ Decidable.isFalse ⋯) fun hv ↦ Decidable.isFalse ⋯) fun hI ↦ Decidable.isFalse ⋯
```

### `Move.det`  (def)

```
Move → Int
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Int) x (fun _ ↦ 1) (fun _ ↦ -1) (fun _ ↦ -1) fun _ ↦ 1
```

### `Move.mul`  (def)

```
Move → Move → Move
:=
fun x x_1 ↦ Move.mul.match_1 (fun x x_2 ↦ Move) x x_1 (fun _ ↦ Move.I) (fun _ ↦ Move.sv) (fun _ ↦ Move.sh) (fun _ ↦ Move.C2) (fun _ ↦ Move.sv) (fun _ ↦ Move.I) (fun _ ↦ Move.C2) (fun _ ↦ Move.sh) (fun _ ↦ Move.sh) (fun _ ↦ Move.C2) (fun _ ↦ Move.I) (fun _ ↦ Move.sv) (fun _ ↦ Move.C2) (fun _ ↦ Move.sh) (fun _ ↦ Move.sv) fun _ ↦ Move.I
```

### `Move.noConfusion`  (def)

```
{P : Sort v✝} → {x y : Move} → Eq x y → Move.noConfusionType P x y
:=
fun {P} {x y} h ↦ noConfusionEnum Move.ctorIdx h
```

### `Move.noConfusionType`  (def)

```
Sort v✝ → Move → Move → Sort v✝
:=
fun P x y ↦ noConfusionTypeEnum Move.ctorIdx P x y
```

### `Move.ofNat`  (def)

```
Nat → Move
:=
fun n ↦ cond (n.ble 1) (cond (n.ble 0) Move.I Move.sv) (cond (n.ble 2) Move.sh Move.C2)
```

### `Move.recOn`  (def)

```
{motive : Move → Sort u} → (t : Move) → motive Move.I → motive Move.sv → motive Move.sh → motive Move.C2 → motive t
:=
fun {motive} t I sv sh C2 ↦ Move.rec I sv sh C2 t
```

### `Move.sh.elim`  (def)

```
{motive : Move → Sort u} → (t : Move) → Eq t.ctorIdx 2 → motive Move.sh → motive t
:=
fun {motive} t h sh ↦ Move.ctorElim 2 t ⋯ { down := sh }
```

### `Move.sv.elim`  (def)

```
{motive : Move → Sort u} → (t : Move) → Eq t.ctorIdx 1 → motive Move.sv → motive t
:=
fun {motive} t h sv ↦ Move.ctorElim 1 t ⋯ { down := sv }
```

### `Move.toCtorIdx`  (def)

```
Move → Nat
:=
Move.ctorIdx
```

### `MoveSet`  (inductive)

```
Type
:=
(no body: this constant is declared, not defined)
```

### `MoveSet.casesOn`  (def)

```
{motive : MoveSet → Sort u} → (t : MoveSet) → ((hasI hasSv hasSh hasC2 : Bool) → motive { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 }) → motive t
:=
fun {motive} t mk ↦ MoveSet.rec (fun hasI hasSv hasSh hasC2 ↦ mk hasI hasSv hasSh hasC2) t
```

### `MoveSet.closed`  (def)

```
MoveSet → Bool
:=
fun s ↦ Move.all.all fun g ↦ Move.all.all fun h ↦ ((s.mem g).and (s.mem h)).not.or (s.mem (g.mul h))
```

### `MoveSet.ctorIdx`  (def)

```
MoveSet → Nat
:=
fun x ↦ 0
```

### `MoveSet.hasC2`  (def)

```
MoveSet → Bool
:=
fun self ↦ self.4
```

### `MoveSet.hasI`  (def)

```
MoveSet → Bool
:=
fun self ↦ self.1
```

### `MoveSet.hasSh`  (def)

```
MoveSet → Bool
:=
fun self ↦ self.3
```

### `MoveSet.hasSv`  (def)

```
MoveSet → Bool
:=
fun self ↦ self.2
```

### `MoveSet.mem`  (def)

```
MoveSet → Move → Bool
:=
fun s x ↦ instReprMove.repr.match_1 (fun x ↦ Bool) x (fun _ ↦ s.hasI) (fun _ ↦ s.hasSv) (fun _ ↦ s.hasSh) fun _ ↦ s.hasC2
```

### `MoveSet.mk.noConfusion`  (def)

```
{P : Sort u} → {hasI hasSv hasSh hasC2 hasI' hasSv' hasSh' hasC2' : Bool} → Eq { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 } { hasI := hasI', hasSv := hasSv', hasSh := hasSh', hasC2 := hasC2' } → (Eq hasI hasI' → Eq hasSv hasSv' → Eq hasSh hasSh' → Eq hasC2 hasC2' → P) → P
:=
fun {P} {hasI hasSv hasSh hasC2 hasI' hasSv' hasSh' hasC2'} eq k ↦ id (MoveSet.noConfusion eq k)
```

### `MoveSet.noConfusion`  (def)

```
{P : Sort u} → {t t' : MoveSet} → Eq t t' → MoveSet.noConfusionType P t t'
:=
fun {P} {t t'} eq ↦ Eq.ndrec (MoveSet.casesOn t fun hasI hasSv hasSh hasC2 k ↦ k ⋯ ⋯ ⋯ ⋯) eq
```

### `MoveSet.noConfusionType`  (def)

```
Sort u → MoveSet → MoveSet → Sort u
:=
fun P t t' ↦ MoveSet.casesOn t fun hasI hasSv hasSh hasC2 ↦ MoveSet.casesOn t' fun hasI_1 hasSv_1 hasSh_1 hasC2_1 ↦ (Eq hasI hasI_1 → Eq hasSv hasSv_1 → Eq hasSh hasSh_1 → Eq hasC2 hasC2_1 → P) → P
```

### `MoveSet.recOn`  (def)

```
{motive : MoveSet → Sort u} → (t : MoveSet) → ((hasI hasSv hasSh hasC2 : Bool) → motive { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 }) → motive t
:=
fun {motive} t mk ↦ MoveSet.rec mk t
```

### `Pt`  (def)

```
Type
:=
Prod Int Int
```

### `R90`  (def)

```
Pt → Pt
:=
fun p ↦ { fst := Int.instNegInt.neg p.snd, snd := p.fst }
```

### `R90inv`  (def)

```
Pt → Pt
:=
fun p ↦ { fst := p.snd, snd := Int.instNegInt.neg p.fst }
```

### `Sq`  (inductive)

```
Type
:=
(no body: this constant is declared, not defined)
```

### `Sq.act`  (def)

```
Sq → Pt → Pt
:=
fun x x_1 ↦ Sq.act.match_1 (fun x x_2 ↦ Pt) x x_1 (fun x y ↦ { fst := x, snd := y }) (fun x y ↦ { fst := Int.instNegInt.neg y, snd := x }) (fun x y ↦ { fst := Int.instNegInt.neg x, snd := Int.instNegInt.neg y }) (fun x y ↦ { fst := y, snd := Int.instNegInt.neg x }) (fun x y ↦ { fst := Int.instNegInt.neg x, snd := y }) (fun x y ↦ { fst := x, snd := Int.instNegInt.neg y }) (fun x y ↦ { fst := y, snd := x }) fun x y ↦ { fst := Int.instNegInt.neg y, snd := Int.instNegInt.neg x }
```

### `Sq.casesOn`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → motive Sq.id → motive Sq.rot90 → motive Sq.rot180 → motive Sq.rot270 → motive Sq.mirV → motive Sq.mirH → motive Sq.mirD → motive Sq.mirA → motive t
:=
fun {motive} t id rot90 rot180 rot270 mirV mirH mirD mirA ↦ Sq.rec id rot90 rot180 rot270 mirV mirH mirD mirA t
```

### `Sq.comp`  (def)

```
Sq → Sq → Sq
:=
fun x x_1 ↦ Sq.comp.match_1 (fun x x_2 ↦ Sq) x x_1 (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.id) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.mirA) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirD) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.rot180) fun _ ↦ Sq.id
```

### `Sq.ctorElim`  (def)

```
{motive : Sq → Sort u} → (ctorIdx : Nat) → (t : Sq) → Eq ctorIdx t.ctorIdx → Sq.ctorElimType ctorIdx → motive t
:=
fun {motive} ctorIdx t h k ↦ Sq.casesOn (motive := fun t ↦ Eq ctorIdx t.ctorIdx → motive t) t (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) (fun h ↦ (Eq.ndrec k h).down) h
```

### `Sq.ctorElimType`  (def)

```
{motive : Sq → Sort u} → Nat → Sort (max 1 u)
:=
fun {motive} ctorIdx ↦ cond (ctorIdx.ble 3) (cond (ctorIdx.ble 1) (cond (ctorIdx.ble 0) (PULift (motive Sq.id)) (PULift (motive Sq.rot90))) (cond (ctorIdx.ble 2) (PULift (motive Sq.rot180)) (PULift (motive Sq.rot270)))) (cond (ctorIdx.ble 5) (cond (ctorIdx.ble 4) (PULift (motive Sq.mirV)) (PULift (motive Sq.mirH))) (cond (ctorIdx.ble 6) (PULift (motive Sq.mirD)) (PULift (motive Sq.mirA))))
```

### `Sq.ctorIdx`  (def)

```
Sq → Nat
:=
fun x ↦ Sq.casesOn x 0 1 2 3 4 5 6 7
```

### `Sq.id.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 0 → motive Sq.id → motive t
:=
fun {motive} t h id ↦ Sq.ctorElim 0 t ⋯ { down := id }
```

### `Sq.inv`  (def)

```
Sq → Sq
:=
fun x ↦ instReprSq.repr.match_1 (fun x ↦ Sq) x (fun _ ↦ Sq.id) (fun _ ↦ Sq.rot270) (fun _ ↦ Sq.rot180) (fun _ ↦ Sq.rot90) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirH) (fun _ ↦ Sq.mirD) fun _ ↦ Sq.mirA
```

### `Sq.mat`  (def)

```
Sq → Prod Int (Prod Int (Prod Int Int))
:=
fun x ↦ instReprSq.repr.match_1 (fun x ↦ Prod Int (Prod Int (Prod Int Int))) x (fun _ ↦ { fst := 1, snd := { fst := 0, snd := { fst := 0, snd := 1 } } }) (fun _ ↦ { fst := 0, snd := { fst := -1, snd := { fst := 1, snd := 0 } } }) (fun _ ↦ { fst := -1, snd := { fst := 0, snd := { fst := 0, snd := -1 } } }) (fun _ ↦ { fst := 0, snd := { fst := 1, snd := { fst := -1, snd := 0 } } }) (fun _ ↦ { fst := -1, snd := { fst := 0, snd := { fst := 0, snd := 1 } } }) (fun _ ↦ { fst := 1, snd := { fst := 0, snd := { fst := 0, snd := -1 } } }) (fun _ ↦ { fst := 0, snd := { fst := 1, snd := { fst := 1, snd := 0 } } }) fun _ ↦ { fst := 0, snd := { fst := -1, snd := { fst := -1, snd := 0 } } }
```

### `Sq.mirA.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 7 → motive Sq.mirA → motive t
:=
fun {motive} t h mirA ↦ Sq.ctorElim 7 t ⋯ { down := mirA }
```

### `Sq.mirD.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 6 → motive Sq.mirD → motive t
:=
fun {motive} t h mirD ↦ Sq.ctorElim 6 t ⋯ { down := mirD }
```

### `Sq.mirH.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 5 → motive Sq.mirH → motive t
:=
fun {motive} t h mirH ↦ Sq.ctorElim 5 t ⋯ { down := mirH }
```

### `Sq.mirV.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 4 → motive Sq.mirV → motive t
:=
fun {motive} t h mirV ↦ Sq.ctorElim 4 t ⋯ { down := mirV }
```

### `Sq.noConfusion`  (def)

```
{P : Sort v✝} → {x y : Sq} → Eq x y → Sq.noConfusionType P x y
:=
fun {P} {x y} h ↦ noConfusionEnum Sq.ctorIdx h
```

### `Sq.noConfusionType`  (def)

```
Sort v✝ → Sq → Sq → Sort v✝
:=
fun P x y ↦ noConfusionTypeEnum Sq.ctorIdx P x y
```

### `Sq.ofMove`  (def)

```
Move → Sq
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Sq) x (fun _ ↦ Sq.id) (fun _ ↦ Sq.mirV) (fun _ ↦ Sq.mirH) fun _ ↦ Sq.rot180
```

### `Sq.ofNat`  (def)

```
Nat → Sq
:=
fun n ↦ cond (n.ble 3) (cond (n.ble 1) (cond (n.ble 0) Sq.id Sq.rot90) (cond (n.ble 2) Sq.rot180 Sq.rot270)) (cond (n.ble 5) (cond (n.ble 4) Sq.mirV Sq.mirH) (cond (n.ble 6) Sq.mirD Sq.mirA))
```

### `Sq.recOn`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → motive Sq.id → motive Sq.rot90 → motive Sq.rot180 → motive Sq.rot270 → motive Sq.mirV → motive Sq.mirH → motive Sq.mirD → motive Sq.mirA → motive t
:=
fun {motive} t id rot90 rot180 rot270 mirV mirH mirD mirA ↦ Sq.rec id rot90 rot180 rot270 mirV mirH mirD mirA t
```

### `Sq.rot180.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 2 → motive Sq.rot180 → motive t
:=
fun {motive} t h rot180 ↦ Sq.ctorElim 2 t ⋯ { down := rot180 }
```

### `Sq.rot270.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 3 → motive Sq.rot270 → motive t
:=
fun {motive} t h rot270 ↦ Sq.ctorElim 3 t ⋯ { down := rot270 }
```

### `Sq.rot90.elim`  (def)

```
{motive : Sq → Sort u} → (t : Sq) → Eq t.ctorIdx 1 → motive Sq.rot90 → motive t
:=
fun {motive} t h rot90 ↦ Sq.ctorElim 1 t ⋯ { down := rot90 }
```

### `Sq.toCtorIdx`  (def)

```
Sq → Nat
:=
Sq.ctorIdx
```

### `Tm`  (inductive)

```
Type
:=
(no body: this constant is declared, not defined)
```

### `Tm.below`  (def)

```
{motive : Tm → Sort u} → Tm → Sort (max 1 u)
:=
fun {motive} t ↦ Tm.rec (fun n ↦ PUnit) PUnit (fun s t s_ih t_ih ↦ PProd (PProd (motive s) s_ih) (PProd (motive t) t_ih)) t
```

### `Tm.brecOn`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → ((t : Tm) → Tm.below t → motive t) → motive t
:=
fun {motive} t F_1 ↦ (Tm.brecOn.go t F_1).1
```

### `Tm.brecOn.go`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → ((t : Tm) → Tm.below t → motive t) → PProd (motive t) (Tm.below t)
:=
fun {motive} t F_1 ↦ Tm.rec (fun n ↦ { fst := F_1 (Tm.var n) PUnit.unit, snd := PUnit.unit }) { fst := F_1 Tm.one PUnit.unit, snd := PUnit.unit } (fun s t s_ih t_ih ↦ { fst := F_1 (s.mulT t) { fst := s_ih, snd := t_ih }, snd := { fst := s_ih, snd := t_ih } }) t
```

### `Tm.casesOn`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → ((n : Nat) → motive (Tm.var n)) → motive Tm.one → ((s t : Tm) → motive (s.mulT t)) → motive t
:=
fun {motive} t var one mulT ↦ Tm.rec (fun n ↦ var n) one (fun s t s_ih t_ih ↦ mulT s t) t
```

### `Tm.ctorElim`  (def)

```
{motive : Tm → Sort u} → (ctorIdx : Nat) → (t : Tm) → Eq ctorIdx t.ctorIdx → Tm.ctorElimType ctorIdx → motive t
:=
fun {motive} ctorIdx t h k ↦ Tm.casesOn (motive := fun t ↦ Eq ctorIdx t.ctorIdx → motive t) t (fun n h ↦ (Eq.ndrec k h).down n) (fun h ↦ (Eq.ndrec k h).down) (fun s t h ↦ (Eq.ndrec k h).down s t) h
```

### `Tm.ctorElimType`  (def)

```
{motive : Tm → Sort u} → Nat → Sort (max 1 u)
:=
fun {motive} ctorIdx ↦ cond (ctorIdx.ble 0) (PULift ((n : Nat) → motive (Tm.var n))) (cond (ctorIdx.ble 1) (PULift (motive Tm.one)) (PULift ((s t : Tm) → motive (s.mulT t))))
```

### `Tm.ctorIdx`  (def)

```
Tm → Nat
:=
fun x ↦ Tm.casesOn x (fun n ↦ 0) 1 fun s t ↦ 2
```

### `Tm.eval`  (def)

```
Tm → (Nat → Move) → Move
:=
fun x x_1 ↦ Tm.brecOn (motive := fun x ↦ (Nat → Move) → Move) x Tm.eval._f x_1
```

### `Tm.mulT.elim`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → Eq t.ctorIdx 2 → ((s t : Tm) → motive (s.mulT t)) → motive t
:=
fun {motive} t h mulT ↦ Tm.ctorElim 2 t ⋯ { down := mulT }
```

### `Tm.mulT.noConfusion`  (def)

```
{P : Sort u} → {s t s' t' : Tm} → Eq (s.mulT t) (s'.mulT t') → (Eq s s' → Eq t t' → P) → P
:=
fun {P} {s t s' t'} eq k ↦ id (@Tm.noConfusion P (s.mulT t) (s'.mulT t') eq k)
```

### `Tm.noConfusion`  (def)

```
{P : Sort u} → {t t' : Tm} → Eq t t' → Tm.noConfusionType P t t'
:=
fun {P} {t t'} eq ↦ Eq.ndrec (Tm.casesOn t (fun n k ↦ k ⋯) (fun k ↦ k) fun s t k ↦ k ⋯ ⋯) eq
```

### `Tm.noConfusionType`  (def)

```
Sort u → Tm → Tm → Sort u
:=
fun P t t' ↦ Tm.casesOn t (fun n ↦ dite (Eq t'.ctorIdx 0) (fun h ↦ Tm.var.elim t' h fun n_1 ↦ (Eq n n_1 → P) → P) fun h ↦ P) (dite (Eq t'.ctorIdx 1) (fun h ↦ Tm.one.elim t' h (P → P)) fun h ↦ P) fun s t ↦ dite (Eq t'.ctorIdx 2) (fun h ↦ Tm.mulT.elim t' h fun s_1 t_1 ↦ (Eq s s_1 → Eq t t_1 → P) → P) fun h ↦ P
```

### `Tm.one.elim`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → Eq t.ctorIdx 1 → motive Tm.one → motive t
:=
fun {motive} t h one ↦ Tm.ctorElim 1 t ⋯ { down := one }
```

### `Tm.recOn`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → ((n : Nat) → motive (Tm.var n)) → motive Tm.one → ((s t : Tm) → motive s → motive t → motive (s.mulT t)) → motive t
:=
fun {motive} t var one mulT ↦ Tm.rec var one mulT t
```

### `Tm.var.elim`  (def)

```
{motive : Tm → Sort u} → (t : Tm) → Eq t.ctorIdx 0 → ((n : Nat) → motive (Tm.var n)) → motive t
:=
fun {motive} t h var ↦ Tm.ctorElim 0 t ⋯ { down := var }
```

### `Tm.var.noConfusion`  (def)

```
{P : Sort u} → {n n' : Nat} → Eq (Tm.var n) (Tm.var n') → (Eq n n' → P) → P
:=
fun {P} {n n'} eq k ↦ id (@Tm.noConfusion P (Tm.var n) (Tm.var n') eq k)
```

### `allSubs`  (def)

```
List MoveSet
:=
List.cons { hasI := Bool.false, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.false } (List.cons { hasI := Bool.false, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.true } (List.cons { hasI := Bool.false, hasSv := Bool.false, hasSh := Bool.true, hasC2 := Bool.false } (List.cons { hasI := Bool.false, hasSv := Bool.false, hasSh := Bool.true, hasC2 := Bool.true } (List.cons { hasI := Bool.false, hasSv := Bool.true, hasSh := Bool.false, hasC2 := Bool.false } (List.cons { hasI := Bool.false, hasSv := Bool.true, hasSh := Bool.false, hasC2 := Bool.true } (List.cons { hasI := Bool.false, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.false } (List.cons { hasI := Bool.false, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.true } (List.cons { hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.false } (List.cons { hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.true } (List.cons { hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.true, hasC2 := Bool.false } (List.cons { hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.true, hasC2 := Bool.true } (List.cons { hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.false, hasC2 := Bool.false } (List.cons { hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.false, hasC2 := Bool.true } (List.cons { hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.false } (List.cons { hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.true } List.nil)))))))))))))))
```

### `corner`  (def)

```
Pt → Prop
:=
fun p ↦ And (Or (Eq p.fst 1) (Eq p.fst (-1))) (Or (Eq p.snd 1) (Eq p.snd (-1)))
```

### `fiveSubgroups`  (def)

```
List MoveSet
:=
List.cons subI (List.cons subSv (List.cons subSh (List.cons subC2 (List.cons subAll List.nil))))
```

### `flag`  (def)

```
Prop → Bool
:=
fun P ↦ Decidable.decide P
```

### `imageOf`  (def)

```
Move → List Pt → List Pt
:=
fun g L ↦ List.map g.act L
```

### `instDecidableEqMove`  (def)

```
DecidableEq Move
:=
fun x y ↦ dite (Eq x.ctorIdx y.ctorIdx) (fun h ↦ Decidable.isTrue ⋯) fun h ↦ Decidable.isFalse ⋯
```

### `instDecidableEqMoveSet`  (def)

```
DecidableEq MoveSet
:=
instDecidableEqMoveSet.decEq
```

### `instDecidableEqMoveSet.decEq`  (def)

```
(x x_1 : MoveSet) → Decidable (Eq x x_1)
:=
fun x x_1 ↦ instDecidableEqMoveSet.decEq.match_1 (fun x x_2 ↦ Decidable (Eq x x_2)) x x_1 fun a a_1 a_2 a_3 b b_1 b_2 b_3 ↦ dite (Eq a b) (fun h ↦ Eq.ndrec (dite (Eq a_1 b_1) (fun h ↦ Eq.ndrec (dite (Eq a_2 b_2) (fun h ↦ Eq.ndrec (dite (Eq a_3 b_3) (fun h ↦ Eq.ndrec (Decidable.isTrue ⋯) h) fun h ↦ Decidable.isFalse ⋯) h) fun h ↦ Decidable.isFalse ⋯) h) fun h ↦ Decidable.isFalse ⋯) h) fun h ↦ Decidable.isFalse ⋯
```

### `instDecidableEqSq`  (def)

```
DecidableEq Sq
:=
fun x y ↦ dite (Eq x.ctorIdx y.ctorIdx) (fun h ↦ Decidable.isTrue ⋯) fun h ↦ Decidable.isFalse ⋯
```

### `instReprMove`  (def)

```
Repr Move
:=
{ reprPrec := instReprMove.repr }
```

### `instReprMove.repr`  (def)

```
Move → Nat → Std.Format
:=
fun x prec ↦ instReprMove.repr.match_1 (fun x ↦ Std.Format) x (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Move.I")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Move.sv")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Move.sh")).group prec) fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Move.C2")).group prec
```

### `instReprMoveSet`  (def)

```
Repr MoveSet
:=
{ reprPrec := instReprMoveSet.repr }
```

### `instReprMoveSet.repr`  (def)

```
MoveSet → Nat → Std.Format
:=
fun x prec ↦ Std.Format.bracket "{ " (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend Std.Format.nil (Std.Format.text "hasI")) (Std.Format.text " := ")) (Std.Format.nest 8 (repr x.hasI)).group) (Std.Format.text ",")) Std.Format.line) (Std.Format.text "hasSv")) (Std.Format.text " := ")) (Std.Format.nest 9 (repr x.hasSv)).group) (Std.Format.text ",")) Std.Format.line) (Std.Format.text "hasSh")) (Std.Format.text " := ")) (Std.Format.nest 9 (repr x.hasSh)).group) (Std.Format.text ",")) Std.Format.line) (Std.Format.text "hasC2")) (Std.Format.text " := ")) (Std.Format.nest 9 (repr x.hasC2)).group) " }"
```

### `instReprSq`  (def)

```
Repr Sq
:=
{ reprPrec := instReprSq.repr }
```

### `instReprSq.repr`  (def)

```
Sq → Nat → Std.Format
:=
fun x prec ↦ instReprSq.repr.match_1 (fun x ↦ Std.Format) x (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.id")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.rot90")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.rot180")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.rot270")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.mirV")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.mirH")).group prec) (fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.mirD")).group prec) fun _ ↦ Repr.addAppParen (Std.Format.nest (ite (GE.ge prec 1024) 1 2) (Std.Format.text "Sq.mirA")).group prec
```

### `isSubgroup`  (def)

```
MoveSet → Bool
:=
fun s ↦ s.hasI.and s.closed
```

### `mark`  (def)

```
Move → List Pt
:=
fun g ↦ instHAppendOfAppend.hAppend seed (imageOf g seed)
```

### `markAll`  (def)

```
List Pt
:=
instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend (instHAppendOfAppend.hAppend seed (imageOf Move.sv seed)) (imageOf Move.sh seed)) (imageOf Move.C2 seed)
```

### `markOf`  (def)

```
Move → List Pt
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ List Pt) x (fun _ ↦ markAll) (fun _ ↦ mark Move.sv) (fun _ ↦ mark Move.sh) fun _ ↦ mark Move.C2
```

### `matAct`  (def)

```
Int → Int → Int → Int → Pt → Pt
:=
fun a b c d p ↦ { fst := instHAdd.hAdd (instHMul.hMul a p.fst) (instHMul.hMul b p.snd), snd := instHAdd.hAdd (instHMul.hMul c p.fst) (instHMul.hMul d p.snd) }
```

### `ofList`  (def)

```
List Pt → Pt → Prop
:=
fun L p ↦ List.instMembership.mem L p
```

### `seed`  (def)

```
List Pt
:=
List.cons { fst := 1, snd := 1 } (List.cons { fst := 2, snd := 1 } (List.cons { fst := 3, snd := 1 } (List.cons { fst := 1, snd := 2 } (List.cons { fst := 1, snd := 3 } List.nil))))
```

### `stab`  (def)

```
Move → MoveSet
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ MoveSet) x (fun _ ↦ subAll) (fun _ ↦ subSv) (fun _ ↦ subSh) fun _ ↦ subC2
```

### `subAll`  (def)

```
MoveSet
:=
{ hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.true, hasC2 := Bool.true }
```

### `subC2`  (def)

```
MoveSet
:=
{ hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.true }
```

### `subI`  (def)

```
MoveSet
:=
{ hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.false, hasC2 := Bool.false }
```

### `subSh`  (def)

```
MoveSet
:=
{ hasI := Bool.true, hasSv := Bool.false, hasSh := Bool.true, hasC2 := Bool.false }
```

### `subSv`  (def)

```
MoveSet
:=
{ hasI := Bool.true, hasSv := Bool.true, hasSh := Bool.false, hasC2 := Bool.false }
```

### `swapVC`  (def)

```
Move → Move
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Move) x (fun _ ↦ Move.I) (fun _ ↦ Move.C2) (fun _ ↦ Move.sh) fun _ ↦ Move.sv
```

### `swapVH`  (def)

```
Move → Move
:=
fun x ↦ instReprMove.repr.match_1 (fun x ↦ Move) x (fun _ ↦ Move.I) (fun _ ↦ Move.sh) (fun _ ↦ Move.sv) fun _ ↦ Move.C2
```

### `symSet`  (def)

```
(Pt → Prop) → MoveSet
:=
fun S ↦ { hasI := flag (Invariant Move.I S), hasSv := flag (Invariant Move.sv S), hasSh := flag (Invariant Move.sh S), hasC2 := flag (Invariant Move.C2 S) }
```

## Generated auxiliaries

Every remaining constant of the compiled module: the names Lean
generates underneath the declarations above — the matchers a definition
by cases compiles to, their splitters, the equation lemmas, the proof
terms a tactic left behind, the `sizeOf` helpers.  Each row carries the
name, the kind, the class the gate put the name in (`aux` for an
auxiliary of a declaration of this module that Lean does not call
internal; `internal` or `private` for a name that belongs to no such
declaration, which the gate also reports as a failure), and the
statement or the body.  The parent of an `aux` name is sometimes a
constructor or a recursor Lean derived, which has no row of its own,
so the set a parent is looked for in is wider than the rows above.

Names under `_private.Subject.0.` are Lean's encoding of a private
declaration: the prefix marks it private, the `0` is Lean's hash field
and `Subject` is the module name, which is the fixed name the gate
compiles the file under.  121 of the rows below are Lean's own private
equation lemmas for matchers, generated and named that way by Lean
itself; the file declares nothing private.

The equation lemmas are the readable ones, and the reason this section
exists.  The printed body of a definition written by pattern matching
is a `brecOn` applied to a matcher, so which arm belongs to which
constructor is not legible in the second section; `Fml.holds.eq_4` says
it outright.  A reviewer swapped the `andF` and `orF` arms of
`Fml.holds` and nothing in the first two sections changed.  Ten rows
of this section change under that swap.  Where a reader regenerates
this listing from a swapped file rather than comparing against the
committed one, the run is green and the listing it writes carries the
swap: that is a limit of regenerating, and the reason the committed
copy is the one the gate compares against.

Auxiliaries listed: 345.

### `Fml._sizeOf_1`  (def, aux)

```
Fml → Nat
:=
fun t ↦ Fml.rec (fun s t ↦ instHAdd.hAdd (instHAdd.hAdd 1 (Tm._sizeOf_inst.sizeOf s)) (Tm._sizeOf_inst.sizeOf t)) (fun s t ↦ instHAdd.hAdd (instHAdd.hAdd 1 (Tm._sizeOf_inst.sizeOf s)) (Tm._sizeOf_inst.sizeOf t)) (fun f f_ih ↦ instHAdd.hAdd 1 f_ih) (fun f g f_ih g_ih ↦ instHAdd.hAdd (instHAdd.hAdd 1 f_ih) g_ih) (fun f g f_ih g_ih ↦ instHAdd.hAdd (instHAdd.hAdd 1 f_ih) g_ih) (fun n f f_ih ↦ instHAdd.hAdd (instHAdd.hAdd 1 (instSizeOfNat.sizeOf n)) f_ih) t
```

### `Fml._sizeOf_inst`  (def, aux)

```
SizeOf Fml
:=
{ sizeOf := fun m ↦ m._sizeOf_1 }
```

### `Fml.holds._f`  (def, aux)

```
(x : Fml) → Fml.below (motive := fun x ↦ (Nat → Move) → Prop) x → (Nat → Move) → Prop
:=
fun x f x_1 ↦ Fml.holds.match_1 (fun x x_2 ↦ Fml.below (motive := fun x ↦ (Nat → Move) → Prop) x → Prop) x x_1 (fun s t r x ↦ Eq (s.eval r) (t.eval r)) (fun s t r x ↦ Eq (s.eval r).det (t.eval r).det) (fun f r x ↦ Not (x.1 r)) (fun f g r x ↦ And (x.1.1 r) (x.2.1 r)) (fun f g r x ↦ Or (x.1.1 r) (x.2.1 r)) (fun n f r x ↦ ∀ (m : Move), x.1 fun k ↦ ite (Eq k n) m (r k)) f
```

### `Fml.holds._sunfold`  (def, aux)

```
Fml → (Nat → Move) → Prop
:=
fun x x_1 ↦ Fml.holds.match_1 (fun x x_2 ↦ Prop) x x_1 (fun s t r ↦ Eq (s.eval r) (t.eval r)) (fun s t r ↦ Eq (s.eval r).det (t.eval r).det) (fun f r ↦ Not (f.holds r)) (fun f g r ↦ And (f.holds r) (g.holds r)) (fun f g r ↦ Or (f.holds r) (g.holds r)) fun n f r ↦ ∀ (m : Move), f.holds fun k ↦ ite (Eq k n) m (r k)
```

### `Fml.holds._unsafe_rec`  (def, aux)

```
Fml → (Nat → Move) → Prop
:=
fun x x_1 ↦ Fml.holds.match_1 (fun x x_2 ↦ Prop) x x_1 (fun s t r ↦ Eq (s.eval r) (t.eval r)) (fun s t r ↦ Eq (s.eval r).det (t.eval r).det) (fun f r ↦ Not (Fml.holds._unsafe_rec f r)) (fun f g r ↦ And (Fml.holds._unsafe_rec f r) (Fml.holds._unsafe_rec g r)) (fun f g r ↦ Or (Fml.holds._unsafe_rec f r) (Fml.holds._unsafe_rec g r)) fun n f r ↦ ∀ (m : Move), Fml.holds._unsafe_rec f fun k ↦ ite (Eq k n) m (r k)
```

### `Fml.holds.eq_1`  (theorem, aux)

```
∀ (x : Nat → Move) (s t : Tm), Eq ((Fml.eqT s t).holds x) (Eq (s.eval x) (t.eval x))
```

### `Fml.holds.eq_2`  (theorem, aux)

```
∀ (x : Nat → Move) (s t : Tm), Eq ((Fml.detT s t).holds x) (Eq (s.eval x).det (t.eval x).det)
```

### `Fml.holds.eq_3`  (theorem, aux)

```
∀ (x : Nat → Move) (f : Fml), Eq (f.neg.holds x) (Not (f.holds x))
```

### `Fml.holds.eq_4`  (theorem, aux)

```
∀ (x : Nat → Move) (f g : Fml), Eq ((f.andF g).holds x) (And (f.holds x) (g.holds x))
```

### `Fml.holds.eq_5`  (theorem, aux)

```
∀ (x : Nat → Move) (f g : Fml), Eq ((f.orF g).holds x) (Or (f.holds x) (g.holds x))
```

### `Fml.holds.eq_6`  (theorem, aux)

```
∀ (x : Nat → Move) (n : Nat) (f : Fml), Eq ((Fml.allF n f).holds x) (∀ (m : Move), f.holds fun k ↦ ite (Eq k n) m (x k))
```

### `Fml.holds.match_1`  (def, aux)

```
(motive : Fml → (Nat → Move) → Sort u_1) → (x : Fml) → (x_1 : Nat → Move) → ((s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) → ((s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) → ((f : Fml) → (r : Nat → Move) → motive f.neg r) → ((f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) → ((f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) → ((n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r) → motive x x_1
:=
fun motive x x_1 h_1 h_2 h_3 h_4 h_5 h_6 ↦ Fml.casesOn x (fun s t ↦ h_1 s t x_1) (fun s t ↦ h_2 s t x_1) (fun f ↦ h_3 f x_1) (fun f g ↦ h_4 f g x_1) (fun f g ↦ h_5 f g x_1) fun n f ↦ h_6 n f x_1
```

### `Move._sizeOf_1`  (def, aux)

```
Move → Nat
:=
fun t ↦ Move.rec 1 1 1 1 t
```

### `Move._sizeOf_inst`  (def, aux)

```
SizeOf Move
:=
{ sizeOf := fun m ↦ m._sizeOf_1 }
```

### `Move.a.eq_1`  (theorem, aux)

```
Eq Move.I.a 1
```

### `Move.a.eq_2`  (theorem, aux)

```
Eq Move.sv.a (-1)
```

### `Move.a.eq_3`  (theorem, aux)

```
Eq Move.sh.a 1
```

### `Move.a.eq_4`  (theorem, aux)

```
Eq Move.C2.a (-1)
```

### `Move.act.eq_1`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Move.I.act { fst := x_2, snd := y }) { fst := x_2, snd := y }
```

### `Move.act.eq_2`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Move.sv.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg x_2, snd := y }
```

### `Move.act.eq_3`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Move.sh.act { fst := x_2, snd := y }) { fst := x_2, snd := Int.instNegInt.neg y }
```

### `Move.act.eq_4`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Move.C2.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg x_2, snd := Int.instNegInt.neg y }
```

### `Move.act.match_1`  (def, aux)

```
(motive : Move → Pt → Sort u_1) → (x : Move) → (x_1 : Pt) → ((x y : Int) → motive Move.I { fst := x, snd := y }) → ((x y : Int) → motive Move.sv { fst := x, snd := y }) → ((x y : Int) → motive Move.sh { fst := x, snd := y }) → ((x y : Int) → motive Move.C2 { fst := x, snd := y }) → motive x x_1
:=
fun motive x x_1 h_1 h_2 h_3 h_4 ↦ Move.casesOn x (Prod.casesOn x_1 fun fst snd ↦ h_1 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_2 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_3 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_4 fst snd)
```

### `Move.b.eq_1`  (theorem, aux)

```
Eq Move.I.b 0
```

### `Move.b.eq_2`  (theorem, aux)

```
Eq Move.sv.b 0
```

### `Move.b.eq_3`  (theorem, aux)

```
Eq Move.sh.b 0
```

### `Move.b.eq_4`  (theorem, aux)

```
Eq Move.C2.b 0
```

### `Move.c.eq_1`  (theorem, aux)

```
Eq Move.I.c 0
```

### `Move.c.eq_2`  (theorem, aux)

```
Eq Move.sv.c 0
```

### `Move.c.eq_3`  (theorem, aux)

```
Eq Move.sh.c 0
```

### `Move.c.eq_4`  (theorem, aux)

```
Eq Move.C2.c 0
```

### `Move.d.eq_1`  (theorem, aux)

```
Eq Move.I.d 1
```

### `Move.d.eq_2`  (theorem, aux)

```
Eq Move.sv.d 1
```

### `Move.d.eq_3`  (theorem, aux)

```
Eq Move.sh.d (-1)
```

### `Move.d.eq_4`  (theorem, aux)

```
Eq Move.C2.d (-1)
```

### `Move.decidableForall._proof_1`  (theorem, aux)

```
∀ (p : Move → Prop), p Move.I → p Move.sv → p Move.sh → p Move.C2 → ∀ (g : Move), p g
```

### `Move.decidableForall._proof_2`  (theorem, aux)

```
∀ (p : Move → Prop), Not (p Move.C2) → (∀ (g : Move), p g) → False
```

### `Move.decidableForall._proof_3`  (theorem, aux)

```
∀ (p : Move → Prop), Not (p Move.sh) → (∀ (g : Move), p g) → False
```

### `Move.decidableForall._proof_4`  (theorem, aux)

```
∀ (p : Move → Prop), Not (p Move.sv) → (∀ (g : Move), p g) → False
```

### `Move.decidableForall._proof_5`  (theorem, aux)

```
∀ (p : Move → Prop), Not (p Move.I) → (∀ (g : Move), p g) → False
```

### `Move.mul.eq_1`  (theorem, aux)

```
Eq (Move.I.mul Move.I) Move.I
```

### `Move.mul.eq_10`  (theorem, aux)

```
Eq (Move.sh.mul Move.sv) Move.C2
```

### `Move.mul.eq_11`  (theorem, aux)

```
Eq (Move.sh.mul Move.sh) Move.I
```

### `Move.mul.eq_12`  (theorem, aux)

```
Eq (Move.sh.mul Move.C2) Move.sv
```

### `Move.mul.eq_13`  (theorem, aux)

```
Eq (Move.C2.mul Move.I) Move.C2
```

### `Move.mul.eq_14`  (theorem, aux)

```
Eq (Move.C2.mul Move.sv) Move.sh
```

### `Move.mul.eq_15`  (theorem, aux)

```
Eq (Move.C2.mul Move.sh) Move.sv
```

### `Move.mul.eq_16`  (theorem, aux)

```
Eq (Move.C2.mul Move.C2) Move.I
```

### `Move.mul.eq_2`  (theorem, aux)

```
Eq (Move.I.mul Move.sv) Move.sv
```

### `Move.mul.eq_3`  (theorem, aux)

```
Eq (Move.I.mul Move.sh) Move.sh
```

### `Move.mul.eq_4`  (theorem, aux)

```
Eq (Move.I.mul Move.C2) Move.C2
```

### `Move.mul.eq_5`  (theorem, aux)

```
Eq (Move.sv.mul Move.I) Move.sv
```

### `Move.mul.eq_6`  (theorem, aux)

```
Eq (Move.sv.mul Move.sv) Move.I
```

### `Move.mul.eq_7`  (theorem, aux)

```
Eq (Move.sv.mul Move.sh) Move.C2
```

### `Move.mul.eq_8`  (theorem, aux)

```
Eq (Move.sv.mul Move.C2) Move.sh
```

### `Move.mul.eq_9`  (theorem, aux)

```
Eq (Move.sh.mul Move.I) Move.sh
```

### `Move.mul.match_1`  (def, aux)

```
(motive : Move → Move → Sort u_1) → (x x_1 : Move) → (Unit → motive Move.I Move.I) → (Unit → motive Move.I Move.sv) → (Unit → motive Move.I Move.sh) → (Unit → motive Move.I Move.C2) → (Unit → motive Move.sv Move.I) → (Unit → motive Move.sv Move.sv) → (Unit → motive Move.sv Move.sh) → (Unit → motive Move.sv Move.C2) → (Unit → motive Move.sh Move.I) → (Unit → motive Move.sh Move.sv) → (Unit → motive Move.sh Move.sh) → (Unit → motive Move.sh Move.C2) → (Unit → motive Move.C2 Move.I) → (Unit → motive Move.C2 Move.sv) → (Unit → motive Move.C2 Move.sh) → (Unit → motive Move.C2 Move.C2) → motive x x_1
:=
fun motive x x_1 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16 ↦ Move.casesOn x (Move.casesOn x_1 (h_1 Unit.unit) (h_2 Unit.unit) (h_3 Unit.unit) (h_4 Unit.unit)) (Move.casesOn x_1 (h_5 Unit.unit) (h_6 Unit.unit) (h_7 Unit.unit) (h_8 Unit.unit)) (Move.casesOn x_1 (h_9 Unit.unit) (h_10 Unit.unit) (h_11 Unit.unit) (h_12 Unit.unit)) (Move.casesOn x_1 (h_13 Unit.unit) (h_14 Unit.unit) (h_15 Unit.unit) (h_16 Unit.unit))
```

### `MoveSet._sizeOf_1`  (def, aux)

```
MoveSet → Nat
:=
fun t ↦ MoveSet.rec (fun hasI hasSv hasSh hasC2 ↦ instHAdd.hAdd (instHAdd.hAdd (instHAdd.hAdd (instHAdd.hAdd 1 (Bool._sizeOf_inst.sizeOf hasI)) (Bool._sizeOf_inst.sizeOf hasSv)) (Bool._sizeOf_inst.sizeOf hasSh)) (Bool._sizeOf_inst.sizeOf hasC2)) t
```

### `MoveSet._sizeOf_inst`  (def, aux)

```
SizeOf MoveSet
:=
{ sizeOf := fun m ↦ m._sizeOf_1 }
```

### `MoveSet.mem.eq_1`  (theorem, aux)

```
∀ (s : MoveSet), Eq (s.mem Move.I) s.hasI
```

### `MoveSet.mem.eq_2`  (theorem, aux)

```
∀ (s : MoveSet), Eq (s.mem Move.sv) s.hasSv
```

### `MoveSet.mem.eq_3`  (theorem, aux)

```
∀ (s : MoveSet), Eq (s.mem Move.sh) s.hasSh
```

### `MoveSet.mem.eq_4`  (theorem, aux)

```
∀ (s : MoveSet), Eq (s.mem Move.C2) s.hasC2
```

### `MoveSet.mk._flat_ctor`  (def, aux)

```
Bool → Bool → Bool → Bool → MoveSet
:=
fun hasI hasSv hasSh hasC2 ↦ { hasI := hasI, hasSv := hasSv, hasSh := hasSh, hasC2 := hasC2 }
```

### `R90.eq_1`  (theorem, aux)

```
∀ (p : Pt), Eq (R90 p) { fst := Int.instNegInt.neg p.snd, snd := p.fst }
```

### `R90inv.eq_1`  (theorem, aux)

```
∀ (p : Pt), Eq (R90inv p) { fst := p.snd, snd := Int.instNegInt.neg p.fst }
```

### `S2_mem_mark._simp_1_1`  (theorem, aux)

```
∀ {α : Type u_1} {a : α} {s t : List α}, Eq (List.instMembership.mem (instHAppendOfAppend.hAppend s t) a) (Or (List.instMembership.mem s a) (List.instMembership.mem t a))
```

### `S2_mem_mark._simp_1_2`  (theorem, aux)

```
∀ {α : Type u_1} {β : Type u_2} {b : β} {f : α → β} {l : List α}, Eq (List.instMembership.mem (List.map f l) b) (Exists fun a ↦ And (List.instMembership.mem l a) (Eq (f a) b))
```

### `S2_quadrant_mark_exact._proof_1_1`  (theorem, aux)

```
∀ (x y : Int), And (Int.instLTInt.lt 0 { fst := x, snd := y }.fst) (Int.instLTInt.lt 0 { fst := x, snd := y }.snd) → Not (Int.instLTInt.lt (Int.instNegInt.neg x) 0) → False
```

### `S2_quadrant_mark_exact._proof_1_2`  (theorem, aux)

```
∀ (x y : Int), And (Int.instLTInt.lt 0 { fst := x, snd := y }.fst) (Int.instLTInt.lt 0 { fst := x, snd := y }.snd) → Not (Int.instLTInt.lt (Int.instNegInt.neg y) 0) → False
```

### `S2_quadrant_mark_exact._proof_1_3`  (theorem, aux)

```
∀ (x y : Int), Int.instLTInt.lt 0 { fst := x, snd := y }.snd → Int.instLTInt.lt 0 (Int.instNegInt.neg y) → False
```

### `S2_quadrant_mark_exact._proof_1_4`  (theorem, aux)

```
∀ (x y : Int), Int.instLTInt.lt 0 { fst := x, snd := y }.fst → Int.instLTInt.lt 0 (Int.instNegInt.neg x) → False
```

### `S2_quadrant_mark_exact._proof_1_5`  (theorem, aux)

```
∀ (x y : Int), Or (And (Int.instLTInt.lt 0 x) (Int.instLTInt.lt 0 y)) (And (Int.instLTInt.lt x 0) (Int.instLTInt.lt y 0)) → Or (And (Int.instLTInt.lt 0 (Int.instNegInt.neg x)) (Int.instLTInt.lt 0 y)) (And (Int.instLTInt.lt (Int.instNegInt.neg x) 0) (Int.instLTInt.lt y 0)) → False
```

### `S2_quadrant_mark_exact._proof_1_6`  (theorem, aux)

```
∀ (x y : Int), Or (And (Int.instLTInt.lt 0 x) (Int.instLTInt.lt 0 y)) (And (Int.instLTInt.lt x 0) (Int.instLTInt.lt y 0)) → Or (And (Int.instLTInt.lt 0 x) (Int.instLTInt.lt 0 (Int.instNegInt.neg y))) (And (Int.instLTInt.lt x 0) (Int.instLTInt.lt (Int.instNegInt.neg y) 0)) → False
```

### `S4_act_matrix._proof_1_20`  (theorem, aux)

```
∀ (x y : Int), Not (Eq x (instHAdd.hAdd (instHMul.hMul 1 x) (instHMul.hMul 0 y))) → False
```

### `S4_act_matrix._proof_1_21`  (theorem, aux)

```
∀ (x y : Int), Not (Eq y (instHAdd.hAdd (instHMul.hMul 0 x) (instHMul.hMul 1 y))) → False
```

### `S4_act_matrix._proof_1_22`  (theorem, aux)

```
∀ (x y : Int), Not (Eq (Int.instNegInt.neg y) (instHAdd.hAdd (instHMul.hMul 0 x) (instHMul.hMul (-1) y))) → False
```

### `S4_act_matrix._proof_1_23`  (theorem, aux)

```
∀ (x y : Int), Not (Eq (Int.instNegInt.neg x) (instHAdd.hAdd (instHMul.hMul (-1) x) (instHMul.hMul 0 y))) → False
```

### `S4_corner_maps._proof_1_11`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq (Int.instNegInt.neg y) 1) (Eq (Int.instNegInt.neg y) (-1))) (Or (Eq x 1) (Eq x (-1)))) → False
```

### `S4_corner_maps._proof_1_12`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq (Int.instNegInt.neg x) 1) (Eq (Int.instNegInt.neg x) (-1))) (Or (Eq (Int.instNegInt.neg y) 1) (Eq (Int.instNegInt.neg y) (-1)))) → False
```

### `S4_corner_maps._proof_1_13`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq y 1) (Eq y (-1))) (Or (Eq (Int.instNegInt.neg x) 1) (Eq (Int.instNegInt.neg x) (-1)))) → False
```

### `S4_corner_maps._proof_1_14`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq (Int.instNegInt.neg x) 1) (Eq (Int.instNegInt.neg x) (-1))) (Or (Eq y 1) (Eq y (-1)))) → False
```

### `S4_corner_maps._proof_1_15`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq x 1) (Eq x (-1))) (Or (Eq (Int.instNegInt.neg y) 1) (Eq (Int.instNegInt.neg y) (-1)))) → False
```

### `S4_corner_maps._proof_1_16`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq y 1) (Eq y (-1))) (Or (Eq x 1) (Eq x (-1)))) → False
```

### `S4_corner_maps._proof_1_17`  (theorem, aux)

```
∀ (x y : Int), And (Or (Eq x 1) (Eq x (-1))) (Or (Eq y 1) (Eq y (-1))) → Not (And (Or (Eq (Int.instNegInt.neg y) 1) (Eq (Int.instNegInt.neg y) (-1))) (Or (Eq (Int.instNegInt.neg x) 1) (Eq (Int.instNegInt.neg x) (-1)))) → False
```

### `S4_entries._proof_1_10`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_11`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_12`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) (-1)) → False
```

### `S4_entries._proof_1_13`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) (-1)) → False
```

### `S4_entries._proof_1_14`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_15`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) (-1)) → False
```

### `S4_entries._proof_1_16`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_17`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_18`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) (-1)) → False
```

### `S4_entries._proof_1_3`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) (-1)) → False
```

### `S4_entries._proof_1_4`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_5`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_6`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d (-1))) (-1)) → False
```

### `S4_entries._proof_1_7`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d 1)) (-1)) → Not (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 0) (And (Eq b (-1)) (And (Eq c 1) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c (-1)) (Eq d 0)))) (Or (And (Eq a (-1)) (And (Eq b 0) (And (Eq c 0) (Eq d 1)))) (Or (And (Eq a 1) (And (Eq b 0) (And (Eq c 0) (Eq d (-1))))) (Or (And (Eq a 0) (And (Eq b 1) (And (Eq c 1) (Eq d 0)))) (And (Eq a 0) (And (Eq b (-1)) (And (Eq c (-1)) (Eq d 0))))))))))) → False
```

### `S4_entries._proof_1_8`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) (-1)) → False
```

### `S4_entries._proof_1_9`  (theorem, aux)

```
∀ (a b c d : Int), And (Eq (instHAdd.hAdd (instHMul.hMul a 1) (instHMul.hMul b (-1))) 1) (Eq (instHAdd.hAdd (instHMul.hMul c 1) (instHMul.hMul d (-1))) 1) → And (Eq (instHAdd.hAdd (instHMul.hMul a (-1)) (instHMul.hMul b 1)) 1) (Eq (instHAdd.hAdd (instHMul.hMul c (-1)) (instHMul.hMul d 1)) (-1)) → False
```

### `S4_matAct_add._proof_1_2`  (theorem, aux)

```
∀ (a b : Int) (p q : Pt), Not (Eq (instHAdd.hAdd (instHAdd.hAdd (instHMul.hMul a p.fst) (instHMul.hMul a q.fst)) (instHAdd.hAdd (instHMul.hMul b p.snd) (instHMul.hMul b q.snd))) (instHAdd.hAdd (instHAdd.hAdd (instHMul.hMul a p.fst) (instHMul.hMul b p.snd)) (instHAdd.hAdd (instHMul.hMul a q.fst) (instHMul.hMul b q.snd)))) → False
```

### `Sq._sizeOf_1`  (def, aux)

```
Sq → Nat
:=
fun t ↦ Sq.rec 1 1 1 1 1 1 1 1 t
```

### `Sq._sizeOf_inst`  (def, aux)

```
SizeOf Sq
:=
{ sizeOf := fun m ↦ m._sizeOf_1 }
```

### `Sq.act.eq_1`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.id.act { fst := x_2, snd := y }) { fst := x_2, snd := y }
```

### `Sq.act.eq_2`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.rot90.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg y, snd := x_2 }
```

### `Sq.act.eq_3`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.rot180.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg x_2, snd := Int.instNegInt.neg y }
```

### `Sq.act.eq_4`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.rot270.act { fst := x_2, snd := y }) { fst := y, snd := Int.instNegInt.neg x_2 }
```

### `Sq.act.eq_5`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.mirV.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg x_2, snd := y }
```

### `Sq.act.eq_6`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.mirH.act { fst := x_2, snd := y }) { fst := x_2, snd := Int.instNegInt.neg y }
```

### `Sq.act.eq_7`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.mirD.act { fst := x_2, snd := y }) { fst := y, snd := x_2 }
```

### `Sq.act.eq_8`  (theorem, aux)

```
∀ (x_2 y : Int), Eq (Sq.mirA.act { fst := x_2, snd := y }) { fst := Int.instNegInt.neg y, snd := Int.instNegInt.neg x_2 }
```

### `Sq.act.match_1`  (def, aux)

```
(motive : Sq → Pt → Sort u_1) → (x : Sq) → (x_1 : Pt) → ((x y : Int) → motive Sq.id { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot90 { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot180 { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot270 { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirV { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirH { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirD { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirA { fst := x, snd := y }) → motive x x_1
:=
fun motive x x_1 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 ↦ Sq.casesOn x (Prod.casesOn x_1 fun fst snd ↦ h_1 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_2 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_3 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_4 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_5 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_6 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_7 fst snd) (Prod.casesOn x_1 fun fst snd ↦ h_8 fst snd)
```

### `Sq.comp.eq_1`  (theorem, aux)

```
Eq (Sq.id.comp Sq.id) Sq.id
```

### `Sq.comp.eq_10`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.rot90) Sq.rot180
```

### `Sq.comp.eq_11`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.rot180) Sq.rot270
```

### `Sq.comp.eq_12`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.rot270) Sq.id
```

### `Sq.comp.eq_13`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.mirV) Sq.mirA
```

### `Sq.comp.eq_14`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.mirH) Sq.mirD
```

### `Sq.comp.eq_15`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.mirD) Sq.mirV
```

### `Sq.comp.eq_16`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.mirA) Sq.mirH
```

### `Sq.comp.eq_17`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.id) Sq.rot180
```

### `Sq.comp.eq_18`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.rot90) Sq.rot270
```

### `Sq.comp.eq_19`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.rot180) Sq.id
```

### `Sq.comp.eq_2`  (theorem, aux)

```
Eq (Sq.id.comp Sq.rot90) Sq.rot90
```

### `Sq.comp.eq_20`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.rot270) Sq.rot90
```

### `Sq.comp.eq_21`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.mirV) Sq.mirH
```

### `Sq.comp.eq_22`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.mirH) Sq.mirV
```

### `Sq.comp.eq_23`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.mirD) Sq.mirA
```

### `Sq.comp.eq_24`  (theorem, aux)

```
Eq (Sq.rot180.comp Sq.mirA) Sq.mirD
```

### `Sq.comp.eq_25`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.id) Sq.rot270
```

### `Sq.comp.eq_26`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.rot90) Sq.id
```

### `Sq.comp.eq_27`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.rot180) Sq.rot90
```

### `Sq.comp.eq_28`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.rot270) Sq.rot180
```

### `Sq.comp.eq_29`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.mirV) Sq.mirD
```

### `Sq.comp.eq_3`  (theorem, aux)

```
Eq (Sq.id.comp Sq.rot180) Sq.rot180
```

### `Sq.comp.eq_30`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.mirH) Sq.mirA
```

### `Sq.comp.eq_31`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.mirD) Sq.mirH
```

### `Sq.comp.eq_32`  (theorem, aux)

```
Eq (Sq.rot270.comp Sq.mirA) Sq.mirV
```

### `Sq.comp.eq_33`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.id) Sq.mirV
```

### `Sq.comp.eq_34`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.rot90) Sq.mirD
```

### `Sq.comp.eq_35`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.rot180) Sq.mirH
```

### `Sq.comp.eq_36`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.rot270) Sq.mirA
```

### `Sq.comp.eq_37`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.mirV) Sq.id
```

### `Sq.comp.eq_38`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.mirH) Sq.rot180
```

### `Sq.comp.eq_39`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.mirD) Sq.rot90
```

### `Sq.comp.eq_4`  (theorem, aux)

```
Eq (Sq.id.comp Sq.rot270) Sq.rot270
```

### `Sq.comp.eq_40`  (theorem, aux)

```
Eq (Sq.mirV.comp Sq.mirA) Sq.rot270
```

### `Sq.comp.eq_41`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.id) Sq.mirH
```

### `Sq.comp.eq_42`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.rot90) Sq.mirA
```

### `Sq.comp.eq_43`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.rot180) Sq.mirV
```

### `Sq.comp.eq_44`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.rot270) Sq.mirD
```

### `Sq.comp.eq_45`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.mirV) Sq.rot180
```

### `Sq.comp.eq_46`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.mirH) Sq.id
```

### `Sq.comp.eq_47`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.mirD) Sq.rot270
```

### `Sq.comp.eq_48`  (theorem, aux)

```
Eq (Sq.mirH.comp Sq.mirA) Sq.rot90
```

### `Sq.comp.eq_49`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.id) Sq.mirD
```

### `Sq.comp.eq_5`  (theorem, aux)

```
Eq (Sq.id.comp Sq.mirV) Sq.mirV
```

### `Sq.comp.eq_50`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.rot90) Sq.mirH
```

### `Sq.comp.eq_51`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.rot180) Sq.mirA
```

### `Sq.comp.eq_52`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.rot270) Sq.mirV
```

### `Sq.comp.eq_53`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.mirV) Sq.rot270
```

### `Sq.comp.eq_54`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.mirH) Sq.rot90
```

### `Sq.comp.eq_55`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.mirD) Sq.id
```

### `Sq.comp.eq_56`  (theorem, aux)

```
Eq (Sq.mirD.comp Sq.mirA) Sq.rot180
```

### `Sq.comp.eq_57`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.id) Sq.mirA
```

### `Sq.comp.eq_58`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.rot90) Sq.mirV
```

### `Sq.comp.eq_59`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.rot180) Sq.mirD
```

### `Sq.comp.eq_6`  (theorem, aux)

```
Eq (Sq.id.comp Sq.mirH) Sq.mirH
```

### `Sq.comp.eq_60`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.rot270) Sq.mirH
```

### `Sq.comp.eq_61`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.mirV) Sq.rot90
```

### `Sq.comp.eq_62`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.mirH) Sq.rot270
```

### `Sq.comp.eq_63`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.mirD) Sq.rot180
```

### `Sq.comp.eq_64`  (theorem, aux)

```
Eq (Sq.mirA.comp Sq.mirA) Sq.id
```

### `Sq.comp.eq_7`  (theorem, aux)

```
Eq (Sq.id.comp Sq.mirD) Sq.mirD
```

### `Sq.comp.eq_8`  (theorem, aux)

```
Eq (Sq.id.comp Sq.mirA) Sq.mirA
```

### `Sq.comp.eq_9`  (theorem, aux)

```
Eq (Sq.rot90.comp Sq.id) Sq.rot90
```

### `Sq.comp.match_1`  (def, aux)

```
(motive : Sq → Sq → Sort u_1) → (x x_1 : Sq) → (Unit → motive Sq.id Sq.id) → (Unit → motive Sq.id Sq.rot90) → (Unit → motive Sq.id Sq.rot180) → (Unit → motive Sq.id Sq.rot270) → (Unit → motive Sq.id Sq.mirV) → (Unit → motive Sq.id Sq.mirH) → (Unit → motive Sq.id Sq.mirD) → (Unit → motive Sq.id Sq.mirA) → (Unit → motive Sq.rot90 Sq.id) → (Unit → motive Sq.rot90 Sq.rot90) → (Unit → motive Sq.rot90 Sq.rot180) → (Unit → motive Sq.rot90 Sq.rot270) → (Unit → motive Sq.rot90 Sq.mirV) → (Unit → motive Sq.rot90 Sq.mirH) → (Unit → motive Sq.rot90 Sq.mirD) → (Unit → motive Sq.rot90 Sq.mirA) → (Unit → motive Sq.rot180 Sq.id) → (Unit → motive Sq.rot180 Sq.rot90) → (Unit → motive Sq.rot180 Sq.rot180) → (Unit → motive Sq.rot180 Sq.rot270) → (Unit → motive Sq.rot180 Sq.mirV) → (Unit → motive Sq.rot180 Sq.mirH) → (Unit → motive Sq.rot180 Sq.mirD) → (Unit → motive Sq.rot180 Sq.mirA) → (Unit → motive Sq.rot270 Sq.id) → (Unit → motive Sq.rot270 Sq.rot90) → (Unit → motive Sq.rot270 Sq.rot180) → (Unit → motive Sq.rot270 Sq.rot270) → (Unit → motive Sq.rot270 Sq.mirV) → (Unit → motive Sq.rot270 Sq.mirH) → (Unit → motive Sq.rot270 Sq.mirD) → (Unit → motive Sq.rot270 Sq.mirA) → (Unit → motive Sq.mirV Sq.id) → (Unit → motive Sq.mirV Sq.rot90) → (Unit → motive Sq.mirV Sq.rot180) → (Unit → motive Sq.mirV Sq.rot270) → (Unit → motive Sq.mirV Sq.mirV) → (Unit → motive Sq.mirV Sq.mirH) → (Unit → motive Sq.mirV Sq.mirD) → (Unit → motive Sq.mirV Sq.mirA) → (Unit → motive Sq.mirH Sq.id) → (Unit → motive Sq.mirH Sq.rot90) → (Unit → motive Sq.mirH Sq.rot180) → (Unit → motive Sq.mirH Sq.rot270) → (Unit → motive Sq.mirH Sq.mirV) → (Unit → motive Sq.mirH Sq.mirH) → (Unit → motive Sq.mirH Sq.mirD) → (Unit → motive Sq.mirH Sq.mirA) → (Unit → motive Sq.mirD Sq.id) → ⋯
:=
fun motive x x_1 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16 h_17 h_18 h_19 h_20 h_21 h_22 h_23 h_24 h_25 h_26 h_27 h_28 h_29 h_30 h_31 h_32 h_33 h_34 h_35 h_36 h_37 h_38 h_39 h_40 h_41 h_42 h_43 h_44 h_45 h_46 h_47 h_48 h_49 h_50 h_51 h_52 h_53 h_54 h_55 h_56 h_57 h_58 h_59 h_60 h_61 h_62 h_63 h_64 ↦ Sq.casesOn x (Sq.casesOn x_1 (h_1 Unit.unit) (h_2 Unit.unit) (h_3 Unit.unit) (h_4 Unit.unit) (h_5 Unit.unit) (h_6 Unit.unit) (h_7 Unit.unit) (h_8 Unit.unit)) (Sq.casesOn x_1 (h_9 Unit.unit) (h_10 Unit.unit) (h_11 Unit.unit) (h_12 Unit.unit) (h_13 Unit.unit) (h_14 Unit.unit) (h_15 Unit.unit) (h_16 Unit.unit)) (Sq.casesOn x_1 (h_17 Unit.unit) (h_18 Unit.unit) (h_19 Unit.unit) (h_20 Unit.unit) (h_21 Unit.unit) (h_22 Unit.unit) (h_23 Unit.unit) (h_24 Unit.unit)) (Sq.casesOn x_1 (h_25 Unit.unit) (h_26 Unit.unit) (h_27 Unit.unit) (h_28 Unit.unit) (h_29 Unit.unit) (h_30 Unit.unit) (h_31 Unit.unit) (h_32 Unit.unit)) (Sq.casesOn x_1 (h_33 Unit.unit) (h_34 Unit.unit) (h_35 Unit.unit) (h_36 Unit.unit) (h_37 Unit.unit) (h_38 Unit.unit) (h_39 Unit.unit) (h_40 Unit.unit)) (Sq.casesOn x_1 (h_41 Unit.unit) (h_42 Unit.unit) (h_43 Unit.unit) (h_44 Unit.unit) (h_45 Unit.unit) (h_46 Unit.unit) (h_47 Unit.unit) (h_48 Unit.unit)) (Sq.casesOn x_1 (h_49 Unit.unit) (h_50 Unit.unit) (h_51 Unit.unit) (h_52 Unit.unit) (h_53 Unit.unit) (h_54 Unit.unit) (h_55 Unit.unit) (h_56 Unit.unit)) (Sq.casesOn x_1 (h_57 Unit.unit) (h_58 Unit.unit) (h_59 Unit.unit) (h_60 Unit.unit) (h_61 Unit.unit) (h_62 Unit.unit) (h_63 Unit.unit) (h_64 Unit.unit))
```

### `Sq.inv.eq_1`  (theorem, aux)

```
Eq Sq.id.inv Sq.id
```

### `Sq.inv.eq_2`  (theorem, aux)

```
Eq Sq.rot90.inv Sq.rot270
```

### `Sq.inv.eq_3`  (theorem, aux)

```
Eq Sq.rot180.inv Sq.rot180
```

### `Sq.inv.eq_4`  (theorem, aux)

```
Eq Sq.rot270.inv Sq.rot90
```

### `Sq.inv.eq_5`  (theorem, aux)

```
Eq Sq.mirV.inv Sq.mirV
```

### `Sq.inv.eq_6`  (theorem, aux)

```
Eq Sq.mirH.inv Sq.mirH
```

### `Sq.inv.eq_7`  (theorem, aux)

```
Eq Sq.mirD.inv Sq.mirD
```

### `Sq.inv.eq_8`  (theorem, aux)

```
Eq Sq.mirA.inv Sq.mirA
```

### `Sq.mat.eq_1`  (theorem, aux)

```
Eq Sq.id.mat { fst := 1, snd := { fst := 0, snd := { fst := 0, snd := 1 } } }
```

### `Sq.mat.eq_2`  (theorem, aux)

```
Eq Sq.rot90.mat { fst := 0, snd := { fst := -1, snd := { fst := 1, snd := 0 } } }
```

### `Sq.mat.eq_3`  (theorem, aux)

```
Eq Sq.rot180.mat { fst := -1, snd := { fst := 0, snd := { fst := 0, snd := -1 } } }
```

### `Sq.mat.eq_4`  (theorem, aux)

```
Eq Sq.rot270.mat { fst := 0, snd := { fst := 1, snd := { fst := -1, snd := 0 } } }
```

### `Sq.mat.eq_5`  (theorem, aux)

```
Eq Sq.mirV.mat { fst := -1, snd := { fst := 0, snd := { fst := 0, snd := 1 } } }
```

### `Sq.mat.eq_6`  (theorem, aux)

```
Eq Sq.mirH.mat { fst := 1, snd := { fst := 0, snd := { fst := 0, snd := -1 } } }
```

### `Sq.mat.eq_7`  (theorem, aux)

```
Eq Sq.mirD.mat { fst := 0, snd := { fst := 1, snd := { fst := 1, snd := 0 } } }
```

### `Sq.mat.eq_8`  (theorem, aux)

```
Eq Sq.mirA.mat { fst := 0, snd := { fst := -1, snd := { fst := -1, snd := 0 } } }
```

### `T3_act_matrix._proof_1_23`  (theorem, aux)

```
∀ (x y : Int), Not (Eq x (instHAdd.hAdd (instHMul.hMul 1 x) (instHMul.hMul 0 y))) → False
```

### `T3_act_matrix._proof_1_24`  (theorem, aux)

```
∀ (x y : Int), Not (Eq y (instHAdd.hAdd (instHMul.hMul 0 x) (instHMul.hMul 1 y))) → False
```

### `T3_act_matrix._proof_1_25`  (theorem, aux)

```
∀ (x y : Int), Not (Eq (Int.instNegInt.neg x) (instHAdd.hAdd (instHMul.hMul (-1) x) (instHMul.hMul 0 y))) → False
```

### `T3_act_matrix._proof_1_26`  (theorem, aux)

```
∀ (x y : Int), Not (Eq (Int.instNegInt.neg y) (instHAdd.hAdd (instHMul.hMul 0 x) (instHMul.hMul (-1) y))) → False
```

### `T4_fix_C2._proof_1_1`  (theorem, aux)

```
∀ (x y : Int), Not (Iff (And (Eq (Int.instNegInt.neg x) x) (Eq (Int.instNegInt.neg y) y)) (And (Eq x 0) (Eq y 0))) → False
```

### `T4_fix_sh._proof_1_1`  (theorem, aux)

```
∀ (x y : Int), Not (Iff (And (Eq x x) (Eq (Int.instNegInt.neg y) y)) (Eq y 0)) → False
```

### `T4_fix_sv._proof_1_1`  (theorem, aux)

```
∀ (x y : Int), Not (Iff (And (Eq (Int.instNegInt.neg x) x) (Eq y y)) (Eq x 0)) → False
```

### `Tm._sizeOf_1`  (def, aux)

```
Tm → Nat
:=
fun t ↦ Tm.rec (fun n ↦ instHAdd.hAdd 1 (instSizeOfNat.sizeOf n)) 1 (fun s t s_ih t_ih ↦ instHAdd.hAdd (instHAdd.hAdd 1 s_ih) t_ih) t
```

### `Tm._sizeOf_inst`  (def, aux)

```
SizeOf Tm
:=
{ sizeOf := fun m ↦ m._sizeOf_1 }
```

### `Tm.eval._f`  (def, aux)

```
(x : Tm) → Tm.below (motive := fun x ↦ (Nat → Move) → Move) x → (Nat → Move) → Move
:=
fun x f x_1 ↦ Tm.eval.match_1 (fun x x_2 ↦ Tm.below (motive := fun x ↦ (Nat → Move) → Move) x → Move) x x_1 (fun n r x ↦ r n) (fun x x_2 ↦ Move.I) (fun s t r x ↦ (x.1.1 r).mul (x.2.1 r)) f
```

### `Tm.eval._sunfold`  (def, aux)

```
Tm → (Nat → Move) → Move
:=
fun x x_1 ↦ Tm.eval.match_1 (fun x x_2 ↦ Move) x x_1 (fun n r ↦ r n) (fun x ↦ Move.I) fun s t r ↦ (s.eval r).mul (t.eval r)
```

### `Tm.eval._unsafe_rec`  (def, aux)

```
Tm → (Nat → Move) → Move
:=
fun x x_1 ↦ Tm.eval.match_1 (fun x x_2 ↦ Move) x x_1 (fun n r ↦ r n) (fun x ↦ Move.I) fun s t r ↦ (Tm.eval._unsafe_rec s r).mul (Tm.eval._unsafe_rec t r)
```

### `Tm.eval.eq_1`  (theorem, aux)

```
∀ (x : Nat → Move) (n : Nat), Eq ((Tm.var n).eval x) (x n)
```

### `Tm.eval.eq_2`  (theorem, aux)

```
∀ (x : Nat → Move), Eq (Tm.one.eval x) Move.I
```

### `Tm.eval.eq_3`  (theorem, aux)

```
∀ (x : Nat → Move) (s t : Tm), Eq ((s.mulT t).eval x) ((s.eval x).mul (t.eval x))
```

### `Tm.eval.match_1`  (def, aux)

```
(motive : Tm → (Nat → Move) → Sort u_1) → (x : Tm) → (x_1 : Nat → Move) → ((n : Nat) → (r : Nat → Move) → motive (Tm.var n) r) → ((x : Nat → Move) → motive Tm.one x) → ((s t : Tm) → (r : Nat → Move) → motive (s.mulT t) r) → motive x x_1
:=
fun motive x x_1 h_1 h_2 h_3 ↦ Tm.casesOn x (fun n ↦ h_1 n x_1) (h_2 x_1) fun s t ↦ h_3 s t x_1
```

### `_private.Subject.0.Fml.holds.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (s t : Tm) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive (Fml.eqT s t) r h_1 h_2 h_3 h_4 h_5 h_6) (h_1 s t r)
```

### `_private.Subject.0.Fml.holds.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (s t : Tm) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive (Fml.detT s t) r h_1 h_2 h_3 h_4 h_5 h_6) (h_2 s t r)
```

### `_private.Subject.0.Fml.holds.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (f : Fml) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive f.neg r h_1 h_2 h_3 h_4 h_5 h_6) (h_3 f r)
```

### `_private.Subject.0.Fml.holds.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (f g : Fml) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive (f.andF g) r h_1 h_2 h_3 h_4 h_5 h_6) (h_4 f g r)
```

### `_private.Subject.0.Fml.holds.match_1.eq_5`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (f g : Fml) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive (f.orF g) r h_1 h_2 h_3 h_4 h_5 h_6) (h_5 f g r)
```

### `_private.Subject.0.Fml.holds.match_1.eq_6`  (theorem, aux)

```
∀ (motive : Fml → (Nat → Move) → Sort u_1) (n : Nat) (f : Fml) (r : Nat → Move) (h_1 : (s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) (h_2 : (s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) (h_3 : (f : Fml) → (r : Nat → Move) → motive f.neg r) (h_4 : (f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) (h_5 : (f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) (h_6 : (n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r), Eq (Fml.holds.match_1 motive (Fml.allF n f) r h_1 h_2 h_3 h_4 h_5 h_6) (h_6 n f r)
```

### `_private.Subject.0.Fml.holds.match_1.splitter`  (def, aux)

```
(motive : Fml → (Nat → Move) → Sort u_1) → (x : Fml) → (x_1 : Nat → Move) → ((s t : Tm) → (r : Nat → Move) → motive (Fml.eqT s t) r) → ((s t : Tm) → (r : Nat → Move) → motive (Fml.detT s t) r) → ((f : Fml) → (r : Nat → Move) → motive f.neg r) → ((f g : Fml) → (r : Nat → Move) → motive (f.andF g) r) → ((f g : Fml) → (r : Nat → Move) → motive (f.orF g) r) → ((n : Nat) → (f : Fml) → (r : Nat → Move) → motive (Fml.allF n f) r) → motive x x_1
:=
Fml.holds.match_1
```

### `_private.Subject.0.Move.act.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Move → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Move.I { fst := x, snd := y }) (h_2 : (x y : Int) → motive Move.sv { fst := x, snd := y }) (h_3 : (x y : Int) → motive Move.sh { fst := x, snd := y }) (h_4 : (x y : Int) → motive Move.C2 { fst := x, snd := y }), Eq (Move.act.match_1 motive Move.I { fst := x, snd := y } h_1 h_2 h_3 h_4) (h_1 x y)
```

### `_private.Subject.0.Move.act.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Move → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Move.I { fst := x, snd := y }) (h_2 : (x y : Int) → motive Move.sv { fst := x, snd := y }) (h_3 : (x y : Int) → motive Move.sh { fst := x, snd := y }) (h_4 : (x y : Int) → motive Move.C2 { fst := x, snd := y }), Eq (Move.act.match_1 motive Move.sv { fst := x, snd := y } h_1 h_2 h_3 h_4) (h_2 x y)
```

### `_private.Subject.0.Move.act.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Move → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Move.I { fst := x, snd := y }) (h_2 : (x y : Int) → motive Move.sv { fst := x, snd := y }) (h_3 : (x y : Int) → motive Move.sh { fst := x, snd := y }) (h_4 : (x y : Int) → motive Move.C2 { fst := x, snd := y }), Eq (Move.act.match_1 motive Move.sh { fst := x, snd := y } h_1 h_2 h_3 h_4) (h_3 x y)
```

### `_private.Subject.0.Move.act.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Move → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Move.I { fst := x, snd := y }) (h_2 : (x y : Int) → motive Move.sv { fst := x, snd := y }) (h_3 : (x y : Int) → motive Move.sh { fst := x, snd := y }) (h_4 : (x y : Int) → motive Move.C2 { fst := x, snd := y }), Eq (Move.act.match_1 motive Move.C2 { fst := x, snd := y } h_1 h_2 h_3 h_4) (h_4 x y)
```

### `_private.Subject.0.Move.act.match_1.splitter`  (def, aux)

```
(motive : Move → Pt → Sort u_1) → (x : Move) → (x_1 : Pt) → ((x y : Int) → motive Move.I { fst := x, snd := y }) → ((x y : Int) → motive Move.sv { fst := x, snd := y }) → ((x y : Int) → motive Move.sh { fst := x, snd := y }) → ((x y : Int) → motive Move.C2 { fst := x, snd := y }) → motive x x_1
:=
Move.act.match_1
```

### `_private.Subject.0.Move.mul.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.I Move.I h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_1 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_10`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sh Move.sv h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_10 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_11`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sh Move.sh h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_11 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_12`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sh Move.C2 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_12 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_13`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.C2 Move.I h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_13 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_14`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.C2 Move.sv h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_14 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_15`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.C2 Move.sh h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_15 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_16`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.C2 Move.C2 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_16 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.I Move.sv h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_2 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.I Move.sh h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_3 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.I Move.C2 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_4 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_5`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sv Move.I h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_5 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_6`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sv Move.sv h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_6 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_7`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sv Move.sh h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_7 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_8`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sv Move.C2 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_8 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.eq_9`  (theorem, aux)

```
∀ (motive : Move → Move → Sort u_1) (h_1 : Unit → motive Move.I Move.I) (h_2 : Unit → motive Move.I Move.sv) (h_3 : Unit → motive Move.I Move.sh) (h_4 : Unit → motive Move.I Move.C2) (h_5 : Unit → motive Move.sv Move.I) (h_6 : Unit → motive Move.sv Move.sv) (h_7 : Unit → motive Move.sv Move.sh) (h_8 : Unit → motive Move.sv Move.C2) (h_9 : Unit → motive Move.sh Move.I) (h_10 : Unit → motive Move.sh Move.sv) (h_11 : Unit → motive Move.sh Move.sh) (h_12 : Unit → motive Move.sh Move.C2) (h_13 : Unit → motive Move.C2 Move.I) (h_14 : Unit → motive Move.C2 Move.sv) (h_15 : Unit → motive Move.C2 Move.sh) (h_16 : Unit → motive Move.C2 Move.C2), Eq (Move.mul.match_1 motive Move.sh Move.I h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 h_9 h_10 h_11 h_12 h_13 h_14 h_15 h_16) (h_9 Unit.unit)
```

### `_private.Subject.0.Move.mul.match_1.splitter`  (def, aux)

```
(motive : Move → Move → Sort u_1) → (x x_1 : Move) → (Unit → motive Move.I Move.I) → (Unit → motive Move.I Move.sv) → (Unit → motive Move.I Move.sh) → (Unit → motive Move.I Move.C2) → (Unit → motive Move.sv Move.I) → (Unit → motive Move.sv Move.sv) → (Unit → motive Move.sv Move.sh) → (Unit → motive Move.sv Move.C2) → (Unit → motive Move.sh Move.I) → (Unit → motive Move.sh Move.sv) → (Unit → motive Move.sh Move.sh) → (Unit → motive Move.sh Move.C2) → (Unit → motive Move.C2 Move.I) → (Unit → motive Move.C2 Move.sv) → (Unit → motive Move.C2 Move.sh) → (Unit → motive Move.C2 Move.C2) → motive x x_1
:=
Move.mul.match_1
```

### `_private.Subject.0.Sq.act.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.id { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_1 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.rot90 { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_2 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.rot180 { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_3 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.rot270 { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_4 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_5`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.mirV { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_5 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_6`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.mirH { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_6 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_7`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.mirD { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_7 x y)
```

### `_private.Subject.0.Sq.act.match_1.eq_8`  (theorem, aux)

```
∀ (motive : Sq → Pt → Sort u_1) (x y : Int) (h_1 : (x y : Int) → motive Sq.id { fst := x, snd := y }) (h_2 : (x y : Int) → motive Sq.rot90 { fst := x, snd := y }) (h_3 : (x y : Int) → motive Sq.rot180 { fst := x, snd := y }) (h_4 : (x y : Int) → motive Sq.rot270 { fst := x, snd := y }) (h_5 : (x y : Int) → motive Sq.mirV { fst := x, snd := y }) (h_6 : (x y : Int) → motive Sq.mirH { fst := x, snd := y }) (h_7 : (x y : Int) → motive Sq.mirD { fst := x, snd := y }) (h_8 : (x y : Int) → motive Sq.mirA { fst := x, snd := y }), Eq (Sq.act.match_1 motive Sq.mirA { fst := x, snd := y } h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_8 x y)
```

### `_private.Subject.0.Sq.act.match_1.splitter`  (def, aux)

```
(motive : Sq → Pt → Sort u_1) → (x : Sq) → (x_1 : Pt) → ((x y : Int) → motive Sq.id { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot90 { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot180 { fst := x, snd := y }) → ((x y : Int) → motive Sq.rot270 { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirV { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirH { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirD { fst := x, snd := y }) → ((x y : Int) → motive Sq.mirA { fst := x, snd := y }) → motive x x_1
:=
Sq.act.match_1
```

### `_private.Subject.0.Sq.comp.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_10`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_11`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_12`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_13`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_14`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_15`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_16`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_17`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_18`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_19`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_20`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_21`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_22`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_23`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_24`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_25`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_26`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_27`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_28`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_29`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_30`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_31`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_32`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_33`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_34`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_35`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_36`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_37`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_38`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_39`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_40`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_41`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_42`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_43`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_44`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_45`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_46`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_47`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_48`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_49`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_5`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_50`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_51`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_52`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_53`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_54`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_55`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_56`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_57`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_58`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_59`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_6`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_60`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_61`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_62`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_63`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_64`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_7`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_8`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.eq_9`  (theorem, aux)

```
∀ (motive : Sq → Sq → Sort u_1) (h_1 : Unit → motive Sq.id Sq.id) (h_2 : Unit → motive Sq.id Sq.rot90) (h_3 : Unit → motive Sq.id Sq.rot180) (h_4 : Unit → motive Sq.id Sq.rot270) (h_5 : Unit → motive Sq.id Sq.mirV) (h_6 : Unit → motive Sq.id Sq.mirH) (h_7 : Unit → motive Sq.id Sq.mirD) (h_8 : Unit → motive Sq.id Sq.mirA) (h_9 : Unit → motive Sq.rot90 Sq.id) (h_10 : Unit → motive Sq.rot90 Sq.rot90) (h_11 : Unit → motive Sq.rot90 Sq.rot180) (h_12 : Unit → motive Sq.rot90 Sq.rot270) (h_13 : Unit → motive Sq.rot90 Sq.mirV) (h_14 : Unit → motive Sq.rot90 Sq.mirH) (h_15 : Unit → motive Sq.rot90 Sq.mirD) (h_16 : Unit → motive Sq.rot90 Sq.mirA) (h_17 : Unit → motive Sq.rot180 Sq.id) (h_18 : Unit → motive Sq.rot180 Sq.rot90) (h_19 : Unit → motive Sq.rot180 Sq.rot180) (h_20 : Unit → motive Sq.rot180 Sq.rot270) (h_21 : Unit → motive Sq.rot180 Sq.mirV) (h_22 : Unit → motive Sq.rot180 Sq.mirH) (h_23 : Unit → motive Sq.rot180 Sq.mirD) (h_24 : Unit → motive Sq.rot180 Sq.mirA) (h_25 : Unit → motive Sq.rot270 Sq.id) (h_26 : Unit → motive Sq.rot270 Sq.rot90) (h_27 : Unit → motive Sq.rot270 Sq.rot180) (h_28 : Unit → motive Sq.rot270 Sq.rot270) (h_29 : Unit → motive Sq.rot270 Sq.mirV) (h_30 : Unit → motive Sq.rot270 Sq.mirH) (h_31 : Unit → motive Sq.rot270 Sq.mirD) (h_32 : Unit → motive Sq.rot270 Sq.mirA) (h_33 : Unit → motive Sq.mirV Sq.id) (h_34 : Unit → motive Sq.mirV Sq.rot90) (h_35 : Unit → motive Sq.mirV Sq.rot180) (h_36 : Unit → motive Sq.mirV Sq.rot270) (h_37 : Unit → motive Sq.mirV Sq.mirV) (h_38 : Unit → motive Sq.mirV Sq.mirH) (h_39 : Unit → motive Sq.mirV Sq.mirD) (h_40 : Unit → motive Sq.mirV Sq.mirA) (h_41 : Unit → motive Sq.mirH Sq.id) (h_42 : Unit → motive Sq.mirH Sq.rot90) (h_43 : Unit → motive Sq.mirH Sq.rot180) (h_44 : Unit → motive Sq.mirH Sq.rot270) (h_45 : Unit → motive Sq.mirH Sq.mirV) (h_46 : Unit → motive Sq.mirH Sq.mirH) (h_47 : Unit → motive Sq.mirH Sq.mirD) (h_48 : Unit → motive Sq.mirH Sq.mirA) (h_49 : Unit → motive Sq.mirD Sq.id) (h_50 : Unit → motive Sq.mirD Sq.rot90), ⋯
```

### `_private.Subject.0.Sq.comp.match_1.splitter`  (def, aux)

```
(motive : Sq → Sq → Sort u_1) → (x x_1 : Sq) → (Unit → motive Sq.id Sq.id) → (Unit → motive Sq.id Sq.rot90) → (Unit → motive Sq.id Sq.rot180) → (Unit → motive Sq.id Sq.rot270) → (Unit → motive Sq.id Sq.mirV) → (Unit → motive Sq.id Sq.mirH) → (Unit → motive Sq.id Sq.mirD) → (Unit → motive Sq.id Sq.mirA) → (Unit → motive Sq.rot90 Sq.id) → (Unit → motive Sq.rot90 Sq.rot90) → (Unit → motive Sq.rot90 Sq.rot180) → (Unit → motive Sq.rot90 Sq.rot270) → (Unit → motive Sq.rot90 Sq.mirV) → (Unit → motive Sq.rot90 Sq.mirH) → (Unit → motive Sq.rot90 Sq.mirD) → (Unit → motive Sq.rot90 Sq.mirA) → (Unit → motive Sq.rot180 Sq.id) → (Unit → motive Sq.rot180 Sq.rot90) → (Unit → motive Sq.rot180 Sq.rot180) → (Unit → motive Sq.rot180 Sq.rot270) → (Unit → motive Sq.rot180 Sq.mirV) → (Unit → motive Sq.rot180 Sq.mirH) → (Unit → motive Sq.rot180 Sq.mirD) → (Unit → motive Sq.rot180 Sq.mirA) → (Unit → motive Sq.rot270 Sq.id) → (Unit → motive Sq.rot270 Sq.rot90) → (Unit → motive Sq.rot270 Sq.rot180) → (Unit → motive Sq.rot270 Sq.rot270) → (Unit → motive Sq.rot270 Sq.mirV) → (Unit → motive Sq.rot270 Sq.mirH) → (Unit → motive Sq.rot270 Sq.mirD) → (Unit → motive Sq.rot270 Sq.mirA) → (Unit → motive Sq.mirV Sq.id) → (Unit → motive Sq.mirV Sq.rot90) → (Unit → motive Sq.mirV Sq.rot180) → (Unit → motive Sq.mirV Sq.rot270) → (Unit → motive Sq.mirV Sq.mirV) → (Unit → motive Sq.mirV Sq.mirH) → (Unit → motive Sq.mirV Sq.mirD) → (Unit → motive Sq.mirV Sq.mirA) → (Unit → motive Sq.mirH Sq.id) → (Unit → motive Sq.mirH Sq.rot90) → (Unit → motive Sq.mirH Sq.rot180) → (Unit → motive Sq.mirH Sq.rot270) → (Unit → motive Sq.mirH Sq.mirV) → (Unit → motive Sq.mirH Sq.mirH) → (Unit → motive Sq.mirH Sq.mirD) → (Unit → motive Sq.mirH Sq.mirA) → (Unit → motive Sq.mirD Sq.id) → ⋯
:=
Sq.comp.match_1
```

### `_private.Subject.0.Tm.eval.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Tm → (Nat → Move) → Sort u_1) (n : Nat) (r : Nat → Move) (h_1 : (n : Nat) → (r : Nat → Move) → motive (Tm.var n) r) (h_2 : (x : Nat → Move) → motive Tm.one x) (h_3 : (s t : Tm) → (r : Nat → Move) → motive (s.mulT t) r), Eq (Tm.eval.match_1 motive (Tm.var n) r h_1 h_2 h_3) (h_1 n r)
```

### `_private.Subject.0.Tm.eval.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Tm → (Nat → Move) → Sort u_1) (x : Nat → Move) (h_1 : (n : Nat) → (r : Nat → Move) → motive (Tm.var n) r) (h_2 : (x : Nat → Move) → motive Tm.one x) (h_3 : (s t : Tm) → (r : Nat → Move) → motive (s.mulT t) r), Eq (Tm.eval.match_1 motive Tm.one x h_1 h_2 h_3) (h_2 x)
```

### `_private.Subject.0.Tm.eval.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Tm → (Nat → Move) → Sort u_1) (s t : Tm) (r : Nat → Move) (h_1 : (n : Nat) → (r : Nat → Move) → motive (Tm.var n) r) (h_2 : (x : Nat → Move) → motive Tm.one x) (h_3 : (s t : Tm) → (r : Nat → Move) → motive (s.mulT t) r), Eq (Tm.eval.match_1 motive (s.mulT t) r h_1 h_2 h_3) (h_3 s t r)
```

### `_private.Subject.0.Tm.eval.match_1.splitter`  (def, aux)

```
(motive : Tm → (Nat → Move) → Sort u_1) → (x : Tm) → (x_1 : Nat → Move) → ((n : Nat) → (r : Nat → Move) → motive (Tm.var n) r) → ((x : Nat → Move) → motive Tm.one x) → ((s t : Tm) → (r : Nat → Move) → motive (s.mulT t) r) → motive x x_1
:=
Tm.eval.match_1
```

### `_private.Subject.0.instReprMove.repr.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Move → Sort u_1) (h_1 : Unit → motive Move.I) (h_2 : Unit → motive Move.sv) (h_3 : Unit → motive Move.sh) (h_4 : Unit → motive Move.C2), Eq (instReprMove.repr.match_1 motive Move.I h_1 h_2 h_3 h_4) (h_1 Unit.unit)
```

### `_private.Subject.0.instReprMove.repr.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Move → Sort u_1) (h_1 : Unit → motive Move.I) (h_2 : Unit → motive Move.sv) (h_3 : Unit → motive Move.sh) (h_4 : Unit → motive Move.C2), Eq (instReprMove.repr.match_1 motive Move.sv h_1 h_2 h_3 h_4) (h_2 Unit.unit)
```

### `_private.Subject.0.instReprMove.repr.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Move → Sort u_1) (h_1 : Unit → motive Move.I) (h_2 : Unit → motive Move.sv) (h_3 : Unit → motive Move.sh) (h_4 : Unit → motive Move.C2), Eq (instReprMove.repr.match_1 motive Move.sh h_1 h_2 h_3 h_4) (h_3 Unit.unit)
```

### `_private.Subject.0.instReprMove.repr.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Move → Sort u_1) (h_1 : Unit → motive Move.I) (h_2 : Unit → motive Move.sv) (h_3 : Unit → motive Move.sh) (h_4 : Unit → motive Move.C2), Eq (instReprMove.repr.match_1 motive Move.C2 h_1 h_2 h_3 h_4) (h_4 Unit.unit)
```

### `_private.Subject.0.instReprMove.repr.match_1.splitter`  (def, aux)

```
(motive : Move → Sort u_1) → (x : Move) → (Unit → motive Move.I) → (Unit → motive Move.sv) → (Unit → motive Move.sh) → (Unit → motive Move.C2) → motive x
:=
instReprMove.repr.match_1
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_1`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.id h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_1 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_2`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.rot90 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_2 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_3`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.rot180 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_3 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_4`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.rot270 h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_4 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_5`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.mirV h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_5 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_6`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.mirH h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_6 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_7`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.mirD h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_7 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.eq_8`  (theorem, aux)

```
∀ (motive : Sq → Sort u_1) (h_1 : Unit → motive Sq.id) (h_2 : Unit → motive Sq.rot90) (h_3 : Unit → motive Sq.rot180) (h_4 : Unit → motive Sq.rot270) (h_5 : Unit → motive Sq.mirV) (h_6 : Unit → motive Sq.mirH) (h_7 : Unit → motive Sq.mirD) (h_8 : Unit → motive Sq.mirA), Eq (instReprSq.repr.match_1 motive Sq.mirA h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8) (h_8 Unit.unit)
```

### `_private.Subject.0.instReprSq.repr.match_1.splitter`  (def, aux)

```
(motive : Sq → Sort u_1) → (x : Sq) → (Unit → motive Sq.id) → (Unit → motive Sq.rot90) → (Unit → motive Sq.rot180) → (Unit → motive Sq.rot270) → (Unit → motive Sq.mirV) → (Unit → motive Sq.mirH) → (Unit → motive Sq.mirD) → (Unit → motive Sq.mirA) → motive x
:=
instReprSq.repr.match_1
```

### `corner.eq_1`  (theorem, aux)

```
∀ (p : Pt), Eq (corner p) (And (Or (Eq p.fst 1) (Eq p.fst (-1))) (Or (Eq p.snd 1) (Eq p.snd (-1))))
```

### `instDecidableEqMove._proof_1`  (theorem, aux)

```
∀ (x y : Move), Eq x.ctorIdx y.ctorIdx → Eq x y
```

### `instDecidableEqMove._proof_2`  (theorem, aux)

```
∀ (x y : Move), Not (Eq x.ctorIdx y.ctorIdx) → Eq x y → False
```

### `instDecidableEqMoveSet.decEq._proof_1`  (theorem, aux)

```
∀ (a a_1 a_2 a_3 : Bool), Eq { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 }
```

### `instDecidableEqMoveSet.decEq._proof_2`  (theorem, aux)

```
∀ (a a_1 a_2 a_3 b : Bool), Not (Eq a_3 b) → Eq { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := b } → False
```

### `instDecidableEqMoveSet.decEq._proof_3`  (theorem, aux)

```
∀ (a a_1 a_2 a_3 b b_1 : Bool), Not (Eq a_2 b) → Eq { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := a, hasSv := a_1, hasSh := b, hasC2 := b_1 } → False
```

### `instDecidableEqMoveSet.decEq._proof_4`  (theorem, aux)

```
∀ (a a_1 a_2 a_3 b b_1 b_2 : Bool), Not (Eq a_1 b) → Eq { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := a, hasSv := b, hasSh := b_1, hasC2 := b_2 } → False
```

### `instDecidableEqMoveSet.decEq._proof_5`  (theorem, aux)

```
∀ (a a_1 a_2 a_3 b b_1 b_2 b_3 : Bool), Not (Eq a b) → Eq { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := b, hasSv := b_1, hasSh := b_2, hasC2 := b_3 } → False
```

### `instDecidableEqMoveSet.decEq.match_1`  (def, aux)

```
(motive : MoveSet → MoveSet → Sort u_1) → (x x_1 : MoveSet) → ((a a_1 a_2 a_3 b b_1 b_2 b_3 : Bool) → motive { hasI := a, hasSv := a_1, hasSh := a_2, hasC2 := a_3 } { hasI := b, hasSv := b_1, hasSh := b_2, hasC2 := b_3 }) → motive x x_1
:=
fun motive x x_1 h_1 ↦ MoveSet.casesOn x fun hasI hasSv hasSh hasC2 ↦ MoveSet.casesOn x_1 fun hasI_1 hasSv_1 hasSh_1 hasC2_1 ↦ h_1 hasI hasSv hasSh hasC2 hasI_1 hasSv_1 hasSh_1 hasC2_1
```

### `instDecidableEqSq._proof_1`  (theorem, aux)

```
∀ (x y : Sq), Eq x.ctorIdx y.ctorIdx → Eq x y
```

### `instDecidableEqSq._proof_2`  (theorem, aux)

```
∀ (x y : Sq), Not (Eq x.ctorIdx y.ctorIdx) → Eq x y → False
```

### `instReprMove.repr.match_1`  (def, aux)

```
(motive : Move → Sort u_1) → (x : Move) → (Unit → motive Move.I) → (Unit → motive Move.sv) → (Unit → motive Move.sh) → (Unit → motive Move.C2) → motive x
:=
fun motive x h_1 h_2 h_3 h_4 ↦ Move.casesOn x (h_1 Unit.unit) (h_2 Unit.unit) (h_3 Unit.unit) (h_4 Unit.unit)
```

### `instReprSq.repr.match_1`  (def, aux)

```
(motive : Sq → Sort u_1) → (x : Sq) → (Unit → motive Sq.id) → (Unit → motive Sq.rot90) → (Unit → motive Sq.rot180) → (Unit → motive Sq.rot270) → (Unit → motive Sq.mirV) → (Unit → motive Sq.mirH) → (Unit → motive Sq.mirD) → (Unit → motive Sq.mirA) → motive x
:=
fun motive x h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8 ↦ Sq.casesOn x (h_1 Unit.unit) (h_2 Unit.unit) (h_3 Unit.unit) (h_4 Unit.unit) (h_5 Unit.unit) (h_6 Unit.unit) (h_7 Unit.unit) (h_8 Unit.unit)
```

### `matAct.eq_1`  (theorem, aux)

```
∀ (a b c d : Int) (p : Pt), Eq (matAct a b c d p) { fst := instHAdd.hAdd (instHMul.hMul a p.fst) (instHMul.hMul b p.snd), snd := instHAdd.hAdd (instHMul.hMul c p.fst) (instHMul.hMul d p.snd) }
```

