"""cat-bio-hodgkin-huxley — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_hodgkin_huxley_constants import *
IMPL = Path(__file__).parent.parent / "bio_hodgkin_huxley.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_na_current_uses_m3h_not_m3(self):
        """Na current MUST include inactivation gate h: g_Na * m^3 * h * (V - E_Na).
        A common LLM error is omitting h entirely (no_inactivation)."""
        m = _i()
        # Compute with h (correct)
        correct = m.i_na(G_NA, M_REST, H_REST, V_REST, E_NA)
        # Compute what you'd get without h (wrong: effectively h=1)
        wrong_no_h = G_NA * M_REST**3 * 1.0 * (V_REST - E_NA)
        assert not math.isclose(correct, wrong_no_h, rel_tol=1e-3), \
            "i_na must depend on h — got same result as if h were absent"
        # Verify correct value matches frozen reference
        assert math.isclose(correct, I_NA_REST, rel_tol=1e-9), \
            f"i_na={correct}, expected {I_NA_REST}"

    def test_k_current_uses_n4_not_n3(self):
        """K current MUST use n^4 not n^3: g_K * n^4 * (V - E_K).
        A common LLM error is using n^3 (n_cubed_not_fourth)."""
        m = _i()
        correct = m.i_k(G_K, N_REST, V_REST, E_K)
        wrong_n3 = G_K * N_REST**3 * (V_REST - E_K)
        assert not math.isclose(correct, wrong_n3, rel_tol=1e-3), \
            "i_k must use n^4 — got same result as n^3"
        assert math.isclose(correct, I_K_REST, rel_tol=1e-9), \
            f"i_k={correct}, expected {I_K_REST}"

    def test_m_rises_h_falls_not_confused(self):
        """m (activation) should INCREASE channel current when it rises.
        h (inactivation) should DECREASE channel current when it falls.
        A common LLM error is confusing which does what (m_h_confusion)."""
        m = _i()
        baseline = m.i_na(G_NA, M_REST, H_REST, V_REST, E_NA)
        # Increase m → current magnitude should increase (more negative)
        higher_m = m.i_na(G_NA, M_REST * 2, H_REST, V_REST, E_NA)
        assert abs(higher_m) > abs(baseline), \
            "Increasing m should increase |I_Na| (m is activation)"
        # Decrease h → current magnitude should decrease (less negative)
        lower_h = m.i_na(G_NA, M_REST, H_REST * 0.5, V_REST, E_NA)
        assert abs(lower_h) < abs(baseline), \
            "Decreasing h should decrease |I_Na| (h is inactivation)"


class TestCorrectness:
    def test_reversal_potential_signs(self):
        """E_Na must be positive, E_K must be negative."""
        assert E_NA > 0, f"E_Na should be positive, got {E_NA}"
        assert E_K < 0, f"E_K should be negative, got {E_K}"

    def test_na_current_at_rest(self):
        m = _i()
        result = m.i_na(G_NA, M_REST, H_REST, V_REST, E_NA)
        assert math.isclose(result, I_NA_REST, rel_tol=1e-9), \
            f"I_Na at rest: {result}, expected {I_NA_REST}"
        assert result < 0, "I_Na at rest should be inward (negative)"

    def test_k_current_at_rest(self):
        m = _i()
        result = m.i_k(G_K, N_REST, V_REST, E_K)
        assert math.isclose(result, I_K_REST, rel_tol=1e-9), \
            f"I_K at rest: {result}, expected {I_K_REST}"
        assert result > 0, "I_K at rest should be outward (positive)"

    def test_leak_current_at_rest(self):
        m = _i()
        result = m.i_leak(G_L, V_REST, E_L)
        assert math.isclose(result, I_L_REST, rel_tol=1e-9), \
            f"I_L at rest: {result}, expected {I_L_REST}"

    def test_total_current_at_rest(self):
        m = _i()
        result = m.total_ionic_current(
            G_NA, M_REST, H_REST, V_REST, E_NA,
            G_K, N_REST, E_K, G_L, E_L)
        assert math.isclose(result, I_TOTAL_REST, rel_tol=1e-9), \
            f"I_total at rest: {result}, expected {I_TOTAL_REST}"

    def test_current_at_reversal_potential(self):
        """At V = E_X, the current through that channel is zero."""
        m = _i()
        assert m.i_na(G_NA, M_REST, H_REST, E_NA, E_NA) == 0.0, \
            "I_Na should be zero when V = E_Na"
        assert m.i_k(G_K, N_REST, E_K, E_K) == 0.0, \
            "I_K should be zero when V = E_K"
        assert m.i_leak(G_L, E_L, E_L) == 0.0, \
            "I_L should be zero when V = E_L"

    def test_total_is_sum_of_components(self):
        """Total current must equal the sum of Na + K + leak."""
        m = _i()
        V_test = -40.0
        m_val, h_val, n_val = 0.3, 0.4, 0.5
        na = m.i_na(G_NA, m_val, h_val, V_test, E_NA)
        k  = m.i_k(G_K, n_val, V_test, E_K)
        lk = m.i_leak(G_L, V_test, E_L)
        total = m.total_ionic_current(
            G_NA, m_val, h_val, V_test, E_NA,
            G_K, n_val, E_K, G_L, E_L)
        assert math.isclose(total, na + k + lk, rel_tol=1e-12), \
            f"total={total}, sum={na + k + lk}"
