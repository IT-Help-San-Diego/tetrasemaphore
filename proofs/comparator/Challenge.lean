/-
  Challenge.lean
  ==============

  Seventeen statements, no proofs: the challenge half of a `lake comparator` statement check
  of `../TetrasemaphoreAlgebra.lean` at tag `v1.2.0`.  Lean's judge confirms that the published
  file proves exactly these statements, with Lean's three standard axioms and no others, and that
  its kernel and the independent checkers accept the proofs.  See README.md in this folder for
  how to run it and for what it does not show.

  The statements were written from the English of the public note, the guide
  (`../README_LEAN.md`, "What is proved") and the four datasheets, not copied from the proof file,
  by Claude Code on 23 November 2026, through three drafters that were given only that English
  and the definitions below.  Where a statement here differs from the published one, the
  difference is the finding and has been left in place; README.md lists each one and says
  whether the judge is expected to accept or reject it.

  The definitions are copied from the published file unchanged: the judge compares, by name,
  every constant a statement uses, so they have to be the same constants.  Everything else in
  this file is a theorem with `sorry` for its proof.  No imports, as in the published file; no
  `open`, no `set_option`, no notation, no definitions of its own.
-/

/-! ## The definitions, copied unchanged from `../TetrasemaphoreAlgebra.lean` at tag `v1.2.0` (commit 63541c93)
    Only what the seventeen statements need. -/

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

/-- The list of all four moves. -/
def all : List Move := [I, sv, sh, C2]

end Move

/-- `Invariant g S` says: the figure `S` looks the same after the move `g`. -/
def Invariant (g : Move) (S : Pt → Prop) : Prop := ∀ p, S (Move.act g p) ↔ S p

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

/-- The five subgroups of T8, as a list. -/
def fiveSubgroups : List MoveSet := [subI, subSv, subSh, subC2, subAll]

/-- A figure given by a finite list of points. -/
def ofList (L : List Pt) : Pt → Prop := fun p => p ∈ L

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

/-! ## The seventeen statements

  Each is preceded by the English it was written from: the handoff's row (the claim in the
  note's or the guide's words), with the guide's or the datasheet's sentence where that fixes
  the reading.  Every proof is `sorry`. -/

/-- "Looking two moves up in the table is the same as making them in turn."  Guide: "looking up two
    moves in the table and applying the result does the same thing to a point as applying the two
    moves in turn."  `mul g h` is "do `h`, then `g`". -/
theorem Move.act_mul (g h : Move) (p : Pt) :
    Move.act (Move.mul g h) p = Move.act g (Move.act h p) := sorry

/-- "Each move is its own way back."  Site: "Every move is its own way back: the diagonal is all I." -/
theorem T1_self_inverse (g : Move) : Move.mul g g = Move.I := sorry

/-- "Order does not matter."  Site: "the table reads the same across its diagonal." -/
theorem T1_mul_comm (g h : Move) : Move.mul g h = Move.mul h g := sorry

/-- "The list of four catches every move" (guide: "the list `[I, sv, sh, C2]` catches every move in
    this alphabet"). -/
theorem T1_mem_all (g : Move) : g ∈ Move.all := sorry

/-- "... and the four are all different" (guide: "with the four entries all different, so 'four' is
    exact rather than loose"). -/
theorem T1_all_distinct : Move.all.Nodup := sorry

/-- "Two different moves send some point to different places."  Guide: "Given two different names,
    there is a point they send to different places." -/
theorem T2_faithful (g h : Move) (hne : g ≠ h) :
    ∃ p : Pt, Move.act g p ≠ Move.act h p := sorry

/-- "Gold: I leaves the whole figure in place."  Guide: "NORMATIVE holds the whole plane." -/
theorem T4_fix_I (p : Pt) : Move.act Move.I p = p := sorry

/-- "Gold: the left-to-right flip leaves exactly the vertical line in place."  Datasheet: "σᵥ fixes
    (x, y) exactly when x = 0: the vertical axis." -/
theorem T4_fix_sv (x y : Int) : Move.act Move.sv (x, y) = (x, y) ↔ x = 0 := sorry

/-- "Gold: the top-to-bottom flip leaves exactly the horizontal line in place."  Datasheet: "σₕ fixes
    (x, y) exactly when y = 0: the horizontal axis." -/
theorem T4_fix_sh (x y : Int) : Move.act Move.sh (x, y) = (x, y) ↔ y = 0 := sorry

/-- "Gold: the half-turn leaves exactly one point in place."  Datasheet: "C₂ fixes (x, y) exactly when
    x = 0 and y = 0: the centre alone." -/
theorem T4_fix_C2 (x y : Int) : Move.act Move.C2 (x, y) = (x, y) ↔ (x = 0 ∧ y = 0) := sorry

/-- "A figure that survives both flips survives the half-turn."  A figure is any `S : Pt → Prop`;
    `Invariant g S` says the figure looks the same after the move `g`. -/
theorem T7_both_mirrors (S : Pt → Prop) (hv : Invariant Move.sv S) (hh : Invariant Move.sh S) :
    Invariant Move.C2 S := sorry

/-- "Exactly five sets of moves are closed, and no sixth."  Guide: "Of those sixteen, five are
    subgroups: `{I}` alone, the three two-element ones `{I, sv}`, `{I, sh}`, `{I, C2}`, and all
    four together."  Read as subgroups (contains the identity and is closed): under `MoveSet.closed`
    alone the empty set is a sixth closed set, so the literal reading of "closed" is false. -/
theorem T8_five_are (s : MoveSet) : isSubgroup s = true ↔ s ∈ fiveSubgroups := sorry

/-- "The moves any figure survives are one of those five sets."  Guide: "Take any figure whatsoever
    ... The set of moves it survives is literally one of the five subgroups of T8." -/
theorem S1_one_of_five (S : Pt → Prop) :
    ∃ s : MoveSet, s ∈ fiveSubgroups ∧ ∀ g : Move, (s.mem g = true ↔ Invariant g S) := sorry

/-- "The sigma-v mark survives only the left-to-right flip (and doing nothing)."  Datasheet: "the mark
    is invariant under k exactly when k is I or σᵥ."  The mark here is the model mark `mark Move.sv`,
    a finite list of points. -/
theorem S2_mark_sv_exact (k : Move) :
    Invariant k (ofList (mark Move.sv)) ↔ (k = Move.I ∨ k = Move.sv) := sorry

/-- "The sigma-h mark survives only the top-to-bottom flip (and doing nothing)."  Datasheet: "the mark
    is invariant under k exactly when k is I or σₕ." -/
theorem S2_mark_sh_exact (k : Move) :
    Invariant k (ofList (mark Move.sh)) ↔ (k = Move.I ∨ k = Move.sh) := sorry

/-- "The C2 mark survives only the half-turn (and doing nothing)."  Datasheet: "the mark is invariant
    under k exactly when k is I or C₂." -/
theorem S2_mark_C2_exact (k : Move) :
    Invariant k (ofList (mark Move.C2)) ↔ (k = Move.I ∨ k = Move.C2) := sorry

/-- "The I mark survives every move."  Datasheet: "the I mark is invariant under every move." -/
theorem S2_markAll_invariant (k : Move) : Invariant k (ofList markAll) := sorry
