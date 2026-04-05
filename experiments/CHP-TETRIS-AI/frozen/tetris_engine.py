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
# Board
# ---------------------------------------------------------------------------

class Board:
    """20×10 Tetris board.  Row 0 is the top; row 19 is the bottom."""

    __slots__ = ("_grid",)

    ROWS = 20
    COLS = 10

    def __init__(self, grid: np.ndarray | None = None) -> None:
        if grid is not None:
            self._grid = grid
        else:
            self._grid = np.zeros((self.ROWS, self.COLS), dtype=np.int8)

    # -- properties ----------------------------------------------------------

    @property
    def grid(self) -> np.ndarray:
        return self._grid

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
        """Return all valid (rotation, row, col) drop placements."""
        moves: list[tuple[int, int, int]] = []
        for rot_idx, shape in enumerate(piece.rotations):
            pr, pc = shape.shape
            mask = shape != 0
            for col in range(self.COLS - pc + 1):
                # Drop: find lowest row where the piece fits
                best_row = -1
                for row in range(self.ROWS - pr + 1):
                    region = self._grid[row:row + pr, col:col + pc]
                    if not np.any(region[mask] != 0):
                        best_row = row
                    else:
                        break  # collision — stop dropping
                if best_row >= 0:
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

    while True:
        piece = gen.next()
        moves = board.get_legal_moves(piece)

        if not moves:
            # No legal placement — game over
            break

        # Evaluate every move, pick the best
        best_val = -np.inf
        best_move: tuple[int, int, int] | None = None

        for rot, row, col in moves:
            trial = board.copy()
            trial.place_piece(piece, rot, row, col)
            trial.clear_lines()
            val = evaluate_fn(trial.grid)
            if val > best_val:
                best_val = val
                best_move = (rot, row, col)

        rot, row, col = best_move  # type: ignore[misc]
        board.place_piece(piece, rot, row, col)
        cleared = board.clear_lines()
        total_lines += cleared
        total_score += _LINE_SCORE.get(cleared, 800)
        pieces_placed += 1

        history.append({
            "board": board.grid.flatten().tolist(),
            "piece": piece.name,
            "position": [row, col],
            "rotation": rot,
            "score": total_score,
        })

        if board.is_game_over():
            break

    return GameResult(
        lines_cleared=total_lines,
        pieces_placed=pieces_placed,
        score=total_score,
        move_history=history,
    )
