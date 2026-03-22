"""cat-earth-ocean-density — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_ocean_density_constants import *
IMPL = Path(__file__).parent.parent / "earth_ocean_density.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_density_uses_temperature(self):
        """Catches 'density_only_salinity': density must vary with T at constant S."""
        m = _i()
        rho_cold = m.seawater_density(5.0, 35.0)
        rho_warm = m.seawater_density(25.0, 35.0)
        assert rho_cold != rho_warm, "Density must depend on temperature, not just salinity"

    def test_freshwater_max_at_4C(self):
        """Catches 'freshwater_max_0C': max freshwater density is at 4°C, not 0°C."""
        m = _i()
        assert abs(m.freshwater_max_density_temp() - T_MAX_DENSITY) < 0.1

    def test_sigma_t_is_offset_not_full(self):
        """Catches 'sigma_t_wrong': σ_t = ρ - 1000, not ρ itself."""
        m = _i()
        st = m.sigma_t(1025.0)
        assert abs(st - 25.0) < 0.01, "σ_t(1025) should be 25, not 1025"

class TestCorrectness:
    def test_density_test_case_1(self):
        """T=10°C, S=35 psu → ρ ≈ 1027.766 kg/m³."""
        m = _i()
        rho = m.seawater_density(TEST_T, TEST_S)
        assert abs(rho - TEST_RHO) < 0.01

    def test_density_test_case_2(self):
        """T=25°C, S=36 psu → ρ ≈ 1025.9335 kg/m³."""
        m = _i()
        rho = m.seawater_density(TEST2_T, TEST2_S)
        assert abs(rho - TEST2_RHO) < 0.01

    def test_sigma_t_test_case(self):
        """σ_t for test case 1 should match."""
        m = _i()
        rho = m.seawater_density(TEST_T, TEST_S)
        st = m.sigma_t(rho)
        assert abs(st - TEST_SIGMA_T) < 0.01

    def test_higher_salinity_higher_density(self):
        """At constant T, higher S → higher density."""
        m = _i()
        rho_low = m.seawater_density(15.0, 33.0)
        rho_high = m.seawater_density(15.0, 37.0)
        assert rho_high > rho_low

    def test_higher_temp_lower_density_above_4C(self):
        """Above 4°C, higher T → lower density at constant S."""
        m = _i()
        change = m.density_change_T(10.0, 20.0, 35.0)
        assert change < 0, "Warming above 4°C should decrease density"

    def test_freshwater_at_4C_is_max(self):
        """Freshwater density at 4°C should exceed density at 0°C and 10°C."""
        m = _i()
        rho_4 = m.seawater_density(4.0, 0.0)
        rho_0 = m.seawater_density(0.0, 0.0)
        rho_10 = m.seawater_density(10.0, 0.0)
        assert rho_4 > rho_0 and rho_4 > rho_10, "Freshwater max density must be at 4°C"

    def test_density_in_ocean_range(self):
        """Typical ocean conditions should yield density in expected range."""
        m = _i()
        rho = m.seawater_density(15.0, 35.0)
        assert RHO_OCEAN_MIN <= rho <= RHO_OCEAN_MAX
