#!/usr/bin/env python3
"""Rebuild every attack of the v2.3 second-opinion packet from its description.

The packet's evidence tree is in a purged scratch directory, so each attack here
is built from the one-line description the packet gives it, applied to the
honest v2.3 source (f066faf6595d22e9, byte-identical to v2.2's).

Usage: build_attacks_v24.py <honest TetrasemaphoreAlgebra.lean> <outdir>
"""
import sys, pathlib, hashlib

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

A_T8 = "theorem T8_sixteen : allSubs.length = 16 := by decide"
A_T8_PRINT = "#print axioms T8_sixteen"
A_T10 = """theorem T10_det_table :
    Move.det Move.I = 1 ∧ Move.det Move.C2 = 1 ∧
    Move.det Move.sv = -1 ∧ Move.det Move.sh = -1 := by decide"""
for a in (A_T8, A_T8_PRINT, A_T10):
    assert src.count(a) == 1, f"anchor not unique: {a[:50]!r}"

attacks = {}


def put(name, text, what):
    assert text != src, f"{name}: the edit changed nothing"
    attacks[name] = (text, what)


def sub(old, new, text=None):
    t = src if text is None else text
    assert t.count(old) == 1, f"not unique: {old[:60]!r}"
    return t.replace(old, new)


# --- L3-BLOCKER-1: the char literal desyncs the scanner --------------------
put("DESYNC_EVAL",
    src + '\ndef dq : Char := \'"\'\n'
    '#eval (do IO.FS.writeFile "EVID_DESYNC.txt" "the eval ran during the gate"; pure ())\n'
    'def rebalance : String := "x"\n',
    "a char literal holding a double quote desyncs scan(), so the #eval on the "
    "next line is blanked, the file is elaborated and the IO runs during the gate")

put("DESYNC_RAWSTRING",
    src + '\ndef rs : String := r#"a " b"#\n'
    '#eval (do IO.FS.writeFile "EVID_RAW.txt" "the eval ran during the gate"; pure ())\n'
    'def rebalance2 : String := "x"\n',
    "written here: the same desync through a raw string, where the backslash "
    "does not escape and the quotation mark inside closes nothing")

put("DESYNC_EOF",
    src + '\ndef dq2 : Char := \'"\'\n'
    'def tail : String := "the file ends inside a string\n',
    "written here: the scanner reaches end of file inside a string, which v2.3 "
    "does not notice")

# --- L3-BLOCKER-2: OfNat behind a reducible abbrev ------------------------
put("ABBREVFALSE",
    src + "\nabbrev ThreeInst := OfNat Nat 3\n"
    "instance myThree : ThreeInst := ⟨(allSubs.filter isSubgroup).length⟩\n\n"
    "theorem T8_three_count_false : (allSubs.filter isSubgroup).length = 3 := rfl\n\n"
    "#print axioms T8_three_count_false\n",
    "an OfNat instance behind a one-line abbrev: section 3k takes the head of "
    "the instance's type and sees the abbrev, not OfNat, so a count of 5 is "
    "proved to be 3")

put("ABBREV16",
    sub(A_T8,
        "abbrev SixteenInst := OfNat Nat 16\n"
        "instance mySixteen : SixteenInst := ⟨allSubs.length⟩\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "the same wrapper rebinding the numeral of the existing public theorem "
    "T8_sixteen, which becomes allSubs.length = allSubs.length")

put("ABBREVFALSE_AUX",
    src + "\nabbrev Move.act._proof_1 := OfNat Nat 3\n"
    "instance Move.act._f : Move.act._proof_1 := ⟨(allSubs.filter isSubgroup).length⟩\n\n"
    "theorem T8_three_count_false : (allSubs.filter isSubgroup).length = 3 := rfl\n\n"
    "#print axioms T8_three_count_false\n",
    "the aux-shaped wrapper: both added constants carry names the gate "
    "classifies as auxiliaries of listed declarations, so their rows land among "
    "the 345 in the third section")

put("ABBREV16_AUX",
    sub(A_T8,
        "abbrev Move.act._proof_1 := OfNat Nat 16\n"
        "instance Move.act._f : Move.act._proof_1 := ⟨allSubs.length⟩\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "the aux-shaped wrapper on T8_sixteen, where the first two sections of the "
    "listing are byte-identical to the honest ones")

# --- L3-BLOCKER-3: a Neg instance rebinds -1 ------------------------------
put("NEGFALSE",
    src + "\ninstance Move.det._f : Neg Int := ⟨fun _ => Move.det Move.I⟩\n\n"
    "theorem T3_detI_is_neg_one : Move.det Move.I = -1 := rfl\n\n"
    "#print axioms T3_detI_is_neg_one\n",
    "a Neg instance under an aux-shaped name rebinds the literal -1, which "
    "section 3k never inspects: det I = -1 is proved where the determinant is 1")

put("NEGFALSE_VISIBLE",
    src + "\ninstance negIntVisible : Neg Int := ⟨fun _ => Move.det Move.I⟩\n\n"
    "theorem T3_detI_is_neg_one : Move.det Move.I = -1 := rfl\n\n"
    "#print axioms T3_detI_is_neg_one\n",
    "the same under a visible name, which is equally green because the gate has "
    "no check on Neg whatever the name is")

put("NEG_LOCAL_SECTION",
    src + "\nsection\n\n"
    "local instance negIntLocal : Neg Int := ⟨fun _ => Move.det Move.I⟩\n\n"
    "theorem T3_detI_is_neg_one : Move.det Move.I = -1 := rfl\n\n"
    "#print axioms T3_detI_is_neg_one\n\nend\n",
    "a local instance inside a section, the variant the packet's second skeptic "
    "reports; wrapped around an appended theorem here, because wrapping "
    "T10_det_table itself makes its own `decide` proof fail (measured), so the "
    "packet's file differs from its one-line description in a way this rebuild "
    "cannot recover")

# --- L3-SF-1: a forgeable aux name on an ordinary declaration -------------
put("AUXNAME_DEF",
    src + "\ndef Move.det._proof_1 : Nat := 0\n",
    "the enabling primitive of L3-SF-1: an author-declared constant under a "
    "name the gate classifies as a generated auxiliary, reported by no check")

# --- note 1: a projection-class instance swap -----------------------------
put("LTSWAP",
    src + "\ninstance (priority := 10000) myLT : LT Int := ⟨fun _ _ => True⟩\n\n"
    "theorem S2_fake_quadrant (q : Pt) : 0 < q.1 ∧ 0 < q.2 := ⟨trivial, trivial⟩\n\n"
    "#print axioms S2_fake_quadrant\n",
    "note 1: a projection-class instance swap, which passes after regeneration "
    "but prints the foreign instance name in the row, unlike the literal classes")

# --- fid23-1: a private declaration, for the per-toolchain count ----------
put("PRIVATE_DEF",
    src + "\nprivate def hiddenHelper : Nat := 0\n",
    "fid23-1's probe: a private declaration, which 3j reports while the "
    "per-toolchain line prints 'private declarations: 0' as a literal")

index = []
for name, (text, what) in sorted(attacks.items()):
    d = out / name
    d.mkdir(exist_ok=True)
    p = d / "TetrasemaphoreAlgebra.lean"
    p.write_bytes(text.encode())
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    index.append((name, h, what))
    print(f"{name}\t{h}")

(out / "ATTACKS_v24.tsv").write_text("".join(f"{n}\t{h}\t{w}\n" for n, h, w in index))
print(f"{len(index)} attack files written to {out}")
