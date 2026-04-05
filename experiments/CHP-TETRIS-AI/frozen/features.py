"""Frozen feature functions for CHP-TETRIS-AI.

Each function takes a numpy ndarray of shape (20, 10) with dtype int8 and
returns a float. The board convention is row 0 = top, row 19 = bottom.
0 = empty; 1-7 = piece type.

These functions are FROZEN — the CHP loop must not modify them.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _column_heights(grid: np.ndarray) -> np.ndarray:
    """Return an array of shape (10,) with the height of each column.

    Height = 20 - (index of the topmost nonzero row).
    Returns 0 for an empty column.
    """
    # nonzero() returns (row_indices, col_indices) for all filled cells.
    # We want the minimum row index per column (= topmost filled cell).
    heights = np.zeros(10, dtype=np.int32)
    for c in range(10):
        col = grid[:, c]
        filled = np.nonzero(col)[0]
        if filled.size > 0:
            heights[c] = 20 - filled[0]
    return heights


# ---------------------------------------------------------------------------
# Feature 1 — aggregate_height
# ---------------------------------------------------------------------------


def aggregate_height(grid: np.ndarray) -> float:
    """Sum of all column heights."""
    return float(_column_heights(grid).sum())


# ---------------------------------------------------------------------------
# Feature 2 — complete_lines
# ---------------------------------------------------------------------------


def complete_lines(grid: np.ndarray) -> float:
    """Count of rows where every cell is nonzero."""
    return float(np.count_nonzero(np.all(grid != 0, axis=1)))


# ---------------------------------------------------------------------------
# Feature 3 — holes
# ---------------------------------------------------------------------------


def holes(grid: np.ndarray) -> float:
    """Count empty cells that have at least one filled cell above them."""
    total = 0
    for c in range(10):
        col = grid[:, c]
        filled = np.nonzero(col)[0]
        if filled.size == 0:
            continue
        top = filled[0]
        # Count zeros from the topmost filled cell down to row 19
        total += int(np.count_nonzero(col[top:] == 0))
    return float(total)


# ---------------------------------------------------------------------------
# Feature 4 — bumpiness
# ---------------------------------------------------------------------------


def bumpiness(grid: np.ndarray) -> float:
    """Sum of absolute height differences between adjacent columns."""
    h = _column_heights(grid)
    return float(np.sum(np.abs(np.diff(h))))


# ---------------------------------------------------------------------------
# Feature 5 — well_depth
# ---------------------------------------------------------------------------


def well_depth(grid: np.ndarray) -> float:
    """Sum of well depths across all columns.

    For a column i, the well depth is max(0, min_neighbor_height - h[i]),
    where the "neighbors" for edge columns are only the single adjacent
    column (one-sided well).
    """
    h = _column_heights(grid).astype(np.float64)
    total = 0.0

    # Left edge: col 0 — only right neighbor
    depth_0 = h[1] - h[0]
    if depth_0 > 0:
        total += depth_0

    # Interior columns: cols 1-8
    for i in range(1, 9):
        depth = min(h[i - 1], h[i + 1]) - h[i]
        if depth > 0:
            total += depth

    # Right edge: col 9 — only left neighbor
    depth_9 = h[8] - h[9]
    if depth_9 > 0:
        total += depth_9

    return float(total)


# ---------------------------------------------------------------------------
# Feature 6 — tetris_readiness
# ---------------------------------------------------------------------------


def tetris_readiness(grid: np.ndarray) -> float:
    """1.0 if any column has a well depth >= 4, else 0.0."""
    h = _column_heights(grid).astype(np.float64)

    # Left edge
    if h[1] - h[0] >= 4:
        return 1.0

    # Interior
    for i in range(1, 9):
        if min(h[i - 1], h[i + 1]) - h[i] >= 4:
            return 1.0

    # Right edge
    if h[8] - h[9] >= 4:
        return 1.0

    return 0.0


# ---------------------------------------------------------------------------
# Feature 7 — column_transitions
# ---------------------------------------------------------------------------


def column_transitions(grid: np.ndarray) -> float:
    """Count filled/empty transitions within each column's occupied region.

    For each column, the occupied region spans from the topmost filled cell
    down to row 19.  A transition is counted each time adjacant cells differ
    in their filled/empty status.
    """
    total = 0
    for c in range(10):
        col = grid[:, c]
        filled = np.nonzero(col)[0]
        if filled.size == 0:
            continue
        top = filled[0]
        region = (col[top:] != 0).astype(np.int8)
        total += int(np.sum(np.abs(np.diff(region))))
    return float(total)


# ---------------------------------------------------------------------------
# Feature 8 — row_transitions
# ---------------------------------------------------------------------------


def row_transitions(grid: np.ndarray) -> float:
    """Count filled/empty transitions in each row that has at least one cell.

    Edges are treated as filled (i.e., a virtual filled cell exists to the
    left of col 0 and to the right of col 9).  Only rows with at least one
    filled cell are counted.
    """
    total = 0
    for r in range(20):
        row = grid[r, :]
        if not np.any(row != 0):
            continue
        # Pad with 1s on both sides to represent the walls
        padded = np.empty(12, dtype=np.int8)
        padded[0] = 1
        padded[1:11] = (row != 0).astype(np.int8)
        padded[11] = 1
        total += int(np.sum(np.abs(np.diff(padded))))
    return float(total)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

FEATURE_NAMES: list[str] = [
    "aggregate_height",
    "complete_lines",
    "holes",
    "bumpiness",
    "well_depth",
    "tetris_readiness",
    "column_transitions",
    "row_transitions",
]

FEATURE_FNS: dict[str, Callable] = {
    "aggregate_height": aggregate_height,
    "complete_lines": complete_lines,
    "holes": holes,
    "bumpiness": bumpiness,
    "well_depth": well_depth,
    "tetris_readiness": tetris_readiness,
    "column_transitions": column_transitions,
    "row_transitions": row_transitions,
}
