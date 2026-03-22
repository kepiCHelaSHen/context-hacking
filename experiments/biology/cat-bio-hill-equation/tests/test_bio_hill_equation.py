"""cat-bio-hill-equation — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_hill_equation_constants import *
IMPL = Path(__file__).parent.parent / "bio_hill_equation.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_theta_at_kd_equals_half_for_any_n(self):
        """θ(Kd) must equal 0.5 regardless of Hill coefficient n."""
        m = _i()
        for n in [0.5, 1.0, 2.0, 2.8, 4.0, 10.0]:
            theta = m.hill_equation(KD, KD, n)
            assert math.isclose(theta, 0.5, rel_tol=1e-9), \
                f"θ(Kd) should be 0.5 for n={n}, got {theta}"

    def test_n_not_equal_to_binding_sites(self):
        """Hill coefficient n ≠ number of binding sites (n=2.8, sites=4 for hemoglobin)."""
        assert N_HILL != HEMO_SITES, \
            f"Hill coeff n={N_HILL} must NOT equal sites={HEMO_SITES}"
        # n should be less than the number of sites for hemoglobin
        assert N_HILL < HEMO_SITES, \
            f"For hemoglobin, n={N_HILL} should be < sites={HEMO_SITES}"

    def test_n1_is_not_sigmoidal(self):
        """With n=1, the curve is hyperbolic (Michaelis-Menten), not sigmoidal."""
        m = _i()
        coop = m.is_cooperative(1.0)
        assert coop == "none", \
            f"n=1 should give 'none' cooperativity, got '{coop}'"
        # With n=1, θ should be strictly concave (no inflection point)
        # Check: θ at evenly spaced L values should NOT show sigmoidal shape
        thetas = [m.hill_equation(L, KD, 1.0) for L in [2.5, 5.0, 7.5, 10.0]]
        # For hyperbolic: second differences should be negative (concave down)
        d1 = thetas[1] - thetas[0]
        d2 = thetas[2] - thetas[1]
        d3 = thetas[3] - thetas[2]
        assert d1 > d2 > d3, "n=1 should produce a concave-down (hyperbolic) curve"


class TestCorrectness:
    def test_hill_equation_at_L5(self):
        m = _i()
        theta = m.hill_equation(5.0, KD, N_HILL)
        assert math.isclose(theta, THETA_AT_5, rel_tol=1e-9), \
            f"θ(5)={theta}, expected {THETA_AT_5}"

    def test_hill_equation_at_L10(self):
        m = _i()
        theta = m.hill_equation(10.0, KD, N_HILL)
        assert math.isclose(theta, THETA_AT_10, rel_tol=1e-9), \
            f"θ(10)={theta}, expected {THETA_AT_10}"

    def test_hill_equation_at_L20(self):
        m = _i()
        theta = m.hill_equation(20.0, KD, N_HILL)
        assert math.isclose(theta, THETA_AT_20, rel_tol=1e-9), \
            f"θ(20)={theta}, expected {THETA_AT_20}"

    def test_cooperativity_positive(self):
        m = _i()
        assert m.is_cooperative(N_HILL) == "positive"
        assert m.is_cooperative(2.0) == "positive"

    def test_cooperativity_negative(self):
        m = _i()
        assert m.is_cooperative(0.5) == "negative"
        assert m.is_cooperative(0.1) == "negative"

    def test_cooperativity_none(self):
        m = _i()
        assert m.is_cooperative(1.0) == "none"

    def test_half_saturation_equals_kd(self):
        m = _i()
        assert m.half_saturation(KD) == KD
        assert m.half_saturation(50.0) == 50.0

    def test_theta_symmetry(self):
        """θ(Kd/k) + θ(Kd*k) = 1 for any k>0 and any n."""
        m = _i()
        for k in [2.0, 3.0, 5.0]:
            t_low = m.hill_equation(KD / k, KD, N_HILL)
            t_high = m.hill_equation(KD * k, KD, N_HILL)
            assert math.isclose(t_low + t_high, 1.0, rel_tol=1e-9), \
                f"θ({KD/k}) + θ({KD*k}) = {t_low+t_high}, expected 1.0"

    def test_theta_zero_at_L_zero(self):
        m = _i()
        theta = m.hill_equation(0.0, KD, N_HILL)
        assert theta == 0.0, f"θ(0) should be 0, got {theta}"
