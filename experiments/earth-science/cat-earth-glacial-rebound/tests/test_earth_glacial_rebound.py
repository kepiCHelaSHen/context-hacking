"""cat-earth-glacial-rebound — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_glacial_rebound_constants import *
IMPL = Path(__file__).parent.parent / "earth_glacial_rebound.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three known LLM errors."""

    def test_viscosity_correct_order(self):
        """PRIOR_ERROR: viscosity_wrong_order — must be 10^21, not 10^18 or 10^24."""
        m = _i()
        order = m.mantle_viscosity_order()
        assert order == 21, f"Mantle viscosity order should be 21, got {order}"

    def test_exponential_not_linear(self):
        """PRIOR_ERROR: linear_not_exponential — rebound must be exponential decay."""
        m = _i()
        d0 = 1000.0
        tau = 4000.0
        # At t=tau, exponential gives d0*exp(-1) ~ 367.9 m
        # Linear would give d0 - d0/tau*tau = 0 (or some other wrong value)
        d_at_tau = m.rebound_remaining(d0, tau, tau)
        expected = d0 * math.exp(-1)
        assert abs(d_at_tau - expected) < 0.1, (
            f"At t=tau, rebound should be {expected:.1f} m (exponential), got {d_at_tau:.1f}"
        )
        # Also check at t=2*tau: should be d0*exp(-2) ~ 135.3 m, NOT zero or negative
        d_at_2tau = m.rebound_remaining(d0, 2 * tau, tau)
        expected_2tau = d0 * math.exp(-2)
        assert abs(d_at_2tau - expected_2tau) < 0.1, (
            f"At t=2*tau, rebound should be {expected_2tau:.1f} m, got {d_at_2tau:.1f}"
        )

    def test_density_ratio_not_inverted(self):
        """PRIOR_ERROR: density_ratio_inverted — must use rho_ice/rho_mantle, NOT rho_mantle/rho_ice."""
        m = _i()
        d = m.depression_depth(3000.0)
        # Correct: 3000 * 917/3300 = 833.6 m
        # Inverted: 3000 * 3300/917 = 10796 m (absurd — deeper than ice!)
        assert d < 3000.0, f"Depression {d:.1f} m exceeds ice thickness — ratio inverted!"
        expected = 3000.0 * RHO_ICE / RHO_MANTLE
        assert abs(d - expected) < 0.1, f"Depression should be {expected:.1f} m, got {d:.1f}"


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_depression_depth_basic(self):
        m = _i()
        d = m.depression_depth(TEST_H_ICE)
        assert abs(d - TEST_D0) < 0.01, f"Expected {TEST_D0:.2f}, got {d:.2f}"

    def test_depression_depth_custom_densities(self):
        m = _i()
        d = m.depression_depth(2000.0, rho_ice=900, rho_mantle=3300)
        expected = 2000.0 * 900 / 3300
        assert abs(d - expected) < 0.01

    def test_rebound_remaining_at_zero(self):
        """At t=0, full depression remains."""
        m = _i()
        d = m.rebound_remaining(TEST_D0, 0.0, TEST_TAU)
        assert abs(d - TEST_D0) < 0.01

    def test_rebound_remaining_at_test_t(self):
        m = _i()
        d = m.rebound_remaining(TEST_D0, TEST_T, TEST_TAU)
        assert abs(d - TEST_REBOUND_REMAINING) < 0.1, (
            f"Expected {TEST_REBOUND_REMAINING:.1f} m, got {d:.1f}"
        )

    def test_uplift_rate_at_zero(self):
        """Initial uplift rate = d0/tau."""
        m = _i()
        rate = m.uplift_rate(TEST_D0, 0.0, TEST_TAU)
        assert abs(rate - TEST_UPLIFT_RATE_T0) < 1e-4, (
            f"Expected {TEST_UPLIFT_RATE_T0:.4f} m/yr, got {rate:.4f}"
        )

    def test_uplift_rate_at_test_t(self):
        m = _i()
        rate = m.uplift_rate(TEST_D0, TEST_T, TEST_TAU)
        assert abs(rate - TEST_UPLIFT_RATE_T) < 1e-4

    def test_uplift_rate_decreases_with_time(self):
        """Uplift rate should decrease monotonically."""
        m = _i()
        prev = m.uplift_rate(TEST_D0, 0.0, TEST_TAU)
        for t in range(1000, 20001, 1000):
            cur = m.uplift_rate(TEST_D0, float(t), TEST_TAU)
            assert cur < prev, f"Uplift rate not decreasing at t={t}"
            prev = cur

    def test_rebound_approaches_zero(self):
        """After many relaxation times, depression should be negligible."""
        m = _i()
        d = m.rebound_remaining(TEST_D0, 10 * TEST_TAU, TEST_TAU)
        assert d < 0.1, f"After 10*tau, depression should be ~0, got {d:.4f}"

    def test_depression_proportional_to_ice(self):
        """Depression scales linearly with ice thickness."""
        m = _i()
        d1 = m.depression_depth(1000.0)
        d2 = m.depression_depth(2000.0)
        assert abs(d2 / d1 - 2.0) < 1e-10
