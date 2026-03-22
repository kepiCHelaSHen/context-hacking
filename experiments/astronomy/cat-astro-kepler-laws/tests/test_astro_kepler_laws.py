"""cat-astro-kepler-laws — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_kepler_laws_constants import *
IMPL = Path(__file__).parent.parent / "astro_kepler_laws.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


# ── Prior-Error Tests (the mistakes LLMs make) ──────────────────────────

class TestPriorErrors:
    def test_constant_depends_on_mass(self):
        """constant_universal: k must differ when central mass differs."""
        mod = _import_impl()
        k_sun = mod.kepler_constant(M_SUN)
        k_double = mod.kepler_constant(M_DOUBLE_SUN)
        # k should halve when M doubles
        assert abs(k_sun / k_double - 2.0) < 0.001

    def test_mass_in_kepler_constant(self):
        """mass_not_included: k = 4pi²/(GM), must include M."""
        mod = _import_impl()
        k = mod.kepler_constant(M_SUN)
        expected = 4 * math.pi**2 / (G_NEWTON * M_SUN)
        assert abs(k - expected) / expected < 1e-10

    def test_solar_units_not_universal(self):
        """uses_1_au_yr: T²/a³ = 1 yr²/AU³ only for solar system."""
        mod = _import_impl()
        # For a 2*M_sun star, period at 1 AU should be shorter than 1 yr
        T_double = mod.orbital_period(AU_METERS, M_DOUBLE_SUN)
        T_yr = T_double / YR_SECONDS
        a_au = 1.0  # 1 AU
        ratio = T_yr**2 / a_au**3
        # Ratio should be ~0.5, NOT 1.0
        assert abs(ratio - 0.5) < 0.02, (
            f"T²/a³ = {ratio:.4f} yr²/AU³ for 2M_sun; should be ~0.5, not 1.0"
        )


# ── Correctness Tests ────────────────────────────────────────────────────

class TestCorrectness:
    def test_kepler_constant_sun_value(self):
        """k(Sun) should match frozen constant."""
        mod = _import_impl()
        k = mod.kepler_constant(M_SUN)
        assert abs(k - KEPLER_CONSTANT_SUN) / KEPLER_CONSTANT_SUN < 1e-10

    def test_earth_period(self):
        """Earth orbital period should be ~365.26 days."""
        mod = _import_impl()
        T = mod.orbital_period(AU_METERS, M_SUN)
        T_days = T / 86400
        assert abs(T_days - T_EARTH_DAYS) < 0.5

    def test_double_star_period(self):
        """Planet at 1 AU around 2M_sun: period ~ T_earth/sqrt(2)."""
        mod = _import_impl()
        T = mod.orbital_period(AU_METERS, M_DOUBLE_SUN)
        T_days = T / 86400
        assert abs(T_days - T_DOUBLE_AT_1AU_DAYS) < 0.5

    def test_semi_major_axis_roundtrip(self):
        """semi_major_axis(orbital_period(a, M), M) should recover a."""
        mod = _import_impl()
        a_in = 2.279e11  # Mars orbit ~1.524 AU in metres
        T = mod.orbital_period(a_in, M_SUN)
        a_out = mod.semi_major_axis(T, M_SUN)
        assert abs(a_out - a_in) / a_in < 1e-9

    def test_kepler_ratio_solar(self):
        """Solar system ratio should be exactly 1.0 yr²/AU³."""
        mod = _import_impl()
        assert mod.kepler_ratio_solar() == 1.0

    def test_ratio_earth_in_si(self):
        """T²/a³ for Earth should match kepler_constant(M_sun) in SI."""
        mod = _import_impl()
        T = mod.orbital_period(AU_METERS, M_SUN)
        ratio = T**2 / AU_METERS**3
        k = mod.kepler_constant(M_SUN)
        assert abs(ratio - k) / k < 1e-9
