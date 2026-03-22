"""cat-stat-binomial — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_binomial_constants import *
IMPL = Path(__file__).parent.parent / "stat_binomial.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_normal_approx_rejects_small_np(self):
        """np=0.1 < 5 — normal approx must be rejected."""
        m = _i()
        assert m.normal_approx_valid(N2, P2) is False

    def test_normal_approx_accepts_large_np(self):
        """np=50, n(1-p)=50 — normal approx is valid."""
        m = _i()
        assert m.normal_approx_valid(N1, P1) is True

    def test_exact_pmf_small_n_x0(self):
        """P(X=0) for n=10, p=0.01 must match frozen value."""
        m = _i()
        assert abs(m.binom_pmf(N2, 0, P2) - EXACT_P_X0) < 1e-12

    def test_exact_pmf_small_n_x1(self):
        """P(X=1) for n=10, p=0.01 must match frozen value."""
        m = _i()
        assert abs(m.binom_pmf(N2, 1, P2) - EXACT_P_X1) < 1e-12


class TestCorrectness:
    def test_binom_pmf_scenario1(self):
        """P(X=55) for n=100, p=0.5 must match frozen value."""
        m = _i()
        assert abs(m.binom_pmf(N1, K1, P1) - EXACT_P_55) < 1e-12

    def test_mean(self):
        m = _i()
        assert m.binom_mean(N1, P1) == MEAN1
        assert abs(m.binom_mean(N2, P2) - MEAN2) < 1e-12

    def test_variance(self):
        m = _i()
        assert m.binom_var(N1, P1) == VAR1
        assert abs(m.binom_var(N2, P2) - VAR2) < 1e-12

    def test_binom_coeff(self):
        m = _i()
        assert m.binom_coeff(100, 55) == math.comb(100, 55)
        assert m.binom_coeff(10, 0) == 1
        assert m.binom_coeff(10, 10) == 1
