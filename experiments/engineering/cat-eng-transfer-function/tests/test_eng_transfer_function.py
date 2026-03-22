"""cat-eng-transfer-function — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_transfer_function_constants import *
IMPL = Path(__file__).parent.parent / "eng_transfer_function.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Tests targeting the 3 known LLM failure modes."""

    def test_poles_not_swapped_with_zeros(self):
        """Zeros are roots of numerator, poles are roots of denominator."""
        m = _i()
        # Denominator s²+4s+3 → roots must be -1, -3 (the POLES)
        roots = m.find_roots_quadratic(QUAD_A, QUAD_B, QUAD_C)
        roots_sorted = sorted(roots)
        assert abs(roots_sorted[0] - POLES[1]) < 1e-10  # -3
        assert abs(roots_sorted[1] - POLES[0]) < 1e-10  # -1

    def test_rhp_zero_does_not_mean_unstable(self):
        """A system with RHP zero but LHP poles is STABLE."""
        m = _i()
        # H(s) = (s-5)/((s+1)(s+3)) → zero at +5 (RHP), poles at -1,-3 (LHP)
        # Must be stable because poles are all in LHP
        assert m.is_stable([-1.0, -3.0]) is True

    def test_dc_gain_at_s_zero_not_s_one(self):
        """DC gain = H(0), NOT H(1)."""
        m = _i()
        gain = m.dc_gain(NUM_COEFFS, DEN_COEFFS)
        assert abs(gain - DC_GAIN) < 1e-10

class TestStability:
    def test_stable_system(self):
        m = _i()
        assert m.is_stable(POLES) is True

    def test_unstable_system(self):
        m = _i()
        assert m.is_stable([UNSTABLE_POLE]) is False

    def test_marginal_imaginary_poles(self):
        """Poles on imaginary axis (Re=0) → NOT strictly stable."""
        m = _i()
        assert m.is_stable([complex(0, 1), complex(0, -1)]) is False

    def test_complex_poles_lhp(self):
        """Complex poles with negative real parts → stable."""
        m = _i()
        assert m.is_stable([complex(-1, 2), complex(-1, -2)]) is True

class TestQuadratic:
    def test_real_roots(self):
        m = _i()
        roots = m.find_roots_quadratic(QUAD_A, QUAD_B, QUAD_C)
        roots_sorted = sorted(roots)
        assert abs(roots_sorted[0] - (-3.0)) < 1e-10
        assert abs(roots_sorted[1] - (-1.0)) < 1e-10

    def test_complex_roots(self):
        """s² + 2s + 5 → roots = -1 ± 2j."""
        m = _i()
        roots = m.find_roots_quadratic(1.0, 2.0, 5.0)
        # Sort by imaginary part
        roots_sorted = sorted(roots, key=lambda r: r.imag)
        assert abs(roots_sorted[0] - complex(-1, -2)) < 1e-10
        assert abs(roots_sorted[1] - complex(-1, 2)) < 1e-10

    def test_repeated_root(self):
        """s² + 4s + 4 → double root at s = -2."""
        m = _i()
        roots = m.find_roots_quadratic(1.0, 4.0, 4.0)
        assert abs(roots[0] - (-2.0)) < 1e-10
        assert abs(roots[1] - (-2.0)) < 1e-10

class TestFactoredEvaluation:
    def test_at_zero(self):
        m = _i()
        val = m.pole_zero_from_factored(ZEROS, POLES, 0)
        assert abs(val - FACTORED_AT_ZERO) < 1e-10

    def test_at_neg_half(self):
        m = _i()
        val = m.pole_zero_from_factored(ZEROS, POLES, -0.5)
        assert abs(val - H_AT_NEG05) < 1e-10

    def test_dc_gain_matches(self):
        """Factored form at s=0 must equal polynomial DC gain."""
        m = _i()
        factored = m.pole_zero_from_factored(ZEROS, POLES, 0)
        poly = m.dc_gain(NUM_COEFFS, DEN_COEFFS)
        assert abs(factored - poly) < 1e-10
