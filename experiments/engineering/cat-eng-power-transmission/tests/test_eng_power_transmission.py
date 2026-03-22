"""cat-eng-power-transmission — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_power_transmission_constants import *
IMPL = Path(__file__).parent.parent / "eng_power_transmission.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_ratio_uses_radians_not_degrees(self):
        """theta must be in RADIANS. Using degrees gives e^54 ~ 2.83e23 (absurd!)."""
        m = _i(); ratio = m.tension_ratio(MU_REF, THETA_RAD_REF)
        assert abs(ratio - RATIO_REF) / RATIO_REF < 1e-9
        assert ratio < 100, f"Ratio = {ratio:.4e} — likely using degrees instead of radians!"

    def test_ratio_not_astronomically_large(self):
        """Sanity: for mu=0.3, theta=pi, ratio should be ~2.57, not ~10^23."""
        m = _i(); ratio = m.tension_ratio(MU_REF, THETA_RAD_REF)
        assert 2.0 < ratio < 5.0, f"Expected ~2.57, got {ratio:.4e}"

    def test_t1_greater_than_t2(self):
        """T1 (tight side) must be GREATER than T2 (slack side)."""
        m = _i(); T1 = m.tight_side_tension(T2_REF, MU_REF, THETA_RAD_REF)
        assert T1 > T2_REF, f"T1={T1:.2f} should be > T2={T2_REF:.2f} — sides may be swapped!"

    def test_t1_not_swapped(self):
        """Swapping T1/T2 gives T1 = T2/ratio ~ 194.8 N — must not be less than T2."""
        m = _i(); T1 = m.tight_side_tension(T2_REF, MU_REF, THETA_RAD_REF)
        assert abs(T1 - T1_REF) / T1_REF < 1e-9
        assert abs(T1 - T1_SWAPPED) > 100, "T1 and T2 appear to be swapped!"

    def test_power_uses_tension_difference(self):
        """P = (T1-T2)*v, NOT P = T1*v. Using T1 alone overstates power."""
        m = _i(); P = m.belt_power(T1_REF, T2_REF, V_REF)
        assert abs(P - P_REF) / P_REF < 1e-9
        assert abs(P - P_WRONG_T1_ONLY) > 100, "Using P=T1*v instead of P=(T1-T2)*v!"

    def test_power_not_using_t1_only(self):
        """If T2 is changed, power should change — proves (T1-T2)*v is used."""
        m = _i()
        P_a = m.belt_power(1000.0, 400.0, 10.0)  # (1000-400)*10 = 6000
        P_b = m.belt_power(1000.0, 200.0, 10.0)  # (1000-200)*10 = 8000
        assert abs(P_a - 6000.0) < 1e-9
        assert abs(P_b - 8000.0) < 1e-9
        assert P_a != P_b, "Power unchanged when T2 changed — likely using P=T1*v"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_wrap_angle_90(self):
        m = _i(); assert abs(m.wrap_angle_rad(90) - WRAP_90_RAD) < 1e-12

    def test_wrap_angle_180(self):
        m = _i(); assert abs(m.wrap_angle_rad(180) - WRAP_180_RAD) < 1e-12

    def test_wrap_angle_270(self):
        m = _i(); assert abs(m.wrap_angle_rad(270) - WRAP_270_RAD) < 1e-12

    def test_wrap_angle_360(self):
        m = _i(); assert abs(m.wrap_angle_rad(360) - 2.0 * math.pi) < 1e-12

    def test_tension_ratio_value(self):
        m = _i(); ratio = m.tension_ratio(MU_REF, THETA_RAD_REF)
        expected = math.exp(0.3 * math.pi)
        assert abs(ratio - expected) < 1e-12

    def test_tension_ratio_zero_friction(self):
        """mu=0: ratio should be 1 (no friction, equal tensions)."""
        m = _i(); ratio = m.tension_ratio(0.0, math.pi)
        assert abs(ratio - 1.0) < 1e-12

    def test_tension_ratio_increases_with_mu(self):
        m = _i()
        r1 = m.tension_ratio(0.2, math.pi)
        r2 = m.tension_ratio(0.4, math.pi)
        assert r2 > r1, "Higher friction should give higher tension ratio"

    def test_tension_ratio_increases_with_theta(self):
        m = _i()
        r1 = m.tension_ratio(0.3, math.pi / 2)
        r2 = m.tension_ratio(0.3, math.pi)
        assert r2 > r1, "Larger wrap angle should give higher tension ratio"

    def test_tight_side_tension_value(self):
        m = _i(); T1 = m.tight_side_tension(T2_REF, MU_REF, THETA_RAD_REF)
        assert abs(T1 - T1_REF) / T1_REF < 1e-9

    def test_tight_side_tension_manual(self):
        """T1 = 500 * e^(0.3*pi) = 500 * 2.5663... = 1283.17 N."""
        m = _i(); T1 = m.tight_side_tension(500.0, 0.3, math.pi)
        assert abs(T1 - 500.0 * math.exp(0.3 * math.pi)) < 1e-6

    def test_belt_power_value(self):
        m = _i(); P = m.belt_power(T1_REF, T2_REF, V_REF)
        assert abs(P - P_REF) / P_REF < 1e-9

    def test_belt_power_manual(self):
        """P = (1283.17 - 500) * 10 = 7831.66 W."""
        m = _i(); P = m.belt_power(1283.17, 500.0, 10.0)
        assert abs(P - (1283.17 - 500.0) * 10.0) < 1e-6

    def test_belt_power_zero_speed(self):
        """At v=0, no power transmitted regardless of tension."""
        m = _i(); P = m.belt_power(1000.0, 500.0, 0.0)
        assert P == 0.0

    def test_belt_power_proportional_to_speed(self):
        """Doubling speed should double power."""
        m = _i()
        P1 = m.belt_power(1000.0, 400.0, 5.0)
        P2 = m.belt_power(1000.0, 400.0, 10.0)
        assert abs(P2 / P1 - 2.0) < 1e-12
