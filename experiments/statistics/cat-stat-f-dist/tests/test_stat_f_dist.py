"""cat-stat-f-dist — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_f_dist_constants import *
IMPL = Path(__file__).parent.parent / "stat_f_dist.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


class TestPriorErrors:
    """Guard against documented LLM hallucination patterns."""

    def test_f_is_msb_over_msw_not_inverted(self):
        """PRIOR_ERROR: f_msw_over_msb — F must be MSB/MSW, not MSW/MSB."""
        m = _i()
        F = m.f_statistic(MSB, MSW)
        # MSB=125, MSW=10 → F=12.5, NOT 0.08
        assert F == pytest.approx(12.5, abs=0.01)
        assert F > 1.0, "F = MSB/MSW should be >1 when MSB > MSW"

    def test_df_between_is_k_minus_1(self):
        """PRIOR_ERROR: df_swapped — df_between must be k-1, not N-k."""
        m = _i()
        df_b, _ = m.anova_df(K_GROUPS, N_TOTAL)
        assert df_b == DF_BETWEEN  # 2, not 12

    def test_df_within_is_N_minus_k(self):
        """PRIOR_ERROR: df_swapped / df_within_n_minus_1 — df_within must be N-k, not k-1 or N-1."""
        m = _i()
        _, df_w = m.anova_df(K_GROUPS, N_TOTAL)
        assert df_w == DF_WITHIN   # 12, not 2 and not 14
        assert df_w != N_TOTAL - 1, "df_within should be N-k, not N-1"


class TestCorrectness:
    """Verify numerical results against frozen constants."""

    def test_ssb_value(self):
        m = _i()
        ssb = m.ss_between(GROUP_MEANS, OVERALL_MEAN, N_PER_GROUP)
        assert ssb == pytest.approx(SSB, abs=0.01)  # 250.0

    def test_f_statistic_value(self):
        m = _i()
        F = m.f_statistic(MSB, MSW)
        assert F == pytest.approx(F_STAT, abs=0.01)  # 12.5

    def test_df_tuple(self):
        m = _i()
        df = m.anova_df(K_GROUPS, N_TOTAL)
        assert df == (DF_BETWEEN, DF_WITHIN)  # (2, 12)

    def test_ss_within_from_total(self):
        m = _i()
        ss_total = SSB + SSW  # 370
        ssw = m.ss_within_from_total(ss_total, SSB)
        assert ssw == pytest.approx(SSW, abs=0.01)  # 120.0

    def test_mean_square(self):
        m = _i()
        assert m.ms(SSB, DF_BETWEEN) == pytest.approx(MSB, abs=0.01)
        assert m.ms(SSW, DF_WITHIN) == pytest.approx(MSW, abs=0.01)
