"""cat-econ-portfolio — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_portfolio_constants import *
IMPL = Path(__file__).parent.parent / "econ_portfolio.py"

def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_no_covariance_caught(self):
        """Variance MUST include 2*w1*w2*sigma12. If omitted, result is too low."""
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, RHO)
        var_wrong = W1**2 * S1**2 + W2**2 * S2**2  # missing covariance
        assert var_p > var_wrong, "Covariance term is missing — variance too low"
        assert abs(var_p - VAR_P) < 1e-8

    def test_not_weighted_avg(self):
        """Portfolio std is NOT simply w1*s1 + w2*s2."""
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, RHO)
        std_p = m.portfolio_std(var_p)
        naive_std = W1 * S1 + W2 * S2  # wrong: weighted average of stds
        assert abs(std_p - naive_std) > 0.01, "Should not equal weighted avg of stds"

    def test_correlation_used(self):
        """Different rho values MUST produce different variances."""
        m = _i()
        var_rho03 = m.portfolio_variance_2asset(W1, W2, S1, S2, 0.3)
        var_rho00 = m.portfolio_variance_2asset(W1, W2, S1, S2, 0.0)
        var_rho10 = m.portfolio_variance_2asset(W1, W2, S1, S2, 1.0)
        assert var_rho10 > var_rho03 > var_rho00, "Variance must increase with correlation"


class TestCorrectness:
    """Verify results against frozen spec values."""

    def test_portfolio_return(self):
        m = _i()
        er_p = m.portfolio_return([W1, W2], [ER1, ER2])
        assert abs(er_p - ER_P) < 1e-10

    def test_covariance(self):
        m = _i()
        cov = m.covariance(S1, S2, RHO)
        assert abs(cov - COV12) < 1e-10

    def test_portfolio_variance(self):
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, RHO)
        assert abs(var_p - VAR_P) < 1e-8

    def test_portfolio_std(self):
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, RHO)
        std_p = m.portfolio_std(var_p)
        assert abs(std_p - STD_P) < 1e-6

    def test_diversification_benefit_positive(self):
        """When rho < 1, diversification benefit must be positive."""
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, RHO)
        std_p = m.portfolio_std(var_p)
        benefit = m.diversification_benefit(S1, S2, std_p, W1, W2)
        assert benefit > 0
        assert abs(benefit - DIV_BENEFIT) < 1e-6

    def test_perfect_correlation_no_benefit(self):
        """When rho=1, portfolio std = weighted avg std (no diversification)."""
        m = _i()
        var_p = m.portfolio_variance_2asset(W1, W2, S1, S2, 1.0)
        std_p = m.portfolio_std(var_p)
        benefit = m.diversification_benefit(S1, S2, std_p, W1, W2)
        assert abs(benefit) < 1e-10
