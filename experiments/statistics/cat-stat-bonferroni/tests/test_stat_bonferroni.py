"""cat-stat-bonferroni — Multiple Comparisons Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_bonferroni_constants import *
IMPL = Path(__file__).parent.parent / "stat_bonferroni.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_bh_rejects_more_than_bonferroni(self):
        """BH (FDR) must reject strictly more hypotheses than Bonferroni.

        The 'bonferroni_sufficient' error assumes Bonferroni is enough;
        BH is less conservative and should discover more true effects.
        """
        m = _i()
        bonf = m.count_rejections(m.bonferroni_reject(P_VALUES, ALPHA))
        bh = m.count_rejections(m.bh_reject(P_VALUES, ALPHA))
        assert bh > bonf, (
            f"BH should reject more than Bonferroni: BH={bh}, Bonf={bonf}"
        )

    def test_bonferroni_threshold_below_alpha(self):
        """Bonferroni threshold must be strictly less than original α.

        The 'no_correction_needed' error skips correction entirely.
        """
        m = _i()
        thresh = m.bonferroni_threshold(ALPHA, M)
        assert thresh < ALPHA, (
            f"Bonferroni threshold {thresh} must be < α={ALPHA}"
        )


class TestCorrectness:
    def test_bonferroni_threshold_value(self):
        """Bonferroni threshold = α/m = 0.05/10 = 0.005."""
        m = _i()
        assert abs(m.bonferroni_threshold(ALPHA, M) - BONFERRONI_THRESHOLD) < 1e-12

    def test_bonferroni_rejection_count(self):
        """Bonferroni must reject exactly 2 hypotheses."""
        m = _i()
        n = m.count_rejections(m.bonferroni_reject(P_VALUES, ALPHA))
        assert n == BONFERRONI_REJECTIONS

    def test_bh_rejection_count(self):
        """BH must reject exactly 5 hypotheses."""
        m = _i()
        n = m.count_rejections(m.bh_reject(P_VALUES, ALPHA))
        assert n == BH_REJECTIONS

    def test_bh_largest_k(self):
        """BH largest k (the step-up cutoff) must equal 5.

        Verifying the BH step-up: the first 5 sorted p-values satisfy
        p_(k) ≤ (k/m)·α, while p_(6) = 0.04 > 0.03 = (6/10)·0.05.
        """
        m = _i()
        rejects = m.bh_reject(P_VALUES, ALPHA)
        # The first BH_LARGEST_K sorted p-values must be rejected
        sorted_pvals = sorted(range(len(P_VALUES)), key=lambda i: P_VALUES[i])
        for rank, idx in enumerate(sorted_pvals):
            if rank < BH_LARGEST_K:
                assert rejects[idx], f"Rank {rank+1} (p={P_VALUES[idx]}) should be rejected"
            else:
                assert not rejects[idx], f"Rank {rank+1} (p={P_VALUES[idx]}) should NOT be rejected"
