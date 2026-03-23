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

# ⚡ THE CHP RIGOR BENCHMARK (ALPHA)

**This is a Context Hijack for Scientific Determinism.** Standard LLMs operate on probabilistic "vibes." CHP is a 9-layer containment field that weaponizes LLM failure modes (hallucinations, sycophancy, amnesia) into a deterministic verification engine.

### 1. The 62,500x Precision Jump

Native LLM float precision hits a "guessing ceiling" at ~16 digits. CHP bypasses this token-limit bottleneck through multi-turn algorithmic sprints.

- **Native Precision:** ~16 decimal places.
- **CHP Verified Precision:** 1,000,000 digits.
- **The Multiplier:** **62,500x** native capability.
- **Proof:** Verified 1M digit runs for $\pi$ (Chudnovsky), $\sqrt{2}$ (Newton-Raphson), and $e$.

### 2. The 64% Prior-Drift Kill

We measured "Training Gravity"—the tendency for LLMs to default to textbook data over user specs.

- **Baseline Drift:** **64%** (LLMs ignore specific parameters in favor of common training priors).
- **CHP Drift:** **0%**.
- **The Mechanism:** **Layer 1 (Prior-as-Detector)** treats common LLM answers as a tripwire. If the output matches the "textbook" value instead of the "frozen" spec, the build is killed instantly.

### 3. Sigma-Gated Scientific Rigor

CHP replaces "plausible" code with statistical proof. Every simulation must pass **Layer 6 (Sigma-Gating)** or the turn aborts.

- **Threshold:** **$\sigma < 0.15$** across 30 seeds.
- **Lorenz Attractor:** Forced **RK45 adaptive integration** (Lyapunov = 0.346) where the LLM prior defaults to unstable Euler.
- **Grover’s Quantum Search:** Verified sinusoidal probability peaking at **$P = 0.9995$** ($k_{opt}=25$).
- **Izhikevich Neurons:** Mapping 5 distinct spiking patterns while successfully killing the **Hodgkin-Huxley prior**.

### 4. The 9-Layer Stack

| **Layer** | **Name**                 | **Function**                                                |
| --------- | ------------------------ | ----------------------------------------------------------- |
| **1**     | **Prior-as-Detector**    | Uses the LLM's own bias as a drift tripwire.                |
| **2**     | **Synthetic Dialectic**  | Forces adversarial review (Builder/Critic/Reviewer).        |
| **3**     | **Frozen Code Forcing**  | Renders specs physically immutable to the agent.            |
| **4**     | **Multi-Model Council**  | Triangulates Grok, GPT, and Claude to find prior-overlap.   |
| **5**     | **Context Window Mgmt**  | Persists "Dead Ends" and State outside the window.          |
| **6**     | **Sigma-Gated**          | Blocks any result not meeting statistical thresholds.       |
| **7**     | **Two-Mode Feedback**    | Toggles between Exploration and strict Validation.          |
| **8**     | **Token-Efficient**      | Uses 3-line health checks to prevent "Context Drunkenness." |
| **9**     | **Self-Correcting Loop** | Automated kill-switches for performance plateaus.           |

---

## The Core Idea: 9 LLM Weaknesses Turned Into Strengths

Every layer in CHP maps to a specific, well-documented LLM weakness. We don't fix
these weaknesses. We **flip them** — turning each failure mode into the mechanism
that prevents it.

| # | The LLM Weakness | The Flip | CHP Layer |
|---|-------------------|----------|-----------|
| 1 | **Hallucination** — generates plausible values from training priors instead of reading specs | The gap between prior and spec **IS the drift detector**. When the LLM produces 0.30 for a 0.10 parameter, the divergence triggers the alarm. | **Prior-as-Detector** |
| 2 | **Sycophancy** — agrees with itself, never challenges its own output | Force **three opposing roles** (Builder/Critic/Reviewer) so agreement means convergence, not self-confirmation. The Critic's job is to argue AGAINST the science before scoring it. | **Synthetic Dialectic** |
| 3 | **Boundary violation** — modifies what it shouldn't, ignores constraints | Declare published code **physically immutable**. All new code composes WITH frozen files. The LLM literally cannot edit the spec — only build on top of it. | **Frozen Code Forcing** |
| 4 | **Model-specific bias** — each LLM has different blind spots baked into training | Send the same work to **multiple models** (GPT-4o, Grok, Claude). Different priors = different errors. Disagreement between models IS the drift signal. | **Multi-Model Council** |
| 5 | **Amnesia** — forgets everything across sessions and context resets | Write **three external files** (state vector, innovation log, dead ends) that persist outside the context window. The LLM reads them at the start of every turn. Memory survives infinite resets. | **Context Window Mgmt** |
| 6 | **Vibes-based evaluation** — can't judge statistical significance, cherry-picks results | Replace judgment with **math**. Multi-seed runs with hard sigma thresholds. If variance across seeds > 0.15, the build is blocked. No amount of persuasive text overrides a failed statistical gate. | **Sigma-Gated Verification** |
| 7 | **Mode collapse** — either too conservative (copies spec verbatim) or too creative (ignores spec entirely) | **Two modes with automatic switching.** Validation (strict, Critic blocks) for known mechanisms. Exploration (loose, Critic advises) when stuck. Stagnation triggers creativity. Anomaly triggers reversion. Neither extreme persists. | **Two-Mode Feedback** |
| 8 | **Context waste** — fills the window with irrelevant information, loses track of what matters | **Targeted 3-line health checks** instead of full-context reviews. Single source of truth (CHAIN_PROMPT.md). State vectors compress 50 turns into 15 lines. Every token in the context is there for a reason. | **Token-Efficient Arch** |
| 9 | **No stopping criterion** — keeps generating forever, doesn't know when it's done or going in circles | **Five kill-switches** that halt the loop automatically: science complete, performance plateau, unresolvable anomaly, fundamental misalignment, human stop. The system terminates itself. | **Self-Correcting Loop** |

### How each flip works in practice

**Layer 1 — Prior-as-Detector.** We asked GPT-4o and Grok-3 to implement a cooperation
function 10 times each. GPT-4o produced an empathy coefficient of 0.362 on average
(truth: 0.15). Grok-3 produced `social_skill = 0.30` on ALL 10 trials (truth: 0.10,
zero variance). The LLM's prior is so strong it becomes **deterministic** — and that
determinism is what makes it detectable. If you know the LLM will always guess 0.30,
you just check whether the output says 0.30. If it does, it didn't read your spec.

**Layer 2 — Synthetic Dialectic.** The Builder proposed `empathy = 0.20`. Left
unchecked, this ships. But the Critic's instruction is: *"Assume the build failed
until proven otherwise. Argue AGAINST the science."* The Critic cross-references
`resources.py:289` and finds the frozen value is 0.15. Hard block. The Builder's
sycophantic tendency to produce "reasonable" code is defeated by the Critic's
adversarial mandate.

**Layer 3 — Frozen Code Forcing.** The Builder proposed a multiplicative formula
`CAC = mean_eff * density * conformity_amp`. This produces zeros in early simulation
years (density starts near zero). The frozen spec uses an additive decomposition.
Because the frozen code is immutable, the Builder cannot rationalize changing it —
it must compose with it. The boundary violation is architecturally impossible.

**Layer 4 — Multi-Model Council.** GPT-4o drifted empathy to 0.362. Grok-3 drifted
it to 0.235. They're both wrong, but they're wrong in **different ways**. When both
review the same code and disagree about whether it matches the spec, the disagreement
itself flags drift. Unanimous wrong answers are rare across models with different
training distributions.

**Layer 5 — Context Window Management.** Turn 3 tried asynchronous updates.
It failed. The dead end was logged: *"Do NOT repeat: async updates contradict
frozen/schelling_rules.md line 7."* Turn 7 started a new session with a fresh
context window. First thing the Builder reads: the dead ends file. It skips async
updates without being told twice. The LLM's amnesia is defeated by an external
memory it reads before every turn.

**Layer 6 — Sigma-Gated Verification.** Turn 5 found a positive result at n=3
seeds: the Bowles mechanism appeared causal (+0.039). A vibes-based system would
celebrate and ship. CHP's sigma gate said: *"Run at n=10."* At n=10, the effect
vanished (p = 0.954). False positive killed. The LLM's inability to judge
significance is replaced by a statistical gate that cannot be argued with.

**Layer 7 — Two-Mode Feedback.** After 5 turns of Validation with no improvement,
the system automatically switches to Exploration mode. The Builder can now propose
hypotheses beyond the frozen spec. But if an Exploration build produces an anomaly,
the Reversion Protocol fires: roll back to the last passing tag and return to
Validation. Neither creative chaos nor conservative stagnation persists.

**Layer 8 — Token-Efficient Architecture.** Instead of dumping the entire codebase
into context, each turn starts with a 3-line health check: *"Builder: what frozen
file governs this milestone? Critic: what is Gate 1? Reviewer: what architecture
rules apply?"* If any agent fails its check, the turn aborts before wasting tokens
on a build. The context window is curated, not stuffed.

**Layer 9 — Self-Correcting Loop.** At turn 10, the primary metric stopped
improving. At turn 11, it still hadn't improved. At turn 12, EXIT 2 fired:
*"Performance gate: no improvement for N consecutive turns."* The loop terminated
itself. The human reviewed the innovation log, saw that the mechanism was fully
characterized, and confirmed the exit. The LLM didn't loop forever — it
recognized completion and stopped.

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

## Live Dashboard (v0.2)

CHP includes an optional Streamlit dashboard that turns the loop into a
real-time scientific control panel. Install with:

```bash
pip install context-hacking[dashboard]
chp dashboard
```

### What You See

**Header bar** — project name, current turn, and a big colored mode indicator:
green for VALIDATION, amber for EXPLORATION, red for EXIT.

**sigma-Gauge Panel** — real-time gauges for every anomaly check defined in
`config.yaml`. Green = passing, red = failing, with the actual value and
threshold displayed. Updates every 5 seconds from `state_vector.md`.

**Critic Scorecard** — live Gate 1-4 scores from the most recent Critic review.
Color-coded: green >= threshold, red below. Shows blocking vs non-blocking issues.

**Council Votes** — latest GPT-4o and Grok reviews side by side. Consensus
issues highlighted in red. Drift flags shown with a warning banner.

**Innovation Log** — last 15 entries from `innovation_log.md`, scrollable, with
turn numbers, modes, and metric deltas. New entries appear automatically.

**Dead End Tracker** — all logged dead ends with red X markers and the "Do NOT
repeat" rule for each. Visible at a glance so you never drift into one.

**Experiment Gallery** — 9 clickable cards, one per built-in experiment. Each
shows the experiment name, domain, status (not started / in progress / complete),
and which Prior-as-Detector pattern it demonstrates.

**Export Button** — one click generates `paper_appendix.md` with the full
innovation log, dead ends, sigma-gate results, and state vector timeline.

### Experiment-Specific Live Plots

Each experiment gets a domain-appropriate visualization:

| Experiment | Live Plot |
|-----------|-----------|
| **Schelling** | 2D grid heatmap showing agent types + segregation index gauge |
| **Spatial PD** | Lattice with cooperators (blue) / defectors (red) + cooperation rate curve |
| **Lotka-Volterra** | Prey vs predator population time series + phase portrait |
| **SIR** | Epidemic curve (S/I/R stacked area) + R0 estimate badge |
| **ML Hyperparam** | Convergence curve (best-so-far accuracy) + overfitting gap bar |
| **Lorenz** | 3D butterfly attractor (rotatable) + Lyapunov exponent badge |
| **Grover's** | Amplitude bar chart per basis state + sinusoidal success curve |
| **Izhikevich** | Membrane voltage raster plot + ISI histogram |
| **Blockchain** | Node communication graph + safety/liveness status indicators |

Plots auto-detect which experiment is running from `config.yaml` and update
every 5 seconds by reading the experiment's output files.

### Architecture

The dashboard is READ-ONLY. It never writes to any CHP file. It reads:
- `state_vector.md` for current turn, mode, flags
- `innovation_log.md` for turn history
- `dead_ends.md` for failure tracking
- `config.yaml` for experiment identity and gate definitions
- Experiment output CSVs for live plots

This means `chp run` and `chp dashboard` can run simultaneously without
interference. The dashboard watches for file changes and updates automatically.

---

## Quick Start

### Install

```bash
pip install context-hacking              # core only
pip install context-hacking[dashboard]   # with live Streamlit dashboard
pip install context-hacking[all]         # everything (dashboard + ML experiments)
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

### Launch the live dashboard

```bash
chp dashboard
```

Opens the Streamlit dashboard at `http://localhost:8501` with real-time mode
indicator, sigma-gauges, innovation log, dead end tracker, and experiment-specific
plots. Requires `pip install context-hacking[dashboard]`.

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

## Ablation Study — Does Each Layer Matter?

Tested on the Schelling segregation model (11 frozen coefficients):

| Condition | Coefficient Accuracy | Behavioral Correctness | False Positive Caught? |
|-----------|---------------------|----------------------|----------------------|
| **A) No Protocol** (just "build Schelling") | 36% (4/11 match) | Not tested | No |
| **B) Spec Only** (frozen spec, no critic) | 100% (11/11) | ~60% (update order drifts) | No |
| **C) Full CHP** (spec + critic + gates) | 100% (11/11) | 100% (critic catches order) | **Yes** |

Each layer catches what the others miss:

| Layer | What It Catches | Without It |
|-------|----------------|-----------|
| Frozen Spec | Wrong coefficient values | 64% drift rate |
| Critic | Wrong execution behavior | False positives pass undetected |
| sigma-Gates | Stochastic instability | Lucky-seed results accepted |
| Dead Ends | Repeated mistakes | Same bug rediscovered each session |

Full ablation report: [`ablation/ABLATION_REPORT.md`](ablation/ABLATION_REPORT.md)

## Validated on SIMSIV

CHP was developed and proven on [SIMSIV](https://github.com/kepiCHelaSHen/SIMSIV)
— a calibrated agent-based simulation of human social evolution.

| Metric | Result |
|--------|--------|
| Lines of code built autonomously | 7,663 (11 turns) |
| Experiments run | ~100 (~20,000 simulation-years) |
| False positives caught | 1 (n=3 interaction effect killed at n=10) |
| Code bugs found by review | 6 (migration routing, death year, fitness blend, ...) |
| Final scientific result | p < 0.0001, d = -5.97 (North wins, 6/6 seeds) |

---

## The Core Insight

> **Don't fight what LLMs are bad at. Build systems that use it.**

LLMs hallucinate. That's not a bug to patch — it's a signal to exploit. When an LLM
generates from priors instead of from your source code, the divergence between prior
and source IS the drift detector.

CHP doesn't make LLMs smarter. It makes their failures visible, measurable, and
automatically correctable.

---

## Limitations

Honest assessment of what CHP is and isn't:

- **Not fully autonomous.** The API runner manages multi-turn conversations but
  requires an Anthropic API key and cannot handle all edge cases (complex file
  operations, environment setup, dependency installation). The Claude Code CLI
  method requires a human to launch it. CHP is a structured human-AI protocol,
  not a replacement for human judgment.

- **Validated on one project at scale.** SIMSIV is the only production-scale
  validation (7,663 lines, 11 turns). The 9 demo experiments are ~100-230 lines
  each. Generalization to other large codebases is plausible but unproven.

- **Claude-centric.** The Builder/Critic/Reviewer prompts are tuned for Claude's
  instruction-following style. The council calls GPT and Grok for review, but the
  build loop runs best in Claude Code. Portability to other LLMs is untested.

- **No comparison to existing frameworks.** CHP has not been benchmarked against
  DSPy, LATS, Reflexion, or other LLM agent frameworks. The ablation study
  compares CHP layers against each other, not against alternative approaches.

- **The drift measurement is domain-specific.** The 99% drift rate (95/96) was
  measured on SIMSIV implementation tasks. Different domains may have different
  drift rates depending on how well-represented they are in LLM training data.

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

---

## Experiment Registry

Full machine-readable index: [`EXPERIMENT_INDEX.json`](EXPERIMENT_INDEX.json)

### Loop-run experiments (`chp-test-run/experiments/`)
Built through the full CHP orchestrator loop with innovation logs and telemetry.

| Experiment | Domain | Turns | FPs | Key Result |
|-----------|--------|-------|-----|-----------|
| schelling-segregation | Social Science | 4 | 1 | p<0.000001, d=-1.83 |
| spatial-prisoners-dilemma | Game Theory | 3 | 1 | coop=0.41, std=0.017 |
| sir-epidemic | Epidemiology | 2 | 1 | fadeout=3% (impossible in ODE) |
| lorenz-attractor | Chaos Theory | 2 | 1 | RK45, Lyapunov=0.35 |
| izhikevich-neurons | Neuroscience | 2 | 1 | 5 patterns, no HH contamination |
| quantum-grover | Quantum Computing | 2 | 1 | P=0.9995 at k_opt=25 |
| blockchain-consensus | Distributed Systems | 2 | 1 | PBFT safety f<N/3 confirmed |
| lotka-volterra | Ecology | 2 | 1 | extinction confirmed (impossible in ODE) |
| ml-hyperparam-search | Machine Learning | 2 | 1 | val=0.87-0.92, no leakage |
| metal-harmony | Music Theory | 1 | 1 | classical: 6-9 errors. metal: 0 |

### Direct-prompt experiments (`experiments/`)
Built via single CLI prompt, verified against frozen reference.

| Experiment | Domain | Algorithm | Digits | Multiplier |
|-----------|--------|-----------|--------|-----------|
| euler-e | Mathematics | Taylor series | 10,000 | 667x LLM ceiling |
| pi-machin | Mathematics | Machin formula | 10,000 | 667x LLM ceiling |
| sqrt2-newton | Mathematics | Newton (14 iter) | 10,000 | 625x LLM ceiling |
| anatomy-viewer | Medical Visualization | HTML Canvas | N/A | 5 prior errors checked |
| anatomy-viewer-vtk | Medical Visualization | VTK 3D | N/A | 5 prior errors checked |
| schroeder-reverb | Audio DSP | Freeverb | N/A | 8 combs vs 4 (prior) |
| time_sprint | Mathematics | Binary splitting | 100,000 | 6,250x LLM ceiling |
| omega_sentinel_1M | Mathematics | Chudnovsky/Newton | 1,000,000 | 62,500x LLM ceiling |

### Staged experiments — spec written, not yet run
| Experiment | What it will build |
|-----------|-------------------|
| simsiv-v1-replication | 35-trait social evolution sim, ~10k lines |
| simsiv-v2-replication | SIMSIV with institutional differentiation |

### Framework assets
- `ablation/` — 3-condition ablation study: no spec (36% accuracy) -> spec only (100% values) -> full CHP (behavioral verification)
- `docs/methods_section.md` — publication-ready methods section
- `prompts/PROMPTS_INDEX.md` — index of all CLI prompts
