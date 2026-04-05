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


_ch_cache_hash: bytes = b""
_ch_cache_val: np.ndarray = np.zeros(10, dtype=np.int32)


def _column_heights(grid: np.ndarray) -> np.ndarray:
    """Return an array of shape (10,) with the height of each column.

    Height = 20 - (index of the topmost nonzero row).
    Returns 0 for an empty column.

    Results are cached per grid content so that multiple features
    evaluating the same board avoid redundant computation.
    """
    global _ch_cache_hash, _ch_cache_val
    ghash = grid.data.tobytes()
    if ghash == _ch_cache_hash:
        return _ch_cache_val

    heights = np.zeros(10, dtype=np.int32)
    for c in range(10):
        for r in range(20):
            if grid[r, c] != 0:
                heights[c] = 20 - r
                break
    _ch_cache_hash = ghash
    _ch_cache_val = heights
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
        found_top = False
        col_holes = 0
        for r in range(20):
            if grid[r, c] != 0:
                found_top = True
            elif found_top:
                col_holes += 1
        total += col_holes
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
        # Find topmost filled cell
        top = -1
        for r in range(20):
            if grid[r, c] != 0:
                top = r
                break
        if top < 0:
            continue
        # Count transitions from top to bottom
        prev_filled = True  # first cell is filled by definition
        for r in range(top + 1, 20):
            cur_filled = grid[r, c] != 0
            if cur_filled != prev_filled:
                total += 1
            prev_filled = cur_filled
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
        row = grid[r]
        # Quick check: skip empty rows
        has_any = False
        for c in range(10):
            if row[c] != 0:
                has_any = True
                break
        if not has_any:
            continue
        # Left wall (filled) -> col 0
        prev = True  # wall is filled
        for c in range(10):
            cur = row[c] != 0
            if cur != prev:
                total += 1
            prev = cur
        # col 9 -> right wall (filled)
        if not prev:
            total += 1
    return float(total)


# ---------------------------------------------------------------------------
# Fast single-pass evaluation
# ---------------------------------------------------------------------------


_ZERO = b'\x00'


def evaluate_all(
    grid: np.ndarray,
    need_col_trans: bool = True,
    need_row_trans: bool = True,
) -> dict[str, float]:
    """Compute all 8 features using fast bytes operations.

    Uses ``grid.tobytes()`` and bytes methods (lstrip, count) for
    C-speed column processing, then a flat-bytes scan for row features.
    Returns a dict mapping feature name -> float value.

    If *need_col_trans* or *need_row_trans* is False, those features
    are returned as 0.0 but not computed (saving ~20% of time).
    """
    flat = grid.tobytes()

    # --- Column features: heights, holes, column_transitions ---
    total_holes = 0
    total_col_trans = 0
    h = [0] * 10

    if need_col_trans:
        for c in range(10):
            col = flat[c::10]  # 20-byte column slice (C-speed)
            stripped = col.lstrip(_ZERO)
            sz = len(stripped)
            if not sz:
                continue
            h[c] = sz
            total_holes += stripped.count(0)
            prev = 1
            for i in range(1, sz):
                cur = 1 if stripped[i] else 0
                if cur != prev:
                    total_col_trans += 1
                prev = cur
    else:
        for c in range(10):
            col = flat[c::10]
            stripped = col.lstrip(_ZERO)
            sz = len(stripped)
            if not sz:
                continue
            h[c] = sz
            total_holes += stripped.count(0)

    # --- Derived from heights ---
    h0 = h[0]; h1 = h[1]; h2 = h[2]; h3 = h[3]; h4 = h[4]
    h5 = h[5]; h6 = h[6]; h7 = h[7]; h8 = h[8]; h9 = h[9]

    agg_height = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9

    # bumpiness
    d01 = h0 - h1; d12 = h1 - h2; d23 = h2 - h3
    d34 = h3 - h4; d45 = h4 - h5; d56 = h5 - h6
    d67 = h6 - h7; d78 = h7 - h8; d89 = h8 - h9
    bump = ((d01 if d01 > 0 else -d01) + (d12 if d12 > 0 else -d12)
            + (d23 if d23 > 0 else -d23) + (d34 if d34 > 0 else -d34)
            + (d45 if d45 > 0 else -d45) + (d56 if d56 > 0 else -d56)
            + (d67 if d67 > 0 else -d67) + (d78 if d78 > 0 else -d78)
            + (d89 if d89 > 0 else -d89))

    # well_depth and tetris_readiness (fully unrolled)
    total_well = 0.0
    has_tetris = False

    dw = h1 - h0
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h0 if h0 < h2 else h2) - h1
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h1 if h1 < h3 else h3) - h2
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h2 if h2 < h4 else h4) - h3
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h3 if h3 < h5 else h5) - h4
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h4 if h4 < h6 else h6) - h5
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h5 if h5 < h7 else h7) - h6
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h6 if h6 < h8 else h8) - h7
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = (h7 if h7 < h9 else h9) - h8
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True
    dw = h8 - h9
    if dw > 0:
        total_well += dw
    if dw >= 4:
        has_tetris = True

    # --- Row features: complete_lines, row_transitions ---
    total_complete = 0
    total_row_trans = 0

    if need_row_trans:
        for r in range(20):
            base = r * 10
            row_bytes = flat[base:base + 10]
            nz = 10 - row_bytes.count(0)
            if nz == 10:
                total_complete += 1
            elif nz == 0:
                continue

            c0 = row_bytes[0]; c1 = row_bytes[1]; c2 = row_bytes[2]
            c3 = row_bytes[3]; c4 = row_bytes[4]; c5 = row_bytes[5]
            c6 = row_bytes[6]; c7 = row_bytes[7]; c8 = row_bytes[8]
            c9 = row_bytes[9]
            rt = 0
            if not c0:
                rt += 1
            if bool(c0) != bool(c1):
                rt += 1
            if bool(c1) != bool(c2):
                rt += 1
            if bool(c2) != bool(c3):
                rt += 1
            if bool(c3) != bool(c4):
                rt += 1
            if bool(c4) != bool(c5):
                rt += 1
            if bool(c5) != bool(c6):
                rt += 1
            if bool(c6) != bool(c7):
                rt += 1
            if bool(c7) != bool(c8):
                rt += 1
            if bool(c8) != bool(c9):
                rt += 1
            if not c9:
                rt += 1
            total_row_trans += rt
    else:
        for r in range(20):
            base = r * 10
            row_bytes = flat[base:base + 10]
            if row_bytes.count(0) == 0:
                total_complete += 1

    return {
        "aggregate_height": float(agg_height),
        "complete_lines": float(total_complete),
        "holes": float(total_holes),
        "bumpiness": float(bump),
        "well_depth": float(total_well),
        "tetris_readiness": 1.0 if has_tetris else 0.0,
        "column_transitions": float(total_col_trans),
        "row_transitions": float(total_row_trans),
    }


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
