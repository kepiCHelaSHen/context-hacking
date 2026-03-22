"""cat-bio-phylogenetic-distance — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_phylogenetic_distance_constants import *
IMPL = Path(__file__).parent.parent / "bio_phylogenetic_distance.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_jc_exceeds_raw_for_all_positive_p(self):
        """The #1 LLM error: using raw p instead of JC-corrected d."""
        m = _i()
        for p_val in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60]:
            d = m.jukes_cantor(p_val)
            assert d > p_val, (
                f"JC distance {d:.6f} must exceed raw distance {p_val} — "
                f"raw_not_corrected error?"
            )

    def test_correction_diverges_near_saturation(self):
        """JC correction must grow without bound as p -> 0.75."""
        m = _i()
        # At p = 0.74 the correction should be very large
        d_074 = m.jukes_cantor(0.74)
        assert d_074 > 3.0, f"At p=0.74, d={d_074:.4f} — should be very large (diverges at 0.75)"
        # At p = 0.75 should raise or return inf
        with pytest.raises(ValueError):
            m.jukes_cantor(0.75)

    def test_wrong_formula_constants(self):
        """Ensure the 3/4 and 4/3 constants are correct, not swapped or wrong."""
        m = _i()
        d = m.jukes_cantor(RAW_P)
        # If someone used -(2/3)*ln(1-(3/2)*p) that would give a different answer
        wrong_d = -(2 / 3) * math.log(1 - (3 / 2) * RAW_P)
        assert not math.isclose(d, wrong_d, rel_tol=1e-3), (
            f"Got d={d:.6f} which matches wrong formula — wrong_correction_formula error"
        )


class TestCorrectness:
    def test_count_differences(self):
        """Count mismatches between test sequences."""
        m = _i()
        assert m.count_differences(SEQ1, SEQ2) == 2

    def test_raw_distance(self):
        """Raw distance p = differences / length."""
        m = _i()
        p = m.raw_distance(SEQ1, SEQ2)
        assert math.isclose(p, RAW_P, rel_tol=1e-9), f"Raw p={p}, expected {RAW_P}"

    def test_jc_at_p025(self):
        """JC distance at p=0.25 (test sequences)."""
        m = _i()
        d = m.jukes_cantor(RAW_P)
        assert math.isclose(d, JC_D, rel_tol=1e-3), f"JC d={d:.6f}, expected {JC_D}"

    def test_jc_at_p030(self):
        """JC distance at p=0.3."""
        m = _i()
        d = m.jukes_cantor(0.3)
        assert math.isclose(d, JC_D_03, rel_tol=1e-3), f"JC d={d:.6f}, expected {JC_D_03}"

    def test_saturation_check_below(self):
        """p=0.25 should not be flagged as saturated."""
        m = _i()
        assert m.is_saturated(RAW_P) is False

    def test_saturation_check_above(self):
        """p=0.72 should be flagged as saturated (threshold=0.70)."""
        m = _i()
        assert m.is_saturated(0.72) is True

    def test_jc_zero_distance(self):
        """Identical sequences should give distance 0."""
        m = _i()
        assert m.jukes_cantor(0.0) == 0.0

    def test_end_to_end(self):
        """Full pipeline: sequences -> raw distance -> JC correction."""
        m = _i()
        p = m.raw_distance(SEQ1, SEQ2)
        d = m.jukes_cantor(p)
        assert math.isclose(p, RAW_P, rel_tol=1e-9)
        assert math.isclose(d, JC_D, rel_tol=1e-3)
        assert d > p, "JC corrected distance must exceed raw distance"
