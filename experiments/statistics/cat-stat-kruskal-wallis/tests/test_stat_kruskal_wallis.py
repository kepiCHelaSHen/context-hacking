"""cat-stat-kruskal-wallis — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_kruskal_wallis_constants import *
IMPL = Path(__file__).parent.parent / "stat_kruskal_wallis.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_df_is_k_minus_1_not_k(self):
        """df = k-1, NOT k."""
        m = _i()
        df = m.kruskal_wallis_df(K)
        assert df != K, f"Got k={K}, should be k-1={DF}"
        assert df == DF  # = 2

    def test_df_is_k_minus_1_not_n_minus_1(self):
        """df = k-1, NOT N-1."""
        m = _i()
        df = m.kruskal_wallis_df(K)
        assert df != N - 1, f"Got N-1={N-1}, should be k-1={DF}"
        assert df == DF  # = 2

    def test_tie_correction_makes_h_larger_or_equal(self):
        """With ties, H_corrected >= H (dividing by factor <= 1 increases H)."""
        m = _i()
        # Data with ties: two 5s
        groups_tied = [[4, 5, 5], [1, 2, 3], [7, 8, 9]]
        h_raw = m.kruskal_wallis_h(groups_tied)
        tc = m.tie_correction_factor(groups_tied)
        h_corrected = h_raw / tc
        assert tc <= 1.0, "Tie correction factor must be <= 1.0"
        assert h_corrected >= h_raw - 1e-12, \
            f"H_corrected={h_corrected} should be >= H_raw={h_raw}"

    def test_no_ties_correction_is_one(self):
        """Without ties, tie correction factor = 1.0 (no change to H)."""
        m = _i()
        tc = m.tie_correction_factor(GROUPS)
        assert tc == 1.0, f"No ties → correction should be 1.0, got {tc}"

    def test_tie_correction_uses_t_cubed(self):
        """Tie correction uses t³-t, NOT t²-t (the common LLM error)."""
        m = _i()
        # Single tie group of size 2 in N=9
        groups_tied = [[4, 5, 5], [1, 2, 3], [7, 8, 9]]
        tc = m.tie_correction_factor(groups_tied)
        # Correct: 1 - (2³-2)/(9³-9) = 1 - 6/720 = 0.991667
        correct = 1 - (2 ** 3 - 2) / (9 ** 3 - 9)
        # Wrong (t²-t): 1 - (4-2)/(729-9) = 1 - 2/720 = 0.997222
        wrong = 1 - (2 ** 2 - 2) / (9 ** 3 - 9)
        assert abs(tc - correct) < 1e-9, \
            f"Got {tc}, expected {correct} (t³-t formula)"
        assert abs(tc - wrong) > 1e-6, \
            f"Got {tc} which matches wrong t²-t formula {wrong}"


class TestCorrectness:
    def test_h_stat_value(self):
        """H = 7.2 for the 3-group test data."""
        m = _i()
        h = m.kruskal_wallis_h(GROUPS)
        assert abs(h - H_STAT) < 1e-9, f"H={h}, expected {H_STAT}"

    def test_rank_sums(self):
        """Rank sums: A=15, B=6, C=24."""
        m = _i()
        rs = m.rank_all(GROUPS)
        assert abs(rs[0] - R_A) < 1e-9, f"R_A={rs[0]}, expected {R_A}"
        assert abs(rs[1] - R_B) < 1e-9, f"R_B={rs[1]}, expected {R_B}"
        assert abs(rs[2] - R_C) < 1e-9, f"R_C={rs[2]}, expected {R_C}"

    def test_df_value(self):
        """df = 2 for k=3 groups."""
        m = _i()
        assert m.kruskal_wallis_df(K) == DF

    def test_tie_correction_value(self):
        """Tie correction for t=2 in N=9: ≈ 0.99167."""
        m = _i()
        groups_tied = [[4, 5, 5], [1, 2, 3], [7, 8, 9]]
        tc = m.tie_correction_factor(groups_tied)
        assert abs(tc - TIE_CORRECTION) < 1e-4, \
            f"Tie correction={tc}, expected ≈{TIE_CORRECTION}"

    def test_h_stat_matches_constant(self):
        """Verify computed H matches the frozen constant exactly."""
        m = _i()
        h = m.kruskal_wallis_h(GROUPS)
        assert abs(h - 7.2) < 1e-9
