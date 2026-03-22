"""cat-astro-equilibrium-temp — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_equilibrium_temp_constants import *
IMPL = Path(__file__).parent.parent / "astro_equilibrium_temp.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-error tests ──────────────────────────────────────────────

class TestPriorErrors:
    def test_teq_is_not_surface_earth(self):
        """teq_is_surface: Earth T_eq (~254 K) must NOT equal actual surface T (288 K)."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        # T_eq should be well below actual surface temperature
        assert T_eq < T_ACTUAL_EARTH - 20, (
            f"T_eq={T_eq:.1f} K is too close to actual {T_ACTUAL_EARTH} K — "
            "equilibrium temperature ignores greenhouse effect"
        )

    def test_teq_is_not_surface_venus(self):
        """teq_is_surface: Venus T_eq (~227 K) must NOT equal actual surface T (737 K)."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_VENUS, A_VENUS)
        assert T_eq < T_ACTUAL_VENUS - 400, (
            f"T_eq={T_eq:.1f} K is too close to actual {T_ACTUAL_VENUS} K — "
            "Venus has massive greenhouse effect"
        )

    def test_albedo_matters(self):
        """no_albedo: forgetting (1-A) gives wrong answer.
        With A=0 vs A=0.306, temperatures must differ significantly."""
        m = _i()
        T_no_albedo = m.equilibrium_temp(L_SUN, D_EARTH, 0.0)
        T_with_albedo = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        # (1-0)^0.25 / (1-0.306)^0.25 = 1/0.694^0.25 = 1/0.913 = 1.095
        # So T_no_albedo should be ~9.5% higher
        ratio = T_no_albedo / T_with_albedo
        assert ratio > 1.05, (
            f"T(A=0)/T(A=0.306) = {ratio:.3f}; albedo should matter by ~9.5%"
        )

    def test_higher_albedo_means_lower_teq(self):
        """no_albedo: higher albedo reflects more light, must reduce T_eq."""
        m = _i()
        T_low_A = m.equilibrium_temp(L_SUN, D_EARTH, 0.1)
        T_high_A = m.equilibrium_temp(L_SUN, D_EARTH, 0.9)
        assert T_high_A < T_low_A, "Higher albedo must give lower equilibrium T"

    def test_greenhouse_positive_earth(self):
        """greenhouse_negative: greenhouse effect must be positive (warming) for Earth."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        dT = m.greenhouse_effect(T_ACTUAL_EARTH, T_eq)
        assert dT > 0, (
            f"Greenhouse effect={dT:.1f} K is negative — "
            "greenhouse always warms planets with atmospheres"
        )

    def test_greenhouse_positive_venus(self):
        """greenhouse_negative: greenhouse effect must be positive for Venus."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_VENUS, A_VENUS)
        dT = m.greenhouse_effect(T_ACTUAL_VENUS, T_eq)
        assert dT > 400, (
            f"Venus greenhouse={dT:.1f} K; should be >400 K (massive CO2 atmosphere)"
        )


# ── Correctness tests ──────────────────────────────────────────────

class TestEquilibriumTemp:
    def test_earth_teq(self):
        """Earth T_eq should be ~254 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        assert abs(T_eq - T_EQ_EARTH) / T_EQ_EARTH < 0.001

    def test_venus_teq(self):
        """Venus T_eq should be ~227 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_VENUS, A_VENUS)
        assert abs(T_eq - T_EQ_VENUS) / T_EQ_VENUS < 0.001

    def test_mars_teq(self):
        """Mars T_eq should be ~210 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_MARS, A_MARS)
        assert abs(T_eq - T_EQ_MARS) / T_EQ_MARS < 0.001

    def test_earth_teq_absolute(self):
        """Earth T_eq must be within 2 K of 254.0 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        assert abs(T_eq - 254.0) < 2.0, f"T_eq={T_eq:.2f} K, expected ~254 K"

    def test_closer_means_hotter(self):
        """Planet closer to star must have higher T_eq (same albedo)."""
        m = _i()
        T_close = m.equilibrium_temp(L_SUN, 1.0e11, 0.3)
        T_far   = m.equilibrium_temp(L_SUN, 3.0e11, 0.3)
        assert T_close > T_far

    def test_brighter_star_means_hotter(self):
        """More luminous star must give higher T_eq (same distance, albedo)."""
        m = _i()
        T_dim    = m.equilibrium_temp(1e26, D_EARTH, 0.3)
        T_bright = m.equilibrium_temp(1e27, D_EARTH, 0.3)
        assert T_bright > T_dim

    def test_zero_albedo(self):
        """A=0 (perfect absorber) gives maximum T_eq for given L, d."""
        m = _i()
        T_max = m.equilibrium_temp(L_SUN, D_EARTH, 0.0)
        T_partial = m.equilibrium_temp(L_SUN, D_EARTH, 0.5)
        assert T_max > T_partial


class TestGreenhouseEffect:
    def test_earth_greenhouse(self):
        """Earth greenhouse ~34 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_EARTH, A_EARTH)
        dT = m.greenhouse_effect(T_ACTUAL_EARTH, T_eq)
        assert abs(dT - GREENHOUSE_EARTH) < 1.0

    def test_venus_greenhouse(self):
        """Venus greenhouse ~510 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_VENUS, A_VENUS)
        dT = m.greenhouse_effect(T_ACTUAL_VENUS, T_eq)
        assert abs(dT - GREENHOUSE_VENUS) < 1.0

    def test_mars_greenhouse(self):
        """Mars greenhouse ~8 K."""
        m = _i()
        T_eq = m.equilibrium_temp(L_SUN, D_MARS, A_MARS)
        dT = m.greenhouse_effect(T_ACTUAL_MARS, T_eq)
        assert abs(dT - GREENHOUSE_MARS) < 1.0

    def test_no_atmosphere(self):
        """If T_actual == T_eq, greenhouse effect is zero."""
        m = _i()
        assert m.greenhouse_effect(250.0, 250.0) == 0.0


class TestIsHabitable:
    def test_earth_habitable(self):
        m = _i()
        assert m.is_habitable(T_ACTUAL_EARTH) is True

    def test_venus_not_habitable(self):
        m = _i()
        assert m.is_habitable(T_ACTUAL_VENUS) is False

    def test_mars_not_habitable(self):
        m = _i()
        assert m.is_habitable(T_ACTUAL_MARS) is False

    def test_freezing_boundary(self):
        m = _i()
        assert m.is_habitable(273) is True
        assert m.is_habitable(272.9) is False

    def test_boiling_boundary(self):
        m = _i()
        assert m.is_habitable(373) is True
        assert m.is_habitable(373.1) is False


class TestEdgeCases:
    def test_zero_distance_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium_temp(L_SUN, 0, 0.3)

    def test_negative_distance_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium_temp(L_SUN, -1e11, 0.3)

    def test_albedo_one_raises(self):
        """A=1 means perfect reflector — no absorption, T_eq=0. We disallow it."""
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium_temp(L_SUN, D_EARTH, 1.0)

    def test_negative_albedo_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium_temp(L_SUN, D_EARTH, -0.1)

    def test_negative_luminosity_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.equilibrium_temp(-1e26, D_EARTH, 0.3)
