"""cat-stat-clt — Central Limit Theorem Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_clt_constants import *
IMPL = Path(__file__).parent.parent / "stat_clt.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_clt_does_not_apply_to_cauchy(self):
        """Cauchy has no finite mean and no finite variance — CLT does NOT apply."""
        m = _i()
        assert not m.clt_applies(CAUCHY_HAS_MEAN, CAUCHY_HAS_VARIANCE)
        # Also verify via explicit False flags
        assert not m.clt_applies(False, False)

    def test_finite_mean_alone_not_sufficient(self):
        """Having only a finite mean (but not finite variance) is NOT enough for CLT."""
        m = _i()
        assert not m.clt_applies(True, False)

    def test_finite_variance_alone_not_sufficient(self):
        """Having only a finite variance (but not finite mean) is NOT enough for CLT."""
        m = _i()
        assert not m.clt_applies(False, True)

    def test_se_uses_sqrt_n(self):
        """SE = σ/√n, NOT σ.  The √n denominator is essential."""
        m = _i()
        se = m.sampling_se(SIGMA_UNIFORM, 30)
        # SE must be much smaller than σ itself
        assert se < SIGMA_UNIFORM
        # SE must match σ/√n, not σ
        assert abs(se - SIGMA_UNIFORM) > 0.1  # they must differ
        assert abs(se - SE_30) < 1e-12        # must match frozen value


class TestCorrectness:
    def test_se_n30(self):
        """SE for n=30: σ/√30 ≈ 0.05270."""
        m = _i()
        se = m.sampling_se(SIGMA_UNIFORM, 30)
        assert abs(se - SE_30) < 1e-12

    def test_se_n100(self):
        """SE for n=100: σ/√100 = σ/10 ≈ 0.02887."""
        m = _i()
        se = m.sampling_se(SIGMA_UNIFORM, 100)
        assert abs(se - SE_100) < 1e-12

    def test_uniform_mean(self):
        """Mean of Uniform(0,1) = 0.5."""
        m = _i()
        assert abs(m.uniform_mean(0, 1) - MU_UNIFORM) < 1e-15

    def test_uniform_variance(self):
        """Variance of Uniform(0,1) = 1/12."""
        m = _i()
        assert abs(m.uniform_variance(0, 1) - VAR_UNIFORM) < 1e-15

    def test_sampling_distribution_params(self):
        """sampling_distribution_params returns (μ, σ/√n)."""
        m = _i()
        mean, se = m.sampling_distribution_params(MU_UNIFORM, SIGMA_UNIFORM, 30)
        assert abs(mean - MU_UNIFORM) < 1e-15
        assert abs(se - SE_30) < 1e-12

    def test_clt_applies_normal(self):
        """CLT applies to distributions with finite mean and finite variance."""
        m = _i()
        assert m.clt_applies(True, True)
