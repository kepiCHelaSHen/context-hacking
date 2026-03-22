"""cat-astro-main-sequence — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_main_sequence_constants import *
IMPL = Path(__file__).parent.parent / "astro_main_sequence.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_massive_star_shorter_life(self):
        """PRIOR_ERROR: lifetime_proportional_mass — bigger mass = SHORTER life."""
        m = _i()
        t10 = m.ms_lifetime(10.0)
        t1 = m.ms_lifetime(1.0)
        assert t10 < t1, "10 M_sun must live SHORTER than 1 M_sun"
    def test_alpha_not_universal(self):
        """PRIOR_ERROR: ml_exponent_wrong — different alpha gives different results."""
        m = _i()
        L_35 = m.mass_luminosity(5.0, alpha=3.5)
        L_40 = m.mass_luminosity(5.0, alpha=4.0)
        assert abs(L_35 - L_40) > 1.0, "alpha=3.5 vs 4.0 must give different luminosities"
    def test_sun_lifetime_10gyr(self):
        """PRIOR_ERROR: sun_lifetime_wrong — Sun MS lifetime is ~10 Gyr, not 4.6."""
        assert abs(T_SUN_GYR - 10.0) < 0.5

class TestCorrectness:
    def test_mass_luminosity_10Msun(self):
        m = _i()
        L = m.mass_luminosity(10.0, alpha=3.5)
        assert abs(L - L_10MSUN) < 0.1
    def test_ms_lifetime_10Msun(self):
        m = _i()
        t = m.ms_lifetime(10.0, alpha=3.5)
        assert abs(t - T_10MSUN_GYR) < 1e-4
    def test_ms_lifetime_05Msun(self):
        m = _i()
        t = m.ms_lifetime(0.5, alpha=4.0)
        assert abs(t - T_05MSUN_GYR) < 0.1
    def test_ms_lifetime_02Msun(self):
        m = _i()
        t = m.ms_lifetime(0.2, alpha=2.3)
        assert abs(t - T_02MSUN_GYR) < 0.1
    def test_lifetime_ratio_5_1(self):
        m = _i()
        r = m.lifetime_ratio(5.0, 1.0, alpha=3.5)
        assert abs(r - RATIO_5_1) < 1e-5
    def test_sun_is_unity(self):
        m = _i()
        assert abs(m.mass_luminosity(1.0) - 1.0) < 1e-10
        assert abs(m.ms_lifetime(1.0) - T_SUN_GYR) < 1e-10
        assert abs(m.lifetime_ratio(1.0, 1.0) - 1.0) < 1e-10
