"""cat-eng-gear-ratios — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_gear_ratios_constants import *
IMPL = Path(__file__).parent.parent / "eng_gear_ratios.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_direction_reversed_odd_meshes(self):
        """1 external mesh MUST reverse direction — the #1 LLM error."""
        m = _i()
        assert m.rotation_reversed(1) is True, "1 mesh must reverse direction!"
        assert m.rotation_reversed(3) is True, "3 meshes (odd) must reverse direction!"

    def test_direction_same_even_meshes(self):
        """Even number of meshes -> same direction as input."""
        m = _i()
        assert m.rotation_reversed(2) is False, "2 meshes must NOT reverse direction!"
        assert m.rotation_reversed(4) is False, "4 meshes must NOT reverse direction!"

    def test_ratio_not_inverted(self):
        """GR must be N_driven/N_driver, NOT N_driver/N_driven."""
        m = _i(); GR = m.gear_ratio(N1, N2)
        assert abs(GR - GR_SIMPLE) < 1e-9
        assert abs(GR - GR_INVERTED) > 0.1, "Using N_driver/N_driven instead of N_driven/N_driver!"

    def test_speed_reduces_not_increases(self):
        """With GR=3 (reduction), output speed must be LESS than input."""
        m = _i(); w = m.output_speed(OMEGA_IN, N1, N2)
        assert w < OMEGA_IN, f"Output speed {w} >= input {OMEGA_IN} — should be reduced!"
        assert abs(w - OMEGA_OUT_WRONG) > 100, "Using inverted ratio — speed increased instead of decreased!"

    def test_torque_increases_with_reduction(self):
        """Speed reduction INCREASES torque — NOT decreases it."""
        m = _i()
        GR = m.gear_ratio(N1, N2)
        t_out = m.output_torque(TAU_IN_REF, GR)
        assert t_out > TAU_IN_REF, f"Output torque {t_out} <= input {TAU_IN_REF} — torque must increase!"
        assert abs(t_out - TAU_OUT_WRONG) > 1.0, "Dividing by GR instead of multiplying — torque wrongly decreases!"

    def test_gr_greater_than_one_for_reduction(self):
        """A speed-reducing gear pair must have GR > 1."""
        m = _i(); GR = m.gear_ratio(N1, N2)
        assert GR > 1.0, f"GR={GR} but N2>N1 means GR should be > 1 (speed reduction)"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_gear_ratio_value(self):
        m = _i(); GR = m.gear_ratio(N1, N2)
        assert abs(GR - 3.0) < 1e-9

    def test_gear_ratio_unity(self):
        """Equal teeth -> GR = 1."""
        m = _i(); assert abs(m.gear_ratio(30, 30) - 1.0) < 1e-9

    def test_output_speed_value(self):
        m = _i(); w = m.output_speed(OMEGA_IN, N1, N2)
        assert abs(w - OMEGA_OUT) / OMEGA_OUT < 1e-9

    def test_output_speed_exact(self):
        """1000 RPM with GR=3 -> 333.333... RPM."""
        m = _i(); w = m.output_speed(1000.0, 20, 60)
        assert abs(w - 1000.0 / 3.0) < 1e-9

    def test_output_torque_value(self):
        m = _i(); t = m.output_torque(TAU_IN_REF, GR_SIMPLE)
        assert abs(t - TAU_OUT_SIMPLE) < 1e-9

    def test_output_torque_exact(self):
        """10 N*m input with GR=3 -> 30 N*m output."""
        m = _i(); t = m.output_torque(10.0, 3.0)
        assert abs(t - 30.0) < 1e-9

    def test_rotation_reversed_zero_meshes(self):
        """0 meshes (same shaft) -> not reversed."""
        m = _i(); assert m.rotation_reversed(0) is False

    def test_compound_ratio_value(self):
        m = _i()
        pairs = [(NC1_DRIVER, NC1_DRIVEN), (NC2_DRIVER, NC2_DRIVEN)]
        GR = m.compound_ratio(pairs)
        assert abs(GR - GR_COMPOUND) < 1e-9

    def test_compound_ratio_exact(self):
        """(20->40)*(15->45) = 2*3 = 6."""
        m = _i()
        GR = m.compound_ratio([(20, 40), (15, 45)])
        assert abs(GR - 6.0) < 1e-9

    def test_compound_speed(self):
        """Compound GR=6: 1000 RPM -> 166.666... RPM."""
        m = _i()
        GR = m.compound_ratio([(NC1_DRIVER, NC1_DRIVEN), (NC2_DRIVER, NC2_DRIVEN)])
        w = m.output_speed(OMEGA_IN, 1, GR)
        assert abs(w - OMEGA_COMPOUND_OUT) / OMEGA_COMPOUND_OUT < 1e-9

    def test_compound_single_stage(self):
        """Single-stage compound should match simple gear_ratio."""
        m = _i()
        GR_s = m.gear_ratio(N1, N2)
        GR_c = m.compound_ratio([(N1, N2)])
        assert abs(GR_s - GR_c) < 1e-9

    def test_torque_proportional_to_gr(self):
        """Doubling GR should double output torque."""
        m = _i()
        t1 = m.output_torque(10.0, 2.0)
        t2 = m.output_torque(10.0, 4.0)
        assert abs(t2 / t1 - 2.0) < 1e-12

    def test_power_conservation(self):
        """Power in = Power out (ideal): tau_in * omega_in = tau_out * omega_out."""
        m = _i()
        GR = m.gear_ratio(N1, N2)
        w_out = m.output_speed(OMEGA_IN, N1, N2)
        t_out = m.output_torque(TAU_IN_REF, GR)
        P_in = TAU_IN_REF * OMEGA_IN
        P_out = t_out * w_out
        assert abs(P_in - P_out) / P_in < 1e-9, "Power not conserved — ideal gears must conserve power!"
