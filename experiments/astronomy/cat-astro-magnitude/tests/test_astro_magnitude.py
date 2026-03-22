"""cat-astro-magnitude — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_magnitude_constants import *
IMPL = Path(__file__).parent.parent / "astro_magnitude.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_distance_modulus_has_minus_5(self):
        """Catches distance_modulus_no_minus_5: dm must be 5*log10(d)-5, not 5*log10(d).
        At d=100pc: correct dm=5, wrong dm=10."""
        m = _i()
        dm = m.distance_modulus(D_TEST)
        assert abs(dm - DM_TEST) < 0.001
        assert abs(dm - DM_TEST_WRONG) > 4.0  # must differ from wrong answer

    def test_brighter_is_lower_m(self):
        """Catches brighter_is_larger: brighter star must have LOWER apparent magnitude."""
        m = _i()
        # Star at 10 pc vs 100 pc, same M: closer star is brighter (lower m)
        m_near = m.apparent_from_absolute(0.0, 10.0)
        m_far = m.apparent_from_absolute(0.0, 100.0)
        assert m_near < m_far  # closer = brighter = lower m

    def test_flux_ratio_pogson(self):
        """Catches flux_ratio_wrong: 5 magnitudes must equal exactly 100x flux ratio."""
        m = _i()
        fr = m.flux_ratio(0.0, 5.0)
        assert abs(fr - 100.0) < 0.01

    def test_flux_ratio_1mag(self):
        """Catches flux_ratio_wrong: 1 magnitude ~ 2.512x flux ratio."""
        m = _i()
        fr = m.flux_ratio(0.0, 1.0)
        assert abs(fr - FLUX_RATIO_1MAG) < 0.001

class TestCorrectness:
    def test_dm_at_10pc_is_zero(self):
        """At reference distance 10 pc, distance modulus must be 0 (m = M)."""
        m = _i()
        dm = m.distance_modulus(10.0)
        assert abs(dm) < 0.001

    def test_test_star(self):
        """d=100pc, M=0 => m=5."""
        m = _i()
        app = m.apparent_from_absolute(M_TEST, D_TEST)
        assert abs(app - M_APP_TEST) < 0.001

    def test_sun_distance_modulus(self):
        """Sun at 1 AU: dm ~ -31.57."""
        m = _i()
        dm = m.distance_modulus(AU_IN_PC)
        assert abs(dm - DM_SUN) < 0.05

    def test_sun_absolute_magnitude(self):
        """Recover Sun's M from apparent m and distance."""
        m = _i()
        M_calc = m.absolute_from_apparent(M_SUN_APP, AU_IN_PC)
        assert abs(M_calc - M_SUN_ABS) < 0.05

    def test_sirius_apparent_mag(self):
        """Sirius: M=1.42, d=2.64pc => m ~ -1.47."""
        m = _i()
        app = m.apparent_from_absolute(M_SIRIUS_ABS, D_SIRIUS)
        assert abs(app - M_SIRIUS_APP) < 0.01

    def test_roundtrip_apparent_absolute(self):
        """apparent_from_absolute and absolute_from_apparent must be inverses."""
        m = _i()
        M_orig = 3.5
        d = 50.0
        app = m.apparent_from_absolute(M_orig, d)
        M_back = m.absolute_from_apparent(app, d)
        assert abs(M_back - M_orig) < 0.0001

    def test_flux_ratio_symmetric(self):
        """F1/F2 * F2/F1 = 1."""
        m = _i()
        fr_12 = m.flux_ratio(2.0, 5.0)
        fr_21 = m.flux_ratio(5.0, 2.0)
        assert abs(fr_12 * fr_21 - 1.0) < 0.0001

    def test_flux_ratio_zero_diff(self):
        """Same magnitude => flux ratio = 1."""
        m = _i()
        fr = m.flux_ratio(3.0, 3.0)
        assert abs(fr - 1.0) < 0.0001
