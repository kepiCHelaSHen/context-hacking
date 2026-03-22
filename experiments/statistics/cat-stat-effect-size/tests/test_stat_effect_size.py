"""cat-stat-effect-size — Pooled-SD Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_effect_size_constants import *
IMPL = Path(__file__).parent.parent / "stat_effect_size.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_pooled_sd_differs_from_simple_average(self):
        """When n₁ ≠ n₂ the correct pooled SD must differ from √((s₁²+s₂²)/2).

        The equal-n shortcut is the most common LLM error for Cohen's d.
        """
        m = _i()
        correct = m.pooled_sd(S1, N1, S2, N2)
        wrong = math.sqrt((S1**2 + S2**2) / 2)
        # They must not be equal (sample sizes differ: 30 vs 25)
        assert abs(correct - wrong) > 0.05, (
            f"pooled_sd returned {correct}, which is suspiciously close to "
            f"the equal-n shortcut {wrong}"
        )
        # Correct value must match frozen constant
        assert abs(correct - SD_POOLED_CORRECT) < 1e-10

    def test_cohens_d_uses_pooled_not_individual_sd(self):
        """Cohen's d must use the pooled SD, not s₁ or s₂ alone."""
        m = _i()
        sd = m.pooled_sd(S1, N1, S2, N2)
        d = m.cohens_d(M1, M2, sd)
        # d with s1 alone: 5/10 = 0.5
        d_s1_only = (M1 - M2) / S1
        # d with s2 alone: 5/12 ≈ 0.4167
        d_s2_only = (M1 - M2) / S2
        # Correct d must differ from both
        assert abs(d - d_s1_only) > 0.01
        assert abs(d - d_s2_only) > 0.01
        assert abs(d - D_CORRECT) < 1e-10

    def test_pooled_sd_equal_when_n_equal(self):
        """When n₁ = n₂ the two pooled SD formulas must agree."""
        m = _i()
        # Use equal sample sizes
        n = 30
        correct = m.pooled_sd(S1, n, S2, n)
        shortcut = math.sqrt((S1**2 + S2**2) / 2)
        assert abs(correct - shortcut) < 1e-10, (
            "With equal n, both formulas should give the same result"
        )


class TestCorrectness:
    def test_pooled_sd_value(self):
        """SD_pooled must match the frozen constant."""
        m = _i()
        sd = m.pooled_sd(S1, N1, S2, N2)
        assert abs(sd - SD_POOLED_CORRECT) < 1e-10

    def test_cohens_d_value(self):
        """Cohen's d must match the frozen constant."""
        m = _i()
        sd = m.pooled_sd(S1, N1, S2, N2)
        d = m.cohens_d(M1, M2, sd)
        assert abs(d - D_CORRECT) < 1e-10

    def test_eta_squared_value(self):
        """η² = SS_between / SS_total must match frozen constant."""
        m = _i()
        eta = m.eta_squared(SS_BETWEEN, SS_TOTAL)
        assert abs(eta - ETA_SQUARED) < 1e-12

    def test_eta_squared_is_proportion(self):
        """η² must be in [0, 1]."""
        m = _i()
        eta = m.eta_squared(SS_BETWEEN, SS_TOTAL)
        assert 0.0 <= eta <= 1.0

    def test_d_category_small(self):
        """Our test d ≈ 0.457 should classify as 'small' (0.2 ≤ |d| < 0.5)."""
        m = _i()
        sd = m.pooled_sd(S1, N1, S2, N2)
        d = m.cohens_d(M1, M2, sd)
        assert m.d_category(d) == "small"

    def test_d_category_boundaries(self):
        """Verify Cohen's d category boundaries."""
        m = _i()
        assert m.d_category(0.1) == "negligible"
        assert m.d_category(0.2) == "small"
        assert m.d_category(0.49) == "small"
        assert m.d_category(0.5) == "medium"
        assert m.d_category(0.79) == "medium"
        assert m.d_category(0.8) == "large"
        assert m.d_category(1.5) == "large"
        # Negative values use absolute value
        assert m.d_category(-0.6) == "medium"
