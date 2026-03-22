"""cat-econ-cobb-douglas — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_cobb_douglas_constants import *
IMPL = Path(__file__).parent.parent / "econ_cobb_douglas.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_exponents_need_not_sum_to_1(self):
        """PRIOR_ERROR: exponents_sum_1 — alpha+beta can exceed 1 (IRS)."""
        m = _i()
        # Must accept alpha+beta = 1.1 without error
        Y = m.cobb_douglas(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        assert Y > 0
        assert ALPHA_TEST + BETA_TEST > 1.0  # confirms IRS case

    def test_mpk_uses_alpha_minus_1(self):
        """PRIOR_ERROR: mpk_wrong_exponent — exponent on K must be alpha-1."""
        m = _i()
        result = m.mpk(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        assert abs(result - MPK_TEST) < 0.001

    def test_irs_is_possible(self):
        """PRIOR_ERROR: irs_impossible — IRS exists when alpha+beta > 1."""
        m = _i()
        rts = m.returns_to_scale(ALPHA_TEST, BETA_TEST)
        assert rts == "increasing"


class TestCorrectness:
    def test_cobb_douglas_baseline(self):
        """Y(K=100, L=200) with alpha=0.4, beta=0.7."""
        m = _i()
        Y = m.cobb_douglas(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        assert abs(Y - Y1) < 0.01

    def test_cobb_douglas_doubled(self):
        """Y(K=200, L=400) with alpha=0.4, beta=0.7."""
        m = _i()
        Y = m.cobb_douglas(A_TEST, K2, ALPHA_TEST, L2, BETA_TEST)
        assert abs(Y - Y2) < 0.01

    def test_doubling_ratio_exceeds_2(self):
        """With IRS (alpha+beta=1.1), doubling inputs more than doubles output."""
        m = _i()
        Y_base = m.cobb_douglas(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        Y_doubled = m.cobb_douglas(A_TEST, K2, ALPHA_TEST, L2, BETA_TEST)
        ratio = Y_doubled / Y_base
        assert ratio > 2.0
        assert abs(ratio - THEORETICAL_RATIO) < 0.01

    def test_returns_to_scale_increasing(self):
        m = _i()
        assert m.returns_to_scale(0.4, 0.7) == "increasing"

    def test_returns_to_scale_constant(self):
        m = _i()
        assert m.returns_to_scale(0.3, 0.7) == "constant"

    def test_returns_to_scale_decreasing(self):
        m = _i()
        assert m.returns_to_scale(0.3, 0.5) == "decreasing"

    def test_mpk_value(self):
        m = _i()
        result = m.mpk(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        assert abs(result - MPK_TEST) < 0.001

    def test_mpl_value(self):
        m = _i()
        result = m.mpl(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
        assert abs(result - MPL_TEST) < 0.001

    def test_factor_shares_under_crs(self):
        """Under CRS, MPL*L/Y = beta and MPK*K/Y = alpha (Euler's theorem)."""
        m = _i()
        K, L = 50, 100
        Y = m.cobb_douglas(1, K, ALPHA_CRS, L, BETA_CRS)
        labor_share = m.mpl(1, K, ALPHA_CRS, L, BETA_CRS) * L / Y
        capital_share = m.mpk(1, K, ALPHA_CRS, L, BETA_CRS) * K / Y
        assert abs(labor_share - LABOR_SHARE_CRS) < 1e-9
        assert abs(capital_share - CAPITAL_SHARE_CRS) < 1e-9

    def test_tfp_scales_output(self):
        """Doubling A doubles output."""
        m = _i()
        Y_A1 = m.cobb_douglas(1, K1, ALPHA_TEST, L1, BETA_TEST)
        Y_A2 = m.cobb_douglas(2, K1, ALPHA_TEST, L1, BETA_TEST)
        assert abs(Y_A2 / Y_A1 - 2.0) < 1e-9
