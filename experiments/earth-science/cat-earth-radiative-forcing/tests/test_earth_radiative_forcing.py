"""cat-earth-radiative-forcing — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_radiative_forcing_constants import *
IMPL = Path(__file__).parent.parent / "earth_radiative_forcing.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Guard against known LLM confusions about radiative forcing."""

    def test_not_linear(self):
        """Prior error: linear_not_log — must use ln, not linear scaling."""
        m = _i()
        dF = m.radiative_forcing(C_CURRENT, C0)
        # Correct logarithmic result: 5.35 * ln(1.5) = 2.169
        # Wrong linear result: 5.35 * 0.5 = 2.675
        assert abs(dF - DF_TEST) < 0.01, (
            f"Expected {DF_TEST:.4f} (logarithmic), got {dF:.4f} — "
            f"if ~2.675, likely using linear formula"
        )
        assert abs(dF - DF_LINEAR_WRONG) > 0.1, (
            f"Got {dF:.4f} which matches the LINEAR formula ({DF_LINEAR_WRONG}) — must use ln(C/C0)"
        )

    def test_coefficient_is_5_35_not_3_7(self):
        """Prior error: wrong_coefficient — 3.7 is the doubling RESULT, not the coefficient."""
        m = _i()
        # If coefficient were 3.7 instead of 5.35:
        # dF = 3.7 * ln(1.5) = 3.7 * 0.4055 = 1.500
        dF_wrong = 3.7 * LN_RATIO_TEST  # ~1.500
        dF = m.radiative_forcing(C_CURRENT, C0)
        assert abs(dF - dF_wrong) > 0.3, (
            f"Got {dF:.4f} which matches coefficient=3.7 ({dF_wrong:.4f}) — "
            f"coefficient should be 5.35, not 3.7"
        )

    def test_uses_natural_log_not_log10(self):
        """Prior error: base10_not_natural — must use ln, not log10."""
        m = _i()
        # If using log10: dF = 5.35 * log10(1.5) = 5.35 * 0.17609 = 0.9421
        dF_log10 = ALPHA * math.log10(RATIO_TEST)  # ~0.942
        dF = m.radiative_forcing(C_CURRENT, C0)
        assert abs(dF - dF_log10) > 0.5, (
            f"Got {dF:.4f} which matches log10 formula ({dF_log10:.4f}) — must use ln, not log10"
        )

    def test_is_logarithmic_returns_true(self):
        """The relationship MUST be logarithmic."""
        m = _i()
        assert m.is_logarithmic() is True

class TestRadiativeForcing:
    def test_current_co2(self):
        """C=420, C0=280 -> dF = 5.35 * ln(1.5) = 2.169 W/m^2."""
        m = _i()
        dF = m.radiative_forcing(C_CURRENT, C0)
        assert abs(dF - DF_TEST) < 0.01, f"Expected {DF_TEST:.4f}, got {dF:.4f}"

    def test_preindustrial_is_zero(self):
        """At reference concentration, forcing is zero."""
        m = _i()
        dF = m.radiative_forcing(C0, C0)
        assert abs(dF) < 1e-10, f"dF at C=C0 should be 0, got {dF}"

    def test_doubling_symmetry(self):
        """Doubling from any base gives the same forcing increment."""
        m = _i()
        dF_280_560 = m.radiative_forcing(560, 280)
        dF_560_1120 = m.radiative_forcing(1120, 560)
        assert abs(dF_280_560 - dF_560_1120) < 0.001, (
            f"Doubling forcing not equal: {dF_280_560:.4f} vs {dF_560_1120:.4f}"
        )

    def test_negative_for_lower_co2(self):
        """CO2 below reference gives negative forcing."""
        m = _i()
        dF = m.radiative_forcing(200, C0)
        assert dF < 0, f"Forcing should be negative for C < C0, got {dF}"

class TestForcingDoubling:
    def test_doubling_value(self):
        """dF_2x = 5.35 * ln(2) = 3.708 W/m^2."""
        m = _i()
        dF2x = m.forcing_doubling()
        assert abs(dF2x - DF_DOUBLING) < 0.001, f"Expected {DF_DOUBLING:.4f}, got {dF2x:.4f}"

    def test_doubling_approx_3_7(self):
        """Standard result: ~3.7 W/m^2 for doubling."""
        m = _i()
        dF2x = m.forcing_doubling()
        assert 3.6 < dF2x < 3.8, f"Doubling forcing should be ~3.7, got {dF2x:.4f}"

    def test_consistent_with_radiative_forcing(self):
        """forcing_doubling() must equal radiative_forcing(2*C0, C0)."""
        m = _i()
        dF2x = m.forcing_doubling()
        dF_calc = m.radiative_forcing(2 * C0, C0)
        assert abs(dF2x - dF_calc) < 1e-10

class TestCO2ForForcing:
    def test_inverse_roundtrip(self):
        """co2_for_forcing(dF) should recover the original concentration."""
        m = _i()
        dF = m.radiative_forcing(C_CURRENT, C0)
        C_recovered = m.co2_for_forcing(dF, C0)
        assert abs(C_recovered - C_CURRENT) < 0.01, (
            f"Expected {C_CURRENT}, got {C_recovered:.4f}"
        )

    def test_zero_forcing_returns_c0(self):
        """Zero forcing means CO2 is at the reference level."""
        m = _i()
        C = m.co2_for_forcing(0.0, C0)
        assert abs(C - C0) < 1e-10

    def test_doubling_forcing_returns_double(self):
        """Forcing of dF_2x should give 2*C0."""
        m = _i()
        C = m.co2_for_forcing(DF_DOUBLING, C0)
        assert abs(C - 2 * C0) < 0.01, f"Expected {2*C0}, got {C:.4f}"

    def test_inverse_at_560(self):
        """co2_for_forcing at doubling forcing from C0=280 -> 560 ppm."""
        m = _i()
        C = m.co2_for_forcing(DF_DOUBLING, C0)
        assert abs(C - 560.0) < 0.1
