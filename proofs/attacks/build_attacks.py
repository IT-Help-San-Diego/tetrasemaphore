#!/usr/bin/env python3
"""Rebuild every attack named in the v2.2 second-opinion packet, and the eight
v2.1-era attacks of SCIENCE_CHECK_v2.2.md's table, from the honest v2.2 source.

Each attack is one edit, described in the packet in one line; the evidence files
of the packet itself are in a purged scratch directory, so these are rebuilt
from those descriptions rather than copied.  Usage:

    build_attacks.py <honest TetrasemaphoreAlgebra.lean> <outdir>
"""
import sys, pathlib, hashlib

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

# ---- the anchors every edit is relative to, checked rather than assumed ----
A_T8 = "theorem T8_sixteen : allSubs.length = 16 := by decide"
A_AND = "  | andF f g, r => f.holds r ∧ g.holds r"
A_OR = "  | orF f g,  r => f.holds r ∨ g.holds r"
A_IMAGEOF = "def imageOf (g : Move) (L : List Pt) : List Pt := L.map (Move.act g)"
A_FIVE = "theorem T8_five_count : (allSubs.filter isSubgroup).length = 5 := by decide"
A_PRINT_SV = "#print axioms S2_mark_sv_exact_via_general"
A_SEED = "def seed : List Pt := [(1, 1), (2, 1), (3, 1), (1, 2), (1, 3)]"
A_PRINT_T8 = "#print axioms T8_sixteen"
for a in (A_T8, A_AND, A_OR, A_IMAGEOF, A_FIVE, A_PRINT_SV, A_SEED, A_PRINT_T8):
    assert src.count(a) == 1, f"anchor not unique: {a!r}"

attacks = {}


def put(name, text, what):
    assert text != src, f"{name}: the edit changed nothing"
    attacks[name] = (text, what)


def sub(old, new, text=None):
    t = src if text is None else text
    assert t.count(old) == 1, f"not unique: {old[:60]!r}"
    return t.replace(old, new)


# --- section 2, the blocker ------------------------------------------------
put("N1_hidden_instance",
    sub(A_T8,
        "instance _i : OfNat Nat 16 := \u27e8allSubs.length\u27e9\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "a hidden instance under a name Lean calls internal rebinds the numeral in "
    "T8_sixteen, which becomes allSubs.length = allSubs.length")

put("K1d_proofN_name",
    sub(A_T8,
        "instance proof_1 : OfNat Nat 16 := \u27e8allSubs.length\u27e9\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "the same with the name proof_1, which Name.isInternalDetail also calls "
    "internal and which has no leading underscore")

put("N1b_false_row_hidden_instance",
    sub(A_FIVE,
        A_FIVE + "\n\n"
        "instance _k : OfNat Nat 3 := \u27e8(allSubs.filter isSubgroup).length\u27e9\n\n"
        "theorem T8_three_count : (allSubs.filter isSubgroup).length = 3 := rfl\n\n"
        "#print axioms T8_three_count"),
    "a hidden _k proves a count that is false (the true value is 5); as "
    "submitted it fails on the listing count, and after the listing is "
    "regenerated the row reads as a proved falsehood")

put("N1c_visible_instance",
    sub(A_T8,
        "instance inst16vis : OfNat Nat 16 := \u27e8allSubs.length\u27e9\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "the control: the same attack under a visible name, which v2.2 caught on "
    "the listing alone")

put("N1e_aux_named_instance",
    sub(A_T8,
        "instance Move.act._f : OfNat Nat 16 := \u27e8allSubs.length\u27e9\n\n"
        "theorem T8_sixteen : allSubs.length = 16 := rfl"),
    "written here, not in the packet: the same instance under a name that is "
    "both a shape Lean generates and the child of a listed declaration, which "
    "v2.3's name classification accepts as an auxiliary")

# --- section 3, should-fix -------------------------------------------------
put("N6_eval_sees_wrapper",
    sub(A_T8,
        'open Nat in #eval (IO.FS.withFile "evidence_N6.txt" IO.FS.Mode.append '
        'fun h => h.putStrLn "the gate ran this")\n\n' + A_T8),
    "open X in <command> satisfies an allowlist that reads the first word of a "
    "line, so a smuggled #eval runs disk IO while the gate is running")

put("N6b_indented_eval",
    sub(A_T8,
        '  #eval (IO.FS.withFile "evidence_N6b.txt" IO.FS.Mode.append '
        'fun h => h.putStrLn "the gate ran this too")\n\n' + A_T8),
    "written here, not in the packet: the same IO from an #eval that is merely "
    "indented, which Lean accepts as a top-level command and v2.2's allowlist "
    "never looks at")

put("N3b_extern_existing_def",
    sub(A_IMAGEOF, '@[inline, extern "lean_nat_add"]\n' + A_IMAGEOF),
    "an extern attribute in second position on an already-listed definition: "
    "v2.2's pattern matched extern only as the first attribute")

put("F2_string_sorry",
    sub(A_SEED,
        'def noteText : String := "contains sorry and axiom and set_option as prose"\n\n'
        + A_SEED),
    "honest Lean that v2.2 refused: a string literal carrying banned words, "
    "which the scanner did not blank")

put("Comm_tamper_dangling_print",
    sub(A_PRINT_SV, "#print axioms Nat.add_comm"),
    "the tamper that only the comm-based checks catch: a theorem's #print "
    "axioms line replaced by one naming a core lemma, so one theorem is "
    "unprinted and one printed name is not a theorem of this file")

# --- honest control --------------------------------------------------------
put("F1_honest_variants",
    sub(A_T8,
        "/-- sorry sorryAx admit axiom opaque native_decide unsafe set_option\n"
        "    implemented_by extern partial import: every word this gate refuses,\n"
        "    written in a doc comment, where it is prose and not code. -/\n"
        + A_T8 + "\n\nnamespace Extra\n\n"
        "theorem extra_sixteen : allSubs.length = 16 := by decide\n\n"
        "#print axioms Extra.extra_sixteen\n\nend Extra"),
    "the honest variant that has to pass: a doc comment made of banned words, "
    "a namespaced extra theorem with its own #print axioms line")

# --- section 5's rows that were never tested -------------------------------
put("S5_22_attr_newline_axiom",
    sub(A_T8,
        "@[simp]\naxiom ZA_evil : Move.sv = Move.sh\n\n" + A_T8),
    "section 5 row 2.2, never tested: an axiom whose attribute sits on the "
    "line above it, so the declaration line does not begin with the word")

put("S5_31_keyword_split_newline",
    sub(A_T8, "set_option\n  debug.skipKernelTC true in\n" + A_T8),
    "section 5 row 3.1, never tested: a keyword split from its argument across "
    "a line break, which Lean reads as whitespace")

put("S5_24_exit",
    sub(A_FIVE, "#exit\n\n" + A_FIVE),
    "section 5 row 2.4, not re-tested since v2.1: #exit cuts the file short, "
    "so the theorems after it are never elaborated")

# --- the eight v2.1-era attacks of SCIENCE_CHECK's table --------------------
put("a2_guard_msgs_printaxioms",
    sub(A_PRINT_T8, "#guard_msgs(drop info) in\n" + A_PRINT_T8),
    "v2.1 (a): a theorem's own #print axioms line swallowed by "
    "#guard_msgs(drop info)")

put("a5_macro_decide_native",
    sub(A_T8,
        'macro "kernelcheck" : tactic => `(tactic| decide +native)\n\n'
        "theorem T8_sixteen : allSubs.length = 16 := by kernelcheck"),
    "v2.1 (c, g): decide +native behind a macro alias")

put("a9_quoted_sorryAx",
    sub(A_T8, "theorem T8_sixteen : allSubs.length = 16 := "
        "@\u00absorryAx\u00bb _ false"),
    "v2.1 (f): sorryAx written inside French quotation marks")

put("a10_macro_command",
    sub(A_PRINT_T8,
        'syntax "printax" ident : command\n'
        "macro_rules | `(printax $n) => `(#print axioms $n)\n"
        "printax T8_sixteen"),
    "v2.1 (g): a command of the file's own standing in for #print axioms")

put("a13_extern_space",
    sub(A_IMAGEOF,
        '@[ extern "lean_imageof"] opaque imageOfExtern (g : Move) '
        "(L : List Pt) : List Pt\n\n" + A_IMAGEOF),
    'v2.1 (h): @[ extern "…"] opaque, with a space after the bracket')

put("a15_full_chain",
    sub(A_PRINT_T8,
        "#guard_msgs(drop info) in\n" + A_PRINT_T8 + "\n"
        '#eval IO.println "\'T8_sixteen\' does not depend on any axioms"',
        sub(A_T8,
            'macro "kernelcheck" : tactic => `(tactic| decide +native)\n\n'
            "theorem T8_sixteen : allSubs.length = 16 := by kernelcheck")),
    "v2.1 (c, e, g): macro-hidden decide +native plus a forged footprint")

put("a16_macro_sorry",
    sub(A_T8,
        'macro "obvious" : tactic => `(tactic| sorry)\n\n'
        "theorem T8_sixteen : allSubs.length = 16 := by obvious"),
    "v2.1 (f): sorry reached only through a macro alias")

put("a17_poison_audit",
    sub(A_T8,
        "namespace Lean\n\n"
        "def collectAxioms (n : Nat) : Nat := n\n\n"
        "end Lean\n\n" + A_T8),
    "v2.1 (h): namespace Lean declaring a name the checking program's own "
    "machinery uses")

# --- the two further spellings of 3.5, and 3.4 as the skeptic wrote it ------
put("M1a_holds_arm_swap",
    sub(A_OR, "  | andF f g, r => f.holds r \u2228 g.holds r",
        sub(A_AND, "  | orF f g,  r => f.holds r \u2227 g.holds r")),
    "the packet's own file: the arms swapped, so the arm order changes and the "
    "right-hand sides stay where they were; both halves of v2.2's listing are "
    "byte-identical to the honest build")

put("M1b_holds_rhs_swap",
    sub(A_AND, "  | andF f g, r => f.holds r \u2228 g.holds r",
        sub(A_OR, "  | orF f g,  r => f.holds r \u2227 g.holds r")),
    "the other spelling: the right-hand sides swapped with the arm order left "
    "alone, which v2.2 catches on the Fml.holds.eq_def row")

put("N3b_extern_sameline",
    sub(A_IMAGEOF, '@[inline, extern "lean_nat_add"] ' + A_IMAGEOF),
    "3.4 as skeptic 2 wrote it: the attribute on the same line as the "
    "definition, which the allowlist does not reject as an unrecognised line")

index = []
for name, (text, what) in sorted(attacks.items()):
    d = out / name
    d.mkdir(exist_ok=True)
    p = d / "TetrasemaphoreAlgebra.lean"
    p.write_bytes(text.encode())
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    index.append((name, h, what))
    print(f"{name}\t{h}")

(out / "ATTACKS.tsv").write_text(
    "".join(f"{n}\t{h}\t{w}\n" for n, h, w in index))
print(f"{len(index)} attack files written to {out}")
