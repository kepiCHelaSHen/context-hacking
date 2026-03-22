"""cat-earth-geostrophic-wind — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_geostrophic_wind_constants import *
IMPL = Path(__file__).parent.parent / "earth_geostrophic_wind.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_wind_parallel_to_isobars(self):
        """Catches 'wind_across_isobars' — wind must NOT cross isobars."""
        m = _i()
        assert m.wind_direction_nh() != "high to low"
        assert m.wind_direction_sh() != "high to low"
    def test_nh_sh_differ(self):
        """Catches 'nh_sh_same' — NH and SH must have opposite conventions."""
        m = _i()
        assert m.wind_direction_nh() != m.wind_direction_sh()
    def test_gradient_units(self):
        """Catches 'gradient_wrong_units' — pressure_gradient must return Pa/m."""
        m = _i()
        grad = m.pressure_gradient(400.0, 500_000.0)
        assert abs(grad - 8.0e-4) < 1e-8

class TestCorrectness:
    def test_geostrophic_speed_reference(self):
        m = _i()
        grad = m.pressure_gradient(DP_TEST, DX_TEST)
        vg = m.geostrophic_speed(grad, RHO_AIR, F_TEST)
        assert abs(vg - VG_TEST) < 0.01
    def test_buys_ballot_nh(self):
        m = _i()
        assert m.wind_direction_nh() == "low to left"
    def test_buys_ballot_sh(self):
        m = _i()
        assert m.wind_direction_sh() == "low to right"
    def test_speed_scales_with_gradient(self):
        """Doubling pressure gradient should double geostrophic speed."""
        m = _i()
        v1 = m.geostrophic_speed(8e-4, RHO_AIR, F_TEST)
        v2 = m.geostrophic_speed(16e-4, RHO_AIR, F_TEST)
        assert abs(v2 / v1 - 2.0) < 0.001
    def test_coriolis_parameter(self):
        """f = 2Ω sin(φ) at 45° should match frozen constant."""
        f_check = 2 * OMEGA_EARTH * math.sin(math.radians(PHI_TEST))
        assert abs(f_check - F_TEST) < 1e-12
