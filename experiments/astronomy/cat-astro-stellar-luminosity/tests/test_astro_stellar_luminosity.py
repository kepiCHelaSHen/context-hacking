"""cat-astro-stellar-luminosity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_stellar_luminosity_constants import *
IMPL = Path(__file__).parent.parent / "astro_stellar_luminosity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_r_must_be_meters(self):
        """r_not_meters: using km gives wildly wrong answer."""
        m = _i()
        L_correct = m.luminosity(R_SUN, T_SUN)
        L_wrong_km = m.luminosity(R_SUN_KM, T_SUN)  # R in km — 1e6 too small
        assert abs(L_correct - L_SUN_CALC) / L_SUN_CALC < 0.001
        assert L_wrong_km < L_correct * 1e-4  # km gives ~1e-6 of correct

    def test_sigma_correct(self):
        """sigma_wrong: must use 5.670e-8, not 5.670e-9 or other wrong value."""
        m = _i()
        L_correct = m.luminosity(R_SUN, T_SUN, sigma=5.670e-8)
        L_wrong   = m.luminosity(R_SUN, T_SUN, sigma=5.670e-9)
        assert abs(L_correct - L_SUN_CALC) / L_SUN_CALC < 0.001
        assert abs(L_wrong - L_SUN_CALC) / L_SUN_CALC > 0.5  # off by 10x

    def test_t_fourth_not_squared(self):
        """t_squared_not_fourth: T^4 gives ~3.8e26 W; T^2 gives ~1.2e19 — way too small."""
        m = _i()
        L = m.luminosity(R_SUN, T_SUN)
        # If T^2 were used instead of T^4: 4*pi*R^2*sigma*T^2 ~ 1.15e19 (7 orders too small)
        L_if_t2 = 4 * math.pi * R_SUN**2 * SIGMA * T_SUN**2
        assert L > 1e25  # must be star-scale (~3.8e26), not 1.15e19
        assert L_if_t2 < 1e20  # T^2 would give ~1e19, clearly not a star luminosity

class TestCorrectness:
    def test_sun_luminosity_si(self):
        m = _i()
        L = m.luminosity(R_SUN, T_SUN)
        assert abs(L - L_SUN_CALC) / L_SUN_CALC < 0.001

    def test_sun_luminosity_close_to_nominal(self):
        m = _i()
        L = m.luminosity(R_SUN, T_SUN)
        assert abs(L - L_SUN) / L_SUN < 0.01  # within 1% of IAU nominal

    def test_sirius_luminosity_si(self):
        m = _i()
        L = m.luminosity(R_SIRIUS_M, T_SIRIUS)
        assert abs(L - L_SIRIUS) / L_SIRIUS < 0.001

    def test_sirius_luminosity_solar_units(self):
        m = _i()
        L_sol = m.luminosity_solar(R_SIRIUS_RSUN, T_SIRIUS)
        assert abs(L_sol - L_SIRIUS_SOLAR) / L_SIRIUS_SOLAR < 0.01

    def test_solar_constants(self):
        m = _i()
        assert m.solar_luminosity() == 3.828e26
        assert m.solar_radius() == 6.957e8

    def test_hotter_star_more_luminous(self):
        """At same radius, hotter star must be more luminous (T^4 dependence)."""
        m = _i()
        L_cool = m.luminosity(R_SUN, 4000)
        L_hot  = m.luminosity(R_SUN, 8000)
        assert L_hot > L_cool * 10  # 2x T => 16x L
