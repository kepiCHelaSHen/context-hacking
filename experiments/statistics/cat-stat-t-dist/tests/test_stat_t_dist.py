"""cat-stat-t-dist — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_t_dist_constants import *
IMPL = Path(__file__).parent.parent / "stat_t_dist.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_df_is_n_minus_1_not_n(self):
        """df must be n-1, not n — the single most common LLM error."""
        m = _i()
        assert m.degrees_of_freedom(N_SAMPLE) == DF_CORRECT
        assert m.degrees_of_freedom(N_SAMPLE) != DF_WRONG
    def test_se_uses_sqrt_n(self):
        """SE = s / sqrt(n), NOT s / n."""
        m = _i()
        se = m.standard_error(S_SAMPLE, N_SAMPLE)
        assert abs(se - SE) < 1e-9
        assert abs(se - S_SAMPLE / N_SAMPLE) > 0.1  # must differ from wrong formula

class TestCorrectness:
    def test_ci_bounds_match_frozen(self):
        """95% CI with correct df=24 must match frozen constants."""
        m = _i()
        lo, hi = m.confidence_interval(XBAR, S_SAMPLE, N_SAMPLE, T_CRIT_24)
        assert abs(lo - CI_LOWER) < 0.001, f"Lower bound {lo} != {CI_LOWER}"
        assert abs(hi - CI_UPPER) < 0.001, f"Upper bound {hi} != {CI_UPPER}"
    def test_t_statistic_computation(self):
        """t = (xbar - mu0) / SE; for xbar=100, mu0=95, SE=3 -> t=5/3."""
        m = _i()
        t = m.t_statistic(XBAR, 95.0, S_SAMPLE, N_SAMPLE)
        expected = (XBAR - 95.0) / SE  # 5 / 3 = 1.6667
        assert abs(t - expected) < 1e-6
