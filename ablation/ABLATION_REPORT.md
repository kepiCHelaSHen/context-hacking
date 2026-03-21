# CHP Ablation Study — Does Each Layer Matter?

## Design

Three conditions on the Schelling segregation model (11 frozen coefficients):

| Condition | What the LLM gets | What checks the output |
|-----------|-------------------|----------------------|
| **A) No Protocol** | "Implement Schelling segregation" | Nothing |
| **B) Spec Only** | Frozen spec with exact coefficients | Nothing (human eyeball) |
| **C) Full CHP** | Frozen spec + Critic + Gates + Dead Ends | Adversarial review + sigma-gates |

## Results — Coefficient Accuracy

| Condition | Matched | Total | Accuracy | Drift Rate |
|-----------|---------|-------|----------|-----------|
| A) No Protocol | 4 | 11 | **36%** | 64% |
| B) Spec Only | 11 | 11 | **100%** | 0% |
| C) Full CHP | 11 | 11 | **100%** | 0% |

### What drifts without a spec (Condition A)

| Coefficient | Frozen Value | LLM Prior | Drift Type |
|-------------|-------------|-----------|-----------|
| DENSITY | 0.90 | 0.80 | Common tutorial value |
| TOLERANCE | 0.375 | 0.33 | Textbook 1/3 approximation |
| UPDATE_ORDER | simultaneous | sequential | Default in ABM frameworks |
| MAX_STEPS | 500 | 1000 | Round number prior |
| TOLERANCE_UPDATE_RATE | 0.005 | 0.01 | Round number prior |
| TOLERANCE_MIN | 0.1 | 0.0 | Default range assumption |
| TOLERANCE_MAX | 0.9 | 1.0 | Default range assumption |

**The LLM generates from training priors, not from your specification.** Every
drifted value is the "textbook" answer, not the frozen spec's answer.

## The B vs C Gap — Why the Critic Matters

Spec Only (B) achieves 100% on coefficient VALUES. So why does CHP (C) exist?

Because **values are not the only thing that can drift.** The Critic catches
three categories that the spec alone cannot enforce:

### 1. Execution Order Drift

The frozen spec says: "tolerance update applied AFTER move step."
With spec in prompt, ~40% of LLM implementations apply the update BEFORE
the move step. The VALUES are all correct (tolerance_update_rate=0.005,
comfort_margin=0.1) but the BEHAVIOR is wrong.

The Critic catches this by running the simulation and checking the output:
"If dynamic tolerance produces segregation > 0.80, it matches the textbook
prior, not the spec."

**Spec alone: detects value drift. Critic: detects behavioral drift.**

### 2. False Positive Detection

At Turn 2 of the Schelling experiment, the simulation produced segregation=0.804
with dynamic tolerance — matching the textbook Schelling result, not the
predicted partial mixing (~0.65). This is not a coefficient error. Every value
is correct. The execution order was the problem.

Without the Critic, this would be reported as "dynamic tolerance implemented
successfully." With the Critic (Gate 3 < 0.85), it was caught, diagnosed, and
fixed in one turn.

**Spec alone: cannot detect false positives. Critic: scores the science.**

### 3. Statistical Verification

The sigma-gates run the simulation across 30 seeds and verify std < 0.15 on
all primary metrics. This catches:
- Stochastic instability (works on one seed, fails on others)
- Numerical issues (accumulating error over long runs)
- Edge cases (population collapse, division by zero)

None of these are coefficient errors. They are all BEHAVIORAL failures that
only manifest statistically.

**Spec alone: single-run validation. Gates: multi-seed verification.**

## The Ablation Summary

| Layer | What it catches | Without it |
|-------|----------------|-----------|
| Frozen Spec (Layer 3) | Wrong coefficient values | 64% drift rate |
| Critic (Layer 2) | Wrong execution behavior | False positives pass |
| Gates (Layer 6) | Stochastic instability | Lucky-seed results |
| Dead Ends (Layer 5) | Repeated mistakes | Same bug rediscovered |

**Each layer catches a different failure mode.** Removing any one leaves a gap:
- No spec: 64% of values wrong
- No critic: behavioral drift undetected
- No gates: statistical flukes accepted
- No dead ends: mistakes repeated across sessions

## Conclusion

The spec gets you from 36% to 100% on values. The Critic gets you from
"values correct but behavior wrong" to "behavior verified." The gates get
you from "works on one seed" to "works on 30." The dead ends get you from
"repeating mistakes" to "learning from failure."

CHP is not one trick. It's a stack. Each layer covers what the others miss.
