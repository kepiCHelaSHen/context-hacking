# Context Hacking Protocol (CHP)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/context-hacking.svg)](https://pypi.org/project/context-hacking/)

**A 9-layer anti-drift framework for trustworthy LLM-assisted scientific code generation.**

LLMs get scientific code wrong 99% of the time. We measured it (95/96 coefficients incorrect, Fisher's exact p = 4x10^-10). Then we built a system that turns that weakness into a feature.

```bash
pip install context-hacking
chp init my-project
chp run
```

---

## The Origin Story

We pointed an autonomous AI loop at a 30-year debate in evolutionary biology: does war make humans cooperative (Bowles 2006) or do institutions (North 1990)?

The loop built 7,663 lines of simulation code. Ran 100 experiments. Got a positive result at n=3 seeds — the Bowles mechanism appeared to be causally operative (interaction effect +0.039).

**Then the loop's own Critic said: "Replicate it."**

At n=10 seeds the effect vanished. p = 0.954. It was a false positive.

The loop logged it as a dead end. Scaled up to 20 competing tribes. Found the real answer: institutions win, p < 0.0001, Cohen's d = -5.97, 6/6 seeds consistent.

**The false positive wasn't a failure. It was the system working correctly.**

Error → Detection → Correction → Stronger result. That sequence — fully documented in a git log — is what CHP produces.

---

## The 9 Layers

### Layer 1: Prior-as-Detector

LLMs generate from training priors, not from your specification. CHP exploits this: when the Builder's output matches the "textbook answer" instead of your frozen source code, the Critic flags it as drift.

The model's tendency to hallucinate becomes a tripwire.

### Layer 2: Synthetic Dialectic

Three agents with deliberately opposing goals:

| Agent | Role | Mindset |
|-------|------|---------|
| **Builder** | Implement exactly what's specified | "Read the constitution before every build" |
| **Critic** | Prove the science is wrong | "Assume the build failed until proven otherwise" |
| **Reviewer** | Code hygiene only | "No opinions about science or architecture" |

The system only converges when all three agree. Tension is the feature, not the bug.

### Layer 3: Frozen Code Forcing

A published or submitted codebase is declared immutable. No agent can modify it. All new code must compose WITH the frozen code. Every coefficient traces to a source file and line number.

This forces generation to ground against actual source, not the model's prior beliefs about what the code should look like.

### Layer 4: Multi-Model Council

After every build turn, multiple LLMs (configurable: GPT-4o, Grok, Gemini, Claude) review the work against the same grounding documents. Different models have different training priors.

- Both flag the same issue → must fix (consensus)
- One flags, other doesn't → use judgment
- Both flag DRIFT → halt and re-read the master spec

Disagreement between models IS the drift signal.

### Layer 5: Context Window Management

Long AI sessions collapse. CHP manages context as a resource:

- **State Vector**: Every N turns, the system writes a 10-15 line "save game" — turn number, milestone, mode, failures, winning parameters, metric status, next focus.
- **Innovation Log**: Persistent external memory that survives context resets. Every turn appends: what was built, what failed, critic scores, anomaly results, metric deltas.
- **Dead End Tracking**: Failed approaches are logged with what was tried, why it failed, and why it's a dead end. The system reads this before every build — it cannot repeat logged failures.

### Layer 6: σ-Gated Statistical Verification

Nothing merges on vibes. Every build runs multi-seed anomaly checks:

```yaml
anomaly_checks:
  cooperation: "> 0.25"
  aggression: "< 0.70"
  population: "> 0"
  cooperation_std: "< 0.15"
  aggression_std: "< 0.15"
```

Configurable per project. Fail any check → blocked. Fail three consecutive turns → EXIT (halt and wait for human).

The convergence battery extends this: N milestones x M seeds, all primary metrics must have σ below threshold.

### Layer 7: Two Modes with Negative Feedback

**Validation Mode** (default): Full literature grounding. Critic is a hard blocker. Council runs before build.

**Exploration Mode** (when stuck): Hypothesis-driven. Critic is advisory. Reversion protocol active — if anomaly check fails, `git checkout` to last passing tag. No patching broken exploration code.

Automatic switching:
- No improvement for N turns → forced Exploration
- Exploration fails anomaly → automatic Reversion
- K Exploration turns with no improvement → EXIT

The system oscillates between rigor and creativity with automatic damping.

### Layer 8: Token-Efficient Architecture

Multi-agent workflows burn tokens (4-7x single session). CHP minimizes waste:

- Subagents get targeted prompts, not full project context
- Health checks are 3 lines (verify role, proceed or re-invoke)
- One master document (CHAIN_PROMPT.md) is the single source of truth
- Partial results save incrementally (crash recovery)
- State vector compression prevents context re-reading

### Layer 9: Self-Correcting Loop

The system iterates: build → critique → fix → verify → commit → repeat.

Exit conditions halt the loop automatically:
1. **Science complete** — all criteria in the findings doc are met
2. **Performance gate** — no metric improvement across N turns
3. **Unresolvable anomaly** — multi-seed anomaly on K consecutive turns
4. **Fundamental misalignment** — critic says the root is broken
5. **Human stop** — STOP file exists in project directory

The loop doesn't just execute. It makes scientific judgments: "this needs replication," "n=4 is too small," "this dead end shouldn't be repeated."

---

## Quick Start

### Install

```bash
pip install context-hacking
```

### Initialize a project

```bash
chp init my-research-project
cd my-research-project
```

This creates:

```
my-research-project/
├── config.yaml              # CHP configuration (all 9 layers tunable)
├── CHAIN_PROMPT.md           # Master design doc (your single source of truth)
├── innovation_log.md         # Persistent memory across turns
├── dead_ends.md              # Failed approaches (never repeated)
├── state_vector.md           # Context reset anchor
├── frozen/                   # Immutable published code goes here
├── prompts/                  # Agent prompt templates
│   ├── builder.md
│   ├── critic.md
│   ├── reviewer.md
│   ├── council_gpt.md
│   ├── council_grok.md
│   └── health_check.md
└── .chp/                     # Runtime state (gitignored)
```

### Configure

Edit `config.yaml`:

```yaml
project:
  name: "my-research-project"
  description: "What this project does"
  frozen_paths: ["src/v1/"]

models:
  builder: "claude-sonnet-4-20250514"
  critic: "claude-sonnet-4-20250514"
  reviewer: "claude-sonnet-4-20250514"
  council:
    - provider: "openai"
      model: "gpt-4o"
    - provider: "xai"
      model: "grok-3"

gates:
  anomaly_checks:
    - metric: "accuracy"
      operator: ">"
      threshold: 0.80
    - metric: "loss_std"
      operator: "<"
      threshold: 0.10
  seeds: 3
  convergence_seeds: 30
  sigma_threshold: 0.15

loop:
  max_turns: 50
  validation_to_exploration_threshold: 5  # turns without improvement
  max_consecutive_exploration: 3
  context_reset_interval: 15
  state_vector_interval: 5

exit_conditions:
  science_complete: true
  performance_gate: true
  unresolvable_anomaly: true
  fundamental_misalignment: true
  human_stop: true
```

### Run the loop

```bash
chp run
```

### Check status

```bash
chp status
```

```
CHP Status: my-research-project
  Turn:       7 / 50
  Mode:       VALIDATION
  Last gate:  PASS (3/3 seeds)
  Streak:     2 turns without improvement
  Dead ends:  1 logged
  Next focus: "Increase band count to n=20"
```

---

## How It Was Proven

CHP was developed and validated on [SIMSIV](https://github.com/kepiCHelaSHen/SIMSIV) — a calibrated agent-based simulation of human social evolution (35 heritable traits, 9 engines, 187 tests, calibrated against Hadza/!Kung/Ache ethnographic data).

| Metric | Without CHP | With CHP |
|--------|------------|---------|
| Coefficient accuracy | 1% (1/96) | 100% (96/96) |
| False positives caught | 0 | 1 (Exp 2 n=3, p=0.954 at n=10) |
| Code bugs found by review | 0 | 6 (migration routing, death year, law_strength read, ...) |
| Final result significance | — | p < 0.0001, d = -5.97 |

The full development history — every turn, every false positive, every correction — is in the [SIMSIV git log](https://github.com/kepiCHelaSHen/SIMSIV).

---

## Drift Experiment

**"LLMs Generate from Priors, Not Specifications"**

We measured specification drift across GPT-4o, Grok-3, and Claude on SIMSIV implementation tasks:

- Without source code in prompt: **99% incorrect** (95/96, Fisher's exact p = 4x10^-10)
- With CHP Builder/Critic/Reviewer protocol: **0% drift**

Full paper: [SIMSIV v2 Working Paper](https://github.com/kepiCHelaSHen/SIMSIV/blob/main/docs/SIMSIV_V2_White_Paper.md)

---

## Integration

### Cursor / Claude Code

```bash
chp init my-project --cursor
```

Generates `.cursorrules` and a `skills/` folder that auto-inject the Critic, gates, and mode logic into your Cursor or Claude Code sessions.

### Existing Projects

```bash
cd my-existing-project
chp init . --existing
```

CHP wraps around your existing codebase. Point `frozen_paths` at your stable code. New development runs through the protocol.

---

## API

```python
from context_hacking import Orchestrator, Config

config = Config.from_yaml("config.yaml")
loop = Orchestrator(config)

# Run the full loop
loop.run()

# Or step through manually
loop.step()  # one turn
print(loop.status())
```

---

## Philosophy

**Don't fight what LLMs are bad at. Build systems that use it.**

LLMs hallucinate. That's not a bug to patch — it's a signal to exploit. When an LLM generates from priors instead of from your source code, the divergence between prior and source IS the drift detector.

CHP doesn't make LLMs smarter. It makes their failures visible, measurable, and automatically correctable.

---

## License

MIT. Use it. Break it. Ship science with it.

---

## Citation

```bibtex
@software{rice2026chp,
  author = {Rice, James},
  title = {Context Hacking Protocol: A 9-Layer Anti-Drift Framework for LLM-Assisted Scientific Code Generation},
  year = {2026},
  url = {https://github.com/kepiCHelaSHen/context-hacking}
}
```
