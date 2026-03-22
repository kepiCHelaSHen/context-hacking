"""cat-bio-simpson-diversity -- Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_simpson_diversity_constants import *
IMPL = Path(__file__).parent.parent / "bio_simpson_diversity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_d_is_dominance_not_diversity(self):
        """D is DOMINANCE: single-species community has D=1.0 (MAXIMUM D, minimum diversity)."""
        m = _i()
        d = m.simpson_D(SINGLE_COUNTS)
        assert math.isclose(d, 1.0, rel_tol=1e-9), (
            f"Single-species D should be 1.0 (max dominance), got {d}"
        )
        # And diversity should be 0 — if D were diversity, this would be wrong
        div = m.simpson_diversity(SINGLE_COUNTS)
        assert math.isclose(div, 0.0, abs_tol=1e-9), (
            f"Single-species diversity (1-D) should be 0.0, got {div}"
        )

    def test_reciprocal_not_equal_complement(self):
        """1/D != 1-D — these are different measures and must not be confused."""
        m = _i()
        d = m.simpson_D(COUNTS)
        div = m.simpson_diversity(COUNTS)
        rec = m.simpson_reciprocal(COUNTS)
        assert not math.isclose(div, rec, rel_tol=1e-3), (
            f"1-D ({div}) should differ from 1/D ({rec}) — they are different indices!"
        )


class TestCorrectness:
    def test_simpson_D(self):
        m = _i()
        d = m.simpson_D(COUNTS)
        assert math.isclose(d, D, rel_tol=1e-9), f"D={d}, expected {D}"

    def test_simpson_diversity(self):
        m = _i()
        div = m.simpson_diversity(COUNTS)
        assert math.isclose(div, DIVERSITY_1_MINUS_D, rel_tol=1e-9), (
            f"1-D={div}, expected {DIVERSITY_1_MINUS_D}"
        )

    def test_simpson_reciprocal(self):
        m = _i()
        rec = m.simpson_reciprocal(COUNTS)
        assert math.isclose(rec, RECIPROCAL_1_OVER_D, rel_tol=1e-9), (
            f"1/D={rec}, expected {RECIPROCAL_1_OVER_D}"
        )

    def test_even_community(self):
        """Perfectly even 5-species community: D=0.2, 1-D=0.8, 1/D=5.0."""
        m = _i()
        d = m.simpson_D(EVEN_COUNTS)
        div = m.simpson_diversity(EVEN_COUNTS)
        rec = m.simpson_reciprocal(EVEN_COUNTS)
        assert math.isclose(d, EVEN_D, rel_tol=1e-9), f"Even D={d}, expected {EVEN_D}"
        assert math.isclose(div, EVEN_DIVERSITY, rel_tol=1e-9)
        assert math.isclose(rec, EVEN_RECIPROCAL, rel_tol=1e-9)

    def test_single_species(self):
        """Single species: D=1.0, 1-D=0.0, 1/D=1.0."""
        m = _i()
        d = m.simpson_D(SINGLE_COUNTS)
        div = m.simpson_diversity(SINGLE_COUNTS)
        rec = m.simpson_reciprocal(SINGLE_COUNTS)
        assert math.isclose(d, SINGLE_D, rel_tol=1e-9)
        assert math.isclose(div, SINGLE_DIVERSITY, abs_tol=1e-9)
        assert math.isclose(rec, SINGLE_RECIPROCAL, rel_tol=1e-9)
