"""cat-econ-gini — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_gini_constants import *
IMPL = Path(__file__).parent.parent / "econ_gini.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that specifically catch known LLM errors."""

    def test_sorts_before_lorenz(self):
        """PRIOR: unsorted_data — must sort incomes ascending before Lorenz curve."""
        m = _i()
        # Unsorted input must produce same Gini as sorted input
        g_sorted = m.gini_coefficient(INCOMES_SORTED)
        g_unsorted = m.gini_coefficient(INCOMES_UNSORTED)
        assert abs(g_sorted - g_unsorted) < 1e-12, (
            f"Unsorted input gave Gini={g_unsorted}, sorted gave {g_sorted} — data not sorted"
        )

    def test_lorenz_uses_cumulative_shares(self):
        """PRIOR: lorenz_no_cumulative — Lorenz Y values must be cumulative, not raw shares."""
        m = _i()
        cum_pop, cum_income = m.lorenz_curve(INCOMES)
        # Cumulative income shares must be non-decreasing
        for i in range(1, len(cum_income)):
            assert cum_income[i] >= cum_income[i - 1], (
                f"Lorenz income shares not cumulative: {cum_income[i]} < {cum_income[i-1]}"
            )
        # Must match frozen values
        assert len(cum_income) == len(CUM_INCOME_SHARES), (
            f"Expected {len(CUM_INCOME_SHARES)} points, got {len(cum_income)}"
        )
        for i, (got, exp) in enumerate(zip(cum_income, CUM_INCOME_SHARES)):
            assert abs(got - exp) < 1e-9, (
                f"Lorenz income share [{i}]: expected {exp}, got {got}"
            )

    def test_gini_in_valid_range(self):
        """PRIOR: gini_range_wrong — Gini must be in [0, 1]."""
        m = _i()
        for data in [INCOMES, EQUAL_INCOMES, EXTREME_INCOMES, INCOMES_UNSORTED]:
            g = m.gini_coefficient(data)
            assert 0.0 <= g <= 1.0, f"Gini={g} out of range [0,1] for data={data}"


class TestCorrectness:
    """Numerical verification against frozen constants."""

    def test_gini_main_vector(self):
        m = _i()
        g = m.gini_coefficient(INCOMES)
        assert abs(g - GINI_TEST) < 1e-9, f"Expected {GINI_TEST}, got {g}"

    def test_gini_perfect_equality(self):
        m = _i()
        g = m.gini_coefficient(EQUAL_INCOMES)
        assert abs(g - GINI_EQUAL) < 1e-9, f"Expected {GINI_EQUAL}, got {g}"

    def test_gini_extreme_inequality(self):
        m = _i()
        g = m.gini_coefficient(EXTREME_INCOMES)
        assert abs(g - GINI_EXTREME) < 1e-9, f"Expected {GINI_EXTREME}, got {g}"

    def test_gini_unsorted_input(self):
        m = _i()
        g = m.gini_coefficient(INCOMES_UNSORTED)
        assert abs(g - GINI_TEST) < 1e-9, f"Expected {GINI_TEST}, got {g}"

    def test_lorenz_population_shares(self):
        m = _i()
        cum_pop, _ = m.lorenz_curve(INCOMES)
        for got, exp in zip(cum_pop, CUM_POP_SHARES):
            assert abs(got - exp) < 1e-9, f"Pop share: expected {exp}, got {got}"

    def test_lorenz_income_shares(self):
        m = _i()
        _, cum_income = m.lorenz_curve(INCOMES)
        for got, exp in zip(cum_income, CUM_INCOME_SHARES):
            assert abs(got - exp) < 1e-9, f"Income share: expected {exp}, got {got}"

    def test_lorenz_endpoints(self):
        m = _i()
        cum_pop, cum_income = m.lorenz_curve(INCOMES)
        assert cum_pop[0] == 0.0 and cum_income[0] == 0.0, "Lorenz must start at (0, 0)"
        assert abs(cum_pop[-1] - 1.0) < 1e-12 and abs(cum_income[-1] - 1.0) < 1e-12, (
            "Lorenz must end at (1, 1)"
        )

    def test_is_perfectly_equal_true(self):
        m = _i()
        assert m.is_perfectly_equal(0.0) is True
        assert m.is_perfectly_equal(0.005) is True

    def test_is_perfectly_equal_false(self):
        m = _i()
        assert m.is_perfectly_equal(0.40) is False
        assert m.is_perfectly_equal(0.80) is False

    def test_is_perfectly_equal_custom_tol(self):
        m = _i()
        assert m.is_perfectly_equal(0.05, tol=0.1) is True
        assert m.is_perfectly_equal(0.05, tol=0.01) is False
