"""cat-stat-chi-squared — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_chi_squared_constants import *
IMPL = Path(__file__).parent.parent / "stat_chi_squared.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_independence_df_is_product_not_rc_minus_1(self):
        """df = (r-1)(c-1), NOT r*c-1."""
        m = _i()
        df = m.independence_df(IND_ROWS, IND_COLS)
        wrong_df = IND_ROWS * IND_COLS - 1  # = 5
        assert df != wrong_df, f"Got r*c-1={wrong_df}, should be (r-1)(c-1)={IND_DF}"
        assert df == IND_DF  # = 2

    def test_independence_df_is_product_not_sum(self):
        """df = (r-1)*(c-1), NOT (r-1)+(c-1)."""
        m = _i()
        df = m.independence_df(IND_ROWS, IND_COLS)
        wrong_df = (IND_ROWS - 1) + (IND_COLS - 1)  # = 3
        assert df != wrong_df, f"Got (r-1)+(c-1)={wrong_df}, should be (r-1)*(c-1)={IND_DF}"
        assert df == IND_DF  # = 2

    def test_gof_df_is_k_minus_1(self):
        """GoF degrees of freedom = k - 1."""
        m = _i()
        assert m.gof_df(GOF_K) == GOF_DF  # 6-1 = 5


class TestCorrectness:
    def test_chi_squared_gof_value(self):
        """χ² GoF for die fairness data = 3.2."""
        m = _i()
        chi2 = m.chi_squared_gof(GOF_OBSERVED, GOF_EXPECTED)
        assert abs(chi2 - GOF_CHI2) < 1e-9

    def test_contingency_expected_values(self):
        """Expected frequencies from marginals for 2x3 table."""
        m = _i()
        expected = m.contingency_expected(IND_TABLE)
        for i in range(IND_ROWS):
            for j in range(IND_COLS):
                assert abs(expected[i][j] - IND_EXPECTED[i][j]) < 1e-9, \
                    f"E[{i}][{j}]: got {expected[i][j]}, want {IND_EXPECTED[i][j]}"

    def test_chi_squared_independence_value(self):
        """χ² independence for 2x3 table ≈ 4.5022."""
        m = _i()
        chi2 = m.chi_squared_independence(IND_TABLE)
        assert abs(chi2 - IND_CHI2) < 1e-4
