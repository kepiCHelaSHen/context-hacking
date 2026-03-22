"""cat-bio-dna-melting — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_dna_melting_constants import *
IMPL = Path(__file__).parent.parent / "bio_dna_melting.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM errors from PRIOR_ERRORS."""

    def test_wallace_same_for_different_order(self):
        """order_irrelevant: Wallace gives SAME Tm for seqs with same composition
        but different order — proving Wallace ignores order (which is a weakness)."""
        m = _i()
        tm1 = m.wallace_tm(SEQ1)
        tm2 = m.wallace_tm(SEQ2)
        assert tm1 == tm2 == WALLACE_TM_1, (
            f"Wallace should give identical Tm for same-composition seqs: "
            f"got {tm1} vs {tm2}, expected {WALLACE_TM_1}"
        )

    def test_nn_pairs_differ_for_different_order(self):
        """order_irrelevant: NN pairs MUST differ when base order differs —
        this is the whole point of nearest-neighbor over %GC."""
        m = _i()
        pairs1 = m.nn_pairs(SEQ1)
        pairs2 = m.nn_pairs(SEQ2)
        assert pairs1 != pairs2, (
            "NN pairs should differ for sequences with different base order"
        )
        # Verify against frozen expected pairs
        assert tuple(pairs1) == NN_PAIRS_SEQ1
        assert tuple(pairs2) == NN_PAIRS_SEQ2

    def test_gc_content_identical_for_both(self):
        """gc_method_accurate: Both seqs have same GC content — so any
        %GC-based method cannot distinguish them. NN method can."""
        m = _i()
        gc1 = m.gc_content(SEQ1)
        gc2 = m.gc_content(SEQ2)
        assert gc1 == gc2 == SEQ1_GC, (
            f"Both seqs should have GC={SEQ1_GC}: got {gc1}, {gc2}"
        )


class TestCorrectness:
    """Verify core computation logic."""

    def test_wallace_tm_basic(self):
        """Wallace rule: Tm = 2*(A+T) + 4*(G+C) for ATCGATCG."""
        m = _i()
        assert m.wallace_tm(TEST_SEQ) == TEST_WALLACE_TM

    def test_gc_content(self):
        """GC content of AATTGGCC = 4/8 = 0.50."""
        m = _i()
        assert m.gc_content(SEQ1) == pytest.approx(0.50)

    def test_gc_content_all_gc(self):
        """GC content of GGCC = 1.0."""
        m = _i()
        assert m.gc_content("GGCC") == pytest.approx(1.0)

    def test_gc_content_no_gc(self):
        """GC content of AATT = 0.0."""
        m = _i()
        assert m.gc_content("AATT") == pytest.approx(0.0)

    def test_base_counts(self):
        """Base counts for SEQ1: A=2, T=2, G=2, C=2."""
        m = _i()
        counts = m.base_counts(SEQ1)
        assert counts == {"A": 2, "T": 2, "G": 2, "C": 2}

    def test_base_counts_case_insensitive(self):
        """base_counts should handle lowercase input."""
        m = _i()
        counts = m.base_counts("aattggcc")
        assert counts == {"A": 2, "T": 2, "G": 2, "C": 2}

    def test_nn_pairs_length(self):
        """An 8-bp sequence has 7 nearest-neighbor steps."""
        m = _i()
        pairs = m.nn_pairs(SEQ1)
        assert len(pairs) == SEQ1_LENGTH - 1

    def test_nn_pairs_seq1(self):
        """NN pairs for AATTGGCC: AA, AT, TT, TG, GG, GC, CC."""
        m = _i()
        assert tuple(m.nn_pairs(SEQ1)) == NN_PAIRS_SEQ1

    def test_nn_pairs_seq2(self):
        """NN pairs for AGCTCGAT: AG, GC, CT, TC, CG, GA, AT."""
        m = _i()
        assert tuple(m.nn_pairs(SEQ2)) == NN_PAIRS_SEQ2

    def test_invalid_base_raises(self):
        """Invalid DNA base should raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.base_counts("ATXG")
