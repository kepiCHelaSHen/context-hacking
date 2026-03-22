"""cat-stat-fisher-exact — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_fisher_exact_constants import *
IMPL = Path(__file__).parent.parent / "stat_fisher_exact.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_uses_combinatorics_not_chi_sq(self):
        """Fisher exact test must use exact combinatorics, not chi-squared approx."""
        m = _i()
        import inspect
        src = inspect.getsource(m.hypergeom_pmf)
        # Must use math.comb (combinatorial), not chi-squared keywords
        assert "comb" in src, "hypergeom_pmf should use math.comb for exact calculation"

    def test_two_tail_not_double_one_tail(self):
        """Two-tailed p != 2 * one-tailed p in general (asymmetric margins)."""
        m = _i()
        # Asymmetric table: R1=3, R2=7 => skewed hypergeometric distribution
        asym_table = [[3, 0], [1, 6]]
        p_one = m.fisher_one_tail(asym_table, direction="greater")
        p_two = m.fisher_two_tail(asym_table)
        # one-tail(>=3) = 7/210, two-tail = 7/210, 2*one-tail = 14/210
        assert abs(p_two - 2 * p_one) > 1e-9, \
            f"Two-tail ({p_two}) should NOT equal 2 * one-tail ({2 * p_one})"

    def test_hypergeom_not_wrong_formula(self):
        """P(a) must equal C(R1,a)*C(R2,C1-a)/C(N,C1), not a wrong variant."""
        m = _i()
        p = m.hypergeom_pmf(3, R1, R2, C1, N)
        # Verify it matches the exact fraction 16/70
        assert abs(p - 16 / 70) < 1e-12, \
            f"P(3) should be 16/70={16/70:.10f}, got {p:.10f}"


class TestCorrectness:
    def test_hypergeom_pmf_a3(self):
        """P(a=3) = C(4,3)*C(4,1)/C(8,4) = 16/70."""
        m = _i()
        p = m.hypergeom_pmf(3, R1, R2, C1, N)
        assert abs(p - P_EXACT) < 1e-12

    def test_one_tail_p(self):
        """One-tailed P(a>=3) = 17/70."""
        m = _i()
        p = m.fisher_one_tail(TABLE, direction="greater")
        assert abs(p - P_ONE_TAIL) < 1e-12

    def test_two_tail_p(self):
        """Two-tailed p (sum of P <= P_obs) = 34/70."""
        m = _i()
        p = m.fisher_two_tail(TABLE)
        assert abs(p - P_TWO_TAIL) < 1e-12

    def test_margins(self):
        """table_margins returns correct (R1, R2, C1, C2, N)."""
        m = _i()
        r1, r2, c1, c2, n = m.table_margins(TABLE)
        assert (r1, r2, c1, c2, n) == (R1, R2, C1, C2, N)

    def test_hypergeom_boundary_values(self):
        """P(a) = 0 for impossible cell counts."""
        m = _i()
        # a = -1 or a > R1 should give 0
        assert m.hypergeom_pmf(-1, R1, R2, C1, N) == 0.0
        assert m.hypergeom_pmf(5, R1, R2, C1, N) == 0.0

    def test_all_probs_sum_to_one(self):
        """Full hypergeometric distribution sums to 1."""
        m = _i()
        total = sum(m.hypergeom_pmf(a, R1, R2, C1, N) for a in range(0, min(R1, C1) + 1))
        assert abs(total - 1.0) < 1e-12
