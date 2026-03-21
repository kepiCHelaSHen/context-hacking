# The Context Hacking Standard

## The Insight

LLMs don't read your specification. They generate from what they've seen before.

Ask any frontier model to implement a scientific algorithm without source code in
the prompt. It will confidently produce something that looks right — correct
structure, plausible variable names, reasonable logic. But the coefficients,
the execution order, the edge cases — those come from training data, not from
your spec. We measured it: **64% of coefficients drift to LLM priors** when the
frozen specification isn't in context.

The standard response is to fight this. Prompt harder. Add more instructions.
Hope the model follows them.

Context Hacking goes the other direction: **build systems that USE the weakness.**

If the model generates from priors, the divergence between what it generates
(prior) and what you specified (frozen spec) IS the error signal. The prior
becomes the detector. The weakness becomes the instrument.

That's the core insight. Everything else follows from it.

---

## The Protocol: 9 Layers

Each layer addresses a specific failure mode of LLM-assisted code generation.
Remove any one, and a gap opens that the others cannot cover.

### Layer 1 — Prior-as-Detector

**Failure mode:** LLM generates the textbook answer instead of your spec.

**How it works:** When the Critic sees output that matches the well-known version
of an algorithm instead of the frozen specification, it flags the divergence.
The model's tendency to generate from memory becomes a tripwire.

**Example:** Schelling tolerance=0.33 (the textbook 1/3) instead of 0.375
(the frozen spec). The LLM "knows" Schelling and generates its prior. The
Critic catches it because it knows what the prior looks like.

**Setup requirement:** The frozen spec must differ from the textbook version
in at least one measurable coefficient. If your spec IS the textbook, this
layer has nothing to detect.

### Layer 2 — Synthetic Dialectic

**Failure mode:** Builder confirms its own output (self-reinforcing bias).

**How it works:** Three roles with opposing goals:
- **Builder:** wants to finish (completion bias)
- **Critic:** wants to fail it (adversarial bias)
- **Reviewer:** doesn't care about either (neutral hygiene)

The system only converges when all three agree. The Builder can't self-approve.
The Critic can't build. The Reviewer can't have opinions about science.

**Setup requirement:** The Critic prompt must explicitly say "argue AGAINST
the science before scoring it." Without this instruction, the Critic degenerates
into a yes-man.

### Layer 3 — Frozen Code Forcing

**Failure mode:** LLM rewrites existing code from priors instead of composing
with it.

**How it works:** A published or validated codebase is declared immutable.
The `frozen/` directory cannot be modified by any agent. All new code must
work WITH the frozen code. Every coefficient must trace to a source file
and line number.

**Setup requirement:** You need an immutable reference — a published paper,
a validated implementation, a submitted specification. Without frozen code,
there's nothing to drift FROM.

### Layer 4 — Multi-Model Council

**Failure mode:** Single model has blind spots in its training data.

**How it works:** After each build turn, 2+ different LLMs review the work
against the same grounding documents. Different models have different training
priors. Disagreement between models signals an area where priors diverge —
exactly where drift is most dangerous.

**Protocol:**
- Both flag the same issue → must fix (consensus)
- One flags, other doesn't → use judgment
- Both flag DRIFT → stop everything, re-read CHAIN_PROMPT.md

**Setup requirement:** API keys for at least 2 providers. The council is
optional but significantly reduces single-model blind spots.

### Layer 5 — Context Window Management

**Failure mode:** Long sessions lose coherence (the model forgets earlier decisions).

**How it works:** Three external memory files that survive context resets:

- **state_vector.md** — 10-15 line "save game" written every N turns.
  Contains: turn number, mode, milestone, failures, winning parameters,
  metric status, next focus. After a context reset, this is the anchor.

- **innovation_log.md** — Append-only persistent memory. Every turn records
  what was built, what failed, critic scores, anomaly results, and what
  next turn should do. This IS the memory.

- **dead_ends.md** — Failed approaches with reasons. The system reads this
  BEFORE every build turn and cannot repeat logged failures.

**Setup requirement:** These files must exist in the project root. The loop
prompt must instruct the agent to read them before building.

### Layer 6 — Sigma-Gated Verification

**Failure mode:** Code works on one lucky seed but fails on others.

**How it works:** Every build runs the simulation across N seeds (default 3).
Configurable thresholds check bounds (metric > X) and variance (std < 0.15).
Nothing merges on vibes.

**Gate types:**
- **Bound check:** every seed must pass every threshold
- **Variance check:** std across seeds must be below sigma threshold
- **Trend check:** no metric monotonically worsening across 3 turns

**Setup requirement:** You need a simulation or test that can run with
different random seeds. The output must have at least one measurable metric.
Define thresholds in config.yaml.

### Layer 7 — Two-Mode Negative Feedback

**Failure mode:** Loop gets stuck (stagnation) or goes wild (chaos).

**How it works:** Two modes with automatic switching:

- **VALIDATION** (default): strict, citation-required, critic blocks.
  Use for known mechanisms and calibration.
- **EXPLORATION** (when stuck): hypothesis-driven, critic advisory,
  reversion protocol active. Use for novel approaches.

Automatic switching prevents both problems:
- No improvement for N turns → forced into Exploration
- Exploration anomaly → automatic Reversion to last passing tag
- K Exploration turns with no improvement → EXIT (wait for human)

**Setup requirement:** The loop prompt must check mode before each turn
and apply the appropriate rigor level.

### Layer 8 — Token-Efficient Architecture

**Failure mode:** Multi-agent workflows burn tokens wastefully.

**How it works:**
- Subagents get targeted prompts (the Builder gets "build X," not "here's
  the whole project")
- Health checks are 3 lines (verify role, proceed or re-invoke)
- One master document (CHAIN_PROMPT.md) is the single source of truth
- Partial results save incrementally (crash recovery)
- State vector compression prevents redundant context re-reading

**Setup requirement:** CHAIN_PROMPT.md must be comprehensive enough that
reading it once gives full context. If agents need to read 10 files to
understand the project, the architecture is wrong.

### Layer 9 — Self-Correcting Loop

**Failure mode:** Errors compound across turns without detection.

**How it works:** The loop iterates: build → critique → fix → verify →
commit → repeat. Five kill-switches halt automatically:

1. **Science complete** — all criteria met
2. **Performance gate** — no improvement for N turns
3. **Unresolvable anomaly** — K consecutive failures
4. **Fundamental misalignment** — critic says root is broken
5. **Human stop** — STOP file exists

**Setup requirement:** Define exit criteria BEFORE starting the loop.
What does "done" look like? What metrics must be in what ranges?

---

## How to Set Up a Successful CHP Project

### Step 1: Choose the right problem

Good CHP projects have:
- **Measurable outputs** (not just "write a web app" — you need metrics)
- **A frozen reference** (paper, spec, validated implementation to ground against)
- **Known LLM priors** (the textbook version differs from your spec)
- **Multi-seed testability** (run it 30 times, check variance)

Bad CHP projects:
- Pure creative work (no ground truth to drift from)
- One-off scripts (no iteration, no metrics)
- Projects where the textbook answer IS the right answer

### Step 2: Write the frozen spec

Put your immutable specification in `frozen/`. Include:
- Exact coefficient values (with notes on what LLMs commonly generate wrong)
- Execution order requirements (simultaneous vs sequential, etc.)
- Architecture rules (no print, seeded rng, no circular imports)
- Expected outputs at known inputs

The frozen spec should be detailed enough that ANY competent programmer
(human or AI) could implement it correctly by reading only this document.

### Step 3: Pre-load dead ends

If you know common mistakes for this domain, log them in `dead_ends.md`
BEFORE starting the loop. This prevents the Builder from discovering
mistakes you already know about.

Format:
```
## DEAD END N — [title]
**What was attempted:** [what went wrong]
**Why this is a dead end:** [why it can't work]
**Do NOT repeat:** [specific thing to avoid]
```

### Step 4: Define sigma-gates

In `config.yaml`, define your anomaly checks:
```yaml
gates:
  seeds: 3
  sigma_threshold: 0.15
  anomaly_checks:
    - metric: "primary_output"
      operator: ">"
      threshold: 0.50
```

Ask: "What would a wrong implementation produce?" Then set a threshold
that catches it. The Schelling experiment uses segregation < 0.80 to catch
the textbook result when dynamic tolerance should produce partial mixing.

### Step 5: Write the expected false positive

In `spec.md`, describe the false positive you expect the Builder to hit.
This is the Prior-as-Detector moment — the point where the LLM generates
from training priors instead of from the frozen spec.

Every good CHP experiment has one. If yours doesn't, either:
- Your spec IS the textbook (Layer 1 won't activate)
- Your problem doesn't have strong LLM priors (try a different domain)
- You haven't thought hard enough about where drift will happen

### Step 6: Run the loop

```
/chp-init     → creates project structure
/chp-run      → Turn 1: first milestone
/chp-run      → Turn 2: next milestone (false positive may appear here)
/chp-critic   → extra review if needed
/chp-gates    → multi-seed verification
/chp-status   → check progress
```

Each turn: read dead ends → build one milestone → critique → test → log.
The loop converges when all milestones are complete and all gates pass.

---

## What Makes CHP Different

| Approach | What it does | What it misses |
|----------|-------------|---------------|
| "Just prompt better" | Better instructions | No verification, no memory |
| RAG | Puts docs in context | No adversarial review, no statistical testing |
| Chain-of-thought | Step-by-step reasoning | No external critique, no multi-seed gates |
| DSPy | Optimizes prompts | No frozen spec, no false positive detection |
| Reflexion | Self-reflection | Single model, no multi-model disagreement |
| **CHP** | All of the above + adversarial dialectic + sigma-gates + dead end memory + mode switching | Requires measurable outputs and a frozen reference |

CHP is not one trick. It's a stack where each layer covers what the others miss.

---

## The Standard in One Sentence

**Don't fight what LLMs are bad at. Build systems that use it.**
