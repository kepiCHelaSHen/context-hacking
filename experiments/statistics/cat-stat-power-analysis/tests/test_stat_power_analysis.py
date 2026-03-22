"""cat-stat-power-analysis — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_power_analysis_constants import *
IMPL = Path(__file__).parent.parent / "stat_power_analysis.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_cohens_d_standardises_not_raw(self):
        """raw_not_standardized: d must equal Delta/sigma, NOT Delta itself."""
        m = _i()
        d = m.cohens_d(DELTA_RAW, SIGMA)
        assert abs(d - D_CORRECT) < 1e-6
        assert abs(d - DELTA_RAW) > 1.0, "cohens_d returned raw difference, forgot to divide by sigma"

    def test_sample_size_rounds_up(self):
        """forgets_round_up: n must be an integer, rounded UP."""
        m = _i()
        n = m.sample_size_per_group(D_CORRECT, Z_ALPHA2, Z_BETA)
        assert isinstance(n, int), "sample_size_per_group must return an int"
        assert n > 62, "sample size must be rounded UP (ceil), not down"

    def test_per_group_not_total(self):
        """one_group_n: sample_size_per_group returns n for ONE group."""
        m = _i()
        n = m.sample_size_per_group(D_CORRECT, Z_ALPHA2, Z_BETA)
        total = m.total_sample_size(n)
        assert total == 2 * n

class TestCorrectness:
    def test_n_per_group_is_63(self):
        m = _i()
        n = m.sample_size_per_group(D_CORRECT, Z_ALPHA2, Z_BETA)
        assert n == N_PER_GROUP

    def test_total_sample_size_is_126(self):
        m = _i()
        assert m.total_sample_size(N_PER_GROUP) == 126

    def test_effect_size_category_small(self):
        m = _i()
        assert m.effect_size_category(D_SMALL) == "small"
        assert m.effect_size_category(0.1) == "small"

    def test_effect_size_category_medium(self):
        m = _i()
        assert m.effect_size_category(D_MEDIUM) == "medium"
        assert m.effect_size_category(0.5) == "medium"

    def test_effect_size_category_large(self):
        m = _i()
        assert m.effect_size_category(D_LARGE) == "large"
        assert m.effect_size_category(1.0) == "large"

    def test_cohens_d_basic(self):
        m = _i()
        assert abs(m.cohens_d(10, 20) - 0.5) < 1e-6
        assert abs(m.cohens_d(0, 10) - 0.0) < 1e-6
        assert abs(m.cohens_d(8, 10) - 0.8) < 1e-6

    def test_cohens_d_rejects_nonpositive_sigma(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cohens_d(5, 0)
        with pytest.raises(ValueError):
            m.cohens_d(5, -1)

    def test_sample_size_rejects_nonpositive_d(self):
        m = _i()
        with pytest.raises(ValueError):
            m.sample_size_per_group(0, Z_ALPHA2, Z_BETA)
        with pytest.raises(ValueError):
            m.sample_size_per_group(-0.5, Z_ALPHA2, Z_BETA)
