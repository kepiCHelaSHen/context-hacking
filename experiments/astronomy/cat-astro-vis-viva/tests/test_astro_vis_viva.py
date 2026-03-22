"""cat-astro-vis-viva — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_vis_viva_constants import *
IMPL = Path(__file__).parent.parent / "astro_vis_viva.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_escape_has_sqrt2(self):
        """Catches escape_no_sqrt2: v_esc must be v_c * sqrt(2), not just sqrt(GM/r)."""
        m = _i()
        v_esc = m.escape_velocity(MU_SUN, AU)
        v_circ = m.circular_velocity(MU_SUN, AU)
        assert abs(v_esc / v_circ - math.sqrt(2)) < 0.001

    def test_vis_viva_not_circular(self):
        """Catches circular_for_elliptical: elliptical orbit speed != circular speed at same r."""
        m = _i()
        v_ell = m.vis_viva(MU_SUN, R_PERIHELION, A_ELLIPTICAL)
        v_circ = m.circular_velocity(MU_SUN, R_PERIHELION)
        # At perihelion of a larger orbit, v > v_circ at that r
        assert v_ell > v_circ

    def test_2_over_r_not_1_over_r(self):
        """Catches missing_2_over_r: vis-viva has 2/r, not 1/r."""
        m = _i()
        v_vv = m.vis_viva(MU_SUN, AU, AU)  # circular case: should equal v_circ
        v_circ = m.circular_velocity(MU_SUN, AU)
        # If 2/r were replaced with 1/r, vis_viva(GM, r, r) = sqrt(GM*(1/r - 1/r)) = 0
        assert abs(v_vv - v_circ) < 1.0  # must match, not be zero

class TestCorrectness:
    def test_circular_earth(self):
        m = _i()
        v = m.circular_velocity(MU_SUN, AU)
        assert abs(v - V_CIRC_EARTH) < 5.0  # within 5 m/s

    def test_escape_1au(self):
        m = _i()
        v = m.escape_velocity(MU_SUN, AU)
        assert abs(v - V_ESC_1AU) < 5.0

    def test_vis_viva_perihelion(self):
        m = _i()
        v = m.vis_viva(MU_SUN, R_PERIHELION, A_ELLIPTICAL)
        assert abs(v - V_PERIHELION) < 5.0

    def test_vis_viva_aphelion(self):
        m = _i()
        v = m.vis_viva(MU_SUN, R_APHELION, A_ELLIPTICAL)
        assert abs(v - V_APHELION) < 5.0

    def test_aphelion_slower_than_perihelion(self):
        """Kepler's 2nd law: slower at aphelion."""
        m = _i()
        vp = m.vis_viva(MU_SUN, R_PERIHELION, A_ELLIPTICAL)
        va = m.vis_viva(MU_SUN, R_APHELION, A_ELLIPTICAL)
        assert vp > va

    def test_circular_is_vis_viva_special_case(self):
        """When r=a, vis-viva reduces to circular velocity."""
        m = _i()
        v_vv = m.vis_viva(MU_SUN, AU, AU)
        v_c = m.circular_velocity(MU_SUN, AU)
        assert abs(v_vv - v_c) < 0.01

    def test_escape_is_vis_viva_limit(self):
        """When a->inf, vis-viva reduces to escape velocity."""
        m = _i()
        v_vv = m.vis_viva(MU_SUN, AU, float('inf'))
        v_esc = m.escape_velocity(MU_SUN, AU)
        assert abs(v_vv - v_esc) < 0.01

    def test_is_bound_circular(self):
        m = _i()
        v_circ = m.circular_velocity(MU_SUN, AU)
        assert m.is_bound(v_circ, MU_SUN, AU) is True

    def test_is_bound_escape(self):
        m = _i()
        v_esc = m.escape_velocity(MU_SUN, AU)
        assert m.is_bound(v_esc * 1.01, MU_SUN, AU) is False
