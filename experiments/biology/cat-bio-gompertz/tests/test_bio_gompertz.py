"""cat-bio-gompertz — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_gompertz_constants import *
IMPL = Path(__file__).parent.parent / "bio_gompertz.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_inflection_at_k_over_e_not_k_half(self):
        """The #1 LLM error: using K/2 (logistic) instead of K/e (Gompertz) for inflection."""
        m = _i()
        infl = m.gompertz_inflection(K)
        assert math.isclose(infl, INFLECTION_N, rel_tol=1e-9), (
            f"Inflection should be K/e={INFLECTION_N:.4f}, got {infl:.4f}"
        )
        assert not math.isclose(infl, WRONG_INFLECTION, rel_tol=0.01), (
            f"Got K/2={WRONG_INFLECTION} — that's the logistic inflection, not Gompertz!"
        )

    def test_growth_rate_includes_ln_term(self):
        """Growth rate must use -alpha*N*ln(N/K), not alpha*N*(1-N/K)."""
        m = _i()
        N_test = 500.0
        correct = -ALPHA * N_test * math.log(N_test / K)
        logistic_wrong = ALPHA * N_test * (1 - N_test / K)  # = 0.1 * 500 * 0.5 = 25.0
        result = m.gompertz_dNdt(ALPHA, K, N_test)
        assert math.isclose(result, correct, rel_tol=1e-9), (
            f"dN/dt should be {correct:.4f}, got {result:.4f}"
        )
        assert not math.isclose(result, logistic_wrong, rel_tol=0.01), (
            f"Got logistic rate {logistic_wrong:.4f} — missing ln(N/K) term!"
        )

    def test_asymmetry(self):
        """Gompertz is asymmetric: inflection at K/e ≈ 0.368*K, NOT at K/2 = 0.5*K."""
        m = _i()
        # The fundamental asymmetry: inflection is below the midpoint K/2.
        # In the logistic model, inflection is at exactly K/2.
        infl = m.gompertz_inflection(K)
        assert infl < K / 2, (
            f"Gompertz inflection ({infl:.1f}) must be below K/2 ({K/2:.1f}) — "
            f"it's asymmetric, not symmetric like logistic"
        )
        # Also verify via growth rates at wider spread
        N_below = INFLECTION_N - 200  # ~167.88
        N_above = INFLECTION_N + 200  # ~567.88
        rate_below = m.gompertz_dNdt(ALPHA, K, N_below)
        rate_above = m.gompertz_dNdt(ALPHA, K, N_above)
        assert not math.isclose(rate_below, rate_above, rel_tol=0.05), (
            f"Rates at N={N_below:.1f} and N={N_above:.1f} should differ (asymmetric), "
            f"got {rate_below:.4f} and {rate_above:.4f}"
        )

class TestCorrectness:
    def test_N_at_t0(self):
        """N(0) must equal N0."""
        m = _i()
        result = m.gompertz_N(K, ALPHA, N0, 0)
        assert math.isclose(result, N0, rel_tol=1e-6), f"N(0)={result}, expected {N0}"

    def test_N_at_t20(self):
        m = _i()
        result = m.gompertz_N(K, ALPHA, N0, 20)
        assert math.isclose(result, N_20, rel_tol=1e-4), f"N(20)={result:.4f}, expected {N_20:.4f}"

    def test_N_at_t50(self):
        m = _i()
        result = m.gompertz_N(K, ALPHA, N0, 50)
        assert math.isclose(result, N_50, rel_tol=1e-4), f"N(50)={result:.4f}, expected {N_50:.4f}"

    def test_inflection_value(self):
        m = _i()
        infl = m.gompertz_inflection(K)
        assert math.isclose(infl, K / math.e, rel_tol=1e-9), (
            f"Inflection={infl:.4f}, expected K/e={K/math.e:.4f}"
        )

    def test_approaches_K(self):
        """N(t) must approach K as t → ∞."""
        m = _i()
        result = m.gompertz_N(K, ALPHA, N0, 1000)
        assert math.isclose(result, K, rel_tol=1e-6), f"N(1000)={result:.4f}, expected ~{K}"

    def test_growth_rate_zero_at_K(self):
        """dN/dt = 0 when N = K (carrying capacity)."""
        m = _i()
        rate = m.gompertz_dNdt(ALPHA, K, K)
        assert math.isclose(rate, 0.0, abs_tol=1e-12), f"dN/dt at K should be 0, got {rate}"

    def test_growth_rate_max_at_inflection(self):
        """dN/dt is maximal at N = K/e."""
        m = _i()
        rate_infl = m.gompertz_dNdt(ALPHA, K, INFLECTION_N)
        # Check nearby points have lower rate
        for offset in [-50, -10, 10, 50]:
            N_nearby = INFLECTION_N + offset
            if 0 < N_nearby < K:
                rate_nearby = m.gompertz_dNdt(ALPHA, K, N_nearby)
                assert rate_infl >= rate_nearby, (
                    f"Rate at inflection ({rate_infl:.4f}) should be >= rate at "
                    f"N={N_nearby:.1f} ({rate_nearby:.4f})"
                )
