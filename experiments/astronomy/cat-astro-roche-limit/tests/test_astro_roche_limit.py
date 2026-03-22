"""cat-astro-roche-limit — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_roche_limit_constants import *
IMPL = Path(__file__).parent.parent / "astro_roche_limit.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_density_ratio_uses_cube_root(self):
        """density_ratio_linear: must use (rho_M/rho_m)^(1/3), NOT rho_M/rho_m."""
        m = _i()
        ratio = m.density_ratio_cuberoot(RHO_EARTH, RHO_MOON)
        linear = RHO_EARTH / RHO_MOON  # ~1.6496 — WRONG
        correct = (RHO_EARTH / RHO_MOON) ** (1/3)  # ~1.1817 — RIGHT
        assert abs(ratio - correct) < 0.001
        assert abs(ratio - linear) > 0.1  # must NOT be the linear ratio

    def test_fluid_uses_correct_coefficient(self):
        """rigid_fluid_confused: fluid body uses 2.456, not (2)^(1/3)≈1.26."""
        m = _i()
        d_fluid = m.roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
        d_rigid = m.roche_limit_rigid(R_EARTH, RHO_EARTH, RHO_MOON)
        # Fluid limit (2.456*R*ratio^1/3) must be larger than rigid (R*(2*ratio)^1/3)
        assert d_fluid > d_rigid
        # Fluid must be close to known value
        assert abs(d_fluid - D_ROCHE_FLUID_EARTH_MOON) / D_ROCHE_FLUID_EARTH_MOON < 0.01

    def test_inside_roche_means_unstable(self):
        """roche_inside_means_stable: inside Roche limit = disrupted, NOT stable."""
        m = _i()
        d_roche = 18000e3  # 18000 km Roche limit
        # Object at 10000 km (inside) — should return True (is inside → unstable)
        assert m.is_inside_roche(10000e3, d_roche) is True
        # Object at 25000 km (outside) — should return False (is outside → stable)
        assert m.is_inside_roche(25000e3, d_roche) is False


class TestCorrectness:
    def test_rigid_roche_earth_moon(self):
        m = _i()
        d = m.roche_limit_rigid(R_EARTH, RHO_EARTH, RHO_MOON)
        assert abs(d - D_ROCHE_RIGID_EARTH_MOON) < 1000  # within 1 km

    def test_fluid_roche_earth_moon(self):
        m = _i()
        d = m.roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
        assert abs(d - D_ROCHE_FLUID_EARTH_MOON) < 1000  # within 1 km

    def test_fluid_roche_earth_moon_value(self):
        """Fluid Roche limit for Earth-Moon ≈ 18483 km."""
        m = _i()
        d = m.roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
        d_km = d / 1e3
        assert 18000 < d_km < 19000  # ~18483 km

    def test_moon_outside_roche(self):
        """Moon at 384400 km is well outside Earth's Roche limit (~18483 km)."""
        m = _i()
        d_roche = m.roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
        assert m.is_inside_roche(D_MOON_ACTUAL, d_roche) is False
        assert D_MOON_ACTUAL > d_roche * 10  # Moon is >10x the Roche distance

    def test_saturn_rings_inside_roche(self):
        """Saturn's B ring outer edge is inside Roche limit for ice particles."""
        m = _i()
        d_roche = m.roche_limit_fluid(R_SATURN, RHO_SATURN, RHO_ICE)
        assert m.is_inside_roche(D_SATURN_RING_OUTER, d_roche) is True

    def test_density_ratio_cuberoot_value(self):
        m = _i()
        ratio = m.density_ratio_cuberoot(RHO_EARTH, RHO_MOON)
        assert abs(ratio - DENSITY_RATIO_CUBEROOT) < 0.0001

    def test_rigid_less_than_fluid(self):
        """Rigid Roche limit is always less than fluid for same system."""
        m = _i()
        d_rigid = m.roche_limit_rigid(R_EARTH, RHO_EARTH, RHO_MOON)
        d_fluid = m.roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
        assert d_rigid < d_fluid

    def test_equal_densities(self):
        """When rho_M == rho_m, cube root ratio is 1.0."""
        m = _i()
        ratio = m.density_ratio_cuberoot(5000.0, 5000.0)
        assert abs(ratio - 1.0) < 1e-10
        d_fluid = m.roche_limit_fluid(1e7, 5000.0, 5000.0)
        assert abs(d_fluid - 2.456 * 1e7) < 100  # d = 2.456 * R_M when densities equal
