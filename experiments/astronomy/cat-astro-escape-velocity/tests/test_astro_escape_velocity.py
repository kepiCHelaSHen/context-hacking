"""cat-astro-escape-velocity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_escape_velocity_constants import *
IMPL = Path(__file__).parent.parent / "astro_escape_velocity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_uses_mean_not_equatorial_radius(self):
        """wrong_radius: must use mean 6371km, not equatorial 6378km."""
        m = _i()
        v_correct = m.escape_velocity(M_EARTH, R_EARTH_MEAN)
        v_wrong   = m.escape_velocity(M_EARTH, R_EARTH_EQUATORIAL)
        assert abs(v_correct - V_ESC_EARTH) < 1.0
        assert abs(v_wrong - V_ESC_EARTH) > 1.0  # equatorial gives different answer

    def test_has_sqrt(self):
        """no_sqrt: result must be sqrt(2GM/R), not 2GM/R."""
        m = _i()
        v = m.escape_velocity(M_EARTH, R_EARTH_MEAN)
        raw = 2 * G * M_EARTH / R_EARTH_MEAN  # without sqrt — ~1.25e8
        assert v < 1e6  # reasonable velocity, not 1.25e8

    def test_mass_radius_not_swapped(self):
        """mass_radius_swapped: sqrt(2GM/R) not sqrt(2GR/M)."""
        m = _i()
        v = m.escape_velocity(M_EARTH, R_EARTH_MEAN)
        # If swapped: sqrt(2*G*R/M) ≈ sqrt(2*6.674e-11*6.371e6/5.972e24) ≈ 1.2e-10 — tiny
        assert v > 1000  # must be > 1 km/s for Earth

class TestCorrectness:
    def test_earth_escape_velocity(self):
        m = _i()
        assert abs(m.escape_velocity(M_EARTH, R_EARTH_MEAN) - V_ESC_EARTH) < 1.0

    def test_moon_escape_velocity(self):
        m = _i()
        assert abs(m.escape_velocity(M_MOON, R_MOON) - V_ESC_MOON) < 1.0

    def test_mars_escape_velocity(self):
        m = _i()
        assert abs(m.escape_velocity(M_MARS, R_MARS) - V_ESC_MARS) < 1.0

    def test_jupiter_escape_velocity(self):
        m = _i()
        assert abs(m.escape_velocity(M_JUPITER, R_JUPITER) - V_ESC_JUPITER) < 10.0

    def test_escape_velocity_km_s(self):
        m = _i()
        v_km = m.escape_velocity_km_s(M_EARTH, R_EARTH_MEAN)
        assert abs(v_km - V_ESC_EARTH / 1000.0) < 0.01

    def test_surface_gravity_earth(self):
        m = _i()
        g = m.surface_gravity(M_EARTH, R_EARTH_MEAN)
        assert abs(g - G_EARTH) < 0.01

    def test_scaling_larger_planet_larger_v_esc(self):
        """v_esc proportional to sqrt(M/R) — Jupiter > Earth > Mars > Moon."""
        m = _i()
        v_j = m.escape_velocity(M_JUPITER, R_JUPITER)
        v_e = m.escape_velocity(M_EARTH, R_EARTH_MEAN)
        v_m = m.escape_velocity(M_MARS, R_MARS)
        v_moon = m.escape_velocity(M_MOON, R_MOON)
        assert v_j > v_e > v_m > v_moon
