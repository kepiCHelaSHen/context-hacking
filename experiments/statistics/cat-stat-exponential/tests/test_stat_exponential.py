"""cat-stat-exponential — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_exponential_constants import *
IMPL = Path(__file__).parent.parent / "stat_exponential.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_mean_is_one_over_lambda_not_lambda(self):
        """Mean must be 1/lam, NOT lam — the single most common LLM error."""
        m = _i()
        computed = m.exp_mean(LAMBDA)
        assert abs(computed - MEAN) < 1e-12, f"exp_mean({LAMBDA}) = {computed}, expected {MEAN}"
        assert abs(computed - MEAN_WRONG) > 0.1, "Mean must NOT equal lambda"

    def test_variance_is_one_over_lambda_squared(self):
        """Variance must be 1/lam^2, NOT lam."""
        m = _i()
        computed = m.exp_variance(LAMBDA)
        assert abs(computed - VARIANCE) < 1e-12, f"exp_variance({LAMBDA}) = {computed}, expected {VARIANCE}"
        assert abs(computed - VARIANCE_WRONG) > 0.1, "Variance must NOT equal lambda"

    def test_memoryless_property_holds(self):
        """P(X > s+t | X > s) must equal P(X > t) — memoryless property."""
        m = _i()
        cond, marg = m.memoryless_check(LAMBDA, MEMORYLESS_S, MEMORYLESS_T)
        assert abs(cond - marg) < 1e-12, (
            f"Memoryless violated: P(X>{MEMORYLESS_S+MEMORYLESS_T}|X>{MEMORYLESS_S})"
            f"={cond:.9f} != P(X>{MEMORYLESS_T})={marg:.9f}"
        )
        assert abs(cond - MEMORYLESS_COND) < 1e-9

class TestCorrectness:
    def test_cdf_at_1(self):
        """P(X <= 1) for lam=0.5 must match frozen constant."""
        m = _i()
        assert abs(m.exp_cdf(LAMBDA, 1) - CDF_1) < 1e-9, f"CDF(1) mismatch"

    def test_cdf_at_2(self):
        """P(X <= 2) for lam=0.5 must match frozen constant."""
        m = _i()
        assert abs(m.exp_cdf(LAMBDA, 2) - CDF_2) < 1e-9, f"CDF(2) mismatch"

    def test_survival_at_3(self):
        """P(X > 3) = e^(-1.5) must match frozen constant."""
        m = _i()
        assert abs(m.exp_survival(LAMBDA, 3) - SURV_3) < 1e-9, f"Survival(3) mismatch"

    def test_pdf_values(self):
        """PDF spot-checks at x=1 and x=2."""
        m = _i()
        assert abs(m.exp_pdf(LAMBDA, 1) - PDF_1) < 1e-9
        assert abs(m.exp_pdf(LAMBDA, 2) - PDF_2) < 1e-9

    def test_cdf_and_survival_sum_to_one(self):
        """CDF(x) + S(x) = 1 for any x >= 0."""
        m = _i()
        for x in [0.5, 1.0, 2.0, 5.0, 10.0]:
            total = m.exp_cdf(LAMBDA, x) + m.exp_survival(LAMBDA, x)
            assert abs(total - 1.0) < 1e-12, f"CDF+Survival != 1 at x={x}"
