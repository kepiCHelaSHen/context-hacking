"""cat-econ-solow-model — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_solow_model_constants import *
IMPL = Path(__file__).parent.parent / "econ_solow_model.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_uses_n_plus_delta_not_just_delta(self):
        """PRIOR_ERROR: only_depreciation — denominator must be (n+delta), not delta alone."""
        m = _i()
        k_correct = m.steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
        k_wrong_delta_only = (S_TEST / DELTA_TEST) ** (1 / (1 - ALPHA_TEST))
        # Correct result must differ substantially from the delta-only mistake
        assert abs(k_correct - K_STAR) < 0.001
        assert abs(k_correct - k_wrong_delta_only) > 1.0  # big gap proves n is included

    def test_golden_rule_uses_mpk_condition(self):
        """PRIOR_ERROR: golden_rule_s — golden rule comes from MPK=n+delta, not s=alpha."""
        m = _i()
        k_g = m.golden_rule_k(ALPHA_TEST, N_TEST, DELTA_TEST)
        # Verify MPK = n + delta at golden rule
        mpk_at_gold = ALPHA_TEST * k_g ** (ALPHA_TEST - 1)
        assert abs(mpk_at_gold - N_PLUS_DELTA) < 1e-9

    def test_steady_state_formula_exponent(self):
        """PRIOR_ERROR: steady_state_formula — exponent is 1/(1-alpha), not 1/alpha."""
        m = _i()
        k_correct = m.steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
        k_wrong_exp = (S_TEST / N_PLUS_DELTA) ** (1 / ALPHA_TEST)  # wrong exponent
        assert abs(k_correct - K_STAR) < 0.001
        assert abs(k_correct - k_wrong_exp) > 1.0  # wrong exponent gives very different answer


class TestCorrectness:
    def test_steady_state_k(self):
        """k* = (s/(n+delta))^(1/(1-alpha)) with test parameters."""
        m = _i()
        k = m.steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
        assert abs(k - K_STAR) < 1e-6

    def test_steady_state_y(self):
        """y* = k*^alpha."""
        m = _i()
        y = m.steady_state_y(K_STAR, ALPHA_TEST)
        assert abs(y - Y_STAR) < 1e-6

    def test_steady_state_condition_holds(self):
        """At k*, actual investment equals break-even investment."""
        m = _i()
        k = m.steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
        ai = m.actual_investment(S_TEST, k, ALPHA_TEST)
        bei = m.break_even_investment(N_TEST, DELTA_TEST, k)
        assert abs(ai - bei) < 1e-9

    def test_golden_rule_k(self):
        """k_gold = (alpha/(n+delta))^(1/(1-alpha))."""
        m = _i()
        k_g = m.golden_rule_k(ALPHA_TEST, N_TEST, DELTA_TEST)
        assert abs(k_g - K_GOLD) < 1e-6

    def test_break_even_investment(self):
        """(n+delta)*k at steady state."""
        m = _i()
        bei = m.break_even_investment(N_TEST, DELTA_TEST, K_STAR)
        assert abs(bei - BREAK_EVEN_STAR) < 1e-6

    def test_actual_investment(self):
        """s*k^alpha at steady state."""
        m = _i()
        ai = m.actual_investment(S_TEST, K_STAR, ALPHA_TEST)
        assert abs(ai - ACTUAL_INV_STAR) < 1e-6

    def test_capital_accumulates_below_steady_state(self):
        """Below k*, actual investment > break-even => k_dot > 0."""
        m = _i()
        ai = m.actual_investment(S_TEST, K_LOW, ALPHA_TEST)
        bei = m.break_even_investment(N_TEST, DELTA_TEST, K_LOW)
        assert ai > bei

    def test_capital_decumulates_above_steady_state(self):
        """Above k*, actual investment < break-even => k_dot < 0."""
        m = _i()
        ai = m.actual_investment(S_TEST, K_HIGH, ALPHA_TEST)
        bei = m.break_even_investment(N_TEST, DELTA_TEST, K_HIGH)
        assert ai < bei

    def test_wrong_delta_only_overestimates(self):
        """Using only delta gives k* ~65.7% too high."""
        m = _i()
        k_correct = m.steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
        k_wrong = m.steady_state_k(S_TEST, 0, DELTA_TEST, ALPHA_TEST)  # n=0 simulates mistake
        error_pct = (k_wrong - k_correct) / k_correct * 100
        assert abs(error_pct - K_STAR_ERROR_PCT) < 0.1

    def test_golden_rule_savings_rate(self):
        """For Cobb-Douglas, golden rule savings rate is alpha."""
        m = _i()
        # At golden rule: s_gold * k_gold^alpha = (n+delta) * k_gold
        # => s_gold = (n+delta) * k_gold^(1-alpha) = alpha (for Cobb-Douglas)
        k_g = m.golden_rule_k(ALPHA_TEST, N_TEST, DELTA_TEST)
        s_gold = N_PLUS_DELTA * k_g ** (1 - ALPHA_TEST) / (k_g ** ALPHA_TEST) * k_g ** ALPHA_TEST
        # Simplify: s_gold = (n+delta) * k_gold / k_gold^alpha = (n+delta) * k_gold^(1-alpha)
        s_gold = N_PLUS_DELTA * k_g ** (1 - ALPHA_TEST)
        assert abs(s_gold - S_GOLD) < 1e-9
