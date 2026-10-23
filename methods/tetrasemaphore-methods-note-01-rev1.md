# Tetrasemaphore — Methods Note 01

**Status:** DRAFT for red-team review. Nothing in this note is validated. Each item states what it claims, what it does not establish, and what would falsify it.
**Origin:** Drafted by Claude Chat (Anthropic) at the end of an exploratory dialogue with Carey on 2026-10-11; revision 1 by Claude Science. The dialogue is case
material only. No claim below depends on facts about any individual. **Revision:** 1, proposed by Claude Science on 2026-10-11 from its red-team review and
Carey's answers to it. The changes and the reason for each are listed at the end. The original is unchanged at `tetrasemaphore-methods-note-01.md`.

---

## Summary

This note proposes four working principles for the Tetrasemaphore method:

1. **Carrier color** has several working definitions, kept side by side and open. Its shared case, correlated error, is the one principle 3 targets.
2. The core operation is the **search for invariants under reflection**, not averaging between positions.
3. A candidate instrument scores **resistance to plausible consensus falsehood** rather than pattern-building speed.
4. **Untried space** is a deliberate search target.

A worked example follows: the project's own rename, which applies principle 2 to its title.

---

## 1. Carrier color: working definitions (open)

**Status.** Open by design. The definitions below are kept side by side. A definition is added when it explains a case the others miss, and two are merged only when one is shown to cover the other. Which of them, if any, is *the* definition is a question for peer review.

| | Working definition | Where it comes from | What it explains | What it leaves out |
|---|---|---|---|---|
| D1 | The meaning a carrier (a picture, a word, a symbol) brings with it, beyond the structure it carries | the project record and the public note; SciSpace's "social" sense is close to it ("learned, datable per receiver") | the owl: one picture, different meanings for different readers | error that is not about meaning |
| D2 | Error that a group shares: a premise accepted together because it is socially confirmed, not because anyone checked it | this note, from the 2026-10-11 dialogue | why agreement can make a false claim look established | one person's frame |
| D3 | One person's history coloring one claim | the same dialogue, where the term is used this way | a personal prior riding onto an unrelated claim | error that a group shares |
| D4 | *Question:* does carrier color also attach to output from a system that generates, such as an AI model? | Carey, 2026-10-11 | see below | untested |
| D5 | Perceptual: the physical properties of the medium change how the signal is processed, independent of its content | SciSpace's revision of the dose 01 document (September 2026), citing Pegado, Nakamura, Cohen & Dehaene 2011 (NeuroImage 55:742-749, doi:10.1016/j.neuroimage.2010.11.043), where the brain's word-reading area told mirror-image single letters apart in skilled readers, yet treated mirror-image pictures of matched complexity as the same | why a left-right flip can show on a letter and vanish on a picture | meaning |

**D4: two cases from this project's own record.** An AI search assistant built on a figure its user had not checked, instead of correcting it (6 October 2026). This note's own D2 wording entered from an AI dialogue, where it was accepted without being checked against D1 (2026-10-11). A mechanism is documented: language models tend to agree with the views of the person they are talking to (Sharma et al. 2023, "Towards Understanding Sycophancy in Language Models", arXiv:2310.13548).

**Candidate invariant (not established).** In every definition so far, carrier color is something the structure itself does not determine, added by a frame: the sender's or the receiver's, one person's or a group's, a human's or a system's. *Falsifier:* a case everyone would call carrier color in which no frame adds anything, or a frame-added meaning nobody would call carrier color.

### The shared case: correlated error (D2)

**Claim.** When a group shares a frame, carrier color becomes error the group shares: a premise members accept together because it is socially confirmed, not because anyone checked it. Unlike one person's bias, it does not cancel out across observers.

**Why the distinction matters.** Random error averages out across observers. Correlated error does not. Adding observers who share it does not shrink it. More people agree, and their confidence rises, so the error looks more like an established fact.
- *Arithmetic:* if n observers share an error b and each adds independent noise of spread s, their average is off by b plus noise of spread s/√n. As n grows the noise shrinks and b stays.
- *Experiment:* Lorenz, Rauhut, Schweitzer & Helbing 2011, PNAS 108:9020-9025, doi:10.1073/pnas.1008636108. Seeing others' estimates narrowed the spread of estimates without improving their collective error, and raised confidence.

**Operational consequence.** Carrier color should be detectable by its signature. Agreement on the claim is high, but evidence that was independently checked is low or absent. The test question is: *how many of the people who agree with this claim each checked it independently?*

**Not established.** No measurement procedure exists yet. "Detectable" is a hypothesis.

**Falsifier.** If, across a set of claims, high consensus with low independent verification does not predict falsity at a higher rate than high consensus with high verification, the signature carries no information.

---

## 2. Invariants under reflection, not the middle

**Claim.** The method's core operation is not "find the middle ground between positions." Instead it:

- states a claim;
- applies transformations to the frame (reverse it, take the opposing view, take the forbidden or unpopular view, change cultural or linguistic context);
- keeps only what holds under **every** transformation.

**Formal anchor.** The Klein four-group V₄ is isomorphic to the dihedral group of order 4, D₂, the symmetry group of a non-square rectangle. (Textbooks that name dihedral groups by their order write D₄.) It contains:

- the identity;
- two reflections;
- one 180° rotation.

So the four-state structure already *is* a reflection group. The method's operation matches the algebra's actual content, which is symmetry and invariance. It does not match averaging. *(Standard group theory, checked: of the square's eight symmetries, exactly I, σᵥ, σₕ and C₂ also map a 2 × 1 rectangle onto itself. The project's Lean file proves the square's eight, `S4_eight_are_all`, and that each of the four moves undoes itself, `T1_self_inverse`.)*

**Why "middle" fails.** A midpoint is defined on the axis that the disputing parties chose. Standing at the midpoint accepts their axis. An invariant is defined independently of any position on that axis, so it can expose the axis itself as the unexamined premise.

**Not established.** That this operation produces more accurate judgments than alternatives. That is an empirical claim and remains untested.

**Falsifier.** Run a comparison. If raters using invariant-search do not outperform raters using position-averaging on claims with known ground truth, the claimed advantage fails.

---

## 3. Candidate instrument: resistance to consensus falsehood

**Claim.** A useful measure of reasoning quality is how reliably a person refuses to accept a plausible, socially endorsed falsehood. A test of this kind would contain:

- immutable, independently verifiable facts, each presented from several angles;
- interleaved widely accepted non-facts;
- scoring of each non-fact accepted as fact as a failure.

**Rationale.** Pattern-building ability can make this failure worse. A stronger pattern-builder can build a more convincing rationalization for a false premise.

**Correction to the source dialogue.** The dialogue called this concept "novel." That is withdrawn. Closely related prior work exists and must be read and cited before any novelty claim. These are pointers to read in the original, not citations:

- the Cognitive Reflection Test (Frederick, 2005);
- the Comprehensive Assessment of Rational Thinking / rationality quotient work (Stanovich, West & Toplak, 2016);
- misinformation-susceptibility instruments such as the MIST (Maertens et al., 2023).

The possible contribution is narrower. It would come from targeting *correlated* consensus falsehoods specifically, rather than general reasoning errors. Whether that distinction is new is **not established**.

**Hard constraint: answer-key integrity.** The test is only valid if its answer key is free of the test authors' own carrier color. If an author marks a consensus non-fact as "true," the instrument inverts and rewards conformity. Items are limited to claims that can be checked against evidence; matters of faith and of value are outside the instrument. Required mitigations, at minimum:

- every keyed item must cite independently checkable primary evidence;
- item review must use reviewers from different cultural and disciplinary frames, applying principle 2 to the answer key itself;
- items that fail under frame change are dropped, not adjudicated.

**Falsifier.** If test scores do not predict accuracy on held-out consensus-falsehood items better than existing instruments (CRT, CART, MIST) do, the instrument adds nothing.

---

## 4. Untried space as a search target

**Claim.** Method audits usually cover what was done: what worked and what failed. The proposal adds a third category, **what was never tried**, as an explicit search target. That includes approaches skipped because consensus said they would not work, which is principle 1 applied to the research process.

**Prior art to engage.** Publication bias and the file-drawer problem (unreported negative results) are related, well-documented phenomena. This principle extends the audit from *unreported* attempts to *unattempted* ones.

**Procedure (draft).** For each research question, maintain three ledgers:

| Ledger | Contents |
|---|---|
| Tried, worked | Approaches attempted that produced results |
| Tried, failed | Approaches attempted that did not |
| Not tried | Each untried approach plus the stated reason it was skipped |

Any skip reason that is consensus rather than evidence gets flagged for review.

**Not established.** That this ledger yields discoveries at a rate that justifies its cost.

---

## Worked example: Owl Semaphore → Tetrasemaphore

The project was originally named for the owl, on the premise "owl = wisdom." Under a change of cultural frame, the symbol does not hold: the sources show owls read differently between countries, between centuries and between neighbours (public note, "Why we left the owl").

The symbol failed under reflection, so it was carrier color: a local consensus mistaken for a universal meaning (D1, shared as in D2). The replacement carries the four-fold structure, which is mathematical and the same in every frame. The name, the notation and the colors remain conventions, and the public note lists them.

**Record handling.** The published Owl Semaphore record keeps its title and versions. A metadata-only edit links it to the new Tetrasemaphore DOI and says why the project moved on.

---

## Related work

Carrier color is a new name for an old observation, studied under other names. Communication research holds that every message has a content
aspect and a relationship aspect, and that the relationship aspect tells the receiver how to take the content (Watzlawick, Beavin & Jackson 1967,
*Pragmatics of Human Communication*). Semiotics calls the second-order meanings that a culture lays over a sign's literal meaning its connotation
(Barthes 1964, *Elements of Semiology*). Media theory makes a stronger claim, that a medium's own characteristics shape its effects more than the
content it carries does (McLuhan 1964, *Understanding Media*, chapter 1); definition D5 is the closest to it.

The four-group has also described reasoning before. Piaget held that formal reasoning rests on two structures that appear only at the stage
of formal operations: a combinatorial system, and a group of four transformations, identity, negation, reciprocal and correlative (the INRC
group), which he modelled on Klein's four-group (Inhelder & Piaget 1958, *The Growth of Logical Thinking: From Childhood to Adolescence*,
doi:10.1037/10034-000); its mathematics was later examined in detail (Ascher 1984, *Journal of Mathematical Psychology* 28:282-316,
doi:10.1016/0022-2496(84)90002-6).

None of this is claimed as new here. What the project tries is narrower: to carry four states with notation rather than a picture, and to test
whether readers read them the same way.

## What this note does not show

- No principle here has been tested.
- No principle here has been compared against a baseline.
- No principle here has been replicated by anyone.
- All four principles are hypotheses with stated falsifiers.
- The test design (principle 3) has substantial prior art and must be positioned against it before any claim of contribution.

---

## Revision 1: what changed and why

- **Principle 1, the definition: kept open, not corrected.** The single definition became four working definitions side by side (D1, D2, D3 and D5) and one open question (D4), with a candidate invariant and its falsifier. This follows Carey's answer: keep what is valid; when two ideas are equally good, keep both and ask why they are not one yet. D4 is his question about AI.
- **Principle 1, more observers: a correction, by arithmetic and experiment** (shown in the section). The earlier sentence said shared error grows with more observers. The error stays the same size; what grows is agreement and confidence.
- **Principle 2, the name of the group:** "the dihedral group of order 4" added, because textbooks differ on whether this group is D₂ or D₄. The check replaces "verify before publication".
- **Worked example, the relayed claim: withdrawn.** The sentence that owls are associated with ill omen or witchcraft in parts of Latin American folklore is replaced by what the sources show: readings differ between countries, between centuries and between neighbours. The source search of 11 October 2026 answered the question its parenthetical left open.
- **Worked example:** "the same in every frame" now applies to the structure only; the name, notation and colors are conventions. The source dialogue said the same in its own earlier turns.
- **Record handling:** the wording matches the DOI decision of 9 October 2026 (a new DOI, linked both ways) and Carey's own words in the dialogue of 2026-10-11, that the owl record "will get an update that points to the new DOI ... and explains why".
- **D5 added:** SciSpace's perceptual sense, from its September revision, kept per the same rule.
- **Unchanged:** principles 3 and 4, their falsifiers, and "What this note does not show".
- **New: Related work.** Carey, 21 October 2026: "So yes, I love anytime we can do something like carrier color new name for an old observation." Sources checked by Science the same day; Carey approved the section on 22 October 2026, on the condition that the Piaget facts are certain.
