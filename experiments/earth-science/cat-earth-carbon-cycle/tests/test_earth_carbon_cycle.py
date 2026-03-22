"""cat-earth-carbon-cycle — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_carbon_cycle_constants import *
IMPL = Path(__file__).parent.parent / "earth_carbon_cycle.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_ocean_is_net_sink(self):
        """Catches 'ocean_is_source': ocean must be a NET SINK, not a source."""
        m = _i()
        assert m.ocean_is_net_sink() is True, "Ocean is a NET SINK of CO₂, not a source"

    def test_atmosphere_not_largest_reservoir(self):
        """Catches 'atmosphere_largest': ocean >> atmosphere in GtC."""
        m = _i()
        ocean = m.reservoir_size("ocean")
        atmos = m.reservoir_size("atmosphere")
        assert ocean > atmos, (
            f"Ocean ({ocean} GtC) must be larger than atmosphere ({atmos} GtC)"
        )

    def test_residence_not_perturbation(self):
        """Catches 'residence_equals_perturbation': ~4 yr ≠ ~100+ yr."""
        assert RESIDENCE_TIME < 10.0, "Residence time should be ~4 years"
        assert PERTURBATION_LIFETIME >= 100.0, "Perturbation lifetime should be ~100+ years"
        assert PERTURBATION_LIFETIME > 10 * RESIDENCE_TIME, (
            "Perturbation lifetime must be much longer than residence time"
        )


class TestCorrectness:
    def test_reservoir_atmosphere(self):
        """Atmosphere ≈ 860 GtC."""
        m = _i()
        assert abs(m.reservoir_size("atmosphere") - RESERVOIR_ATMOSPHERE) < 0.01

    def test_reservoir_ocean(self):
        """Ocean ≈ 38000 GtC."""
        m = _i()
        assert abs(m.reservoir_size("ocean") - RESERVOIR_OCEAN) < 0.01

    def test_reservoir_land_biosphere(self):
        """Land biosphere ≈ 2000 GtC."""
        m = _i()
        assert abs(m.reservoir_size("land_biosphere") - RESERVOIR_LAND_BIO) < 0.01

    def test_reservoir_fossil_fuels(self):
        """Fossil fuels ≈ 10000 GtC."""
        m = _i()
        assert abs(m.reservoir_size("fossil_fuels") - RESERVOIR_FOSSIL) < 0.01

    def test_reservoir_sediments(self):
        """Sediments ≈ 60,000,000 GtC."""
        m = _i()
        assert abs(m.reservoir_size("sediments") - RESERVOIR_SEDIMENTS) < 0.01

    def test_reservoir_unknown_raises(self):
        """Unknown reservoir name should raise KeyError."""
        m = _i()
        with pytest.raises(KeyError):
            m.reservoir_size("mars")

    def test_airborne_fraction_increase(self):
        """11.5 GtC/yr × 0.45 = 5.175 GtC/yr atmospheric increase."""
        m = _i()
        inc = m.airborne_fraction_increase(TOTAL_EMISSIONS)
        assert abs(inc - TEST_ATMOS_INCREASE_GTC) < 0.001

    def test_airborne_fraction_custom(self):
        """Custom airborne fraction should work."""
        m = _i()
        inc = m.airborne_fraction_increase(10.0, af=0.50)
        assert abs(inc - 5.0) < 0.001

    def test_gtc_to_ppm(self):
        """5.175 GtC → ~2.44 ppm."""
        m = _i()
        ppm = m.gtc_to_ppm(TEST_ATMOS_INCREASE_GTC)
        assert abs(ppm - TEST_ATMOS_INCREASE_PPM) < 0.01

    def test_ppm_to_gtc(self):
        """1 ppm → 2.12 GtC."""
        m = _i()
        gtc = m.ppm_to_gtc(1.0)
        assert abs(gtc - GTC_PER_PPM) < 0.001

    def test_roundtrip_gtc_ppm(self):
        """GtC → ppm → GtC roundtrip should be identity."""
        m = _i()
        original = 100.0
        assert abs(m.ppm_to_gtc(m.gtc_to_ppm(original)) - original) < 0.001

    def test_atmos_increase_ppm_near_observed(self):
        """Computed atmospheric increase should be close to observed ~2.5 ppm/yr."""
        m = _i()
        inc_gtc = m.airborne_fraction_increase(TOTAL_EMISSIONS)
        inc_ppm = m.gtc_to_ppm(inc_gtc)
        assert 2.0 < inc_ppm < 3.0, (
            f"Computed {inc_ppm:.2f} ppm/yr — should be near observed ~2.5 ppm/yr"
        )
