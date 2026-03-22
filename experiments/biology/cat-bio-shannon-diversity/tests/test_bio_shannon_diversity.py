"""cat-bio-shannon-diversity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_shannon_diversity_constants import *
IMPL = Path(__file__).parent.parent / "bio_shannon_diversity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_log2_not_ln(self):
        """H'(ln) must differ from H(log2)."""
        m = _i()
        H_ln = m.shannon_index(SPECIES_COUNTS)
        H_l2 = m.shannon_log2(SPECIES_COUNTS)
        assert abs(H_ln - H_l2) > 0.1, "H'(ln) and H(log2) must differ"
        assert H_l2 > H_ln, "H(log2) > H'(ln) by factor 1/ln2"

    def test_evenness_leq_1(self):
        """Pielou J must be in [0, 1]."""
        m = _i()
        H = m.shannon_index(SPECIES_COUNTS)
        Hm = m.max_diversity(NUM_SPECIES)
        J = m.evenness(H, Hm)
        assert 0.0 <= J <= 1.0

    def test_mixed_bases_detected(self):
        """Mixing log2 H with ln H_max gives J > 1 — base mismatch."""
        m = _i()
        H_log2 = m.shannon_log2(SPECIES_COUNTS)
        Hm_ln = m.max_diversity(NUM_SPECIES)
        bad_J = H_log2 / Hm_ln
        assert bad_J > 1.0, "Mixing bases must yield J > 1"

    def test_evenness_raises_on_bad_bases(self):
        m = _i()
        H_log2 = m.shannon_log2(SPECIES_COUNTS)
        Hm_ln = m.max_diversity(NUM_SPECIES)
        with pytest.raises(ValueError):
            m.evenness(H_log2, Hm_ln)

class TestCorrectness:
    def test_shannon_index_value(self):
        m = _i()
        assert abs(m.shannon_index(SPECIES_COUNTS) - SHANNON_LN) < 1e-10

    def test_shannon_log2_value(self):
        m = _i()
        assert abs(m.shannon_log2(SPECIES_COUNTS) - SHANNON_LOG2) < 1e-10

    def test_max_diversity(self):
        m = _i()
        assert abs(m.max_diversity(NUM_SPECIES) - HMAX_LN) < 1e-10

    def test_evenness_value(self):
        m = _i()
        assert abs(m.evenness(SHANNON_LN, HMAX_LN) - EVENNESS_J) < 1e-10

    def test_equal_abundance_j_one(self):
        m = _i()
        H = m.shannon_index(EQUAL_COUNTS)
        Hm = m.max_diversity(len(EQUAL_COUNTS))
        J = m.evenness(H, Hm)
        assert abs(J - 1.0) < 1e-9

    def test_log2_identity(self):
        """H(log2) = H'(ln) / ln(2)."""
        m = _i()
        H_ln = m.shannon_index(SPECIES_COUNTS)
        H_l2 = m.shannon_log2(SPECIES_COUNTS)
        assert abs(H_l2 - H_ln / math.log(2)) < 1e-10

    def test_zero_count_ignored(self):
        m = _i()
        counts_with_zero = list(SPECIES_COUNTS) + [0]
        assert abs(m.shannon_index(counts_with_zero) - SHANNON_LN) < 1e-10

    def test_single_species_zero(self):
        m = _i()
        assert abs(m.shannon_index([100]) - 0.0) < 1e-10

    def test_negative_count_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.shannon_index([10, -5, 20])

    def test_empty_community_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.shannon_index([0, 0, 0])
