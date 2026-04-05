"""Tests for frozen feature functions. Written TDD-first."""

import numpy as np
import pytest

from features import (
    FEATURE_FNS,
    FEATURE_NAMES,
    aggregate_height,
    bumpiness,
    column_transitions,
    complete_lines,
    holes,
    row_transitions,
    tetris_readiness,
    well_depth,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def empty_board() -> np.ndarray:
    return np.zeros((20, 10), dtype=np.int8)


def board_with_full_rows(*row_indices) -> np.ndarray:
    g = empty_board()
    for r in row_indices:
        g[r, :] = 1
    return g


# ---------------------------------------------------------------------------
# TestEmptyBoard — all features should return 0 on a fully empty board
# ---------------------------------------------------------------------------
class TestEmptyBoard:
    def test_aggregate_height_empty(self):
        assert aggregate_height(empty_board()) == 0.0

    def test_complete_lines_empty(self):
        assert complete_lines(empty_board()) == 0.0

    def test_holes_empty(self):
        assert holes(empty_board()) == 0.0

    def test_bumpiness_empty(self):
        assert bumpiness(empty_board()) == 0.0

    def test_well_depth_empty(self):
        assert well_depth(empty_board()) == 0.0

    def test_tetris_readiness_empty(self):
        assert tetris_readiness(empty_board()) == 0.0

    def test_column_transitions_empty(self):
        assert column_transitions(empty_board()) == 0.0

    def test_row_transitions_empty(self):
        assert row_transitions(empty_board()) == 0.0


# ---------------------------------------------------------------------------
# TestCompleteLines
# ---------------------------------------------------------------------------
class TestCompleteLines:
    def test_one_full_row(self):
        assert complete_lines(board_with_full_rows(19)) == 1.0

    def test_two_full_rows(self):
        assert complete_lines(board_with_full_rows(18, 19)) == 2.0

    def test_partial_row_not_counted(self):
        g = empty_board()
        g[19, :9] = 1  # all but last cell
        assert complete_lines(g) == 0.0

    def test_all_rows_full(self):
        g = np.ones((20, 10), dtype=np.int8)
        assert complete_lines(g) == 20.0


# ---------------------------------------------------------------------------
# TestAggregateHeight
# ---------------------------------------------------------------------------
class TestAggregateHeight:
    def test_single_cell_at_bottom(self):
        # Row 19 is bottom → height = 20 - 19 = 1
        g = empty_board()
        g[19, 0] = 1
        assert aggregate_height(g) == 1.0

    def test_single_column_height_2(self):
        # Cells at rows 18 and 19 in col 0 → height = 20 - 18 = 2
        g = empty_board()
        g[18, 0] = 1
        g[19, 0] = 1
        assert aggregate_height(g) == 2.0

    def test_topmost_cell_determines_height(self):
        # Only the topmost nonzero row matters per column
        g = empty_board()
        g[18, 0] = 1
        g[16, 0] = 1  # topmost
        # height = 20 - 16 = 4
        assert aggregate_height(g) == 4.0

    def test_multiple_columns_sum(self):
        # col 0: topmost at row 17 → height 3
        # col 1: topmost at row 15 → height 5
        g = empty_board()
        g[17, 0] = 1
        g[15, 1] = 1
        assert aggregate_height(g) == 8.0

    def test_top_row_height_20(self):
        g = empty_board()
        g[0, 5] = 1
        assert aggregate_height(g) == 20.0


# ---------------------------------------------------------------------------
# TestHoles
# ---------------------------------------------------------------------------
class TestHoles:
    def test_one_hole(self):
        # Col 0: filled at row 18, empty at row 19 → 1 hole
        g = empty_board()
        g[18, 0] = 1
        assert holes(g) == 1.0

    def test_no_hole_when_no_filled_above(self):
        # Empty cell at bottom with nothing above → not a hole
        g = empty_board()
        g[19, 0] = 1  # filled at bottom, nothing above
        assert holes(g) == 0.0

    def test_two_holes_in_one_column(self):
        # Col 0: filled at row 16, empty at 17, empty at 18, filled at 19
        g = empty_board()
        g[16, 0] = 1
        g[19, 0] = 1
        assert holes(g) == 2.0

    def test_multiple_columns_with_holes(self):
        g = empty_board()
        # Col 0: 1 hole (filled at 17, empty at 18&19... wait, 18 and 19 are both empty)
        g[17, 0] = 1  # col 0: topmost at 17, rows 18&19 empty → 2 holes
        g[15, 1] = 1  # col 1: topmost at 15, rows 16-19 empty → 4 holes
        assert holes(g) == 6.0

    def test_no_holes_solid_column(self):
        g = empty_board()
        g[17, 0] = 1
        g[18, 0] = 1
        g[19, 0] = 1
        assert holes(g) == 0.0


# ---------------------------------------------------------------------------
# TestBumpiness
# ---------------------------------------------------------------------------
class TestBumpiness:
    def test_flat_surface_zero(self):
        # All columns same height
        g = empty_board()
        g[19, :] = 1
        assert bumpiness(g) == 0.0

    def test_single_step(self):
        # Col 0 height 1 (row 19), col 1 height 2 (row 18), rest empty
        g = empty_board()
        g[19, 0] = 1
        g[18, 1] = 1
        # |1 - 2| = 1 for pair (0,1); all other pairs 0 because |2-0|, |0-0|... wait
        # col 2..9 are empty (height 0)
        # |h[1]-h[2]| = |2-0| = 2
        # total = 1 + 2 + 0*7 = 3
        assert bumpiness(g) == 3.0

    def test_alternating_heights(self):
        # Alternating 1 and 2 across all 10 columns
        g = empty_board()
        for c in range(10):
            row = 18 if c % 2 == 0 else 19
            g[row, c] = 1
        # Each adjacent pair differs by 1, 9 pairs → bumpiness = 9
        assert bumpiness(g) == 9.0

    def test_two_columns_same(self):
        g = empty_board()
        g[19, 0] = 1
        g[19, 1] = 1
        # pair (0,1): |1-1|=0; pair(1,2): |1-0|=1; pair(2..9): 0 → total=1
        assert bumpiness(g) == 1.0


# ---------------------------------------------------------------------------
# TestWellDepth
# ---------------------------------------------------------------------------
class TestWellDepth:
    def test_simple_well_center(self):
        # col 5 height 0, neighbors (4 and 6) height 3
        g = empty_board()
        g[17, 4] = 1  # height 3
        g[17, 6] = 1  # height 3
        # col 5: well depth = min(3, 3) - 0 = 3
        assert well_depth(g) == 3.0

    def test_no_well_flat(self):
        g = empty_board()
        g[19, :] = 1  # all same height
        assert well_depth(g) == 0.0

    def test_left_edge_well(self):
        # col 0 height 0, col 1 height 3 → edge well depth = min(3) - 0 = 3
        g = empty_board()
        g[17, 1] = 1
        assert well_depth(g) == 3.0

    def test_right_edge_well(self):
        # col 9 height 0, col 8 height 3 → edge well depth = 3
        g = empty_board()
        g[17, 8] = 1
        assert well_depth(g) == 3.0

    def test_multiple_wells(self):
        # col 2 and col 7 are both interior wells, cols 0 and 9 are edge wells
        # h: [0, 3, 0, 3, 0, 0, 3, 0, 3, 0]
        # col 0 edge: h[1]-h[0] = 3-0 = 3
        # col 2 interior: min(h[1],h[3]) - h[2] = min(3,3)-0 = 3
        # col 7 interior: min(h[6],h[8]) - h[7] = min(3,3)-0 = 3
        # col 9 edge: h[8]-h[9] = 3-0 = 3
        # total = 12
        g = empty_board()
        g[17, 1] = 1  # height 3
        g[17, 3] = 1  # height 3 → col 2 well depth = 3
        g[17, 6] = 1  # height 3
        g[17, 8] = 1  # height 3 → col 7 well depth = 3
        assert well_depth(g) == 12.0


# ---------------------------------------------------------------------------
# TestTetrisReadiness
# ---------------------------------------------------------------------------
class TestTetrisReadiness:
    def test_deep_well_gives_readiness_1(self):
        # col 9 (right edge) depth 4: col 8 height 4, col 9 height 0
        g = empty_board()
        g[16, 8] = 1  # height = 20-16 = 4
        assert tetris_readiness(g) == 1.0

    def test_shallow_well_gives_0(self):
        g = empty_board()
        g[17, 1] = 1  # depth 3, not enough
        g[17, 3] = 1
        assert tetris_readiness(g) == 0.0

    def test_exactly_4_gives_readiness_1(self):
        # col 5 height 0, neighbors height 4
        g = empty_board()
        g[16, 4] = 1  # height 4
        g[16, 6] = 1  # height 4
        assert tetris_readiness(g) == 1.0

    def test_no_well_gives_0(self):
        assert tetris_readiness(empty_board()) == 0.0


# ---------------------------------------------------------------------------
# TestColumnTransitions
# ---------------------------------------------------------------------------
class TestColumnTransitions:
    def test_solid_column_no_transitions(self):
        g = empty_board()
        g[17, 0] = 1
        g[18, 0] = 1
        g[19, 0] = 1
        # 3 consecutive filled → 0 transitions within the column
        assert column_transitions(g) == 0.0

    def test_alternating_in_column(self):
        # col 0: filled at 17, empty at 18, filled at 19
        # Within occupied region (rows 17-19): F E F → 2 transitions
        g = empty_board()
        g[17, 0] = 1
        g[19, 0] = 1
        assert column_transitions(g) == 2.0

    def test_multiple_columns_sum(self):
        # col 0: cells at rows 17 and 19, topmost=17
        #   region rows 17-19: [F, E, F] → 2 transitions
        # col 1: cells at rows 16 and 18, topmost=16
        #   region rows 16-19: [F, E, F, E] → 3 transitions
        # total = 5
        g = empty_board()
        g[17, 0] = 1
        g[19, 0] = 1  # col 0: 2 transitions
        g[16, 1] = 1
        g[18, 1] = 1  # col 1: rows 16-19 → F E F E = 3 transitions
        assert column_transitions(g) == 5.0

    def test_empty_columns_no_transitions(self):
        assert column_transitions(empty_board()) == 0.0


# ---------------------------------------------------------------------------
# TestRowTransitions
# ---------------------------------------------------------------------------
class TestRowTransitions:
    def test_full_row_no_transitions(self):
        # A completely full row: edges are treated as filled,
        # so filled→filled at both edges and no internal changes → 0
        g = board_with_full_rows(19)
        # Only row 19 has cells; it's full → 0 transitions
        assert row_transitions(g) == 0.0

    def test_single_cell_in_row(self):
        # Row 19: _ _ _ _ _ 1 _ _ _ _  (only col 5 filled)
        # Left edge (filled) → col 0 (empty): transition
        # col 4 (empty) → col 5 (filled): transition
        # col 5 (filled) → col 6 (empty): transition
        # col 9 (empty) → right edge (filled): transition
        # Total: 4
        g = empty_board()
        g[19, 5] = 1
        assert row_transitions(g) == 4.0

    def test_gap_in_almost_full_row(self):
        # Row 19: all filled except col 5
        # 1 1 1 1 1 0 1 1 1 1
        # left-edge→col0: filled→filled: 0
        # col4→col5: filled→empty: 1
        # col5→col6: empty→filled: 1
        # col9→right-edge: filled→filled: 0
        # Total: 2
        g = empty_board()
        g[19, :] = 1
        g[19, 5] = 0
        assert row_transitions(g) == 2.0

    def test_empty_rows_not_counted(self):
        # Empty rows should not contribute
        assert row_transitions(empty_board()) == 0.0

    def test_two_rows_with_transitions(self):
        # Each row has 1 gap in middle → 2 transitions each → 4 total
        g = empty_board()
        g[18, :] = 1
        g[18, 5] = 0  # 2 transitions in row 18
        g[19, :] = 1
        g[19, 3] = 0  # 2 transitions in row 19
        assert row_transitions(g) == 4.0


# ---------------------------------------------------------------------------
# TestFeatureRegistry
# ---------------------------------------------------------------------------
class TestFeatureRegistry:
    def test_feature_names_has_8(self):
        assert len(FEATURE_NAMES) == 8

    def test_feature_names_are_strings(self):
        for name in FEATURE_NAMES:
            assert isinstance(name, str)

    def test_feature_fns_has_8(self):
        assert len(FEATURE_FNS) == 8

    def test_feature_fns_all_callable(self):
        for name, fn in FEATURE_FNS.items():
            assert callable(fn), f"{name} is not callable"

    def test_feature_fns_keys_match_names(self):
        assert set(FEATURE_FNS.keys()) == set(FEATURE_NAMES)

    def test_all_expected_names_present(self):
        expected = {
            "aggregate_height",
            "complete_lines",
            "holes",
            "bumpiness",
            "well_depth",
            "tetris_readiness",
            "column_transitions",
            "row_transitions",
        }
        assert set(FEATURE_NAMES) == expected

    def test_feature_fns_return_float(self):
        g = empty_board()
        for name, fn in FEATURE_FNS.items():
            result = fn(g)
            assert isinstance(result, float), f"{name} did not return float"
