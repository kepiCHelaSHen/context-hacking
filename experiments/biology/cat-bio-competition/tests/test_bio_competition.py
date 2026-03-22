"""cat-bio-competition — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_competition_constants import *
IMPL = Path(__file__).parent.parent / "bio_competition.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_coexistence_requires_both_conditions(self):
        """Both α₁₂ < K₁/K₂ AND α₂₁ < K₂/K₁ must hold — not just one."""
        m = _i()
        # Both conditions met → coexist
        assert m.can_coexist(K1, K2, ALPHA12, ALPHA21) is True
        # Fail condition 1 only: α₁₂ > K₁/K₂ but α₂₁ < K₂/K₁
        assert m.can_coexist(K1, K2, 1.5, 0.6) is False, \
            "Only one condition met (α₂₁ ok, α₁₂ fails) — must return False"
        # Fail condition 2 only: α₁₂ < K₁/K₂ but α₂₁ > K₂/K₁
        assert m.can_coexist(K1, K2, 0.5, 0.9) is False, \
            "Only one condition met (α₁₂ ok, α₂₁ fails) — must return False"

    def test_non_coexistence_case(self):
        """When both conditions fail, species cannot stably coexist."""
        m = _i()
        assert m.can_coexist(K1, K2, ALPHA12_NO, ALPHA21_NO) is False

    def test_coexistence_direction_not_reversed(self):
        """Catches wrong_coexistence_direction: must be α < K_i/K_j, not >."""
        m = _i()
        # α₁₂=0.5 < K₁/K₂=1.25 → species 1 coexists
        # If direction is reversed, the function would wrongly require α > K_i/K_j
        # and would return False for our coexistence case
        assert m.can_coexist(K1, K2, ALPHA12, ALPHA21) is True
        # With very large alphas (clearly no coexistence), reversed logic would say True
        assert m.can_coexist(K1, K2, 5.0, 5.0) is False, \
            "Large alphas → no coexistence; if True, inequality direction is reversed"


class TestCorrectness:
    def test_equilibrium_N1_star(self):
        m = _i()
        n1s, _ = m.equilibrium(K1, K2, ALPHA12, ALPHA21)
        assert math.isclose(n1s, N1_STAR, rel_tol=1e-9), \
            f"N1*={n1s}, expected {N1_STAR}"

    def test_equilibrium_N2_star(self):
        m = _i()
        _, n2s = m.equilibrium(K1, K2, ALPHA12, ALPHA21)
        assert math.isclose(n2s, N2_STAR, rel_tol=1e-9), \
            f"N2*={n2s}, expected {N2_STAR}"

    def test_growth_rate_species1(self):
        m = _i()
        rate = m.dN1_dt(R1, 100, 50, K1, ALPHA12)
        assert math.isclose(rate, DN1DT_AT_100_50, rel_tol=1e-9), \
            f"dN1/dt={rate}, expected {DN1DT_AT_100_50}"

    def test_growth_rate_species2(self):
        m = _i()
        rate = m.dN2_dt(R2, 50, 100, K2, ALPHA21)
        assert math.isclose(rate, DN2DT_AT_100_50, rel_tol=1e-9), \
            f"dN2/dt={rate}, expected {DN2DT_AT_100_50}"

    def test_coexistence_bool(self):
        m = _i()
        assert m.can_coexist(K1, K2, ALPHA12, ALPHA21) is COEXISTENCE_EXPECTED
        assert m.can_coexist(K1, K2, ALPHA12_NO, ALPHA21_NO) is COEXISTENCE_NO_EXPECTED

    def test_equilibrium_is_true_equilibrium(self):
        """At equilibrium, both growth rates should be zero."""
        m = _i()
        n1s, n2s = m.equilibrium(K1, K2, ALPHA12, ALPHA21)
        rate1 = m.dN1_dt(R1, n1s, n2s, K1, ALPHA12)
        rate2 = m.dN2_dt(R2, n2s, n1s, K2, ALPHA21)
        assert math.isclose(rate1, 0.0, abs_tol=1e-9), \
            f"dN1/dt at equilibrium should be 0, got {rate1}"
        assert math.isclose(rate2, 0.0, abs_tol=1e-9), \
            f"dN2/dt at equilibrium should be 0, got {rate2}"

    def test_equilibrium_raises_when_no_coexistence(self):
        """equilibrium() should raise when coexistence conditions not met."""
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium(K1, K2, ALPHA12_NO, ALPHA21_NO)
