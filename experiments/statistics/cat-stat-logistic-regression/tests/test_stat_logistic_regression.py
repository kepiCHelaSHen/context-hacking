"""cat-stat-logistic-regression — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_logistic_regression_constants import *
IMPL = Path(__file__).parent.parent / "stat_logistic_regression.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_or_is_not_probability_ratio(self):
        """OR = e^beta != P(x+1)/P(x).  They must differ — confusing them is the #1 LLM error."""
        m = _i()
        p3 = m.predict_prob(BETA0, BETA1, 3)
        p4 = m.predict_prob(BETA0, BETA1, 4)
        prob_ratio = p4 / p3                     # ~1.3238  (probability ratio)
        or_value = m.odds_ratio(BETA1)           # ~1.6487  (odds ratio)
        # They must NOT be equal — confusing them is the key error
        assert abs(prob_ratio - or_value) > 0.1, (
            f"Probability ratio ({prob_ratio:.4f}) should differ from "
            f"odds ratio ({or_value:.4f}) — they are fundamentally different quantities"
        )
        # The odds ratio must match e^beta1
        assert abs(or_value - ODDS_RATIO) < 1e-10, (
            f"OR={or_value}, expected e^beta1={ODDS_RATIO}"
        )

    def test_beta_is_not_probability_change(self):
        """beta1 is NOT the probability change per unit x — probability is non-linear."""
        m = _i()
        # If beta1 were the probability change, then P(x+1) - P(x) would equal beta1
        # everywhere.  Show it doesn't.
        diffs = []
        for x in range(0, 6):
            p_curr = m.predict_prob(BETA0, BETA1, x)
            p_next = m.predict_prob(BETA0, BETA1, x + 1)
            diffs.append(p_next - p_curr)
        # All differences should be different from each other (non-constant)
        assert max(diffs) - min(diffs) > 0.01, (
            f"Probability differences {diffs} look constant — "
            f"logistic probability is non-linear, diffs must vary"
        )
        # None of the diffs should equal beta1
        for d in diffs:
            assert abs(d - BETA1) > 0.01, (
                f"Probability diff {d:.4f} ≈ beta1={BETA1} — "
                f"beta1 is NOT the probability change per unit x"
            )


class TestCorrectness:
    def test_logistic_at_z_zero(self):
        """logistic(0) must equal exactly 0.5."""
        m = _i()
        assert m.logistic(0) == 0.5

    def test_predict_prob_at_x3(self):
        """predict_prob(beta0, beta1, 3) must match frozen P_AT_X3."""
        m = _i()
        p = m.predict_prob(BETA0, BETA1, 3)
        assert abs(p - P_AT_X3) < 1e-12, f"p={p}, expected {P_AT_X3}"

    def test_predict_prob_at_x4(self):
        """predict_prob(beta0, beta1, 4) must equal 0.5 (z=0)."""
        m = _i()
        p = m.predict_prob(BETA0, BETA1, 4)
        assert abs(p - 0.5) < 1e-12, f"p={p}, expected 0.5"

    def test_odds_at_x3(self):
        """odds(P_AT_X3) must match frozen ODDS_AT_X3."""
        m = _i()
        o = m.odds(P_AT_X3)
        assert abs(o - ODDS_AT_X3) < 1e-12, f"odds={o}, expected {ODDS_AT_X3}"

    def test_odds_ratio_matches_frozen(self):
        """odds_ratio(beta1) must equal e^beta1 = frozen ODDS_RATIO."""
        m = _i()
        or_val = m.odds_ratio(BETA1)
        assert abs(or_val - ODDS_RATIO) < 1e-12, (
            f"OR={or_val}, expected {ODDS_RATIO}"
        )

    def test_odds_ratio_from_adjacent_x(self):
        """Verify OR = odds(x+1) / odds(x) for any x."""
        m = _i()
        for x in [0, 1, 2, 3, 4, 5]:
            o_curr = m.odds(m.predict_prob(BETA0, BETA1, x))
            o_next = m.odds(m.predict_prob(BETA0, BETA1, x + 1))
            computed_or = o_next / o_curr
            assert abs(computed_or - ODDS_RATIO) < 1e-10, (
                f"At x={x}: odds ratio = {computed_or}, expected {ODDS_RATIO}"
            )

    def test_log_odds_equals_z(self):
        """log_odds(p) must equal the linear predictor z = beta0 + beta1*x."""
        m = _i()
        for x in [1, 2, 3, 4, 5]:
            p = m.predict_prob(BETA0, BETA1, x)
            lo = m.log_odds(p)
            z = BETA0 + BETA1 * x
            assert abs(lo - z) < 1e-10, (
                f"At x={x}: log_odds={lo}, expected z={z}"
            )
