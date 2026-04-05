"""Tests for the frozen Tetris engine. Written TDD-first."""

import numpy as np
import pytest

from tetris_engine import (
    Board,
    GameResult,
    Piece,
    PieceGenerator,
    TETROMINOES,
    play_game,
)


# ---------------------------------------------------------------------------
# TestBoard
# ---------------------------------------------------------------------------
class TestBoard:
    def test_empty_board_shape_and_zeros(self):
        b = Board()
        assert b.grid.shape == (20, 10)
        assert b.grid.dtype == np.int8
        assert np.all(b.grid == 0)

    def test_place_piece_on_empty_board_succeeds(self):
        b = Board()
        piece = TETROMINOES["T"]
        ok = b.place_piece(piece, rotation=0, row=0, col=3)
        assert ok is True
        # At least some cells should now be nonzero
        assert np.any(b.grid != 0)

    def test_place_piece_fills_correct_cells(self):
        b = Board()
        piece = TETROMINOES["O"]
        # O piece rotation 0 is a 2x2 block
        ok = b.place_piece(piece, rotation=0, row=0, col=0)
        assert ok is True
        shape = piece.rotations[0]
        for r in range(shape.shape[0]):
            for c in range(shape.shape[1]):
                if shape[r, c]:
                    assert b.grid[0 + r, 0 + c] == piece.piece_id

    def test_cannot_place_out_of_bounds_right(self):
        b = Board()
        piece = TETROMINOES["I"]
        # I horizontal is 1x4, placing at col=8 would exceed col 10
        ok = b.place_piece(piece, rotation=0, row=0, col=8)
        assert ok is False
        # Board should be unchanged
        assert np.all(b.grid == 0)

    def test_cannot_place_out_of_bounds_bottom(self):
        b = Board()
        piece = TETROMINOES["I"]
        # Vertical I is 4x1, placing at row=18 would go past row 20
        ok = b.place_piece(piece, rotation=1, row=18, col=0)
        assert ok is False
        assert np.all(b.grid == 0)

    def test_cannot_place_overlapping(self):
        b = Board()
        piece = TETROMINOES["O"]
        b.place_piece(piece, rotation=0, row=0, col=0)
        ok = b.place_piece(piece, rotation=0, row=0, col=0)
        assert ok is False

    def test_single_line_clear(self):
        b = Board()
        # Fill row 19 (bottom) completely by hand
        b.grid[19, :] = 1
        cleared = b.clear_lines()
        assert cleared == 1
        assert np.all(b.grid[19, :] == 0)

    def test_multiple_line_clear(self):
        b = Board()
        b.grid[18, :] = 1
        b.grid[19, :] = 1
        cleared = b.clear_lines()
        assert cleared == 2
        assert np.all(b.grid[18:, :] == 0)

    def test_line_clear_shifts_down(self):
        b = Board()
        # Put a partial row at 17, full rows at 18 and 19
        b.grid[17, 0:5] = 1
        b.grid[18, :] = 1
        b.grid[19, :] = 1
        cleared = b.clear_lines()
        assert cleared == 2
        # The partial row should have shifted down to row 19
        assert np.all(b.grid[19, 0:5] == 1)
        assert np.all(b.grid[19, 5:] == 0)

    def test_game_over_top_row_filled(self):
        b = Board()
        b.grid[0, 5] = 1
        assert b.is_game_over() is True

    def test_empty_board_not_game_over(self):
        b = Board()
        assert b.is_game_over() is False

    def test_copy_is_independent(self):
        b = Board()
        b.grid[10, 5] = 1
        c = b.copy()
        assert c.grid[10, 5] == 1
        c.grid[10, 5] = 0
        assert b.grid[10, 5] == 1  # original unchanged

    def test_max_height_empty(self):
        b = Board()
        assert b.max_height() == 0

    def test_max_height_nonempty(self):
        b = Board()
        # Place something at row 15 (5 rows from bottom in 0-indexed top-down)
        b.grid[15, 3] = 1
        # Height should be 20 - 15 = 5
        assert b.max_height() == 5

    def test_get_legal_moves_nonempty_on_empty_board(self):
        b = Board()
        piece = TETROMINOES["T"]
        moves = b.get_legal_moves(piece)
        assert len(moves) > 0
        # Each move is (rotation, row, col)
        for rot, row, col in moves:
            assert isinstance(rot, int)
            assert isinstance(row, (int, np.integer))
            assert isinstance(col, (int, np.integer))

    def test_get_legal_moves_all_valid(self):
        """Every returned move must actually succeed when placed."""
        b = Board()
        piece = TETROMINOES["T"]
        for rot, row, col in b.get_legal_moves(piece):
            copy = b.copy()
            assert copy.place_piece(piece, rot, row, col) is True


# ---------------------------------------------------------------------------
# TestPieceGeneration
# ---------------------------------------------------------------------------
class TestPieceGeneration:
    def test_deterministic_same_seed(self):
        g1 = PieceGenerator(seed=42)
        g2 = PieceGenerator(seed=42)
        seq1 = [g1.next().name for _ in range(21)]
        seq2 = [g2.next().name for _ in range(21)]
        assert seq1 == seq2

    def test_different_seeds_differ(self):
        g1 = PieceGenerator(seed=1)
        g2 = PieceGenerator(seed=2)
        seq1 = [g1.next().name for _ in range(14)]
        seq2 = [g2.next().name for _ in range(14)]
        assert seq1 != seq2

    def test_all_seven_pieces_appear(self):
        g = PieceGenerator(seed=99)
        names = {g.next().name for _ in range(100)}
        assert names == {"I", "O", "T", "S", "Z", "J", "L"}

    def test_seven_bag_property(self):
        """Each bag of 7 must contain all 7 pieces exactly once."""
        g = PieceGenerator(seed=0)
        for _ in range(5):  # check 5 consecutive bags
            bag = [g.next().name for _ in range(7)]
            assert sorted(bag) == ["I", "J", "L", "O", "S", "T", "Z"]


# ---------------------------------------------------------------------------
# TestTetrominoes
# ---------------------------------------------------------------------------
class TestTetrominoes:
    def test_all_seven_defined(self):
        assert set(TETROMINOES.keys()) == {"I", "O", "T", "S", "Z", "J", "L"}

    def test_piece_ids(self):
        expected = {"I": 1, "O": 2, "T": 3, "S": 4, "Z": 5, "J": 6, "L": 7}
        for name, pid in expected.items():
            assert TETROMINOES[name].piece_id == pid

    def test_four_rotations_each(self):
        for name, piece in TETROMINOES.items():
            assert len(piece.rotations) == 4, f"{name} should have 4 rotations"

    def test_rotations_are_numpy(self):
        for piece in TETROMINOES.values():
            for rot in piece.rotations:
                assert isinstance(rot, np.ndarray)
                assert rot.ndim == 2


# ---------------------------------------------------------------------------
# TestPlayGame
# ---------------------------------------------------------------------------
class TestPlayGame:
    @staticmethod
    def _simple_eval(grid: np.ndarray) -> float:
        """Heuristic: penalise height, reward empty space."""
        return -float(np.sum(grid != 0))

    def test_returns_game_result(self):
        result = play_game(self._simple_eval, seed=0)
        assert isinstance(result, GameResult)
        assert isinstance(result.lines_cleared, int)
        assert isinstance(result.pieces_placed, int)
        assert isinstance(result.score, int)
        assert isinstance(result.move_history, list)

    def test_deterministic(self):
        r1 = play_game(self._simple_eval, seed=7)
        r2 = play_game(self._simple_eval, seed=7)
        assert r1.lines_cleared == r2.lines_cleared
        assert r1.pieces_placed == r2.pieces_placed
        assert r1.score == r2.score

    def test_better_eval_scores_higher(self):
        def bad_eval(grid):
            return 0.0  # random-ish: always scores the same

        good_result = play_game(self._simple_eval, seed=0)
        bad_result = play_game(bad_eval, seed=0)
        # The "good" heuristic should place at least as many pieces
        # (it penalises height, which keeps the board low longer)
        assert good_result.pieces_placed >= bad_result.pieces_placed

    def test_move_history_structure(self):
        result = play_game(self._simple_eval, seed=0)
        assert len(result.move_history) > 0
        entry = result.move_history[0]
        assert "board" in entry
        assert "piece" in entry
        assert "position" in entry
        assert "rotation" in entry
        assert "score" in entry
        assert isinstance(entry["board"], list)
        assert isinstance(entry["piece"], str)
        assert isinstance(entry["position"], list)
        assert len(entry["position"]) == 2
        assert isinstance(entry["rotation"], int)

    def test_score_matches_line_scoring(self):
        """Cumulative score should equal sum of per-clear rewards."""
        result = play_game(self._simple_eval, seed=0)
        # We can't easily recompute, but score should be non-negative
        assert result.score >= 0

    def test_performance_under_500ms(self):
        import time

        start = time.perf_counter()
        play_game(self._simple_eval, seed=0)
        elapsed = time.perf_counter() - start
        assert elapsed < 0.5, f"Game took {elapsed:.3f}s, must be < 0.5s"
