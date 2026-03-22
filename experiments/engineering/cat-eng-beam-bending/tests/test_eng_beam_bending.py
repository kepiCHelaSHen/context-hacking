"""cat-eng-beam-bending — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_beam_bending_constants import *
IMPL = Path(__file__).parent.parent / "eng_beam_bending.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_rect_I_not_bh_squared(self):
        """Rectangular I must be b*h^3/12, NOT b*h^2/12 — the #1 LLM error."""
        m = _i(); I = m.rect_I(B_REF, H_REF)
        assert abs(I - I_RECT_REF) / I_RECT_REF < 1e-9
        assert abs(I - I_RECT_WRONG_BH2) > 1e-6, "Using b*h^2/12 instead of b*h^3/12!"

    def test_rect_I_order_of_magnitude(self):
        """I should be ~4.17e-6, not ~4.17e-5 (the bh^2 error gives 10x too large)."""
        m = _i(); I = m.rect_I(B_REF, H_REF)
        assert I < 1e-5, "I is 10x too large — likely using b*h^2/12"
        assert I > 1e-7, "I is too small"

    def test_circular_I_not_polar_J(self):
        """Circular I = pi*d^4/64, NOT pi*d^4/32 (that's polar J)."""
        m = _i(); I = m.circular_I(D_REF)
        assert abs(I - I_CIRC_REF) / I_CIRC_REF < 1e-9
        assert abs(I - J_POLAR_WRONG) > 1e-7, "Using polar J (pi*d^4/32) instead of area I (pi*d^4/64)!"

    def test_circular_I_half_of_J(self):
        """Area moment I should be exactly half of polar moment J."""
        m = _i(); I = m.circular_I(D_REF)
        ratio = J_POLAR_WRONG / I
        assert abs(ratio - 2.0) < 1e-9, f"I should be half of J, got ratio {ratio}"

    def test_deflection_coefficient_48(self):
        """Simply-supported center load: delta = PL^3/(48EI), coefficient must be 48."""
        m = _i(); delta = m.simply_supported_deflection(P_REF, L_REF, E_REF, I_RECT_REF)
        assert abs(delta - DELTA_REF) / DELTA_REF < 1e-9
        # Check it's not using coefficient 24 (cantilevered) or 384 (distributed)
        delta_24 = P_REF * L_REF**3 / (24.0 * E_REF * I_RECT_REF)
        delta_384 = P_REF * L_REF**3 / (384.0 * E_REF * I_RECT_REF)
        assert abs(delta - delta_24) > 1e-6, "Using coefficient 24 instead of 48!"
        assert abs(delta - delta_384) > 1e-6, "Using coefficient 384 instead of 48!"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_rect_I_value(self):
        m = _i(); I = m.rect_I(B_REF, H_REF)
        expected = 0.05 * 0.001 / 12.0  # b*h^3/12 = 0.05*0.1^3/12
        assert abs(I - expected) < 1e-15

    def test_rect_I_unit_square(self):
        """Unit square b=h=1: I = 1/12."""
        m = _i(); I = m.rect_I(1.0, 1.0)
        assert abs(I - 1.0 / 12.0) < 1e-15

    def test_circular_I_value(self):
        m = _i(); I = m.circular_I(D_REF)
        expected = math.pi * 0.1**4 / 64.0
        assert abs(I - expected) < 1e-15

    def test_bending_stress_value(self):
        m = _i(); sigma = m.bending_stress(M_MAX_REF, Y_MAX_REF, I_RECT_REF)
        assert abs(sigma - SIGMA_MAX_REF) / SIGMA_MAX_REF < 1e-9

    def test_bending_stress_units(self):
        """With M=500 Nm, y=0.05 m, I=4.167e-6 m^4, stress should be ~6 MPa."""
        m = _i(); sigma = m.bending_stress(M_MAX_REF, Y_MAX_REF, I_RECT_REF)
        assert 5.9e6 < sigma < 6.1e6, f"Expected ~6 MPa, got {sigma/1e6:.2f} MPa"

    def test_deflection_value(self):
        m = _i(); delta = m.simply_supported_deflection(P_REF, L_REF, E_REF, I_RECT_REF)
        assert abs(delta - DELTA_REF) / DELTA_REF < 1e-9

    def test_deflection_magnitude(self):
        """1 kN on 2 m steel beam: deflection should be ~0.2 mm."""
        m = _i(); delta = m.simply_supported_deflection(P_REF, L_REF, E_REF, I_RECT_REF)
        assert 0.1e-3 < delta < 0.5e-3, f"Expected ~0.2 mm, got {delta*1000:.4f} mm"

    def test_deflection_not_with_wrong_I(self):
        """Deflection with correct I should differ from wrong-I result by 10x."""
        m = _i(); delta = m.simply_supported_deflection(P_REF, L_REF, E_REF, I_RECT_REF)
        ratio = delta / DELTA_WRONG_I
        assert abs(ratio - 10.0) < 1e-6, f"Expected 10x ratio, got {ratio}"

    def test_stress_proportional_to_moment(self):
        """Doubling M should double stress."""
        m = _i()
        s1 = m.bending_stress(100.0, Y_MAX_REF, I_RECT_REF)
        s2 = m.bending_stress(200.0, Y_MAX_REF, I_RECT_REF)
        assert abs(s2 / s1 - 2.0) < 1e-12
