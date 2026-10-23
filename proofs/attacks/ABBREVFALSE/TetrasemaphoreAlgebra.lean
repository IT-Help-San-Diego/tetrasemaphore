/-
  TetrasemaphoreAlgebra.lean
  ==========================

  The algebra behind the four coin designs, machine-checked.

  Nothing in this file is about pixels, paths or printing.  It is about four
  moves of the plane and what follows from them:

      I   the identity          (NORMATIVE)      leave every point alone
      sv  mirror in the y-axis  (NON-NORMATIVE)  (x, y) ↦ (-x,  y)
      sh  mirror in the x-axis  (METACOGNITIVE)  (x, y) ↦ ( x, -y)
      C2  the half-turn         (CRITICAL)       (x, y) ↦ (-x, -y)

  Zero imports: core Lean only.  No `sorry`, no `native_decide`, no `axiom`
  declarations, no `unsafe`, no `set_option`, and no command that changes what
  Lean does or prints.  Every theorem in the file — not only the headline ones —
  is followed by `#print axioms`.  Since version 2.1 the gate no longer takes
  that printing on trust: it compiles this file and reads the axiom footprint
  out of the compiled module, then checks the two agree.

  Coordinates are integers.  The *statements* below use only facts that hold
  for coordinates in any torsion-free abelian group — `-(-x) = x`, and `-x = x`
  exactly when `x = 0` — so they read over ℚ or ℝ unchanged.  The *proofs* do
  not: several close with `omega` or with `decide` on integer arithmetic, both
  of which are specific to ℤ.  A real-plane version would need different
  tactics and Mathlib, and has not been written (see README_LEAN.md).

  Sections 0-11 are the original file.  Sections 12-15 (S0-S3) were added in a
  second pass, after a red-team review recorded in RED_TEAM_LEAN.md: they prove
  that the subset type really is the powerset, that the symmetry set of an
  arbitrary figure is one of the five subgroups, that a concrete asymmetric
  mark has symmetry set exactly `{I, g}`, and that no formula in the language
  of composition-and-determinant separates the two mirrors.

  Section 16 (S4) was added in a third pass.  §6 lists eight symmetries of the
  square and checks they are eight different maps, which is a list rather than
  a classification; S4 proves that every integer 2×2 matrix carrying the four
  corners onto themselves is one of those eight, so "all eight" is a theorem.
-/

/-! ## 0.  Points and moves -/

/-- A point of the integer plane. -/
abbrev Pt := Int × Int

/-- The four moves.  These are the whole alphabet: there is no fifth. -/
inductive Move
  | I
  | sv
  | sh
  | C2
  deriving DecidableEq, Repr

namespace Move

/-- How a move acts on a point. -/
def act : Move → Pt → Pt
  | I,  (x, y) => (x, y)
  | sv, (x, y) => (-x, y)
  | sh, (x, y) => (x, -y)
  | C2, (x, y) => (-x, -y)

@[simp] theorem act_I (p : Pt) : act I p = p := by cases p; rfl
@[simp] theorem act_sv (x y : Int) : act sv (x, y) = (-x, y) := rfl
@[simp] theorem act_sh (x y : Int) : act sh (x, y) = (x, -y) := rfl
@[simp] theorem act_C2 (x y : Int) : act C2 (x, y) = (-x, -y) := rfl

#print axioms Move.act_I
#print axioms Move.act_sv
#print axioms Move.act_sh
#print axioms Move.act_C2

/-- The composition table, written out in full: `mul g h` is "do `h`, then `g`". -/
def mul : Move → Move → Move
  | I,  I  => I
  | I,  sv => sv
  | I,  sh => sh
  | I,  C2 => C2
  | sv, I  => sv
  | sv, sv => I
  | sv, sh => C2
  | sv, C2 => sh
  | sh, I  => sh
  | sh, sv => C2
  | sh, sh => I
  | sh, C2 => sv
  | C2, I  => C2
  | C2, sv => sh
  | C2, sh => sv
  | C2, C2 => I

/-- The table is the composition of the actions, and not merely a table that
    resembles one.  This is the hinge of the whole file: everything proved
    about `mul` afterwards is a statement about moving the plane. -/
theorem act_mul (g h : Move) (p : Pt) : act (mul g h) p = act g (act h p) := by
  cases g <;> cases h <;> cases p <;> simp [mul, act]

#print axioms Move.act_mul

/-! ## 1.  Matrices and the determinant -/

/-- Entry `a` of the 2×2 matrix `[[a, b], [c, d]]` of a move. -/
def a : Move → Int
  | I => 1 | sv => -1 | sh => 1  | C2 => -1

/-- Entry `b`. -/
def b : Move → Int
  | I => 0 | sv => 0  | sh => 0  | C2 => 0

/-- Entry `c`. -/
def c : Move → Int
  | I => 0 | sv => 0  | sh => 0  | C2 => 0

/-- Entry `d`. -/
def d : Move → Int
  | I => 1 | sv => 1  | sh => -1 | C2 => -1

/-- The determinant: `+1` for the two moves that keep the sense of the plane,
    `-1` for the two that reverse it. -/
def det : Move → Int
  | I => 1 | sv => -1 | sh => -1 | C2 => 1

/-- The list of all four moves. -/
def all : List Move := [I, sv, sh, C2]

end Move

/-! ## 2.  T1 — the group equations -/

theorem T1_mul_assoc (g h k : Move) :
    Move.mul (Move.mul g h) k = Move.mul g (Move.mul h k) := by
  cases g <;> cases h <;> cases k <;> rfl

#print axioms T1_mul_assoc

theorem T1_one_mul (g : Move) : Move.mul Move.I g = g := by cases g <;> rfl

#print axioms T1_one_mul

theorem T1_mul_one (g : Move) : Move.mul g Move.I = g := by cases g <;> rfl

#print axioms T1_mul_one

/-- Every move undoes itself.  Doing any of the four twice leaves the plane
    as it was. -/
theorem T1_self_inverse (g : Move) : Move.mul g g = Move.I := by cases g <;> rfl

#print axioms T1_self_inverse

theorem T1_mul_comm (g h : Move) : Move.mul g h = Move.mul h g := by
  cases g <;> cases h <;> rfl

#print axioms T1_mul_comm

/-- There are exactly four moves: the list `[I, sv, sh, C2]` catches every one. -/
theorem T1_mem_all (g : Move) : g ∈ Move.all := by cases g <;> decide

#print axioms T1_mem_all

theorem T1_all_length : Move.all.length = 4 := rfl

#print axioms T1_all_length

/-- …and the four entries are four different moves, so "four" is exact. -/
theorem T1_all_distinct :
    Move.I ≠ Move.sv ∧ Move.I ≠ Move.sh ∧ Move.I ≠ Move.C2 ∧
    Move.sv ≠ Move.sh ∧ Move.sv ≠ Move.C2 ∧ Move.sh ≠ Move.C2 := by decide

#print axioms T1_all_distinct

/-! ## 3.  T2 — the four moves are told apart by their effect

  The point `(1, 1)` already separates all four: it lies on neither axis, so
  each move sends it somewhere different. -/

theorem T2_probe_injective (g h : Move)
    (hp : Move.act g (1, 1) = Move.act h (1, 1)) : g = h := by
  cases g <;> cases h <;> first | rfl | (exact absurd hp (by decide))

#print axioms T2_probe_injective

/-- Faithfulness: different moves do different things somewhere. -/
theorem T2_faithful (g h : Move) (hne : g ≠ h) :
    ∃ p : Pt, Move.act g p ≠ Move.act h p :=
  ⟨(1, 1), fun hp => hne (T2_probe_injective g h hp)⟩

#print axioms T2_faithful

/-! ## 4.  T3 — the determinant is a homomorphism -/

theorem T3_det_mul (g h : Move) :
    Move.det (Move.mul g h) = Move.det g * Move.det h := by
  cases g <;> cases h <;> decide

#print axioms T3_det_mul

/-- The matrix really is the matrix of the action. -/
theorem T3_act_matrix (g : Move) (x y : Int) :
    Move.act g (x, y) = (Move.a g * x + Move.b g * y, Move.c g * x + Move.d g * y) := by
  cases g <;> simp only [Move.act, Move.a, Move.b, Move.c, Move.d, Prod.mk.injEq] <;>
    constructor <;> omega

#print axioms T3_act_matrix

/-- …and `det` is that matrix's determinant, `ad - bc`, not a second convention
    bolted on. -/
theorem T3_det_eq_ad_sub_bc (g : Move) :
    Move.det g = Move.a g * Move.d g - Move.b g * Move.c g := by
  cases g <;> decide

#print axioms T3_det_eq_ad_sub_bc

/-- The kernel of `det` is exactly NORMATIVE and CRITICAL: the two moves that
    keep the sense of the plane are the identity and the half-turn. -/
theorem T3_det_kernel (g : Move) : Move.det g = 1 ↔ (g = Move.I ∨ g = Move.C2) := by
  cases g <;> decide

#print axioms T3_det_kernel

theorem T3_det_mirrors (g : Move) : Move.det g = -1 ↔ (g = Move.sv ∨ g = Move.sh) := by
  cases g <;> decide

#print axioms T3_det_mirrors

/-! ## 5.  T4 — the fixed points: whole plane, two lines, one point

  This is where the four moves stop being interchangeable.  Each one holds a
  different part of the plane still, and that difference is geometric, not
  algebraic (see T6). -/

/-- NORMATIVE holds the whole plane. -/
theorem T4_fix_I (p : Pt) : Move.act Move.I p = p := by cases p; rfl

#print axioms T4_fix_I

/-- NON-NORMATIVE holds exactly the vertical axis. -/
theorem T4_fix_sv (x y : Int) : Move.act Move.sv (x, y) = (x, y) ↔ x = 0 := by
  rw [Move.act_sv, Prod.mk.injEq]
  omega

#print axioms T4_fix_sv

/-- METACOGNITIVE holds exactly the horizontal axis. -/
theorem T4_fix_sh (x y : Int) : Move.act Move.sh (x, y) = (x, y) ↔ y = 0 := by
  rw [Move.act_sh, Prod.mk.injEq]
  omega

#print axioms T4_fix_sh

/-- CRITICAL holds exactly the centre, and nothing else. -/
theorem T4_fix_C2 (x y : Int) :
    Move.act Move.C2 (x, y) = (x, y) ↔ (x = 0 ∧ y = 0) := by
  rw [Move.act_C2, Prod.mk.injEq]
  omega

#print axioms T4_fix_C2

/-- The two mirrors are told apart by which line they hold: `(0,1)` sits still
    under `sv` and moves under `sh`.  T6 shows that no amount of table-and-`det`
    reasoning can do this. -/
theorem T4_mirrors_differ :
    Move.act Move.sv (0, 1) = (0, 1) ∧ Move.act Move.sh (0, 1) ≠ (0, 1) := by decide

#print axioms T4_mirrors_differ

/-! ## 6.  T5 — the twins, and the eight symmetries of the square -/

/-- The quarter turn. -/
def R90 : Pt → Pt := fun p => (-p.2, p.1)

/-- Its inverse, the quarter turn the other way. -/
def R90inv : Pt → Pt := fun p => (p.2, -p.1)

theorem R90_left_inv (p : Pt) : R90inv (R90 p) = p := by
  cases p; simp [R90, R90inv]

theorem R90_right_inv (p : Pt) : R90 (R90inv p) = p := by
  cases p; simp [R90, R90inv]

#print axioms R90_left_inv
#print axioms R90_right_inv

/-- A quarter turn carries METACOGNITIVE onto NON-NORMATIVE: conjugating the
    horizontal mirror by `R90` gives the vertical one.  The two mirrors are
    twins — a rotation of the page exchanges them. -/
theorem T5_R90_conj_sh (p : Pt) :
    R90 (Move.act Move.sh (R90inv p)) = Move.act Move.sv p := by
  cases p; simp [R90, R90inv, Move.act]

#print axioms T5_R90_conj_sh

/-- The half-turn has no twin: conjugating it by a quarter turn gives it back. -/
theorem T5_R90_conj_C2 (p : Pt) :
    R90 (Move.act Move.C2 (R90inv p)) = Move.act Move.C2 p := by
  cases p; simp [R90, R90inv, Move.act]

#print axioms T5_R90_conj_C2

/-- The eight symmetries of the square: four rotations and four mirrors.  The
    four moves sit inside as `id`, `mirV`, `mirH`, `rot180`. -/
inductive Sq
  | id | rot90 | rot180 | rot270 | mirV | mirH | mirD | mirA
  deriving DecidableEq, Repr

namespace Sq

def act : Sq → Pt → Pt
  | id,     (x, y) => (x, y)
  | rot90,  (x, y) => (-y, x)
  | rot180, (x, y) => (-x, -y)
  | rot270, (x, y) => (y, -x)
  | mirV,   (x, y) => (-x, y)
  | mirH,   (x, y) => (x, -y)
  | mirD,   (x, y) => (y, x)
  | mirA,   (x, y) => (-y, -x)

def inv : Sq → Sq
  | id => id | rot90 => rot270 | rot180 => rot180 | rot270 => rot90
  | mirV => mirV | mirH => mirH | mirD => mirD | mirA => mirA

theorem act_inv (s : Sq) (p : Pt) : act s (act (inv s) p) = p := by
  cases s <;> cases p <;> simp [act, inv]

#print axioms Sq.act_inv

/-- The four moves, seen inside the symmetries of the square. -/
def ofMove : Move → Sq
  | Move.I => id | Move.sv => mirV | Move.sh => mirH | Move.C2 => rot180

theorem ofMove_act (g : Move) (p : Pt) : act (ofMove g) p = Move.act g p := by
  cases g <;> cases p <;> rfl

#print axioms Sq.ofMove_act

end Sq

/-- `rot90` and `rot270` are exactly the quarter turns of T5. -/
theorem T5_rot90_eq_R90 (p : Pt) : Sq.act Sq.rot90 p = R90 p := by
  cases p; rfl

theorem T5_rot270_eq_R90inv (p : Pt) : Sq.act Sq.rot270 p = R90inv p := by
  cases p; rfl

#print axioms T5_rot90_eq_R90
#print axioms T5_rot270_eq_R90inv

/-- The eight really are eight: `(1, 2)` goes to eight different places. -/
theorem T5_eight_distinct (s t : Sq) (hp : Sq.act s (1, 2) = Sq.act t (1, 2)) : s = t := by
  cases s <;> cases t <;> first | rfl | (exact absurd hp (by decide))

#print axioms T5_eight_distinct

/-- CRITICAL commutes with every symmetry of the square. -/
theorem T5_C2_commutes (s : Sq) (p : Pt) :
    Sq.act s (Move.act Move.C2 p) = Move.act Move.C2 (Sq.act s p) := by
  cases s <;> cases p <;> rfl

#print axioms T5_C2_commutes

/-- Consequently conjugating the half-turn by any symmetry of the square gives
    the half-turn back. -/
theorem T5_C2_conj_fixed (s : Sq) (p : Pt) :
    Sq.act s (Move.act Move.C2 (Sq.act (Sq.inv s) p)) = Move.act Move.C2 p := by
  rw [T5_C2_commutes, Sq.act_inv]

#print axioms T5_C2_conj_fixed

/-- So no symmetry of the square turns the half-turn into a mirror — not into
    NON-NORMATIVE… -/
theorem T5_C2_never_sv (s : Sq) :
    ¬ (∀ p : Pt, Sq.act s (Move.act Move.C2 (Sq.act (Sq.inv s) p)) = Move.act Move.sv p) := by
  intro hall
  have h1 := hall (1, 1)
  rw [T5_C2_conj_fixed] at h1
  exact absurd h1 (by decide)

#print axioms T5_C2_never_sv

/-- …and not into METACOGNITIVE either.  The mirrors are twins; the half-turn
    is alone. -/
theorem T5_C2_never_sh (s : Sq) :
    ¬ (∀ p : Pt, Sq.act s (Move.act Move.C2 (Sq.act (Sq.inv s) p)) = Move.act Move.sh p) := by
  intro hall
  have h1 := hall (1, 1)
  rw [T5_C2_conj_fixed] at h1
  exact absurd h1 (by decide)

#print axioms T5_C2_never_sh

/-! ## 7.  T6 — what the algebra cannot see

  A relabelling that preserves the composition table is an automorphism: from
  inside the algebra it is invisible.  `swapVH` exchanges the two mirrors and
  keeps both the table and `det`; so no statement in the language of
  multiplication-and-determinant can distinguish `sv` from `sh`.  `swapVC`
  exchanges `sv` with `C2`, keeps the table, and breaks `det`; so `det` is
  exactly what separates the half-turn from the mirrors. -/

/-- Relabelling: exchange the two mirrors. -/
def swapVH : Move → Move
  | Move.I => Move.I | Move.sv => Move.sh | Move.sh => Move.sv | Move.C2 => Move.C2

/-- Relabelling: exchange NON-NORMATIVE with CRITICAL. -/
def swapVC : Move → Move
  | Move.I => Move.I | Move.sv => Move.C2 | Move.sh => Move.sh | Move.C2 => Move.sv

theorem T6_swapVH_hom (g h : Move) :
    swapVH (Move.mul g h) = Move.mul (swapVH g) (swapVH h) := by
  cases g <;> cases h <;> rfl

#print axioms T6_swapVH_hom

theorem T6_swapVH_involution (g : Move) : swapVH (swapVH g) = g := by cases g <;> rfl

#print axioms T6_swapVH_involution

theorem T6_swapVH_det (g : Move) : Move.det (swapVH g) = Move.det g := by
  cases g <;> decide

#print axioms T6_swapVH_det

theorem T6_swapVC_hom (g h : Move) :
    swapVC (Move.mul g h) = Move.mul (swapVC g) (swapVC h) := by
  cases g <;> cases h <;> rfl

#print axioms T6_swapVC_hom

/-- …but `swapVC` does not keep `det`: the half-turn and a mirror have
    different determinants, which is why `det` tells them apart. -/
theorem T6_swapVC_breaks_det : ¬ (∀ g : Move, Move.det (swapVC g) = Move.det g) := by
  intro hall
  exact absurd (hall Move.sv) (by decide)

#print axioms T6_swapVC_breaks_det

/-- The bare table alone treats the three non-identity moves alike: there is a
    relabelling of the four moves that preserves the composition table and
    carries `sv` to `sh`, and another that preserves it and carries `sv` to
    `C2`.  (Earlier versions of this file stated only `swapVH sv = sh ∧
    swapVC sv = C2`, which is an unfolding of the two definitions and does not
    by itself say the relabellings are table-preserving bijections.  The
    hypotheses are now part of the statement; see RED_TEAM_LEAN.md.) -/
theorem T6_three_interchangeable :
    (∃ f : Move → Move, (∀ g, f (f g) = g) ∧
        (∀ g h, f (Move.mul g h) = Move.mul (f g) (f h)) ∧ f Move.sv = Move.sh) ∧
    (∃ f : Move → Move, (∀ g, f (f g) = g) ∧
        (∀ g h, f (Move.mul g h) = Move.mul (f g) (f h)) ∧ f Move.sv = Move.C2) :=
  ⟨⟨swapVH, T6_swapVH_involution, T6_swapVH_hom, rfl⟩,
   ⟨swapVC, fun g => by cases g <;> rfl, T6_swapVC_hom, rfl⟩⟩

#print axioms T6_three_interchangeable

/-! ## 8.  T7 — a figure's symmetries are closed under composition -/

/-- `Invariant g S` says: the figure `S` looks the same after the move `g`. -/
def Invariant (g : Move) (S : Pt → Prop) : Prop := ∀ p, S (Move.act g p) ↔ S p

/-- Every figure survives doing nothing. -/
theorem T7_invariant_I (S : Pt → Prop) : Invariant Move.I S := by
  intro p
  rw [Move.act_I]

#print axioms T7_invariant_I

/-- Surviving two moves means surviving their composition. -/
theorem T7_invariant_mul {g k : Move} {S : Pt → Prop} (hg : Invariant g S) (hk : Invariant k S) :
    Invariant (Move.mul g k) S := by
  intro p
  rw [Move.act_mul]
  exact (hg (Move.act k p)).trans (hk p)

#print axioms T7_invariant_mul

/-- A figure that survives both mirrors survives the half-turn. -/
theorem T7_both_mirrors {S : Pt → Prop} (hv : Invariant Move.sv S) (hh : Invariant Move.sh S) :
    Invariant Move.C2 S := T7_invariant_mul hv hh

#print axioms T7_both_mirrors

/-- …and the other two pairings, in the same way: any two of the three
    non-identity moves hand you the third. -/
theorem T7_mirror_and_turn {S : Pt → Prop} (hv : Invariant Move.sv S) (hc : Invariant Move.C2 S) :
    Invariant Move.sh S := T7_invariant_mul hv hc

theorem T7_turn_and_mirror {S : Pt → Prop} (hh : Invariant Move.sh S) (hc : Invariant Move.C2 S) :
    Invariant Move.sv S := T7_invariant_mul hh hc

#print axioms T7_mirror_and_turn
#print axioms T7_turn_and_mirror

/-! ## 9.  T8 — exactly five subgroups among the sixteen subsets

  Four moves give sixteen subsets.  Five of them are subgroups.  Because a
  figure's symmetries are closed (T7), the set of moves any figure survives is
  one of those five — there is no sixth possibility to design for.

  That last sentence is a conclusion drawn from T7 and T8 together; it is not
  proved by either on its own.  It is proved as `S1_one_of_five` in §13. -/

/-- With only four moves, "for every move" is a decidable question: check all
    four.  This instance is what lets `decide` settle statements below that
    genuinely quantify over moves, rather than over a list that happens to
    contain them. -/
instance Move.decidableForall (p : Move → Prop) [DecidablePred p] :
    Decidable (∀ g, p g) :=
  if hI : p Move.I then
    if hv : p Move.sv then
      if hh : p Move.sh then
        if hc : p Move.C2 then
          isTrue fun g => by cases g <;> assumption
        else isFalse fun hall => hc (hall _)
      else isFalse fun hall => hh (hall _)
    else isFalse fun hall => hv (hall _)
  else isFalse fun hall => hI (hall _)


/-- A subset of the four moves, as four flags. -/
structure MoveSet where
  hasI  : Bool
  hasSv : Bool
  hasSh : Bool
  hasC2 : Bool
  deriving DecidableEq, Repr

def MoveSet.mem (s : MoveSet) : Move → Bool
  | Move.I => s.hasI | Move.sv => s.hasSv | Move.sh => s.hasSh | Move.C2 => s.hasC2

/-- Closed under composition: if two members are in, so is their product. -/
def MoveSet.closed (s : MoveSet) : Bool :=
  Move.all.all fun g => Move.all.all fun h =>
    !(s.mem g && s.mem h) || s.mem (Move.mul g h)

/-- A subgroup here needs only two things: it contains the identity and it is
    closed.  (Inverses come free — every move undoes itself, T1.) -/
def isSubgroup (s : MoveSet) : Bool := s.hasI && s.closed

def subI   : MoveSet := ⟨true, false, false, false⟩
def subSv  : MoveSet := ⟨true, true,  false, false⟩
def subSh  : MoveSet := ⟨true, false, true,  false⟩
def subC2  : MoveSet := ⟨true, false, false, true⟩
def subAll : MoveSet := ⟨true, true,  true,  true⟩

/-- All sixteen subsets. -/
def allSubs : List MoveSet :=
  [⟨false, false, false, false⟩, ⟨false, false, false, true⟩,
   ⟨false, false, true,  false⟩, ⟨false, false, true,  true⟩,
   ⟨false, true,  false, false⟩, ⟨false, true,  false, true⟩,
   ⟨false, true,  true,  false⟩, ⟨false, true,  true,  true⟩,
   ⟨true,  false, false, false⟩, ⟨true,  false, false, true⟩,
   ⟨true,  false, true,  false⟩, ⟨true,  false, true,  true⟩,
   ⟨true,  true,  false, false⟩, ⟨true,  true,  false, true⟩,
   ⟨true,  true,  true,  false⟩, ⟨true,  true,  true,  true⟩]

/-- The Bool test `isSubgroup` is the mathematical condition it is named for:
    the identity is in, and the set is closed under composition — quantified
    over every move, not merely over the entries of a list. -/
theorem T8_isSubgroup_iff (s : MoveSet) :
    isSubgroup s = true ↔
      (s.mem Move.I = true ∧
        ∀ g h : Move, s.mem g = true → s.mem h = true → s.mem (Move.mul g h) = true) := by
  cases s with
  | mk p q r t => cases p <;> cases q <;> cases r <;> cases t <;> decide

#print axioms T8_isSubgroup_iff

theorem T8_sixteen : allSubs.length = 16 := by decide

#print axioms T8_sixteen

/-- The enumeration leaves nothing out. -/
theorem T8_enum_complete (s : MoveSet) : s ∈ allSubs := by
  cases s with
  | mk p q r t => cases p <;> cases q <;> cases r <;> cases t <;> decide

#print axioms T8_enum_complete

theorem T8_five_count : (allSubs.filter isSubgroup).length = 5 := by decide

#print axioms T8_five_count

/-- The five, listed. -/
theorem T8_five_list :
    allSubs.filter isSubgroup = [subI, subC2, subSh, subSv, subAll] := by decide

#print axioms T8_five_list

/-- And they are these five: the trivial one, the three two-element ones, and
    the whole group. -/
theorem T8_five_are (s : MoveSet) :
    isSubgroup s = true ↔
      (s = subI ∨ s = subSv ∨ s = subSh ∨ s = subC2 ∨ s = subAll) := by
  cases s with
  | mk p q r t => cases p <;> cases q <;> cases r <;> cases t <;> decide

#print axioms T8_five_are

/-- A set containing both mirrors but not the half-turn is not closed — the
    concrete reason there is no three-element subgroup. -/
theorem T8_no_three_element : isSubgroup ⟨true, true, true, false⟩ = false := by decide

#print axioms T8_no_three_element

/-! ## 10.  T9 — the construction rule for the marks

  Each coin's mark is a letter together with that letter's image under the
  coin's own move.  Whatever the letter is, the result survives that move. -/

theorem T9_build {g : Move} (hg : Move.mul g g = Move.I) (S : Pt → Prop) :
    Invariant g (fun p => S p ∨ S (Move.act g p)) := by
  have key : ∀ p : Pt, Move.act g (Move.act g p) = p := by
    intro p
    rw [← Move.act_mul, hg, Move.act_I]
  intro p
  simp only [key]
  exact Or.comm

#print axioms T9_build

/-- The hypothesis is free: every one of the four moves undoes itself, so the
    rule applies to all four coins. -/
theorem T9_build_any (g : Move) (S : Pt → Prop) :
    Invariant g (fun p => S p ∨ S (Move.act g p)) := T9_build (T1_self_inverse g) S

#print axioms T9_build_any

/-! ## 11.  T10 — the state assignment

  `stab` below is a *definition*: it writes down which moves each state is
  meant to survive.  The T10 theorems therefore check the table against itself
  — that the four sets written down are subgroups, are four different ones, and
  have the shape `{I, g}`.  None of them says that any figure has these
  symmetries.  That is proved for four concrete marks in §14 (`S2_realizes_stab`). -/

/-- Which moves each state is meant to survive. -/
def stab : Move → MoveSet
  | Move.I  => subAll
  | Move.sv => subSv
  | Move.sh => subSh
  | Move.C2 => subC2

/-- Each assigned set is one of the five.  (A check on the table just written
    down, not a discovery about figures.) -/
theorem T10_stab_subgroup (g : Move) : isSubgroup (stab g) = true := by
  cases g <;> decide

#print axioms T10_stab_subgroup

theorem T10_stab_distinct :
    stab Move.I ≠ stab Move.sv ∧ stab Move.I ≠ stab Move.sh ∧
    stab Move.I ≠ stab Move.C2 ∧ stab Move.sv ≠ stab Move.sh ∧
    stab Move.sv ≠ stab Move.C2 ∧ stab Move.sh ≠ stab Move.C2 := by decide

#print axioms T10_stab_distinct

/-- For a state other than NORMATIVE, the assigned set is exactly `{I, g}`. -/
theorem T10_stab_is_pair (g : Move) (hg : g ≠ Move.I) (k : Move) :
    (stab g).mem k = true ↔ (k = Move.I ∨ k = g) := by
  cases g
  · exact absurd rfl hg
  all_goals cases k <;> decide

#print axioms T10_stab_is_pair

/-- NORMATIVE is assigned the whole group. -/
theorem T10_stab_I (k : Move) : (stab Move.I).mem k = true := by cases k <;> decide

#print axioms T10_stab_I

/-- The trivial subgroup `{I}` is the one of the five that no state uses. -/
theorem T10_subI_unused (g : Move) : stab g ≠ subI := by cases g <;> decide

#print axioms T10_subI_unused

/-- Sense of the plane across the four states: kept by NORMATIVE and CRITICAL,
    reversed by the two mirrors. -/
theorem T10_det_table :
    Move.det Move.I = 1 ∧ Move.det Move.C2 = 1 ∧
    Move.det Move.sv = -1 ∧ Move.det Move.sh = -1 := by decide

#print axioms T10_det_table

/-! ## 12.  S0 — the subset type really is the powerset

  `MoveSet` is four flags.  Before counting subgroups it is worth proving that
  four flags are the same thing as a set of moves: two `MoveSet`s with the same
  members are equal, and the sixteen entries of `allSubs` are sixteen different
  sets.  Without these, "five of the sixteen" would be a statement about a
  hand-written list rather than about subsets of the group. -/

/-- Two subsets with the same members are the same subset. -/
theorem S0_MoveSet_ext {s t : MoveSet} (h : ∀ g, s.mem g = t.mem g) : s = t := by
  cases s; cases t
  have h1 := h Move.I; have h2 := h Move.sv
  have h3 := h Move.sh; have h4 := h Move.C2
  simp only [MoveSet.mem] at h1 h2 h3 h4
  subst h1; subst h2; subst h3; subst h4; rfl

/-- …and conversely. -/
theorem S0_MoveSet_ext_iff (s t : MoveSet) : (∀ g, s.mem g = t.mem g) ↔ s = t :=
  ⟨S0_MoveSet_ext, fun h g => by rw [h]⟩

/-- The sixteen entries of `allSubs` are sixteen *different* subsets, so
    `T8_sixteen` counts subsets and not merely list positions. -/
theorem S0_allSubs_nodup : allSubs.Pairwise (· ≠ ·) := by decide

/-- Every subset of the four moves occurs exactly once in the enumeration. -/
theorem S0_allSubs_exactly_once (s : MoveSet) :
    (allSubs.filter (fun t => t == s)).length = 1 := by
  cases s with
  | mk p q r t => cases p <;> cases q <;> cases r <;> cases t <;> decide

/-- Every set of moves contains an inverse for each of its members, because
    each move is its own inverse (`T1_self_inverse`).  The binder `s` is any
    `MoveSet`: the statement does not use a subgroup hypothesis and does not
    need one, so this is `T1_self_inverse` repackaged rather than a fact about
    subgroups.  An earlier docstring read it as the latter. -/
theorem S0_subgroup_has_inverses (s : MoveSet) (g : Move) (hg : s.mem g = true) :
    ∃ h : Move, s.mem h = true ∧ Move.mul g h = Move.I :=
  ⟨g, hg, T1_self_inverse g⟩

/-- Invariance is set equality: the figure moved is the figure.  This is what
    licenses reading `Invariant g S` as "`S` survives `g`". -/
theorem S0_invariant_iff_eq (g : Move) (S : Pt → Prop) :
    Invariant g S ↔ (fun p => S (Move.act g p)) = S := by
  constructor
  · intro h; funext p; exact propext (h p)
  · intro h p; exact Iff.of_eq (congrFun h p)

#print axioms S0_MoveSet_ext
#print axioms S0_MoveSet_ext_iff
#print axioms S0_allSubs_nodup
#print axioms S0_allSubs_exactly_once
#print axioms S0_subgroup_has_inverses
#print axioms S0_invariant_iff_eq

/-! ## 13.  S1 — the symmetries of *any* figure form one of the five

  T7 says a figure's symmetries contain `I` and are closed; T8 lists the five
  subgroups.  Putting the two together was, until now, something a reader did
  in their head.  This section does it in Lean: for an arbitrary `S : Pt → Prop`
  — any figure at all, drawn or not, finite or not, decidable or not — the set
  of moves it survives is literally one of the five.

  Arbitrary predicates are not decidable, so the symmetry set is built with
  classical logic.  That shows up honestly in the `#print axioms` lines below
  as `Classical.choice`. -/

/-- The five subgroups of T8, as a list. -/
def fiveSubgroups : List MoveSet := [subI, subSv, subSh, subC2, subAll]

/-- Membership in that list is exactly the subgroup property. -/
theorem S1_five_iff_subgroup (s : MoveSet) : s ∈ fiveSubgroups ↔ isSubgroup s = true := by
  cases s with
  | mk p q r t => cases p <;> cases q <;> cases r <;> cases t <;> decide

/-- The set of moves a figure survives, as a `MoveSet`.  Classical: whether an
    arbitrary predicate survives a move need not be decidable, so the flags are
    read off with excluded middle rather than computed. -/
noncomputable def flag (P : Prop) : Bool := @decide P (Classical.propDecidable P)

/-- The flag is `true` exactly when the proposition holds. -/
theorem S1_flag_true (P : Prop) : flag P = true ↔ P :=
  Iff.of_eq (@decide_eq_true_eq P (Classical.propDecidable P))

noncomputable def symSet (S : Pt → Prop) : MoveSet :=
  ⟨flag (Invariant Move.I S), flag (Invariant Move.sv S),
   flag (Invariant Move.sh S), flag (Invariant Move.C2 S)⟩

/-- `symSet` has the members it is supposed to have. -/
theorem S1_symSet_mem (S : Pt → Prop) (g : Move) :
    (symSet S).mem g = true ↔ Invariant g S := by
  cases g <;> exact S1_flag_true _

/-- The symmetry set of any figure contains the identity and is closed under
    composition — T7, restated as a property of the set. -/
theorem S1_symSet_closed (S : Pt → Prop) :
    (symSet S).mem Move.I = true ∧
      ∀ g k : Move, (symSet S).mem g = true → (symSet S).mem k = true →
        (symSet S).mem (Move.mul g k) = true := by
  constructor
  · exact (S1_symSet_mem S Move.I).mpr (T7_invariant_I S)
  · intro g k hg hk
    exact (S1_symSet_mem S _).mpr
      (T7_invariant_mul ((S1_symSet_mem S g).mp hg) ((S1_symSet_mem S k).mp hk))

/-- Hence it is a subgroup. -/
theorem S1_symSet_isSubgroup (S : Pt → Prop) : isSubgroup (symSet S) = true :=
  (T8_isSubgroup_iff (symSet S)).mpr (S1_symSet_closed S)

/-- **The headline.**  For every figure whatsoever, the moves it survives are
    exactly the members of one of the five subgroups.  There is no sixth
    possibility to design for, and this is now a theorem rather than a reading
    of two theorems side by side. -/
theorem S1_one_of_five (S : Pt → Prop) :
    ∃ s ∈ fiveSubgroups, ∀ g : Move, s.mem g = true ↔ Invariant g S :=
  ⟨symSet S, (S1_five_iff_subgroup _).mpr (S1_symSet_isSubgroup S), S1_symSet_mem S⟩

/-- The same statement with the impossibility spelled out: no figure survives
    both mirrors without also surviving the half-turn.  This is `T7_both_mirrors`
    restated — it is that theorem applied, not a second result — and it is kept
    because the S1 section is where a reader looks for the shape of the
    five-subgroup answer.  The count of theorems in this file includes
    restatements of this kind; RED_TEAM_LEAN.md says which ones they are. -/
theorem S1_no_three_element_symmetry (S : Pt → Prop)
    (hv : Invariant Move.sv S) (hh : Invariant Move.sh S) : Invariant Move.C2 S :=
  T7_both_mirrors hv hh

#print axioms S1_five_iff_subgroup
#print axioms S1_flag_true
#print axioms S1_symSet_mem
#print axioms S1_symSet_closed
#print axioms S1_symSet_isSubgroup
#print axioms S1_one_of_five
#print axioms S1_no_three_element_symmetry

/-! ## 14.  S2 — realizability: a concrete mark whose symmetry set is exactly `{I, g}`

  T9 gives half the design claim: seed-plus-image survives its own move,
  whatever the seed.  The other half — that it survives *nothing else* — is
  false for a symmetric seed, so it cannot follow from T9 and needs a concrete
  figure.  This section supplies one and proves the full claim for it.

  The figures here are finite lists of integer points: model marks, not
  artwork.  Whether the drawn coin matches its model mark is measured on the
  files, as the README says. -/

/-- A figure given by a finite list of points. -/
def ofList (L : List Pt) : Pt → Prop := fun p => p ∈ L

/-- **The decision lemma.**  For a figure made of finitely many points,
    invariance — a statement about every point of the infinite plane — reduces
    to a finite check on the list.  The reason is that each move undoes itself
    (T1), so a move that carries the list into itself also carries it back. -/
theorem S2_invariant_ofList (g : Move) (L : List Pt) :
    Invariant g (ofList L) ↔ (L.all fun p => decide (Move.act g p ∈ L)) = true := by
  have key : ∀ p : Pt, Move.act g (Move.act g p) = p := by
    intro p
    rw [← Move.act_mul, T1_self_inverse, Move.act_I]
  rw [List.all_eq_true]
  constructor
  · intro h p hp
    simp only [decide_eq_true_eq]
    exact (h p).mpr hp
  · intro h p
    constructor
    · intro hgp
      have h2 := h _ hgp
      simp only [decide_eq_true_eq, key] at h2
      exact h2
    · intro hp
      have h2 := h _ hp
      simp only [decide_eq_true_eq] at h2
      exact h2

/-- The seed: five points in an L, all in the open first quadrant, so the
    figure meets neither axis and has no symmetry of its own. -/
def seed : List Pt := [(1, 1), (2, 1), (3, 1), (1, 2), (1, 3)]

/-- The image of a figure under a move. -/
def imageOf (g : Move) (L : List Pt) : List Pt := L.map (Move.act g)

/-- A coin's model mark: the seed together with its image under that coin's
    own move.  This is the T9 recipe, with a particular seed. -/
def mark (g : Move) : List Pt := seed ++ imageOf g seed

/-- NORMATIVE's model mark: the seed together with all three images. -/
def markAll : List Pt :=
  seed ++ imageOf Move.sv seed ++ imageOf Move.sh seed ++ imageOf Move.C2 seed

/-- The seed misses both axes.  That is less than the general theorem below
    needs: `S2_quadrant_mark_exact` asks for the seed to be drawn entirely
    inside the open first quadrant, which is `S2_seed_in_quadrant`. -/
theorem S2_seed_off_axes : seed.all (fun p => decide (p.1 ≠ 0 ∧ p.2 ≠ 0)) = true := by decide

/-- The seed is asymmetric: it survives nothing but the identity.  This is what
    makes "exactly its own move" a real claim rather than an accident. -/
theorem S2_seed_asymmetric (k : Move) : Invariant k (ofList seed) ↔ k = Move.I := by
  rw [S2_invariant_ofList]; cases k <;> decide

/-- NON-NORMATIVE's mark survives exactly `{I, sv}`. -/
theorem S2_mark_sv_exact (k : Move) :
    Invariant k (ofList (mark Move.sv)) ↔ (k = Move.I ∨ k = Move.sv) := by
  rw [S2_invariant_ofList]; cases k <;> decide

/-- METACOGNITIVE's mark survives exactly `{I, sh}`. -/
theorem S2_mark_sh_exact (k : Move) :
    Invariant k (ofList (mark Move.sh)) ↔ (k = Move.I ∨ k = Move.sh) := by
  rw [S2_invariant_ofList]; cases k <;> decide

/-- CRITICAL's mark survives exactly `{I, C2}`. -/
theorem S2_mark_C2_exact (k : Move) :
    Invariant k (ofList (mark Move.C2)) ↔ (k = Move.I ∨ k = Move.C2) := by
  rw [S2_invariant_ofList]; cases k <;> decide

/-- NORMATIVE's mark survives all four moves. -/
theorem S2_markAll_invariant (k : Move) : Invariant k (ofList markAll) := by
  rw [S2_invariant_ofList]; cases k <;> decide

/-- Each mark contains its seed, so it really is "the letter, plus its image". -/
theorem S2_seed_subset (g : Move) : seed.all (fun p => decide (p ∈ mark g)) = true := by
  cases g <;> decide

/-! ### S2 continued — the seed was not special

  The theorems above are about one L-shaped seed.  A reviewer is right to ask
  whether the seed was chosen to make them come out.  It was not: the same
  conclusion holds for *any* non-empty finite seed drawn entirely inside the
  open first quadrant.  The argument is the
  one a geometer would give.  `seed ∪ sv(seed)` lies entirely in the upper half
  plane, and both `sh` and `C2` send the upper half plane to the lower one, so
  neither can carry the mark to itself; and symmetrically for the others. -/

/-- A figure lying inside a region that the move `k` sends outside it cannot
    survive `k` — provided the figure has a point at all. -/
theorem S2_not_invariant_of_region (k : Move) (L : List Pt) (region : Pt → Prop)
    (hall : ∀ q ∈ L, region q) (p : Pt) (hp : p ∈ L)
    (hflip : ∀ q : Pt, region q → ¬ region (Move.act k q)) :
    ¬ Invariant k (ofList L) := fun h => hflip p (hall p hp) (hall _ ((h p).mpr hp))

/-- What it is to be a point of a mark. -/
theorem S2_mem_mark (g : Move) (L : List Pt) (q : Pt) :
    q ∈ L ++ L.map (Move.act g) ↔ (q ∈ L ∨ ∃ r, r ∈ L ∧ Move.act g r = q) := by
  simp [List.mem_append, List.mem_map]

/-- A mark is exactly the T9 figure: the seed, together with the points the
    move carries into the seed.  (The two descriptions agree because each move
    undoes itself.) -/
theorem S2_mark_eq_build (g : Move) (L : List Pt) (q : Pt) :
    (q ∈ L ++ L.map (Move.act g)) ↔ (q ∈ L ∨ Move.act g q ∈ L) := by
  have key : ∀ r : Pt, Move.act g (Move.act g r) = r := by
    intro r; rw [← Move.act_mul, T1_self_inverse, Move.act_I]
  rw [S2_mem_mark]
  constructor
  · rintro (h | ⟨r, hr, rfl⟩)
    · exact Or.inl h
    · exact Or.inr (by rw [key]; exact hr)
  · rintro (h | h)
    · exact Or.inl h
    · exact Or.inr ⟨Move.act g q, h, key q⟩

/-- Every mark survives its own move, for every seed — T9 in list form. -/
theorem S2_mark_invariant_self (g : Move) (L : List Pt) :
    Invariant g (ofList (L ++ L.map (Move.act g))) := by
  have heq : ofList (L ++ L.map (Move.act g))
      = fun p => (fun q => q ∈ L) p ∨ (fun q => q ∈ L) (Move.act g p) :=
    funext fun r => propext (S2_mark_eq_build g L r)
  rw [heq]
  exact T9_build_any g (fun q => q ∈ L)

/-- **The general construction.**  Any non-empty seed drawn entirely inside
    the open first quadrant gives, for each move `g` other than the identity, a
    mark that survives exactly `I` and `g`.  A seed that meets an axis, or
    straddles one, is outside this theorem: `[(1, 1), (-1, 1)]` misses both
    axes and its `sh`-mark survives all four moves.  The L-shaped `seed` above
    is one instance and nothing rests on the choice. -/
theorem S2_quadrant_mark_exact (L : List Pt) (p0 : Pt) (hp0 : p0 ∈ L)
    (hq : ∀ q ∈ L, 0 < q.1 ∧ 0 < q.2) (g : Move) (hg : g ≠ Move.I) (k : Move) :
    Invariant k (ofList (L ++ L.map (Move.act g))) ↔ (k = Move.I ∨ k = g) := by
  -- the mark of `sv` lies in the upper half plane; of `sh`, in the right half
  -- plane; of `C2`, in the two quadrants where the coordinates agree in sign.
  have hp0' : ∀ g' : Move, p0 ∈ L ++ L.map (Move.act g') := fun g' =>
    (S2_mem_mark g' L p0).mpr (Or.inl hp0)
  have up : ∀ q ∈ L ++ L.map (Move.act Move.sv), 0 < q.2 := by
    intro q hqm
    rcases (S2_mem_mark Move.sv L q).mp hqm with h | ⟨r, hr, rfl⟩
    · exact (hq q h).2
    · obtain ⟨x, y⟩ := r; exact (hq (x, y) hr).2
  have right : ∀ q ∈ L ++ L.map (Move.act Move.sh), 0 < q.1 := by
    intro q hqm
    rcases (S2_mem_mark Move.sh L q).mp hqm with h | ⟨r, hr, rfl⟩
    · exact (hq q h).1
    · obtain ⟨x, y⟩ := r; exact (hq (x, y) hr).1
  have diag : ∀ q ∈ L ++ L.map (Move.act Move.C2),
      (0 < q.1 ∧ 0 < q.2) ∨ (q.1 < 0 ∧ q.2 < 0) := by
    intro q hqm
    rcases (S2_mem_mark Move.C2 L q).mp hqm with h | ⟨r, hr, rfl⟩
    · exact Or.inl (hq q h)
    · obtain ⟨x, y⟩ := r
      have h2 := hq (x, y) hr
      refine Or.inr ?_
      have hx : (0:Int) < x := h2.1
      have hy : (0:Int) < y := h2.2
      exact ⟨by show -x < 0; omega, by show -y < 0; omega⟩
  have flipY : ∀ k' : Move, (k' = Move.sh ∨ k' = Move.C2) →
      ∀ q : Pt, 0 < q.2 → ¬ (0 < (Move.act k' q).2) := by
    rintro k' (rfl | rfl) ⟨x, y⟩ h <;> (have h' : (0:Int) < y := h) <;>
      (show ¬ ((0:Int) < -y)) <;> omega
  have flipX : ∀ k' : Move, (k' = Move.sv ∨ k' = Move.C2) →
      ∀ q : Pt, 0 < q.1 → ¬ (0 < (Move.act k' q).1) := by
    rintro k' (rfl | rfl) ⟨x, y⟩ h <;> (have h' : (0:Int) < x := h) <;>
      (show ¬ ((0:Int) < -x)) <;> omega
  have flipD : ∀ k' : Move, (k' = Move.sv ∨ k' = Move.sh) →
      ∀ q : Pt, ((0 < q.1 ∧ 0 < q.2) ∨ (q.1 < 0 ∧ q.2 < 0)) →
        ¬ (((0 < (Move.act k' q).1 ∧ 0 < (Move.act k' q).2) ∨
            ((Move.act k' q).1 < 0 ∧ (Move.act k' q).2 < 0))) := by
    rintro k' (rfl | rfl) ⟨x, y⟩ h
    · have h' : (0 < x ∧ 0 < y) ∨ (x < 0 ∧ y < 0) := h
      show ¬ ((0 < -x ∧ 0 < y) ∨ (-x < 0 ∧ y < 0))
      omega
    · have h' : (0 < x ∧ 0 < y) ∨ (x < 0 ∧ y < 0) := h
      show ¬ ((0 < x ∧ 0 < -y) ∨ (x < 0 ∧ -y < 0))
      omega
  constructor
  · intro hinv
    cases g with
    | I => exact absurd rfl hg
    | sv =>
      cases k with
      | I  => exact Or.inl rfl
      | sv => exact Or.inr rfl
      | sh => exact absurd hinv (S2_not_invariant_of_region _ _ _ up p0 (hp0' Move.sv)
                 (flipY Move.sh (Or.inl rfl)))
      | C2 => exact absurd hinv (S2_not_invariant_of_region _ _ _ up p0 (hp0' Move.sv)
                 (flipY Move.C2 (Or.inr rfl)))
    | sh =>
      cases k with
      | I  => exact Or.inl rfl
      | sh => exact Or.inr rfl
      | sv => exact absurd hinv (S2_not_invariant_of_region _ _ _ right p0 (hp0' Move.sh)
                 (flipX Move.sv (Or.inl rfl)))
      | C2 => exact absurd hinv (S2_not_invariant_of_region _ _ _ right p0 (hp0' Move.sh)
                 (flipX Move.C2 (Or.inr rfl)))
    | C2 =>
      cases k with
      | I  => exact Or.inl rfl
      | C2 => exact Or.inr rfl
      | sv => exact absurd hinv (S2_not_invariant_of_region _ _ _ diag p0 (hp0' Move.C2)
                 (flipD Move.sv (Or.inl rfl)))
      | sh => exact absurd hinv (S2_not_invariant_of_region _ _ _ diag p0 (hp0' Move.C2)
                 (flipD Move.sh (Or.inr rfl)))
  · rintro (rfl | rfl)
    · exact T7_invariant_I _
    · exact S2_mark_invariant_self _ L

/-- The L-shaped seed satisfies the hypothesis, so the concrete marks above are
    instances of the general construction and not a separate claim. -/
theorem S2_seed_in_quadrant : ∀ q ∈ seed, 0 < q.1 ∧ 0 < q.2 := by decide

/-! ### S2 continued — the concrete marks, a second time

  `S2_mark_sv_exact` and its two siblings were proved by `decide`: a finite
  check on one list.  The three theorems below prove the same three statements
  again, as one-term instances of the general theorem, using nothing about the
  seed except that it is non-empty and lies inside the open first quadrant.
  Two routes to the same conclusion, one by enumeration and one by the
  geometric argument, which is what "proved two independent ways" means here. -/

/-- NON-NORMATIVE's mark, from the general theorem rather than by enumeration. -/
theorem S2_mark_sv_exact_via_general (k : Move) :
    Invariant k (ofList (mark Move.sv)) ↔ (k = Move.I ∨ k = Move.sv) :=
  S2_quadrant_mark_exact seed (1, 1) (by decide) S2_seed_in_quadrant Move.sv (by decide) k

/-- METACOGNITIVE's mark, the same way. -/
theorem S2_mark_sh_exact_via_general (k : Move) :
    Invariant k (ofList (mark Move.sh)) ↔ (k = Move.I ∨ k = Move.sh) :=
  S2_quadrant_mark_exact seed (1, 1) (by decide) S2_seed_in_quadrant Move.sh (by decide) k

/-- CRITICAL's mark, the same way. -/
theorem S2_mark_C2_exact_via_general (k : Move) :
    Invariant k (ofList (mark Move.C2)) ↔ (k = Move.I ∨ k = Move.C2) :=
  S2_quadrant_mark_exact seed (1, 1) (by decide) S2_seed_in_quadrant Move.C2 (by decide) k

#print axioms S2_not_invariant_of_region
#print axioms S2_mem_mark
#print axioms S2_mark_eq_build
#print axioms S2_mark_invariant_self
#print axioms S2_quadrant_mark_exact
#print axioms S2_seed_in_quadrant
#print axioms S2_mark_sv_exact_via_general
#print axioms S2_mark_sh_exact_via_general
#print axioms S2_mark_C2_exact_via_general

/-- The model mark assigned to each state. -/
def markOf : Move → List Pt
  | Move.I  => markAll
  | Move.sv => mark Move.sv
  | Move.sh => mark Move.sh
  | Move.C2 => mark Move.C2

/-- **The design claim, proved for the model marks.**  For each of the four
    states, the moves its mark survives are exactly the moves T10 assigns to
    it.  `stab` stops being a table someone wrote down and becomes a fact about
    four figures. -/
theorem S2_realizes_stab (g k : Move) :
    (stab g).mem k = true ↔ Invariant k (ofList (markOf g)) := by
  cases g with
  | I =>
    constructor
    · intro _; exact S2_markAll_invariant k
    · intro _; exact T10_stab_I k
  | sv => rw [show markOf Move.sv = mark Move.sv from rfl, S2_mark_sv_exact]
          cases k <;> decide
  | sh => rw [show markOf Move.sh = mark Move.sh from rfl, S2_mark_sh_exact]
          cases k <;> decide
  | C2 => rw [show markOf Move.C2 = mark Move.C2 from rfl, S2_mark_C2_exact]
          cases k <;> decide

/-- Consequently each of the four states is realized by a figure whose symmetry
    set is the assigned subgroup — the five-possibilities theorem S1, met. -/
theorem S2_stab_is_symSet (g : Move) : symSet (ofList (markOf g)) = stab g :=
  S0_MoveSet_ext fun k => by
    rw [Bool.eq_iff_iff, S1_symSet_mem, ← S2_realizes_stab]

#print axioms S2_invariant_ofList
#print axioms S2_seed_off_axes
#print axioms S2_seed_asymmetric
#print axioms S2_mark_sv_exact
#print axioms S2_mark_sh_exact
#print axioms S2_mark_C2_exact
#print axioms S2_markAll_invariant
#print axioms S2_seed_subset
#print axioms S2_realizes_stab
#print axioms S2_stab_is_symSet

/-! ## 15.  S3 — "the algebra cannot see the difference", made into a theorem

  T6 exhibits a relabelling that preserves the composition table and the
  determinant and exchanges the two mirrors.  The docstrings then draw a
  conclusion about *every statement* in that language — which is a claim about
  a formal language, and so is not settled by exhibiting one relabelling.

  This section settles it.  It writes down the language — terms built from
  variables, the identity and composition; formulas built from equations
  between terms, equations between their determinants, negation, conjunction,
  disjunction and quantification over moves — and proves by induction that
  satisfaction is unchanged by the relabelling.  The language deliberately has
  no name for any particular move except the identity: a constant symbol for
  `sv` would separate the mirrors by fiat and would be a statement about the
  naming, not about the structure. -/

/-- `swapVC` is a relabelling too: it undoes itself. -/
theorem S3_swapVC_involution (g : Move) : swapVC (swapVC g) = g := by cases g <;> rfl

/-- Terms: variables, the identity, composition. -/
inductive Tm
  | var (n : Nat)
  | one
  | mulT (s t : Tm)

def Tm.eval : Tm → (Nat → Move) → Move
  | var n,    r => r n
  | one,      _ => Move.I
  | mulT s t, r => Move.mul (s.eval r) (t.eval r)

/-- Formulas of the language of composition-and-determinant. -/
inductive Fml
  | eqT  (s t : Tm)
  | detT (s t : Tm)
  | neg  (f : Fml)
  | andF (f g : Fml)
  | orF  (f g : Fml)
  | allF (n : Nat) (f : Fml)

def Fml.holds : Fml → (Nat → Move) → Prop
  | eqT s t,  r => s.eval r = t.eval r
  | detT s t, r => Move.det (s.eval r) = Move.det (t.eval r)
  | neg f,    r => ¬ f.holds r
  | andF f g, r => f.holds r ∧ g.holds r
  | orF f g,  r => f.holds r ∨ g.holds r
  | allF n f, r => ∀ m : Move, f.holds (fun k => if k = n then m else r k)

/-- Every term commutes with the relabelling. -/
theorem S3_tm_swapVH (t : Tm) (r : Nat → Move) :
    t.eval (fun n => swapVH (r n)) = swapVH (t.eval r) := by
  induction t with
  | var n => rfl
  | one => rfl
  | mulT s t ihs iht => simp only [Tm.eval, ihs, iht, T6_swapVH_hom]

/-- …and so does every formula: relabelling the environment changes nothing
    about what holds. -/
theorem S3_fml_swapVH (f : Fml) (r : Nat → Move) :
    f.holds (fun n => swapVH (r n)) ↔ f.holds r := by
  induction f generalizing r with
  | eqT s t =>
      simp only [Fml.holds, S3_tm_swapVH]
      constructor
      · intro h
        have h2 := congrArg swapVH h
        rwa [T6_swapVH_involution, T6_swapVH_involution] at h2
      · intro h; rw [h]
  | detT s t => simp only [Fml.holds, S3_tm_swapVH, T6_swapVH_det]
  | neg f ih => simp only [Fml.holds, ih]
  | andF f g ihf ihg => simp only [Fml.holds, ihf, ihg]
  | orF f g ihf ihg => simp only [Fml.holds, ihf, ihg]
  | allF n f ih =>
      simp only [Fml.holds]
      constructor
      · intro h m
        refine (ih (fun k => if k = n then m else r k)).mp ?_
        have h2 := h (swapVH m)
        rwa [show (fun k => swapVH (if k = n then m else r k))
               = (fun k => if k = n then swapVH m else swapVH (r k)) from
             funext fun k => by by_cases hk : k = n <;> simp [hk]]
      · intro h m
        have h2 := (ih (fun k => if k = n then swapVH m else r k)).mpr (h (swapVH m))
        rwa [show (fun k => swapVH (if k = n then swapVH m else r k))
               = (fun k => if k = n then m else swapVH (r k)) from
             funext fun k => by
               by_cases hk : k = n <;> simp [hk, T6_swapVH_involution]] at h2

/-- **The headline for T6.**  No formula in the language of composition and the
    determinant separates the two mirrors: whatever such a formula says of
    NON-NORMATIVE it says of METACOGNITIVE, and conversely.  The difference
    between the two mirrors is not in the algebra; it is T4's geometry, which
    line each one holds still. -/
theorem S3_no_formula_separates_mirrors (f : Fml) :
    f.holds (fun _ => Move.sv) ↔ f.holds (fun _ => Move.sh) :=
  (S3_fml_swapVH f (fun _ => Move.sv)).symm

/-- The language is not vacuous — it does separate things it should.  "`det x`
    is the determinant of the identity" holds of the half-turn and fails of a
    mirror, which is T3 said inside the language. -/
theorem S3_language_separates_turn_from_mirror :
    ¬ ((Fml.detT (Tm.var 0) Tm.one).holds (fun _ => Move.sv)) ∧
      (Fml.detT (Tm.var 0) Tm.one).holds (fun _ => Move.C2) := by
  constructor
  · show ¬ (Move.det Move.sv = Move.det Move.I)
    decide
  · show Move.det Move.C2 = Move.det Move.I
    decide

/-- …and it tells the identity from the rest. -/
theorem S3_language_separates_I_from_sv :
    ((Fml.eqT (Tm.var 0) Tm.one).holds (fun _ => Move.I)) ∧
      ¬ ((Fml.eqT (Tm.var 0) Tm.one).holds (fun _ => Move.sv)) := by
  constructor
  · show Move.I = Move.I
    rfl
  · show ¬ (Move.sv = Move.I)
    decide

#print axioms S3_swapVC_involution
#print axioms S3_tm_swapVH
#print axioms S3_fml_swapVH
#print axioms S3_no_formula_separates_mirrors
#print axioms S3_language_separates_turn_from_mirror
#print axioms S3_language_separates_I_from_sv

/-! ## 16.  S4 — the eight really are all of them

  §6 writes down eight maps, calls them the symmetries of the square, and checks
  that they are eight different maps.  That is a list with a distinctness check,
  and a list is not an argument: nothing in §6 rules out a ninth symmetry the
  author forgot.  The README said "all eight symmetries of the square", which is
  a stronger claim than anything §6 proved.

  This section proves it.  Each of the eight acts by an integer 2×2 matrix
  (`S4_act_matrix`), that action is linear (`S4_matAct_add`, `S4_matAct_smul`),
  and it carries the four corners `(±1, ±1)` onto themselves (`S4_corner_maps`,
  `S4_corner_onto`).  The eight are closed under composition, with the identity
  and with inverses (`S4_comp_act` and the four laws after it).  And then the
  converse, which is what turns a list into a classification: every integer 2×2
  matrix carrying the corner set onto itself is the action of exactly one of the
  eight (`S4_entries`, `S4_classification`), so there is no ninth to find.

  The argument is the one a geometer gives.  A linear map is determined by where
  it sends `(1,1)` and `(1,-1)`; both images must be corners; and a corner has
  to come back from somewhere, which rules out the collapsing cases.  What is
  left is sixteen candidate matrices, eight of which fail to be onto — and the
  eight that remain are the eight. -/

/-- The action of the integer matrix `[[a, b], [c, d]]` on a point. -/
def matAct (a b c d : Int) (p : Pt) : Pt := (a * p.1 + b * p.2, c * p.1 + d * p.2)

/-- The four corners of the square: both coordinates `±1`. -/
def corner (p : Pt) : Prop := (p.1 = 1 ∨ p.1 = -1) ∧ (p.2 = 1 ∨ p.2 = -1)

namespace Sq

/-- The matrix of each symmetry, as `(a, b, c, d)`. -/
def mat : Sq → Int × Int × Int × Int
  | id => (1, 0, 0, 1)
  | rot90 => (0, -1, 1, 0)
  | rot180 => (-1, 0, 0, -1)
  | rot270 => (0, 1, -1, 0)
  | mirV => (-1, 0, 0, 1)
  | mirH => (1, 0, 0, -1)
  | mirD => (0, 1, 1, 0)
  | mirA => (0, -1, -1, 0)

/-- The composition table, written out in full: `comp s t` is "do `t`, then `s`".
    `S4_comp_act` proves it is composition of the actual maps. -/
def comp : Sq → Sq → Sq
  | id, id => id
  | id, rot90 => rot90
  | id, rot180 => rot180
  | id, rot270 => rot270
  | id, mirV => mirV
  | id, mirH => mirH
  | id, mirD => mirD
  | id, mirA => mirA
  | rot90, id => rot90
  | rot90, rot90 => rot180
  | rot90, rot180 => rot270
  | rot90, rot270 => id
  | rot90, mirV => mirA
  | rot90, mirH => mirD
  | rot90, mirD => mirV
  | rot90, mirA => mirH
  | rot180, id => rot180
  | rot180, rot90 => rot270
  | rot180, rot180 => id
  | rot180, rot270 => rot90
  | rot180, mirV => mirH
  | rot180, mirH => mirV
  | rot180, mirD => mirA
  | rot180, mirA => mirD
  | rot270, id => rot270
  | rot270, rot90 => id
  | rot270, rot180 => rot90
  | rot270, rot270 => rot180
  | rot270, mirV => mirD
  | rot270, mirH => mirA
  | rot270, mirD => mirH
  | rot270, mirA => mirV
  | mirV, id => mirV
  | mirV, rot90 => mirD
  | mirV, rot180 => mirH
  | mirV, rot270 => mirA
  | mirV, mirV => id
  | mirV, mirH => rot180
  | mirV, mirD => rot90
  | mirV, mirA => rot270
  | mirH, id => mirH
  | mirH, rot90 => mirA
  | mirH, rot180 => mirV
  | mirH, rot270 => mirD
  | mirH, mirV => rot180
  | mirH, mirH => id
  | mirH, mirD => rot270
  | mirH, mirA => rot90
  | mirD, id => mirD
  | mirD, rot90 => mirH
  | mirD, rot180 => mirA
  | mirD, rot270 => mirV
  | mirD, mirV => rot270
  | mirD, mirH => rot90
  | mirD, mirD => id
  | mirD, mirA => rot180
  | mirA, id => mirA
  | mirA, rot90 => mirV
  | mirA, rot180 => mirD
  | mirA, rot270 => mirH
  | mirA, mirV => rot90
  | mirA, mirH => rot270
  | mirA, mirD => rot180
  | mirA, mirA => id

end Sq

/-- Each symmetry of the square acts by its matrix: the eight maps of §6 are
    linear maps of the integer plane, not eight unrelated rules. -/
theorem S4_act_matrix (s : Sq) (p : Pt) :
    Sq.act s p = matAct (Sq.mat s).1 (Sq.mat s).2.1 (Sq.mat s).2.2.1 (Sq.mat s).2.2.2 p := by
  cases s <;> obtain ⟨x, y⟩ := p <;>
    simp only [Sq.act, Sq.mat, matAct, Prod.mk.injEq] <;> constructor <;> omega

/-- A matrix action is additive. -/
theorem S4_matAct_add (a b c d : Int) (p q : Pt) :
    matAct a b c d (p.1 + q.1, p.2 + q.2)
      = ((matAct a b c d p).1 + (matAct a b c d q).1,
         (matAct a b c d p).2 + (matAct a b c d q).2) := by
  simp only [matAct, Int.mul_add, Prod.mk.injEq]
  constructor <;> omega

/-- …and homogeneous, so "linear" is the whole of it. -/
theorem S4_matAct_smul (a b c d n : Int) (p : Pt) :
    matAct a b c d (n * p.1, n * p.2)
      = (n * (matAct a b c d p).1, n * (matAct a b c d p).2) := by
  simp only [matAct, Int.mul_add, Prod.mk.injEq]
  constructor <;> simp [Int.mul_left_comm]

/-- Each symmetry carries corners to corners. -/
theorem S4_corner_maps (s : Sq) (p : Pt) (hp : corner p) : corner (Sq.act s p) := by
  obtain ⟨x, y⟩ := p
  cases s <;> (simp only [Sq.act, corner] at hp ⊢) <;> omega

/-- …and every corner is the image of one, so the corner set is carried *onto*
    itself and not merely into it. -/
theorem S4_corner_onto (s : Sq) (q : Pt) (hq : corner q) :
    ∃ p : Pt, corner p ∧ Sq.act s p = q :=
  ⟨Sq.act (Sq.inv s) q, S4_corner_maps _ q hq, Sq.act_inv s q⟩

/-- The composition table is composition of the actions, and not merely a table
    that resembles one.  This is `Move.act_mul`'s role, for the eight. -/
theorem S4_comp_act (s t : Sq) (p : Pt) : Sq.act (Sq.comp s t) p = Sq.act s (Sq.act t p) := by
  cases s <;> cases t <;> obtain ⟨x, y⟩ := p <;>
    simp [Sq.comp, Sq.act]

theorem S4_comp_assoc (s t u : Sq) :
    Sq.comp (Sq.comp s t) u = Sq.comp s (Sq.comp t u) := by
  cases s <;> cases t <;> cases u <;> rfl

theorem S4_id_comp (s : Sq) : Sq.comp Sq.id s = s := by cases s <;> rfl

theorem S4_comp_id (s : Sq) : Sq.comp s Sq.id = s := by cases s <;> rfl

theorem S4_comp_inv (s : Sq) : Sq.comp s (Sq.inv s) = Sq.id := by cases s <;> rfl

theorem S4_inv_comp (s : Sq) : Sq.comp (Sq.inv s) s = Sq.id := by cases s <;> rfl

/-- Two symmetries that move every point alike are the same symmetry — §6's
    `T5_eight_distinct`, in the form the classification needs. -/
theorem S4_act_injective (s t : Sq) (h : ∀ p : Pt, Sq.act s p = Sq.act t p) : s = t :=
  T5_eight_distinct s t (h (1, 2))

/-- **The sixteen candidates, cut to eight.**  If an integer matrix carries the
    corner set onto itself then its four entries are one of eight quadruples.
    Both halves of "onto itself" are used: the images of `(1,1)` and `(1,-1)`
    must be corners, which leaves sixteen matrices, and every corner must have a
    preimage, which kills the eight singular ones. -/
theorem S4_entries (a b c d : Int)
    (hmaps : ∀ p : Pt, corner p → corner (matAct a b c d p))
    (honto : ∀ q : Pt, corner q → ∃ p : Pt, corner p ∧ matAct a b c d p = q) :
    (a = 1 ∧ b = 0 ∧ c = 0 ∧ d = 1) ∨ (a = 0 ∧ b = -1 ∧ c = 1 ∧ d = 0) ∨
    (a = -1 ∧ b = 0 ∧ c = 0 ∧ d = -1) ∨ (a = 0 ∧ b = 1 ∧ c = -1 ∧ d = 0) ∨
    (a = -1 ∧ b = 0 ∧ c = 0 ∧ d = 1) ∨ (a = 1 ∧ b = 0 ∧ c = 0 ∧ d = -1) ∨
    (a = 0 ∧ b = 1 ∧ c = 1 ∧ d = 0) ∨ (a = 0 ∧ b = -1 ∧ c = -1 ∧ d = 0) := by
  have c11 : corner ((1 : Int), (1 : Int)) := ⟨Or.inl rfl, Or.inl rfl⟩
  have c1m : corner ((1 : Int), (-1 : Int)) := ⟨Or.inl rfl, Or.inr rfl⟩
  have h1 := hmaps _ c11
  have h2 := hmaps _ c1m
  obtain ⟨u, hu, hu'⟩ := honto _ c11
  obtain ⟨v, hv, hv'⟩ := honto _ c1m
  obtain ⟨u1, u2⟩ := u
  obtain ⟨v1, v2⟩ := v
  simp only [matAct, corner, Prod.mk.injEq] at h1 h2 hu hv hu' hv'
  rcases hu.1 with hx | hx <;> rcases hu.2 with hy | hy <;>
    rcases hv.1 with kx | kx <;> rcases hv.2 with ky | ky <;>
      subst hx <;> subst hy <;> subst kx <;> subst ky <;> omega

/-- Having found one symmetry that acts as the matrix, it is the only one. -/
theorem S4_unique_of_act (a b c d : Int) (s : Sq)
    (hs : ∀ p : Pt, matAct a b c d p = Sq.act s p) :
    ∃ t : Sq, (∀ p : Pt, matAct a b c d p = Sq.act t p) ∧
      ∀ u : Sq, (∀ p : Pt, matAct a b c d p = Sq.act u p) → u = t :=
  ⟨s, hs, fun u hu => S4_act_injective u s (fun p => by rw [← hu p, hs p])⟩

/-- **The classification.**  Every integer 2×2 matrix that carries the four
    corners of the square onto themselves is the action of exactly one of the
    eight symmetries.  There is no ninth. -/
theorem S4_classification (a b c d : Int)
    (hmaps : ∀ p : Pt, corner p → corner (matAct a b c d p))
    (honto : ∀ q : Pt, corner q → ∃ p : Pt, corner p ∧ matAct a b c d p = q) :
    ∃ s : Sq, (∀ p : Pt, matAct a b c d p = Sq.act s p) ∧
      ∀ u : Sq, (∀ p : Pt, matAct a b c d p = Sq.act u p) → u = s := by
  rcases S4_entries a b c d hmaps honto with
      ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩ |
      ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩ |
      ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩
  · exact S4_unique_of_act _ _ _ _ Sq.id
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.rot90
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.rot180
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.rot270
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.mirV
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.mirH
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.mirD
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])
  · exact S4_unique_of_act _ _ _ _ Sq.mirA
      (fun p => by obtain ⟨x, y⟩ := p; simp [matAct, Sq.act])

/-- **The square claim, as a biconditional.**  An integer 2×2 matrix carries the
    corner set onto itself exactly when it is one of the eight.  This is what
    "all eight symmetries of the square" means, and it is now a theorem rather
    than a count of a hand-written list. -/
theorem S4_eight_are_all (a b c d : Int) :
    ((∀ p : Pt, corner p → corner (matAct a b c d p)) ∧
      (∀ q : Pt, corner q → ∃ p : Pt, corner p ∧ matAct a b c d p = q))
    ↔ ∃ s : Sq, ∀ p : Pt, matAct a b c d p = Sq.act s p := by
  constructor
  · rintro ⟨h1, h2⟩
    obtain ⟨s, hs, _⟩ := S4_classification a b c d h1 h2
    exact ⟨s, hs⟩
  · rintro ⟨s, hs⟩
    refine ⟨fun p hp => ?_, fun q hq => ?_⟩
    · rw [hs p]; exact S4_corner_maps s p hp
    · obtain ⟨p, hp, hpq⟩ := S4_corner_onto s q hq
      exact ⟨p, hp, by rw [hs p]; exact hpq⟩

#print axioms S4_act_matrix
#print axioms S4_matAct_add
#print axioms S4_matAct_smul
#print axioms S4_corner_maps
#print axioms S4_corner_onto
#print axioms S4_comp_act
#print axioms S4_comp_assoc
#print axioms S4_id_comp
#print axioms S4_comp_id
#print axioms S4_comp_inv
#print axioms S4_inv_comp
#print axioms S4_act_injective
#print axioms S4_entries
#print axioms S4_unique_of_act
#print axioms S4_classification
#print axioms S4_eight_are_all

abbrev ThreeInst := OfNat Nat 3
instance myThree : ThreeInst := ⟨(allSubs.filter isSubgroup).length⟩

theorem T8_three_count_false : (allSubs.filter isSubgroup).length = 3 := rfl

#print axioms T8_three_count_false
