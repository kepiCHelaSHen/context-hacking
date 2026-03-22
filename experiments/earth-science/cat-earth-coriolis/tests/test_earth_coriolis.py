"""cat-earth-coriolis — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_coriolis_constants import *
IMPL = Path(__file__).parent.parent / "earth_coriolis.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three known LLM errors."""

    def test_equator_is_zero_not_max(self):
        """PRIOR_ERROR: max_at_equator — f must be ZERO at equator."""
        m = _i()
        f_eq = m.coriolis_parameter(0.0)
        assert f_eq == 0.0, f"Equator f should be 0, got {f_eq}"

    def test_pole_is_max_not_zero(self):
        """Pole should have MAXIMUM |f|, not zero."""
        m = _i()
        f_pole = m.coriolis_parameter(90.0)
        f_eq = m.coriolis_parameter(0.0)
        assert abs(f_pole) > abs(f_eq), "Pole f must exceed equator f"
        assert abs(f_pole - F_POLE_N) < 1e-10

    def test_sin_not_cos(self):
        """PRIOR_ERROR: cos_not_sin — at 0°, sin(0)=0 but cos(0)=1."""
        m = _i()
        # If cos were used, f(0) would be 2*Omega*cos(0) = 2*Omega ≠ 0
        assert m.coriolis_parameter(0.0) == 0.0
        # And f(90) would be 2*Omega*cos(90) = 0 instead of max
        assert abs(m.coriolis_parameter(90.0)) > 1e-5

    def test_correct_omega(self):
        """PRIOR_ERROR: wrong_omega — must use rotational Omega, not orbital."""
        m = _i()
        omega = m.omega_earth()
        # Earth orbital omega ~ 1.991e-7 rad/s — much smaller than rotational
        assert abs(omega - 7.2921e-5) < 1e-9, f"Wrong omega: {omega}"


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_f_at_30(self):
        m = _i()
        assert abs(m.coriolis_parameter(30.0) - F_30) < 1e-12

    def test_f_at_45(self):
        m = _i()
        assert abs(m.coriolis_parameter(45.0) - F_45) < 1e-12

    def test_f_at_poles_opposite_sign(self):
        m = _i()
        f_n = m.coriolis_parameter(90.0)
        f_s = m.coriolis_parameter(-90.0)
        assert f_n > 0 and f_s < 0, "N pole positive, S pole negative"
        assert abs(f_n + f_s) < 1e-12, "Magnitudes must be equal"

    def test_coriolis_acceleration(self):
        m = _i()
        a = m.coriolis_acceleration(F_30, TEST_V)
        assert abs(a - TEST_ACCEL) < 1e-10

    def test_deflection_nh_right(self):
        m = _i()
        assert m.deflection_direction(45.0) == "right"

    def test_deflection_sh_left(self):
        m = _i()
        assert m.deflection_direction(-45.0) == "left"

    def test_deflection_equator_none(self):
        m = _i()
        assert m.deflection_direction(0.0) == "none"

    def test_f_monotonic_0_to_90(self):
        """f should increase monotonically from equator to pole."""
        m = _i()
        prev = m.coriolis_parameter(0.0)
        for lat in range(5, 95, 5):
            cur = m.coriolis_parameter(lat)
            assert cur > prev, f"f not increasing at lat={lat}"
            prev = cur
