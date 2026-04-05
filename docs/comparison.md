# CHP vs. DSPy, Reflexion, and LATS

An honest comparison of the Context Hacking Protocol against three prominent
LLM agent frameworks, evaluated on axes relevant to scientific code generation.

## Comparison Table

| Axis | CHP | DSPy | Reflexion | LATS |
|------|-----|------|-----------|------|
| **Drift Detection** | **Yes.** Layer 1 uses the LLM's own training prior as a tripwire — if output matches the "textbook" value instead of the frozen spec, the build is killed. Measured: 64% drift rate caught at 0% pass-through. | No. Optimizes prompt quality, not output fidelity to a specification. No concept of spec-vs-prior divergence. | No. Self-reflection checks whether output is "good," not whether it drifted from a reference. | No. Tree search evaluates action trajectories, not specification compliance. |
| **False Positive Handling** | **Yes.** Sigma-gating requires multi-seed replication. In practice: a positive result at n=3 was killed at n=10 (p=0.954). Convergence runs use n=30. | No. Optimizes for metric improvement, not for distinguishing real effects from noise. | Partial. Reflection can catch obviously wrong outputs, but has no statistical machinery to distinguish n=3 flukes from real effects. | No. MCTS reward signal does not include replication across random seeds. |
| **Multi-Seed Validation** | **Yes.** Layer 6 requires sigma < 0.15 across 30 seeds. Any result that passes on one seed but fails on others is blocked. | No. | No. | No. |
| **External Memory** | **Yes.** Layer 5 writes state vector, innovation log, and dead ends to disk. These survive context window resets and are read at the start of every turn. | Partial. DSPy can persist optimized prompts/demos, but has no structured dead-end or state-vector persistence across sessions. | No. Reflection history lives in the context window. No persistence across resets. | No. The search tree is ephemeral. |
| **Multi-Model Consensus** | **Yes.** Layer 4 sends the same work to GPT-4o, Grok, and Claude. Disagreement between models flags drift (different training priors produce different errors). | No. Single pipeline, though it can target different LLMs. | No. Single-model self-reflection. | No. Single model generates and evaluates. |
| **Frozen Spec Enforcement** | **Yes.** Layer 3 declares reference code physically immutable. The agent composes with frozen files but cannot edit them. | No. Signatures define input/output types, not immutable reference implementations. | No. No concept of immutable reference code. | No. |
| **Mode Switching** | **Yes.** Layer 7 automatically toggles between VALIDATION (strict, Critic blocks) and EXPLORATION (loose, Critic advises) based on stagnation and anomaly detection. | Partial. DSPy switches between optimization strategies (bootstrap, MIPRO), but this is prompt optimization, not validation/exploration of scientific hypotheses. | No. Always in reflect-retry mode. | Partial. MCTS balances exploration/exploitation via UCB, but at the action level, not at the validation-vs-hypothesis level. |
| **Self-Correction** | **Yes.** Layer 2 (Synthetic Dialectic) forces Builder/Critic/Reviewer roles. Layer 9 adds kill-switches for performance plateaus. | Partial. Auto-optimization improves prompts based on metrics, but the LLM does not adversarially review its own scientific claims. | **Yes.** Core mechanism. The LLM reflects on its output, identifies errors, and retries. This is Reflexion's primary strength. | **Yes.** MCTS backpropagation updates node values, enabling the agent to avoid previously poor trajectories. |

## What CHP Does NOT Do

These are genuine gaps where CHP offers no capability:

- **Prompt optimization.** DSPy automatically tunes prompts and selects few-shot
  examples to maximize a metric. CHP uses hand-written chain prompts. If your
  bottleneck is prompt quality rather than specification compliance, DSPy is the
  better tool.

- **Tree search over action spaces.** LATS explores multiple reasoning paths via
  Monte Carlo tree search with backpropagation. CHP's loop is linear (one build
  per turn). For tasks where the optimal action sequence is unknown and the search
  space is large, LATS is more systematic.

- **Lightweight self-reflection without infrastructure.** Reflexion requires only
  a single LLM and a feedback signal. CHP requires frozen specs, multi-model API
  keys, external state files, and a configured gate system. For quick iteration
  on well-defined coding tasks, Reflexion has far less setup overhead.

- **Benchmark generality.** DSPy, Reflexion, and LATS have been evaluated on
  standard benchmarks (GSM8K, HumanEval, HotPotQA, WebShop, etc.). CHP has been
  validated on one production project (SIMSIV, 7,663 lines) and 9 domain-specific
  showcase experiments. Broader benchmark evaluation has not been conducted.

## Where Alternatives Excel

- **DSPy** excels when you need to systematically optimize prompt pipelines across
  many tasks. Its compiler-based approach to prompt tuning is unmatched.

- **Reflexion** excels at rapid self-improvement with minimal infrastructure. A
  single model reflecting on its own failures is effective for tasks where the
  correctness signal is clear and immediate (e.g., unit tests pass/fail).

- **LATS** excels at complex decision-making tasks where the search space is large
  and rewards are sparse. The MCTS backbone provides principled
  exploration/exploitation tradeoffs that a linear loop cannot match.

## Where CHP Fills a Gap

None of the three alternatives address the core failure mode CHP targets:
**an LLM that produces plausible, well-structured, syntactically correct code
that silently deviates from a scientific specification.** This failure is
invisible to self-reflection (the code "looks right"), undetectable by prompt
optimization (the prompt is fine, the prior is the problem), and irrelevant to
tree search (every branch produces the same training-prior contamination).

CHP's contribution is the machinery to detect and block this specific class of
error: frozen specs as immutable ground truth, prior-as-detector to catch
training contamination, multi-model consensus to triangulate blind spots, and
sigma-gating to prevent false positives from surviving replication.

## References

1. Khattab, O., et al. "DSPy: Compiling Declarative Language Model Calls into
   Self-Improving Pipelines." arXiv:2310.03714 (2023).

2. Shinn, N., et al. "Reflexion: Language Agents with Verbal Reinforcement
   Learning." NeurIPS 2023. arXiv:2303.11366 (2023).

3. Zhou, A., et al. "Language Agent Tree Search Unifies Reasoning Acting and
   Planning in Language Models." ICML 2024. arXiv:2310.04406 (2023).
