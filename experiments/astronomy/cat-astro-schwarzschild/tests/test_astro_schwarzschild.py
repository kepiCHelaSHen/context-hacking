"""cat-astro-schwarzschild — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_schwarzschild_constants import *
IMPL = Path(__file__).parent.parent / "astro_schwarzschild.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three documented LLM failure modes."""

    def test_factor_of_2_present(self):
        """CRITICAL: r_s must be 2GM/c², NOT GM/c²."""
        m = _i(); rs = m.schwarzschild_radius(M_SUN)
        # Must match 2GM/c² (≈2953.8 m), NOT GM/c² (≈1476.9 m)
        assert abs(rs - RS_SUN) / RS_SUN < 1e-4, f"Got {rs}, expected {RS_SUN} (factor of 2 missing?)"
        assert rs > RS_SUN_WRONG * 1.5, "Result is too close to GM/c² — missing factor of 2!"

    def test_c_squared_not_c(self):
        """Denominator must be c², not c."""
        m = _i(); rs = m.schwarzschild_radius(M_SUN)
        wrong_c = 2 * G * M_SUN / C  # uses c instead of c²
        assert abs(rs - wrong_c) / wrong_c > 0.1, "Got r_s ~ 2GM/c — should be 2GM/c²"

    def test_result_in_meters(self):
        """Result must be in meters, not km."""
        m = _i(); rs = m.schwarzschild_radius(M_SUN)
        # Correct is ~2954 m; if in km it would be ~2.954
        assert rs > 100, f"r_s(Sun) = {rs} — too small, probably in km instead of m"


class TestCorrectness:
    """Verify numerical accuracy against precomputed constants."""

    def test_sun_schwarzschild(self):
        m = _i(); rs = m.schwarzschild_radius(M_SUN)
        assert abs(rs - RS_SUN) / RS_SUN < 1e-4

    def test_earth_schwarzschild(self):
        m = _i(); rs = m.schwarzschild_radius(M_EARTH)
        assert abs(rs - RS_EARTH) / RS_EARTH < 1e-4

    def test_sgr_a_star(self):
        m = _i(); rs = m.schwarzschild_radius(M_SGR_A_STAR)
        assert abs(rs - RS_SGR_A_STAR) / RS_SGR_A_STAR < 1e-4

    def test_solar_masses_helper(self):
        m = _i()
        rs_direct = m.schwarzschild_radius(M_SUN)
        rs_helper = m.schwarzschild_solar_masses(1.0)
        assert abs(rs_direct - rs_helper) < 0.01

    def test_scaling_linear_in_mass(self):
        """r_s ∝ M — doubling mass doubles radius."""
        m = _i()
        rs1 = m.schwarzschild_radius(M_SUN)
        rs2 = m.schwarzschild_radius(2 * M_SUN)
        assert abs(rs2 / rs1 - 2.0) < 1e-10

    def test_is_black_hole_true(self):
        """Object smaller than its Schwarzschild radius → black hole."""
        m = _i(); assert m.is_black_hole(M_SUN, 1000)  # 1 km < 2.95 km

    def test_is_black_hole_false(self):
        """Object larger than its Schwarzschild radius → not a black hole."""
        m = _i(); assert not m.is_black_hole(M_SUN, 7e8)  # Sun's actual radius ~ 696000 km
