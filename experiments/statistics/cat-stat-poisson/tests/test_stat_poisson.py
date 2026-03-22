"""cat-stat-poisson — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_poisson_constants import *
IMPL = Path(__file__).parent.parent / "stat_poisson.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_mean_equals_variance(self):
        """Poisson mean and variance are BOTH λ — LLMs often treat them differently."""
        m = _i()
        assert m.poisson_mean(LAMBDA) == m.poisson_var(LAMBDA)
        assert m.poisson_mean(LAMBDA) == LAMBDA
        assert m.poisson_var(LAMBDA) == LAMBDA

    def test_overdispersion_detected(self):
        """When variance >> mean, Poisson is invalid — must detect overdispersion."""
        m = _i()
        # mean=3.0, variance=9.0 → ratio=3.0, well above default threshold 1.5
        assert m.is_overdispersed(3.0, 9.0) is True

    def test_no_overdispersion_when_equidispersed(self):
        """When variance ≈ mean, Poisson is valid — should NOT flag overdispersion."""
        m = _i()
        assert m.is_overdispersed(3.0, 3.0) is False


class TestCorrectness:
    def test_pmf_values_match_frozen(self):
        """PMF at k=0,1,2,3 for λ=3 must match frozen constants."""
        m = _i()
        assert abs(m.poisson_pmf(LAMBDA, 0) - P_0) < 1e-12, f"P(0) mismatch"
        assert abs(m.poisson_pmf(LAMBDA, 1) - P_1) < 1e-12, f"P(1) mismatch"
        assert abs(m.poisson_pmf(LAMBDA, 2) - P_2) < 1e-12, f"P(2) mismatch"
        assert abs(m.poisson_pmf(LAMBDA, 3) - P_3) < 1e-12, f"P(3) mismatch"

    def test_cdf_value_matches_frozen(self):
        """P(X≤2) must match frozen CDF_2 constant."""
        m = _i()
        cdf = m.poisson_cdf(LAMBDA, 2)
        assert abs(cdf - CDF_2) < 1e-12, f"CDF(2) = {cdf} != {CDF_2}"

    def test_pmf_sums_to_one(self):
        """PMF over a large range should sum to ≈1.0."""
        m = _i()
        total = sum(m.poisson_pmf(LAMBDA, k) for k in range(50))
        assert abs(total - 1.0) < 1e-12, f"PMF sum = {total}, expected ~1.0"
