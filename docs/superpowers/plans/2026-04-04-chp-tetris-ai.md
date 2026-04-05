# CHP-TETRIS-AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a self-improving Tetris AI with a live "mission control" browser dashboard that showcases all 9 CHP protocol layers.

**Architecture:** Single Python process (async) with three components: frozen Tetris engine (pure library), CHP optimizer (API calls + turn loop), and WebSocket server (Starlette + static files). Browser dashboard is a pure renderer — all state pushed via WebSocket.

**Tech Stack:** Python 3.11+, numpy, starlette, uvicorn, websockets, anthropic SDK, vanilla JS + Canvas + SVG

**Spec:** `docs/superpowers/specs/2026-04-04-chp-tetris-ai-design.md`

---

## File Map

| File | Responsibility | Created in Task |
|------|---------------|----------------|
| `experiments/CHP-TETRIS-AI/frozen/tetris_engine.py` | Game engine: board, pieces, SRS rotation, play_game() | 2 |
| `experiments/CHP-TETRIS-AI/frozen/features.py` | 8 frozen feature functions | 3 |
| `experiments/CHP-TETRIS-AI/frozen/prior_errors.py` | KNOWN_TRAPS with detection functions | 4 |
| `experiments/CHP-TETRIS-AI/frozen/tetris_rules.md` | Frozen spec document | 1 |
| `experiments/CHP-TETRIS-AI/tests/__init__.py` | Test package init | 2 |
| `experiments/CHP-TETRIS-AI/tests/test_engine.py` | Engine tests: board ops, piece placement, game play | 2 |
| `experiments/CHP-TETRIS-AI/tests/test_features.py` | Feature function tests on known boards | 3 |
| `experiments/CHP-TETRIS-AI/tests/test_prior_errors.py` | Trap detection tests | 4 |
| `experiments/CHP-TETRIS-AI/tests/test_composition.py` | Weight parsing + validation tests | 5 |
| `experiments/CHP-TETRIS-AI/tests/test_optimizer.py` | Optimizer turn logic tests (mocked API) | 6 |
| `experiments/CHP-TETRIS-AI/optimizer.py` | CHP turn loop: API calls, gates, modes, memory | 6 |
| `experiments/CHP-TETRIS-AI/server.py` | WebSocket server + static file serving | 7 |
| `experiments/CHP-TETRIS-AI/dashboard/index.html` | Mission control HTML shell | 8 |
| `experiments/CHP-TETRIS-AI/dashboard/style.css` | Light theme styles | 8 |
| `experiments/CHP-TETRIS-AI/dashboard/app.js` | WebSocket client, Canvas game, SVG charts, panels | 8 |
| `experiments/CHP-TETRIS-AI/config.yaml` | CHP config for this experiment | 1 |
| `experiments/CHP-TETRIS-AI/metadata.json` | CHP experiment metadata | 1 |
| `experiments/CHP-TETRIS-AI/CHAIN_PROMPT.md` | Master design doc | 1 |
| `experiments/CHP-TETRIS-AI/spec.md` | Experiment specification | 1 |
| `experiments/CHP-TETRIS-AI/prompts/builder.md` | Builder agent prompt | 6 |
| `experiments/CHP-TETRIS-AI/prompts/critic.md` | Critic agent prompt | 6 |
| `experiments/CHP-TETRIS-AI/prompts/reviewer.md` | Reviewer agent prompt | 6 |
| `experiments/CHP-TETRIS-AI/innovation_log.md` | Empty log template | 1 |
| `experiments/CHP-TETRIS-AI/dead_ends.md` | Empty dead ends template | 1 |
| `experiments/CHP-TETRIS-AI/state_vector.md` | Initial state vector | 1 |
| `experiments/CHP-TETRIS-AI/weights.json` | Initial weights (all naive) | 1 |
| `context_hacking/cli.py` | Modify: add --dashboard flag to `chp run` | 9 |
| `pyproject.toml` | Modify: add [tetris] optional dependencies | 9 |

---

### Task 1: Project Scaffold & CHP Template Files

**Files:**
- Create: `experiments/CHP-TETRIS-AI/config.yaml`
- Create: `experiments/CHP-TETRIS-AI/metadata.json`
- Create: `experiments/CHP-TETRIS-AI/CHAIN_PROMPT.md`
- Create: `experiments/CHP-TETRIS-AI/spec.md`
- Create: `experiments/CHP-TETRIS-AI/frozen/tetris_rules.md`
- Create: `experiments/CHP-TETRIS-AI/innovation_log.md`
- Create: `experiments/CHP-TETRIS-AI/dead_ends.md`
- Create: `experiments/CHP-TETRIS-AI/state_vector.md`
- Create: `experiments/CHP-TETRIS-AI/weights.json`
- Create: `experiments/CHP-TETRIS-AI/tests/__init__.py`
- Create: `experiments/CHP-TETRIS-AI/frozen/__init__.py`
- Create: `experiments/CHP-TETRIS-AI/dashboard/` (empty dir)
- Create: `experiments/CHP-TETRIS-AI/prompts/` (empty dir)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p experiments/CHP-TETRIS-AI/{frozen,tests,dashboard,prompts}
```

- [ ] **Step 2: Write config.yaml**

Copy the exact config from the spec (Section: Config.yaml). This includes project metadata, model config, gate thresholds (seeds: 10, cv_threshold: 0.15), loop params (max_turns: 20, stagnation_threshold: 3), exit conditions, critic config, and dashboard port.

- [ ] **Step 3: Write metadata.json**

```json
{
  "display_name": "CHP Tetris AI — Self-Improving Heuristic Optimization",
  "standard": "loop",
  "domain": "Computer Science",
  "sprint": "tetris-ai-2026",
  "status": "in_progress",
  "key_result": null,
  "false_positives_caught": 0,
  "turns": null,
  "gate_scores": null,
  "statistical_result": null,
  "meta_spec_errors": 0,
  "notes": "Showcase experiment for CHP protocol — all 9 layers"
}
```

- [ ] **Step 4: Write frozen/tetris_rules.md**

The frozen spec document. Must include:
- Standard Tetris rules (10x20 board, 7 tetrominoes, SRS rotation, line clearing)
- All 8 feature formulas with exact definitions (copy from spec Section: Frozen Feature Functions)
- The deliberate trap description (Section: Deliberate Trap)
- Prior error patterns that LLMs exhibit
- Composition rule: score = linear weighted sum of frozen features only

- [ ] **Step 5: Write spec.md**

Brief experiment specification with milestones:
1. Frozen engine + features pass all tests
2. Optimizer runs one turn with mocked API
3. Dashboard renders game board and receives WebSocket messages
4. Full live loop: 5 turns with real API, score improves
5. Full 20-turn run: trap caught, dead ends logged, demo mode works

- [ ] **Step 6: Write CHAIN_PROMPT.md**

CHP master design doc template filled in for Tetris:
- Research question: "Can a CHP-guided AI optimize Tetris heuristic weights while maintaining frozen spec compliance?"
- Architecture: frozen features + mutable weights
- Non-negotiable constraints: all 8 features frozen, linear composition only, seeded RNG

- [ ] **Step 7: Write template files**

`innovation_log.md`:
```markdown
# Innovation Log — CHP-TETRIS-AI
```

`dead_ends.md`:
```markdown
# Dead Ends — CHP-TETRIS-AI
```

`state_vector.md`:
```markdown
# State Vector — Save Game
TURN: 0
MODE: VALIDATION
MILESTONE: not started
NEXT_TURN_FOCUS: begin
```

`weights.json`:
```json
{
  "aggregate_height": -1.0,
  "complete_lines": 1.0,
  "holes": -1.0,
  "bumpiness": -1.0,
  "well_depth": 0.0,
  "tetris_readiness": 0.0,
  "column_transitions": 0.0,
  "row_transitions": 0.0
}
```

`tests/__init__.py` and `frozen/__init__.py`: empty files.

- [ ] **Step 8: Commit**

```bash
git add experiments/CHP-TETRIS-AI/
git commit -m "feat(tetris): scaffold CHP-TETRIS-AI experiment structure"
```

---

### Task 2: Frozen Tetris Engine

**Files:**
- Create: `experiments/CHP-TETRIS-AI/frozen/tetris_engine.py`
- Create: `experiments/CHP-TETRIS-AI/tests/test_engine.py`

- [ ] **Step 1: Write test_engine.py — board basics**

```python
import numpy as np
import pytest
from tetris_engine import (
    Board, Piece, TETROMINOES, GameResult, play_game,
)

class TestBoard:
    def test_empty_board_dimensions(self):
        board = Board()
        assert board.grid.shape == (20, 10)
        assert np.all(board.grid == 0)

    def test_place_piece_on_empty_board(self):
        board = Board()
        piece = TETROMINOES["O"]  # 2x2 square
        placed = board.place_piece(piece, row=18, col=4)
        assert placed is True
        assert board.grid[18, 4] != 0
        assert board.grid[18, 5] != 0
        assert board.grid[19, 4] != 0
        assert board.grid[19, 5] != 0

    def test_cannot_place_out_of_bounds(self):
        board = Board()
        piece = TETROMINOES["I"]  # 4-wide
        placed = board.place_piece(piece, row=0, col=8)
        assert placed is False

    def test_cannot_place_overlapping(self):
        board = Board()
        piece = TETROMINOES["O"]
        board.place_piece(piece, row=18, col=4)
        placed = board.place_piece(piece, row=18, col=4)
        assert placed is False

    def test_line_clear(self):
        board = Board()
        # Fill bottom row completely
        board.grid[19, :] = 1
        cleared = board.clear_lines()
        assert cleared == 1
        assert np.all(board.grid[19, :] == 0)

    def test_multiple_line_clear(self):
        board = Board()
        board.grid[18, :] = 1
        board.grid[19, :] = 1
        cleared = board.clear_lines()
        assert cleared == 2

    def test_game_over_detection(self):
        board = Board()
        # Fill top row
        board.grid[0, :] = 1
        assert board.is_game_over() is True

    def test_empty_board_not_game_over(self):
        board = Board()
        assert board.is_game_over() is False
```

Note on imports: The test needs to import from the frozen directory. Use `conftest.py` or `sys.path` manipulation. The simplest approach: add a `conftest.py` in the tests dir that adds the experiment root and frozen dir to sys.path.

Create `experiments/CHP-TETRIS-AI/tests/conftest.py`:
```python
import sys
from pathlib import Path
exp_root = Path(__file__).parent.parent
sys.path.insert(0, str(exp_root))
sys.path.insert(0, str(exp_root / "frozen"))
```

Then tests import directly: `from tetris_engine import Board, ...`

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_engine.py -v
```

Expected: ImportError — `tetris_engine` does not exist yet.

- [ ] **Step 3: Write tetris_engine.py — Board class**

Implement in `experiments/CHP-TETRIS-AI/frozen/tetris_engine.py`:
- `Board` class with numpy grid (20, 10), dtype=int8
- `place_piece(piece, row, col)` — returns bool
- `clear_lines()` — returns count of lines cleared, shifts rows down
- `is_game_over()` — True if any cell in row 0 is filled
- `copy()` — returns a deep copy for move evaluation
- 7 TETROMINOES dict with SRS rotation states (each piece is a list of rotation matrices)
- `Piece` dataclass: `name`, `rotations` (list of 2D numpy arrays), `piece_id` (1-7)

SRS rotation data: each tetromino has 4 rotation states. Store as list of numpy arrays where 1 = filled cell. Standard Tetris piece definitions.

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_engine.py::TestBoard -v
```

Expected: All TestBoard tests pass.

- [ ] **Step 5: Write test_engine.py — piece generation and game play**

```python
class TestPieceGeneration:
    def test_seeded_sequence_is_deterministic(self):
        from tetris_engine import PieceGenerator
        gen1 = PieceGenerator(seed=42)
        gen2 = PieceGenerator(seed=42)
        seq1 = [gen1.next().name for _ in range(20)]
        seq2 = [gen2.next().name for _ in range(20)]
        assert seq1 == seq2

    def test_different_seeds_differ(self):
        from tetris_engine import PieceGenerator
        gen1 = PieceGenerator(seed=42)
        gen2 = PieceGenerator(seed=99)
        seq1 = [gen1.next().name for _ in range(20)]
        seq2 = [gen2.next().name for _ in range(20)]
        assert seq1 != seq2

    def test_all_seven_pieces_appear(self):
        from tetris_engine import PieceGenerator
        gen = PieceGenerator(seed=42)
        names = set(gen.next().name for _ in range(100))
        assert names == {"I", "O", "T", "S", "Z", "J", "L"}


class TestPlayGame:
    def test_returns_game_result(self):
        from tetris_engine import play_game, GameResult
        def dummy_eval(board):
            return 0.0
        result = play_game(dummy_eval, seed=42)
        assert isinstance(result, GameResult)
        assert result.lines_cleared >= 0
        assert result.pieces_placed > 0
        assert len(result.move_history) == result.pieces_placed

    def test_deterministic_with_same_seed(self):
        from tetris_engine import play_game
        def simple_eval(board):
            return -board.max_height()
        r1 = play_game(simple_eval, seed=42)
        r2 = play_game(simple_eval, seed=42)
        assert r1.lines_cleared == r2.lines_cleared
        assert r1.pieces_placed == r2.pieces_placed

    def test_better_eval_scores_higher(self):
        from tetris_engine import play_game
        def bad_eval(board):
            return 0.0  # random placement
        def ok_eval(board):
            return -board.aggregate_height()  # minimize height
        bad = play_game(bad_eval, seed=42)
        ok = play_game(ok_eval, seed=42)
        # ok_eval should survive longer
        assert ok.pieces_placed >= bad.pieces_placed

    def test_move_history_has_board_states(self):
        from tetris_engine import play_game
        def dummy_eval(board):
            return 0.0
        result = play_game(dummy_eval, seed=42)
        move = result.move_history[0]
        assert "board" in move
        assert "piece" in move
        assert "position" in move
        assert "score" in move
```

- [ ] **Step 6: Implement play_game() and PieceGenerator**

Add to `tetris_engine.py`:
- `PieceGenerator(seed)` — uses `numpy.random.Generator` with bag randomizer (standard 7-bag)
- `GameResult` dataclass: `lines_cleared`, `pieces_placed`, `score`, `move_history` (list of dicts)
- `play_game(evaluate_fn, seed)`:
  1. Create Board and PieceGenerator with seed
  2. For each piece: try all valid placements (column x rotation), score each with evaluate_fn on a board copy, pick the best
  3. Place best piece, clear lines, record move
  4. If game over, return GameResult
  5. Move history entry: `{board: grid.flatten().tolist(), piece: name, position: [row, col], rotation: rot_idx, score: cumulative_score}`

Performance target: a single game should complete in <500ms.

- [ ] **Step 7: Run all engine tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_engine.py -v
```

Expected: All pass.

- [ ] **Step 8: Commit**

```bash
git add experiments/CHP-TETRIS-AI/frozen/tetris_engine.py experiments/CHP-TETRIS-AI/tests/test_engine.py experiments/CHP-TETRIS-AI/tests/conftest.py
git commit -m "feat(tetris): frozen Tetris engine with SRS rotation and seeded RNG"
```

---

### Task 3: Frozen Feature Functions

**Files:**
- Create: `experiments/CHP-TETRIS-AI/frozen/features.py`
- Create: `experiments/CHP-TETRIS-AI/tests/test_features.py`

- [ ] **Step 1: Write test_features.py**

Test each of the 8 features against hand-crafted board states:

```python
import numpy as np
import pytest
from features import (
    aggregate_height, complete_lines, holes, bumpiness,
    well_depth, tetris_readiness, column_transitions, row_transitions,
    FEATURE_NAMES,
)

def _make_board(rows):
    """Helper: build a 20x10 board from bottom-up row descriptions."""
    grid = np.zeros((20, 10), dtype=np.int8)
    for i, row in enumerate(reversed(rows)):
        grid[19 - i, :len(row)] = row
    return grid

class TestAggregateHeight:
    def test_empty_board(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert aggregate_height(grid) == 0.0

    def test_single_column(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, 0] = 1  # height 1
        grid[18, 0] = 1  # height 2
        assert aggregate_height(grid) == 2.0

    def test_multiple_columns(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, 0] = 1  # col 0 height 1
        grid[19, 1] = 1  # col 1 height 1
        grid[18, 1] = 1  # col 1 height 2
        assert aggregate_height(grid) == 3.0  # 1 + 2

class TestCompleteLines:
    def test_no_complete(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert complete_lines(grid) == 0.0

    def test_one_complete(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, :] = 1
        assert complete_lines(grid) == 1.0

    def test_two_complete(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, :] = 1
        grid[18, :] = 1
        assert complete_lines(grid) == 2.0

class TestHoles:
    def test_no_holes(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, 0] = 1
        assert holes(grid) == 0.0

    def test_one_hole(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[18, 0] = 1  # filled
        grid[19, 0] = 0  # hole below
        assert holes(grid) == 1.0

    def test_multiple_holes(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[17, 0] = 1
        grid[18, 0] = 0  # hole
        grid[19, 0] = 0  # hole
        assert holes(grid) == 2.0

class TestBumpiness:
    def test_flat_surface(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, :] = 1  # all columns height 1
        assert bumpiness(grid) == 0.0

    def test_bumpy(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, 0] = 1  # col 0 height 1
        grid[19, 1] = 1
        grid[18, 1] = 1  # col 1 height 2
        # bumpiness between col 0 and 1 = |1-2| = 1
        # remaining columns have 0 height, contributes more bumps
        result = bumpiness(grid)
        assert result > 0

class TestWellDepth:
    def test_no_wells(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert well_depth(grid) == 0.0

    def test_simple_well(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        # Create a well: col 5 is empty, cols 4 and 6 are filled
        for row in range(16, 20):
            grid[row, 4] = 1
            grid[row, 6] = 1
        # Col 5 has a well of depth 4
        result = well_depth(grid)
        assert result > 0

class TestTetrisReadiness:
    def test_not_ready(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert tetris_readiness(grid) == 0.0

    def test_ready(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        # Fill bottom 4 rows except rightmost column
        for row in range(16, 20):
            grid[row, :9] = 1
        # Col 9 is empty with depth >= 4, neighbors are tall = tetris ready
        assert tetris_readiness(grid) == 1.0

class TestColumnTransitions:
    def test_empty_board(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert column_transitions(grid) == 0.0

    def test_alternating(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, 0] = 1
        grid[18, 0] = 0
        grid[17, 0] = 1
        # transitions: empty->filled at row 19, filled->empty at 18, empty->filled at 17
        result = column_transitions(grid)
        assert result >= 2

class TestRowTransitions:
    def test_empty_board(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        assert row_transitions(grid) == 0.0

    def test_gap_in_row(self):
        grid = np.zeros((20, 10), dtype=np.int8)
        grid[19, :] = 1
        grid[19, 5] = 0  # gap
        # Two transitions: filled->empty and empty->filled
        result = row_transitions(grid)
        assert result >= 2

class TestFeatureNames:
    def test_all_eight_present(self):
        assert len(FEATURE_NAMES) == 8
        assert "aggregate_height" in FEATURE_NAMES
        assert "holes" in FEATURE_NAMES
        assert "tetris_readiness" in FEATURE_NAMES
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_features.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement features.py**

Implement all 8 feature functions in `experiments/CHP-TETRIS-AI/frozen/features.py`. Each takes a `numpy.ndarray` (20, 10) and returns `float`. Also export `FEATURE_NAMES: list[str]` and `FEATURE_FNS: dict[str, Callable]` mapping name to function.

All implementations must use numpy operations for speed. No Python loops over individual cells where vectorization is possible.

- [ ] **Step 4: Run tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_features.py -v
```

Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add experiments/CHP-TETRIS-AI/frozen/features.py experiments/CHP-TETRIS-AI/tests/test_features.py
git commit -m "feat(tetris): 8 frozen feature functions with full test coverage"
```

---

### Task 4: Prior Errors / Trap Detection

**Files:**
- Create: `experiments/CHP-TETRIS-AI/frozen/prior_errors.py`
- Create: `experiments/CHP-TETRIS-AI/tests/test_prior_errors.py`

- [ ] **Step 1: Write test_prior_errors.py**

```python
from prior_errors import KNOWN_TRAPS

class TestKnownTraps:
    def test_traps_list_not_empty(self):
        assert len(KNOWN_TRAPS) >= 1

    def test_trap_has_required_fields(self):
        for trap in KNOWN_TRAPS:
            assert "name" in trap
            assert "detect" in trap
            assert callable(trap["detect"])
            assert "description" in trap
            assert "correction_hint" in trap

    def test_greedy_line_clear_trap_detected(self):
        """LLMs over-weight complete_lines, under-weight holes."""
        greedy_weights = {
            "aggregate_height": -1.0,
            "complete_lines": 5.0,  # way too high
            "holes": -1.0,         # way too low
            "bumpiness": -1.0,
            "well_depth": 0.0,
            "tetris_readiness": 0.0,
            "column_transitions": 0.0,
            "row_transitions": 0.0,
        }
        trap = next(t for t in KNOWN_TRAPS if "greed" in t["name"].lower())
        assert trap["detect"](greedy_weights) is True

    def test_good_weights_not_flagged(self):
        """Well-tuned weights should not trigger the trap."""
        good_weights = {
            "aggregate_height": -3.0,
            "complete_lines": 1.5,
            "holes": -4.5,
            "bumpiness": -2.0,
            "well_depth": 0.5,
            "tetris_readiness": 2.0,
            "column_transitions": 0.0,
            "row_transitions": 0.0,
        }
        for trap in KNOWN_TRAPS:
            assert trap["detect"](good_weights) is False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_prior_errors.py -v
```

- [ ] **Step 3: Implement prior_errors.py**

```python
"""Known LLM error patterns for Tetris heuristic weights."""

KNOWN_TRAPS = [
    {
        "name": "Line-Clear Greed Trap",
        "detect": lambda w: (
            abs(w.get("complete_lines", 0)) > abs(w.get("holes", 0))
            and abs(w.get("holes", 0)) < 2.0
        ),
        "description": (
            "LLMs consistently over-weight complete_lines and under-weight holes. "
            "This creates a greedy player that chases line clears while burying holes, "
            "leading to rapid stack death."
        ),
        "correction_hint": (
            "The hole penalty should be 3-5x stronger than the line clear reward. "
            "Holes are catastrophic; line clears are nice-to-have."
        ),
    },
]
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_prior_errors.py -v
```

Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add experiments/CHP-TETRIS-AI/frozen/prior_errors.py experiments/CHP-TETRIS-AI/tests/test_prior_errors.py
git commit -m "feat(tetris): prior error trap detection — line-clear greed"
```

---

### Task 5: Composition Layer & Weight Parsing

**Files:**
- Create: `experiments/CHP-TETRIS-AI/tests/test_composition.py`
- Create: `experiments/CHP-TETRIS-AI/composition.py`

- [ ] **Step 1: Write test_composition.py**

```python
import json
import pytest
from composition import (
    parse_weights_from_response, validate_weights,
    build_evaluate_fn, generate_code_display,
)

class TestParseWeights:
    def test_extracts_json_from_response(self):
        response = '''Here are my proposed weights:
        {"aggregate_height": -3.2, "complete_lines": 1.8, "holes": -4.5,
         "bumpiness": -2.3, "well_depth": 0.5, "tetris_readiness": 2.0,
         "column_transitions": 0.0, "row_transitions": 0.0}
        I increased the hole penalty because...'''
        weights = parse_weights_from_response(response)
        assert weights["holes"] == -4.5
        assert weights["well_depth"] == 0.5

    def test_returns_none_on_no_json(self):
        response = "I think we should try different weights."
        weights = parse_weights_from_response(response)
        assert weights is None

    def test_returns_none_on_invalid_keys(self):
        response = '{"unknown_feature": 1.0, "holes": -2.0}'
        weights = parse_weights_from_response(response)
        assert weights is None

class TestValidateWeights:
    def test_valid_weights(self):
        w = {
            "aggregate_height": -3.2, "complete_lines": 1.8,
            "holes": -4.5, "bumpiness": -2.3,
            "well_depth": 0.5, "tetris_readiness": 2.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        assert validate_weights(w) is True

    def test_missing_key(self):
        w = {"aggregate_height": -3.2}  # missing 7 keys
        assert validate_weights(w) is False

    def test_extra_key_fails(self):
        w = {
            "aggregate_height": -3.2, "complete_lines": 1.8,
            "holes": -4.5, "bumpiness": -2.3,
            "well_depth": 0.5, "tetris_readiness": 2.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
            "invented_feature": 1.0,
        }
        assert validate_weights(w) is False

class TestBuildEvaluateFn:
    def test_returns_callable(self):
        w = {
            "aggregate_height": -1.0, "complete_lines": 1.0,
            "holes": -1.0, "bumpiness": -1.0,
            "well_depth": 0.0, "tetris_readiness": 0.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        fn = build_evaluate_fn(w)
        assert callable(fn)

    def test_evaluate_empty_board_is_zero(self):
        import numpy as np
        w = {
            "aggregate_height": -1.0, "complete_lines": 1.0,
            "holes": -1.0, "bumpiness": -1.0,
            "well_depth": 0.0, "tetris_readiness": 0.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        fn = build_evaluate_fn(w)
        grid = np.zeros((20, 10), dtype=np.int8)
        assert fn(grid) == 0.0

class TestGenerateCodeDisplay:
    def test_produces_valid_python(self):
        w = {
            "aggregate_height": -3.2, "complete_lines": 1.8,
            "holes": -4.5, "bumpiness": -2.3,
            "well_depth": 0.5, "tetris_readiness": 2.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        code = generate_code_display(w)
        assert "def evaluate(board):" in code
        assert "-4.500" in code or "-4.5" in code
        # Verify it's syntactically valid
        compile(code, "<test>", "exec")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_composition.py -v
```

- [ ] **Step 3: Implement composition.py**

`experiments/CHP-TETRIS-AI/composition.py`:
- `parse_weights_from_response(text: str) -> dict | None` — regex extract JSON, validate keys, return dict or None
- `validate_weights(weights: dict) -> bool` — exactly 8 keys, all in FEATURE_NAMES, all float values
- `build_evaluate_fn(weights: dict) -> Callable` — returns a function that takes a grid and returns the weighted sum using frozen feature functions
- `generate_code_display(weights: dict) -> str` — generates a readable `def evaluate(board)` string for the dashboard code panel

- [ ] **Step 4: Run tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_composition.py -v
```

Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add experiments/CHP-TETRIS-AI/composition.py experiments/CHP-TETRIS-AI/tests/test_composition.py
git commit -m "feat(tetris): composition layer — weight parsing, validation, evaluate builder"
```

---

### Task 6: Optimizer (CHP Turn Loop)

**Files:**
- Create: `experiments/CHP-TETRIS-AI/optimizer.py`
- Create: `experiments/CHP-TETRIS-AI/tests/test_optimizer.py`
- Create: `experiments/CHP-TETRIS-AI/prompts/builder.md`
- Create: `experiments/CHP-TETRIS-AI/prompts/critic.md`
- Create: `experiments/CHP-TETRIS-AI/prompts/reviewer.md`

This is the largest task. The optimizer implements the full 16-step CHP turn cycle.

- [ ] **Step 1: Write agent prompt files**

`prompts/builder.md` — Builder prompt that:
- Receives current weights, scores, dead ends, feature descriptions
- Must output a JSON weight object
- Must explain reasoning
- Told about all 8 features and which are currently active (non-zero)

`prompts/critic.md` — Critic prompt that:
- Receives proposed weights, game scores, prior_errors info
- Scores 4 gates (frozen, architecture, scientific, drift)
- Checks for the line-clear greed trap explicitly
- Must output structured gate scores and verdict

`prompts/reviewer.md` — Reviewer prompt that:
- Checks the weight vector for hygiene: are values reasonable (not NaN/Inf), are all keys present, no exotic values
- Does NOT evaluate scientific merit (that's the Critic's job)

- [ ] **Step 2: Write test_optimizer.py — core logic tests**

```python
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

class TestOptimizerTurnLogic:
    def test_load_env_keys(self):
        """Optimizer loads api.env at startup."""
        from optimizer import load_env
        # This test verifies the function exists and returns a dict
        # Actual key loading depends on file existing
        result = load_env("api.env")
        assert isinstance(result, dict)

    def test_cv_gate_pass(self):
        from optimizer import check_cv_gate
        scores = [100, 105, 98, 102, 101, 99, 103, 97, 104, 100]
        passed, cv = check_cv_gate(scores, threshold=0.15)
        assert passed is True
        assert cv < 0.15

    def test_cv_gate_fail(self):
        from optimizer import check_cv_gate
        scores = [100, 500, 50, 800, 20, 600, 10, 900, 30, 700]
        passed, cv = check_cv_gate(scores, threshold=0.15)
        assert passed is False
        assert cv > 0.15

    def test_compare_scores_improvement(self):
        from optimizer import is_improvement
        assert is_improvement(new_mean=2400, old_mean=1800) is True
        assert is_improvement(new_mean=1800, old_mean=2400) is False
        assert is_improvement(new_mean=1800, old_mean=1800) is False

    def test_build_builder_prompt(self):
        from optimizer import build_builder_prompt
        prompt = build_builder_prompt(
            weights={"holes": -1.0, "complete_lines": 1.0},
            best_score=500,
            dead_ends=["pure line-clear maximization"],
            innovation_log_tail="Turn 1: baseline",
            feature_descriptions={"holes": "empty cells below filled"},
        )
        assert "holes" in prompt
        assert "500" in prompt
        assert "pure line-clear" in prompt
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_optimizer.py -v
```

- [ ] **Step 4: Implement optimizer.py**

`experiments/CHP-TETRIS-AI/optimizer.py` — The main module. Key functions:

**Utility functions:**
- `load_env(path: str) -> dict` — parse api.env key=value pairs
- `check_cv_gate(scores: list[float], threshold: float) -> tuple[bool, float]` — compute CV, return (passed, cv)
- `is_improvement(new_mean: float, old_mean: float) -> bool`
- `call_anthropic(system: str, prompt: str, model: str, api_key: str) -> str` — async, single API call

**Prompt builders:**
- `build_builder_prompt(weights, best_score, dead_ends, innovation_log_tail, feature_descriptions) -> str`
- `build_critic_prompt(weights, scores, cv, prior_traps_detected) -> str`
- `build_reviewer_prompt(weights) -> str`
- `build_health_check_prompt(agent: str) -> str` — 3-line health check for Builder/Critic/Reviewer

**CHP Layer implementations within run_turn():**

The `run_turn(state: TurnState, broadcast_fn: Callable) -> TurnResult` function implements all 16 steps of the turn cycle:

1. **Health checks (Layer 8):** Call `call_anthropic()` with `build_health_check_prompt()` for each of Builder, Critic, Reviewer. Validate responses using `context_hacking.agents.critic.validate_health_check` and `context_hacking.agents.reviewer.validate_health_check`. Broadcast `{type: "health_check", agent: name, passed: bool}` for each. If any fail, abort the turn.

2. **Dead end check (Layer 5):** `memory.load_dead_ends()` — pass to Builder prompt.

3. **Context load (Layer 5):** `memory.read_state_vector()` and `memory.last_innovation_entry()`.

4. **Council review (Layer 4):** If in VALIDATION mode and council API keys are available, call `context_hacking.agents.council.run_council(innovation_log, council_config)`. Broadcast `{type: "council_result", reviews: [...], drift_flagged: bool}`. If keys not set, skip with log warning. In EXPLORATION mode, defer council to after build (step 12b).

5. **Builder call (Layer 2):** Call Anthropic API with builder prompt. Parse weights from response.

6. **Frozen validation (Layer 3):** `validate_weights()` from composition.py. Gate 1 = 1.0 if valid, 0.0 if not.

7. **Run games (Layer 6):** 10 seeds, `play_game(evaluate_fn, seed)` for each.

8. **Sigma gate (Layer 6):** `check_cv_gate()`. Broadcast `{type: "sigma_gate", ...}`. Track consecutive anomalies.

9. **Critic call (Layer 1, 2):** Call Anthropic API with critic prompt. Parse with `parse_verdict()`. Also check `prior_errors.KNOWN_TRAPS` — if trap was active before but not after, log as false positive catch. Broadcast `{type: "critic_verdict", ...}`.

10. **Reviewer call (Layer 2):** Call Anthropic API with reviewer prompt. Parse with `parse_review()`. Broadcast `{type: "reviewer_verdict", ...}`.

11. **Compare:** `is_improvement()`. If not improved, log reason and revert weights.

12. **Mode check (Layer 7):** `modes.record_turn(metrics_improved, anomaly)`. If mode changed, broadcast `{type: "mode_change", ...}`. If EXPLORATION mode and council was deferred (step 4), run council now.

13. **Record (Layer 5, 8):** `telemetry.add_turn(metrics)`, `memory.append_innovation_log()`, `memory.write_state_vector()`. Write `weights_history.json`.

14. **Broadcast:** `{type: "turn_complete", ...}` with all turn data.

15. **Git tag (Layer 9):** If `config.auto_tag` and gate passed and not anomaly, create git tag `chp-tetris-turn-{N}-pass` using `gitpython`.

16. **Exit check (Layer 9):** Evaluate all 5 kill-switches:
    - EXIT 1: `mean_score >= config.exit_conditions.science_target_lines` AND CV is stable
    - EXIT 2: `modes.stagnation_streak >= stagnation_threshold` AND `modes.exploration_streak >= max_consecutive_exploration`
    - EXIT 3: `consecutive_anomalies >= max_consecutive_anomalies`
    - EXIT 4: Gate 1 < 1.0 (frozen spec violated)
    - EXIT 5: `Path("STOP").exists()` OR `state.stop_requested` (set by server API)
    
    If any exit triggers, broadcast `{type: "exit", reason: "...", turn: N}` and return.

**Loop runner:**
- `run_loop(config_path: str, broadcast_fn: Callable) -> None` — async, initializes TurnState from config, runs `run_turn()` in a loop until exit condition or max_turns reached.

**Framework integration:**
- `context_hacking.core.modes.ModeManager` for VALIDATION/EXPLORATION switching
- `context_hacking.core.memory.MemoryManager` for dead_ends, innovation_log, state_vector
- `context_hacking.core.telemetry.TelemetryStore` for metrics
- `context_hacking.agents.critic.parse_verdict` and `validate_health_check` for Critic
- `context_hacking.agents.reviewer.parse_review` and `validate_health_check` for Reviewer
- `context_hacking.agents.council.run_council` for Multi-Model Council

It does NOT use `GateChecker.evaluate()` — it implements its own CV-based gate.

The `broadcast_fn` callback is called with every WebSocket message dict. The server passes its own broadcast function; tests pass a mock.

- [ ] **Step 5: Run tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_optimizer.py -v
```

Expected: All pass.

- [ ] **Step 6: Commit**

```bash
git add experiments/CHP-TETRIS-AI/optimizer.py experiments/CHP-TETRIS-AI/tests/test_optimizer.py experiments/CHP-TETRIS-AI/prompts/
git commit -m "feat(tetris): CHP optimizer — full 9-layer turn loop with API integration"
```

---

### Task 7: WebSocket Server

**Files:**
- Create: `experiments/CHP-TETRIS-AI/server.py`

- [ ] **Step 1: Implement server.py**

Uses Starlette + uvicorn. Key responsibilities:

- Serve static files from `dashboard/` directory
- WebSocket endpoint at `/ws`
- Track connected clients (set of websockets)
- `broadcast(message: dict)` — JSON-encode and send to all clients
- On WebSocket connect: send full current state (for reconnection)
- `start_live_mode(config_path)` — launch optimizer.run_loop() as async task, passing broadcast as callback
- `start_demo_mode(run_history_path)` — load run_history.json, replay messages with timestamps
- `/api/start` — POST endpoint to start live/demo mode
- `/api/stop` — POST endpoint to stop current run
- `/api/reset` — POST endpoint to reset state
- `/api/speed` — POST endpoint to change replay speed

```python
"""CHP-TETRIS-AI WebSocket server."""
import asyncio
import json
import logging
from pathlib import Path
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.responses import JSONResponse

_log = logging.getLogger(__name__)
EXPERIMENT_DIR = Path(__file__).parent

class TetrisServer:
    def __init__(self):
        self.clients: set[WebSocket] = set()
        self.state: list[dict] = []  # all messages for reconnection
        self.running: bool = False
        self._task: asyncio.Task | None = None

    async def broadcast(self, message: dict):
        self.state.append(message)
        data = json.dumps(message)
        for ws in list(self.clients):
            try:
                await ws.send_text(data)
            except Exception:
                self.clients.discard(ws)

    # ... websocket_endpoint, start/stop/reset handlers, etc.
```

- [ ] **Step 2: Test server manually**

```bash
cd experiments/CHP-TETRIS-AI
python -m uvicorn server:app --port 8080
```

Open http://localhost:8080 — should serve dashboard/index.html (will be empty until Task 8).
Test WebSocket connection with browser console: `new WebSocket('ws://localhost:8080/ws')`

- [ ] **Step 3: Commit**

```bash
git add experiments/CHP-TETRIS-AI/server.py
git commit -m "feat(tetris): WebSocket server — Starlette + static files + broadcast"
```

---

### Task 8: Browser Dashboard

**Files:**
- Create: `experiments/CHP-TETRIS-AI/dashboard/index.html`
- Create: `experiments/CHP-TETRIS-AI/dashboard/style.css`
- Create: `experiments/CHP-TETRIS-AI/dashboard/app.js`

This task builds the mission control UI. Light theme. Six panels.

- [ ] **Step 1: Write index.html**

HTML shell with the grid layout (header, 6 panels, footer). References style.css and app.js. Contains:
- Header: title, turn counter, mode badge, live/demo indicator, speed controls, start/stop/reset buttons
- Left column: game canvas container + weights table
- Center top: score chart SVG container
- Center bottom: decision log container (scrollable)
- Right top: code panel (pre element with syntax highlighting)
- Right bottom: protocol health (gate bars, sigma seeds, stats)
- Footer: experiment path, improvement %, CHP version

- [ ] **Step 2: Write style.css**

Light theme:
- Background: `#f8f9fa` (light gray)
- Panel backgrounds: `#ffffff` with subtle border `#e0e0e0`
- Text: `#1a1a1a`
- Accent colors: green `#2e7d32` (pass/improve), red `#c62828` (fail/dead end), orange `#ef6c00` (warning/FP), blue `#1565c0` (info/turns)
- Monospace font for code and weights: `'Cascadia Code', 'Fira Code', monospace`
- Grid layout matching the mission control mockup
- Responsive to 1920x1080

- [ ] **Step 3: Write app.js — WebSocket connection + message routing**

```javascript
// Core WebSocket client
const ws = new WebSocket(`ws://${location.host}/ws`);
ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    handleMessage(msg);
};

function handleMessage(msg) {
    switch (msg.type) {
        // Turn lifecycle
        case 'turn_start': updateHeader(msg); break;
        case 'health_check': updateHealthCheck(msg); break;
        case 'council_result': updateCouncilResult(msg); break;
        case 'code_update': updateCodePanel(msg); break;
        case 'weights_update': updateWeightsPanel(msg); break;
        case 'game_results': updateScoreChart(msg); break;
        case 'sigma_gate': updateSigmaGate(msg); break;
        case 'critic_verdict': updateProtocolHealth(msg); break;
        case 'reviewer_verdict': updateReviewerVerdict(msg); break;
        case 'turn_complete': addLogEntry(msg); break;
        // Game replay
        case 'game_start': initGameReplay(msg); break;
        case 'game_move': renderGameMove(msg); break;
        case 'game_over': renderGameOver(msg); break;
        // Events
        case 'dead_end': addDeadEndEntry(msg); break;
        case 'false_positive': addFalsePositiveEntry(msg); break;
        case 'mode_change': updateMode(msg); break;
        case 'exit': handleExit(msg); break;
    }
}
```

- [ ] **Step 4: Write app.js — Game Canvas renderer**

Canvas-based 10x20 Tetris board renderer:
- Cell size calculated from container dimensions
- Color map for piece types (I=cyan, O=yellow, T=purple, S=green, Z=red, J=blue, L=orange)
- Grid lines
- Ghost piece (current piece drop preview) if available
- Smooth animation between moves

- [ ] **Step 5: Write app.js — Score Progression Chart**

SVG-based line chart:
- X axis: generation/turn number
- Y axis: average lines cleared
- Variance bands (mean ± std shown as semi-transparent fill)
- Dead end markers (red circles)
- False positive markers (orange circles)
- Current turn highlighted
- Axis labels and gridlines

- [ ] **Step 6: Write app.js — Decision Log panel**

Scrolling timeline:
- Each entry color-coded by type (green border = improvement, red = dead end, orange = false positive, gray = neutral)
- Shows turn number, strategy description, outcome
- Auto-scrolls to newest entry
- Typewriter effect for new entries

- [ ] **Step 7: Write app.js — Code Panel**

Displays the evaluate() function:
- Syntax highlighting (keywords purple, numbers orange, strings green)
- Diff highlighting: new lines get green background, removed lines get red
- Typewriter streaming effect for new code (characters appear sequentially)
- Line numbers

- [ ] **Step 8: Write app.js — Protocol Health panel**

- Gate score bars (1-4): horizontal progress bars with numeric labels
- Sigma gate: row of seed indicators (green check / red X)
- Mode badge: VALIDATION (blue) / EXPLORATION (amber)
- Stats: dead ends count, false positives caught, consecutive passes, total tokens
- CV value display

- [ ] **Step 9: Write app.js — Header controls**

- Start/Stop/Reset buttons wired to server `/api/start`, `/api/stop`, `/api/reset`
- Demo/Live toggle
- Speed selector (1x / 5x / 20x) wired to `/api/speed`
- Auto-reconnect on WebSocket disconnect (2-second interval)

- [ ] **Step 10: Manual test**

Start server and verify:
1. Dashboard loads with empty state
2. WebSocket connects (check browser console)
3. All 6 panels render their empty/default states
4. Buttons are clickable and send requests

- [ ] **Step 11: Commit**

```bash
git add experiments/CHP-TETRIS-AI/dashboard/
git commit -m "feat(tetris): mission control dashboard — light theme, 6 panels, WebSocket client"
```

---

### Task 9: CLI Integration & Dependencies

**Files:**
- Modify: `context_hacking/cli.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Add [tetris] optional dependencies to pyproject.toml**

Add to `[project.optional-dependencies]`:
```toml
tetris = [
    "starlette>=0.37",
    "uvicorn>=0.29",
    "websockets>=12.0",
]
```

Update the `all` group to include `tetris`.

- [ ] **Step 2: Add --dashboard flag to chp run**

In `context_hacking/cli.py`, modify the `run` command to accept `--dashboard`:

```python
@main.command()
@click.option("--experiment", default=None,
              help="Run a specific experiment")
@click.option("--method", type=click.Choice(["auto", "claude-cli", "api", "interactive"]),
              default="auto", help="Execution method")
@click.option("--all-experiments", is_flag=True,
              help="Run all 9 built-in experiments")
@click.option("--dashboard", is_flag=True,
              help="Launch live WebSocket dashboard (for CHP-TETRIS-AI)")
def run(experiment, method, all_experiments, dashboard):
```

When `--dashboard` is True and experiment is "CHP-TETRIS-AI":
- Import and start the Starlette server from the experiment's server.py
- Open the browser to `http://localhost:{port}`
- Run the server (blocking)

- [ ] **Step 3: Install and test**

```bash
pip install -e ".[tetris]"
chp run --experiment CHP-TETRIS-AI --dashboard
```

Expected: Server starts, browser opens to dashboard.

- [ ] **Step 4: Commit**

```bash
git add context_hacking/cli.py pyproject.toml
git commit -m "feat(tetris): add --dashboard flag to CLI + [tetris] dependencies"
```

---

### Task 10: Demo Mode — Recording & Playback

**Files:**
- Modify: `experiments/CHP-TETRIS-AI/server.py`
- Modify: `experiments/CHP-TETRIS-AI/optimizer.py`

- [ ] **Step 1: Add recording to optimizer**

Every `broadcast_fn` call in the optimizer also appends the message (with a `timestamp` field) to a list. After the loop finishes, write the list to `run_history.json`.

```python
import time

class RunRecorder:
    def __init__(self):
        self.messages: list[dict] = []
        self._start = time.time()

    def record(self, message: dict) -> dict:
        message["_timestamp"] = time.time() - self._start
        self.messages.append(message)
        return message

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.messages, f, indent=2)
```

- [ ] **Step 2: Add playback to server**

```python
async def start_demo_mode(self, history_path: str, speed: float = 5.0):
    with open(history_path) as f:
        messages = json.load(f)
    for msg in messages:
        if not self.running:
            break
        delay = msg.get("_timestamp", 0) / speed
        await asyncio.sleep(max(delay - self._elapsed, 0))
        await self.broadcast(msg)
```

- [ ] **Step 3: Manual test**

1. Run a live session (even a short one — 2-3 turns)
2. Verify `run_history.json` is created with timestamped messages
3. Switch to demo mode
4. Verify dashboard replays the same sequence

- [ ] **Step 4: Commit**

```bash
git add experiments/CHP-TETRIS-AI/server.py experiments/CHP-TETRIS-AI/optimizer.py
git commit -m "feat(tetris): demo mode — run history recording and playback"
```

---

### Task 11: End-to-End Integration Test

**Files:**
- Create: `experiments/CHP-TETRIS-AI/tests/test_integration.py`

- [ ] **Step 1: Write integration test**

Tests the full flow without real API calls:

```python
import asyncio
import json
import pytest
from unittest.mock import AsyncMock, patch

class TestEndToEnd:
    @pytest.mark.asyncio
    async def test_single_turn_produces_messages(self):
        """A single optimizer turn broadcasts the expected message sequence."""
        from optimizer import run_turn, TurnState
        messages = []
        async def mock_broadcast(msg):
            messages.append(msg)

        # Mock the API call to return a valid weight proposal
        mock_response = json.dumps({
            "aggregate_height": -2.0, "complete_lines": 1.5,
            "holes": -3.0, "bumpiness": -1.5,
            "well_depth": 0.0, "tetris_readiness": 0.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        })
        with patch("optimizer.call_anthropic", new=AsyncMock(return_value=mock_response)):
            state = TurnState.initial("config.yaml")
            result = await run_turn(state, broadcast_fn=mock_broadcast)

        # Verify message sequence
        types = [m["type"] for m in messages]
        assert "turn_start" in types
        assert "weights_update" in types
        assert "game_results" in types
        assert "sigma_gate" in types
        assert "turn_complete" in types

    def test_engine_performance(self):
        """10 games must complete in under 5 seconds."""
        import time
        from frozen.tetris_engine import play_game
        from composition import build_evaluate_fn

        weights = {
            "aggregate_height": -3.0, "complete_lines": 1.5,
            "holes": -4.5, "bumpiness": -2.0,
            "well_depth": 0.5, "tetris_readiness": 2.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        evaluate_fn = build_evaluate_fn(weights)

        start = time.time()
        for seed in range(10):
            play_game(evaluate_fn, seed=seed)
        elapsed = time.time() - start

        assert elapsed < 5.0, f"10 games took {elapsed:.1f}s, must be < 5s"

    def test_full_data_roundtrip(self):
        """Weights -> evaluate -> play_game -> score is deterministic."""
        from composition import build_evaluate_fn
        from frozen.tetris_engine import play_game

        weights = {
            "aggregate_height": -3.0, "complete_lines": 1.5,
            "holes": -4.5, "bumpiness": -2.0,
            "well_depth": 0.0, "tetris_readiness": 0.0,
            "column_transitions": 0.0, "row_transitions": 0.0,
        }
        fn = build_evaluate_fn(weights)
        r1 = play_game(fn, seed=42)
        r2 = play_game(fn, seed=42)
        assert r1.lines_cleared == r2.lines_cleared
        assert r1.score == r2.score
```

- [ ] **Step 2: Run integration tests**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/test_integration.py -v
```

Expected: All pass (API tests use mocks, performance test uses real engine).

- [ ] **Step 3: Run full test suite**

```bash
python -m pytest experiments/CHP-TETRIS-AI/tests/ -v
```

Expected: All tests across all test files pass.

- [ ] **Step 4: Commit**

```bash
git add experiments/CHP-TETRIS-AI/tests/test_integration.py
git commit -m "test(tetris): end-to-end integration tests — full turn cycle + performance"
```

---

### Task 12: Golden Run & Polish

**Files:**
- Create: `experiments/CHP-TETRIS-AI/run_history.json` (generated)
- Create: `experiments/CHP-TETRIS-AI/REPORT.md` (generated)

- [ ] **Step 1: Run a full live session**

```bash
export ANTHROPIC_API_KEY=<your key>
chp run --experiment CHP-TETRIS-AI --dashboard
```

Run in live mode for 15-20 turns. Watch for:
- Score progression (should climb from ~500 to 5,000+)
- Trap detection (line-clear greed should be caught in turns 1-3)
- At least 1 dead end logged
- At least 1 sigma gate catch
- Mode switching (should enter EXPLORATION if stuck)

- [ ] **Step 2: Save the golden run**

The optimizer automatically saves `run_history.json` after completion. Verify it exists and contains all message types.

- [ ] **Step 3: Test demo mode**

Restart with demo mode. Verify the full replay works in the dashboard at 1x and 20x speed.

- [ ] **Step 4: Write REPORT.md**

Document the results:
- Final best score vs baseline
- Number of turns to convergence
- Traps detected
- Dead ends logged
- Gate scores across all turns
- Screenshot references

- [ ] **Step 5: Update metadata.json**

Fill in actual results:
```json
{
  "status": "complete",
  "key_result": "Baseline 512 → Best 48,230 lines (94x improvement)",
  "false_positives_caught": 1,
  "turns": 18
}
```

- [ ] **Step 6: Final commit**

```bash
git add experiments/CHP-TETRIS-AI/
git commit -m "feat(tetris): CHP-TETRIS-AI complete — golden run + demo mode + report"
```
