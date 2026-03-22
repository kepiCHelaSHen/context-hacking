"""cat-bio-logistic-growth — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_logistic_growth_constants import *
IMPL = Path(__file__).parent.parent / "bio_logistic_growth.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_inflection_at_half_K_not_K(self):
        """The #1 LLM error: claiming inflection at N=K instead of N=K/2."""
        m = _i()
        infl = m.inflection_N(K)
        assert math.isclose(infl, K / 2, rel_tol=1e-9), (
            f"Inflection should be K/2={K/2}, got {infl}"
        )
        assert not math.isclose(infl, K, rel_tol=1e-2), (
            f"Got inflection at K={K} — wrong! Should be K/2"
        )

    def test_max_growth_rate_is_rK_over_4(self):
        """Max growth rate is rK/4, occurring at N=K/2, NOT at small N."""
        m = _i()
        mg = m.max_growth_rate(R, K)
        assert math.isclose(mg, R * K / 4, rel_tol=1e-9), (
            f"Max growth rate should be rK/4={R*K/4}, got {mg}"
        )
        # Confirm dN/dt at K/2 equals the max
        rate_at_half = m.logistic_dNdt(R, K, K / 2)
        assert math.isclose(rate_at_half, mg, rel_tol=1e-9), (
            f"dN/dt at K/2 should equal max={mg}, got {rate_at_half}"
        )

    def test_max_rate_not_at_small_N(self):
        """Growth rate at N=K/2 must exceed growth rate near N=0."""
        m = _i()
        rate_small = m.logistic_dNdt(R, K, 1)   # near zero
        rate_half = m.logistic_dNdt(R, K, K / 2)
        assert rate_half > rate_small, (
            f"Rate at K/2={rate_half} should exceed rate near 0={rate_small}"
        )


class TestCorrectness:
    def test_N_at_10(self):
        m = _i()
        n10 = m.logistic_N(R, K, N0, 10)
        assert math.isclose(n10, N_AT_10, rel_tol=1e-6), (
            f"N(10) should be {N_AT_10:.4f}, got {n10:.4f}"
        )

    def test_N_at_20(self):
        m = _i()
        n20 = m.logistic_N(R, K, N0, 20)
        assert math.isclose(n20, N_AT_20, rel_tol=1e-6), (
            f"N(20) should be {N_AT_20:.4f}, got {n20:.4f}"
        )

    def test_dNdt_at_100(self):
        m = _i()
        rate = m.logistic_dNdt(R, K, 100)
        assert math.isclose(rate, DNDT_AT_100, rel_tol=1e-9), (
            f"dN/dt at N=100 should be {DNDT_AT_100}, got {rate}"
        )

    def test_dNdt_at_500(self):
        m = _i()
        rate = m.logistic_dNdt(R, K, 500)
        assert math.isclose(rate, DNDT_AT_500, rel_tol=1e-9), (
            f"dN/dt at N=500 should be {DNDT_AT_500}, got {rate}"
        )

    def test_dNdt_at_900(self):
        m = _i()
        rate = m.logistic_dNdt(R, K, 900)
        assert math.isclose(rate, DNDT_AT_900, rel_tol=1e-9), (
            f"dN/dt at N=900 should be {DNDT_AT_900}, got {rate}"
        )

    def test_dNdt_symmetry(self):
        """dN/dt at N and K-N should be equal (equidistant from K/2)."""
        m = _i()
        rate_low = m.logistic_dNdt(R, K, 200)
        rate_high = m.logistic_dNdt(R, K, 800)
        assert math.isclose(rate_low, rate_high, rel_tol=1e-9), (
            f"dN/dt at 200={rate_low} should equal dN/dt at 800={rate_high}"
        )

    def test_N_approaches_K(self):
        """At large t, N(t) should approach carrying capacity K."""
        m = _i()
        n_large = m.logistic_N(R, K, N0, 100)
        assert math.isclose(n_large, K, rel_tol=1e-6), (
            f"N(100) should approach K={K}, got {n_large}"
        )

    def test_N_at_0_equals_N0(self):
        """N(0) should equal initial population N0."""
        m = _i()
        n0 = m.logistic_N(R, K, N0, 0)
        assert math.isclose(n0, N0, rel_tol=1e-9), (
            f"N(0) should be N0={N0}, got {n0}"
        )
