"""cat-earth-milankovitch — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_milankovitch_constants import *
IMPL = Path(__file__).parent.parent / "earth_milankovitch.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_precession_not_26k(self):
        """LLM trap: climatic precession is ~23,000 yr, NOT 26,000 yr (axial precession)."""
        m = _i(); p = m.climatic_precession_period()
        assert p != 26_000, "26,000 yr is AXIAL precession — climatic precession is ~23,000 yr"
        assert 20_000 <= p <= 25_000, f"Climatic precession must be 20–25 kyr, got {p}"

    def test_obliquity_range_correct(self):
        """LLM trap: obliquity range is 22.1°–24.5°, not some other range."""
        assert abs(OBLIQUITY_MIN - 22.1) < 0.01, f"Obliquity min must be 22.1°, got {OBLIQUITY_MIN}"
        assert abs(OBLIQUITY_MAX - 24.5) < 0.01, f"Obliquity max must be 24.5°, got {OBLIQUITY_MAX}"

    def test_eccentricity_not_23k_or_41k(self):
        """LLM trap: eccentricity period is ~100 kyr, NOT 23k or 41k."""
        m = _i(); e = m.eccentricity_period()
        assert e != 23_000, "23,000 yr is precession, not eccentricity"
        assert e != 41_000, "41,000 yr is obliquity, not eccentricity"
        assert 90_000 <= e <= 110_000, f"Eccentricity must be ~100 kyr, got {e}"


class TestCorrectness:
    def test_eccentricity_period(self):
        m = _i()
        assert m.eccentricity_period() == ECCENTRICITY_PERIOD

    def test_obliquity_period(self):
        m = _i()
        assert m.obliquity_period() == OBLIQUITY_PERIOD

    def test_climatic_precession_period(self):
        m = _i()
        assert m.climatic_precession_period() == CLIMATIC_PRECESSION_PERIOD

    def test_axial_precession_period(self):
        m = _i()
        assert m.axial_precession_period() == AXIAL_PRECESSION_PERIOD

    def test_current_obliquity(self):
        m = _i()
        assert abs(m.current_obliquity() - CURRENT_OBLIQUITY) < 1e-6

    def test_climatic_less_than_axial(self):
        """Climatic precession period must be shorter than axial precession period."""
        m = _i()
        assert m.climatic_precession_period() < m.axial_precession_period(), \
            "Climatic precession (~23 kyr) must be < axial precession (~26 kyr)"

    def test_period_ordering(self):
        """Eccentricity > obliquity > climatic precession."""
        m = _i()
        assert m.eccentricity_period() > m.obliquity_period() > m.climatic_precession_period()
