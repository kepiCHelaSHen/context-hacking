"""Frozen Tetris engine — immutable core for CHP-TETRIS-AI.

This module must never be modified by the CHP optimization loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np


# ---------------------------------------------------------------------------
# Piece & TETROMINOES
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Piece:
    name: str
    rotations: list  # list[np.ndarray]  (each 2-D, nonzero = filled)
    piece_id: int


def _a(rows: list[list[int]]) -> np.ndarray:
    """Shorthand: build an int8 ndarray from nested lists."""
    return np.array(rows, dtype=np.int8)


TETROMINOES: dict[str, Piece] = {
    # --- I (id=1) — 4 rotations (horizontal & vertical repeat) ---
    "I": Piece("I", [
        _a([[1, 1, 1, 1]]),                      # 0°  (1×4)
        _a([[1], [1], [1], [1]]),                 # 90° (4×1)
        _a([[1, 1, 1, 1]]),                      # 180°
        _a([[1], [1], [1], [1]]),                 # 270°
    ], piece_id=1),

    # --- O (id=2) — 4 identical rotations ---
    "O": Piece("O", [
        _a([[1, 1], [1, 1]]),
        _a([[1, 1], [1, 1]]),
        _a([[1, 1], [1, 1]]),
        _a([[1, 1], [1, 1]]),
    ], piece_id=2),

    # --- T (id=3) — 4 SRS rotations ---
    "T": Piece("T", [
        _a([[0, 1, 0],
            [1, 1, 1]]),     # 0°
        _a([[1, 0],
            [1, 1],
            [1, 0]]),        # 90° (R)
        _a([[1, 1, 1],
            [0, 1, 0]]),     # 180°
        _a([[0, 1],
            [1, 1],
            [0, 1]]),        # 270° (L)
    ], piece_id=3),

    # --- S (id=4) — 2 unique, repeated for 4 ---
    "S": Piece("S", [
        _a([[0, 1, 1],
            [1, 1, 0]]),     # 0°
        _a([[1, 0],
            [1, 1],
            [0, 1]]),        # 90°
        _a([[0, 1, 1],
            [1, 1, 0]]),     # 180°
        _a([[1, 0],
            [1, 1],
            [0, 1]]),        # 270°
    ], piece_id=4),

    # --- Z (id=5) — 2 unique, repeated for 4 ---
    "Z": Piece("Z", [
        _a([[1, 1, 0],
            [0, 1, 1]]),     # 0°
        _a([[0, 1],
            [1, 1],
            [1, 0]]),        # 90°
        _a([[1, 1, 0],
            [0, 1, 1]]),     # 180°
        _a([[0, 1],
            [1, 1],
            [1, 0]]),        # 270°
    ], piece_id=5),

    # --- J (id=6) — 4 SRS rotations ---
    "J": Piece("J", [
        _a([[1, 0, 0],
            [1, 1, 1]]),     # 0°
        _a([[1, 1],
            [1, 0],
            [1, 0]]),        # 90°
        _a([[1, 1, 1],
            [0, 0, 1]]),     # 180°
        _a([[0, 1],
            [0, 1],
            [1, 1]]),        # 270°
    ], piece_id=6),

    # --- L (id=7) — 4 SRS rotations ---
    "L": Piece("L", [
        _a([[0, 0, 1],
            [1, 1, 1]]),     # 0°
        _a([[1, 0],
            [1, 0],
            [1, 1]]),        # 90°
        _a([[1, 1, 1],
            [1, 0, 0]]),     # 180°
        _a([[1, 1],
            [0, 1],
            [0, 1]]),        # 270°
    ], piece_id=7),
}


# ---------------------------------------------------------------------------
# Pre-compute unique rotation indices for each piece to skip duplicates
# ---------------------------------------------------------------------------

_UNIQUE_ROTATIONS: dict[str, list[int]] = {}

def _init_unique_rotations() -> None:
    for name, piece in TETROMINOES.items():
        seen: list[int] = []
        seen_keys: list[tuple[tuple[int, ...], bytes]] = []
        for i, rot in enumerate(piece.rotations):
            key = (rot.shape, rot.tobytes())
            if key not in seen_keys:
                seen_keys.append(key)
                seen.append(i)
        _UNIQUE_ROTATIONS[name] = seen

_init_unique_rotations()


# ---------------------------------------------------------------------------
# Pre-compute filled cell offsets for each rotation (used for fast drop)
# ---------------------------------------------------------------------------

def _precompute_piece_cells() -> (
    dict[str, list[tuple[int, int, list[tuple[int, int]], dict[int, int]]]]
):
    """For each piece, for each unique rotation, compute:
    - pr, pc: shape rows, cols
    - cells: list of (dr, dc) offsets where the piece is filled
    - col_bottoms: {dc: max_dr} — the lowest filled row in each column of the shape
    """
    result: dict[str, list[tuple[int, int, list[tuple[int, int]], dict[int, int]]]] = {}
    for name, piece in TETROMINOES.items():
        entries = []
        for rot_idx in _UNIQUE_ROTATIONS[name]:
            shape = piece.rotations[rot_idx]
            pr, pc = shape.shape
            cells: list[tuple[int, int]] = []
            col_bottoms: dict[int, int] = {}
            for dr in range(pr):
                for dc in range(pc):
                    if shape[dr, dc] != 0:
                        cells.append((dr, dc))
                        if dc not in col_bottoms or dr > col_bottoms[dc]:
                            col_bottoms[dc] = dr
            entries.append((rot_idx, pr, pc, cells, col_bottoms))
        result[name] = entries
    return result

_PIECE_DATA = _precompute_piece_cells()


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------

class Board:
    """20×10 Tetris board.  Row 0 is the top; row 19 is the bottom."""

    __slots__ = ("_grid", "_col_heights")

    ROWS = 20
    COLS = 10

    def __init__(self, grid: np.ndarray | None = None) -> None:
        if grid is not None:
            self._grid = grid
        else:
            self._grid = np.zeros((self.ROWS, self.COLS), dtype=np.int8)
        self._col_heights: np.ndarray | None = None

    # -- properties ----------------------------------------------------------

    @property
    def grid(self) -> np.ndarray:
        return self._grid

    # -- column height cache -------------------------------------------------

    def _get_col_heights(self) -> np.ndarray:
        """Return cached column heights (height = ROWS - topmost_filled_row)."""
        if self._col_heights is None:
            self._col_heights = self._compute_col_heights()
        return self._col_heights

    def _compute_col_heights(self) -> np.ndarray:
        heights = np.zeros(self.COLS, dtype=np.int32)
        grid = self._grid
        for c in range(self.COLS):
            for r in range(self.ROWS):
                if grid[r, c] != 0:
                    heights[c] = self.ROWS - r
                    break
        return heights

    def _invalidate_heights(self) -> None:
        self._col_heights = None

    # -- mutation ------------------------------------------------------------

    def place_piece(self, piece: Piece, rotation: int, row: int, col: int) -> bool:
        """Place *piece* at (*row*, *col*).  Return True on success."""
        shape = piece.rotations[rotation]
        pr, pc = shape.shape

        # bounds check
        if row < 0 or col < 0 or row + pr > self.ROWS or col + pc > self.COLS:
            return False

        # collision check
        region = self._grid[row:row + pr, col:col + pc]
        mask = shape != 0
        if np.any(region[mask] != 0):
            return False

        # place
        region[mask] = piece.piece_id
        self._invalidate_heights()
        return True

    def clear_lines(self) -> int:
        """Remove complete rows, shift everything above down.  Return count."""
        full = np.all(self._grid != 0, axis=1)
        n_full = int(np.sum(full))
        if n_full == 0:
            return 0
        keep = self._grid[~full]
        # prepend empty rows at top
        empty = np.zeros((n_full, self.COLS), dtype=np.int8)
        self._grid = np.vstack([empty, keep])
        self._invalidate_heights()
        return n_full

    def is_game_over(self) -> bool:
        return bool(np.any(self._grid[0] != 0))

    def copy(self) -> Board:
        return Board(self._grid.copy())

    def max_height(self) -> int:
        """Height of the tallest column (measured from the bottom)."""
        filled_rows = np.any(self._grid != 0, axis=1)
        if not np.any(filled_rows):
            return 0
        top_filled_row = int(np.argmax(filled_rows))  # first True from top
        return self.ROWS - top_filled_row

    def get_legal_moves(self, piece: Piece) -> list[tuple[int, int, int]]:
        """Return all valid (rotation, row, col) drop placements.

        Uses column heights for fast O(1) drop calculation per move,
        and deduplicates rotations for symmetric pieces.
        """
        moves: list[tuple[int, int, int]] = []
        grid = self._grid
        col_heights = self._get_col_heights()
        ROWS = self.ROWS
        COLS = self.COLS

        for rot_idx, pr, pc, cells, col_bottoms in _PIECE_DATA[piece.name]:
            for col in range(COLS - pc + 1):
                # For each column dc in the piece shape, find the highest
                # row the piece can reach. The piece's bottom cell in column
                # dc is at row (drop_row + col_bottoms[dc]). This must land
                # on top of the existing column at (col + dc).
                # So: drop_row + col_bottoms[dc] <= ROWS - 1 - col_heights[col + dc]
                # => drop_row <= (ROWS - 1 - col_heights[col+dc]) - col_bottoms[dc]
                # But it can also sit ON existing pieces, so the constraint is
                # the piece cell must land at or above the first occupied row.
                # The first occupied row in column (col+dc) is at
                # ROWS - col_heights[col+dc].
                # The piece fills row (drop_row + bottom_dr). This must be
                # strictly above the first occupied row OR on an empty column.
                # So: drop_row + bottom_dr < ROWS - col_heights[col+dc]
                # Which gives: drop_row < ROWS - col_heights[col+dc] - bottom_dr
                # => drop_row <= ROWS - col_heights[col+dc] - bottom_dr - 1
                best_row = ROWS  # will take min over all piece columns
                for dc, bottom_dr in col_bottoms.items():
                    # The piece's bottom cell in this column lands at
                    # (drop_row + bottom_dr). It must be < first_occupied_row
                    # of the board column (col + dc), unless column is empty.
                    h = col_heights[col + dc]
                    first_occupied = ROWS - h  # row index of first filled cell (ROWS if empty)
                    # Piece cell at (drop_row + bottom_dr) must be < first_occupied
                    # So drop_row must be <= first_occupied - bottom_dr - 1
                    max_row = first_occupied - bottom_dr - 1
                    if max_row < best_row:
                        best_row = max_row

                if best_row < 0:
                    continue  # can't place

                # Clamp: piece must fit within the board (top edge)
                if best_row + pr > ROWS:
                    best_row = ROWS - pr

                # Verify: no collision (needed for complex shapes where
                # the height-based calculation may not account for overhangs).
                ok = True
                for dr, dc in cells:
                    if grid[best_row + dr, col + dc] != 0:
                        ok = False
                        break
                if ok:
                    moves.append((rot_idx, best_row, col))
        return moves


# ---------------------------------------------------------------------------
# PieceGenerator  (7-bag randomiser)
# ---------------------------------------------------------------------------

class PieceGenerator:
    _PIECE_NAMES = ["I", "O", "T", "S", "Z", "J", "L"]

    def __init__(self, seed: int) -> None:
        self._rng = np.random.default_rng(seed)
        self._bag: list[str] = []

    def _refill(self) -> None:
        bag = list(self._PIECE_NAMES)
        self._rng.shuffle(bag)
        self._bag = bag

    def next(self) -> Piece:
        if not self._bag:
            self._refill()
        return TETROMINOES[self._bag.pop()]


# ---------------------------------------------------------------------------
# GameResult
# ---------------------------------------------------------------------------

@dataclass
class GameResult:
    lines_cleared: int
    pieces_placed: int
    score: int
    move_history: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scoring helper
# ---------------------------------------------------------------------------

_LINE_SCORE = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}


# ---------------------------------------------------------------------------
# play_game
# ---------------------------------------------------------------------------

def play_game(
    evaluate_fn: Callable[[np.ndarray], float],
    seed: int,
) -> GameResult:
    """Run a complete Tetris game and return the result.

    Parameters
    ----------
    evaluate_fn : callable
        Accepts a (20, 10) int8 grid, returns a float score.
        Higher is better.
    seed : int
        Seed for the piece generator (deterministic replay).
    """
    board = Board()
    gen = PieceGenerator(seed)

    total_lines = 0
    total_score = 0
    pieces_placed = 0
    history: list[dict] = []

    ROWS = Board.ROWS
    COLS = Board.COLS

    while True:
        piece = gen.next()
        moves = board.get_legal_moves(piece)

        if not moves:
            # No legal placement — game over
            break

        # Evaluate every move, pick the best — using in-place place/undo
        best_val = -np.inf
        best_move: tuple[int, int, int] | None = None
        grid = board.grid
        pid = piece.piece_id

        for rot, row, col in moves:
            shape = piece.rotations[rot]
            pr, pc = shape.shape
            mask = shape != 0

            # -- place piece in-place --
            region = grid[row:row + pr, col:col + pc]
            region[mask] = pid

            # -- check for complete lines in the affected rows --
            # Use fast row check: a row is full if no cell is 0.
            n_full = 0
            row_end = row + pr
            if row_end > ROWS:
                row_end = ROWS
            for rr in range(row, row_end):
                gr = grid[rr]
                is_full = True
                for cc in range(COLS):
                    if gr[cc] == 0:
                        is_full = False
                        break
                if is_full:
                    n_full += 1

            if n_full:
                # Build the cleared grid: remove full rows, add empty on top
                full = np.all(grid[row:row_end] != 0, axis=1)
                keep_mask = np.ones(ROWS, dtype=bool)
                for fi in range(row, row_end):
                    if full[fi - row]:
                        keep_mask[fi] = False
                kept = grid[keep_mask]
                temp_grid = np.vstack([
                    np.zeros((n_full, COLS), dtype=np.int8),
                    kept,
                ])
                val = evaluate_fn(temp_grid)
            else:
                val = evaluate_fn(grid)

            # -- undo placement --
            region[mask] = 0

            if val > best_val:
                best_val = val
                best_move = (rot, row, col)

        rot, row, col = best_move  # type: ignore[misc]
        board.place_piece(piece, rot, row, col)
        cleared = board.clear_lines()
        total_lines += cleared
        total_score += _LINE_SCORE.get(cleared, 800)
        pieces_placed += 1

        # Record history: full board snapshot every 10th piece,
        # plus always the 1st and last. Others get an empty list placeholder.
        record_board = (
            pieces_placed == 1
            or pieces_placed % 10 == 0
        )
        history.append({
            "board": board.grid.flatten().tolist() if record_board else [],
            "piece": piece.name,
            "position": [row, col],
            "rotation": rot,
            "score": total_score,
        })

        if board.is_game_over():
            break

    # Ensure the last entry always has the board state
    if history and not history[-1]["board"]:
        history[-1]["board"] = board.grid.flatten().tolist()

    return GameResult(
        lines_cleared=total_lines,
        pieces_placed=pieces_placed,
        score=total_score,
        move_history=history,
    )
