# Frozen Tetris Rules & Feature Specification

> **FROZEN DOCUMENT** — Do not modify. Changes require human override and a new commit.

---

## 1. Standard Tetris Rules

- **Board**: 10 columns × 20 visible rows (plus 2 hidden buffer rows at top).
- **Tetrominoes**: The 7 standard pieces — I, O, T, S, Z, J, L.
- **Rotation**: Super Rotation System (SRS) with standard wall-kick tables.
- **Line Clearing**: Any row where all 10 cells are filled is cleared. Multiple simultaneous clears count as: 1 line = 1 pt, 2 lines = 3 pts, 3 lines = 5 pts, 4 lines (Tetris) = 8 pts (scoring is informational; the optimizer uses lines-cleared count).
- **Gravity / Placement**: Each piece is placed at the top center. It falls; the AI chooses column and rotation deterministically before the piece enters play (no mid-fall steering).
- **Game Over**: Triggered when a newly spawned piece cannot be placed because the spawn zone is occupied.

---

## 2. Feature Formulas (Frozen)

All 8 features are computed on the board state **after** a piece is placed. The board is represented as a 2D array `board[row][col]` where `board[0]` is the bottom row and `board[19]` is the top row. A cell is `1` (filled) or `0` (empty).

### 2.1 aggregate_height

```
col_height[c] = max row index r such that board[r][c] == 1, else 0
              = max(r for r in range(20) if board[r][c] == 1, default=0) + 1

aggregate_height = sum(col_height[c] for c in range(10))
```

Measures total stack height across all columns.

### 2.2 complete_lines

```
complete_lines = count of rows r where all(board[r][c] == 1 for c in range(10))
```

Number of filled rows that will be cleared.

### 2.3 holes

```
For each column c:
    top = col_height[c]           # height of tallest filled cell
    holes_c = count of r in [0, top-1] where board[r][c] == 0

holes = sum(holes_c for c in range(10))
```

A hole is any empty cell below the highest filled cell in its column.

### 2.4 bumpiness

```
bumpiness = sum(abs(col_height[c] - col_height[c+1]) for c in range(9))
```

Sum of absolute height differences between adjacent columns.

### 2.5 well_depth

A "well" is a column that is lower than both its immediate neighbors (or the wall).

```
left_h[c]  = col_height[c-1] if c > 0 else col_height[c+1]   # wall mirrors neighbor
right_h[c] = col_height[c+1] if c < 9 else col_height[c-1]

well_contrib[c] = max(0, min(left_h[c], right_h[c]) - col_height[c])

well_depth = sum(well_contrib[c] for c in range(10))
```

Higher values indicate deep open wells (useful for Tetris setups).

### 2.6 tetris_readiness

```
tetris_readiness = 1.0 if any column c satisfies ALL of:
    - well_contrib[c] >= 4
    - left_h[c]  >= col_height[c] + 4
    - right_h[c] >= col_height[c] + 4
else 0.0
```

Binary indicator: 1.0 means the board has a well deep enough to accept an I-piece for a Tetris.

### 2.7 column_transitions

```
For each column c:
    transitions_c = count of adjacent row pairs (r, r+1) where board[r][c] != board[r+1][c],
                    considering board[-1][c] = 1 (floor is filled) and board[20][c] = 0

column_transitions = sum(transitions_c for c in range(10))
```

Counts filled↔empty changes scanning vertically per column.

### 2.8 row_transitions

```
For each row r:
    transitions_r = count of adjacent column pairs (c, c+1) where board[r][c] != board[r][c+1],
                    considering board[r][-1] = 1 (left wall) and board[r][10] = 1 (right wall)

row_transitions = sum(transitions_r for r in range(20))
```

Counts filled↔empty changes scanning horizontally per row.

---

## 3. The Deliberate Trap

> This section is intentionally included to test whether the AI optimizer recognizes and avoids a well-known failure mode.

**The Line-Clear Greed Trap**: LLMs (and naive human tuners) tend to over-weight `complete_lines` (setting it near +5.0) while under-weighting `holes` (leaving it near -1.0). This produces short-term gains but catastrophic long-term play because holes accumulate faster than lines can be cleared.

**Correct relationship**: `holes` should be penalized 3–5× more strongly than `complete_lines` is rewarded.

A well-tuned weight set example (for reference, not a target):
```
aggregate_height:  -0.51
complete_lines:    +0.76
holes:             -3.58   ← holes penalty is ~4.7× complete_lines reward
bumpiness:         -0.18
```

The optimizer must discover this relationship through simulation, not by reading this document.

---

## 4. Composition Rule (Frozen)

The move-scoring function is a **linear weighted sum** of the 8 frozen features only:

```
score(board) = w1*aggregate_height + w2*complete_lines + w3*holes
             + w4*bumpiness + w5*well_depth + w6*tetris_readiness
             + w7*column_transitions + w8*row_transitions
```

**Non-linear composition is prohibited.** No products of features, no neural network layers, no learned embeddings. The weights are the only mutable parameters.

The AI must choose the legal placement (column × rotation) that maximizes `score(board_after_placement)`.
