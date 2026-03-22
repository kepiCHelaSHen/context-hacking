"""cat-bio-goldman-equation — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_goldman_equation_constants import *
IMPL = Path(__file__).parent.parent / "bio_goldman_equation.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_vm_is_near_minus75_not_minus21(self):
        """V_m ≈ -75 mV with correct Cl⁻ handling. If Cl⁻ is treated like a cation
        (cl_like_cation error), you get ≈ -21 mV — far too depolarized."""
        m = _i()
        V_m = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
        assert math.isclose(V_m, V_M_REST, rel_tol=1e-6), \
            f"V_m={V_m:.2f} mV, expected {V_M_REST:.2f} mV"
        # Must NOT be close to the wrong-Cl value
        assert abs(V_m - V_M_WRONG_CL) > 40.0, \
            f"V_m={V_m:.2f} mV is suspiciously close to wrong-Cl value {V_M_WRONG_CL:.2f} mV"

    def test_cl_goes_reversed_in_ghk(self):
        """Cl⁻ (anion) must be reversed: [Cl]_i in numerator, [Cl]_o in denominator.
        This catches the cl_like_cation error directly by checking numerator/denominator."""
        m = _i()
        num = m.ghk_numerator(P_K, K_O, P_NA, NA_O, P_CL, CL_I)
        den = m.ghk_denominator(P_K, K_I, P_NA, NA_I, P_CL, CL_O)
        # Correct: num uses Cl_i=4, den uses Cl_o=120
        assert math.isclose(num, GHK_NUMERATOR, rel_tol=1e-9), \
            f"Numerator={num}, expected {GHK_NUMERATOR} — Cl_i should be in numerator"
        assert math.isclose(den, GHK_DENOMINATOR, rel_tol=1e-9), \
            f"Denominator={den}, expected {GHK_DENOMINATOR} — Cl_o should be in denominator"
        # Verify that swapping would give wrong result
        num_wrong = P_K * K_O + P_NA * NA_O + P_CL * CL_O  # Cl_o in num (WRONG)
        assert not math.isclose(num, num_wrong, rel_tol=0.1), \
            "Numerator looks like Cl was treated as a cation"

    def test_permeabilities_matter(self):
        """Using equal permeabilities (permeability_ignored) gives a very different V_m.
        P_K:P_Na:P_Cl = 1:0.04:0.45 at rest — not 1:1:1."""
        m = _i()
        V_correct = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
        V_equal_p = m.goldman_potential(1.0, K_O, K_I, 1.0, NA_O, NA_I, 1.0, CL_O, CL_I, T)
        assert not math.isclose(V_correct, V_equal_p, abs_tol=5.0), \
            f"V_correct={V_correct:.2f} should differ from V_equal_P={V_equal_p:.2f}"

    def test_missing_anion_detected(self):
        """If Cl⁻ is omitted entirely (missing_anion), V_m ≈ -71 mV instead of ≈ -75 mV.
        The difference is detectable."""
        m = _i()
        V_with_cl = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
        V_no_cl   = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, 0.0,  CL_O, CL_I, T)
        assert not math.isclose(V_with_cl, V_no_cl, abs_tol=1.0), \
            f"V_with_cl={V_with_cl:.2f} should differ from V_no_cl={V_no_cl:.2f}"
        assert math.isclose(V_no_cl, V_M_NO_CL, rel_tol=1e-6), \
            f"V_no_cl={V_no_cl:.2f} should match frozen V_M_NO_CL={V_M_NO_CL:.2f}"


class TestCorrectness:
    def test_numerator(self):
        """GHK numerator = P_K*[K]_o + P_Na*[Na]_o + P_Cl*[Cl]_i = 11.6."""
        m = _i()
        num = m.ghk_numerator(P_K, K_O, P_NA, NA_O, P_CL, CL_I)
        assert math.isclose(num, GHK_NUMERATOR, rel_tol=1e-9), \
            f"Numerator={num}, expected {GHK_NUMERATOR}"

    def test_denominator(self):
        """GHK denominator = P_K*[K]_i + P_Na*[Na]_i + P_Cl*[Cl]_o = 194.48."""
        m = _i()
        den = m.ghk_denominator(P_K, K_I, P_NA, NA_I, P_CL, CL_O)
        assert math.isclose(den, GHK_DENOMINATOR, rel_tol=1e-9), \
            f"Denominator={den}, expected {GHK_DENOMINATOR}"

    def test_vm_value(self):
        """V_m ≈ -75.35 mV for standard mammalian neuron concentrations."""
        m = _i()
        V_m = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
        assert math.isclose(V_m, V_M_REST, rel_tol=1e-6), \
            f"V_m={V_m:.4f} mV, expected {V_M_REST:.4f} mV"

    def test_vm_without_cl(self):
        """With P_Cl=0, V_m is computed from K⁺ and Na⁺ only ≈ -71.16 mV."""
        m = _i()
        V_m = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, 0.0, CL_O, CL_I, T)
        assert math.isclose(V_m, V_M_NO_CL, rel_tol=1e-6), \
            f"V_m(no Cl)={V_m:.4f} mV, expected {V_M_NO_CL:.4f} mV"

    def test_vm_is_negative(self):
        """Resting membrane potential must be negative."""
        m = _i()
        V_m = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
        assert V_m < 0, f"V_m={V_m:.2f} mV should be negative"

    def test_temperature_dependence(self):
        """Higher temperature increases RT/F, scaling V_m proportionally."""
        m = _i()
        V_37 = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, 310.15)
        V_25 = m.goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, 298.15)
        # V scales with T: V_37/V_25 ≈ 310.15/298.15
        ratio = V_37 / V_25
        expected_ratio = 310.15 / 298.15
        assert math.isclose(ratio, expected_ratio, rel_tol=1e-6), \
            f"V_m ratio={ratio:.4f}, expected T ratio={expected_ratio:.4f}"
