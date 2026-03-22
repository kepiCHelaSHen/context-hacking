"""cat-eng-thermal-expansion — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_thermal_expansion_constants import *
IMPL = Path(__file__).parent.parent / "eng_thermal_expansion.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Catch the 3 documented LLM errors."""

    def test_volume_uses_3alpha_not_alpha(self):
        """PRIOR_ERROR: volume_uses_alpha — must use 3*alpha, not alpha."""
        m = _i()
        dV = m.volumetric_expansion(ALPHA_STEEL, V0_STEEL, DT_TEST)
        # Correct answer is 3x the wrong answer
        assert abs(dV - DV_STEEL_CORRECT) < 1e-10
        assert abs(dV - DV_STEEL_WRONG) > 1e-10  # must NOT match the wrong value

    def test_area_uses_2alpha_not_alpha(self):
        """PRIOR_ERROR: area_uses_alpha — must use 2*alpha, not alpha."""
        m = _i()
        dA = m.area_expansion(ALPHA_STEEL, A0_STEEL, DT_TEST)
        assert abs(dA - DA_STEEL_CORRECT) < 1e-10
        assert abs(dA - DA_STEEL_WRONG) > 1e-10  # must NOT match the wrong value

    def test_cooling_negative_dT(self):
        """PRIOR_ERROR: delta_t_sign — cooling must produce negative expansion (contraction)."""
        m = _i()
        dL = m.linear_expansion(ALPHA_STEEL, L0_STEEL, -50.0)
        assert dL < 0, "Cooling (negative dT) must give negative dL"

class TestCorrectness:
    """Verify formulas against frozen constants."""

    def test_linear_expansion_steel(self):
        m = _i()
        dL = m.linear_expansion(ALPHA_STEEL, L0_STEEL, DT_TEST)
        assert abs(dL - DL_STEEL) < 1e-12

    def test_volumetric_expansion_steel(self):
        m = _i()
        dV = m.volumetric_expansion(ALPHA_STEEL, V0_STEEL, DT_TEST)
        assert abs(dV - DV_STEEL_CORRECT) < 1e-12

    def test_area_expansion_steel(self):
        m = _i()
        dA = m.area_expansion(ALPHA_STEEL, A0_STEEL, DT_TEST)
        assert abs(dA - DA_STEEL_CORRECT) < 1e-12

    def test_volumetric_coefficient(self):
        m = _i()
        beta = m.volumetric_coefficient(ALPHA_STEEL)
        assert abs(beta - BETA_STEEL) < 1e-15

    def test_volume_is_3x_linear(self):
        """Volumetric expansion must be exactly 3x linear for same-dimension input."""
        m = _i()
        dL = m.linear_expansion(ALPHA_STEEL, 1.0, DT_TEST)
        dV = m.volumetric_expansion(ALPHA_STEEL, 1.0, DT_TEST)
        assert abs(dV / dL - 3.0) < 1e-10

    def test_area_is_2x_linear(self):
        """Area expansion must be exactly 2x linear for same-dimension input."""
        m = _i()
        dL = m.linear_expansion(ALPHA_STEEL, 1.0, DT_TEST)
        dA = m.area_expansion(ALPHA_STEEL, 1.0, DT_TEST)
        assert abs(dA / dL - 2.0) < 1e-10

    def test_aluminum_linear(self):
        """Cross-check with aluminum."""
        m = _i()
        dL = m.linear_expansion(ALPHA_ALUMINUM, 2.0, 50.0)
        expected = 23e-6 * 2.0 * 50.0  # = 0.0023 m
        assert abs(dL - expected) < 1e-12

    def test_copper_volumetric(self):
        """Cross-check with copper."""
        m = _i()
        dV = m.volumetric_expansion(ALPHA_COPPER, 0.5, 200.0)
        expected = 3 * 17e-6 * 0.5 * 200.0  # = 0.0051 m^3
        assert abs(dV - expected) < 1e-12
