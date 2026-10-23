# Test register: every way to check, red-team, prove or validate the Tetrasemaphore (Claude Science, 11 October 2026)

Carey, 11 October: "we should be collecting all of our good ideas like this of how we can always red team and check and prove and validate", and
"when we publish, we're very well directed and we don't distract people."

**How it keeps the publication focused.**
- The public note carries only the six tests a reader can run in minutes (part 1).
- Everything else lives here, and the note links to it once.
- A test moves up to the note only when a reader can run it without help.

**Updated 22 October 2026.** The camera test moved from the note to here (R4, C4), C5 and part 8, "The body and the exit", were
added, and the pictures are called semaphores, as in the note.

**Status:** proved · passed · in the note · designed (ready to run) · proposed (idea, not designed) · open (no method yet).
**Needs:** what running it takes.

## 1. In the public note: the reader's own tests
| # | Test | Status |
|---|---|---|
| R1 | Do the moves | in the note |
| R2 | Two mirrors make a half-turn | in the note |
| R3 | Take the colour away | in the note |
| R4 | Ask a camera | moved out of the note, 22 October 2026: no reader has passed it yet (C4) |
| R5 | Check the proofs | in the note |
| R6 | Teach it to someone | in the note |
| R7 | Ask what the picture means | in the note |

The note numbers its six tests in order: R1 to R3 are its tests 1 to 3, and R5 to R7 its tests 4 to 6.

## 2. Mathematics
| # | Claim tested | Test | Status | Needs |
|---|---|---|---|---|
| M1 | The four moves form the group the semaphores use | Lean v2.4: 118 theorems, the same statements and proofs since v2.2, zero imports; green on three Lean versions; 38 attack files, all failing against the committed listing; with the listing regenerated first, three pass: one honest variant and two spellings of one swapped definition, which shows in `STATEMENTS.md` (M2) | proved | nothing |
| M2 | The statements say what we claim | A reader who does not trust us reads `STATEMENTS.md` (the gate can check how a proof was made, not what it states) | designed | one sceptical reader |
| M3 | The checker catches every attack built against it so far | Claude Code's reviews: v2.2 (one blocker, fixed in v2.3), v2.3 (three blockers, fixed in v2.4); for v2.4, Claude Code re-runs its existing attacks, with no new hunt (Carey, 22 October 2026). A checker refuses only the tricks its authors know of, so the published file is also checked by its hash against the DOI record and by reading `STATEMENTS.md` (M2) | in progress | Claude Code |
| M4 | σᵥ and C₂ differ without using the determinant | A stronger theorem | open | a proof |

## 3. The semaphores as objects
| # | Claim tested | Test | Status | Needs |
|---|---|---|---|---|
| C1 | Each mark survives only its own move | Survival scores in every build check | passed (build 6) | re-run on build 7 |
| C2 | Each build changes only what it says | The six build-7 checks | designed | build 7 (Tuesday) |
| C3 | The fine detail survives cloth and washing | Calibration tile 2: photos after printing, then after 1 and 5 washes | designed | a print order |
| C4 | A camera reads the formula correctly | The four readable-half cards in `scan-cards/`, one at a time; a pass is the symbol alone (I, σᵥ, σₕ or C₂), "finds a formula" is not a pass, the first try counts and every try is reported. The whole semaphores are a known limit: a transcriber cannot read a mirrored glyph | not passed. October 2026, phone readers: they did not read the cards reliably. 22 October 2026, Mathpix Snip on a phone, the cards shown on a computer screen, seven tries: one exact (σₕ, on its readable half), one with the right letter in the wrong case (σ_V), one whole semaphore read as a fraction, four with no result. The test returns to the note when a reader passes it | a phone and a formula reader |
| C5 | An AI model names the four states | The four readable-half cards, without words; a new chat, with memory and web search turned off where the product allows; the first answer counts; the model, the date and the settings are recorded. A pass names all four states and their moves. The project's pages are public, so a model may answer from them rather than from the card (benchmark contamination; Xu et al. 2024, arXiv:2406.04244) | proposed. Baseline, 6 October 2026, Google's AI Mode shown a word-free card, not a cold first answer: the moves 4 of 4, the names 3 of 4 (NORMATIVE's gold I read as the chemists' i, inversion) | an AI model |

## 4. Reading and teaching (tests with people)
| # | Claim tested | Test | Status | Needs |
|---|---|---|---|---|
| P1 | Moving the body helps people learn the states (Carey, 11 Oct) | One group flips the semaphore, then makes the move with the hands, then sees the symbol; the other sees pictures only. A week later both take the twenty-print test (note test 5). *Falsifier:* no difference at one week. *Background:* trained abacus users calculate by moving the beads of an imagined abacus; practised users' calculations are relatively insensitive to verbal interference (Frank & Barner 2012, Journal of Experimental Psychology: General 141:134-149, doi:10.1037/a0024427) and worse under motor interference, and their hands often move as if on a real abacus (Brooks, Barner, Frank & Goldin-Meadow 2018, Cognitive Science 42:554-575, doi:10.1111/cogs.12527). Mental abacus instruction has itself been tested in randomized classroom trials (Barner et al. 2016, Child Development 87:1146-1158, doi:10.1111/cdev.12515); a one-year trial found limited evidence that it helped (Barner et al. 2018, Journal of Numerical Cognition 3:540-558, doi:10.5964/jnc.v3i3.106). Citations checked against Crossref and the claims against the papers' own summaries, 22 October 2026 | proposed | people |
| P2 | Doing the moves raises intrinsic motivation | After the session, leave the semaphores out and record who keeps using them, unasked (the free-choice measure, Deci 1971). *Falsifier:* no difference in free-choice time | proposed | people |
| P3 | Practising the four states improves metacognition | Measure how well confidence tracks accuracy before and after practice (Fleming & Lau 2014) | proposed | people |
| P4 | Owl readings vary between neighbours, not only between countries | Note test 6, with the answers grouped by where people grew up and compared within one place (the Caldas survey found both) | proposed | people |
| P5 | The method can be learned and checked with nothing but the body and a scrap of paper (Carey, 11 Oct: for people without a device or printing) | Teach the two questions and the four moves by speaking and showing them. A week later: (a) the teacher makes one of the four body moves (stand still, turn around, look between the legs, both) and the learner names it; (b) the learner writes I, A, D and N on a scrap of paper, holds it to the light, turns it over side to side, turns it over top to bottom, and spins it half way round, each time from the start, and says which letter survives which move (measured: I survives all three; A, D and N one each, in DejaVu Sans Bold, Arial and Helvetica). *Falsifier:* no better than one in four | in the note (test 6 can be run with the body alone); not yet run | people; no equipment |
| P6 | The two moves commute in use: reversing the stance and then looking at the frame lands where doing them the other way round does | Give readers a claim; half make the stance move first, half the frame move first; compare where each group lands. *Falsifier:* the order changes the state, which a non-commuting structure would fit better than the four | proposed | readers |
| P7 | Four is easier to learn and undo than three, in the body | Teach one group the four (half-turns: turn around, look between your legs, a sideways tip-over, still facing forward) and another a three-state system (third-turns). A week later, ask each to undo random sequences of moves. *Falsifier:* no difference in errors. (A real cartwheel is none of the four: it turns the body sideways first. Withdrawn 21 October 2026.) | proposed | people; no equipment |
| P8 | A group's question-by-question verdict matches what its members chose | When several readers classify one text, compare the state given by the majority on each question with each reader's own state (computed example, 12 Oct: three readers, NON-NORMATIVE, METACOGNITIVE and CRITICAL, give CRITICAL by majorities, chosen by 1 of 3; List & Pettit 2002). Report every reader's state | proposed | readers |
| P9 | A single yes/no hides the second question in a predictable way (Carey's "binary under pressure", 12 Oct) | Give readers texts of known state. One group sorts them with only normative / non-normative, another with the four. Prediction from the table: with two labels, METACOGNITIVE texts go with NORMATIVE and CRITICAL texts with NON-NORMATIVE. *Falsifier:* they split at random, or by another pairing | proposed | readers |
| P10 | Which semaphore is hardest to read by eye, and whether the notation reads better than the owl | Time and score readers naming the state of prints, each left alone, flipped or turned at random. Two predictions from verified work: mirror symmetry about a vertical or horizontal axis is detected faster than half-turn symmetry (Royer 1981, doi:10.1037/0096-1523.7.6.1186), so CRITICAL's mark is the slowest; and the visual system treats a picture and its mirror image as the same (Pegado et al. 2011, doi:10.1016/j.neuroimage.2010.11.043), so states told apart by which way a picture faces (the owl edition) are confused more than states told apart by a mark's own symmetry (the notation edition). *Falsifier:* no difference between states, or the owl reads as well as the notation | proposed | readers; printouts or a screen |
| P11 | Whether someone watching can tell which of the four states another person's thinking is in: the outside side of the first-person paragraph (Carey, 21 Oct: "it also needs to be equally addressed on the other side") | For each of 20 short trials the thinker privately picks one of the four states and talks a problem through in it; an observer who is not told names the state. The observer writes down, separately, what they saw or heard and their own reading of it, so each miss can be traced. Chance is 1 in 4: 9 or more right of 20 gives p = 0.041, 11 or more p = 0.004 (binomial, computed 21 Oct). Prediction, from lie-truth judgments averaging 54% against 50% chance (Bond & DePaulo 2006, doi:10.1207/s15327957pspr1003_2): above chance, far from perfect. | Proposed, not run | Two people who agree to take part; 20 trials; a sheet |

**What the research already says about P1 and P2** (each checked against its abstract, 11 Oct):
- **Gesture:** children required to gesture correctly learned more than children required to gesture partly correctly, who learned more than children required
  not to gesture (Goldin-Meadow, Cook & Mitchell 2009, Psychological Science 20:267-272, doi:10.1111/j.1467-9280.2009.02297.x).
- **Gesture over handling objects:** only gesture led to success on problems that required generalizing what was learned (Novack et al. 2014,
  Psychological Science 25:903-910, doi:10.1177/0956797613518351). Hence P1's order: the semaphore first, then the hands alone, then the symbol.
- **Objects in maths:** small to moderate benefits over abstract symbols alone, larger for retention than for transfer, and dependent on the instruction
  (Carbonneau, Marley & Selig 2013, J. Educational Psychology 105:380-400, doi:10.1037/a0031084).
- **Movement that is part of the lesson:** in preschoolers, it gave the best learning, still there six weeks later, and more enjoyment than no movement
  (Mavilidi, Okely, Chandler & Paas 2017, Applied Cognitive Psychology 31:281-290, doi:10.1002/acp.3325). Enjoyment is not yet intrinsic motivation;
  that is P2.
- **Interesting but irrelevant additions:** they reduced recall of the main ideas and transfer, and did more harm when they came first (Harp & Mayer 1998,
  J. Educational Psychology 90:414-434, doi:10.1037/0022-0663.90.3.414).

**Design rule that follows:** every activity is the move itself, not decoration around it. Stories come after the method, not before it.

## 5. Carrier colour and the method
| # | Claim tested | Test | Status | Needs |
|---|---|---|---|---|
| K1 | Naming carrier colour reduces generalizations about groups, in any direction (Carey, 11 Oct) | People who practise naming carrier colour, against a matched group doing an equally engaging activity. Standard writing prompts weeks later; generalizations about groups coded by readers who do not know the condition; pre-registered. *Falsifier:* no difference in what people write | proposed | a study |
| K2 | Each principle of methods note 01 | The falsifier written under each principle | designed | readers |
| K4 | What holds across many AI models holds up under independent checks (Carey's cross-model method, 11 Oct) | From the working record, list the claims that held across models; check each against a proof, a primary source or a measurement; report how many failed. The owl story is one that failed | proposed | the working record |
| K3 | Carrier colour has one invariant across its working definitions | The candidate invariant and its falsifier (methods note 01, revision 1) | open | cases |

**Why K1 is designed this way** (checked 11 Oct):
- **Quick anti-bias exercises fade.** Every intervention tested in a large study worked at first; none was effective after a delay of several hours to several
  days (Lai et al. 2016, J. Experimental Psychology: General 145:1001-1016, doi:10.1037/xge0000179).
- **Behaviour barely moves.** Changing measured bias "generally produced trivial changes in behavior" (Forscher et al. 2019, J. Personality and Social
  Psychology 117:522-559, doi:10.1037/pspa0000160).
- **Long-term effects are mostly unknown.** About three-quarters of prejudice-reduction studies test light-touch interventions (Paluck et al. 2021, Annual
  Review of Psychology 72:533-560, doi:10.1146/annurev-psych-071620-030619).
- **Closest tested method:** prejudice habit-breaking: notice, name, replace (Devine et al. 2012, J. Experimental Social Psychology 48:1267-1278,
  doi:10.1016/j.jesp.2012.06.003).

## 6. Records and process
| # | Check | Status |
|---|---|---|
| E1 | The five checks on every published text, whoever wrote it | done for the 30 quotes; running |
| E2 | Nobody certifies their own work | running |
| E3 | Only sources actually read; identifiers verified; quotes at most 25 words | running. Open: re-download the Florentine Codex and Popol Vuh files with certificate checks on before publication |
| E4 | The failure-modes register | running (release plan §6) |

**Tests with people** (part 4, K1): each participant gives informed consent. To publish a result as research, the study first passes an ethics review
(an institutional review board or equivalent).

## 7. The ladder: the order to run the tests with people, and what each rung lets the project say
Added 15 October 2026, after Carey: "Can I prove measurable steps towards success? Then I don't mind." Each rung is a claim the public text states
only after the test beside it has passed; anything above the highest passed rung is labelled as proposed. Each rung needs only what the one below
produced. Today no rung has been run.

| rung | the claim it allows | the test | passes if |
|---|---|---|---|
| 1. Readable | someone other than its maker can read the code | the note's test 5, "teach it to someone": five minutes of teaching, then twenty prints, each left alone, flipped or turned at random; P10 adds timing per state | chance is 5 of 20; **9 or more right gives p < 0.05, and 11 or more p < 0.01**, for one person (binomial, computed) |
| 2. Learnable | it is kept | the same a week later, with no teaching in between; P1 and P5 compare semaphore, hands and paper | the same thresholds, a week later |
| 3. Agreed | the four sort real texts the same way for different readers | several readers classify the same texts; compare their agreement with chance, and each reader with the group (P8, P9) | agreement clearly above chance, and P9's predicted pattern under a single yes/no |
| 4. Helpful | practising the four improves thinking about thinking | P3: whether practice improves how well confidence tracks accuracy, measured with bias-free methods (Fleming & Lau 2014, doi:10.3389/fnhum.2014.00443), against a group that practises something else | a pre-registered difference, beyond chance |

Rungs 1 and 2 need one other person and some paper. Rung 4 needs a controlled study, consent and, to be published as research, an ethics review.
Why the order matters: a popular account of self-control, that it runs down like a muscle, was tested in 23 laboratories with 2,141 people under one
pre-registered protocol, and the effect was small, with a 95 % confidence interval that included zero (Hagger et al. 2016, doi:10.1177/1745691616652873).
Self-control itself is real and measurable: in 1,000 children followed to age 32, childhood self-control predicted health, wealth and criminal
offending, separately from intelligence and social class (Moffitt et al. 2011, doi:10.1073/pnas.1010076108). The ladder keeps the project's claims to
what it has measured.

## 8. The body and the exit
Added 22 October 2026. The public note states one hypothesis, untested: a move learned together with one of the four states can later serve
as a cue to stop and check, a way out of a line of thinking, and with practice it can shrink to a small gesture or a thought. This part sets
out how to test it and what is known for and against it. Testing it properly needs people who have not read the note, their consent and an
ethics review, and it needs funding the project does not have.

**One design rule for every test here.**
- The participants have not read the note. What people believe an experiment is looking for can shape what they do, and it varies with
  their previous experience (Orne 1962, doi:10.1037/h0043424).
- One group is shown a way to use the moves; another gets only the four states and the moves.
- A record is kept of what each person actually does with them, in their own words.

This measures whether showing people a way helps, hurts or narrows what they come up with. Across 53 studies with 166 comparisons, solving
a problem before instruction beat instruction first (Hedges' g 0.36, 95 % CI 0.20 to 0.51), but for younger learners (second to fifth grade)
and for domain-general skills the effects favoured instruction first (Sinha & Kapur 2021, doi:10.3102/00346543211019105). Naming the state
of one's own thinking may be a domain-general skill, so the order is itself a question to test.

| # | Claim tested | Test | Status | Needs |
|---|---|---|---|---|
| B1 | A state learned with the body is learned better | P1: the semaphore first, then the hands alone, then the symbol | proposed | people |
| B2 | A move learned with a state works as a cue to stop and check | Three groups learn the four states. One also learns a body move as its cue to stop and name its state; one makes a plan in words ("if I notice this, then I stop and name my state"); one is told to pause. Then each answers new questions that have a tempting wrong answer. Measure: how often each group stops and gets them right, and, with practice, whether the move shrinks to a small gesture. *Falsifier:* the move group does no better than the other two | proposed | people, consent, an ethics review |
| B3 | A move learned while moving helps later, sitting still | Learn the states while moving; a week later, answer seated in three conditions: make the move, picture the move, or neither. *Falsifier:* no difference between the three | proposed | people |
| B4 | The check holds under social pressure | After moving in step with a group and its leader, does a learned move still prompt a check before agreeing to a request? No request asks anything harmful of anyone | proposed | people, consent, an ethics review |

**What is known, for and against.**
- *Movement that is the lesson.* Preschool children who learned the planets with task-relevant physical activities learned the most, both
  straight after and six weeks later, and enjoyed it more than children taught in the usual sedentary way (Mavilidi, Okely, Chandler & Paas
  2017, doi:10.1002/acp.3325). Gesture and the imagined abacus: see P1.
- *Plans made in advance.* Across 94 independent tests, plans of the form "if situation Y is encountered, then I will do X" had a positive
  effect on reaching goals (Gollwitzer & Sheeran 2006, doi:10.1016/S0065-2601(06)38002-1). B2 compares a body move with such a plan.
- *The body changes its own state quickly.* Immersing the face in cold water regularly slows the heart (Malinowski et al. 2023,
  doi:10.3390/biology12060869); that is physiology, not thinking, and it is not proposed here as a practice. Walking raised the scores of 81 %
  of participants on a test of divergent thinking (many uses for one object) but of only 23 % on a test of convergent thinking (one right
  answer), and some of the boost remained after sitting down (Oppezzo & Schwartz 2014, doi:10.1037/a0036577).
- *Learned moving, used sitting still.* Divers' word lists learnt underwater were best recalled underwater, and lists learnt on land best on
  land (Godden & Baddeley 1975, doi:10.1111/j.2044-8295.1975.tb01468.x); a replication with sixteen divers did not find this (Murre 2021,
  doi:10.1098/rsos.200724). Across many studies, environmental context effects were reliable, and mentally reinstating the context at test
  reduced them (Smith & Vela 2001, doi:10.3758/BF03196157), which is why B3 includes picturing the move.
- *The body carries pressure too.* People who walked in step with a leader felt closer to him and were more willing to kill sow bugs at his
  request (Wiltermuth 2012, doi:10.1080/15534510.2012.658653). The hypothesis is that the same channel can carry a check instead; B4 tests it.
- *Ideas of this kind that failed.* A large repeat of power posing found no effect on hormones and risk tolerance (Ranehill et al. 2015,
  doi:10.1177/0956797614553946). A pre-registered repeat of an experiment in which prompting analytic thinking reduced religious belief found
  little to no effect (d = 0.07 in the wrong direction, N = 941; Sanchez et al. 2017, doi:10.1371/journal.pone.0172636).
- *Who it is for.* Self-determination theory proposes three innate psychological needs, competence, autonomy and relatedness (Ryan & Deci
  2000, doi:10.1037/0003-066X.55.1.68), and interest develops in phases, from an interest something triggers to one a person keeps (Hidi &
  Renninger 2006, doi:10.1207/s15326985ep4102_4). The note's tests serve all three: a reader checks it alone, passes a test, and does it with
  someone else.

Citations checked against Crossref and the claims against the papers' own abstracts, 22 October 2026.
