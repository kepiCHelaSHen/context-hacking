"""cat-earth-greenhouse-simple — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_greenhouse_simple_constants import *
IMPL = Path(__file__).parent.parent / "earth_greenhouse_simple.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three known LLM errors."""

    def test_emissivity_not_always_1(self):
        """PRIOR_ERROR: emissivity_always_1 — single-layer ε=1 overshoots observed 288K."""
        m = _i()
        Tb = m.bare_earth_temp()
        T1 = m.greenhouse_1layer_temp(Tb)
        # ε=1 model must give ~303K, which is ABOVE observed 288K
        assert T1 > T_SURFACE_OBSERVED, (
            f"1-layer ε=1 should OVERESTIMATE: got {T1:.2f}K, observed {T_SURFACE_OBSERVED}K"
        )

    def test_no_albedo_caught(self):
        """PRIOR_ERROR: no_albedo — forgetting albedo gives T_bare ≈ 279K, not 255K."""
        m = _i()
        Tb = m.bare_earth_temp(S=S_SOLAR, alpha=ALPHA)
        # With albedo: ~255K.  Without albedo (alpha=0): ~279K
        T_no_albedo = m.bare_earth_temp(S=S_SOLAR, alpha=0.0)
        assert Tb < T_no_albedo, "With albedo, T_bare must be LESS than without albedo"
        assert abs(Tb - T_BARE) < 0.01, f"T_bare should be {T_BARE:.2f}K, got {Tb:.2f}K"

    def test_bare_earth_not_288(self):
        """PRIOR_ERROR: bare_earth_too_warm — T_bare ≈ 255K, NOT 288K."""
        m = _i()
        Tb = m.bare_earth_temp()
        assert Tb < 260, f"T_bare should be ~255K, got {Tb:.2f}K (confused with observed 288K?)"
        assert Tb > 250, f"T_bare should be ~255K, got {Tb:.2f}K"


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_bare_earth_temp_default(self):
        m = _i()
        Tb = m.bare_earth_temp()
        assert abs(Tb - T_BARE) < 0.01, f"Expected {T_BARE:.4f}K, got {Tb:.4f}K"

    def test_bare_earth_temp_celsius(self):
        m = _i()
        Tb = m.bare_earth_temp()
        T_celsius = Tb - 273.15
        assert T_celsius < 0, f"Bare earth must be below freezing: {T_celsius:.1f}°C"

    def test_greenhouse_1layer_temp(self):
        m = _i()
        T1 = m.greenhouse_1layer_temp(T_BARE)
        assert abs(T1 - T_SURFACE_1LAYER) < 0.01, f"Expected {T_SURFACE_1LAYER:.4f}K, got {T1:.4f}K"

    def test_greenhouse_1layer_factor(self):
        """T_surface / T_bare must equal 2^(1/4)."""
        m = _i()
        T1 = m.greenhouse_1layer_temp(T_BARE)
        ratio = T1 / T_BARE
        assert abs(ratio - FACTOR_1LAYER) < 1e-6, f"Ratio should be 2^(1/4)={FACTOR_1LAYER:.6f}, got {ratio:.6f}"

    def test_stefan_boltzmann_flux_full(self):
        m = _i()
        F = m.stefan_boltzmann_flux(TEST_T, epsilon=1.0)
        assert abs(F - TEST_FLUX_FULL) < 0.1, f"Expected {TEST_FLUX_FULL:.2f}, got {F:.2f}"

    def test_stefan_boltzmann_flux_partial(self):
        m = _i()
        F = m.stefan_boltzmann_flux(TEST_T, epsilon=TEST_EPSILON)
        assert abs(F - TEST_FLUX_PARTIAL) < 0.1, f"Expected {TEST_FLUX_PARTIAL:.2f}, got {F:.2f}"

    def test_stefan_boltzmann_epsilon_scales(self):
        """Flux with ε<1 must be less than ε=1."""
        m = _i()
        F_full = m.stefan_boltzmann_flux(300.0, epsilon=1.0)
        F_part = m.stefan_boltzmann_flux(300.0, epsilon=0.5)
        assert F_part < F_full, "Partial emissivity flux must be less"
        assert abs(F_part - 0.5 * F_full) < 1e-6

    def test_greenhouse_effect_observed(self):
        m = _i()
        Tb = m.bare_earth_temp()
        dT = m.greenhouse_effect(T_SURFACE_OBSERVED, Tb)
        assert abs(dT - GREENHOUSE_EFFECT_OBSERVED) < 0.01, f"Expected {GREENHOUSE_EFFECT_OBSERVED:.2f}K, got {dT:.2f}K"

    def test_greenhouse_effect_positive(self):
        m = _i()
        dT = m.greenhouse_effect(T_SURFACE_OBSERVED, T_BARE)
        assert dT > 0, "Greenhouse effect must be positive"

    def test_absorbed_flux_roundtrip(self):
        """σ * T_bare^4 must equal F_absorbed (energy balance)."""
        m = _i()
        Tb = m.bare_earth_temp()
        F = m.stefan_boltzmann_flux(Tb, epsilon=1.0)
        assert abs(F - F_ABSORBED) < 0.01, f"Flux {F:.3f} ≠ absorbed {F_ABSORBED:.3f}"

    def test_greenhouse_1layer_overestimates(self):
        """ε=1 model gives ~303K > observed 288K — key insight."""
        m = _i()
        Tb = m.bare_earth_temp()
        T1 = m.greenhouse_1layer_temp(Tb)
        dT_model = m.greenhouse_effect(T1, Tb)
        dT_obs = m.greenhouse_effect(T_SURFACE_OBSERVED, Tb)
        assert dT_model > dT_obs, "ε=1 model overestimates greenhouse effect vs observation"
