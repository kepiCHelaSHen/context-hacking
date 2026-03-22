"""cat-earth-soil-classification — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_soil_classification_constants import *
IMPL = Path(__file__).parent.parent / "earth_soil_classification.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ── Prior-Error Tests (the mistakes LLMs commonly make) ──────────────

class TestPriorErrors:
    """Tests targeting documented PRIOR_ERRORS."""

    def test_composition_must_sum_to_100(self):
        """PRIOR_ERROR: sum_not_100 — reject compositions not summing to 100."""
        m = _i()
        assert m.validate_composition(20, 40, 40) is True
        assert m.validate_composition(30, 30, 30) is False  # sums to 90
        assert m.validate_composition(40, 40, 40) is False  # sums to 120

    def test_classify_rejects_bad_sum(self):
        """PRIOR_ERROR: sum_not_100 — classify_simple must raise on bad sum."""
        m = _i()
        with pytest.raises(ValueError):
            m.classify_simple(30, 30, 30)

    def test_clay_boundary_is_40(self):
        """PRIOR_ERROR: clay_boundary_wrong — clay class starts at 40% clay."""
        m = _i()
        assert m.is_clay_dominated(40) is True
        assert m.is_clay_dominated(39) is False
        assert m.classify_simple(40, 30, 30) == "clay"
        assert m.classify_simple(39, 31, 30) != "clay"

    def test_loam_definition(self):
        """PRIOR_ERROR: loam_definition_wrong — loam is 7-27% clay, 28-50% silt, <=52% sand."""
        m = _i()
        assert m.classify_simple(20, 40, 40) == "loam"
        # Outside loam: too much clay
        assert m.classify_simple(30, 40, 30) != "loam"


# ── Correctness Tests ─────────────────────────────────────────────────

class TestCorrectness:
    """Verify known test vectors from the USDA texture triangle."""

    def test_loam_vector(self):
        m = _i()
        assert m.classify_simple(
            TEST_LOAM["clay"], TEST_LOAM["silt"], TEST_LOAM["sand"]
        ) == TEST_LOAM["expected"]

    def test_clay_vector(self):
        m = _i()
        assert m.classify_simple(
            TEST_CLAY["clay"], TEST_CLAY["silt"], TEST_CLAY["sand"]
        ) == TEST_CLAY["expected"]

    def test_loamy_sand_vector(self):
        m = _i()
        assert m.classify_simple(
            TEST_LOAMY_SAND["clay"], TEST_LOAMY_SAND["silt"], TEST_LOAMY_SAND["sand"]
        ) == TEST_LOAMY_SAND["expected"]

    def test_sand_vector(self):
        m = _i()
        assert m.classify_simple(
            TEST_SAND["clay"], TEST_SAND["silt"], TEST_SAND["sand"]
        ) == TEST_SAND["expected"]

    def test_validate_good(self):
        m = _i()
        assert m.validate_composition(33.3, 33.3, 33.4) is True

    def test_validate_edge_tolerance(self):
        m = _i()
        assert m.validate_composition(33, 33, 33.5) is True   # sum=99.5
        assert m.validate_composition(33, 33, 34.5) is True   # sum=100.5
        assert m.validate_composition(33, 33, 35) is False     # sum=101

    def test_is_sandy(self):
        m = _i()
        assert m.is_sandy(90, 5) is True
        assert m.is_sandy(85, 10) is False  # clay not < 10
        assert m.is_sandy(80, 5) is False   # sand < 85
