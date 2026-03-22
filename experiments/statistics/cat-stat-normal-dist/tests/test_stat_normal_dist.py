"""cat-stat-normal-dist — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_normal_dist_constants import *
IMPL = Path(__file__).parent.parent / "stat_normal_dist.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_689599_not_exact(self):
        """68-95-99.7 rule values must NOT be used as exact."""
        m = _i()
        # ±1σ ≈ 0.6827, not 0.68
        assert abs(m.symmetric_interval(1) - P_WITHIN_1SIGMA) < 1e-6
        assert abs(m.symmetric_interval(1) - 0.68) > 0.002
        # ±3σ ≈ 0.9973, not 0.997
        assert abs(m.symmetric_interval(3) - P_WITHIN_3SIGMA) < 1e-6
        assert abs(m.symmetric_interval(3) - 0.997) > 0.0003

    def test_pdf_not_probability(self):
        """PDF at the mean is a density (~0.3989), not bounded to small values."""
        m = _i()
        assert m.pdf(0) > 0.39
        assert abs(m.pdf(0) - ONE_OVER_SQRT2PI) < 1e-8


class TestCorrectness:
    def test_z_score(self):
        m = _i()
        assert abs(m.z_score(X_TEST, MU_TEST, SIGMA_TEST) - Z_TEST) < 1e-10

    def test_cdf_values(self):
        m = _i()
        assert abs(m.cdf_approx(1.5) - CDF_Z_TEST) < 1e-8
        assert abs(m.cdf_approx(1.96) - CDF_Z196) < 1e-8

    def test_symmetric_interval_2sigma(self):
        m = _i()
        assert abs(m.symmetric_interval(2) - P_WITHIN_2SIGMA) < 1e-8
