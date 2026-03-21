# Context Hacking Protocol (CHP)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/context-hacking.svg)](https://pypi.org/project/context-hacking/)

**A 9-layer anti-drift framework for trustworthy LLM-assisted scientific code generation.**

LLMs get scientific code wrong 99% of the time. We measured it (95/96 coefficients
incorrect across GPT-4o, Grok-3, and Claude; Fisher's exact p = 4x10^-10). Then we
built a system that turns that weakness into a feature.

```bash
pip install context-hacking
chp init my-project
chp run
```

---

## Why This Exists

We pointed an autonomous AI loop at a 30-year debate in evolutionary biology: does
war make humans cooperative (Bowles 2006) or do institutions (North 1990)?

The loop built 7,663 lines of simulation code. Ran 100 experiments. Got a positive
result at n=3 seeds — the Bowles mechanism appeared causally operative (+0.039).

**Then the loop's own Critic said: "Replicate it."**

At n=10 the effect vanished. p = 0.954. False positive.

The loop logged the dead end. Scaled to 20 competing tribes. Found the real answer:
institutions win, p < 0.0001, Cohen's d = -5.97, 6/6 seeds.

**The false positive wasn't a failure. It was the system working correctly.**

CHP is that system, extracted into a pip-installable framework.

Full proof: [SIMSIV repository](https://github.com/kepiCHelaSHen/SIMSIV)

---

## The 9 Layers

| # | Layer | Core Idea |
|---|-------|-----------|
| 1 | **Prior-as-Detector** | LLM hallucination becomes a drift tripwire |
| 2 | **Synthetic Dialectic** | Builder/Critic/Reviewer with opposing goals |
| 3 | **Frozen Code Forcing** | Immutable published code grounds all generation |
| 4 | **Multi-Model Council** | Different LLM priors = disagreement = drift signal |
| 5 | **Context Window Management** | State vectors, innovation logs, dead-end tracking |
| 6 | **sigma-Gated Verification** | Multi-seed statistical gates block noisy code |
| 7 | **Two-Mode Negative Feedback** | Validation/Exploration with automatic switching |
| 8 | **Token-Efficient Architecture** | Targeted prompts, incremental saves, health checks |
| 9 | **Self-Correcting Loop** | Build, critique, fix, verify, commit, repeat |

### Layer 1: Prior-as-Detector

LLMs generate from training priors, not your specification. CHP exploits this: when
the Builder's output matches the "textbook answer" instead of your frozen source code,
the Critic flags it. The model's tendency to hallucinate becomes the detection mechanism.

### Layer 2: Synthetic Dialectic

Three agents with deliberately opposing goals:

| Agent | Goal | Mindset |
|-------|------|---------|
| **Builder** | Implement exactly what's specified | "Read the constitution before every build" |
| **Critic** | Prove the science is wrong | "Argue AGAINST the finding, then score it" |
| **Reviewer** | Code hygiene only | "No opinions about science or architecture" |

The system only converges when all three agree. Tension is the feature.

### Layer 3: Frozen Code Forcing

A published or submitted codebase is declared immutable. No agent can modify it. All
new code must compose WITH the frozen code. Every coefficient traces to a source file
and line number.

### Layer 4: Multi-Model Council

After every build turn, multiple LLMs review the work against the same grounding
documents. Different models have different priors. Disagreement IS the drift signal.

Configurable providers: OpenAI (GPT-4o), xAI (Grok-3), Google (Gemini), Anthropic (Claude).

### Layer 5: Context Window Management

- **State Vector**: Every N turns, a 10-15 line "save game" captures the full system state.
- **Innovation Log**: Persistent memory that survives context resets.
- **Dead End Tracking**: Failed approaches logged with reasons. The system reads this
  before every build and cannot repeat logged failures.

### Layer 6: sigma-Gated Statistical Verification

Nothing merges on vibes. Every build runs multi-seed anomaly checks with configurable
thresholds. Fail any check: blocked. Fail K consecutive turns: EXIT.

### Layer 7: Two Modes with Negative Feedback

**Validation** (default): strict, citation-required, critic blocks.
**Exploration** (when stuck): hypothesis-driven, critic advisory, reversion protocol active.

Automatic switching prevents both stagnation and chaos.

### Layer 8: Token-Efficient Architecture

Targeted subagent prompts. 3-line health checks. Single source of truth document.
Incremental saves. Context compression via state vectors.

### Layer 9: Self-Correcting Loop

Five kill-switches halt the loop automatically:
1. Science complete
2. Performance gate (no improvement for N turns)
3. Unresolvable anomaly (K consecutive failures)
4. Fundamental misalignment (critic says root is broken)
5. Human stop (STOP file)

---

## Built-in Showcase Experiments

CHP ships with **9 experiments** across 5 domains, each fully wired with frozen specs,
sigma-gates, and pre-loaded false-positive stories demonstrating the protocol in action.

| # | Experiment | Domain | Prior-as-Detector Catches |
|---|-----------|--------|--------------------------|
| 1 | Schelling Segregation | Social science | tolerance=0.33 drift, sequential update |
| 2 | Spatial Prisoner's Dilemma | Game theory | T/R/P/S payoff, async update, missing self |
| 3 | Lotka-Volterra | Ecology | ODE difference equations, alpha/beta variables |
| 4 | SIR Epidemic | Epidemiology | Rate equations dS/dt, float I(t), zero fadeout |
| 5 | ML Hyperparameter Search | Machine learning | Grid search instead of Bayesian, accuracy inflation |
| 6 | Lorenz Attractor | Chaos theory | Wrong sigma/rho/beta constants, fixed-step RK4 |
| 7 | Grover's Algorithm | Quantum computing | Classical brute-force, wrong oracle sign, missing diffusion |
| 8 | Izhikevich Neurons | Neuroscience | Hodgkin-Huxley contamination, wrong a/b/c/d constants |
| 9 | Blockchain Consensus | Distributed systems | Centralized leader instead of Byzantine fault tolerance |

### 1. Schelling Segregation (the star demo)

The 1971 Schelling model of spatial segregation + a 2025 dynamic-tolerance extension.

**Why this is perfect for CHP**: Every LLM has seen the Schelling model in training.
Ask any frontier model to implement it without source code and it will generate a
"textbook" version with standard thresholds (tolerance = 0.375, 8-cell Moore
neighborhood). The Prior-as-Detector layer catches this immediately — if the
Builder produces the textbook version instead of YOUR frozen spec with modified
parameters, the Critic flags the divergence.

**sigma-gates**: segregation index in [0.3, 0.8], cluster count > 1, population stable,
std across 30 seeds < 0.15.

**Pre-loaded false positive**: At low tolerance (0.2), the textbook predicts near-complete
segregation. The dynamic-tolerance extension shows partial mixing — but only if the
tolerance-update rule is implemented correctly. LLMs that generate from priors produce
the textbook result (wrong). The Critic catches it.

```bash
chp init my-project --experiment schelling
chp run
```

### 2. Spatial Prisoner's Dilemma

Nowak & May (1992) Nature paper — spatial PD on a lattice with deterministic imitation.

**Why it matters**: The imitation rule is subtle. Nowak & May use synchronous update
where each cell copies the HIGHEST-payoff neighbor. Most LLMs implement asynchronous
update (one cell at a time) because that's more common in ABM tutorials. This single
difference changes the emergent patterns completely. Prior-as-Detector catches the
update-order drift.

**sigma-gates**: cooperation rate in [0.2, 0.8], spatial clustering coefficient > 0,
pattern stability (Hamming distance between generations < threshold), std < 0.15.

**Pre-loaded false positive**: At b=1.8 (benefit-to-cost ratio), cooperators survive in
the spatial model but go extinct in well-mixed. LLMs that implement well-mixed dynamics
(the "textbook PD") report extinction — wrong. The frozen spec enforces spatial structure.

```bash
chp init my-project --experiment spatial-pd
chp run
```

### 3. Lotka-Volterra (Agent-Based)

Agent-based predator-prey with oscillation stability metrics. Calibrated against
classic Lotka-Volterra ODE predictions but with stochastic individual-level dynamics.

**Why it matters**: The ODE version is in every ecology textbook. LLMs generate ODE
coefficients when asked for "Lotka-Volterra." The agent-based version has DIFFERENT
dynamics — demographic stochasticity causes extinctions that the ODE cannot predict.
Prior-as-Detector catches ODE-parameter contamination in the agent-based model.

**sigma-gates**: prey population > 0 (no extinction), predator population > 0,
oscillation period within +/-20% of target, amplitude coefficient of variation < 0.5,
std < 0.15.

**Pre-loaded false positive**: Small populations (N=100) show apparent stable oscillations
for 50 generations, then one species goes extinct. The ODE predicts eternal oscillation.
If the Builder reports "stable oscillations" without checking for late-time extinction,
the Critic catches the premature conclusion.

```bash
chp init my-project --experiment lotka-volterra
chp run
```

### 4. SIR Epidemic

Stochastic SIR model with parameter inference and extinction checks.

**Why it matters**: The deterministic SIR has an exact analytical solution (R0 threshold).
LLMs know this and will generate deterministic dynamics even when asked for stochastic.
The stochastic version shows fadeout (disease extinction before reaching endemic
equilibrium) that the deterministic model cannot capture. Prior-as-Detector catches
deterministic contamination.

**sigma-gates**: final epidemic size within theoretical bounds, R0 recovery within +/-10%
of input, extinction probability matches analytical prediction for small N, std < 0.15.

**Pre-loaded false positive**: At R0=1.5 with N=200, the deterministic model predicts
a clean epidemic curve. The stochastic model shows fadeout in ~30% of runs. If the
Builder reports zero fadeout, it implemented deterministic dynamics — the Critic flags it.

```bash
chp init my-project --experiment sir
chp run
```

### 5. ML Hyperparameter Search

Bayesian optimization for neural network hyperparameters with proper cross-validation.

**Why it matters**: LLMs default to grid search (exhaustive, scales exponentially)
when asked for "hyperparameter optimization." The frozen spec requires Bayesian
optimization with Gaussian process surrogate. LLMs also inflate accuracy by
evaluating on training data — the spec enforces strict train/val/test splits.

**sigma-gates**: best_val_accuracy in [0.85, 0.99], overfitting_gap < 0.10
(train_acc - val_acc), search efficiency > grid baseline, std < 0.15.

**Pre-loaded false positive**: Builder reports 99.2% accuracy — but it's train
accuracy, not validation. The Critic catches the data leakage.

```bash
chp init my-project --experiment ml-hyperparam
chp run
```

### 6. Lorenz Attractor

Chaotic Lorenz (1963) system with sensitivity-to-initial-conditions verification.

**Why it matters**: Every LLM knows the Lorenz equations (sigma=10, rho=28, beta=8/3).
But most generate FIXED-STEP Euler integration, which is numerically unstable for
chaotic systems. The frozen spec requires adaptive RK45. The Prior-as-Detector
catches Euler contamination by checking trajectory divergence against the reference
solution.

**sigma-gates**: Lyapunov exponent in [0.8, 1.0], attractor bounded (|x| < 25),
trajectory does NOT converge to fixed point, std of Lyapunov < 0.15.

**Pre-loaded false positive**: Fixed-step Euler at dt=0.01 produces a trajectory
that looks correct for 10 time units, then diverges catastrophically. The Builder
reports "Lorenz attractor verified" from the first 10 units. The 30-seed battery
at t=50 catches the numerical instability.

```bash
chp init my-project --experiment lorenz
chp run
```

### 7. Grover's Algorithm (Quantum Simulation)

Simulated Grover's search algorithm with exact oracle and diffusion operators.

**Why it matters**: LLMs confuse Grover's quadratic speedup with classical brute-force
search. The frozen spec requires the exact quantum circuit: Hadamard, oracle
(phase flip on target), diffusion (inversion about mean). LLMs that generate from
priors produce classical search with O(N) complexity instead of O(sqrt(N)) iterations.

**sigma-gates**: success_probability > 0.90 at optimal iterations, iteration count
within +/-1 of floor(pi/4 * sqrt(N)), amplitude of target state > 0.95, std < 0.15.

**Pre-loaded false positive**: Builder implements classical random search and
reports "found target in sqrt(N) steps on average." But the distribution is
geometric (classical), not the peaked distribution at exactly floor(pi/4 * sqrt(N))
iterations (quantum). The Critic checks the iteration-count distribution.

```bash
chp init my-project --experiment quantum-grover
chp run
```

### 8. Izhikevich Neurons

Izhikevich (2003) spiking neuron model — the simple model that reproduces 20+
firing patterns.

**Why it matters**: LLMs commonly generate Hodgkin-Huxley equations (4 variables,
ionic conductances) when asked for "spiking neurons." The Izhikevich model uses
only 2 variables (v, u) with 4 parameters (a, b, c, d) and is a completely
different model. The Prior-as-Detector catches Hodgkin-Huxley contamination
by checking variable count and parameter names.

**sigma-gates**: spike_count in expected range for each firing pattern,
membrane potential bounded [-90, 40] mV, recovery variable bounded,
inter-spike-interval CV matches pattern type, std < 0.15.

**Pre-loaded false positive**: Builder produces "regular spiking" pattern but
uses Hodgkin-Huxley parameters (gNa, gK, gL). The model works but is the
WRONG MODEL. The Critic catches it by checking for the Izhikevich-specific
parameter set (a=0.02, b=0.2, c=-65, d=8 for regular spiking).

```bash
chp init my-project --experiment izhikevich
chp run
```

### 9. Blockchain Consensus

Simplified Byzantine fault-tolerant consensus (PBFT-style) with crash and
Byzantine failure injection.

**Why it matters**: LLMs default to centralized leader election (Raft/Paxos style)
when asked for "consensus algorithm." The frozen spec requires BYZANTINE fault
tolerance where nodes can send conflicting messages. The Prior-as-Detector
catches the Raft prior by checking whether the system survives Byzantine
(not just crash) failures.

**sigma-gates**: consensus_reached in > 95% of rounds with f < N/3 Byzantine
nodes, consensus_failed with f >= N/3, message_complexity within O(N^2) bound,
safety (no two honest nodes disagree) = 100%, std < 0.15.

**Pre-loaded false positive**: Builder implements Raft (crash-fault-tolerant only)
and reports "consensus reached with 1/3 faulty nodes." But Raft doesn't handle
Byzantine faults — nodes that lie. The system passes with crash faults but fails
when Byzantine nodes send conflicting prepare messages. The Critic injects
Byzantine behavior and watches it break.

```bash
chp init my-project --experiment blockchain
chp run
```

---

## Quick Start

### Install

```bash
pip install context-hacking
```

### Initialize a new project

```bash
chp init my-research-project
cd my-research-project
```

### Initialize with a showcase experiment

```bash
chp init my-project --experiment schelling
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
  Next focus: "Increase grid size to 100x100"
```

### Export paper appendix

```bash
chp export-paper
```

Generates a structured appendix with: full innovation log, dead ends, sigma-gate
results per turn, git diff summary, and the state vector timeline.

### Generate Cursor rules

```bash
chp cursor
```

Creates `.cursorrules` and `skills/` folder that auto-inject the Critic, gates,
and mode logic into Cursor or Claude Code sessions.

---

## Configuration

```yaml
# config.yaml
project:
  name: "my-research-project"
  description: "What this project investigates"
  frozen_paths: ["frozen/"]
  chain_prompt: "CHAIN_PROMPT.md"

models:
  builder: "claude-sonnet-4-20250514"
  critic: "claude-sonnet-4-20250514"
  reviewer: "claude-sonnet-4-20250514"
  council:
    - provider: "openai"
      model: "gpt-4o"
      api_key_env: "OPENAI_API_KEY"
    - provider: "xai"
      model: "grok-3"
      api_key_env: "GROK_API_KEY"

gates:
  seeds: 3
  convergence_seeds: 30
  sigma_threshold: 0.15
  anomaly_checks:
    - metric: "primary_metric"
      operator: ">"
      threshold: 0.25
    - metric: "primary_metric_std"
      operator: "<"
      threshold: 0.15
  max_consecutive_anomalies: 3

loop:
  max_turns: 50
  stagnation_threshold: 5
  max_consecutive_exploration: 3
  context_reset_interval: 15
  state_vector_interval: 5
  auto_tag: true

exit_conditions:
  science_complete: true
  performance_gate: true
  unresolvable_anomaly: true
  fundamental_misalignment: true
  human_stop: true

critic:
  mindset: "Assume the build failed until proven otherwise"
  instruction: "Argue AGAINST the science before scoring it"
  gates:
    - name: "frozen_compliance"
      threshold: 1.0
      blocking: true
    - name: "architecture"
      threshold: 0.85
      blocking: false
    - name: "scientific_validity"
      threshold: 0.85
      blocking: false
    - name: "drift_check"
      threshold: 0.85
      blocking: false
```

---

## Python API

```python
from context_hacking import Orchestrator, Config

config = Config.from_yaml("config.yaml")
loop = Orchestrator(config)

# Run the full loop until an exit condition
loop.run()

# Or step through manually
result = loop.step()  # one turn
print(loop.status())

# Access state
print(loop.current_mode)       # "VALIDATION" or "EXPLORATION"
print(loop.turn)               # current turn number
print(loop.dead_ends)          # list of logged dead ends
print(loop.innovation_log)     # full log
```

---

## How It Was Proven

CHP was developed and validated on [SIMSIV](https://github.com/kepiCHelaSHen/SIMSIV)
— a calibrated agent-based simulation of human social evolution.

| Metric | Without CHP | With CHP |
|--------|------------|---------|
| Coefficient accuracy | 1/96 (1%) | 96/96 (100%) |
| False positives caught | 0 | 1 (n=3, replicated and killed at n=10) |
| Code bugs found | 0 | 6 (migration routing, death year, fitness blend, ...) |
| Final result | — | p < 0.0001, d = -5.97, 6/6 seeds |
| Lines of code built | — | 7,663 (autonomous, 11 turns) |
| Experiments run | — | ~100 (~20,000 simulation-years) |

---

## The Core Insight

> **Don't fight what LLMs are bad at. Build systems that use it.**

LLMs hallucinate. That's not a bug to patch — it's a signal to exploit. When an LLM
generates from priors instead of from your source code, the divergence between prior
and source IS the drift detector.

CHP doesn't make LLMs smarter. It makes their failures visible, measurable, and
automatically correctable.

---

## License

MIT. Use it. Break it. Ship science with it.

## Citation

```bibtex
@software{rice2026chp,
  author = {Rice, James},
  title = {Context Hacking Protocol: A 9-Layer Anti-Drift Framework
           for LLM-Assisted Scientific Code Generation},
  year = {2026},
  url = {https://github.com/kepiCHelaSHen/context-hacking}
}
```
