# Tetrasemaphore — Methods Note 01

**Status:** DRAFT for red-team review. Nothing in this note is validated. Each item states what it claims, what it does not establish, and what would falsify it.
**Origin:** Extracted from an exploratory dialogue on 2026-10-11. The dialogue is case material only. No claim below depends on facts about any individual.

---

## Summary

This note proposes four working principles for the Tetrasemaphore method:

1. **Carrier color** is correlated error, not random error.
2. The core operation is the **search for invariants under reflection**, not averaging between positions.
3. A candidate instrument scores **resistance to plausible consensus falsehood** rather than pattern-building speed.
4. **Untried space** is a deliberate search target.

A worked example follows: the project's own rename, which applies principle 2 to its title.

---

## 1. Carrier color is correlated error

**Claim.** Carrier color is error that a group shares. It is a premise that members accept together because it is socially confirmed, not because anyone checked it. It differs from individual bias, which varies from person to person.

**Why the distinction matters.** Random error averages out across observers. Correlated error does not; adding observers who share it makes it stronger. A carrier-color claim therefore looks like an established fact, because many people agree with it.

**Operational consequence.** Carrier color should be detectable by its signature. Agreement on the claim is high, but evidence that was independently checked is low or absent. The test question is: *how many of the people who agree with this claim each checked it independently?*

**Not established.** No measurement procedure exists yet. "Detectable" is a hypothesis.

**Falsifier.** If, across a set of claims, high consensus with low independent verification does not predict falsity at a higher rate than high consensus with high verification, the signature carries no information.

---

## 2. Invariants under reflection, not the middle

**Claim.** The method's core operation is not "find the middle ground between positions." Instead it:

- states a claim;
- applies transformations to the frame (reverse it, take the opposing view, take the forbidden or unpopular view, change cultural or linguistic context);
- keeps only what holds under **every** transformation.

**Formal anchor.** The Klein four-group V₄ is isomorphic to the dihedral group D₂, the symmetry group of a non-square rectangle. It contains:

- the identity;
- two reflections;
- one 180° rotation.

So the four-state structure already *is* a reflection group. The method's operation matches the algebra's actual content, which is symmetry and invariance. It does not match averaging. *(Isomorphism V₄ ≅ D₂ is standard group theory; verify against a group-theory text before publication.)*

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

**Hard constraint: answer-key integrity.** The test is only valid if its answer key is free of the test authors' own carrier color. If an author marks a consensus non-fact as "true," the instrument inverts and rewards conformity. Required mitigations, at minimum:

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

The project was originally named for the owl, on the premise "owl = wisdom." Under a change of cultural frame, the symbol does not hold. In parts of Latin American folklore the owl is associated with ill omen or witchcraft rather than wisdom. *(This is a relayed claim, consistent with general folklore knowledge but not verified against a primary ethnographic source for this note. Verify before publishing.)*

The symbol failed under reflection, so it was carrier color: a local consensus mistaken for a universal meaning. The replacement name refers to the four-fold structure, which is mathematical and therefore frame-invariant.

**Record handling.** The published Owl Semaphore V3 record will receive an update that points to the new Tetrasemaphore DOI and states the reason for the change. The old record stays visible and is superseded in place, not removed.

---

## What this note does not show

- No principle here has been tested.
- No principle here has been compared against a baseline.
- No principle here has been replicated by anyone.
- All four principles are hypotheses with stated falsifiers.
- The test design (principle 3) has substantial prior art and must be positioned against it before any claim of contribution.
