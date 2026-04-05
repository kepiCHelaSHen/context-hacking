# CHP 10/10 Master Roadmap

**Goal:** Take Context Hacking Protocol from 7.6/10 to 10/10 — ready for academic publication AND open-source adoption.

**Target audience:** Dual — peer reviewers at ML/AI venues (ICLR, NeurIPS workshops, ACL) AND developers who want to `pip install` and use it.

**Timeline:** No deadline. Do it right.

**Constraint:** No second large-scale deployment site available. We validate with what we have and document the gap honestly as future work.

---

## Dependency Graph

```
Phase 1: Core Completion ───────┐
  (runner.py, telemetry,        │
   crash recovery)              ├──> Phase 4: Testing
                                │     (integration tests need
Phase 2: Robustness ────────────┘      working core + robust parsing)
  (structured outputs,                        │
   config validation,                         v
   error handling)              Phase 5: Documentation
                                  (comparison table, methods,
Phase 3: Council Completion          cleanup untracked files)
  (consensus_issues,                          │
   disagreement detection)                    v
         │                      Phase 6: Final Polish
         └──────────────────>     (benchmarks, DX improvements,
                                   code quality sweep)
```

Phases 1-3 can be done in order but are internally independent. Phase 4 depends on 1+2. Phase 5 depends on 4. Phase 6 depends on everything.

---

## Phase 1: Core Framework Completion

**Current state:** Orchestrator loop defined but `runner.py` is partially implemented. Telemetry dataclass exists but isn't wired into the orchestrator. No crash recovery — if a run dies at turn 10, you start over.

**Goal:** Fully autonomous multi-turn execution with state persistence.

### 1.1 Complete runner.py (dual-mode: CLI + API)

**Files:** `context_hacking/runner.py`

The runner must support two execution methods — users choose based on their setup:
- `--method cli`: Agents run as Claude Code subagents (current partial implementation). No API key needed, uses the user's Claude Code session.
- `--method api`: Agents run via direct Anthropic API calls. Requires ANTHROPIC_API_KEY. Enables fully headless/autonomous runs.

Both methods share the same orchestrator loop and state management. The method only affects how agent prompts are sent and responses received.

The multi-turn loop needs:
- Anthropic API integration for `--method api` (Builder/Critic/Reviewer as API calls)
- Claude Code CLI piping for `--method cli` (current approach, needs completion)
- Token tracking per turn (feed into telemetry)
- Context window management — when messages list exceeds 150K tokens, summarize older turns into a 500-token synopsis and replace them. Track token count via API response `usage` field (api mode) or estimate from character count (cli mode).
- Error handling: API timeouts, rate limits, malformed responses — retry with exponential backoff (max 3 retries), all retry logic lives here in runner.py
- Clean exit on any of the 5 kill-switches

**Architecture note:** The orchestrator manages state (mode, gates, memory, telemetry). The runner manages execution (sending prompts, receiving responses). For `--method api`, runner calls through orchestrator.step() which updates state, then runner sends the appropriate agent prompts. They compose — runner drives, orchestrator governs.

**Acceptance criteria:**
- `chp run --method api` executes a full experiment autonomously (requires ANTHROPIC_API_KEY)
- `chp run --method cli` executes via Claude Code (no API key needed)
- Each turn logs tokens used, duration, and agent responses
- API errors retry with exponential backoff (max 3 retries) — retry logic in runner.py only
- Context window management: messages exceeding 150K tokens trigger summarization of older turns

### 1.2 Wire telemetry into orchestrator

**Files:** `context_hacking/core/orchestrator.py`, `context_hacking/core/telemetry.py`

TurnMetrics dataclass is defined with 50+ fields but not collected during runs.

- Orchestrator.step() must populate a TurnMetrics at the end of each turn
- TelemetryStore must persist after each turn (not just at end of run)
- Expose telemetry via `chp status --telemetry`
- Aggregate stats available programmatically for paper figures

**Acceptance criteria:**
- After each turn, `.chp/telemetry.json` contains full metrics
- `chp status` shows turn count, tokens used, drift rate, anomaly rate
- Telemetry survives crashes (persisted per-turn, not batch)

### 1.3 Crash recovery / checkpoint resume

**Files:** `context_hacking/core/orchestrator.py`, `context_hacking/core/memory.py`, `context_hacking/cli.py`

- `state_vector.md` already written each turn — make it machine-parseable
- Add `chp run --resume` that reads state_vector.md and continues from last turn
- Validate resume state: check innovation_log turn count matches, dead_ends consistent
- On resume: reload telemetry, restore mode (VALIDATION/EXPLORATION), restore streak counters

**Acceptance criteria:**
- Kill a run at turn 5, `chp run --resume` continues from turn 6
- All state restored: mode, streaks, gate history, telemetry
- Invalid state_vector.md produces clear error, not silent corruption

---

## Phase 2: Robustness Hardening

**Current state:** Critic verdicts parsed via regex on unstructured text. Config loaded from YAML with no schema validation. Health checks use hardcoded strings. One API timeout kills the entire run.

**Goal:** Eliminate fragile parsing, validate all inputs, handle all errors gracefully.

### 2.1 Structured LLM outputs

**Files:** `context_hacking/agents/critic.py`, `context_hacking/agents/reviewer.py`, `context_hacking/agents/council.py`

**Council (direct API):**
- OpenAI: use `response_format: { type: "json_object" }` with explicit JSON schema
- xAI/Grok: structured JSON prompt with validation on parse

**Critic + Reviewer (Claude Code CLI):**
- Redesign prompt templates to enforce strict output format (XML-tagged sections)
- Parse with explicit section extraction, not loose regex
- Add fallback: if primary parse fails, attempt secondary patterns
- Add validation: parsed gate scores must be floats in [0, 1], severity must be in {CRITICAL, WARNING, MINOR}
- On parse failure: log raw response to `.chp/parse_failures/`, return a "PARSE_FAILED" verdict that blocks merge (fail-safe, not fail-silent)

**Acceptance criteria:**
- Council returns structured JSON (no regex parsing)
- Critic/Reviewer prompt templates in `prompts/` updated with explicit XML-tagged output format instructions
- Critic/Reviewer parse failures are caught, logged, and block (not silently pass)
- Malformed gate scores (e.g., "0.95/1.0" instead of "0.95") handled gracefully

### 2.2 Remove hardcoded heuristics from runner

**Files:** `context_hacking/runner.py`

The `_extract_code_blocks` function (line ~296) uses hardcoded experiment-name checks ("schelling", "spatial", "prey", etc.) to determine output filenames. This is the most fragile code in the repo — adding a new experiment requires editing the runner.

- Replace heuristic filename detection with config-driven output mapping
- Experiment config specifies expected output files, runner uses those
- Fallback: if no config, use generic `output_{turn}.py` naming

**Acceptance criteria:**
- No experiment-specific strings in runner.py
- New experiments work without modifying runner code
- Existing experiments produce same output filenames as before

### 2.3 Config schema validation


**Files:** `context_hacking/core/orchestrator.py` (Config class)

- Define expected config schema (required keys, types, value ranges)
- Validate on load: missing keys get defaults with warning, invalid types raise
- Catch typos: `stagnation_threshhold` vs `stagnation_threshold` — flag unknown keys
- Add `chp validate` CLI command that checks config without running

**Acceptance criteria:**
- Misspelled config key produces warning listing closest valid key
- Missing required key produces error with default value shown
- `chp validate` exits 0 on good config, 1 on bad

### 2.4 Error handling in orchestrator loop

**Files:** `context_hacking/core/orchestrator.py`

Note: API retry logic lives in runner.py (Phase 1.1). This section covers orchestrator-level error handling only.

- Wrap each step of the 16-step cycle in try/except
- Step failures: log error with context (which step, which turn, which agent), skip step with warning (not crash)
- File I/O errors: log and continue (don't lose a 40-turn run because dead_ends.md has a permission error)
- Unhandled exceptions: catch at top level, write emergency state_vector, exit cleanly

**Acceptance criteria:**
- No single API call failure crashes the run
- Emergency state dump on unhandled exception
- All errors logged with context (which step, which turn, which agent)

---

## Phase 3: Council Completion

**Current state:** Council calls OpenAI and xAI APIs, collects responses, but `consensus_issues` returns empty list. Layer 4 (Multi-Model Council) is the most novel claim and it's half-built.

**Goal:** Council actually detects cross-model agreement/disagreement and acts on it.

### 3.1 Implement consensus detection

**Files:** `context_hacking/agents/council.py`

- Parse each council response for: flagged issues, drift warnings, suggested changes
- Cross-reference: if 2+ models flag the same issue → consensus issue (must fix)
- If only 1 model flags → advisory (note but don't block)
- If models disagree on a specific value → drift signal (flag for human review)

**Acceptance criteria:**
- `CouncilResult.consensus_issues` returns actual list of cross-model agreement issues
- `CouncilResult.any_drift_flagged` returns True when any model detects drift
- Disagreement between models on specific values logged as drift signal

### 3.2 Wire council decisions into orchestrator

**Files:** `context_hacking/core/orchestrator.py`

- In VALIDATION mode: consensus issues block the build (before step 8)
- In EXPLORATION mode: consensus issues are advisory (after step 12)
- Council drift signals increment a counter; N consecutive → EXIT condition
- Log council decisions in innovation_log.md

**Acceptance criteria:**
- Consensus issue in VALIDATION mode prevents build from proceeding
- Council decisions visible in `chp status` and innovation log
- Consecutive drift signals from council trigger exit

---

## Phase 4: Testing

**Current state:** Framework unit tests solid (~320 lines). No integration tests. No CLI tests beyond basic. No mocked council tests.

**Goal:** Comprehensive test suite that proves the 16-step cycle works end-to-end.

### 4.1 Integration tests for orchestrator

**Files:** `tests/test_integration.py`

- Mock LLM responses (Builder returns code, Critic returns verdict, Reviewer returns review)
- Run orchestrator for 5 turns
- Assert: mode switches happen on stagnation, gates fire correctly, telemetry populated, memory files written
- Assert: kill-switch exits work (max turns, consecutive anomalies, human stop)

**Acceptance criteria:**
- 5-turn integration test passes with mocked LLM
- Mode switch from VALIDATION → EXPLORATION → VALIDATION covered
- All 5 exit conditions tested

### 4.2 CLI tests

**Files:** `tests/test_cli.py`

- `chp init`: creates correct directory structure
- `chp validate`: catches bad config
- `chp status`: outputs correct format
- `chp run --resume`: resumes from state vector

**Acceptance criteria:**
- All CLI commands have at least one happy-path and one error-path test

### 4.3 Council mock tests

**Files:** `tests/test_council.py`

- Mock OpenAI and xAI responses
- Test consensus detection: 2 models agree → consensus issue found
- Test disagreement: models diverge → drift flagged
- Test API failure: one model fails → graceful degradation (use remaining)

**Acceptance criteria:**
- Consensus detection logic tested without real API calls
- Partial council failure (1 of 2 models down) handled gracefully

### 4.4 Parse robustness tests

**Files:** `tests/test_parsing.py`

- Critic parse: normal format, variant formats, malformed, empty
- Reviewer parse: all severity levels, missing fields, garbage input
- Council parse: valid JSON, invalid JSON, partial response

**Acceptance criteria:**
- Every parser has at least: happy path, variant format, malformed input, empty input tests
- Malformed input never raises unhandled exception

---

## Phase 5: Documentation

**Current state:** README is excellent (774 lines). Missing: comparison to alternatives, methodology clarity for 62,500x claim, untracked files in working tree.

**Goal:** Publication-ready documentation + clean repo state.

### 5.1 Comparison table vs. alternatives

**Files:** `README.md` or `docs/comparison.md`

Build a comparison table on axes that matter:
- Drift detection (CHP yes, DSPy no, Reflexion partial, LATS no)
- False positive handling (CHP yes via sigma-gating, others no)
- Multi-seed validation (CHP yes, others no)
- External memory / context survival (CHP yes, Reflexion partial, others no)
- Multi-model consensus (CHP yes, others no)
- Publication: cite DSPy (Khattab et al.), Reflexion (Shinn et al.), LATS (Zhou et al.)

**Acceptance criteria:**
- Table in README or linked doc with honest assessment (don't oversell)
- Each claim backed by specific mechanism, not handwaving

### 5.2 Methods section clarity

**Files:** `docs/methods_section.md`

- 62,500x precision claim: add explicit methodology (baseline digits, CHP digits, how measured)
- Prior-drift measurement: clarify how 95/96 was counted (which LLMs, which coefficients, how was "correct" defined)
- Ablation: make it more prominent (move from appendix-style to core results)

**Acceptance criteria:**
- A reviewer can reproduce the 62,500x claim from the methods section alone — includes exact baseline digit count, CHP digit count, and the formula used
- 95/96 methodology is unambiguous — lists which LLMs, which coefficients, and how "correct" was defined

### 5.3 Repository cleanup

**Files:** working tree

- Commit or .gitignore the untracked files: `CORE METHODOLOGY.MD`, `docs/MML_arXiv_paper.*`, `docs/MML_launch_tweet.md`, `docs/MML_plain_summary.md`, `video/`
- Clean up `.claude/settings.local.json` from tracked changes
- Ensure `api.env` is in .gitignore (never committed)
- Add CONTRIBUTING.md (for open-source adoption)

**Acceptance criteria:**
- `git status` is clean
- No credentials in repo history
- CONTRIBUTING.md exists with basic setup instructions

---

## Phase 6: Final Polish

**Current state:** Framework works. Need DX improvements and final quality sweep.

**Goal:** The experience of using CHP is as polished as the ideas behind it.

### 6.1 DX improvements

**Files:** `context_hacking/cli.py`

- `chp run --dry-run`: show what would happen without executing (print 16-step plan)
- `chp run --resume`: implemented in Phase 1, ensure polished UX
- `chp run --verbose`: debug logging mode

**Acceptance criteria:**
- Each flag works and has help text
- --dry-run shows full execution plan without API calls

Note: LaTeX export (`--format latex`) deferred — users can convert markdown output with pandoc. Not worth custom implementation.

### 6.2 Benchmarks vs. alternatives

**Files:** `docs/benchmarks.md`

CHP solves a different problem than DSPy/Reflexion/LATS (anti-drift governance vs. prompt optimization/self-reflection/tree search). Direct quantitative comparison is apples-to-oranges. Instead:

- Run CHP on 2-3 experiments and measure: drift rate, false positive rate, turns to convergence, token cost
- Compare to published self-correction rates from Reflexion paper and token efficiency from DSPy where axes overlap
- Be explicit about what CAN'T be compared and why (different task domains)
- If direct benchmarks emerge naturally during testing, include them; don't force weak numbers

**Acceptance criteria:**
- CHP's own metrics (drift rate, false positive rate, token cost) quantified across experiments
- Qualitative comparison table (from 5.1) is the primary comparison artifact
- Any quantitative comparison includes honest caveats about task domain differences

### 6.3 Code quality sweep

**Files:** all source files

- Run ruff + mypy strict on full codebase, fix all issues
- Ensure all public functions have docstrings
- Remove any dead code or commented-out blocks
- Final review of all 15 core framework files

**Acceptance criteria:**
- `ruff check .` passes with 0 errors
- `mypy --strict context_hacking/` passes (or known exceptions documented)
- No dead code in core package

### 6.4 Future work documentation

**Files:** `README.md` or `docs/future_work.md`

Document what's needed but not yet done:
- Second large-scale validation on a different codebase
- Multi-builder support (not just Claude)
- Async council calls (parallel GPT-4o + Grok)
- Streaming telemetry dashboard
- Community experiment contributions

**Acceptance criteria:**
- Future work section is honest, specific, and doesn't undermine current claims

---

## Success Criteria (10/10)

When all 6 phases are complete:

- [ ] `chp run --method api` executes a full experiment autonomously, no human in loop
- [ ] Crash at any turn → `chp run --resume` continues cleanly
- [ ] All LLM outputs parsed structurally (no fragile regex)
- [ ] Council consensus detection works and influences orchestrator decisions
- [ ] Integration test proves 5-turn orchestrator loop with mode switching
- [ ] All CLI commands tested
- [ ] Comparison table vs. DSPy/Reflexion/LATS published
- [ ] 62,500x claim methodology is reviewer-reproducible
- [ ] `git status` clean, no credentials, CONTRIBUTING.md exists
- [ ] `ruff check .` and `mypy --strict` pass
- [ ] Future work documented honestly

**Score projection:**
| Category | Current | After |
|----------|---------|-------|
| Code Quality | 8/10 | 10/10 |
| Documentation | 9/10 | 10/10 |
| Testing | 7/10 | 9.5/10 |
| Architecture | 9/10 | 10/10 |
| Novelty | 9/10 | 10/10 |
| Completeness | 7/10 | 10/10 |
| Production Readiness | 5/10 | 8.5/10 |
| Performance | 6/10 | 8/10 |

Testing stays at 9.5 because full end-to-end testing requires real API calls on real experiments, which is hard to automate perfectly. Production readiness at 8.5 because async + monitoring would push it to 10 but are correctly scoped as future work.

**Weighted average: ~9.5/10** — the remaining 0.5 comes from second large-scale validation and production hardening, both documented as future work.
