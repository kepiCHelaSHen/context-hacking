"""cat-stat-hypothesis-testing — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_hypothesis_testing_constants import *
IMPL = Path(__file__).parent.parent / "stat_hypothesis_testing.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_p_value_is_not_prob_h0(self):
        """p-value must be in (0,1) and match the frozen computed value,
        confirming it is P(data|H0), NOT P(H0|data)."""
        m = _i()
        p = m.p_value_two_tailed(Z_STAT)
        assert 0.0 < p < 1.0, "p-value must be in (0, 1)"
        assert abs(p - P_VALUE_TWO) < 1e-6, f"p={p} != frozen {P_VALUE_TWO}"

    def test_reject_at_alpha_05_not_alpha_01(self):
        """At alpha=0.05 we reject; at alpha=0.01 we do not.
        Ensures alpha is applied correctly and not swapped with beta."""
        m = _i()
        p = m.p_value_two_tailed(Z_STAT)
        assert m.reject_h0(p, ALPHA_05) is True, "Should reject at alpha=0.05"
        assert m.reject_h0(p, ALPHA_01) is False, "Should NOT reject at alpha=0.01"

    def test_two_tailed_not_one_tailed(self):
        """Two-tailed p must equal 2*(1-Phi(|z|)), not 1*(1-Phi(|z|))."""
        m = _i()
        p_two = m.p_value_two_tailed(Z_STAT)
        # One-tailed (wrong) would be half: 0.5*(1 - erf(|z|/sqrt(2)))
        p_one_wrong = 0.5 * (1.0 - math.erf(abs(Z_STAT) / math.sqrt(2)))
        assert abs(p_two - 2.0 * p_one_wrong) < 1e-10, "Two-tailed must be double one-tailed"

class TestCorrectness:
    def test_z_statistic(self):
        """z = (xbar - mu0) / SE = (104 - 100) / 2.0 = 2.0"""
        m = _i()
        z = m.z_test_statistic(XBAR, MU_0, SIGMA, N)
        assert abs(z - Z_STAT) < 1e-9, f"z={z} != {Z_STAT}"

    def test_p_value_two_tailed(self):
        """p = 1 - erf(|z|/sqrt(2)) = 0.04550 (five significant figures)."""
        m = _i()
        p = m.p_value_two_tailed(Z_STAT)
        assert abs(p - P_VALUE_TWO) < 1e-6

    def test_reject_h0_at_alpha_05_but_not_01(self):
        """p=0.0455 < 0.05 -> reject; p=0.0455 > 0.01 -> fail to reject."""
        m = _i()
        p = m.p_value_two_tailed(Z_STAT)
        assert m.reject_h0(p, ALPHA_05) is True
        assert m.reject_h0(p, ALPHA_01) is False

    def test_power_definition(self):
        """Power = 1 - beta."""
        m = _i()
        assert abs(m.power(0.20) - 0.80) < 1e-9
        assert abs(m.power(0.0) - 1.0) < 1e-9
