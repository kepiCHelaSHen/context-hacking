# Experiment Specification — CHP-TETRIS-AI

## Research Question

Can a CHP-guided AI optimize Tetris heuristic weights while maintaining frozen spec compliance, avoiding the line-clear greed trap, and demonstrating measurable performance improvement over a naive baseline?

## Milestones

### Milestone 1: Frozen Engine + Features Pass All Tests
- Tetris board engine implemented (10×20, SRS rotation, line clearing, game-over detection)
- All 8 frozen features implemented per `frozen/tetris_rules.md` formulas exactly
- Unit tests pass for all features with known board states
- AI move selector (linear weighted sum) operational

### Milestone 2: Optimizer Runs One Turn with Mocked API
- CHP loop scaffold in place
- Turn 1 completes with mocked Builder/Critic/Reviewer API calls
- weights.json updated from naive baseline
- State vector and innovation log updated correctly

### Milestone 3: Dashboard Renders Game Board and Receives WebSocket Messages
- WebSocket server streams board state, score, piece, weights
- Dashboard HTML/JS renders 10×20 board with colored tetrominoes
- Speed control (1–10×) functional
- Connects to live game or replays from log

### Milestone 4: Full Live Loop — 5 Turns with Real API, Score Improves
- 5 complete turns run against real Claude API
- At least one turn detects line-clear greed (complete_lines over-weighted)
- Weights improve measurably (lines cleared > naive baseline over 10 seeds)
- All gate checks logged

### Milestone 5: Full 20-Turn Run — Trap Caught, Dead Ends Logged, Demo Mode Works
- All 20 turns complete without unresolvable anomaly
- Line-clear greed trap explicitly caught and logged in dead_ends.md
- holes weight reaches at least −3.0 (3× stronger than complete_lines)
- Demo mode: auto-play visible in dashboard for human observer
- Final weights outperform naive baseline by ≥50% on lines-cleared metric

## Baseline

Naive weights (`weights.json` at turn 0):
- aggregate_height: -1.0, complete_lines: +1.0, holes: -1.0, bumpiness: -1.0
- well_depth, tetris_readiness, column_transitions, row_transitions: 0.0

Baseline performance target: establish mean lines-cleared over 10 seeded games before turn 1.

## Statistical Protocol

- Each weight set evaluated over 10 seeds (seeds 0–9)
- Primary metric: mean lines cleared per game
- Gate threshold: CV ≤ 0.15 (coefficient of variation across seeds)
- Anomaly: any turn where mean lines < previous best by >20%

## Constraints

- All 8 features frozen — no feature modification permitted
- Linear composition only — no non-linear scoring
- Seeded RNG — reproducibility required
- No `print()` — structured logging only
- Dashboard must not block game loop
