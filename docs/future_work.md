# Future Work

Honest gaps and next steps. For reviewers and contributors.

---

## High Priority (would strengthen publication)

**1. Second large-scale validation.**
CHP is proven at scale on one project: SIMSIV (7,663 lines, 11 turns, p < 0.0001).
The 9 showcase experiments are 100-230 lines each. A second large-scale deployment
in a different domain (e.g., computational chemistry, robotics control) would prove
generalizability. Currently no second deployment site is available. This is the
single biggest gap.

**2. Head-to-head benchmark against existing frameworks.**
A qualitative comparison table exists (`docs/comparison.md`), but there are no
quantitative numbers against DSPy, Reflexion, or LATS on a shared task. The core
difficulty: these frameworks solve different problems (prompt optimization and
self-reflection vs. anti-drift governance). An apples-to-apples comparison requires
a task where both "optimize output quality" and "prevent specification drift" matter.
If such a task can be designed, the numbers would be compelling. Without it, the
qualitative comparison is the primary artifact.

**3. Council consensus detection (Layer 4 incomplete).**
`CouncilResult.consensus_issues` currently returns an empty list. The council calls
GPT-4o and Grok and collects responses, but cross-model agreement/disagreement is
not parsed or acted on. This is the most novel architectural claim (Layer 4) and
it is half-built. Spec: roadmap Phase 3.

---

## Medium Priority (would improve adoption)

**4. Multi-builder support.**
Builder/Critic/Reviewer are Claude-only. Supporting GPT-4o and Grok as builders
(not just council reviewers) would validate the framework is model-agnostic. The
prompts are tuned for Claude's instruction-following style and would need adaptation.

**5. Async council calls.**
Council currently calls OpenAI and xAI sequentially. Parallel async calls would
halve wall-clock time. Straightforward with `asyncio.gather`.

**6. Crash recovery (`chp run --resume`).**
If a run dies at turn 10, you start over. The state vector is written each turn
but isn't machine-parseable enough to restore mode, streaks, and gate history.
Spec: roadmap Phase 1.3.

**7. Streaming telemetry dashboard.**
The Streamlit dashboard exists but doesn't auto-refresh. Live streaming via
`st.experimental_rerun` or file-watcher would improve the development experience.

**8. `chp run --method cli` completion.**
The CLI method (Claude Code subagents) is partially implemented. The API method
(`--method api`) is the primary path. CLI mode needs completion for users without
an Anthropic API key.

---

## Low Priority (nice to have)

**9. Pydantic models.**
Replace dataclasses with Pydantic for runtime validation of config, telemetry,
and agent responses. Not urgent -- dataclasses work fine and the codebase is small.

**10. Standard benchmark evaluation.**
Run CHP on established LLM benchmarks (HumanEval, MBPP) to show general-purpose
applicability beyond scientific simulation code.

**11. Community experiment contributions.**
Infrastructure for community-submitted experiments: validation CI, experiment
catalog, submission guidelines.

## Explicitly Out of Scope

- **LaTeX export.** Use pandoc on the markdown output.
- **LangChain/LlamaIndex integration.** CHP uses direct API calls by design.
- **Web UI beyond Streamlit.** Focus stays on CLI + API.
- **Full production hardening.** CHP is a research protocol, not a SaaS product.
