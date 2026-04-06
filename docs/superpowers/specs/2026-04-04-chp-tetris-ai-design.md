# CHP-TETRIS-AI — Design Specification

## Overview

A self-improving Tetris AI that showcases the full 9-layer CHP protocol. The AI optimizes heuristic weights to play Tetris better each turn while the CHP loop catches mistakes, logs dead ends, detects false positives, and proves every improvement is real via sigma-gated statistical verification.

The primary purpose is a live demo: a "mission control" browser dashboard where observers watch the AI learn in real time — seeing the game, the score climb, the code being written, the strategies tried and failed, and the full CHP protocol health.

## Goals

- Showcase all 9 CHP layers working together on a visible, understandable problem
- Produce a "golden standard demo" that makes non-technical observers understand what CHP does
- Run live on a workstation or via screenshare — no static deployments needed
- Support both live mode (real API calls, real optimization) and demo mode (replay of a pre-baked run)

## Architecture

### Single-process monolith with library discipline

One Python process runs three async components:

1. **CHP Runner (optimizer.py)** — drives the optimization loop: calls Anthropic API, runs games, records telemetry, pushes state via WebSocket
2. **Tetris Engine (frozen/tetris_engine.py)** — pure library with zero I/O, called by the runner
3. **WebSocket Server (server.py)** — async Starlette/aiohttp server, serves dashboard HTML and pushes real-time state updates to the browser

The browser dashboard is a pure renderer. All state comes from the server via WebSocket. No game logic in JavaScript.

### Entry point

```
chp run --experiment CHP-TETRIS-AI --dashboard
```

Starts the WebSocket server, opens the browser, and either replays demo data or begins a live CHP run.

**Note:** The `--dashboard` flag is a new addition to `chp run` (it does not currently exist). This is a WebSocket-based dashboard served by Starlette, separate from the existing Streamlit `chp dashboard` command. Implementation must add this flag to the CLI.

### Execution model

The optimizer.py does **not** use `runner.py`. It implements its own turn loop making separate API calls for Builder, Critic, and Reviewer as independent prompts. It uses the framework's state management classes (Config, GateChecker, ModeManager, MemoryManager, TelemetryStore) for state tracking, but owns the API interaction and turn sequencing.

## Tetris Engine

Location: `experiments/CHP-TETRIS-AI/frozen/tetris_engine.py`

Implements:
- Standard 10x20 board
- 7 standard tetrominoes (I, O, T, S, Z, J, L) with SRS (Super Rotation System) rotation
- Gravity, line clearing, game-over detection
- Seeded RNG for piece sequence (numpy.random.Generator)
- `play_game(evaluate_fn, seed) -> GameResult` — plays a full game using the provided evaluation function, returns score, lines cleared, pieces placed, and full move history (for replay)

The engine is frozen (immutable). It lives in the `frozen/` directory and is never modified by the CHP loop. Gate 1 verifies this.

## Frozen Feature Functions

Location: `experiments/CHP-TETRIS-AI/frozen/features.py`

Eight feature functions, each taking a board state (2D numpy array) and returning a float:

| Feature | Description | Formula |
|---------|-------------|---------|
| `aggregate_height` | Sum of all column heights | `sum(max nonzero row per column)` |
| `complete_lines` | Full rows ready to clear | `count rows where all cells filled` |
| `holes` | Empty cells below a filled cell | `count per-column gaps below highest filled cell` |
| `bumpiness` | Height variation between adjacent columns | `sum(abs(h[i] - h[i+1]))` |
| `well_depth` | Deep single-column gaps | `sum(min(left_h, right_h) - col_h) for qualifying columns` |
| `tetris_readiness` | Is there a >=4 deep well with flat surroundings? | Binary: 1.0 if conditions met, 0.0 otherwise |
| `column_transitions` | Vertical filled/empty transitions | `count per-column filled↔empty changes` |
| `row_transitions` | Horizontal filled/empty transitions | `count per-row filled↔empty changes` |

All feature functions are frozen (immutable). The CHP loop cannot modify them. Gate 1 verifies this.

## Composition Layer

The only mutable part. Each CHP turn produces a `weights.json`:

```json
{
  "aggregate_height": -3.2,
  "complete_lines": 1.8,
  "holes": -4.5,
  "bumpiness": -2.3,
  "well_depth": 0.0,
  "tetris_readiness": 0.0,
  "column_transitions": 0.0,
  "row_transitions": 0.0
}
```

The evaluate function composes: `score = sum(weight * feature(board) for each feature)`.

Features with weight 0.0 are "undiscovered." The AI activates them by setting a non-zero weight.

**Validation:** The composition must only reference features that exist in the frozen set. Any reference to an unknown feature fails Gate 1.

### Builder output parsing contract

The Builder must output a JSON object with feature names as keys and float weights as values. The optimizer extracts this JSON from the Builder's response via regex (`\{[^}]+\}` matching the weight object).

The code panel in the dashboard shows a `def evaluate(board)` function **generated from the parsed weights** for readability. This display function is syntactically valid Python but is never executed — execution always uses the frozen features with the extracted weight floats. This means the Builder cannot introduce non-linear composition (e.g., `max(holes, bumpiness)`) — the composition is always a linear weighted sum.

If the Builder's response cannot be parsed into the 8-key weight vector, the turn is rejected and logged as a Critic Gate 1 failure.

## Deliberate Trap (PRIOR_ERRORS)

Location: `experiments/CHP-TETRIS-AI/frozen/prior_errors.py`

This module exports `KNOWN_TRAPS: list[dict]` where each dict has:
- `name: str` — human-readable trap name
- `detect(weights: dict) -> bool` — returns True if the weights exhibit this trap pattern
- `description: str` — what the trap does and why it's wrong
- `correction_hint: str` — guidance for the Critic/Builder

The optimizer checks all traps before and after each Builder response. If a trap is detected in the initial weights but corrected after, it's logged as a false positive catch.

LLMs consistently:
- Over-weight `complete_lines` (~+5.0) — greedy instinct to clear any line immediately
- Under-weight `holes` (~-1.0) — fail to see that buried holes are catastrophic long-term

This creates a player that clears singles and doubles but creates buried holes that kill the game.

The correct insight: `holes` should be weighted ~3-5x heavier than `complete_lines`. Penalizing holes is more important than rewarding clears.

The frozen spec documents this trap explicitly. The Critic watches for it. When the system catches and corrects this pattern, it is logged as a false positive detection — the showcase moment of the demo.

## CHP Loop — Full 9-Layer Implementation

### Turn cycle

1. **Health checks (Layer 8):** Builder, Critic, and Reviewer each receive a 3-line health check prompt. If any fails, the turn does not proceed.
2. **Dead end check (Layer 5):** Read dead_ends.md. Avoid repeating logged failures.
3. **Context load (Layer 5):** Read state_vector.md and last innovation_log entry.
4. **Council review (Layer 4):** In VALIDATION mode, send innovation log to GPT-4o and Grok-3 before build. In EXPLORATION mode, send after build. Council is optional — skipped if API keys not set.
5. **Builder (Layer 2):** Receives frozen spec, current weights, last scores, dead ends, innovation log. Proposes new weights.json and an evaluate() composition.
6. **Frozen validation (Layer 3):** Parse composition, verify all referenced features exist in frozen set. Gate 1 must equal 1.0.
7. **Run games (Layer 6):** Play 10 games with 10 different seeds using new weights. Compute mean score and coefficient of variation (CV = σ/μ). The engine must complete all 10 games in under 5 seconds; the dashboard shows a progress indicator during game execution.
8. **Sigma gate (Layer 6):** Pass if CV < 0.15. This is a **hard gate failure** (blocking), not a warning. The optimizer implements its own CV-based gate check rather than delegating to `GateChecker.evaluate()`, which uses raw standard deviation. Track consecutive anomalies. 3 consecutive failures trigger EXIT 3.
9. **Critic review (Layer 1, 2):** Score 4 gates. Check for known prior errors (trap detection). Argue against the result. In VALIDATION mode: Critic is hard blocker. In EXPLORATION mode: Critic is advisory.
10. **Reviewer (Layer 2):** Check code hygiene on the evaluate() composition. Valid Python, only frozen features, no unseeded randomness, no hardcoded magic numbers.
11. **Compare:** Is mean score better than previous best? If yes, accept. If no, log reason and revert.
12. **Mode check (Layer 7):** If stagnation >= 3 turns, switch to EXPLORATION. If EXPLORATION anomaly, revert to VALIDATION. Max 2 consecutive EXPLORATION turns.
13. **Record (Layer 5, 8):** Update telemetry.json, innovation_log.md, state_vector.md, weights_history.json.
14. **Broadcast:** Push all state to browser via WebSocket.
15. **Git tag (Layer 9):** Auto-tag on passing turns.
16. **Exit check (Layer 9):** Evaluate all 5 kill-switches.

### Five exit conditions (Layer 9)

- **EXIT 1 — Science complete:** Average score exceeds target threshold (e.g., 10,000 lines) AND variance is stable across seeds.
- **EXIT 2 — Performance plateau:** No improvement for N turns and exploration turns exhausted.
- **EXIT 3 — Unresolvable anomaly:** 3 consecutive sigma gate failures.
- **EXIT 4 — Fundamental misalignment:** Critic scores Gate 1 < 1.0 (frozen spec violated).
- **EXIT 5 — Human stop:** STOP file detected or user clicks stop in dashboard.

### Turn count target

15-20 turns for a full run. Enough for a clear progression arc: naive baseline → trap caught → breakthrough → refinement → convergence.

## WebSocket Data Flow

### Message types

```
Turn lifecycle:
  {type: "turn_start", turn: 7, mode: "VALIDATION"}
  {type: "health_check", agent: "builder", passed: true}
  {type: "health_check", agent: "critic", passed: true}
  {type: "health_check", agent: "reviewer", passed: true}
  {type: "council_result", reviews: [...], drift_flagged: false}
  {type: "code_update", code: "def evaluate(board):...", diff: [...]}
  {type: "weights_update", weights: {...}, previous: {...}}
  {type: "game_results", scores: [...], mean: 2400, cv: 0.08}
  {type: "sigma_gate", passed: true, cv: 0.08, threshold: 0.15, seeds: [...]}
  {type: "critic_verdict", gates: {...}, blocking: [...], verdict: "PASS"}
  {type: "reviewer_verdict", issues: [...], verdict: "APPROVE"}
  {type: "turn_complete", turn: 7, accepted: true, best_score: 2400}

Game replay (best game from current generation):
  {type: "game_start", seed: 42, generation: 7}
  {type: "game_move", board: [...], piece: "T", position: [4,2], rotation: 1, score: 2847}
  {type: "game_over", final_score: 48230, lines: 2847}

Events:
  {type: "dead_end", title: "...", reason: "..."}
  {type: "false_positive", description: "..."}
  {type: "mode_change", from: "VALIDATION", to: "EXPLORATION"}
  {type: "exit", reason: "EXIT 1: Science complete", turn: 18}
```

### Game replay encoding

The `board` field in `game_move` messages is a flat array of 200 integers (10 columns x 20 rows). Values: 0=empty, 1-7=piece type (I=1, O=2, T=3, S=4, Z=5, J=6, L=7). The `score` field is cumulative (running total). The `lines` field in `game_over` is total lines cleared (a good AI clears ~200-500 lines per game; early generations may clear <50).

### Demo mode vs Live mode

- **Demo mode:** Loads `run_history.json` (every WebSocket message from a previous run, timestamped). Replays at adjustable speed. No API calls, no computation. Works without API key.
- **Live mode:** Real API calls, real computation, real WebSocket pushes. Same message format — browser cannot distinguish.
- **Mode selection:** Mode is selected at startup via a toggle in the dashboard header. Switching modes mid-run resets the dashboard state and either starts a fresh live run or begins replaying from the start of the demo data. The optimization loop is stopped/started accordingly.

## Browser Dashboard

### Technology

Single HTML page, no build tools. Vanilla JavaScript + Canvas for the game board, SVG for charts. Connects to WebSocket on load. Pure renderer — all state from server. The server serves `index.html` and static assets (`app.js`, `style.css`) via Starlette's `StaticFiles` mount.

### Visual style

Light theme. White/light gray backgrounds, dark text, colored accents for status indicators. Clinical, data-dense. Designed for 1920x1080 workstation display.

### Layout — Mission Control

```
┌─────────────────────────────────────────────────────────────┐
│ CHP TETRIS AI — MISSION CONTROL    Turn 7/20  MODE  ● LIVE │
├──────────┬─────────────────────────────┬────────────────────┤
│          │                             │                    │
│  Live    │   Score Progression Chart   │   Live Code        │
│  Game    │   (SVG line chart with      │   (evaluate() fn   │
│  (Canvas)│   variance bands, markers)  │   syntax highlight │
│          │                             │   typewriter effect│
│  10x20   ├─────────────────────────────┤   diff highlights) │
│  board   │                             │                    │
│          │   Decision Log              ├────────────────────┤
│──────────│   (scrolling timeline,      │                    │
│ Current  │   color-coded entries:      │  Protocol Health   │
│ Weights  │   green=improve,            │  Gate 1-4 bars     │
│ (table)  │   red=dead end,             │  Sigma gate seeds  │
│          │   orange=false positive)    │  Mode badge        │
│          │                             │  Stats counters    │
├──────────┴─────────────────────────────┴────────────────────┤
│ experiments/CHP-TETRIS-AI    +9,320% improvement   CHP 0.2 │
└─────────────────────────────────────────────────────────────┘
```

### Header bar
- Experiment name
- Current turn / max turns
- Mode badge (VALIDATION / EXPLORATION)
- Live/Demo indicator
- Speed control (1x / 5x / 20x)
- Start / Stop / Reset buttons
- Demo / Live toggle

### Footer bar
- Experiment path
- Cumulative improvement percentage
- CHP version

## CHP Layer Reference

| Layer | Name | Where it appears in turn cycle |
|-------|------|-------------------------------|
| 1 | Prior-as-Detector | Step 9: Critic checks for known prior errors (PRIOR_ERRORS trap) |
| 2 | Synthetic Dialectic | Steps 5, 9, 10: Builder proposes, Critic argues against, Reviewer checks hygiene |
| 3 | Frozen Code Forcing | Step 6: Composition validated against frozen feature set, Gate 1 = 1.0 |
| 4 | Multi-Model Council | Step 4: GPT-4o + Grok-3 review, disagreement = drift signal |
| 5 | Context Window Mgmt | Steps 2, 3, 13: dead_ends.md, state_vector.md, innovation_log.md |
| 6 | Sigma-Gated Verification | Steps 7, 8: 10-seed games, CV < 0.15 threshold |
| 7 | Two-Mode Feedback | Step 12: VALIDATION/EXPLORATION switching, reversion protocol |
| 8 | Token-Efficient Arch | Steps 1, 13: Health checks, state vector compression |
| 9 | Self-Correcting Loop | Steps 15, 16: Git tags, 5 kill-switches (EXIT 1-5) |

## File Structure

The experiment lives at the project root level: `experiments/CHP-TETRIS-AI/`. This bypasses the discipline subfolder convention used by `cat-` prefixed experiments because this is a top-level showcase experiment, not a domain-specific one.

```
experiments/CHP-TETRIS-AI/
├── frozen/
│   ├── tetris_engine.py          # Game engine (immutable)
│   ├── features.py               # 8 feature functions (immutable)
│   ├── tetris_rules.md           # Frozen spec: rules, formulas, sources
│   └── prior_errors.py           # Known LLM mistakes + detection
├── tests/
│   ├── test_engine.py            # Engine correctness (deterministic games)
│   ├── test_features.py          # Feature functions on known boards
│   ├── test_composition.py       # Composition validation (frozen features only)
│   └── test_prior_errors.py      # Trap detection tests
├── dashboard/
│   ├── index.html                # Single-page mission control (light theme)
│   ├── app.js                    # WebSocket client, canvas renderer, charts
│   └── style.css                 # Light theme styles
├── server.py                     # WebSocket server (Starlette/aiohttp)
├── optimizer.py                  # CHP turn logic (API calls, games, gates)
├── weights.json                  # Current best weights
├── weights_history.json          # All weights per turn (for charts)
├── run_history.json              # Saved WebSocket messages (for demo mode)
├── metadata.json                 # CHP experiment metadata
├── config.yaml                   # CHP config (gates, seeds, thresholds, exits)
├── CHAIN_PROMPT.md               # Master design document
├── spec.md                       # Full specification
├── innovation_log.md             # Turn-by-turn log (append-only)
├── dead_ends.md                  # Failed strategies
├── state_vector.md               # Current state snapshot
└── REPORT.md                     # Generated after completion
```

## Dependencies

Added as optional dependency group `[tetris]` in pyproject.toml:
- `starlette` — async web framework
- `uvicorn` — ASGI server
- `websockets` — WebSocket protocol support

## Integration with Existing CHP

The optimizer.py imports from the existing CHP framework:
- `context_hacking.core.orchestrator` — Config, Orchestrator
- `context_hacking.core.gates` — GateChecker
- `context_hacking.core.modes` — ModeManager
- `context_hacking.core.memory` — MemoryManager
- `context_hacking.core.telemetry` — TelemetryStore, TurnMetrics
- `context_hacking.agents.critic` — parse_verdict, CriticVerdict
- `context_hacking.agents.reviewer` — parse_review, ReviewResult
- `context_hacking.agents.council` — run_council, CouncilResult

This is a real CHP experiment using the real framework, not a standalone project.

## Config.yaml

```yaml
project:
  name: "CHP-TETRIS-AI"
  description: "Self-improving Tetris AI — heuristic weight optimization"
  frozen_paths: ["frozen/"]
  chain_prompt: "CHAIN_PROMPT.md"
  innovation_log: "innovation_log.md"
  dead_ends: "dead_ends.md"
  state_vector: "state_vector.md"

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
      api_key_env: "XAI_API_KEY"

gates:
  seeds: 10
  cv_threshold: 0.15
  max_consecutive_anomalies: 3

loop:
  max_turns: 20
  stagnation_threshold: 3
  max_consecutive_exploration: 2
  state_vector_interval: 3
  auto_tag: true

exit_conditions:
  science_complete: true
  science_target_lines: 10000
  performance_gate: true
  unresolvable_anomaly: true
  fundamental_misalignment: true
  human_stop: true

critic:
  mindset: "Assume the weights are worse until the data proves otherwise"
  instruction: "Check for the line-clear greed trap. Verify hole penalty is adequate."
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

dashboard:
  port: 8080
  speed: 5
```

## Telemetry

Telemetry is stored at `.chp/telemetry.json` using the framework's `TelemetryStore` (default location). The experiment directory does not store its own copy. The dashboard reads telemetry via the WebSocket connection, not directly from the file.

## Environment

API keys are loaded from `api.env` in the project root. The optimizer loads this file at startup using `dotenv` or manual parsing. The file contains:
- `OPENAI_API_KEY` — used by the Multi-Model Council (GPT-4o)
- `XAI_API_KEY` — used by the Multi-Model Council (Grok-3)
- `ANTHROPIC_API_KEY` — must be set in the shell environment (not in api.env) for the Builder/Critic/Reviewer API calls

The `api.env` file is gitignored and must never be committed.

## Error Handling

- **API failure:** Retry once with 5-second backoff. If second attempt fails, log as a failed turn (no weight change), increment stagnation counter, continue to next turn.
- **WebSocket disconnect:** Browser auto-reconnects every 2 seconds. On reconnect, server pushes the full current state (current turn, all weights history, latest game board) so the browser can rebuild.
- **Game evaluation exception:** Catch the exception, score that seed's game as 0 lines. If >50% of seeds fail, treat the entire turn as an anomaly.
- **Invalid Builder output:** If weights cannot be parsed from the Builder's response, log as Gate 1 failure, increment anomaly counter, continue.

## Success Criteria

1. A fresh run from zero shows visible score improvement over 15-20 turns
2. The deliberate trap (line-clear greed) is detected and corrected, visible in the decision log
3. At least one dead end is logged and subsequently avoided
4. The sigma gate catches at least one high-variance result (false positive)
5. All 9 CHP layers are exercised and visible in the dashboard
6. Demo mode replays a polished golden run reliably
7. Live mode runs real API calls and produces genuine optimization
8. A non-technical observer can watch the dashboard and understand that the AI is learning, catching its own mistakes, and proving its improvements are real
