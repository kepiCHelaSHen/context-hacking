"""cat-stat-mle — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_mle_constants import *
IMPL = Path(__file__).parent.parent / "stat_mle.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_mle_variance_divides_by_n_not_n_minus_1(self):
        """MLE of σ² divides by n (biased). Using n-1 is unbiased, not MLE."""
        m = _i()
        var_mle = m.mle_variance(list(DATA))
        assert abs(var_mle - MLE_VAR) < 1e-9, "MLE variance should be 8.0 (divides by n)"
        assert abs(var_mle - UNBIASED_VAR) > 0.5, "MLE variance must NOT equal the unbiased variance"

    def test_exp_mle_is_reciprocal_of_mean(self):
        """MLE of exponential λ = 1/x̄, not x̄."""
        m = _i()
        lam = m.mle_exp_lambda(list(DATA))
        assert abs(lam - MLE_LAMBDA_EXP) < 1e-9, "Exp MLE λ should be 1/x̄"
        assert abs(lam - XBAR) > 1.0, "Exp MLE λ must NOT equal x̄"


class TestCorrectness:
    def test_mle_mean(self):
        m = _i()
        assert abs(m.mle_mean(list(DATA)) - XBAR) < 1e-9

    def test_mle_variance_value(self):
        m = _i()
        assert abs(m.mle_variance(list(DATA)) - 8.0) < 1e-9

    def test_loglikelihood_is_negative(self):
        """Normal log-likelihood at MLE is always negative for finite data."""
        m = _i()
        ll = m.normal_loglikelihood(list(DATA), XBAR, MLE_VAR)
        assert ll < 0, "Log-likelihood should be negative"
        assert abs(ll - LOGLIK_AT_MLE) < 1e-4, f"Log-likelihood should be ≈{LOGLIK_AT_MLE:.4f}"
