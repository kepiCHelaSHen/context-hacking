"""cat-econ-gdp-deflator — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_gdp_deflator_constants import *
IMPL = Path(__file__).parent.parent / "econ_gdp_deflator.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_real_gdp_uses_base_prices(self):
        """Catch: real_current_prices — must use BASE YEAR prices, not current."""
        m = _i()
        real = m.real_gdp(BASE_PRICES, YEAR1_QUANTS)
        wrong_real = m.nominal_gdp(YEAR1_PRICES, YEAR1_QUANTS)  # common LLM error
        assert abs(real - REAL_Y1) < 1e-6
        assert real != wrong_real, "Real GDP must not equal nominal (uses base prices)"

    def test_deflator_not_inverted(self):
        """Catch: deflator_inverted — must be Nominal/Real, not Real/Nominal."""
        m = _i()
        d = m.gdp_deflator(NOMINAL_Y1, REAL_Y1)
        inverted = (REAL_Y1 / NOMINAL_Y1) * 100  # wrong formula
        assert abs(d - DEFLATOR_Y1) < 0.01
        assert abs(d - inverted) > 1.0, "Deflator must be Nominal/Real, not Real/Nominal"

    def test_base_year_deflator_is_100(self):
        """Catch: base_year_not_100 — in base year, deflator must equal 100."""
        m = _i()
        d0 = m.gdp_deflator(NOMINAL_Y0, REAL_Y0)
        assert abs(d0 - 100.0) < 1e-9, "Base year deflator must be exactly 100"


class TestCorrectness:
    def test_nominal_gdp_year0(self):
        m = _i()
        assert abs(m.nominal_gdp(BASE_PRICES, BASE_QUANTS) - NOMINAL_Y0) < 1e-6

    def test_nominal_gdp_year1(self):
        m = _i()
        assert abs(m.nominal_gdp(YEAR1_PRICES, YEAR1_QUANTS) - NOMINAL_Y1) < 1e-6

    def test_real_gdp_year0(self):
        m = _i()
        assert abs(m.real_gdp(BASE_PRICES, BASE_QUANTS) - REAL_Y0) < 1e-6

    def test_real_gdp_year1(self):
        m = _i()
        assert abs(m.real_gdp(BASE_PRICES, YEAR1_QUANTS) - REAL_Y1) < 1e-6

    def test_deflator_year1(self):
        m = _i()
        d = m.gdp_deflator(NOMINAL_Y1, REAL_Y1)
        assert abs(d - DEFLATOR_Y1) < 0.01

    def test_inflation_rate(self):
        m = _i()
        inf = m.inflation_rate(DEFLATOR_Y1, DEFLATOR_Y0)
        assert abs(inf - INFLATION_01) < 0.01
