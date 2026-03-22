"""cat-eng-darcy-weisbach — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_darcy_weisbach_constants import *
IMPL = Path(__file__).parent.parent / "eng_darcy_weisbach.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_darcy_not_fanning(self):
        """Darcy f_D = 64/Re, NOT 16/Re (Fanning)."""
        m = _i(); f_D = m.darcy_friction_laminar(RE_REF)
        assert abs(f_D - FD_REF) < 1e-12
        assert abs(f_D - FF_REF) > 0.01, "Returned Fanning f instead of Darcy f!"

    def test_fanning_not_darcy(self):
        """Fanning f_F = 16/Re, NOT 64/Re (Darcy)."""
        m = _i(); f_F = m.fanning_friction_laminar(RE_REF)
        assert abs(f_F - FF_REF) < 1e-12
        assert abs(f_F - FD_REF) > 0.01, "Returned Darcy f instead of Fanning f!"

    def test_darcy_fanning_ratio_is_4(self):
        """f_D / f_F must be exactly 4."""
        m = _i()
        f_D = m.darcy_friction_laminar(RE_REF)
        f_F = m.fanning_friction_laminar(RE_REF)
        assert abs(f_D / f_F - 4.0) < 1e-12, "Darcy/Fanning ratio must be 4!"

    def test_head_loss_uses_darcy_f(self):
        """Head loss with Darcy f must match reference, not the 4x-too-small Fanning result."""
        m = _i()
        f_D = m.darcy_friction_laminar(RE_REF)
        hf = m.head_loss_darcy(f_D, L_REF, D_PIPE_REF, V_REF, G_REF)
        assert abs(hf - HF_DARCY_REF) < 1e-10
        assert abs(hf - HF_FANNING_WRONG) > 0.1, "Head loss is 4x too small — Fanning f in Darcy equation?"

    def test_not_32_over_Re(self):
        """Darcy f must NOT be 32/Re (a common wrong formula)."""
        m = _i(); f_D = m.darcy_friction_laminar(RE_REF)
        assert abs(f_D - FD_WRONG_32) > 0.01, "Got 32/Re — neither Darcy (64/Re) nor Fanning (16/Re)!"

    def test_head_loss_g_not_imperial(self):
        """Head loss must use g=9.81 m/s^2, not 32.2 ft/s^2."""
        m = _i()
        f_D = m.darcy_friction_laminar(RE_REF)
        hf = m.head_loss_darcy(f_D, L_REF, D_PIPE_REF, V_REF, G_REF)
        # If g=32.2 were used, hf would be ~0.1987 (wrong)
        hf_imperial_g = f_D * (L_REF / D_PIPE_REF) * (V_REF**2 / (2.0 * 32.2))
        assert abs(hf - hf_imperial_g) > 0.1, "Looks like g=32.2 ft/s^2 was used instead of 9.81 m/s^2"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_darcy_friction_value(self):
        m = _i(); f_D = m.darcy_friction_laminar(RE_REF)
        assert abs(f_D - 0.064) < 1e-12

    def test_fanning_friction_value(self):
        m = _i(); f_F = m.fanning_friction_laminar(RE_REF)
        assert abs(f_F - 0.016) < 1e-12

    def test_head_loss_value(self):
        m = _i()
        hf = m.head_loss_darcy(FD_REF, L_REF, D_PIPE_REF, V_REF, G_REF)
        assert abs(hf - HF_DARCY_REF) < 1e-10

    def test_darcy_to_fanning_conversion(self):
        m = _i(); f_F = m.darcy_to_fanning(FD_REF)
        assert abs(f_F - FF_REF) < 1e-12

    def test_darcy_to_fanning_roundtrip(self):
        """darcy_to_fanning(darcy_friction_laminar(Re)) == fanning_friction_laminar(Re)."""
        m = _i()
        f_F_via_convert = m.darcy_to_fanning(m.darcy_friction_laminar(RE_REF))
        f_F_direct = m.fanning_friction_laminar(RE_REF)
        assert abs(f_F_via_convert - f_F_direct) < 1e-12

    def test_different_Re(self):
        """Test at Re=2000 (still laminar)."""
        m = _i()
        f_D = m.darcy_friction_laminar(2000.0)
        assert abs(f_D - 64.0 / 2000.0) < 1e-12
        f_F = m.fanning_friction_laminar(2000.0)
        assert abs(f_F - 16.0 / 2000.0) < 1e-12

    def test_head_loss_scales_with_length(self):
        """Doubling L doubles head loss."""
        m = _i()
        hf1 = m.head_loss_darcy(FD_REF, L_REF, D_PIPE_REF, V_REF, G_REF)
        hf2 = m.head_loss_darcy(FD_REF, 2 * L_REF, D_PIPE_REF, V_REF, G_REF)
        assert abs(hf2 / hf1 - 2.0) < 1e-10

    def test_head_loss_scales_with_v_squared(self):
        """Doubling v quadruples head loss."""
        m = _i()
        hf1 = m.head_loss_darcy(FD_REF, L_REF, D_PIPE_REF, V_REF, G_REF)
        hf2 = m.head_loss_darcy(FD_REF, L_REF, D_PIPE_REF, 2 * V_REF, G_REF)
        assert abs(hf2 / hf1 - 4.0) < 1e-10

    def test_head_loss_default_g(self):
        """head_loss_darcy uses g=9.81 by default."""
        m = _i()
        hf = m.head_loss_darcy(FD_REF, L_REF, D_PIPE_REF, V_REF)
        assert abs(hf - HF_DARCY_REF) < 1e-10
