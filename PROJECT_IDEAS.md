# 10 CHP Project Ideas — Ready to Vibe Code

Each project has: a frozen reference, measurable outputs, known LLM priors
that will drift, and a predictable false positive the Critic will catch.

---

## 1. Stock Trading Backtester

**What:** Build a backtesting engine for a specific published trading strategy
(e.g., Fama-French 3-factor model) and test it against real historical data.

**Frozen spec:** The exact Fama-French factors (SMB, HML, market premium)
with published coefficients from the original 1993 paper.

**LLM prior to catch:** LLMs generate "moving average crossover" strategies
when asked for "trading strategy." The Critic catches: "This is a momentum
strategy, not a factor model."

**False positive:** Backtester shows 15% annual returns — but it has
look-ahead bias (using future data in position sizing). The Critic catches
it via walk-forward validation.

**sigma-gates:** Sharpe ratio in [0.3, 1.5], max drawdown < 30%, no
look-ahead bias (walk-forward vs full-period returns must differ < 5%).

---

## 2. Protein Folding Energy Calculator

**What:** Implement a Lennard-Jones potential energy calculator for protein
backbone atoms, validated against published benchmark energies.

**Frozen spec:** The AMBER force field parameters (bond lengths, angles,
dihedral coefficients) from the published ff14SB parameter set.

**LLM prior to catch:** LLMs generate the generic 12-6 Lennard-Jones
potential with epsilon=1, sigma=1 (dimensionless units). The frozen spec
uses AMBER's atom-type-specific parameters (epsilon varies by residue).

**False positive:** Energy minimization converges to a local minimum that
looks stable but has the wrong chirality. The 30-seed test catches it:
different initial conformations should converge to the same global minimum.

**sigma-gates:** Total energy within 5% of published benchmark, RMSD < 2.0 A
from crystal structure, chirality correct on all residues.

---

## 3. Music Theory Harmony Analyzer

**What:** Build a chord progression analyzer that identifies functional
harmony (per Kostka & Payne "Tonal Harmony") and detects voice leading errors.

**Frozen spec:** The exact rules from Kostka & Payne Chapter 6: parallel
fifths forbidden, resolution of 7ths downward by step, doubling rules for
each inversion, acceptable cadence types.

**LLM prior to catch:** LLMs generate jazz harmony rules (ii-V-I, tritone
substitution) when asked for "harmony analysis." Classical tonal harmony
has DIFFERENT rules. The Critic catches jazz contamination.

**False positive:** Analyzer accepts parallel fifths between inner voices
because LLMs learned from jazz (where parallel fifths are acceptable).
The frozen spec says: parallel fifths forbidden in ALL voice pairs.

**sigma-gates:** Error detection rate > 95% on published exercise sets,
false positive rate < 5%, all cadence types correctly identified.

---

## 4. Compiler Optimizer (Peephole)

**What:** Build a peephole optimizer for a simple instruction set that
implements the exact optimization rules from a published textbook
(Aho, Sethi, Ullman "Dragon Book" Chapter 9).

**Frozen spec:** The 12 specific peephole patterns from Dragon Book Table 9.1
(redundant load elimination, strength reduction, dead code removal, etc.).

**LLM prior to catch:** LLMs generate LLVM-style optimization passes when
asked for "compiler optimization." The Dragon Book patterns are simpler and
more specific. The Critic catches LLVM contamination.

**False positive:** Optimizer "improves" code by reordering instructions
that have side effects. The Dragon Book rules explicitly preserve side-effect
ordering. The Critic checks: "Did the optimization change observable behavior?"

**sigma-gates:** All 12 patterns correctly applied on test suite, no
false optimizations (observable behavior unchanged), compilation time < 2x.

---

## 5. Cryptographic Hash Implementation

**What:** Implement SHA-256 from the FIPS 180-4 specification, byte-for-byte
correct against the published test vectors.

**Frozen spec:** FIPS 180-4 Section 6.2: exact initial hash values (H0-H7),
exact round constants (K0-K63), exact sigma/Sigma rotation amounts, exact
message schedule formula.

**LLM prior to catch:** LLMs generate SHA-256 from memory and get the round
constants or initial hash values wrong (off by one bit). Every constant must
match FIPS 180-4 exactly — one wrong bit = completely different hash.

**False positive:** Implementation produces correct hashes for short inputs
but fails on inputs > 55 bytes (the padding boundary). The multi-length
test battery catches it.

**sigma-gates:** 100% match on all NIST test vectors (no tolerance — crypto
is exact), padding correct at all boundary lengths, performance within 2x
of reference implementation.

---

## 6. Climate Model (Energy Balance)

**What:** Build a zero-dimensional energy balance model calibrated against
the published IPCC AR6 equilibrium climate sensitivity range.

**Frozen spec:** Stefan-Boltzmann constant (exact), solar constant 1361 W/m2
(SORCE measurement), albedo 0.30 (CERES satellite), CO2 forcing coefficient
5.35 ln(C/C0) per Myhre et al. (1998).

**LLM prior to catch:** LLMs generate the simple Stefan-Boltzmann model
with blackbody temperature (255K). The frozen spec includes the greenhouse
effect, water vapor feedback, and ice-albedo feedback. Without feedbacks,
ECS = 1.1K. With feedbacks: ECS = 2.5-4.0K (IPCC range).

**False positive:** Model produces ECS = 1.1K (no feedback — the textbook
blackbody result). The Critic catches: "This matches the no-feedback prior,
not the spec that includes feedbacks."

**sigma-gates:** ECS in [2.0, 5.0]K (IPCC AR6 likely range), transient
response in [1.0, 2.5]K, equilibrium reached within 1000 years.

---

## 7. Natural Language Parser (CFG)

**What:** Build a CYK parser for a specific context-free grammar published
in a textbook (Jurafsky & Martin Chapter 14), tested on the Penn Treebank.

**Frozen spec:** The exact grammar rules from J&M Figure 14.1 (the toy
grammar), extended with the 20 most common Penn Treebank rules.

**LLM prior to catch:** LLMs generate recursive descent parsers (top-down)
when asked for "parser." CYK is bottom-up dynamic programming. The algorithms
produce different parse trees for ambiguous sentences. The Critic catches:
"This is top-down, not CYK."

**False positive:** Parser correctly handles unambiguous sentences but
produces the WRONG parse for "I saw the man with the telescope" (PP
attachment ambiguity). The CYK chart should contain BOTH parses. If only
one: the parser is wrong.

**sigma-gates:** Precision > 0.85, recall > 0.85 on test set, all ambiguous
sentences produce multiple parses, no crashes on 1000-sentence battery.

---

## 8. Robotics PID Controller

**What:** Implement a PID controller with Ziegler-Nichols tuning, tested
on a simulated inverted pendulum with exact physical parameters.

**Frozen spec:** Ziegler-Nichols ultimate gain method: Kp = 0.6*Ku,
Ki = 2*Kp/Tu, Kd = Kp*Tu/8. Pendulum: mass 1.0 kg, length 0.5 m,
gravity 9.81 m/s2, friction 0.1 Ns/m.

**LLM prior to catch:** LLMs generate generic PID with Kp=1, Ki=0.1, Kd=0.01
(arbitrary defaults). The Ziegler-Nichols values are SPECIFIC to the plant
(pendulum parameters). The Critic catches: "These gains aren't from Z-N tuning."

**False positive:** Controller stabilizes the pendulum but oscillates
continuously (steady-state error > 5%). The Z-N tuning should produce
damped oscillation converging to < 1% error. The Critic checks the
settling time and overshoot.

**sigma-gates:** Settling time < 5s, overshoot < 20%, steady-state error < 2%,
no instability across 30 initial conditions, std < 0.15.

---

## 9. Recommendation Engine (Collaborative Filtering)

**What:** Implement matrix factorization (SVD++) for movie recommendations,
validated against the published Netflix Prize benchmark.

**Frozen spec:** SVD++ formulation from Koren (2008) "Factorization meets
the neighborhood." Exact regularization lambda=0.02, learning rate=0.007,
latent factors k=100, implicit feedback terms included.

**LLM prior to catch:** LLMs generate basic SVD (no implicit feedback) when
asked for "collaborative filtering." SVD++ includes implicit feedback terms
that improve RMSE by ~2%. The Critic catches: "Where are the implicit terms?"

**False positive:** RMSE = 0.89 on test set — looks good, but the model is
overfit (RMSE on training = 0.60). The 5-fold cross-validation gate catches
the overfitting: train-test gap must be < 0.05.

**sigma-gates:** Test RMSE < 0.92, train-test gap < 0.05, convergence
within 50 epochs, std across folds < 0.02.

---

## 10. Game AI (Minimax with Alpha-Beta)

**What:** Implement minimax search with alpha-beta pruning for chess endgames,
validated against published Lomonosov tablebases (perfect play).

**Frozen spec:** Standard minimax with alpha-beta from Russell & Norvig
Chapter 5. Evaluation function: material counting with standard piece values
(P=1, N=3, B=3, R=5, Q=9). Search depth: 6 ply minimum.

**LLM prior to catch:** LLMs generate Monte Carlo Tree Search (MCTS) when
asked for "game AI" because AlphaGo made MCTS famous. Minimax and MCTS
produce different move choices in the same position. The Critic catches:
"This is MCTS, not minimax."

**False positive:** AI plays reasonable moves but misses a forced mate-in-3
that minimax at depth 6 should find. The Lomonosov tablebase test battery
checks: all positions with known perfect play must match the tablebase move.

**sigma-gates:** 100% match on tablebase positions (depth 6), alpha-beta
prunes > 50% of nodes (vs no pruning), no illegal moves, endgame conversion
rate > 90%.

---

## Choosing Your First Project

| If you want... | Try... | Time estimate |
|----------------|--------|---------------|
| Quick win, impressive demo | #5 (SHA-256) — exact verification | 2-3 hours |
| Real science | #6 (Climate model) — IPCC validation | 1 day |
| Practical tool | #9 (Recommendation engine) — Netflix data | 1 day |
| Fun to watch | #8 (PID controller) — pendulum animation | 3-4 hours |
| Most LLM-prior-catching | #3 (Music theory) — jazz vs classical | 4-5 hours |
| Hardest challenge | #10 (Game AI) — tablebase verification | 2 days |

Pick one. Type `/chp-init`. Start building.
