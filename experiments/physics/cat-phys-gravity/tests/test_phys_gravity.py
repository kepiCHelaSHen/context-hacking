"""cat-phys-gravity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_gravity_constants import *
IMPL = Path(__file__).parent.parent / "phys_gravity.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_escape_gt_orbital(self):
        mod = _import_impl()
        v_esc = mod.escape_velocity(M_EARTH, R_EARTH)
        v_orb = mod.orbital_velocity(M_EARTH, R_EARTH)
        assert abs(v_esc / v_orb - math.sqrt(2)) < 0.01
    def test_inverse_square(self):
        mod = _import_impl()
        F1 = mod.gravitational_force(1, 1, 1)
        F2 = mod.gravitational_force(1, 1, 2)
        assert abs(F1 / F2 - 4.0) < 0.01
    def test_G_precise(self):
        assert G_NEWTON != 6.67e-11
        assert abs(G_NEWTON - 6.67430e-11) < 1e-15
class TestCorrectness:
    def test_earth_surface_g(self):
        mod = _import_impl()
        g = mod.surface_gravity(M_EARTH, R_EARTH)
        assert abs(g - G_SURFACE) < 0.05
    def test_escape_velocity_earth(self):
        mod = _import_impl()
        v = mod.escape_velocity(M_EARTH, R_EARTH)
        assert abs(v - V_ESC_EARTH) < 10
    def test_earth_period(self):
        mod = _import_impl()
        T = mod.orbital_period(M_SUN, R_EARTH_ORBIT)
        assert abs(T / 86400 - 365.25) < 1.0
